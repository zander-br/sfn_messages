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
)

from .validations import PartyValidations

PATH = 'DOC/SISMSG/STR0005'
PATH_R1 = 'DOC/SISMSG/STR0005R1'
PATH_R2 = 'DOC/SISMSG/STR0005R2'
PATH_E = 'DOC/SISMSG/STR0005'
XML_NAMESPACE = 'http://www.bcb.gov.br/SPB/STR0005.xsd'
XML_NAMESPACE_ERROR = 'http://www.bcb.gov.br/SPB/STR0005E.xsd'


class STR0005(PartyValidations, BaseMessage):
    XML_NAMESPACE: ClassVar[str | None] = XML_NAMESPACE

    document_parties: ClassVar[list[str]] = ['sender', 'recipient']
    account_parties: ClassVar[list[str]] = ['debtor', 'creditor']
    others_enum_value: ClassVar[CustomerPurpose | None] = CustomerPurpose.OTHERS
    purpose_attr: ClassVar[str] = 'purpose'
    description_attr: ClassVar[str] = 'description'

    message_code: Annotated[Literal['STR0005'], XmlPath(f'{PATH}/CodMsg/text()')] = 'STR0005'
    institution_control_number: Annotated[InstitutionControlNumber, XmlPath(f'{PATH}/NumCtrlIF/text()')]
    debtor_institution_ispb: Annotated[Ispb, XmlPath(f'{PATH}/ISPBIFDebtd/text()')]
    debtor_branch: Annotated[Branch, XmlPath(f'{PATH}/AgDebtd/text()')]
    sender_type: Annotated[PersonType, XmlPath(f'{PATH}/TpPessoaRemet/text()')]
    sender_document: Annotated[Cnpj | Cpf, XmlPath(f'{PATH}/CNPJ_CPFRemet/text()')]
    sender_name: Annotated[Name, XmlPath(f'{PATH}/NomRemet/text()')]
    creditor_institution_ispb: Annotated[Ispb, XmlPath(f'{PATH}/ISPBIFCredtd/text()')]
    creditor_branch: Annotated[Branch | None, XmlPath(f'{PATH}/AgCredtd/text()')] = None
    creditor_account_number: Annotated[AccountNumber | None, XmlPath(f'{PATH}/CtCredtd/text()')] = None
    creditor_payment_account_number: Annotated[AccountNumber | None, XmlPath(f'{PATH}/CtPgtoCredtd/text()')] = None
    creditor_account_type: Annotated[AccountType | None, XmlPath(f'{PATH}/TpCtCredtd/text()')] = None
    recipient_type: Annotated[PersonType, XmlPath(f'{PATH}/TpPessoaDestinatario/text()')]
    recipient_document: Annotated[Cnpj | Cpf, XmlPath(f'{PATH}/CNPJ_CPFDestinatario/text()')]
    recipient_name: Annotated[Name, XmlPath(f'{PATH}/NomDestinatario/text()')]
    amount: Annotated[Decimal, XmlPath(f'{PATH}/VlrLanc/text()')]
    purpose: Annotated[CustomerPurpose, XmlPath(f'{PATH}/FinlddCli/text()')]
    description: Annotated[Description | None, XmlPath(f'{PATH}/Hist/text()')] = None
    scheduled_date: Annotated[date | None, XmlPath(f'{PATH}/DtAgendt/text()')] = None
    scheduled_time: Annotated[time | None, XmlPath(f'{PATH}/HrAgendt/text()')] = None
    priority: Annotated[Priority | None, XmlPath(f'{PATH}/NivelPref/text()')] = None
    settlement_date: Annotated[date, XmlPath(f'{PATH}/DtMovto/text()')]


class STR0005R1(BaseMessage):
    XML_NAMESPACE: ClassVar[str | None] = XML_NAMESPACE

    message_code: Annotated[Literal['STR0005R1'], XmlPath(f'{PATH_R1}/CodMsg/text()')] = 'STR0005R1'
    institution_control_number: Annotated[InstitutionControlNumber, XmlPath(f'{PATH_R1}/NumCtrlIF/text()')]
    debtor_institution_ispb: Annotated[Ispb, XmlPath(f'{PATH_R1}/ISPBIFDebtd/text()')]
    str_control_number: Annotated[StrControlNumber, XmlPath(f'{PATH_R1}/NumCtrlSTR/text()')]
    str_settlement_status: Annotated[StrSettlementStatus, XmlPath(f'{PATH_R1}/SitLancSTR/text()')]
    settlement_timestamp: Annotated[datetime, XmlPath(f'{PATH_R1}/DtHrSit/text()')]
    settlement_date: Annotated[date, XmlPath(f'{PATH_R1}/DtMovto/text()')]


