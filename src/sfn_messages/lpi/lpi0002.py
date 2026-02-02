from datetime import date, datetime
from decimal import Decimal
from typing import Annotated, ClassVar, Literal

from sfn_messages.core.models import BaseMessage, XmlPath
from sfn_messages.core.types import ErrorCode, InstitutionControlNumber, Ispb, StrControlNumber, StrSettlementStatus

PATH = 'DOC/SISMSG/LPI0002'
PATH_R1 = 'DOC/SISMSG/LPI0002R1'
PATH_E = 'DOC/SISMSG/LPI0002'
XML_NAMESPACE = 'http://www.bcb.gov.br/SPB/LPI0002.xsd'
XML_NAMESPACE_ERROR = 'http://www.bcb.gov.br/SPB/LPI0002E.xsd'


class LPI0002(BaseMessage):
    XML_NAMESPACE: ClassVar[str | None] = XML_NAMESPACE

    message_code: Annotated[Literal['LPI0002'], XmlPath(f'{PATH}/CodMsg/text()')] = 'LPI0002'
    ieme_control_number: Annotated[InstitutionControlNumber, XmlPath(f'{PATH}/NumCtrlIEME/text()')]
    ieme_ispb: Annotated[Ispb | None, XmlPath(f'{PATH}/ISPBIEME/text()')] = None
    amount: Annotated[Decimal, XmlPath(f'{PATH}/VlrLanc/text()')]
    settlement_date: Annotated[date, XmlPath(f'{PATH}/DtMovto/text()')]


class LPI0002R1(BaseMessage):
    XML_NAMESPACE: ClassVar[str | None] = XML_NAMESPACE

    message_code: Annotated[Literal['LPI0002R1'], XmlPath(f'{PATH_R1}/CodMsg/text()')] = 'LPI0002R1'
    ieme_control_number: Annotated[InstitutionControlNumber, XmlPath(f'{PATH_R1}/NumCtrlIEME/text()')]
    ieme_ispb: Annotated[Ispb | None, XmlPath(f'{PATH_R1}/ISPBIEME/text()')] = None
    str_control_number: Annotated[StrControlNumber, XmlPath(f'{PATH_R1}/NumCtrlSTR/text()')]
    str_settlement_status: Annotated[StrSettlementStatus | None, XmlPath(f'{PATH_R1}/SitLancSTR/text()')] = None
    settlement_timestamp: Annotated[datetime, XmlPath(f'{PATH_R1}/DtHrSit/text()')]
    settlement_date: Annotated[date, XmlPath(f'{PATH_R1}/DtMovto/text()')]


class LPI0002E(BaseMessage):
    XML_NAMESPACE: ClassVar[str | None] = XML_NAMESPACE_ERROR

    message_code: Annotated[Literal['LPI0002E'], XmlPath(f'{PATH_E}/CodMsg/text()')] = 'LPI0002E'
    ieme_control_number: Annotated[InstitutionControlNumber | None, XmlPath(f'{PATH_E}/NumCtrlIEME/text()')] = None
    ieme_ispb: Annotated[Ispb | None, XmlPath(f'{PATH_E}/ISPBIEME/text()')] = None
    amount: Annotated[Decimal | None, XmlPath(f'{PATH_E}/VlrLanc/text()')] = None
    settlement_date: Annotated[date | None, XmlPath(f'{PATH_E}/DtMovto/text()')] = None

    general_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH_E}/@CodErro')] = None
    ieme_control_number_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH_E}/NumCtrlIEME/@CodErro')] = None
    ieme_ispb_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH_E}/ISPBIEME/@CodErro')] = None
    amount_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH_E}/VlrLanc/@CodErro')] = None
    settlement_date_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH_E}/DtMovto/@CodErro')] = None
