from datetime import date, datetime, time
from decimal import Decimal
from typing import Annotated, ClassVar, Literal

from sfn_messages.core.models import BaseMessage, XmlPath
from sfn_messages.core.types import (
    Branch,
    Description,
    ErrorCode,
    InstitutionControlNumber,
    Ispb,
    Priority,
    StrControlNumber,
    StrSettlementStatus,
    TransactionId,
)

from .types import InstitutionPurpose

PATH = 'DOC/SISMSG/STR0004'
PATH_R1 = 'DOC/SISMSG/STR0004R1'
PATH_R2 = 'DOC/SISMSG/STR0004R2'
PATH_E = 'DOC/SISMSG/STR0004'
XML_NAMESPACE = 'http://www.bcb.gov.br/SPB/STR0004.xsd'
XML_NAMESPACE_ERROR = 'http://www.bcb.gov.br/SPB/STR0004E.xsd'


class STR0004(BaseMessage):
    XML_NAMESPACE: ClassVar[str | None] = XML_NAMESPACE

    message_code: Annotated[Literal['STR0004'], XmlPath(f'{PATH}/CodMsg/text()')] = 'STR0004'
    institution_control_number: Annotated[InstitutionControlNumber, XmlPath(f'{PATH}/NumCtrlIF/text()')]
    debtor_institution_ispb: Annotated[Ispb, XmlPath(f'{PATH}/ISPBIFDebtd/text()')]
    creditor_institution_ispb: Annotated[Ispb, XmlPath(f'{PATH}/ISPBIFCredtd/text()')]
    creditor_branch: Annotated[Branch | None, XmlPath(f'{PATH}/AgCredtd/text()')] = None
    purpose: Annotated[InstitutionPurpose, XmlPath(f'{PATH}/FinlddIF/text()')]
    transaction_id: Annotated[TransactionId | None, XmlPath(f'{PATH}/CodIdentdTransf/text()')] = None
    amount: Annotated[Decimal, XmlPath(f'{PATH}/VlrLanc/text()')]
    description: Annotated[Description, XmlPath(f'{PATH}/Hist/text()')]
    scheduled_date: Annotated[date | None, XmlPath(f'{PATH}/DtAgendt/text()')] = None
    scheduled_time: Annotated[time | None, XmlPath(f'{PATH}/HrAgendt/text()')] = None
    priority: Annotated[Priority | None, XmlPath(f'{PATH}/NivelPref/text()')] = None
    settlement_date: Annotated[date, XmlPath(f'{PATH}/DtMovto/text()')]


class STR0004R1(BaseMessage):
    XML_NAMESPACE: ClassVar[str | None] = XML_NAMESPACE

    message_code: Annotated[Literal['STR0004R1'], XmlPath(f'{PATH_R1}/CodMsg/text()')] = 'STR0004R1'
    institution_control_number: Annotated[InstitutionControlNumber, XmlPath(f'{PATH_R1}/NumCtrlIF/text()')]
    debtor_institution_ispb: Annotated[Ispb, XmlPath(f'{PATH_R1}/ISPBIFDebtd/text()')]
    str_control_number: Annotated[StrControlNumber, XmlPath(f'{PATH_R1}/NumCtrlSTR/text()')]
    str_settlement_status: Annotated[StrSettlementStatus, XmlPath(f'{PATH_R1}/SitLancSTR/text()')]
    settlement_timestamp: Annotated[datetime, XmlPath(f'{PATH_R1}/DtHrSit/text()')]
    settlement_date: Annotated[date, XmlPath(f'{PATH_R1}/DtMovto/text()')]


