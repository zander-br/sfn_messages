from datetime import date, datetime
from typing import Annotated, Literal

from sfn_messages.core.models import BaseMessage, XmlPath
from sfn_messages.core.types import Description, InstitutionControlNumber, Ispb

from .types import CertificateIssue, CertificateSerialNumber


class GEN0006(BaseMessage):
    message_code: Annotated[Literal['GEN0006'], XmlPath('DOC/SISMSG/GEN0006/CodMsg/text()')] = 'GEN0006'
    institution_control_number: Annotated[InstitutionControlNumber, XmlPath('DOC/SISMSG/GEN0006/NumCtrlIF/text()')]
    institution_ispb: Annotated[Ispb, XmlPath('DOC/SISMSG/GEN0006/ISPBIF/text()')]
    certificate_issue: Annotated[CertificateIssue, XmlPath('DOC/SISMSG/GEN0006/CodCertifrAtv/text()')]
    certificate_serial_number: Annotated[CertificateSerialNumber, XmlPath('DOC/SISMSG/GEN0006/CertifAtv/text()')]
    description: Annotated[Description | None, XmlPath('DOC/SISMSG/GEN0006/Hist/text()')] = None
    settlement_date: Annotated[date, XmlPath('DOC/SISMSG/GEN0006/DtMovto/text()')]


class GEN0006R1(BaseMessage):
    message_code: Annotated[Literal['GEN0006R1'], XmlPath('DOC/SISMSG/GEN0006R1/CodMsg/text()')] = 'GEN0006R1'
    institution_control_number: Annotated[InstitutionControlNumber, XmlPath('DOC/SISMSG/GEN0006R1/NumCtrlIF/text()')]
    institution_ispb: Annotated[Ispb, XmlPath('DOC/SISMSG/GEN0006R1/ISPBIF/text()')]
    provider_timestamp: Annotated[datetime, XmlPath('DOC/SISMSG/GEN0006R1/DtHrBC/text()')]
    settlement_date: Annotated[date, XmlPath('DOC/SISMSG/GEN0006R1/DtMovto/text()')]
