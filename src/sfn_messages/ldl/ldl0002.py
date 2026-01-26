from datetime import date, datetime
from decimal import Decimal
from typing import Annotated, ClassVar, Literal

from pydantic import Field

from sfn_messages.core.models import BaseMessage, BaseSubMessage, XmlPath
from sfn_messages.core.types import (
    Cnpj,
    CreditDebitType,
    ErrorCode,
    GridCode,
    InformationSequenceNumber,
    Ispb,
    LdlControlNumber,
    ParticipantIdentifier,
    ProductCode,
)

PATH = 'DOC/SISMSG/LDL0002'
PATH_GROUP = 'Grupo_LDL0002_ResultLiqd'
PATH_R1 = 'DOC/SISMSG/LDL0002R1'
PATH_E = 'DOC/SISMSG/LDL0002'
XML_NAMESPACE = 'http://www.bcb.gov.br/SPB/LDL0002.xsd'
XML_NAMESPACE_ERROR = 'http://www.bcb.gov.br/SPB/LDL0002E.xsd'


class NetResult(BaseSubMessage):
    participant_ispb: Annotated[ParticipantIdentifier | None, XmlPath(f'{PATH_GROUP}/ISPBPart/text()')] = None
    amount: Annotated[Decimal, XmlPath(f'{PATH_GROUP}/VlrLanc/text()')]
    cnpj: Annotated[Cnpj, XmlPath(f'{PATH_GROUP}/CNPJNLiqdant/text()')]
    credit_debit_type: Annotated[CreditDebitType, XmlPath(f'{PATH_GROUP}/TpDeb_Cred/text()')]


class LDL0002(BaseMessage):
    XML_NAMESPACE: ClassVar[str | None] = XML_NAMESPACE

    message_code: Annotated[Literal['LDL0002'], XmlPath(f'{PATH}/CodMsg/text()')] = 'LDL0002'
    ldl_control_number: Annotated[LdlControlNumber, XmlPath(f'{PATH}/NumCtrlLDL/text()')]
    ldl_ispb: Annotated[Ispb, XmlPath(f'{PATH}/ISPBLDL/text()')]
    # Deve ser reiniciado diariamente com o valor 1.
    settlement_cycle_seq_num: Annotated[
        InformationSequenceNumber | None, XmlPath(f'{PATH}/NumSeqCicloLiquid/text()')
    ] = None
    product_code: Annotated[ProductCode | None, XmlPath(f'{PATH}/CodProdt/text()')] = None
    liquidation_date: Annotated[date, XmlPath(f'{PATH}/DtLiquid/text()')]
    code: Annotated[GridCode | None, XmlPath(f'{PATH}/CodGrd/text()')] = None
    net_result_group: Annotated[list[NetResult], XmlPath(f'{PATH}')] = Field(default_factory=list)
    ldl_timestamp: Annotated[datetime, XmlPath(f'{PATH}/DtHrLDL/text()')]
    settlement_date: Annotated[date, XmlPath(f'{PATH}/DtMovto/text()')]


class LDL0002R1(BaseMessage):
    XML_NAMESPACE: ClassVar[str | None] = XML_NAMESPACE

    message_code: Annotated[Literal['LDL0002R1'], XmlPath(f'{PATH_R1}/CodMsg/text()')] = 'LDL0002R1'
    ldl_control_number: Annotated[LdlControlNumber, XmlPath(f'{PATH_R1}/NumCtrlLDL/text()')]
    ldl_ispb: Annotated[Ispb, XmlPath(f'{PATH_R1}/ISPBLDL/text()')]
    vendor_timestamp: Annotated[datetime, XmlPath(f'{PATH_R1}/DtHrBC/text()')]
    settlement_date: Annotated[date, XmlPath(f'{PATH_R1}/DtMovto/text()')]


class NetResultError(BaseSubMessage):
    participant_ispb: Annotated[ParticipantIdentifier | None, XmlPath(f'{PATH_GROUP}/ISPBPart/text()')] = None
    amount: Annotated[Decimal | None, XmlPath(f'{PATH_GROUP}/VlrLanc/text()')] = None
    cnpj: Annotated[Cnpj | None, XmlPath(f'{PATH_GROUP}/CNPJNLiqdant/text()')] = None
    credit_debit_type: Annotated[CreditDebitType | None, XmlPath(f'{PATH_GROUP}/TpDeb_Cred/text()')] = None

    participant_ispb_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH_GROUP}/ISPBPart/@CodErro')] = None
    amount_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH_GROUP}/VlrLanc/@CodErro')] = None
    cnpj_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH_GROUP}/CNPJNLiqdant/@CodErro')] = None
    credit_debit_type_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH_GROUP}/TpDeb_Cred/@CodErro')] = None


class LDL0002E(BaseMessage):
    XML_NAMESPACE: ClassVar[str | None] = XML_NAMESPACE_ERROR

    message_code: Annotated[Literal['LDL0002E'], XmlPath(f'{PATH_E}/CodMsg/text()')] = 'LDL0002E'
    ldl_control_number: Annotated[LdlControlNumber | None, XmlPath(f'{PATH_E}/NumCtrlLDL/text()')] = None
    ldl_ispb: Annotated[Ispb | None, XmlPath(f'{PATH_E}/ISPBLDL/text()')] = None
    settlement_cycle_seq_num: Annotated[
        InformationSequenceNumber | None, XmlPath(f'{PATH_E}/NumSeqCicloLiquid/text()')
    ] = None
    product_code: Annotated[ProductCode | None, XmlPath(f'{PATH_E}/CodProdt/text()')] = None
    liquidation_date: Annotated[date | None, XmlPath(f'{PATH_E}/DtLiquid/text()')] = None
    code: Annotated[GridCode | None, XmlPath(f'{PATH_E}/CodGrd/text()')] = None
    net_result_group: Annotated[list[NetResultError], XmlPath(f'{PATH_E}')] = Field(default_factory=list)
    ldl_timestamp: Annotated[datetime | None, XmlPath(f'{PATH_E}/DtHrLDL/text()')] = None
    settlement_date: Annotated[date | None, XmlPath(f'{PATH_E}/DtMovto/text()')] = None

    general_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH_E}/@CodErro')] = None
    ldl_control_number_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH_E}/NumCtrlLDL/@CodErro')] = None
    ldl_ispb_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH_E}/ISPBLDL/@CodErro')] = None
    settlement_cycle_seq_num_error_code: Annotated[
        ErrorCode | None, XmlPath(f'{PATH_E}/NumSeqCicloLiquid/@CodErro')
    ] = None
    product_code_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH_E}/CodProdt/@CodErro')] = None
    liquidation_date_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH_E}/DtLiquid/@CodErro')] = None
    code_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH_E}/CodGrd/@CodErro')] = None
    ldl_timestamp_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH_E}/DtHrLDL/@CodErro')] = None
    settlement_date_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH_E}/DtMovto/@CodErro')] = None
