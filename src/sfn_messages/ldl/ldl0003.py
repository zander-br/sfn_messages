from datetime import date, datetime
from decimal import Decimal
from typing import Annotated, ClassVar, Literal

from pydantic import Field

from sfn_messages.core.models import BaseMessage, BaseSubMessage, XmlPath
from sfn_messages.core.types import (
    Cnpj,
    CreditDebitType,
    ErrorCode,
    Ispb,
    LdlControlNumber,
    ParticipantIdentifier,
    ReconciliationType,
)

PATH = 'DOC/SISMSG/LDL0003'
PATH_GROUP = 'Grupo_LDL0003_ResultLiqd'
PATH_R1 = 'DOC/SISMSG/LDL0003R1'
PATH_E = 'DOC/SISMSG/LDL0003'
XML_NAMESPACE = 'http://www.bcb.gov.br/SPB/LDL0003.xsd'
XML_NAMESPACE_ERROR = 'http://www.bcb.gov.br/SPB/LDL0003E.xsd'


class NetResult(BaseSubMessage):
    cnpj: Annotated[Cnpj, XmlPath(f'{PATH_GROUP}/CNPJNLiqdant/text()')]
    participant_identifier: Annotated[ParticipantIdentifier | None, XmlPath(f'{PATH_GROUP}/IdentdPartCamr/text()')] = (
        None
    )
    amount: Annotated[Decimal, XmlPath(f'{PATH_GROUP}/VlrResultLiqdNLiqdant/text()')]
    reconciliation_type: Annotated[ReconciliationType, XmlPath(f'{PATH_GROUP}/TpConf_Divg/text()')]


class LDL0003(BaseMessage):
    XML_NAMESPACE: ClassVar[str | None] = XML_NAMESPACE

    message_code: Annotated[Literal['LDL0003'], XmlPath(f'{PATH}/CodMsg/text()')] = 'LDL0003'
    institution_control_number: Annotated[LdlControlNumber, XmlPath(f'{PATH}/NumCtrlIF/text()')]
    institution_ispb: Annotated[Ispb, XmlPath(f'{PATH}/ISPBIF/text()')]
    original_ldl_control_number: Annotated[LdlControlNumber, XmlPath(f'{PATH}/NumCtrlLDLOr/text()')]
    ldl_ispb: Annotated[Ispb, XmlPath(f'{PATH}/ISPBLDL/text()')]
    liquidation_date: Annotated[date, XmlPath(f'{PATH}/DtLiquid/text()')]
    amount: Annotated[Decimal, XmlPath(f'{PATH}/VlrLanc/text()')]
    credit_debit_type: Annotated[CreditDebitType, XmlPath(f'{PATH}/TpDeb_Cred/text()')]
    net_result_group: Annotated[list[NetResult], XmlPath(f'{PATH}')] = Field(default_factory=list)
    institution_timestamp: Annotated[datetime, XmlPath(f'{PATH}/DtHrIF/text()')]
    settlement_date: Annotated[date, XmlPath(f'{PATH}/DtMovto/text()')]


class LDL0003R1(BaseMessage):
    XML_NAMESPACE: ClassVar[str | None] = XML_NAMESPACE

    message_code: Annotated[Literal['LDL0003R1'], XmlPath(f'{PATH_R1}/CodMsg/text()')] = 'LDL0003R1'
    institution_control_number: Annotated[LdlControlNumber, XmlPath(f'{PATH_R1}/NumCtrlIF/text()')]
    ldl_ispb: Annotated[Ispb, XmlPath(f'{PATH_R1}/ISPBLDL/text()')]
    ldl_timestamp: Annotated[datetime, XmlPath(f'{PATH_R1}/DtHrLDL/text()')]
    settlement_date: Annotated[date, XmlPath(f'{PATH_R1}/DtMovto/text()')]


class NetResultError(BaseSubMessage):
    cnpj: Annotated[Cnpj | None, XmlPath(f'{PATH_GROUP}/CNPJNLiqdant/text()')] = None
    participant_identifier: Annotated[ParticipantIdentifier | None, XmlPath(f'{PATH_GROUP}/IdentdPartCamr/text()')] = (
        None
    )
    amount: Annotated[Decimal | None, XmlPath(f'{PATH_GROUP}/VlrResultLiqdNLiqdant/text()')] = None
    reconciliation_type: Annotated[ReconciliationType | None, XmlPath(f'{PATH_GROUP}/TpConf_Divg/text()')] = None

    cnpj_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH_GROUP}/CNPJNLiqdant/@CodErro')] = None
    participant_identifier_error_code: Annotated[
        ErrorCode | None, XmlPath(f'{PATH_GROUP}/IdentdPartCamr/@CodErro')
    ] = None
    amount_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH_GROUP}/VlrResultLiqdNLiqdant/@CodErro')] = None
    reconciliation_type_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH_GROUP}/TpConf_Divg/@CodErro')] = None


class LDL0003E(BaseMessage):
    XML_NAMESPACE: ClassVar[str | None] = XML_NAMESPACE_ERROR

    message_code: Annotated[Literal['LDL0003E'], XmlPath(f'{PATH_E}/CodMsg/text()')] = 'LDL0003E'
    institution_control_number: Annotated[LdlControlNumber | None, XmlPath(f'{PATH_E}/NumCtrlIF/text()')] = None
    institution_ispb: Annotated[Ispb | None, XmlPath(f'{PATH_E}/ISPBIF/text()')] = None
    original_ldl_control_number: Annotated[LdlControlNumber | None, XmlPath(f'{PATH_E}/NumCtrlLDLOr/text()')] = None
    ldl_ispb: Annotated[Ispb | None, XmlPath(f'{PATH_E}/ISPBLDL/text()')] = None
    liquidation_date: Annotated[date | None, XmlPath(f'{PATH_E}/DtLiquid/text()')] = None
    amount: Annotated[Decimal | None, XmlPath(f'{PATH_E}/VlrLanc/text()')] = None
    credit_debit_type: Annotated[CreditDebitType | None, XmlPath(f'{PATH_E}/TpDeb_Cred/text()')] = None
    net_result_group: Annotated[list[NetResultError], XmlPath(f'{PATH_E}')] = Field(default_factory=list)
    institution_timestamp: Annotated[datetime | None, XmlPath(f'{PATH_E}/DtHrIF/text()')] = None
    settlement_date: Annotated[date | None, XmlPath(f'{PATH_E}/DtMovto/text()')] = None

    general_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH_E}/@CodErro')] = None
    institution_control_number_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH_E}/NumCtrlIF/@CodErro')] = None
    institution_ispb_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH_E}/ISPBIF/@CodErro')] = None
    original_ldl_control_number_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH_E}/NumCtrlLDLOr/@CodErro')] = (
        None
    )
    ldl_ispb_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH_E}/ISPBLDL/@CodErro')] = None
    liquidation_date_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH_E}/DtLiquid/@CodErro')] = None
    amount_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH_E}/VlrLanc/@CodErro')] = None
    credit_debit_type_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH_E}/TpDeb_Cred/@CodErro')] = None
    institution_timestamp_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH_E}/DtHrIF/@CodErro')] = None
    settlement_date_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH_E}/DtMovto/@CodErro')] = None
