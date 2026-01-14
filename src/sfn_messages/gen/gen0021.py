from datetime import date, datetime
from typing import Annotated, ClassVar, Literal

from sfn_messages.core.models import BaseMessage, BaseSubMessage, XmlPath
from sfn_messages.core.types import ErrorCode, GridCode, Ispb, ProductCode, TimeType

PATH = 'DOC/SISMSG/GEN0021'
PATH_R1_GROUP = 'Grupo_GEN0021_GrdHrio'
PATH_E = 'DOC/SISMSG/GEN0021E'
XML_NAMESPACE = 'http://www.bcb.gov.br/GEN/GEN0021.xsd'
XML_NAMESPACE_ERROR = 'http://www.bcb.gov.br/GEN/GEN0021E.xsd'


class ScheduleGrid(BaseSubMessage):
    code: Annotated[GridCode, XmlPath(f'{PATH_R1_GROUP}/CodGrd/text()')]
    opening_hour: Annotated[datetime, XmlPath(f'{PATH_R1_GROUP}/DtHrAbert/text()')]
    closing_hour: Annotated[datetime, XmlPath(f'{PATH_R1_GROUP}/DtHrFcht/text()')]
    hour_type: Annotated[TimeType, XmlPath(f'{PATH_R1_GROUP}/TpHrio/text()')]


class GEN0021(BaseMessage):
    XML_NAMESPACE: ClassVar[str | None] = XML_NAMESPACE

    message_code: Annotated[Literal['GEN0021'], XmlPath(f'{PATH}/CodMsg/text()')] = 'GEN0021'
    provider_ispb: Annotated[Ispb, XmlPath(f'{PATH}/ISPBPrestd/text()')]
    product_code: Annotated[ProductCode | None, XmlPath(f'{PATH}/CodProdt/text()')] = None
    schedule_grid_group: Annotated[list[ScheduleGrid], XmlPath(f'{PATH}')]
    reference_date: Annotated[date, XmlPath(f'{PATH}/DtRef/text()')]
    provider_datetime: Annotated[datetime, XmlPath(f'{PATH}/DtHrPrestd/text()')]
    settlement_date: Annotated[date, XmlPath(f'{PATH}/DtMovto/text()')]


class ScheduleGridError(BaseSubMessage):
    code: Annotated[GridCode, XmlPath(f'{PATH_R1_GROUP}/CodGrd/text()')]
    opening_hour: Annotated[datetime, XmlPath(f'{PATH_R1_GROUP}/DtHrAbert/text()')]
    closing_hour: Annotated[datetime, XmlPath(f'{PATH_R1_GROUP}/DtHrFcht/text()')]
    hour_type: Annotated[TimeType, XmlPath(f'{PATH_R1_GROUP}/TpHrio/text()')]

    code_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH_R1_GROUP}/CodGrd/@CodErro')] = None
    opening_hour_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH_R1_GROUP}/DtHrAbert/@CodErro')] = None
    closing_hour_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH_R1_GROUP}/DtHrFcht/@CodErro')] = None
    hour_type_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH_R1_GROUP}/TpHrio/@CodErro')] = None


class GEN0021E(BaseMessage):
    XML_NAMESPACE: ClassVar[str | None] = XML_NAMESPACE_ERROR

    message_code: Annotated[Literal['GEN0021'], XmlPath(f'{PATH_E}/CodMsg/text()')] = 'GEN0021'
    provider_ispb: Annotated[Ispb, XmlPath(f'{PATH_E}/ISPBPrestd/text()')]
    product_code: Annotated[ProductCode | None, XmlPath(f'{PATH_E}/CodProdt/text()')] = None
    schedule_grid_group: Annotated[list[ScheduleGridError], XmlPath(f'{PATH_E}')]
    reference_date: Annotated[date, XmlPath(f'{PATH_E}/DtRef/text()')]
    provider_datetime: Annotated[datetime, XmlPath(f'{PATH_E}/DtHrPrestd/text()')]
    settlement_date: Annotated[date, XmlPath(f'{PATH_E}/DtMovto/text()')]

    general_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH_E}/@CodErro')] = None
    provider_ispb_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH_E}/ISPBPrestd/@CodErro')] = None
    product_code_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH_E}/CodProdt/@CodErro')] = None
    reference_date_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH_E}/DtRef/@CodErro')] = None
    provider_datetime_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH_E}/DtHrPrestd/@CodErro')] = None
    settlement_date_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH_E}/DtMovto/@CodErro')] = None
