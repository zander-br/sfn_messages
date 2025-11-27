from datetime import date, datetime
from typing import Annotated, Literal

from sfn_messages.core.models import BaseMessage, XmlPath
from sfn_messages.core.types import InstitutionControlNumber, Ispb

PATH = 'DOC/SISMSG/GEN0008'
PATH_R1 = 'DOC/SISMSG/GEN0008R1'


class GEN0008(BaseMessage):
    message_code: Annotated[Literal['GEN0008'], XmlPath(f'{PATH}/CodMsg/text()')] = 'GEN0008'
    institution_control_number: Annotated[InstitutionControlNumber, XmlPath(f'{PATH}/NumCtrlIF/text()')]
    institution_ispb: Annotated[Ispb, XmlPath(f'{PATH}/ISPBIF/text()')]
    instituition_certificate: Annotated[Ispb, XmlPath(f'{PATH}/ISPBIFCertif/text()')]
    settlement_date: Annotated[date, XmlPath(f'{PATH}/DtMovto/text()')]


class GEN0008R1(BaseMessage):
    message_code: Annotated[Literal['GEN0008R1'], XmlPath(f'{PATH_R1}/CodMsg/text()')] = 'GEN0008R1'
    institution_control_number: Annotated[InstitutionControlNumber, XmlPath(f'{PATH_R1}/NumCtrlIF/text()')]
    institution_ispb: Annotated[Ispb, XmlPath(f'{PATH_R1}/ISPBIF/text()')]
    instituition_certificate: Annotated[Ispb, XmlPath(f'{PATH_R1}/ISPBIFCertif/text()')]
    settlement_date: Annotated[date, XmlPath(f'{PATH_R1}/DtMovto/text()')]
    vendor_timestamp: Annotated[datetime, XmlPath(f'{PATH_R1}/DtHrBC/text()')]
