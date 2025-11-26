from datetime import date, datetime, time
from decimal import Decimal
from typing import Annotated, Literal

from sfn_messages.core.models import BaseMessage, XmlPath
from sfn_messages.core.types import (
    AccountNumber,
    AccountType,
    Branch,
    Cnpj,
    Cpf,
    CreditContractNumber,
    CreditorName,
    Description,
    InstitutionControlNumber,
    Ispb,
    PersonType,
    Priority,
    SenderName,
    StrControlNumber,
    StrSettlementStatus,
    TransactionId,
)

from .types import InstitutionPurpose
from .validation import StrPartyValidation

PATH = 'DOC/SISMSG/STR0007'
PATH_R1 = 'DOC/SISMSG/STR0007R1'
PATH_R2 = 'DOC/SISMSG/STR0007R2'


class STR0007(StrPartyValidation, BaseMessage):
    _document_parties = ('sender', 'creditor')
    _account_parties = ('creditor',)
    _others_enum_value = InstitutionPurpose.OTHERS
    _purpose_attr = 'purpose'
    _description_attr = 'description'

    message_code: Annotated[Literal['STR0007'], XmlPath(f'{PATH}/CodMsg/text()')] = 'STR0007'
    institution_control_number: Annotated[InstitutionControlNumber, XmlPath(f'{PATH}/NumCtrlIF/text()')]
    debtor_institution_ispb: Annotated[Ispb, XmlPath(f'{PATH}/ISPBIFDebtd/text()')]
    sender_type: Annotated[PersonType | None, XmlPath(f'{PATH}/TpPessoaRemet/text()')] = None
    sender_document: Annotated[Cnpj | Cpf | None, XmlPath(f'{PATH}/CNPJ_CPFRemet/text()')] = None
    sender_name: Annotated[SenderName | None, XmlPath(f'{PATH}/NomRemet/text()')] = None
    creditor_institution_ispb: Annotated[Ispb, XmlPath(f'{PATH}/ISPBIFCredtd/text()')]
    creditor_branch: Annotated[Branch | None, XmlPath(f'{PATH}/AgCredtd/text()')] = None
    creditor_account_type: Annotated[AccountType, XmlPath(f'{PATH}/TpCtCredtd/text()')]
    creditor_account_number: Annotated[AccountNumber | None, XmlPath(f'{PATH}/CtCredtd/text()')] = None
    creditor_payment_account_number: Annotated[AccountNumber | None, XmlPath(f'{PATH}/CtPgtoCredtd/text()')] = None
    creditor_type: Annotated[PersonType, XmlPath(f'{PATH}/TpPessoaCredtd/text()')]
    creditor_document: Annotated[Cnpj | Cpf, XmlPath(f'{PATH}/CNPJ_CPFCliCredtd/text()')]
    creditor_name: Annotated[CreditorName, XmlPath(f'{PATH}/NomCliCredtd/text()')]
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
    message_code: Annotated[Literal['STR0007R1'], XmlPath(f'{PATH_R1}/CodMsg/text()')] = 'STR0007R1'
    institution_control_number: Annotated[InstitutionControlNumber, XmlPath(f'{PATH_R1}/NumCtrlIF/text()')]
    debtor_institution_ispb: Annotated[Ispb, XmlPath(f'{PATH_R1}/ISPBIFDebtd/text()')]
    str_control_number: Annotated[StrControlNumber, XmlPath(f'{PATH_R1}/NumCtrlSTR/text()')]
    str_settlement_status: Annotated[StrSettlementStatus, XmlPath(f'{PATH_R1}/SitLancSTR/text()')]
    settlement_timestamp: Annotated[datetime, XmlPath(f'{PATH_R1}/DtHrSit/text()')]
    settlement_date: Annotated[date, XmlPath(f'{PATH_R1}/DtMovto/text()')]


class STR0007R2(StrPartyValidation, BaseMessage):
    _document_parties = ('sender', 'creditor')
    _account_parties = ('creditor',)
    _others_enum_value = InstitutionPurpose.OTHERS
    _purpose_attr = 'purpose'
    _description_attr = 'description'

    message_code: Annotated[Literal['STR0007R2'], XmlPath(f'{PATH_R2}/CodMsg/text()')] = 'STR0007R2'
    str_control_number: Annotated[StrControlNumber, XmlPath(f'{PATH_R2}/NumCtrlSTR/text()')]
    vendor_timestamp: Annotated[datetime, XmlPath(f'{PATH_R2}/DtHrBC/text()')]
    debtor_institution_ispb: Annotated[Ispb, XmlPath(f'{PATH_R2}/ISPBIFDebtd/text()')]
    sender_type: Annotated[PersonType | None, XmlPath(f'{PATH_R2}/TpPessoaRemet/text()')] = None
    sender_document: Annotated[Cnpj | Cpf | None, XmlPath(f'{PATH_R2}/CNPJ_CPFRemet/text()')] = None
    sender_name: Annotated[SenderName | None, XmlPath(f'{PATH_R2}/NomRemet/text()')] = None
    creditor_institution_ispb: Annotated[Ispb, XmlPath(f'{PATH_R2}/ISPBIFCredtd/text()')]
    creditor_branch: Annotated[Branch | None, XmlPath(f'{PATH_R2}/AgCredtd/text()')] = None
    creditor_account_type: Annotated[AccountType, XmlPath(f'{PATH_R2}/TpCtCredtd/text()')]
    creditor_account_number: Annotated[AccountNumber | None, XmlPath(f'{PATH_R2}/CtCredtd/text()')] = None
    creditor_payment_account_number: Annotated[AccountNumber | None, XmlPath(f'{PATH_R2}/CtPgtoCredtd/text()')] = None
    creditor_type: Annotated[PersonType, XmlPath(f'{PATH_R2}/TpPessoaCredtd/text()')]
    creditor_document: Annotated[Cnpj | Cpf, XmlPath(f'{PATH_R2}/CNPJ_CPFCliCredtd/text()')]
    creditor_name: Annotated[CreditorName, XmlPath(f'{PATH_R2}/NomCliCredtd/text()')]
    credit_contract_number: Annotated[CreditContractNumber | None, XmlPath(f'{PATH_R2}/NumCtrdCredtd/text()')] = None
    amount: Annotated[Decimal, XmlPath(f'{PATH_R2}/VlrLanc/text()')]
    purpose: Annotated[InstitutionPurpose, XmlPath(f'{PATH_R2}/FinlddIF/text()')]
    transaction_id: Annotated[TransactionId | None, XmlPath(f'{PATH_R2}/CodIdentdTransf/text()')] = None
    description: Annotated[Description | None, XmlPath(f'{PATH_R2}/Hist/text()')] = None
    settlement_date: Annotated[date, XmlPath(f'{PATH_R2}/DtMovto/text()')]
