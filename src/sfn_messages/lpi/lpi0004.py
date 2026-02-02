from datetime import date, datetime
from decimal import Decimal
from typing import Annotated, ClassVar, Literal

from sfn_messages.core.models import BaseMessage, XmlPath
from sfn_messages.core.types import (
    ErrorCode,
    InstitutionControlNumber,
    Ispb,
    StrControlNumber,
    StrSettlementStatus,
)

PATH = 'DOC/SISMSG/LPI0004'
PATH_R1 = 'DOC/SISMSG/LPI0004R1'
PATH_E = 'DOC/SISMSG/LPI0004'
XML_NAMESPACE = 'http://www.bcb.gov.br/SPB/LPI0004.xsd'
XML_NAMESPACE_ERROR = 'http://www.bcb.gov.br/SPB/LPI0004E.xsd'


class LPI0004(BaseMessage):
    XML_NAMESPACE: ClassVar[str | None] = XML_NAMESPACE

    message_code: Annotated[Literal['LPI0004'], XmlPath(f'{PATH}/CodMsg/text()')] = 'LPI0004'
    pspi_control_number: Annotated[InstitutionControlNumber, XmlPath(f'{PATH}/NumCtrlPSPI/text()')]
    pspi_ispb: Annotated[Ispb, XmlPath(f'{PATH}/ISPBPSPI/text()')]
    amount: Annotated[Decimal, XmlPath(f'{PATH}/VlrLanc/text()')]
    settlement_date: Annotated[date, XmlPath(f'{PATH}/DtMovto/text()')]


class LPI0004R1(BaseMessage):
    XML_NAMESPACE: ClassVar[str | None] = XML_NAMESPACE

    message_code: Annotated[Literal['LPI0004R1'], XmlPath(f'{PATH_R1}/CodMsg/text()')] = 'LPI0004R1'
    pspi_control_number: Annotated[InstitutionControlNumber, XmlPath(f'{PATH_R1}/NumCtrlPSPI/text()')]
    pspi_ispb: Annotated[Ispb, XmlPath(f'{PATH_R1}/ISPBPSPI/text()')]
    str_control_number: Annotated[StrControlNumber, XmlPath(f'{PATH_R1}/NumCtrlSTR/text()')]
    str_settlement_status: Annotated[StrSettlementStatus | None, XmlPath(f'{PATH_R1}/SitLancSTR/text()')] = None
    settlement_timestamp: Annotated[datetime, XmlPath(f'{PATH_R1}/DtHrSit/text()')]
    settlement_date: Annotated[date, XmlPath(f'{PATH_R1}/DtMovto/text()')]


class LPI0004E(BaseMessage):
    XML_NAMESPACE: ClassVar[str | None] = XML_NAMESPACE_ERROR

    message_code: Annotated[Literal['LPI0004E'], XmlPath(f'{PATH_E}/CodMsg/text()')] = 'LPI0004E'
    pspi_control_number: Annotated[InstitutionControlNumber | None, XmlPath(f'{PATH_E}/NumCtrlPSPI/text()')] = None
    pspi_ispb: Annotated[Ispb | None, XmlPath(f'{PATH_E}/ISPBPSPI/text()')] = None
    amount: Annotated[Decimal | None, XmlPath(f'{PATH_E}/VlrLanc/text()')] = None
    settlement_date: Annotated[date | None, XmlPath(f'{PATH_E}/DtMovto/text()')] = None

    general_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH_E}/@CodErro')] = None
    pspi_control_number_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH_E}/NumCtrlPSPI/@CodErro')] = None
    pspi_ispb_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH_E}/ISPBPSPI/@CodErro')] = None
    amount_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH_E}/VlrLanc/@CodErro')] = None
    settlement_date_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH_E}/DtMovto/@CodErro')] = None
