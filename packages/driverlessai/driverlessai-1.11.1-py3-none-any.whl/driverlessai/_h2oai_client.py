import functools
import importlib
import importlib.util
import inspect
import re
import sys
import time
from pathlib import Path
from types import ModuleType
from typing import Any, Callable, Optional

from driverlessai import _logging, _server


def ignore_unexpected_kwargs(func: Callable) -> Callable:
    """Ignores passed kwargs to a function that are not function parameters."""

    @functools.wraps(func)
    def _wrapper(*args: Any, **kwargs: Any) -> Any:
        function_params = inspect.signature(func).parameters.keys()
        filtered_kwargs = {}
        for k, v in kwargs.items():
            if k in function_params:
                filtered_kwargs[k] = v
            else:
                _logging.logger.debug(
                    f"Parameter '{k}={v}' is ignored from "
                    f"function '{func.__qualname__}'. {function_params}"
                )
        return func(*args, **filtered_kwargs)

    return _wrapper


def apply_decorator_to_methods(
    decorator: Callable,
    include_regex: Optional[str] = None,
    exclude_regex: Optional[str] = None,
) -> Callable:
    """
    Applies the given decorator to all methods in a class.

    Args:
        decorator: the decorator to be applied
        include_regex: regular expression that will be matched with method names and
            included if so
        exclude_regex: regular expression that will be matched with method named and
            excluded from applying the decorator
    """

    def _wrapper(cls: type) -> type:
        methods = inspect.getmembers(
            cls,
            predicate=lambda m: inspect.isfunction(m) and not inspect.isbuiltin(m),
        )
        if include_regex:
            include_pattern = re.compile(include_regex)
            methods = [i for i in methods if include_pattern.match(i[0])]
        if exclude_regex:
            exclude_pattern = re.compile(exclude_regex)
            methods = [i for i in methods if not exclude_pattern.match(i[0])]
        for name, fn in methods:
            _logging.logger.debug(
                f"Applying decorator '{decorator.__name__}' "
                f"to method '{cls.__name__}.{name}'."
            )
            setattr(cls, name, decorator(fn))
        return cls

    return _wrapper


H2OAI_CLIENT_MODEL_NAME = "h2oai_client"


def _load_h2oai_client_module(module_version: str) -> Optional[ModuleType]:
    module_path = (
        Path(__file__).parent.absolute()
        / f"_{H2OAI_CLIENT_MODEL_NAME}_{module_version.replace('.', '_')}"
        / "__init__.py"
    )
    if not module_path.exists():
        return None

    spec = importlib.util.spec_from_file_location(H2OAI_CLIENT_MODEL_NAME, module_path)
    if not spec:
        raise ImportError(
            f"Couldn't load module '{H2OAI_CLIENT_MODEL_NAME}' from '{module_path}'."
        )
    module = importlib.util.module_from_spec(spec)
    sys.modules[H2OAI_CLIENT_MODEL_NAME] = module
    spec.loader.exec_module(module)
    return module


def _patch_messages_classes(h2oai_client_module: ModuleType) -> None:
    references_sub_module = h2oai_client_module.references
    messages_sub_module = h2oai_client_module.messages
    for name, cls in inspect.getmembers(messages_sub_module, predicate=inspect.isclass):
        if hasattr(references_sub_module, name):
            _logging.logger.debug(
                f"Class h2oai_client.messages.{name} is imported from "
                f"h2oai_client.references submodule. Hence skipping from "
                f"applying the 'ignore_unexpected_kwargs' decorator."
            )
            continue
        setattr(
            messages_sub_module,
            name,
            apply_decorator_to_methods(
                ignore_unexpected_kwargs,
                include_regex="^__init__$",
            )(cls),
        )


