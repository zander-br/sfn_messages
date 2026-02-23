from datetime import date, datetime
from decimal import Decimal
from typing import Annotated, ClassVar, Literal

from sfn_messages.core.models import BaseMessage, XmlPath
from sfn_messages.core.types import ErrorCode, Ispb

from .types import BalanceType

PATH = 'DOC/SISMSG/STR0016'
PATH_E = 'DOC/SISMSG/STR0016'
XML_NAMESPACE = 'http://www.bcb.gov.br/SPB/STR0016.xsd'
XML_NAMESPACE_ERROR = 'http://www.bcb.gov.br/SPB/STR0016E.xsd'


class STR0016(BaseMessage):
    XML_NAMESPACE: ClassVar[str | None] = XML_NAMESPACE

    message_code: Annotated[Literal['STR0016'], XmlPath(f'{PATH}/CodMsg/text()')] = 'STR0016'
    participant_ispb: Annotated[Ispb, XmlPath(f'{PATH}/ISPBPart/text()')]
    balance_type: Annotated[BalanceType, XmlPath(f'{PATH}/TpSld/text()')]
    balance: Annotated[Decimal, XmlPath(f'{PATH}/SldRB_CL/text()')]
    vendor_timestamp: Annotated[datetime, XmlPath(f'{PATH}/DtHrBC/text()')]
    settlement_date: Annotated[date, XmlPath(f'{PATH}/DtMovto/text()')]


class STR0016E(BaseMessage):
    XML_NAMESPACE: ClassVar[str | None] = XML_NAMESPACE_ERROR

    message_code: Annotated[Literal['STR0016E'], XmlPath(f'{PATH_E}/CodMsg/text()')] = 'STR0016E'
    participant_ispb: Annotated[Ispb | None, XmlPath(f'{PATH}/ISPBPart/text()')] = None
    balance_type: Annotated[BalanceType | None, XmlPath(f'{PATH}/TpSld/text()')] = None
    balance: Annotated[Decimal | None, XmlPath(f'{PATH}/SldRB_CL/text()')] = None
    vendor_timestamp: Annotated[datetime | None, XmlPath(f'{PATH}/DtHrBC/text()')] = None
    settlement_date: Annotated[date | None, XmlPath(f'{PATH}/DtMovto/text()')] = None

    general_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH_E}/@CodErro')] = None
    participant_ispb_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH}/ISPBPart/@CodErro')] = None
    balance_type_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH}/TpSld/@CodErro')] = None
    balance_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH}/SldRB_CL/@CodErro')] = None
    vendor_timestamp_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH}/DtHrBC/@CodErro')] = None
    settlement_date_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH}/DtMovto/@CodErro')] = None
