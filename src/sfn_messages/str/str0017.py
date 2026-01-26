from datetime import date, datetime
from typing import Annotated, ClassVar, Literal

from sfn_messages.core.models import BaseMessage, XmlPath
from sfn_messages.core.types import ErrorCode

PATH = 'DOC/SISMSG/STR0017'
PATH_E = 'DOC/SISMSG/STR0017'
XML_NAMESPACE = 'http://www.bcb.gov.br/SPB/STR0017.xsd'
XML_NAMESPACE_ERROR = 'http://www.bcb.gov.br/SPB/STR0017E.xsd'


class STR0017(BaseMessage):
    XML_NAMESPACE: ClassVar[str | None] = XML_NAMESPACE

    message_code: Annotated[Literal['STR0017'], XmlPath(f'{PATH}/CodMsg/text()')] = 'STR0017'
    opening_timestamp: Annotated[datetime, XmlPath(f'{PATH}/DtHrAbert/text()')]
    vendor_timestamp: Annotated[datetime, XmlPath(f'{PATH}/DtHrBC/text()')]
    settlement_date: Annotated[date, XmlPath(f'{PATH}/DtMovto/text()')]


class STR0017E(BaseMessage):
    XML_NAMESPACE: ClassVar[str | None] = XML_NAMESPACE_ERROR

    message_code: Annotated[Literal['STR0017E'], XmlPath(f'{PATH_E}/CodMsg/text()')] = 'STR0017E'
    opening_timestamp: Annotated[datetime | None, XmlPath(f'{PATH_E}/DtHrAbert/text()')] = None
    vendor_timestamp: Annotated[datetime | None, XmlPath(f'{PATH_E}/DtHrBC/text()')] = None
    settlement_date: Annotated[date | None, XmlPath(f'{PATH_E}/DtMovto/text()')] = None

    general_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH_E}/@CodErro')] = None
    opening_timestamp_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH_E}/DtHrAbert/@CodErro')] = None
    vendor_timestamp_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH_E}/DtHrBC/@CodErro')] = None
    settlement_date_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH_E}/DtMovto/@CodErro')] = None
