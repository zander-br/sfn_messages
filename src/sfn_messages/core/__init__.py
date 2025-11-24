import re
from importlib import import_module
from typing import Any, cast

from .errors import MessageCodeNotFoundError, MessageNotImplementedError
from .models import BaseMessage

MESSAGE_CODE_TAG_RE = re.compile(r'<CodMsg>(?P<message_code>.*?)</CodMsg>')
MESSAGE_CODE_RE = re.compile(r'^(?P<event>(?P<service>[A-Za-z]{3})[0-9]{4}).*$')


def get_message_code(xml: str, /) -> str:
    result = MESSAGE_CODE_TAG_RE.search(xml)
    if result is None:
        raise MessageCodeNotFoundError
    return result.group('message_code')


def load_message_class(message_code: str, /) -> type[BaseMessage]:
    parts = MESSAGE_CODE_RE.match(message_code)
    if parts is None:
        raise ValueError
    service = parts.group('service').lower()
    event = parts.group('event').lower()
    package_name = f'sfn_messages.{service}.{event}'
    try:
        klass = cast('type[BaseMessage]', getattr(import_module(package_name), message_code))
    except (ModuleNotFoundError, AttributeError):
        raise MessageNotImplementedError(message_code=message_code) from None
    return klass


def to_xml(message_code: str, msg: dict[Any, Any], /) -> str:
    klass = load_message_class(message_code)
    module = klass.model_validate(msg)
    return module.to_xml()


def from_xml(xml: str, /) -> BaseMessage:
    message_code = get_message_code(xml)
    klass = load_message_class(message_code)
    return klass.from_xml(xml)
