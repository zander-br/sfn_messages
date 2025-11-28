from datetime import date, datetime
from typing import Annotated, ClassVar, Literal

from sfn_messages.core.models import BaseMessage, XmlPath
from sfn_messages.core.types import Description, InstitutionControlNumber, Ispb

from .types import CertificateIssue, CertificateSerialNumber

PATH = 'DOC/SISMSG/GEN0006'
PATH_R1 = 'DOC/SISMSG/GEN0006R1'
XML_NAMESPACE = 'http://www.bcb.gov.br/GEN/GEN0006.xsd'


class GEN0006(BaseMessage):
    XML_NAMESPACE: ClassVar[str | None] = XML_NAMESPACE

    message_code: Annotated[Literal['GEN0006'], XmlPath(f'{PATH}/CodMsg/text()')] = 'GEN0006'
    institution_control_number: Annotated[InstitutionControlNumber, XmlPath(f'{PATH}/NumCtrlIF/text()')]
    institution_ispb: Annotated[Ispb, XmlPath(f'{PATH}/ISPBIF/text()')]
    certificate_issue: Annotated[CertificateIssue, XmlPath(f'{PATH}/CodCertifrAtv/text()')]
    certificate_serial_number: Annotated[CertificateSerialNumber, XmlPath(f'{PATH}/CertifAtv/text()')]
    description: Annotated[Description | None, XmlPath(f'{PATH}/Hist/text()')] = None
    settlement_date: Annotated[date, XmlPath(f'{PATH}/DtMovto/text()')]


class GEN0006R1(BaseMessage):
    XML_NAMESPACE: ClassVar[str | None] = XML_NAMESPACE
    message_code: Annotated[Literal['GEN0006R1'], XmlPath(f'{PATH_R1}/CodMsg/text()')] = 'GEN0006R1'
    institution_control_number: Annotated[InstitutionControlNumber, XmlPath(f'{PATH_R1}/NumCtrlIF/text()')]
    institution_ispb: Annotated[Ispb, XmlPath(f'{PATH_R1}/ISPBIF/text()')]
    vendor_timestamp: Annotated[datetime, XmlPath(f'{PATH_R1}/DtHrBC/text()')]
    settlement_date: Annotated[date, XmlPath(f'{PATH_R1}/DtMovto/text()')]
