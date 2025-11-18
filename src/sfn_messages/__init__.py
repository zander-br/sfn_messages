import re
from typing import TYPE_CHECKING, Any

from sfn_messages.core.errors import InvalidMessageCodeError
from sfn_messages.core.registry import resolve

if TYPE_CHECKING:
    from sfn_messages.core.base_message import BaseMessage


def from_xml(xml: str) -> BaseMessage:
    pattern = r'<CodMsg>(.*?)</CodMsg>'
    match = re.search(pattern, xml)
    if not match:
        raise InvalidMessageCodeError

    message_code = match.group(1).strip().upper()
    cls = resolve(message_code, None)
    return cls.from_xml(xml)


def to_xml(data: dict[str, Any], message_code: str, version: str | None = None) -> str:
    normalized_code = message_code.replace('.', '').upper()
    cls = resolve(normalized_code, version)
    message = cls.model_validate(data)
    return message.to_xml()
