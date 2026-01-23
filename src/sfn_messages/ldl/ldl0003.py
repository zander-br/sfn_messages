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
PATH_E = 'DOC/SISMSG/LDL0003E'
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
    institution_datetime: Annotated[datetime, XmlPath(f'{PATH}/DtHrIF/text()')]
    settlement_date: Annotated[date, XmlPath(f'{PATH}/DtMovto/text()')]


class LDL0003R1(BaseMessage):
    XML_NAMESPACE: ClassVar[str | None] = XML_NAMESPACE

    message_code: Annotated[Literal['LDL0003R1'], XmlPath(f'{PATH_R1}/CodMsg/text()')] = 'LDL0003R1'
    institution_control_number: Annotated[LdlControlNumber, XmlPath(f'{PATH_R1}/NumCtrlIF/text()')]
    ldl_ispb: Annotated[Ispb, XmlPath(f'{PATH_R1}/ISPBLDL/text()')]
    ldl_timestamp: Annotated[datetime, XmlPath(f'{PATH_R1}/DtHrLDL/text()')]
    settlement_date: Annotated[date, XmlPath(f'{PATH_R1}/DtMovto/text()')]


class NetResultError(BaseSubMessage):
    cnpj: Annotated[Cnpj, XmlPath(f'{PATH_GROUP}/CNPJNLiqdant/text()')]
    participant_identifier: Annotated[ParticipantIdentifier | None, XmlPath(f'{PATH_GROUP}/IdentdPartCamr/text()')] = (
        None
    )
    amount: Annotated[Decimal, XmlPath(f'{PATH_GROUP}/VlrResultLiqdNLiqdant/text()')]
    reconciliation_type: Annotated[ReconciliationType, XmlPath(f'{PATH_GROUP}/TpConf_Divg/text()')]

    cnpj_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH_GROUP}/CNPJNLiqdant/@CodErro')] = None
    participant_identifier_error_code: Annotated[
        ErrorCode | None, XmlPath(f'{PATH_GROUP}/IdentdPartCamr/@CodErro')
    ] = None
    amount_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH_GROUP}/VlrResultLiqdNLiqdant/@CodErro')] = None
    reconciliation_type_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH_GROUP}/TpConf_Divg/@CodErro')] = None


class LDL0003E(BaseMessage):
    XML_NAMESPACE: ClassVar[str | None] = XML_NAMESPACE_ERROR

    message_code: Annotated[Literal['LDL0003'], XmlPath(f'{PATH}/CodMsg/text()')] = 'LDL0003'
    institution_control_number: Annotated[LdlControlNumber, XmlPath(f'{PATH}/NumCtrlIF/text()')]
    institution_ispb: Annotated[Ispb, XmlPath(f'{PATH}/ISPBIF/text()')]
    original_ldl_control_number: Annotated[LdlControlNumber, XmlPath(f'{PATH}/NumCtrlLDLOr/text()')]
    ldl_ispb: Annotated[Ispb, XmlPath(f'{PATH}/ISPBLDL/text()')]
    liquidation_date: Annotated[date, XmlPath(f'{PATH}/DtLiquid/text()')]
    amount: Annotated[Decimal, XmlPath(f'{PATH}/VlrLanc/text()')]
    credit_debit_type: Annotated[CreditDebitType, XmlPath(f'{PATH}/TpDeb_Cred/text()')]
    net_result_group: Annotated[list[NetResult], XmlPath(f'{PATH}')] = Field(default_factory=list)
    institution_datetime: Annotated[datetime, XmlPath(f'{PATH}/DtHrIF/text()')]
    settlement_date: Annotated[date, XmlPath(f'{PATH}/DtMovto/text()')]

    general_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH_E}/@CodErro')] = None
    institution_control_number_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH}/NumCtrlIF/@CodErro')] = None
    institution_ispb_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH}/ISPBIF/@CodErro')] = None
    original_ldl_control_number_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH}/NumCtrlLDLOr/@CodErro')] = (
        None
    )
    ldl_ispb_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH}/ISPBLDL/@CodErro')] = None
    liquidation_date_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH}/DtLiquid/@CodErro')] = None
    amount_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH}/VlrLanc/@CodErro')] = None
    credit_debit_type_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH}/TpDeb_Cred/@CodErro')] = None
    institution_datetime_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH}/DtHrIF/@CodErro')] = None
    settlement_date_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH}/DtMovto/@CodErro')] = None
