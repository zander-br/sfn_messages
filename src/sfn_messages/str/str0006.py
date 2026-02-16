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
    CustomerPurpose,
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

from .validations import PartyValidations

PATH = 'DOC/SISMSG/STR0006'
PATH_R1 = 'DOC/SISMSG/STR0006R1'
PATH_R2 = 'DOC/SISMSG/STR0006R2'
PATH_E = 'DOC/SISMSG/STR0006'
XML_NAMESPACE = 'http://www.bcb.gov.br/SPB/STR0006.xsd'
XML_NAMESPACE_ERROR = 'http://www.bcb.gov.br/SPB/STR0006E.xsd'


class STR0006(PartyValidations, BaseMessage):
    XML_NAMESPACE: ClassVar[str | None] = XML_NAMESPACE

    document_parties: ClassVar[list[str]] = ['sender', 'recipient']
    account_parties: ClassVar[list[str]] = ['debtor']
    others_enum_value: ClassVar[CustomerPurpose | None] = CustomerPurpose.OTHERS
    purpose_attr: ClassVar[str] = 'purpose'
    description_attr: ClassVar[str] = 'description'

    message_code: Annotated[Literal['STR0006'], XmlPath(f'{PATH}/CodMsg/text()')] = 'STR0006'
    institution_control_number: Annotated[InstitutionControlNumber, XmlPath(f'{PATH}/NumCtrlIF/text()')]
    debtor_institution_ispb: Annotated[Ispb, XmlPath(f'{PATH}/ISPBIFDebtd/text()')]
    debtor_branch: Annotated[Branch | None, XmlPath(f'{PATH}/AgDebtd/text()')] = None
    debtor_account_type: Annotated[AccountType, XmlPath(f'{PATH}/Grupo_STR0006_CtDebtd/TpCtDebtd/text()')]
    debtor_account_number: Annotated[AccountNumber | None, XmlPath(f'{PATH}/Grupo_STR0006_CtDebtd/CtDebtd/text()')] = (
        None
    )
    debtor_payment_account_number: Annotated[
        AccountNumber | None, XmlPath(f'{PATH}/Grupo_STR0006_CtDebtd/CtPgtoDebtd/text()')
    ] = None
    sender_type: Annotated[PersonType | None, XmlPath(f'{PATH}/TpPessoaDebtd_Remet/text()')] = None
    sender_document: Annotated[Cnpj | Cpf | None, XmlPath(f'{PATH}/CNPJ_CPFCliDebtd_Remet/text()')] = None
    sender_name: Annotated[Name | None, XmlPath(f'{PATH}/NomCliDebtd_Remet/text()')] = None
    creditor_institution_ispb: Annotated[Ispb, XmlPath(f'{PATH}/ISPBIFCredtd/text()')]
    creditor_branch: Annotated[Branch | None, XmlPath(f'{PATH}/AgCredtd/text()')] = None
    creditor_account_number: Annotated[AccountNumber | None, XmlPath(f'{PATH}/CtCredtd/text()')] = None
    recipient_type: Annotated[PersonType | None, XmlPath(f'{PATH}/TpPessoaDestinatario/text()')] = None
    recipient_document: Annotated[Cnpj | Cpf | None, XmlPath(f'{PATH}/CNPJ_CPFDestinatario/text()')] = None
    recipient_name: Annotated[Name | None, XmlPath(f'{PATH}/NomDestinatario/text()')] = None
    credit_contract_number: Annotated[CreditContractNumber | None, XmlPath(f'{PATH}/NumContrtoOpCred/text()')] = None
    amount: Annotated[Decimal, XmlPath(f'{PATH}/VlrLanc/text()')]
    purpose: Annotated[CustomerPurpose, XmlPath(f'{PATH}/FinlddCli/text()')]
    transaction_id: Annotated[TransactionId | None, XmlPath(f'{PATH}/CodIdentdTransf/text()')] = None
    description: Annotated[Description | None, XmlPath(f'{PATH}/Hist/text()')] = None
    scheduled_date: Annotated[date | None, XmlPath(f'{PATH}/DtAgendt/text()')] = None
    scheduled_time: Annotated[time | None, XmlPath(f'{PATH}/HrAgendt/text()')] = None
    priority: Annotated[Priority | None, XmlPath(f'{PATH}/NivelPref/text()')] = None
    settlement_date: Annotated[date, XmlPath(f'{PATH}/DtMovto/text()')]


