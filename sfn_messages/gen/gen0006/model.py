from datetime import date, datetime

from sfn_messages.core.base_message import BaseMessage
from sfn_messages.gen.gen0006.enums import CertificateIssue, MessageCode


class GEN0006(BaseMessage):
    message_code: MessageCode = MessageCode.GEN0006
    internal_control_number: str
    settlement_date: date
    internal_ispb: str
    certificate_issue: CertificateIssue | None = None
    certificate_serial_number: str | None = None
    version: str | None = None
    provider_timestamp: datetime | None = None
    description: str | None = None
