from datetime import date, datetime
from typing import Annotated, ClassVar, Literal

from sfn_messages.core.models import BaseMessage, XmlPath
from sfn_messages.core.types import ErrorCode, Ispb

from .types import Certificate, CertificateIssue, CertificateSerialNumber

PATH = 'DOC/SISMSG/GEN0007'
PATH_E = 'DOC/SISMSG/GEN0007E'
XML_NAMESPACE = 'http://www.bcb.gov.br/GEN/GEN0007.xsd'
XML_NAMESPACE_ERROR = 'http://www.bcb.gov.br/GEN/GEN0007E.xsd'


class GEN0007(BaseMessage):
    XML_NAMESPACE: ClassVar[str | None] = XML_NAMESPACE

    message_code: Annotated[Literal['GEN0007'], XmlPath(f'{PATH}/CodMsg/text()')] = 'GEN0007'
    instituition_certificate: Annotated[Ispb, XmlPath(f'{PATH}/ISPBIFCertif/text()')]
    certificate: Annotated[Certificate, XmlPath(f'{PATH}/CertifDig/text()')]
    certificate_issue: Annotated[CertificateIssue, XmlPath(f'{PATH}/CodCertifrAtv/text()')]
    certificate_serial_number: Annotated[CertificateSerialNumber, XmlPath(f'{PATH}/CertifAtv/text()')]
    vendor_timestamp: Annotated[datetime, XmlPath(f'{PATH}/DtHrBC/text()')]
    settlement_date: Annotated[date, XmlPath(f'{PATH}/DtMovto/text()')]


class GEN0007E(BaseMessage):
    XML_NAMESPACE: ClassVar[str | None] = XML_NAMESPACE_ERROR

    message_code: Annotated[Literal['GEN0007'], XmlPath(f'{PATH_E}/CodMsg/text()')] = 'GEN0007'
    instituition_certificate: Annotated[Ispb, XmlPath(f'{PATH_E}/ISPBIFCertif/text()')]
    certificate: Annotated[Certificate, XmlPath(f'{PATH_E}/CertifDig/text()')]
    certificate_issue: Annotated[CertificateIssue, XmlPath(f'{PATH_E}/CodCertifrAtv/text()')]
    certificate_serial_number: Annotated[CertificateSerialNumber, XmlPath(f'{PATH_E}/CertifAtv/text()')]
    vendor_timestamp: Annotated[datetime, XmlPath(f'{PATH_E}/DtHrBC/text()')]
    settlement_date: Annotated[date, XmlPath(f'{PATH_E}/DtMovto/text()')]

    general_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH_E}/@CodErro')] = None
    instituition_certificate_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH_E}/ISPBIFCertif/@CodErro')] = None
    certificate_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH_E}/CertifDig/@CodErro')] = None
    certificate_issue_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH_E}/CodCertifrAtv/@CodErro')] = None
    certificate_serial_number_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH_E}/CertifAtv/@CodErro')] = None
    vendor_timestamp_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH_E}/DtHrBC/@CodErro')] = None
    settlement_date_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH_E}/DtMovto/@CodErro')] = None
