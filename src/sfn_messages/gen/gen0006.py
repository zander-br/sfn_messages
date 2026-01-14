from datetime import date, datetime
from typing import Annotated, ClassVar, Literal

from sfn_messages.core.models import BaseMessage, XmlPath
from sfn_messages.core.types import Description, ErrorCode, InstitutionControlNumber, Ispb

from .types import CertificateIssue, CertificateSerialNumber

PATH = 'DOC/SISMSG/GEN0006'
PATH_R1 = 'DOC/SISMSG/GEN0006R1'
PATH_E = 'DOC/SISMSG/GEN0006E'
XML_NAMESPACE = 'http://www.bcb.gov.br/GEN/GEN0006.xsd'
XML_NAMESPACE_ERROR = 'http://www.bcb.gov.br/GEN/GEN0006E.xsd'


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


class GEN0006E(BaseMessage):
    XML_NAMESPACE: ClassVar[str | None] = XML_NAMESPACE_ERROR

    message_code: Annotated[Literal['GEN0006'], XmlPath(f'{PATH_E}/CodMsg/text()')] = 'GEN0006'
    institution_control_number: Annotated[InstitutionControlNumber, XmlPath(f'{PATH_E}/NumCtrlIF/text()')]
    institution_ispb: Annotated[Ispb, XmlPath(f'{PATH_E}/ISPBIF/text()')]
    certificate_issue: Annotated[CertificateIssue, XmlPath(f'{PATH_E}/CodCertifrAtv/text()')]
    certificate_serial_number: Annotated[CertificateSerialNumber, XmlPath(f'{PATH_E}/CertifAtv/text()')]
    description: Annotated[Description | None, XmlPath(f'{PATH_E}/Hist/text()')] = None
    settlement_date: Annotated[date, XmlPath(f'{PATH_E}/DtMovto/text()')]

    general_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH_E}/@CodErro')] = None
    institution_control_number_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH_E}/NumCtrlIF/@CodErro')] = None
    institution_ispb_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH_E}/ISPBIF/@CodErro')] = None
    certificate_issue_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH_E}/CodCertifrAtv/@CodErro')] = None
    certificate_serial_number_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH_E}/CertifAtv/@CodErro')] = None
    description_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH_E}/Hist/@CodErro')] = None
    settlement_date_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH_E}/DtMovto/@CodErro')] = None
