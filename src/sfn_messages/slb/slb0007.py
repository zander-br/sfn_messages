from datetime import date, datetime
from decimal import Decimal
from typing import Annotated, ClassVar, Literal

from sfn_messages.core.models import BaseMessage, XmlPath
from sfn_messages.core.types import (
    Cnpj,
    Description,
    ErrorCode,
    InstitutionControlNumber,
    Ispb,
    Priority,
    StrControlNumber,
)

from .types import SlbControlNumber, SlbPurpose, SlbSettlementStatus

PATH = 'DOC/SISMSG/SLB0007'
PATH_R1 = 'DOC/SISMSG/SLB0007R1'
PATH_E = 'DOC/SISMSG/SLB0007E'
XML_NAMESPACE = 'http://www.bcb.gov.br/SPB/SLB0007.xsd'
XML_NAMESPACE_ERROR = 'http://www.bcb.gov.br/SPB/SLB0007E.xsd'


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


class SLB0007E(BaseMessage):
    XML_NAMESPACE: ClassVar[str | None] = XML_NAMESPACE_ERROR

    message_code: Annotated[Literal['SLB0007'], XmlPath(f'{PATH_E}/CodMsg/text()')] = 'SLB0007'
    participant_institution_control_number: Annotated[
        InstitutionControlNumber, XmlPath(f'{PATH_E}/NumCtrlPart/text()')
    ]
    participant_ispb: Annotated[Ispb, XmlPath(f'{PATH_E}/ISPBPart/text()')]
    original_slb_control_number: Annotated[SlbControlNumber | None, XmlPath(f'{PATH_E}/NumCtrlSLBOr/text()')] = None
    partner_cnpj: Annotated[Cnpj | None, XmlPath(f'{PATH_E}/CNPJConv/text()')] = None
    slb_purpose: Annotated[SlbPurpose, XmlPath(f'{PATH_E}/FinlddSLB/text()')]
    amount: Annotated[Decimal, XmlPath(f'{PATH_E}/VlrLanc/text()')]
    priority: Annotated[Priority | None, XmlPath(f'{PATH_E}/NivelPref/text()')] = None
    description: Annotated[Description, XmlPath(f'{PATH_E}/Hist/text()')]
    settlement_date: Annotated[date, XmlPath(f'{PATH_E}/DtMovto/text()')]

    general_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH_E}/@CodErro')] = None
    participant_institution_control_number_error_code: Annotated[
        ErrorCode | None, XmlPath(f'{PATH_E}/NumCtrlPart/@CodErro')
    ] = None
    participant_ispb_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH_E}/ISPBPart/@CodErro')] = None
    original_slb_control_number_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH_E}/NumCtrlSLBOr/@CodErro')] = (
        None
    )
    partner_cnpj_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH_E}/CNPJConv/@CodErro')] = None
    slb_purpose_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH_E}/FinlddSLB/@CodErro')] = None
    amount_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH_E}/VlrLanc/@CodErro')] = None
    priority_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH_E}/NivelPref/@CodErro')] = None
    description_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH_E}/Hist/@CodErro')] = None
    settlement_date_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH_E}/DtMovto/@CodErro')] = None
