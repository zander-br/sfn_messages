from datetime import date, datetime, time
from decimal import Decimal
from typing import Annotated, ClassVar, Literal

from sfn_messages.core.models import BaseMessage, BaseSubMessage, XmlPath
from sfn_messages.core.types import (
    AccountNumber,
    Branch,
    Cnpj,
    Cpf,
    Description,
    ErrorCode,
    InstitutionControlNumber,
    Ispb,
    Name,
    Priority,
    StrControlNumber,
    StrSettlementStatus,
)

from .types import PortabilityNumber

PATH = 'DOC/SISMSG/STR0047'
PATH_DEBIT_GROUP = 'Grupo_STR0047_AgtFinancDebtd'
PATH_CREDIT_GROUP = 'Grupo_STR0047_AgtFinancCredtd'
PATH_R1 = 'DOC/SISMSG/STR0047R1'
PATH_R2 = 'DOC/SISMSG/STR0047R2'
PATH_R2_DEBIT_GROUP = 'Grupo_STR0047R2_AgtFinancDebtd'
PATH_R2_CREDIT_GROUP = 'Grupo_STR0047R2_AgtFinancCredtd'
PATH_R3 = 'DOC/SISMSG/STR0047R3'
PATH_R3_DEBIT_GROUP = 'Grupo_STR0047R3_AgtFinancDebtd'
PATH_R3_CREDIT_GROUP = 'Grupo_STR0047R3_AgtFinancCredtd'
PATH_E = 'DOC/SISMSG/STR0047'
XML_NAMESPACE = 'http://www.bcb.gov.br/SPB/STR0047.xsd'
XML_NAMESPACE_ERROR = 'http://www.bcb.gov.br/SPB/STR0047E.xsd'


class FinancialAgentDebitedGroup(BaseSubMessage):
    debtor_account_number: Annotated[AccountNumber, XmlPath(f'{PATH_DEBIT_GROUP}/CtDebtd/text()')]
    debtor_document: Annotated[Cnpj | Cpf, XmlPath(f'{PATH_DEBIT_GROUP}/CNPJ_CPFCliDebtd/text()')]
    debtor_name: Annotated[Name, XmlPath(f'{PATH_DEBIT_GROUP}/NomeCliDebtd/text()')]


class FinancialAgentCreditorGroup(BaseSubMessage):
    creditor_account_number: Annotated[AccountNumber | None, XmlPath(f'{PATH_CREDIT_GROUP}/CtCredtd/text()')]
    creditor_document: Annotated[Cnpj | None, XmlPath(f'{PATH_CREDIT_GROUP}/CNPJCliCredtd/text()')]
    creditor_name: Annotated[Name | None, XmlPath(f'{PATH_CREDIT_GROUP}/NomCliCredtd/text()')]


class STR0047(BaseMessage):
    XML_NAMESPACE: ClassVar[str | None] = XML_NAMESPACE

    message_code: Annotated[Literal['STR0047'], XmlPath(f'{PATH}/CodMsg/text()')] = 'STR0047'
    institution_control_number: Annotated[InstitutionControlNumber, XmlPath(f'{PATH}/NumCtrlIF/text()')]
    debtor_institution_ispb: Annotated[Ispb, XmlPath(f'{PATH}/ISPBIFDebtd/text()')]
    debtor_branch: Annotated[Branch | None, XmlPath(f'{PATH}/AgDebtd/text()')] = None
    financial_debit_group: Annotated[FinancialAgentDebitedGroup | None, XmlPath(f'{PATH}')] = None
    creditor_institution_ispb: Annotated[Ispb, XmlPath(f'{PATH}/ISPBIFCredtd/text()')]
    creditor_branch: Annotated[Branch, XmlPath(f'{PATH}/AgCredtd/text()')]
    financial_credit_group: Annotated[FinancialAgentCreditorGroup | None, XmlPath(f'{PATH}')] = None
    amount: Annotated[Decimal, XmlPath(f'{PATH}/VlrLanc/text()')]
    portability_number: Annotated[PortabilityNumber, XmlPath(f'{PATH}/NUPortdd/text()')]
    provider_ispb: Annotated[Ispb, XmlPath(f'{PATH}/ISPBPrestd/text()')]
    description: Annotated[Description | None, XmlPath(f'{PATH}/Hist/text()')] = None
    priority: Annotated[Priority | None, XmlPath(f'{PATH}/NivelPref/text()')] = None
    scheduled_date: Annotated[date | None, XmlPath(f'{PATH}/DtAgendt/text()')] = None
    scheduled_time: Annotated[time | None, XmlPath(f'{PATH}/HrAgendt/text()')] = None
    settlement_date: Annotated[date, XmlPath(f'{PATH}/DtMovto/text()')]


