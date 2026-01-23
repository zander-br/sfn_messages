from datetime import date, datetime, time
from decimal import Decimal
from typing import Annotated, ClassVar, Literal

from sfn_messages.core.models import BaseMessage, XmlPath
from sfn_messages.core.types import (
    AccountNumber,
    AccountType,
    Branch,
    Cnpj,
    Cpf,
    CreditContractNumber,
    Description,
    ErrorCode,
    InstitutionControlNumber,
    Ispb,
    Name,
    PersonType,
    Priority,
    StrControlNumber,
    StrSettlementStatus,
    TransactionId,
)

from .types import InstitutionPurpose
from .validations import PartyValidations

PATH = 'DOC/SISMSG/STR0007'
PATH_R1 = 'DOC/SISMSG/STR0007R1'
PATH_R2 = 'DOC/SISMSG/STR0007R2'
PATH_E = 'DOC/SISMSG/STR0007'
XML_NAMESPACE = 'http://www.bcb.gov.br/SPB/STR0007.xsd'
XML_NAMESPACE_ERROR = 'http://www.bcb.gov.br/SPB/STR0007E.xsd'


class STR0007(PartyValidations, BaseMessage):
    XML_NAMESPACE: ClassVar[str | None] = XML_NAMESPACE

    document_parties: ClassVar[list[str]] = ['sender', 'creditor']
    account_parties: ClassVar[list[str]] = ['creditor']
    others_enum_value: ClassVar[InstitutionPurpose | None] = InstitutionPurpose.OTHERS
    purpose_attr: ClassVar[str] = 'purpose'
    description_attr: ClassVar[str] = 'description'

    message_code: Annotated[Literal['STR0007'], XmlPath(f'{PATH}/CodMsg/text()')] = 'STR0007'
    institution_control_number: Annotated[InstitutionControlNumber, XmlPath(f'{PATH}/NumCtrlIF/text()')]
    debtor_institution_ispb: Annotated[Ispb, XmlPath(f'{PATH}/ISPBIFDebtd/text()')]
    sender_type: Annotated[PersonType | None, XmlPath(f'{PATH}/TpPessoaRemet/text()')] = None
    sender_document: Annotated[Cnpj | Cpf | None, XmlPath(f'{PATH}/CNPJ_CPFRemet/text()')] = None
    sender_name: Annotated[Name | None, XmlPath(f'{PATH}/NomRemet/text()')] = None
    creditor_institution_ispb: Annotated[Ispb, XmlPath(f'{PATH}/ISPBIFCredtd/text()')]
    creditor_branch: Annotated[Branch | None, XmlPath(f'{PATH}/AgCredtd/text()')] = None
    creditor_account_type: Annotated[AccountType, XmlPath(f'{PATH}/TpCtCredtd/text()')]
    creditor_account_number: Annotated[AccountNumber | None, XmlPath(f'{PATH}/CtCredtd/text()')] = None
    creditor_payment_account_number: Annotated[AccountNumber | None, XmlPath(f'{PATH}/CtPgtoCredtd/text()')] = None
    creditor_type: Annotated[PersonType, XmlPath(f'{PATH}/TpPessoaCredtd/text()')]
    creditor_document: Annotated[Cnpj | Cpf, XmlPath(f'{PATH}/CNPJ_CPFCliCredtd/text()')]
    creditor_name: Annotated[Name, XmlPath(f'{PATH}/NomCliCredtd/text()')]
    credit_contract_number: Annotated[CreditContractNumber | None, XmlPath(f'{PATH}/NumCtrdCredtd/text()')] = None
    amount: Annotated[Decimal, XmlPath(f'{PATH}/VlrLanc/text()')]
    purpose: Annotated[InstitutionPurpose, XmlPath(f'{PATH}/FinlddIF/text()')]
    transaction_id: Annotated[TransactionId | None, XmlPath(f'{PATH}/CodIdentdTransf/text()')] = None
    description: Annotated[Description | None, XmlPath(f'{PATH}/Hist/text()')] = None
    scheduled_date: Annotated[date | None, XmlPath(f'{PATH}/DtAgendt/text()')] = None
    scheduled_time: Annotated[time | None, XmlPath(f'{PATH}/HrAgendt/text()')] = None
    priority: Annotated[Priority | None, XmlPath(f'{PATH}/NivelPref/text()')] = None
    settlement_date: Annotated[date, XmlPath(f'{PATH}/DtMovto/text()')]


