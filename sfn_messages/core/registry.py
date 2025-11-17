from __future__ import annotations

import importlib
from sfn_messages.core.errors import MessageNotImplementedError

MESSAGE_REGISTRY: dict[tuple[str, str], type] = {}
DEFAULT_VERSION: dict[str, str] = {}


def register(message_code: str, version: str, cls: type) -> None:
    MESSAGE_REGISTRY[(message_code, version)] = cls
    DEFAULT_VERSION.setdefault(message_code, version)


def _auto_import(message_code: str, version: str | None) -> None:
    system = message_code[:3].lower()
    code = message_code.lower()

    if version is None:
        module_name = f'sfn_messages.{system}.{code}.default'
    else:
        ver_suffix = version.replace('.', '')
        module_name = f'sfn_messages.{system}.{code}.v{ver_suffix}'

    try:
        importlib.import_module(module_name)
    except ModuleNotFoundError:
        return


def resolve(message_code: str, version: str | None):
    message_code = message_code.upper()
    _auto_import(message_code, version)

    if version is None:
        if message_code not in DEFAULT_VERSION:
            raise MessageNotImplementedError(f'{message_code} does not have a default version.')
        version = DEFAULT_VERSION[message_code]

    key = (message_code, version)

    if key not in MESSAGE_REGISTRY:
        _auto_import(message_code, version)
        if key not in MESSAGE_REGISTRY:
            raise MessageNotImplementedError(f'{message_code} version {version} is not implemented.')

    return MESSAGE_REGISTRY[key]
