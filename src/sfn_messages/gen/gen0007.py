from datetime import date, datetime
from typing import Annotated, Literal

from sfn_messages.core.models import BaseMessage, XmlPath
from sfn_messages.core.types import Ispb

from .types import Certificate, CertificateIssue, CertificateSerialNumber

PATH = 'DOC/SISMSG/GEN0007'


class GEN0007(BaseMessage):
    message_code: Annotated[Literal['GEN0007'], XmlPath(f'{PATH}/CodMsg/text()')] = 'GEN0007'
    instituition_certificate: Annotated[Ispb, XmlPath(f'{PATH}/ISPBIFCertif/text()')]
    certificate: Annotated[Certificate, XmlPath(f'{PATH}/CertifDig/text()')]
    certificate_issue: Annotated[CertificateIssue, XmlPath(f'{PATH}/CodCertifrAtv/text()')]
    certificate_serial_number: Annotated[CertificateSerialNumber, XmlPath(f'{PATH}/CertifAtv/text()')]
    vendor_timestamp: Annotated[datetime, XmlPath(f'{PATH}/DtHrBC/text()')]
    settlement_date: Annotated[date, XmlPath(f'{PATH}/DtMovto/text()')]
