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
    DepositIdentifier,
    ErrorCode,
    InstitutionControlNumber,
    Ispb,
    Name,
    PersonType,
    Priority,
    StrControlNumber,
    StrSettlementStatus,
)

from .validations import PartyValidations

PATH = 'DOC/SISMSG/STR0025'
PATH_R1 = 'DOC/SISMSG/STR0025R1'
PATH_R2 = 'DOC/SISMSG/STR0025R2'
PATH_E = 'DOC/SISMSG/STR0025'
XML_NAMESPACE = 'http://www.bcb.gov.br/SPB/STR0025.xsd'
XML_NAMESPACE_ERROR = 'http://www.bcb.gov.br/SPB/STR0025E.xsd'


class STR0025(PartyValidations, BaseMessage):
    XML_NAMESPACE: ClassVar[str | None] = XML_NAMESPACE

    document_parties: ClassVar[list[str]] = ['creditor']
    account_parties: ClassVar[list[str]] = ['debtor']

    message_code: Annotated[Literal['STR0025'], XmlPath(f'{PATH}/CodMsg/text()')] = 'STR0025'
    institution_control_number: Annotated[InstitutionControlNumber, XmlPath(f'{PATH}/NumCtrlIF/text()')]
    debtor_institution_ispb: Annotated[Ispb, XmlPath(f'{PATH}/ISPBIFDebtd/text()')]
    debtor_branch: Annotated[Branch | None, XmlPath(f'{PATH}/AgDebtd/text()')] = None
    debtor_account_type: Annotated[AccountType | None, XmlPath(f'{PATH}/TpCtDebtd/text()')] = None
    debtor_account_number: Annotated[AccountNumber | None, XmlPath(f'{PATH}/CtDebtd/text()')] = None
    debtor_payment_account_number: Annotated[AccountNumber | None, XmlPath(f'{PATH}/CtPgtoDebtd/text()')] = None
    debtor_name: Annotated[Name, XmlPath(f'{PATH}/NomCliDebtd/text()')]
    debtor_type: Annotated[PersonType, XmlPath(f'{PATH}/TpPessoaDebtd/text()')]
    debtor_document: Annotated[Cnpj | Cpf, XmlPath(f'{PATH}/CNPJ_CPFCliDebtd/text()')]
    creditor_institution_ispb: Annotated[Ispb, XmlPath(f'{PATH}/ISPBIFCredtd/text()')]
    amount: Annotated[Decimal, XmlPath(f'{PATH}/VlrLanc/text()')]
    priority: Annotated[Priority | None, XmlPath(f'{PATH}/NivelPref/text()')] = None
    deposit_identifier: Annotated[DepositIdentifier, XmlPath(f'{PATH}/IdentcDep/text()')]
    scheduled_date: Annotated[date | None, XmlPath(f'{PATH}/DtAgendt/text()')] = None
    scheduled_time: Annotated[time | None, XmlPath(f'{PATH}/HrAgendt/text()')] = None
    settlement_date: Annotated[date, XmlPath(f'{PATH}/DtMovto/text()')]


class STR0025R1(BaseMessage):
    XML_NAMESPACE: ClassVar[str | None] = XML_NAMESPACE

    message_code: Annotated[Literal['STR0025R1'], XmlPath(f'{PATH_R1}/CodMsg/text()')] = 'STR0025R1'
    institution_control_number: Annotated[InstitutionControlNumber, XmlPath(f'{PATH_R1}/NumCtrlIF/text()')]
    debtor_institution_ispb: Annotated[Ispb, XmlPath(f'{PATH_R1}/ISPBIFDebtd/text()')]
    str_control_number: Annotated[StrControlNumber, XmlPath(f'{PATH_R1}/NumCtrlSTR/text()')]
    str_settlement_status: Annotated[StrSettlementStatus, XmlPath(f'{PATH_R1}/SitLancSTR/text()')]
    settlement_timestamp: Annotated[datetime, XmlPath(f'{PATH_R1}/DtHrSit/text()')]
    settlement_date: Annotated[date, XmlPath(f'{PATH_R1}/DtMovto/text()')]


class STR0025R2(PartyValidations, BaseMessage):
    XML_NAMESPACE: ClassVar[str | None] = XML_NAMESPACE

    document_parties: ClassVar[list[str]] = ['creditor']
    account_parties: ClassVar[list[str]] = ['debtor']

    message_code: Annotated[Literal['STR0025R2'], XmlPath(f'{PATH_R2}/CodMsg/text()')] = 'STR0025R2'
    str_control_number: Annotated[StrControlNumber, XmlPath(f'{PATH_R2}/NumCtrlSTR/text()')]
    vendor_timestamp: Annotated[datetime, XmlPath(f'{PATH_R2}/DtHrBC/text()')]
    debtor_institution_ispb: Annotated[Ispb, XmlPath(f'{PATH_R2}/ISPBIFDebtd/text()')]
    debtor_branch: Annotated[Branch | None, XmlPath(f'{PATH_R2}/AgDebtd/text()')] = None
    debtor_account_type: Annotated[AccountType | None, XmlPath(f'{PATH_R2}/TpCtDebtd/text()')] = None
    debtor_account_number: Annotated[AccountNumber | None, XmlPath(f'{PATH_R2}/CtDebtd/text()')] = None
    debtor_payment_account_number: Annotated[AccountNumber | None, XmlPath(f'{PATH_R2}/CtPgtoDebtd/text()')] = None
    creditor_name: Annotated[Name, XmlPath(f'{PATH_R2}/NomCliCredtd/text()')]
    creditor_type: Annotated[PersonType, XmlPath(f'{PATH_R2}/TpPessoaCredtd/text()')]
    creditor_document: Annotated[Cnpj | Cpf, XmlPath(f'{PATH_R2}/CNPJ_CPFCliCredtd/text()')]
    creditor_institution_ispb: Annotated[Ispb, XmlPath(f'{PATH_R2}/ISPBIFCredtd/text()')]
    amount: Annotated[Decimal, XmlPath(f'{PATH_R2}/VlrLanc/text()')]
    deposit_identifier: Annotated[DepositIdentifier, XmlPath(f'{PATH_R2}/IdentcDep/text()')]
    settlement_date: Annotated[date, XmlPath(f'{PATH_R2}/DtMovto/text()')]


