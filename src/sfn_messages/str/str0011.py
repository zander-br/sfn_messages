from datetime import date, datetime
from typing import Annotated, ClassVar, Literal

from sfn_messages.core.models import BaseMessage, XmlPath
from sfn_messages.core.types import InstitutionControlNumber, Ispb, StrControlNumber

PATH = 'DOC/SISMSG/STR0011'
PATH_R1 = 'DOC/SISMSG/STR0011R1'
XML_NAMESPACE = 'http://www.bcb.gov.br/SPB/STR0011.xsd'


class STR0011(BaseMessage):
    XML_NAMESPACE: ClassVar[str | None] = XML_NAMESPACE

    message_code: Annotated[Literal['STR0011'], XmlPath(f'{PATH}/CodMsg/text()')] = 'STR0011'
    institution_control_number: Annotated[InstitutionControlNumber, XmlPath(f'{PATH}/NumCtrlIF/text()')]
    institution_ispb: Annotated[Ispb, XmlPath(f'{PATH}/ISPBIF/text()')]
    original_str_control_number: Annotated[StrControlNumber, XmlPath(f'{PATH}/NumCtrlSTR/text()')]
    settlement_date: Annotated[date, XmlPath(f'{PATH}/DtMovto/text()')]


class STR0011R1(BaseMessage):
    XML_NAMESPACE: ClassVar[str | None] = XML_NAMESPACE

    message_code: Annotated[Literal['STR0011'], XmlPath(f'{PATH_R1}/CodMsg/text()')] = 'STR0011'
    institution_control_number: Annotated[InstitutionControlNumber, XmlPath(f'{PATH_R1}/NumCtrlIF/text()')]
    institution_ispb: Annotated[Ispb, XmlPath(f'{PATH_R1}/ISPBIF/text()')]
    vendor_timestamp: Annotated[datetime, XmlPath(f'{PATH_R1}/DtHrBC/text()')]
    settlement_date: Annotated[date, XmlPath(f'{PATH_R1}/DtMovto/text()')]