class STR0006R1(BaseMessage):
    XML_NAMESPACE: ClassVar[str | None] = XML_NAMESPACE

    message_code: Annotated[Literal['STR0006R1'], XmlPath(f'{PATH_R1}/CodMsg/text()')] = 'STR0006R1'
    institution_control_number: Annotated[InstitutionControlNumber, XmlPath(f'{PATH_R1}/NumCtrlIF/text()')]
    debtor_institution_ispb: Annotated[Ispb, XmlPath(f'{PATH_R1}/ISPBIFDebtd/text()')]
    str_control_number: Annotated[StrControlNumber, XmlPath(f'{PATH_R1}/NumCtrlSTR/text()')]
    str_settlement_status: Annotated[StrSettlementStatus, XmlPath(f'{PATH_R1}/SitLancSTR/text()')]
    settlement_timestamp: Annotated[datetime, XmlPath(f'{PATH_R1}/DtHrSit/text()')]
    settlement_date: Annotated[date, XmlPath(f'{PATH_R1}/DtMovto/text()')]


class STR0006R2(PartyValidations, BaseMessage):
    XML_NAMESPACE: ClassVar[str | None] = XML_NAMESPACE

    document_parties: ClassVar[list[str]] = ['sender', 'recipient']
    account_parties: ClassVar[list[str]] = ['debtor']
    others_enum_value: ClassVar[CustomerPurpose | None] = CustomerPurpose.OTHERS
    purpose_attr: ClassVar[str] = 'purpose'
    description_attr: ClassVar[str] = 'description'

    message_code: Annotated[Literal['STR0006R2'], XmlPath(f'{PATH_R2}/CodMsg/text()')] = 'STR0006R2'
    str_control_number: Annotated[StrControlNumber, XmlPath(f'{PATH_R2}/NumCtrlSTR/text()')]
    vendor_timestamp: Annotated[datetime, XmlPath(f'{PATH_R2}/DtHrBC/text()')]
    debtor_institution_ispb: Annotated[Ispb, XmlPath(f'{PATH_R2}/ISPBIFDebtd/text()')]
    debtor_branch: Annotated[Branch | None, XmlPath(f'{PATH_R2}/AgDebtd/text()')] = None
    debtor_account_type: Annotated[AccountType, XmlPath(f'{PATH_R2}/Grupo_STR0006R2_CtDebtd/TpCtDebtd/text()')]
    debtor_account_number: Annotated[
        AccountNumber | None, XmlPath(f'{PATH_R2}/Grupo_STR0006R2_CtDebtd/CtDebtd/text()')
    ] = None
    debtor_payment_account_number: Annotated[
        AccountNumber | None, XmlPath(f'{PATH_R2}/Grupo_STR0006R2_CtDebtd/CtPgtoDebtd/text()')
    ] = None
    sender_type: Annotated[PersonType | None, XmlPath(f'{PATH_R2}/TpPessoaDebtd_Remet/text()')] = None
    sender_document: Annotated[Cnpj | Cpf | None, XmlPath(f'{PATH_R2}/CNPJ_CPFCliDebtd_Remet/text()')] = None
    sender_name: Annotated[Name | None, XmlPath(f'{PATH_R2}/NomCliDebtd_Remet/text()')] = None
    creditor_institution_ispb: Annotated[Ispb, XmlPath(f'{PATH_R2}/ISPBIFCredtd/text()')]
    creditor_branch: Annotated[Branch | None, XmlPath(f'{PATH_R2}/AgCredtd/text()')] = None
    creditor_account_number: Annotated[AccountNumber | None, XmlPath(f'{PATH_R2}/CtCredtd/text()')] = None
    recipient_type: Annotated[PersonType | None, XmlPath(f'{PATH_R2}/TpPessoaDestinatario/text()')] = None
    recipient_document: Annotated[Cnpj | Cpf | None, XmlPath(f'{PATH_R2}/CNPJ_CPFDestinatario/text()')] = None
    recipient_name: Annotated[Name | None, XmlPath(f'{PATH_R2}/NomDestinatario/text()')] = None
    credit_contract_number: Annotated[CreditContractNumber | None, XmlPath(f'{PATH_R2}/NumContrtoOpCred/text()')] = (
        None
    )
    amount: Annotated[Decimal, XmlPath(f'{PATH_R2}/VlrLanc/text()')]
    purpose: Annotated[CustomerPurpose, XmlPath(f'{PATH_R2}/FinlddCli/text()')]
    transaction_id: Annotated[TransactionId | None, XmlPath(f'{PATH_R2}/CodIdentdTransf/text()')] = None
    description: Annotated[Description | None, XmlPath(f'{PATH_R2}/Hist/text()')] = None
    settlement_date: Annotated[date, XmlPath(f'{PATH_R2}/DtMovto/text()')]


