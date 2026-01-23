from datetime import date, datetime
from decimal import Decimal
from typing import Annotated, ClassVar, Literal

from pydantic import Field

from sfn_messages.core.models import BaseMessage, BaseSubMessage, XmlPath
from sfn_messages.core.types import (
    Cnpj,
    ErrorCode,
    InstitutionControlNumber,
    Ispb,
    LdlControlNumber,
    LdlSettlementStatus,
    ParticipantIdentifier,
    StrControlNumber,
)

PATH = 'DOC/SISMSG/LDL0014'
PATH_GROUP = 'Grupo_LDL0014_Dep'
PATH_R1 = 'DOC/SISMSG/LDL0014R1'
PATH_R2 = 'DOC/SISMSG/LDL0014R2'
PATH_GROUP_R2 = 'Grupo_LDL0014R2_Dep'
PATH_E = 'DOC/SISMSG/LDL0014'
XML_NAMESPACE = 'http://www.bcb.gov.br/SPB/LDL0014.xsd'
XML_NAMESPACE_ERROR = 'http://www.bcb.gov.br/SPB/LDL0014E.xsd'


class DepositGroup(BaseSubMessage):
    cnpj: Annotated[Cnpj, XmlPath(f'{PATH_GROUP}/CNPJNLiqdant/text()')]
    participant_identifier: Annotated[ParticipantIdentifier | None, XmlPath(f'{PATH_GROUP}/IdentdPartCamr/text()')] = (
        None
    )
    amount: Annotated[Decimal, XmlPath(f'{PATH_GROUP}/VlrNLiqdant/text()')]
    original_ldl_acceptance_control_number: Annotated[
        InstitutionControlNumber, XmlPath(f'{PATH_GROUP}/NumCtrlActeLDLOr/text()')
    ]
    original_if_request_control_number: Annotated[
        InstitutionControlNumber, XmlPath(f'{PATH_GROUP}/NumCtrlReqIFOr/text()')
    ]


class LDL0014(BaseMessage):
    XML_NAMESPACE: ClassVar[str | None] = XML_NAMESPACE

    message_code: Annotated[Literal['LDL0014'], XmlPath(f'{PATH}/CodMsg/text()')] = 'LDL0014'
    institution_control_number: Annotated[InstitutionControlNumber, XmlPath(f'{PATH}/NumCtrlIF/text()')]
    original_ldl_control_number: Annotated[LdlControlNumber, XmlPath(f'{PATH}/NumCtrlLDLOr/text()')]
    institution_ispb: Annotated[Ispb, XmlPath(f'{PATH}/ISPBIF/text()')]
    ldl_ispb: Annotated[Ispb, XmlPath(f'{PATH}/ISPBLDL/text()')]
    amount: Annotated[Decimal, XmlPath(f'{PATH}/VlrLanc/text()')]
    deposit_group: Annotated[list[DepositGroup], XmlPath(f'{PATH}')] = Field(default_factory=list)
    settlement_date: Annotated[date, XmlPath(f'{PATH}/DtMovto/text()')]


class LDL0014R1(BaseMessage):
    XML_NAMESPACE: ClassVar[str | None] = XML_NAMESPACE

    message_code: Annotated[Literal['LDL0014R1'], XmlPath(f'{PATH_R1}/CodMsg/text()')] = 'LDL0014R1'
    institution_control_number: Annotated[InstitutionControlNumber, XmlPath(f'{PATH_R1}/NumCtrlIF/text()')]
    institution_ispb: Annotated[Ispb, XmlPath(f'{PATH_R1}/ISPBIF/text()')]
    str_control_number: Annotated[StrControlNumber, XmlPath(f'{PATH_R1}/NumCtrlSTR/text()')]
    ldl_settlement_status: Annotated[LdlSettlementStatus, XmlPath(f'{PATH_R1}/SitLancLDL/text()')]
    settlement_timestamp: Annotated[datetime, XmlPath(f'{PATH_R1}/DtHrSit/text()')]
    settlement_date: Annotated[date, XmlPath(f'{PATH_R1}/DtMovto/text()')]


class DepositGroupR2(BaseSubMessage):
    cnpj: Annotated[Cnpj, XmlPath(f'{PATH_GROUP_R2}/CNPJNLiqdant/text()')]
    participant_identifier: Annotated[
        ParticipantIdentifier | None, XmlPath(f'{PATH_GROUP_R2}/IdentdPartCamr/text()')
    ] = None
    amount: Annotated[Decimal, XmlPath(f'{PATH_GROUP_R2}/VlrNLiqdant/text()')]
    original_ldl_acceptance_control_number: Annotated[
        str | None, XmlPath(f'{PATH_GROUP_R2}/NumCtrlActeLDLOr/text()')
    ] = None