class STR0047R1(BaseMessage):
    XML_NAMESPACE: ClassVar[str | None] = XML_NAMESPACE

    message_code: Annotated[Literal['STR0047R1'], XmlPath(f'{PATH_R1}/CodMsg/text()')] = 'STR0047R1'
    institution_control_number: Annotated[InstitutionControlNumber, XmlPath(f'{PATH_R1}/NumCtrlIF/text()')]
    debtor_institution_ispb: Annotated[Ispb, XmlPath(f'{PATH_R1}/ISPBIFDebtd/text()')]
    str_control_number: Annotated[StrControlNumber, XmlPath(f'{PATH_R1}/NumCtrlSTR/text()')]
    str_settlement_status: Annotated[StrSettlementStatus, XmlPath(f'{PATH_R1}/SitLancSTR/text()')]
    settlement_timestamp: Annotated[datetime, XmlPath(f'{PATH_R1}/DtHrSit/text()')]
    settlement_date: Annotated[date, XmlPath(f'{PATH_R1}/DtMovto/text()')]


class FinancialAgentDebitedR2Group(BaseSubMessage):
    debtor_account_number: Annotated[AccountNumber, XmlPath(f'{PATH_R2_DEBIT_GROUP}/CtDebtd/text()')]
    debtor_document: Annotated[Cnpj | Cpf, XmlPath(f'{PATH_R2_DEBIT_GROUP}/CNPJ_CPFCliDebtd/text()')]
    debtor_name: Annotated[Name, XmlPath(f'{PATH_R2_DEBIT_GROUP}/NomeCliDebtd/text()')]


class FinancialAgentCreditorR2Group(BaseSubMessage):
    creditor_account_number: Annotated[AccountNumber, XmlPath(f'{PATH_R2_CREDIT_GROUP}/CtCredtd/text()')]
    creditor_document: Annotated[Cnpj, XmlPath(f'{PATH_R2_CREDIT_GROUP}/CNPJCliCredtd/text()')]
    creditor_name: Annotated[Name, XmlPath(f'{PATH_R2_CREDIT_GROUP}/NomCliCredtd/text()')]


class STR0047R2(BaseMessage):
    XML_NAMESPACE: ClassVar[str | None] = XML_NAMESPACE

    message_code: Annotated[Literal['STR0047R2'], XmlPath(f'{PATH_R2}/CodMsg/text()')] = 'STR0047R2'
    str_control_number: Annotated[StrControlNumber, XmlPath(f'{PATH_R2}/NumCtrlSTR/text()')]
    vendor_timestamp: Annotated[datetime, XmlPath(f'{PATH_R2}/DtHrBC/text()')]
    debtor_institution_ispb: Annotated[Ispb, XmlPath(f'{PATH_R2}/ISPBIFDebtd/text()')]
    debtor_branch: Annotated[Branch | None, XmlPath(f'{PATH_R2}/AgDebtd/text()')] = None
    financial_debit_group: Annotated[FinancialAgentDebitedR2Group | None, XmlPath(f'{PATH_R2}')] = None
    creditor_institution_ispb: Annotated[Ispb, XmlPath(f'{PATH_R2}/ISPBIFCredtd/text()')]
    creditor_branch: Annotated[Branch, XmlPath(f'{PATH_R2}/AgCredtd/text()')]
    financial_credit_group: Annotated[FinancialAgentCreditorR2Group | None, XmlPath(f'{PATH_R2}')] = None
    amount: Annotated[Decimal, XmlPath(f'{PATH_R2}/VlrLanc/text()')]
    portability_number: Annotated[PortabilityNumber, XmlPath(f'{PATH_R2}/NUPortdd/text()')]
    provider_ispb: Annotated[Ispb, XmlPath(f'{PATH_R2}/ISPBPrestd/text()')]
    description: Annotated[Description | None, XmlPath(f'{PATH_R2}/Hist/text()')] = None
    settlement_date: Annotated[date, XmlPath(f'{PATH_R2}/DtMovto/text()')]