class STR0006E(PartyValidations, BaseMessage):
    XML_NAMESPACE: ClassVar[str | None] = XML_NAMESPACE_ERROR

    document_parties: ClassVar[list[str]] = ['sender', 'recipient']
    account_parties: ClassVar[list[str]] = ['debtor']
    others_enum_value: ClassVar[CustomerPurpose | None] = CustomerPurpose.OTHERS
    purpose_attr: ClassVar[str] = 'purpose'
    description_attr: ClassVar[str] = 'description'

    message_code: Annotated[Literal['STR0006E'], XmlPath(f'{PATH_E}/CodMsg/text()')] = 'STR0006E'
    institution_control_number: Annotated[InstitutionControlNumber | None, XmlPath(f'{PATH_E}/NumCtrlIF/text()')] = (
        None
    )
    debtor_institution_ispb: Annotated[Ispb | None, XmlPath(f'{PATH_E}/ISPBIFDebtd/text()')] = None
    debtor_branch: Annotated[Branch | None, XmlPath(f'{PATH_E}/AgDebtd/text()')] = None
    debtor_account_type: Annotated[AccountType | None, XmlPath(f'{PATH_E}/Grupo_STR0006_CtDebtd/TpCtDebtd/text()')] = (
        None
    )
    debtor_account_number: Annotated[
        AccountNumber | None, XmlPath(f'{PATH_E}/Grupo_STR0006_CtDebtd/CtDebtd/text()')
    ] = None
    debtor_payment_account_number: Annotated[
        AccountNumber | None, XmlPath(f'{PATH_E}/Grupo_STR0006_CtDebtd/CtPgtoDebtd/text()')
    ] = None
    sender_type: Annotated[PersonType | None, XmlPath(f'{PATH_E}/TpPessoaDebtd_Remet/text()')] = None
    sender_document: Annotated[Cnpj | Cpf | None, XmlPath(f'{PATH_E}/CNPJ_CPFCliDebtd_Remet/text()')] = None
    sender_name: Annotated[Name | None, XmlPath(f'{PATH_E}/NomCliDebtd_Remet/text()')] = None
    creditor_institution_ispb: Annotated[Ispb | None, XmlPath(f'{PATH_E}/ISPBIFCredtd/text()')] = None
    creditor_branch: Annotated[Branch | None, XmlPath(f'{PATH_E}/AgCredtd/text()')] = None
    creditor_account_number: Annotated[AccountNumber | None, XmlPath(f'{PATH_E}/CtCredtd/text()')] = None
    recipient_type: Annotated[PersonType | None, XmlPath(f'{PATH_E}/TpPessoaDestinatario/text()')] = None
    recipient_document: Annotated[Cnpj | Cpf | None, XmlPath(f'{PATH_E}/CNPJ_CPFDestinatario/text()')] = None
    recipient_name: Annotated[Name | None, XmlPath(f'{PATH_E}/NomDestinatario/text()')] = None
    credit_contract_number: Annotated[CreditContractNumber | None, XmlPath(f'{PATH_E}/NumContrtoOpCred/text()')] = None
    amount: Annotated[Decimal | None, XmlPath(f'{PATH_E}/VlrLanc/text()')] = None
    purpose: Annotated[CustomerPurpose | None, XmlPath(f'{PATH_E}/FinlddCli/text()')] = None
    transaction_id: Annotated[TransactionId | None, XmlPath(f'{PATH_E}/CodIdentdTransf/text()')] = None
    description: Annotated[Description | None, XmlPath(f'{PATH_E}/Hist/text()')] = None
    scheduled_date: Annotated[date | None, XmlPath(f'{PATH_E}/DtAgendt/text()')] = None
    scheduled_time: Annotated[time | None, XmlPath(f'{PATH_E}/HrAgendt/text()')] = None
    priority: Annotated[Priority | None, XmlPath(f'{PATH_E}/NivelPref/text()')] = None
    settlement_date: Annotated[date | None, XmlPath(f'{PATH_E}/DtMovto/text()')] = None

    general_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH_E}/@CodErro')] = None
    institution_control_number_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH_E}/NumCtrlIF/@CodErro')] = None
    debtor_institution_ispb_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH_E}/ISPBIFDebtd/@CodErro')] = None
    debtor_branch_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH_E}/AgDebtd/@CodErro')] = None
    debtor_account_type_error_code: Annotated[
        ErrorCode | None, XmlPath(f'{PATH_E}/Grupo_STR0006_CtDebtd/TpCtDebtd/@CodErro')
    ] = None
    debtor_account_number_error_code: Annotated[
        ErrorCode | None, XmlPath(f'{PATH_E}/Grupo_STR0006_CtDebtd/CtDebtd/@CodErro')
    ] = None
    debtor_payment_account_number_error_code: Annotated[
        ErrorCode | None, XmlPath(f'{PATH_E}/Grupo_STR0006_CtDebtd/CtPgtoDebtd/@CodErro')
    ] = None
    sender_type_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH_E}/TpPessoaDebtd_Remet/@CodErro')] = None
    sender_document_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH_E}/CNPJ_CPFCliDebtd_Remet/@CodErro')] = (
        None
    )
    sender_name_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH_E}/NomCliDebtd_Remet/@CodErro')] = None
    creditor_institution_ispb_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH_E}/ISPBIFCredtd/@CodErro')] = (
        None
    )
    creditor_branch_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH_E}/AgCredtd/@CodErro')] = None
    creditor_account_number_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH_E}/CtCredtd/@CodErro')] = None
    recipient_type_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH_E}/TpPessoaDestinatario/@CodErro')] = None
    recipient_document_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH_E}/CNPJ_CPFDestinatario/@CodErro')] = (
        None
    )
    recipient_name_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH_E}/NomDestinatario/@CodErro')] = None
    credit_contract_number_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH_E}/NumContrtoOpCred/@CodErro')] = (
        None
    )
    amount_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH_E}/VlrLanc/@CodErro')] = None
    purpose_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH_E}/FinlddCli/@CodErro')] = None
    transaction_id_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH_E}/CodIdentdTransf/@CodErro')] = None
    description_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH_E}/Hist/@CodErro')] = None
    scheduled_date_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH_E}/DtAgendt/@CodErro')] = None
    scheduled_time_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH_E}/HrAgendt/@CodErro')] = None
    priority_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH_E}/NivelPref/@CodErro')] = None
    settlement_date_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH_E}/DtMovto/@CodErro')] = None
