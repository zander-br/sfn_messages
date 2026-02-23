from datetime import date, datetime
from typing import Annotated, ClassVar, Literal

from sfn_messages.core.models import BaseMessage, XmlPath
from sfn_messages.core.types import ErrorCode

PATH = 'DOC/SISMSG/STR0015'
PATH_E = 'DOC/SISMSG/STR0015'
XML_NAMESPACE = 'http://www.bcb.gov.br/SPB/STR0015.xsd'
XML_NAMESPACE_ERROR = 'http://www.bcb.gov.br/SPB/STR0015E.xsd'


class STR0015(BaseMessage):
    XML_NAMESPACE: ClassVar[str | None] = XML_NAMESPACE

    message_code: Annotated[Literal['STR0015'], XmlPath(f'{PATH}/CodMsg/text()')] = 'STR0015'
    closing_timestamp: Annotated[datetime, XmlPath(f'{PATH}/DtHrFcht/text()')]
    vendor_timestamp: Annotated[datetime, XmlPath(f'{PATH}/DtHrBC/text()')]
    settlement_date: Annotated[date, XmlPath(f'{PATH}/DtMovto/text()')]


class STR0015E(BaseMessage):
    XML_NAMESPACE: ClassVar[str | None] = XML_NAMESPACE_ERROR

    message_code: Annotated[Literal['STR0015E'], XmlPath(f'{PATH_E}/CodMsg/text()')] = 'STR0015E'
    closing_timestamp: Annotated[datetime | None, XmlPath(f'{PATH_E}/DtHrFcht/text()')] = None
    vendor_timestamp: Annotated[datetime | None, XmlPath(f'{PATH_E}/DtHrBC/text()')] = None
    settlement_date: Annotated[date | None, XmlPath(f'{PATH_E}/DtMovto/text()')] = None

    general_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH_E}/@CodErro')] = None
    closing_timestamp_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH_E}/DtHrFcht/@CodErro')] = None
    vendor_timestamp_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH_E}/DtHrBC/@CodErro')] = None
    settlement_date_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH_E}/DtMovto/@CodErro')] = None
