from datetime import date, datetime
from typing import Annotated, ClassVar, Literal

from sfn_messages.core.models import BaseMessage, XmlPath
from sfn_messages.core.types import (
    ErrorCode,
    InstitutionControlNumber,
    Ispb,
    StrControlNumber,
)

PATH = 'DOC/SISMSG/STR0043'
PATH_R1 = 'DOC/SISMSG/STR0043R1'
PATH_E = 'DOC/SISMSG/STR0043'
XML_NAMESPACE = 'http://www.bcb.gov.br/SPB/STR0043.xsd'
XML_NAMESPACE_ERROR = 'http://www.bcb.gov.br/SPB/STR0043E.xsd'


class STR0043(BaseMessage):
    XML_NAMESPACE: ClassVar[str | None] = XML_NAMESPACE

    message_code: Annotated[Literal['STR0043'], XmlPath(f'{PATH}/CodMsg/text()')] = 'STR0043'
    participant_institution_control_number: Annotated[InstitutionControlNumber, XmlPath(f'{PATH}/NumCtrlPart/text()')]
    participant_ispb: Annotated[Ispb, XmlPath(f'{PATH}/ISPBPart/text()')]
    start_timestamp: Annotated[datetime, XmlPath(f'{PATH}/DtHrIniTeste/text()')]
    settlement_date: Annotated[date, XmlPath(f'{PATH}/DtMovto/text()')]


class STR0043R1(BaseMessage):
    XML_NAMESPACE: ClassVar[str | None] = XML_NAMESPACE

    message_code: Annotated[Literal['STR0043R1'], XmlPath(f'{PATH_R1}/CodMsg/text()')] = 'STR0043R1'
    participant_institution_control_number: Annotated[
        InstitutionControlNumber, XmlPath(f'{PATH_R1}/NumCtrlPart/text()')
    ]
    participant_ispb: Annotated[Ispb, XmlPath(f'{PATH_R1}/ISPBPart/text()')]
    str_control_number: Annotated[StrControlNumber, XmlPath(f'{PATH_R1}/NumCtrlSTR/text()')]
    vendor_timestamp: Annotated[datetime, XmlPath(f'{PATH_R1}/DtHrBC/text()')]
    settlement_date: Annotated[date, XmlPath(f'{PATH_R1}/DtMovto/text()')]


class STR0043E(BaseMessage):
    XML_NAMESPACE: ClassVar[str | None] = XML_NAMESPACE_ERROR

    message_code: Annotated[Literal['STR0043E'], XmlPath(f'{PATH_E}/CodMsg/text()')] = 'STR0043E'
    participant_institution_control_number: Annotated[
        InstitutionControlNumber | None, XmlPath(f'{PATH_E}/NumCtrlPart/text()')
    ] = None
    participant_ispb: Annotated[Ispb | None, XmlPath(f'{PATH_E}/ISPBPart/text()')] = None
    start_timestamp: Annotated[datetime | None, XmlPath(f'{PATH_E}/DtHrIniTeste/text()')] = None
    settlement_date: Annotated[date | None, XmlPath(f'{PATH_E}/DtMovto/text()')] = None

    general_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH_E}/@CodErro')] = None
    participant_institution_control_number_error_code: Annotated[
        ErrorCode | None, XmlPath(f'{PATH_E}/NumCtrlPart/@CodErro')
    ] = None
    participant_ispb_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH}/ISPBPart/@CodErro')] = None
    start_timestamp_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH}/DtHrIniTeste/@CodErro')] = None
    settlement_date_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH}/DtMovto/@CodErro')] = None
