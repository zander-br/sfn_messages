from datetime import date, datetime
from typing import Annotated, ClassVar, Literal

from sfn_messages.core.models import BaseMessage, BaseSubMessage, XmlPath
from sfn_messages.core.types import GridCode, Ispb, ProductCode, TimeType

PATH = 'DOC/SISMSG/GEN0021'
PATH_R1_GROUP = 'Grupo_GEN0021_GrdHrio'
XML_NAMESPACE = 'http://www.bcb.gov.br/GEN/GEN0021.xsd'


class GEN0021SCHEDULEGRIDGROUP(BaseSubMessage):
    grid_code: Annotated[GridCode, XmlPath(f'{PATH_R1_GROUP}/CodGrd/text()')]
    grid_opening_hour: Annotated[datetime, XmlPath(f'{PATH_R1_GROUP}/DtHrAbert/text()')]
    grid_closing_hour: Annotated[datetime, XmlPath(f'{PATH_R1_GROUP}/DtHrFcht/text()')]
    grid_hour_type: Annotated[TimeType, XmlPath(f'{PATH_R1_GROUP}/TpHrio/text()')]


class GEN0021(BaseMessage):
    XML_NAMESPACE: ClassVar[str | None] = XML_NAMESPACE

    message_code: Annotated[Literal['GEN0021'], XmlPath(f'{PATH}/CodMsg/text()')] = 'GEN0021'
    provider_ispb: Annotated[Ispb, XmlPath(f'{PATH}/ISPBPrestd/text()')]
    product_code: Annotated[ProductCode | None, XmlPath(f'{PATH}/CodProdt/text()')] = None
    schedule_grid_group: Annotated[list[GEN0021SCHEDULEGRIDGROUP], XmlPath(f'{PATH}')]
    reference_date: Annotated[date, XmlPath(f'{PATH}/DtRef/text()')]
    provider_datetime: Annotated[datetime, XmlPath(f'{PATH}/DtHrPrestd/text()')]
    settlement_date: Annotated[date, XmlPath(f'{PATH}/DtMovto/text()')]
