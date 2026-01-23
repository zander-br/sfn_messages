from datetime import date, datetime
from decimal import Decimal
from typing import Annotated, ClassVar, Literal

from pydantic import Field

from sfn_messages.core.models import BaseMessage, BaseSubMessage, XmlPath
from sfn_messages.core.types import (
    Cnpj,
    CreditDebitType,
    ErrorCode,
    InformationType,
    Ispb,
    LdlControlNumber,
    ParticipantIdentifier,
)

PATH = 'DOC/SISMSG/LDL0001'
PATH_GROUP = 'Grupo_LDL0001_ResultLiqd'
PATH_E = 'DOC/SISMSG/LDL0001E'
XML_NAMESPACE = 'http://www.bcb.gov.br/SPB/LDL0001.xsd'
XML_NAMESPACE_ERROR = 'http://www.bcb.gov.br/SPB/LDL0001E.xsd'


class InformationNetResult(BaseSubMessage):
    cnpj: Annotated[Cnpj, XmlPath(f'{PATH_GROUP}/CNPJNLiqdant/text()')]
    participant_identifier: Annotated[ParticipantIdentifier | None, XmlPath(f'{PATH_GROUP}/IdentdPartCamr/text()')] = (
        None
    )
    amount: Annotated[Decimal, XmlPath(f'{PATH_GROUP}/VlrResultLiqdNLiqdant/text()')]


class LDL0001(BaseMessage):
    XML_NAMESPACE: ClassVar[str | None] = XML_NAMESPACE

    message_code: Annotated[Literal['LDL0001'], XmlPath(f'{PATH}/CodMsg/text()')] = 'LDL0001'
    ldl_control_number: Annotated[LdlControlNumber, XmlPath(f'{PATH}/NumCtrlLDL/text()')]
    ldl_ispb: Annotated[Ispb, XmlPath(f'{PATH}/ISPBLDL/text()')]
    institution_ispb: Annotated[Ispb, XmlPath(f'{PATH}/ISPBIF/text()')]
    information_type: Annotated[InformationType, XmlPath(f'{PATH}/TpInf/text()')]
    liquidation_date: Annotated[date, XmlPath(f'{PATH}/DtLiquid/text()')]
    amount: Annotated[Decimal, XmlPath(f'{PATH}/VlrLanc/text()')]
    credit_debit_type: Annotated[CreditDebitType, XmlPath(f'{PATH}/TpDeb_Cred/text()')]
    net_result_group: Annotated[list[InformationNetResult], XmlPath(f'{PATH}')] = Field(default_factory=list)
    ldl_timestamp: Annotated[datetime, XmlPath(f'{PATH}/DtHrLDL/text()')]
    settlement_date: Annotated[date, XmlPath(f'{PATH}/DtMovto/text()')]


class InformationNetResultError(BaseSubMessage):
    cnpj: Annotated[Cnpj, XmlPath(f'{PATH_GROUP}/CNPJNLiqdant/text()')]
    participant_identifier: Annotated[ParticipantIdentifier | None, XmlPath(f'{PATH_GROUP}/IdentdPartCamr/text()')] = (
        None
    )
    amount: Annotated[Decimal, XmlPath(f'{PATH_GROUP}/VlrResultLiqdNLiqdant/text()')]

    cnpj_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH_GROUP}/CNPJNLiqdant/@CodErro')] = None
    participant_identifier_error_code: Annotated[
        ErrorCode | None, XmlPath(f'{PATH_GROUP}/IdentdPartCamr/@CodErro')
    ] = None
    amount_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH_GROUP}/VlrResultLiqdNLiqdant/@CodErro')] = None


class LDL0001E(BaseMessage):
    XML_NAMESPACE: ClassVar[str | None] = XML_NAMESPACE_ERROR

    message_code: Annotated[Literal['LDL0001'], XmlPath(f'{PATH_E}/CodMsg/text()')] = 'LDL0001'
    ldl_control_number: Annotated[LdlControlNumber, XmlPath(f'{PATH_E}/NumCtrlLDL/text()')]
    ldl_ispb: Annotated[Ispb, XmlPath(f'{PATH_E}/ISPBLDL/text()')]
    institution_ispb: Annotated[Ispb, XmlPath(f'{PATH_E}/ISPBIF/text()')]
    information_type: Annotated[InformationType, XmlPath(f'{PATH_E}/TpInf/text()')]
    liquidation_date: Annotated[date, XmlPath(f'{PATH_E}/DtLiquid/text()')]
    amount: Annotated[Decimal, XmlPath(f'{PATH_E}/VlrLanc/text()')]
    credit_debit_type: Annotated[CreditDebitType, XmlPath(f'{PATH_E}/TpDeb_Cred/text()')]
    net_result_group: Annotated[list[InformationNetResultError], XmlPath(f'{PATH_E}')] = Field(default_factory=list)
    ldl_timestamp: Annotated[datetime, XmlPath(f'{PATH_E}/DtHrLDL/text()')]
    settlement_date: Annotated[date, XmlPath(f'{PATH_E}/DtMovto/text()')]

    general_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH_E}/NumCtrlLDL/@CodErro')] = None
    ldl_control_number_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH_E}/NumCtrlLDL/@CodErro')]
    ldl_ispb_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH_E}/ISPBLDL/@CodErro')] = None
    institution_ispb_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH_E}/ISPBIF/@CodErro')] = None
    information_type_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH_E}/TpInf/@CodErro')] = None
    liquidation_date_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH_E}/DtLiquid/@CodErro')] = None
    amount_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH_E}/VlrLanc/@CodErro')] = None
    credit_debit_type_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH_E}/TpDeb_Cred/@CodErro')] = None
    ldl_timestamp_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH_E}/DtHrLDL/@CodErro')] = None
    settlement_date_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH_E}/DtMovto/@CodErro')] = None
