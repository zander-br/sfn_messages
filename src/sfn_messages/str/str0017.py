from datetime import date, datetime
from typing import Annotated, ClassVar, Literal

from sfn_messages.core.models import BaseMessage, XmlPath

PATH = 'DOC/SISMSG/STR0017'
XML_NAMESPACE = 'http://www.bcb.gov.br/SPB/STR0017.xsd'


class STR017(BaseMessage):
    XML_NAMESPACE: ClassVar[str | None] = XML_NAMESPACE

    message_code: Annotated[Literal['STR0017'], XmlPath(f'{PATH}/CodMsg/text()')] = 'STR0017'
    opening_timestamp: Annotated[datetime, XmlPath(f'{PATH}/DtHrAbert/text()')]
    vendor_timestamp: Annotated[datetime, XmlPath(f'{PATH}/DtHrBC/text()')]
    settlement_date: Annotated[date, XmlPath(f'{PATH}/DtMovto/text()')]