class LDL0014R2(BaseMessage):
    XML_NAMESPACE: ClassVar[str | None] = XML_NAMESPACE

    message_code: Annotated[Literal['LDL0014R2'], XmlPath(f'{PATH_R2}/CodMsg/text()')] = 'LDL0014R2'
    str_control_number: Annotated[StrControlNumber, XmlPath(f'{PATH_R2}/NumCtrlSTR/text()')]
    vendor_timestamp: Annotated[datetime, XmlPath(f'{PATH_R2}/DtHrBC/text()')]
    original_ldl_control_number: Annotated[LdlControlNumber, XmlPath(f'{PATH_R2}/NumCtrlLDLOr/text()')]
    institution_ispb: Annotated[Ispb, XmlPath(f'{PATH_R2}/ISPBIF/text()')]
    ldl_ispb: Annotated[Ispb, XmlPath(f'{PATH_R2}/ISPBLDL/text()')]
    amount: Annotated[Decimal, XmlPath(f'{PATH_R2}/VlrLanc/text()')]
    deposit_group: Annotated[list[DepositGroupR2], XmlPath(f'{PATH_R2}')] = Field(default_factory=list)
    settlement_date: Annotated[date, XmlPath(f'{PATH_R2}/DtMovto/text()')]


class DepositGroupError(BaseSubMessage):
    cnpj: Annotated[Cnpj | None, XmlPath(f'{PATH_GROUP}/CNPJNLiqdant/text()')] = None
    participant_identifier: Annotated[ParticipantIdentifier | None, XmlPath(f'{PATH_GROUP}/IdentdPartCamr/text()')] = (
        None
    )
    amount: Annotated[Decimal | None, XmlPath(f'{PATH_GROUP}/VlrNLiqdant/text()')] = None
    original_ldl_acceptance_control_number: Annotated[
        InstitutionControlNumber | None, XmlPath(f'{PATH_GROUP}/NumCtrlActeLDLOr/text()')
    ] = None
    original_if_request_control_number: Annotated[
        InstitutionControlNumber | None, XmlPath(f'{PATH_GROUP}/NumCtrlReqIFOr/text()')
    ] = None

    cnpj_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH_GROUP}/CNPJNLiqdant/@CodErro')] = None
    participant_identifier_error_code: Annotated[
        ErrorCode | None, XmlPath(f'{PATH_GROUP}/IdentdPartCamr/@CodErro')
    ] = None
    amount_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH_GROUP}/VlrNLiqdant/@CodErro')] = None
    original_ldl_acceptance_control_number_error_code: Annotated[
        ErrorCode | None, XmlPath(f'{PATH_GROUP}/NumCtrlActeLDLOr/@CodErro')
    ] = None
    original_if_request_control_number_error_code: Annotated[
        ErrorCode | None, XmlPath(f'{PATH_GROUP}/NumCtrlReqIFOr/@CodErro')
    ] = None


class LDL0014E(BaseMessage):
    XML_NAMESPACE: ClassVar[str | None] = XML_NAMESPACE_ERROR

    message_code: Annotated[Literal['LDL0014E'], XmlPath(f'{PATH_E}/CodMsg/text()')] = 'LDL0014E'
    institution_control_number: Annotated[InstitutionControlNumber | None, XmlPath(f'{PATH_E}/NumCtrlIF/text()')] = (
        None
    )
    original_ldl_control_number: Annotated[LdlControlNumber | None, XmlPath(f'{PATH_E}/NumCtrlLDLOr/text()')] = None
    institution_ispb: Annotated[Ispb | None, XmlPath(f'{PATH_E}/ISPBIF/text()')] = None
    ldl_ispb: Annotated[Ispb | None, XmlPath(f'{PATH_E}/ISPBLDL/text()')] = None
    amount: Annotated[Decimal | None, XmlPath(f'{PATH_E}/VlrLanc/text()')] = None
    deposit_group: Annotated[list[DepositGroupError], XmlPath(f'{PATH_E}')] = Field(default_factory=list)
    settlement_date: Annotated[date | None, XmlPath(f'{PATH_E}/DtMovto/text()')] = None

    general_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH_E}/@CodErro')] = None
    institution_control_number_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH_E}/NumCtrlIF/@CodErro')] = None
    original_ldl_control_number_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH_E}/NumCtrlLDLOr/@CodErro')] = (
        None
    )
    institution_ispb_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH_E}/ISPBIF/@CodErro')] = None
    ldl_ispb_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH_E}/ISPBLDL/@CodErro')] = None
    amount_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH_E}/VlrLanc/@CodErro')] = None
    settlement_date_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH_E}/DtMovto/@CodErro')] = None
