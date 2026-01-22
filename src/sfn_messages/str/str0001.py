from datetime import date, datetime
from typing import Annotated, ClassVar, Literal

from pydantic import Field

from sfn_messages.core.models import BaseMessage, BaseSubMessage, XmlPath
from sfn_messages.core.types import (
    ErrorCode,
    GridCode,
    InstitutionControlNumber,
    Ispb,
    TimeType,
)

PATH = 'DOC/SISMSG/STR0001'
PATH_R1 = 'DOC/SISMSG/STR0001R1'
PATH_R1_GROUP = 'Grupo_STR0001R1_GrdHrio'
PATH_E = 'DOC/SISMSG/STR0001E'
XML_NAMESPACE = 'http://www.bcb.gov.br/SPB/STR0001.xsd'
XML_NAMESPACE_ERROR = 'http://www.bcb.gov.br/SPB/STR0001E.xsd'


class STR0001(BaseMessage):
    XML_NAMESPACE: ClassVar[str | None] = XML_NAMESPACE

    message_code: Annotated[Literal['STR0001'], XmlPath(f'{PATH}/CodMsg/text()')] = 'STR0001'
    institution_control_number: Annotated[InstitutionControlNumber, XmlPath(f'{PATH}/NumCtrlIF/text()')]
    institution_ispb: Annotated[Ispb, XmlPath(f'{PATH}/ISPBIF/text()')]
    reference_date: Annotated[date, XmlPath(f'{PATH}/DtRef/text()')]
    hour_type: Annotated[TimeType, XmlPath(f'{PATH}/TpHrio/text()')]


class ScheduleGrid(BaseSubMessage):
    code: Annotated[GridCode, XmlPath(f'{PATH_R1_GROUP}/CodGrd/text()')]
    opening_hour: Annotated[datetime, XmlPath(f'{PATH_R1_GROUP}/DtHrAbert/text()')]
    closing_hour: Annotated[datetime, XmlPath(f'{PATH_R1_GROUP}/DtHrFcht/text()')]
    hour_type: Annotated[TimeType, XmlPath(f'{PATH_R1_GROUP}/TpHrio/text()')]


class STR0001R1(BaseMessage):
    XML_NAMESPACE: ClassVar[str | None] = XML_NAMESPACE

    message_code: Annotated[Literal['STR0001R1'], XmlPath(f'{PATH_R1}/CodMsg/text()')] = 'STR0001R1'
    institution_control_number: Annotated[InstitutionControlNumber, XmlPath(f'{PATH_R1}/NumCtrlIF/text()')]
    institution_ispb: Annotated[Ispb, XmlPath(f'{PATH_R1}/ISPBIF/text()')]
    schedule_grid_group: Annotated[list[ScheduleGrid], XmlPath(f'{PATH_R1}')] = Field(default_factory=list)
    reference_date: Annotated[date, XmlPath(f'{PATH_R1}/DtRef/text()')]
    vendor_timestamp: Annotated[datetime, XmlPath(f'{PATH_R1}/DtHrBC/text()')]


class STR0001E(BaseMessage):
    XML_NAMESPACE: ClassVar[str | None] = XML_NAMESPACE_ERROR

    message_code: Annotated[Literal['STR0001'], XmlPath(f'{PATH_E}/CodMsg/text()')] = 'STR0001'
    institution_control_number: Annotated[InstitutionControlNumber, XmlPath(f'{PATH_E}/NumCtrlIF/text()')]
    institution_ispb: Annotated[Ispb, XmlPath(f'{PATH_E}/ISPBIF/text()')]
    reference_date: Annotated[date, XmlPath(f'{PATH_E}/DtRef/text()')]
    hour_type: Annotated[TimeType, XmlPath(f'{PATH_E}/TpHrio/text()')]

    general_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH_E}/@CodErro')] = None
    institution_control_number_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH_E}/NumCtrlIF/@CodErro')] = None
    institution_ispb_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH_E}/ISPBIF/@CodErro')] = None
    reference_date_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH_E}/DtRef/@CodErro')] = None
    hour_type_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH_E}/TpHrio/@CodErro')] = None