class STR0005R2(PartyValidations, BaseMessage):
    XML_NAMESPACE: ClassVar[str | None] = XML_NAMESPACE

    document_parties: ClassVar[list[str]] = ['debtor', 'creditor']
    account_parties: ClassVar[list[str]] = ['debtor', 'creditor']
    others_enum_value: ClassVar[CustomerPurpose | None] = CustomerPurpose.OTHERS
    purpose_attr: ClassVar[str] = 'purpose'
    description_attr: ClassVar[str] = 'description'

    message_code: Annotated[Literal['STR0005R2'], XmlPath(f'{PATH_R2}/CodMsg/text()')] = 'STR0005R2'
    str_control_number: Annotated[StrControlNumber, XmlPath(f'{PATH_R2}/NumCtrlSTR/text()')]
    vendor_timestamp: Annotated[datetime, XmlPath(f'{PATH_R2}/DtHrBC/text()')]
    debtor_institution_ispb: Annotated[Ispb, XmlPath(f'{PATH_R2}/ISPBIFDebtd/text()')]
    debtor_branch: Annotated[Branch, XmlPath(f'{PATH_R2}/AgDebtd/text()')]
    sender_type: Annotated[PersonType, XmlPath(f'{PATH_R2}/TpPessoaRemet/text()')]
    sender_document: Annotated[Cnpj | Cpf, XmlPath(f'{PATH_R2}/CNPJ_CPFRemet/text()')]
    sender_name: Annotated[Name, XmlPath(f'{PATH_R2}/NomRemet/text()')]
    creditor_institution_ispb: Annotated[Ispb, XmlPath(f'{PATH_R2}/ISPBIFCredtd/text()')]
    creditor_branch: Annotated[Branch | None, XmlPath(f'{PATH_R2}/AgCredtd/text()')] = None
    creditor_account_number: Annotated[AccountNumber | None, XmlPath(f'{PATH_R2}/CtCredtd/text()')] = None
    creditor_payment_account_number: Annotated[AccountNumber | None, XmlPath(f'{PATH_R2}/CtPgtoCredtd/text()')] = None
    creditor_account_type: Annotated[AccountType | None, XmlPath(f'{PATH_R2}/TpCtCredtd/text()')] = None
    recipient_type: Annotated[PersonType, XmlPath(f'{PATH_R2}/TpPessoaDestinatario/text()')]
    recipient_document: Annotated[Cnpj | Cpf, XmlPath(f'{PATH_R2}/CNPJ_CPFDestinatario/text()')]
    recipient_name: Annotated[Name, XmlPath(f'{PATH_R2}/NomDestinatario/text()')]
    amount: Annotated[Decimal, XmlPath(f'{PATH_R2}/VlrLanc/text()')]
    purpose: Annotated[CustomerPurpose, XmlPath(f'{PATH_R2}/FinlddCli/text()')]
    description: Annotated[Description | None, XmlPath(f'{PATH_R2}/Hist/text()')] = None
    settlement_date: Annotated[date, XmlPath(f'{PATH_R2}/DtMovto/text()')]