class FinancialAgentDebitedR3Group(BaseSubMessage):
    debtor_account_number: Annotated[AccountNumber, XmlPath(f'{PATH_R3_DEBIT_GROUP}/CtDebtd/text()')]
    debtor_document: Annotated[Cnpj | Cpf, XmlPath(f'{PATH_R3_DEBIT_GROUP}/CNPJ_CPFCliDebtd/text()')]
    debtor_name: Annotated[Name, XmlPath(f'{PATH_R3_DEBIT_GROUP}/NomeCliDebtd/text()')]


class FinancialAgentCreditorR3Group(BaseSubMessage):
    creditor_account_number: Annotated[AccountNumber, XmlPath(f'{PATH_R3_CREDIT_GROUP}/CtCredtd/text()')]
    creditor_document: Annotated[Cnpj, XmlPath(f'{PATH_R3_CREDIT_GROUP}/CNPJCliCredtd/text()')]
    creditor_name: Annotated[Name, XmlPath(f'{PATH_R3_CREDIT_GROUP}/NomCliCredtd/text()')]


class STR0047R3(BaseMessage):
    XML_NAMESPACE: ClassVar[str | None] = XML_NAMESPACE

    message_code: Annotated[Literal['STR0047R3'], XmlPath(f'{PATH_R3}/CodMsg/text()')] = 'STR0047R3'
    str_control_number: Annotated[StrControlNumber, XmlPath(f'{PATH_R3}/NumCtrlSTR/text()')]
    vendor_timestamp: Annotated[datetime, XmlPath(f'{PATH_R3}/DtHrBC/text()')]
    debtor_institution_ispb: Annotated[Ispb, XmlPath(f'{PATH_R3}/ISPBIFDebtd/text()')]
    debtor_branch: Annotated[Branch | None, XmlPath(f'{PATH_R3}/AgDebtd/text()')] = None
    financial_debit_group: Annotated[FinancialAgentDebitedR3Group | None, XmlPath(f'{PATH_R3}')] = None
    creditor_institution_ispb: Annotated[Ispb, XmlPath(f'{PATH_R3}/ISPBIFCredtd/text()')]
    creditor_branch: Annotated[Branch, XmlPath(f'{PATH_R3}/AgCredtd/text()')]
    financial_credit_group: Annotated[FinancialAgentCreditorR3Group | None, XmlPath(f'{PATH_R3}')] = None
    amount: Annotated[Decimal, XmlPath(f'{PATH_R3}/VlrLanc/text()')]
    portability_number: Annotated[PortabilityNumber, XmlPath(f'{PATH_R3}/NUPortdd/text()')]
    provider_ispb: Annotated[Ispb, XmlPath(f'{PATH_R3}/ISPBPrestd/text()')]
    description: Annotated[Description | None, XmlPath(f'{PATH_R3}/Hist/text()')] = None
    settlement_date: Annotated[date, XmlPath(f'{PATH_R3}/DtMovto/text()')]


class FinancialAgentDebitedGroupError(BaseSubMessage):
    debtor_account_number: Annotated[AccountNumber | None, XmlPath(f'{PATH_DEBIT_GROUP}/CtDebtd/text()')] = None
    debtor_document: Annotated[Cnpj | Cpf | None, XmlPath(f'{PATH_DEBIT_GROUP}/CNPJ_CPFCliDebtd/text()')] = None
    debtor_name: Annotated[Name | None, XmlPath(f'{PATH_DEBIT_GROUP}/NomeCliDebtd/text()')] = None

    debtor_account_number_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH_DEBIT_GROUP}/CtDebtd/@CodErro')] = (
        None
    )
    debtor_document_error_code: Annotated[
        ErrorCode | Cpf | None, XmlPath(f'{PATH_DEBIT_GROUP}/CNPJ_CPFCliDebtd/@CodErro')
    ] = None
    debtor_name_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH_DEBIT_GROUP}/NomeCliDebtd/@CodErro')] = None