class STR0007R1(BaseMessage):
    XML_NAMESPACE: ClassVar[str | None] = XML_NAMESPACE

    message_code: Annotated[Literal['STR0007R1'], XmlPath(f'{PATH_R1}/CodMsg/text()')] = 'STR0007R1'
    institution_control_number: Annotated[InstitutionControlNumber, XmlPath(f'{PATH_R1}/NumCtrlIF/text()')]
    debtor_institution_ispb: Annotated[Ispb, XmlPath(f'{PATH_R1}/ISPBIFDebtd/text()')]
    str_control_number: Annotated[StrControlNumber, XmlPath(f'{PATH_R1}/NumCtrlSTR/text()')]
    str_settlement_status: Annotated[StrSettlementStatus, XmlPath(f'{PATH_R1}/SitLancSTR/text()')]
    settlement_timestamp: Annotated[datetime, XmlPath(f'{PATH_R1}/DtHrSit/text()')]
    settlement_date: Annotated[date, XmlPath(f'{PATH_R1}/DtMovto/text()')]


class STR0007R2(PartyValidations, BaseMessage):
    XML_NAMESPACE: ClassVar[str | None] = XML_NAMESPACE

    document_parties: ClassVar[list[str]] = ['sender', 'creditor']
    account_parties: ClassVar[list[str]] = ['creditor']
    others_enum_value: ClassVar[InstitutionPurpose | None] = InstitutionPurpose.OTHERS
    purpose_attr: ClassVar[str] = 'purpose'
    description_attr: ClassVar[str] = 'description'

    message_code: Annotated[Literal['STR0007R2'], XmlPath(f'{PATH_R2}/CodMsg/text()')] = 'STR0007R2'
    str_control_number: Annotated[StrControlNumber, XmlPath(f'{PATH_R2}/NumCtrlSTR/text()')]
    vendor_timestamp: Annotated[datetime, XmlPath(f'{PATH_R2}/DtHrBC/text()')]
    debtor_institution_ispb: Annotated[Ispb, XmlPath(f'{PATH_R2}/ISPBIFDebtd/text()')]
    sender_type: Annotated[PersonType | None, XmlPath(f'{PATH_R2}/TpPessoaRemet/text()')] = None
    sender_document: Annotated[Cnpj | Cpf | None, XmlPath(f'{PATH_R2}/CNPJ_CPFRemet/text()')] = None
    sender_name: Annotated[Name | None, XmlPath(f'{PATH_R2}/NomRemet/text()')] = None
    creditor_institution_ispb: Annotated[Ispb, XmlPath(f'{PATH_R2}/ISPBIFCredtd/text()')]
    creditor_branch: Annotated[Branch | None, XmlPath(f'{PATH_R2}/AgCredtd/text()')] = None
    creditor_account_type: Annotated[AccountType, XmlPath(f'{PATH_R2}/TpCtCredtd/text()')]
    creditor_account_number: Annotated[AccountNumber | None, XmlPath(f'{PATH_R2}/CtCredtd/text()')] = None
    creditor_payment_account_number: Annotated[AccountNumber | None, XmlPath(f'{PATH_R2}/CtPgtoCredtd/text()')] = None
    creditor_type: Annotated[PersonType, XmlPath(f'{PATH_R2}/TpPessoaCredtd/text()')]
    creditor_document: Annotated[Cnpj | Cpf, XmlPath(f'{PATH_R2}/CNPJ_CPFCliCredtd/text()')]
    creditor_name: Annotated[Name, XmlPath(f'{PATH_R2}/NomCliCredtd/text()')]
    credit_contract_number: Annotated[CreditContractNumber | None, XmlPath(f'{PATH_R2}/NumCtrdCredtd/text()')] = None
    amount: Annotated[Decimal, XmlPath(f'{PATH_R2}/VlrLanc/text()')]
    purpose: Annotated[InstitutionPurpose, XmlPath(f'{PATH_R2}/FinlddIF/text()')]
    transaction_id: Annotated[TransactionId | None, XmlPath(f'{PATH_R2}/CodIdentdTransf/text()')] = None
    description: Annotated[Description | None, XmlPath(f'{PATH_R2}/Hist/text()')] = None
    settlement_date: Annotated[date, XmlPath(f'{PATH_R2}/DtMovto/text()')]


