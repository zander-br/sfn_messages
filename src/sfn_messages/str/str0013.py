from datetime import date, datetime
from typing import Annotated, ClassVar, Literal

from sfn_messages.core.models import BaseMessage, XmlPath
from sfn_messages.core.types import Amount, ErrorCode, InstitutionControlNumber, Ispb

PATH = 'DOC/SISMSG/STR0013'
PATH_R1 = 'DOC/SISMSG/STR0013R1'
PATH_E = 'DOC/SISMSG/STR0013'
XML_NAMESPACE = 'http://www.bcb.gov.br/SPB/STR0013.xsd'
XML_NAMESPACE_ERROR = 'http://www.bcb.gov.br/SPB/STR0013E.xsd'


class STR0013(BaseMessage):
    XML_NAMESPACE: ClassVar[str | None] = XML_NAMESPACE

    message_code: Annotated[Literal['STR0013'], XmlPath(f'{PATH}/CodMsg/text()')] = 'STR0013'
    institution_control_number: Annotated[InstitutionControlNumber, XmlPath(f'{PATH}/NumCtrlIF_LDL/text()')]
    institution_ispb: Annotated[Ispb, XmlPath(f'{PATH}/ISPBIF_LDL/text()')]
    settlement_date: Annotated[date, XmlPath(f'{PATH}/DtMovto/text()')]


class STR0013R1(BaseMessage):
    XML_NAMESPACE: ClassVar[str | None] = XML_NAMESPACE

    message_code: Annotated[Literal['STR0013R1'], XmlPath(f'{PATH_R1}/CodMsg/text()')] = 'STR0013R1'
    institution_control_number: Annotated[InstitutionControlNumber, XmlPath(f'{PATH_R1}/NumCtrlIF_LDL/text()')]
    institution_ispb: Annotated[Ispb, XmlPath(f'{PATH_R1}/ISPBIF_LDL/text()')]
    balance: Annotated[Amount, XmlPath(f'{PATH_R1}/SldRB_CL/text()')]
    vendor_timestamp: Annotated[datetime, XmlPath(f'{PATH_R1}/DtHrBC/text()')]
    settlement_date: Annotated[date, XmlPath(f'{PATH_R1}/DtMovto/text()')]


class STR0013E(BaseMessage):
    XML_NAMESPACE: ClassVar[str | None] = XML_NAMESPACE_ERROR

    message_code: Annotated[Literal['STR0013E'], XmlPath(f'{PATH_E}/CodMsg/text()')] = 'STR0013E'
    institution_control_number: Annotated[
        InstitutionControlNumber | None, XmlPath(f'{PATH_E}/NumCtrlIF_LDL/text()')
    ] = None
    institution_ispb: Annotated[Ispb | None, XmlPath(f'{PATH_E}/ISPBIF_LDL/text()')] = None
    settlement_date: Annotated[date | None, XmlPath(f'{PATH_E}/DtMovto/text()')] = None

    general_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH_E}/@CodErro')] = None
    institution_control_number_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH_E}/NumCtrlIF_LDL/@CodErro')] = (
        None
    )
    institution_ispb_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH_E}/ISPBIF_LDL/@CodErro')] = None
    settlement_date_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH_E}/DtMovto/@CodErro')] = None
