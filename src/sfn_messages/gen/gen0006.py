from datetime import date
from typing import Annotated, Literal

from sfn_messages.core.models import BaseMessage, XmlPath
from sfn_messages.core.types import CertificateIssue, Ispb


class GEN0006(BaseMessage):
    message_code: Annotated[Literal['GEN0006'], XmlPath('DOC/SISMSG/GEN0006/CodMsg/text()')] = 'GEN0006'
    internal_control_number: Annotated[str, XmlPath('DOC/SISMSG/GEN0006/NumCtrlIF/text()')]
    internal_ispb: Annotated[Ispb, XmlPath('DOC/SISMSG/GEN0006/ISPBIF/text()')]
    certificate_issue: Annotated[CertificateIssue, XmlPath('DOC/SISMSG/GEN0006/CodCertifrAtv/text()')]
    certificate_serial_number: Annotated[str, XmlPath('DOC/SISMSG/GEN0006/CertifAtv/text()')]
    description: Annotated[str | None, XmlPath('DOC/SISMSG/GEN0006/Hist/text()')] = None
    settlement_date: Annotated[date, XmlPath('DOC/SISMSG/GEN0006/DtMovto/text()')]