class STR0007E(PartyValidations, BaseMessage):
    XML_NAMESPACE: ClassVar[str | None] = XML_NAMESPACE_ERROR

    document_parties: ClassVar[list[str]] = ['sender', 'creditor']
    account_parties: ClassVar[list[str]] = ['creditor']
    others_enum_value: ClassVar[InstitutionPurpose | None] = InstitutionPurpose.OTHERS
    purpose_attr: ClassVar[str] = 'purpose'
    description_attr: ClassVar[str] = 'description'

    message_code: Annotated[Literal['STR0007E'], XmlPath(f'{PATH_E}/CodMsg/text()')] = 'STR0007E'
    institution_control_number: Annotated[InstitutionControlNumber | None, XmlPath(f'{PATH_E}/NumCtrlIF/text()')] = (
        None
    )
    debtor_institution_ispb: Annotated[Ispb | None, XmlPath(f'{PATH_E}/ISPBIFDebtd/text()')] = None
    sender_type: Annotated[PersonType | None, XmlPath(f'{PATH_E}/TpPessoaRemet/text()')] = None
    sender_document: Annotated[Cnpj | None | Cpf, XmlPath(f'{PATH_E}/CNPJ_CPFRemet/text()')] = None
    sender_name: Annotated[Name | None, XmlPath(f'{PATH_E}/NomRemet/text()')] = None
    creditor_institution_ispb: Annotated[Ispb | None, XmlPath(f'{PATH_E}/ISPBIFCredtd/text()')] = None
    creditor_branch: Annotated[Branch | None, XmlPath(f'{PATH_E}/AgCredtd/text()')] = None
    creditor_account_type: Annotated[AccountType | None, XmlPath(f'{PATH_E}/TpCtCredtd/text()')] = None
    creditor_account_number: Annotated[AccountNumber | None, XmlPath(f'{PATH_E}/CtCredtd/text()')] = None
    creditor_payment_account_number: Annotated[AccountNumber | None, XmlPath(f'{PATH_E}/CtPgtoCredtd/text()')] = None
    creditor_type: Annotated[PersonType | None, XmlPath(f'{PATH_E}/TpPessoaCredtd/text()')] = None
    creditor_document: Annotated[Cnpj | None | Cpf, XmlPath(f'{PATH_E}/CNPJ_CPFCliCredtd/text()')] = None
    creditor_name: Annotated[Name | None, XmlPath(f'{PATH_E}/NomCliCredtd/text()')] = None
    credit_contract_number: Annotated[CreditContractNumber | None, XmlPath(f'{PATH_E}/NumCtrdCredtd/text()')] = None
    amount: Annotated[Decimal | None, XmlPath(f'{PATH_E}/VlrLanc/text()')] = None
    purpose: Annotated[InstitutionPurpose | None, XmlPath(f'{PATH_E}/FinlddIF/text()')] = None
    transaction_id: Annotated[TransactionId | None, XmlPath(f'{PATH_E}/CodIdentdTransf/text()')] = None
    description: Annotated[Description | None, XmlPath(f'{PATH_E}/Hist/text()')] = None
    scheduled_date: Annotated[date | None, XmlPath(f'{PATH_E}/DtAgendt/text()')] = None
    scheduled_time: Annotated[time | None, XmlPath(f'{PATH_E}/HrAgendt/text()')] = None
    priority: Annotated[Priority | None, XmlPath(f'{PATH_E}/NivelPref/text()')] = None
    settlement_date: Annotated[date | None, XmlPath(f'{PATH_E}/DtMovto/text()')] = None

    general_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH_E}/@CodErro')] = None
    institution_control_number_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH_E}/NumCtrlIF/@CodErro')] = None
    debtor_institution_ispb_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH_E}/ISPBIFDebtd/@CodErro')] = None
    sender_type_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH_E}/TpPessoaRemet/@CodErro')] = None
    sender_document_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH_E}/CNPJ_CPFRemet/@CodErro')] = None
    sender_name_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH_E}/NomRemet/@CodErro')] = None
    creditor_institution_ispb_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH_E}/ISPBIFCredtd/@CodErro')] = (
        None
    )
    creditor_branch_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH_E}/AgCredtd/@CodErro')] = None
    creditor_account_type_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH_E}/TpCtCredtd/@CodErro')] = None
    creditor_account_number_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH_E}/CtCredtd/@CodErro')] = None
    creditor_payment_account_number_error_code: Annotated[
        ErrorCode | None, XmlPath(f'{PATH_E}/CtPgtoCredtd/@CodErro')
    ] = None
    creditor_type_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH_E}/TpPessoaCredtd/@CodErro')] = None
    creditor_document_error_code: Annotated[
        ErrorCode | None | Cpf, XmlPath(f'{PATH_E}/CNPJ_CPFCliCredtd/@CodErro')
    ] = None
    creditor_name_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH_E}/NomCliCredtd/@CodErro')] = None
    credit_contract_number_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH_E}/NumCtrdCredtd/@CodErro')] = None
    amount_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH_E}/VlrLanc/@CodErro')] = None
    purpose_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH_E}/FinlddIF/@CodErro')] = None
    transaction_id_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH_E}/CodIdentdTransf/@CodErro')] = None
    description_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH_E}/Hist/@CodErro')] = None
    scheduled_date_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH_E}/DtAgendt/@CodErro')] = None
    scheduled_time_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH_E}/HrAgendt/@CodErro')] = None
    priority_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH_E}/NivelPref/@CodErro')] = None
    settlement_date_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH_E}/DtMovto/@CodErro')] = None