class STR0004R2(BaseMessage):
    XML_NAMESPACE: ClassVar[str | None] = XML_NAMESPACE

    message_code: Annotated[Literal['STR0004R2'], XmlPath(f'{PATH_R2}/CodMsg/text()')] = 'STR0004R2'
    str_control_number: Annotated[StrControlNumber, XmlPath(f'{PATH_R2}/NumCtrlSTR/text()')]
    vendor_timestamp: Annotated[datetime, XmlPath(f'{PATH_R2}/DtHrBC/text()')]
    debtor_institution_ispb: Annotated[Ispb, XmlPath(f'{PATH_R2}/ISPBIFDebtd/text()')]
    creditor_institution_ispb: Annotated[Ispb, XmlPath(f'{PATH_R2}/ISPBIFCredtd/text()')]
    creditor_branch: Annotated[Branch | None, XmlPath(f'{PATH_R2}/AgCredtd/text()')] = None
    amount: Annotated[Decimal, XmlPath(f'{PATH_R2}/VlrLanc/text()')]
    transaction_id: Annotated[TransactionId | None, XmlPath(f'{PATH_R2}/CodIdentdTransf/text()')] = None
    purpose: Annotated[InstitutionPurpose, XmlPath(f'{PATH_R2}/FinlddIF/text()')]
    description: Annotated[Description, XmlPath(f'{PATH_R2}/Hist/text()')]
    settlement_date: Annotated[date, XmlPath(f'{PATH_R2}/DtMovto/text()')]


class STR0004E(BaseMessage):
    XML_NAMESPACE: ClassVar[str | None] = XML_NAMESPACE_ERROR

    message_code: Annotated[Literal['STR0004E'], XmlPath(f'{PATH_E}/CodMsg/text()')] = 'STR0004E'
    institution_control_number: Annotated[InstitutionControlNumber | None, XmlPath(f'{PATH_E}/NumCtrlIF/text()')] = (
        None
    )
    debtor_institution_ispb: Annotated[Ispb | None, XmlPath(f'{PATH_E}/ISPBIFDebtd/text()')] = None
    creditor_institution_ispb: Annotated[Ispb | None, XmlPath(f'{PATH_E}/ISPBIFCredtd/text()')] = None
    creditor_branch: Annotated[Branch | None, XmlPath(f'{PATH_E}/AgCredtd/text()')] = None
    purpose: Annotated[InstitutionPurpose | None, XmlPath(f'{PATH_E}/FinlddIF/text()')] = None
    transaction_id: Annotated[TransactionId | None, XmlPath(f'{PATH_E}/CodIdentdTransf/text()')] = None
    amount: Annotated[Decimal | None, XmlPath(f'{PATH_E}/VlrLanc/text()')] = None
    description: Annotated[Description | None, XmlPath(f'{PATH_E}/Hist/text()')] = None
    scheduled_date: Annotated[date | None, XmlPath(f'{PATH_E}/DtAgendt/text()')] = None
    scheduled_time: Annotated[time | None, XmlPath(f'{PATH_E}/HrAgendt/text()')] = None
    priority: Annotated[Priority | None, XmlPath(f'{PATH_E}/NivelPref/text()')] = None
    settlement_date: Annotated[date | None, XmlPath(f'{PATH_E}/DtMovto/text()')] = None

    general_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH_E}/@CodErro')] = None
    institution_control_number_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH_E}/NumCtrlIF/@CodErro')] = None
    debtor_institution_ispb_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH_E}/ISPBIFDebtd/@CodErro')] = None
    creditor_institution_ispb_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH_E}/ISPBIFCredtd/@CodErro')] = (
        None
    )
    creditor_branch_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH_E}/AgCredtd/@CodErro')] = None
    purpose_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH_E}/FinlddIF/@CodErro')] = None
    transaction_id_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH_E}/CodIdentdTransf/@CodErro')] = None
    amount_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH_E}/VlrLanc/@CodErro')] = None
    description_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH_E}/Hist/@CodErro')] = None
    scheduled_date_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH_E}/DtAgendt/@CodErro')] = None
    scheduled_time_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH_E}/HrAgendt/@CodErro')] = None
    priority_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH_E}/NivelPref/@CodErro')] = None
    settlement_date_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH_E}/DtMovto/@CodErro')] = None