def get_h2oai_client_module_for(server_version: str) -> ModuleType:
    """
    Returns the `h2oai_client` for a given Driverless AI server version.

    Args:
        server_version: Driverless AI server version

    Returns:
        The `h2oai_client` module.
    """
    if H2OAI_CLIENT_MODEL_NAME in sys.modules:
        _logging.logger.debug(f"Module '{H2OAI_CLIENT_MODEL_NAME}' is already loaded.")
        h2oai_client_module = sys.modules[H2OAI_CLIENT_MODEL_NAME]
        return h2oai_client_module

    h2oai_client_module = _load_h2oai_client_module(server_version)
    if not h2oai_client_module:
        dai_version = _server.Version(server_version)
        compatible_module_versions = [
            f"{dai_version.major}.{dai_version.minor}.{dai_version.micro}.{i}"
            for i in reversed(range(1, dai_version.patch))
        ]
        _logging.logger.debug(
            f"Couldn't find the exact '{H2OAI_CLIENT_MODEL_NAME}' module version "
            f"for server version '{server_version}'. "
            f"Searching in compatible versions {compatible_module_versions}."
        )
        for module_version in compatible_module_versions:
            h2oai_client_module = _load_h2oai_client_module(module_version)
            if h2oai_client_module:
                _logging.logger.info(
                    f"Found matching '{H2OAI_CLIENT_MODEL_NAME}' "
                    f"module version '{module_version}' for "
                    f"server version '{server_version}'."
                )
                break

    if not h2oai_client_module:
        raise ModuleNotFoundError(
            f"Cannot find a matching '{H2OAI_CLIENT_MODEL_NAME}' "
            f"module for server version '{server_version}'."
        )

    _patch_messages_classes(h2oai_client_module)
    _add_patched_client_class(h2oai_client_module)
    return h2oai_client_module


def _add_patched_client_class(h2oai_client_module: ModuleType) -> None:
    import json
    import requests
    from urllib3.util.retry import Retry

    Client: type = h2oai_client_module.protocol.Client
    RequestError: type = h2oai_client_module.protocol.RequestError
    RemoteError: type = h2oai_client_module.protocol.RemoteError

    @apply_decorator_to_methods(ignore_unexpected_kwargs, exclude_regex="^_+")
    class PatchedClient(Client):
        def __init__(
            self,
            address: str,
            username: Optional[str] = None,
            password: Optional[str] = None,
            verify: bool = True,
            cert: str = None,
            authentication_method: Optional[str] = None,
            *args: Any,
            token_provider: Callable[[], str] = None,
        ) -> None:
            super().__init__(
                address=address,
                username=username,
                password=password,
                verify=verify,
                cert=cert,
                authentication_method=authentication_method,
                *args,
                token_provider=token_provider,
            )

            retries = Retry(
                total=5,
                backoff_factor=0.2,
                status_forcelist=[403, 500, 502, 503, 504],
                allowed_methods=["POST"],
            )
            self._session.mount(
                "http://", requests.adapters.HTTPAdapter(max_retries=retries)
            )
            self._session.mount(
                "https://", requests.adapters.HTTPAdapter(max_retries=retries)
            )

        def _request(self, method: str, params: dict) -> Any:
            self._cid = self._cid + 1  # type: ignore
            req = json.dumps(dict(id=self._cid, method="api_" + method, params=params))
            max_retires = 5
            for i in range(max_retires):
                res = self._session.post(
                    self.address + "/rpc",
                    data=req,
                    headers=self._get_authorization_headers(),
                )
                if (not res.url.endswith("/rpc")) and ("login" in res.url):
                    # exponential backoff sleep time
                    sleep_time = 2 * (i + 1)
                    retry_message = (
                        f"RPC call to '{method}' responded with '{res.url}' URL "
                        f"and {res.status_code} status. "
                        f"Retrying ... {i + 1}/{max_retires}"
                    )
                    _logging.logger.debug(retry_message)
                    time.sleep(sleep_time)
                else:
                    break
            try:
                res.raise_for_status()
            except requests.HTTPError as e:
                msg = f"Driverless AI server responded with {res.status_code}."
                _logging.logger.error(f"[ERROR] {msg}\n\n{res.content}")
                raise RequestError(msg) from e

            try:
                response = res.json()
            except json.JSONDecodeError as e:
                msg = "Driverless AI server response is not a valid JSON."
                _logging.logger.error(f"[ERROR] {msg}\n\n{res.content}")
                raise RequestError(msg) from e

            if "error" in response:
                raise RemoteError(response["error"])

            return response["result"]

    setattr(h2oai_client_module, "PatchedClient", PatchedClient)
