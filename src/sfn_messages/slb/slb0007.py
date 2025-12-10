from datetime import date, datetime
from decimal import Decimal
from typing import Annotated, ClassVar, Literal

from sfn_messages.core.models import BaseMessage, XmlPath
from sfn_messages.core.types import (
    Cnpj,
    Description,
    InstitutionControlNumber,
    Ispb,
    Priority,
    StrControlNumber,
)

from .types import SlbControlNumber, SlbPurpose, SlbSettlementStatus

PATH = 'DOC/SISMSG/SLB0007'
PATH_R1 = 'DOC/SISMSG/SLB0007R1'
XML_NAMESPACE = 'http://www.bcb.gov.br/SLB/SLB0007.xsd'


class SLB0007(BaseMessage):
    XML_NAMESPACE: ClassVar[str | None] = XML_NAMESPACE

    message_code: Annotated[Literal['SLB0007'], XmlPath(f'{PATH}/CodMsg/text()')] = 'SLB0007'
    participant_institution_control_number: Annotated[InstitutionControlNumber, XmlPath(f'{PATH}/NumCtrlPart/text()')]
    participant_ispb: Annotated[Ispb, XmlPath(f'{PATH}/ISPBPart/text()')]
    original_slb_control_number: Annotated[SlbControlNumber | None, XmlPath(f'{PATH}/NumCtrlSLBOr/text()')] = None
    partner_cnpj: Annotated[Cnpj | None, XmlPath(f'{PATH}/CNPJConv/text()')] = None
    slb_purpose: Annotated[SlbPurpose, XmlPath(f'{PATH}/FinlddSLB/text()')]
    amount: Annotated[Decimal, XmlPath(f'{PATH}/VlrLanc/text()')]
    priority: Annotated[Priority | None, XmlPath(f'{PATH}/NivelPref/text()')] = None
    description: Annotated[Description, XmlPath(f'{PATH}/Hist/text()')]
    settlement_date: Annotated[date, XmlPath(f'{PATH}/DtMovto/text()')]


class SLB0007R1(BaseMessage):
    XML_NAMESPACE: ClassVar[str | None] = XML_NAMESPACE

    message_code: Annotated[Literal['SLB0007R1'], XmlPath(f'{PATH_R1}/CodMsg/text()')] = 'SLB0007R1'
    participant_institution_control_number: Annotated[
        InstitutionControlNumber, XmlPath(f'{PATH_R1}/NumCtrlPart/text()')
    ]
    participant_ispb: Annotated[Ispb, XmlPath(f'{PATH_R1}/ISPBPart/text()')]
    original_slb_control_number: Annotated[InstitutionControlNumber, XmlPath(f'{PATH_R1}/NumCtrlSLB/text()')]
    str_control_number: Annotated[StrControlNumber, XmlPath(f'{PATH_R1}/NumCtrlSTR/text()')]
    slb_settlement_status: Annotated[SlbSettlementStatus, XmlPath(f'{PATH_R1}/SitLancSLB/text()')]
    settlement_timestamp: Annotated[datetime, XmlPath(f'{PATH_R1}/DtHrSit/text()')]
    settlement_date: Annotated[date, XmlPath(f'{PATH_R1}/DtMovto/text()')]
