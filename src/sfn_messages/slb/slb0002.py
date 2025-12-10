from datetime import date, datetime
from decimal import Decimal
from typing import Annotated, ClassVar, Literal

from sfn_messages.core.models import BaseMessage, XmlPath
from sfn_messages.core.types import (
    InstitutionControlNumber,
    Ispb,
    Priority,
)

from .types import SlbControlNumber, SlbSettlementStatus

PATH = 'DOC/SISMSG/SLB0002'
PATH_R1 = 'DOC/SISMSG/SLB0002R1'
XML_NAMESPACE = 'http://www.bcb.gov.br/SLB/SLB0002.xsd'


class SLB0002(BaseMessage):
    XML_NAMESPACE: ClassVar[str | None] = XML_NAMESPACE

    message_code: Annotated[Literal['SLB0002'], XmlPath(f'{PATH}/CodMsg/text()')] = 'SLB0002'
    participant_institution_control_number: Annotated[InstitutionControlNumber, XmlPath(f'{PATH}/NumCtrlPart/text()')]
    participant_ispb: Annotated[Ispb, XmlPath(f'{PATH}/ISPBPart/text()')]
    original_slb_control_number: Annotated[SlbControlNumber, XmlPath(f'{PATH}/NumCtrlSLBOr/text()')]
    priority: Annotated[Priority | None, XmlPath(f'{PATH}/NivelPref/text()')] = None
    amount: Annotated[Decimal, XmlPath(f'{PATH}/VlrLanc/text()')]
    settlement_date: Annotated[date, XmlPath(f'{PATH}/DtMovto/text()')]


class SLB0002R1(BaseMessage):
    XML_NAMESPACE: ClassVar[str | None] = XML_NAMESPACE

    message_code: Annotated[Literal['SLB0002R1'], XmlPath(f'{PATH_R1}/CodMsg/text()')] = 'SLB0002R1'
    participant_institution_control_number: Annotated[
        InstitutionControlNumber, XmlPath(f'{PATH_R1}/NumCtrlPart/text()')
    ]
    participant_ispb: Annotated[Ispb, XmlPath(f'{PATH_R1}/ISPBPart/text()')]
    str_control_number: Annotated[InstitutionControlNumber | None, XmlPath(f'{PATH_R1}/NumCtrlSTR/text()')] = None
    slb_settlement_status: Annotated[SlbSettlementStatus, XmlPath(f'{PATH_R1}/SitLancSLB/text()')]
    settlement_timestamp: Annotated[datetime, XmlPath(f'{PATH_R1}/DtHrSit/text()')]
    settlement_date: Annotated[date, XmlPath(f'{PATH_R1}/DtMovto/text()')]