class STR0005E(PartyValidations, BaseMessage):
    XML_NAMESPACE: ClassVar[str | None] = XML_NAMESPACE_ERROR

    document_parties: ClassVar[list[str]] = ['sender', 'recipient']
    account_parties: ClassVar[list[str]] = ['debtor', 'creditor']
    others_enum_value: ClassVar[CustomerPurpose | None] = CustomerPurpose.OTHERS
    purpose_attr: ClassVar[str] = 'purpose'
    description_attr: ClassVar[str] = 'description'

    message_code: Annotated[Literal['STR0005E'], XmlPath(f'{PATH_E}/CodMsg/text()')] = 'STR0005E'
    institution_control_number: Annotated[InstitutionControlNumber | None, XmlPath(f'{PATH_E}/NumCtrlIF/text()')] = (
        None
    )
    debtor_institution_ispb: Annotated[Ispb | None, XmlPath(f'{PATH_E}/ISPBIFDebtd/text()')] = None
    debtor_branch: Annotated[Branch | None, XmlPath(f'{PATH_E}/AgDebtd/text()')] = None
    sender_type: Annotated[PersonType | None, XmlPath(f'{PATH_E}/TpPessoaRemet/text()')] = None
    sender_document: Annotated[Cnpj | None | Cpf, XmlPath(f'{PATH_E}/CNPJ_CPFRemet/text()')] = None
    sender_name: Annotated[Name | None, XmlPath(f'{PATH_E}/NomRemet/text()')] = None
    creditor_institution_ispb: Annotated[Ispb | None, XmlPath(f'{PATH_E}/ISPBIFCredtd/text()')] = None
    creditor_branch: Annotated[Branch | None, XmlPath(f'{PATH_E}/AgCredtd/text()')] = None
    creditor_account_number: Annotated[AccountNumber | None, XmlPath(f'{PATH_E}/CtCredtd/text()')] = None
    creditor_payment_account_number: Annotated[AccountNumber | None, XmlPath(f'{PATH_E}/CtPgtoCredtd/text()')] = None
    creditor_account_type: Annotated[AccountType | None, XmlPath(f'{PATH_E}/TpCtCredtd/text()')] = None
    recipient_type: Annotated[PersonType | None, XmlPath(f'{PATH_E}/TpPessoaDestinatario/text()')] = None
    recipient_document: Annotated[Cnpj | None | Cpf, XmlPath(f'{PATH_E}/CNPJ_CPFDestinatario/text()')] = None
    recipient_name: Annotated[Name | None, XmlPath(f'{PATH_E}/NomDestinatario/text()')] = None
    amount: Annotated[Decimal | None, XmlPath(f'{PATH_E}/VlrLanc/text()')] = None
    purpose: Annotated[CustomerPurpose | None, XmlPath(f'{PATH_E}/FinlddCli/text()')] = None
    description: Annotated[Description | None, XmlPath(f'{PATH_E}/Hist/text()')] = None
    scheduled_date: Annotated[date | None, XmlPath(f'{PATH_E}/DtAgendt/text()')] = None
    scheduled_time: Annotated[time | None, XmlPath(f'{PATH_E}/HrAgendt/text()')] = None
    priority: Annotated[Priority | None, XmlPath(f'{PATH_E}/NivelPref/text()')] = None
    settlement_date: Annotated[date | None, XmlPath(f'{PATH_E}/DtMovto/text()')] = None

    general_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH_E}/@CodErro')] = None
    institution_control_number_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH_E}/NumCtrlIF/@CodErro')] = None
    debtor_institution_ispb_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH_E}/ISPBIFDebtd/@CodErro')] = None
    debtor_branch_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH_E}/AgDebtd/@CodErro')] = None
    sender_type_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH_E}/TpPessoaRemet/@CodErro')] = None
    sender_document_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH_E}/CNPJ_CPFRemet/@CodErro')] = None
    sender_name_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH_E}/NomRemet/@CodErro')] = None
    creditor_institution_ispb_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH_E}/ISPBIFCredtd/@CodErro')] = (
        None
    )
    creditor_branch_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH_E}/AgCredtd/@CodErro')] = None
    creditor_account_number_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH_E}/CtCredtd/@CodErro')] = None
    creditor_payment_account_number_error_code: Annotated[
        ErrorCode | None, XmlPath(f'{PATH_E}/CtPgtoCredtd/@CodErro')
    ] = None
    creditor_account_type_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH_E}/TpCtCredtd/@CodErro')] = None
    recipient_type_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH_E}/TpPessoaDestinatario/@CodErro')] = None
    recipient_document_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH_E}/CNPJ_CPFDestinatario/@CodErro')] = (
        None
    )
    recipient_name_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH_E}/NomDestinatario/@CodErro')] = None
    amount_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH_E}/VlrLanc/@CodErro')] = None
    purpose_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH_E}/FinlddCli/@CodErro')] = None
    description_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH_E}/Hist/@CodErro')] = None
    scheduled_date_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH_E}/DtAgendt/@CodErro')] = None
    scheduled_time_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH_E}/HrAgendt/@CodErro')] = None
    priority_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH_E}/NivelPref/@CodErro')] = None
    settlement_date_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH_E}/DtMovto/@CodErro')] = None