class STR0025E(PartyValidations, BaseMessage):
    XML_NAMESPACE: ClassVar[str | None] = XML_NAMESPACE_ERROR

    document_parties: ClassVar[list[str]] = ['creditor']
    account_parties: ClassVar[list[str]] = ['debtor']

    message_code: Annotated[Literal['STR0025E'], XmlPath(f'{PATH_E}/CodMsg/text()')] = 'STR0025E'
    institution_control_number: Annotated[InstitutionControlNumber | None, XmlPath(f'{PATH_E}/NumCtrlIF/text()')] = (
        None
    )
    debtor_institution_ispb: Annotated[Ispb | None, XmlPath(f'{PATH_E}/ISPBIFDebtd/text()')] = None
    debtor_branch: Annotated[Branch | None, XmlPath(f'{PATH_E}/AgDebtd/text()')] = None
    debtor_account_type: Annotated[AccountType | None, XmlPath(f'{PATH_E}/TpCtDebtd/text()')] = None
    debtor_account_number: Annotated[AccountNumber | None, XmlPath(f'{PATH_E}/CtDebtd/text()')] = None
    debtor_payment_account_number: Annotated[AccountNumber | None, XmlPath(f'{PATH_E}/CtPgtoDebtd/text()')] = None
    creditor_name: Annotated[Name | None, XmlPath(f'{PATH_E}/NomCliCredtd/text()')] = None
    creditor_type: Annotated[PersonType | None, XmlPath(f'{PATH_E}/TpPessoaCredtd/text()')] = None
    creditor_document: Annotated[Cnpj | None | Cpf, XmlPath(f'{PATH_E}/CNPJ_CPFCliCredtd/text()')] = None
    creditor_institution_ispb: Annotated[Ispb | None, XmlPath(f'{PATH_E}/ISPBIFCredtd/text()')] = None
    amount: Annotated[Decimal | None, XmlPath(f'{PATH_E}/VlrLanc/text()')] = None
    priority: Annotated[Priority | None, XmlPath(f'{PATH_E}/NivelPref/text()')] = None
    deposit_identifier: Annotated[DepositIdentifier | None, XmlPath(f'{PATH_E}/IdentcDep/text()')] = None
    scheduled_date: Annotated[date | None, XmlPath(f'{PATH_E}/DtAgendt/text()')] = None
    scheduled_time: Annotated[time | None, XmlPath(f'{PATH_E}/HrAgendt/text()')] = None
    settlement_date: Annotated[date | None, XmlPath(f'{PATH_E}/DtMovto/text()')] = None

    general_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH_E}/@CodErro')] = None
    institution_control_number_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH_E}/NumCtrlIF/@CodErro')] = None
    debtor_institution_ispb_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH_E}/ISPBIFDebtd/@CodErro')] = None
    debtor_branch_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH_E}/AgDebtd/@CodErro')] = None
    debtor_account_type_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH_E}/TpCtDebtd/@CodErro')] = None
    debtor_account_number_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH_E}/CtDebtd/@CodErro')] = None
    debtor_payment_account_number_error_code: Annotated[
        ErrorCode | None, XmlPath(f'{PATH_E}/CtPgtoDebtd/@CodErro')
    ] = None
    creditor_name_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH_E}/NomCliCredtd/@CodErro')] = None
    creditor_type_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH_E}/TpPessoaCredtd/@CodErro')] = None
    creditor_document_error_code: Annotated[
        ErrorCode | None | Cpf, XmlPath(f'{PATH_E}/CNPJ_CPFCliCredtd/@CodErro')
    ] = None
    creditor_institution_ispb_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH_E}/ISPBIFCredtd/@CodErro')] = (
        None
    )
    amount_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH_E}/VlrLanc/@CodErro')] = None
    priority_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH_E}/NivelPref/@CodErro')] = None
    deposit_identifier_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH_E}/IdentcDep/@CodErro')] = None
    scheduled_date_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH_E}/DtAgendt/@CodErro')] = None
    scheduled_time_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH_E}/HrAgendt/@CodErro')] = None
    settlement_date_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH_E}/DtMovto/@CodErro')] = None
