from __future__ import annotations

import re
from typing import Any

from sfn_messages.core.base_message import BaseMessage
from sfn_messages.core.registry import resolve


def from_xml(xml: str) -> BaseMessage:
    pattern = r'<CodMsg>(.*?)</CodMsg>'
    match = re.search(pattern, xml)
    if not match:
        raise ValueError('Message code not found in XML')

    message_code = match.group(1).strip().upper()
    cls: type[BaseMessage] = resolve(message_code, None)
    return cls.from_xml(xml)


def to_xml(data: dict[str, Any], message_code: str, version: str | None = None) -> str:
    normalized_code = message_code.replace('.', '').upper()
    cls: type[BaseMessage] = resolve(normalized_code, version)
    message = cls.model_validate(data)
    return message.to_xml()