class FinancialAgentCreditorGroupError(BaseSubMessage):
    creditor_account_number: Annotated[AccountNumber | None, XmlPath(f'{PATH_CREDIT_GROUP}/CtCredtd/text()')] = None
    creditor_document: Annotated[Cnpj | None, XmlPath(f'{PATH_CREDIT_GROUP}/CNPJCliCredtd/text()')] = None
    creditor_name: Annotated[Name | None, XmlPath(f'{PATH_CREDIT_GROUP}/NomCliCredtd/text()')] = None

    creditor_account_number_error_code: Annotated[
        ErrorCode | None, XmlPath(f'{PATH_CREDIT_GROUP}/CtCredtd/@CodErro')
    ] = None
    creditor_document_error_code: Annotated[
        ErrorCode | None, XmlPath(f'{PATH_CREDIT_GROUP}/CNPJCliCredtd/@CodErro')
    ] = None
    creditor_name_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH_CREDIT_GROUP}/NomCliCredtd/@CodErro')] = None


class STR0047E(BaseMessage):
    XML_NAMESPACE: ClassVar[str | None] = XML_NAMESPACE_ERROR

    message_code: Annotated[Literal['STR0047E'], XmlPath(f'{PATH}/CodMsg/text()')] = 'STR0047E'
    institution_control_number: Annotated[InstitutionControlNumber | None, XmlPath(f'{PATH}/NumCtrlIF/text()')] = None
    debtor_institution_ispb: Annotated[Ispb | None, XmlPath(f'{PATH}/ISPBIFDebtd/text()')] = None
    debtor_branch: Annotated[Branch | None, XmlPath(f'{PATH}/AgDebtd/text()')] = None
    financial_debit_group: Annotated[FinancialAgentDebitedGroupError | None, XmlPath(f'{PATH}')] = None
    creditor_institution_ispb: Annotated[Ispb | None, XmlPath(f'{PATH}/ISPBIFCredtd/text()')] = None
    creditor_branch: Annotated[Branch | None, XmlPath(f'{PATH}/AgCredtd/text()')] = None
    financial_credit_group: Annotated[FinancialAgentCreditorGroupError | None, XmlPath(f'{PATH}')] = None
    amount: Annotated[Decimal | None, XmlPath(f'{PATH}/VlrLanc/text()')] = None
    portability_number: Annotated[PortabilityNumber | None, XmlPath(f'{PATH}/NUPortdd/text()')] = None
    provider_ispb: Annotated[Ispb | None, XmlPath(f'{PATH}/ISPBPrestd/text()')] = None
    description: Annotated[Description | None, XmlPath(f'{PATH}/Hist/text()')] = None
    priority: Annotated[Priority | None, XmlPath(f'{PATH}/NivelPref/text()')] = None
    scheduled_date: Annotated[date | None, XmlPath(f'{PATH}/DtAgendt/text()')] = None
    scheduled_time: Annotated[time | None, XmlPath(f'{PATH}/HrAgendt/text()')] = None
    settlement_date: Annotated[date | None, XmlPath(f'{PATH}/DtMovto/text()')] = None

    general_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH}/@CodErro')] = None
    institution_control_number_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH}/NumCtrlIF/@CodErro')] = None
    debtor_institution_ispb_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH}/ISPBIFDebtd/@CodErro')] = None
    debtor_branch_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH}/AgDebtd/@CodErro')] = None
    creditor_institution_ispb_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH}/ISPBIFCredtd/@CodErro')] = None
    creditor_branch_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH}/AgCredtd/@CodErro')] = None
    amount_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH}/VlrLanc/@CodErro')] = None
    portability_number_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH}/NUPortdd/@CodErro')] = None
    provider_ispb_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH}/ISPBPrestd/@CodErro')] = None
    description_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH}/Hist/@CodErro')] = None
    priority_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH}/NivelPref/@CodErro')] = None
    scheduled_date_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH}/DtAgendt/@CodErro')] = None
    scheduled_time_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH}/HrAgendt/@CodErro')] = None
    settlement_date_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH}/DtMovto/@CodErro')] = None
