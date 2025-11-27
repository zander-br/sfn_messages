from datetime import date, datetime
from typing import Annotated, Literal

from sfn_messages.core.models import BaseMessage, XmlPath

PATH = 'DOC/SISMSG/STR0017'


class STR017(BaseMessage):
    message_code: Annotated[Literal['STR0017'], XmlPath(f'{PATH}/CodMsg/text()')] = 'STR0017'
    opening_timestamp: Annotated[datetime, XmlPath(f'{PATH}/DtHrAbert/text()')]
    vendor_timestamp: Annotated[datetime, XmlPath(f'{PATH}/DtHrBC/text()')]
    settlement_date: Annotated[date, XmlPath(f'{PATH}/DtMovto/text()')]
