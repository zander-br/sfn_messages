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

PATH = 'DOC/SISMSG/STR0008'
PATH_R1 = 'DOC/SISMSG/STR0008R1'
PATH_R2 = 'DOC/SISMSG/STR0008R2'
XML_NAMESPACE = 'http://www.bcb.gov.br/SPB/STR0008.xsd'


class STR0008(PartyValidations, BaseMessage):
    XML_NAMESPACE: ClassVar[str | None] = XML_NAMESPACE

    document_parties: ClassVar[list[str]] = ['debtor', 'creditor']
    account_parties: ClassVar[list[str]] = ['debtor', 'creditor']
    others_enum_value: ClassVar[CustomerPurpose | None] = CustomerPurpose.OTHERS
    purpose_attr: ClassVar[str] = 'purpose'
    description_attr: ClassVar[str] = 'description'

    message_code: Annotated[Literal['STR0008'], XmlPath(f'{PATH}/CodMsg/text()')] = 'STR0008'
    institution_control_number: Annotated[InstitutionControlNumber, XmlPath(f'{PATH}/NumCtrlIF/text()')]
    debtor_institution_ispb: Annotated[Ispb, XmlPath(f'{PATH}/ISPBIFDebtd/text()')]
    debtor_branch: Annotated[Branch | None, XmlPath(f'{PATH}/AgDebtd/text()')] = None
    debtor_account_type: Annotated[AccountType, XmlPath(f'{PATH}/TpCtDebtd/text()')]
    debtor_account_number: Annotated[AccountNumber | None, XmlPath(f'{PATH}/CtDebtd/text()')] = None
    debtor_payment_account_number: Annotated[AccountNumber | None, XmlPath(f'{PATH}/CtPgtoDebtd/text()')] = None
    debtor_type: Annotated[PersonType, XmlPath(f'{PATH}/TpPessoaDebtd/text()')]
    debtor_document: Annotated[Cnpj | Cpf, XmlPath(f'{PATH}/CNPJ_CPFCliDebtd/text()')]
    debtor_name: Annotated[Name, XmlPath(f'{PATH}/NomCliDebtd/text()')]
    creditor_institution_ispb: Annotated[Ispb, XmlPath(f'{PATH}/ISPBIFCredtd/text()')]
    creditor_branch: Annotated[Branch | None, XmlPath(f'{PATH}/AgCredtd/text()')] = None
    creditor_account_type: Annotated[AccountType, XmlPath(f'{PATH}/TpCtCredtd/text()')]
    creditor_account_number: Annotated[AccountNumber | None, XmlPath(f'{PATH}/CtCredtd/text()')] = None
    creditor_payment_account_number: Annotated[AccountNumber | None, XmlPath(f'{PATH}/CtPgtoCredtd/text()')] = None
    creditor_type: Annotated[PersonType, XmlPath(f'{PATH}/TpPessoaCredtd/text()')]
    creditor_document: Annotated[Cnpj | Cpf, XmlPath(f'{PATH}/CNPJ_CPFCliCredtd/text()')]
    creditor_name: Annotated[Name, XmlPath(f'{PATH}/NomCliCredtd/text()')]
    amount: Annotated[Decimal, XmlPath(f'{PATH}/VlrLanc/text()')]
    purpose: Annotated[CustomerPurpose, XmlPath(f'{PATH}/FinlddCli/text()')]
    transaction_id: Annotated[TransactionId | None, XmlPath(f'{PATH}/CodIdentdTransf/text()')] = None
    description: Annotated[Description | None, XmlPath(f'{PATH}/Hist/text()')] = None
    scheduled_date: Annotated[date | None, XmlPath(f'{PATH}/DtAgendt/text()')] = None
    scheduled_time: Annotated[time | None, XmlPath(f'{PATH}/HrAgendt/text()')] = None
    priority: Annotated[Priority | None, XmlPath(f'{PATH}/NivelPref/text()')] = None
    settlement_date: Annotated[date, XmlPath(f'{PATH}/DtMovto/text()')]


class STR0008R1(BaseMessage):
    XML_NAMESPACE: ClassVar[str | None] = XML_NAMESPACE

    message_code: Annotated[Literal['STR0008R1'], XmlPath(f'{PATH_R1}/CodMsg/text()')] = 'STR0008R1'
    institution_control_number: Annotated[InstitutionControlNumber, XmlPath(f'{PATH_R1}/NumCtrlIF/text()')]
    debtor_institution_ispb: Annotated[Ispb, XmlPath(f'{PATH_R1}/ISPBIFDebtd/text()')]
    str_control_number: Annotated[StrControlNumber, XmlPath(f'{PATH_R1}/NumCtrlSTR/text()')]
    str_settlement_status: Annotated[StrSettlementStatus, XmlPath(f'{PATH_R1}/SitLancSTR/text()')]
    settlement_timestamp: Annotated[datetime, XmlPath(f'{PATH_R1}/DtHrSit/text()')]
    settlement_date: Annotated[date, XmlPath(f'{PATH_R1}/DtMovto/text()')]


class STR0008R2(PartyValidations, BaseMessage):
    XML_NAMESPACE: ClassVar[str | None] = XML_NAMESPACE

    document_parties: ClassVar[list[str]] = ['debtor', 'creditor']
    account_parties: ClassVar[list[str]] = ['debtor', 'creditor']
    others_enum_value: ClassVar[CustomerPurpose | None] = CustomerPurpose.OTHERS
    purpose_attr: ClassVar[str] = 'purpose'
    description_attr: ClassVar[str] = 'description'

    message_code: Annotated[Literal['STR0008R2'], XmlPath(f'{PATH_R2}/CodMsg/text()')] = 'STR0008R2'
    str_control_number: Annotated[StrControlNumber, XmlPath(f'{PATH_R2}/NumCtrlSTR/text()')]
    vendor_timestamp: Annotated[datetime, XmlPath(f'{PATH_R2}/DtHrBC/text()')]
    debtor_institution_ispb: Annotated[Ispb, XmlPath(f'{PATH_R2}/ISPBIFDebtd/text()')]
    debtor_branch: Annotated[Branch | None, XmlPath(f'{PATH_R2}/AgDebtd/text()')] = None
    debtor_account_type: Annotated[AccountType, XmlPath(f'{PATH_R2}/TpCtDebtd/text()')]
    debtor_account_number: Annotated[AccountNumber | None, XmlPath(f'{PATH_R2}/CtDebtd/text()')] = None
    debtor_payment_account_number: Annotated[AccountNumber | None, XmlPath(f'{PATH_R2}/CtPgtoDebtd/text()')] = None
    debtor_type: Annotated[PersonType, XmlPath(f'{PATH_R2}/TpPessoaDebtd/text()')]
    debtor_document: Annotated[Cnpj | Cpf, XmlPath(f'{PATH_R2}/CNPJ_CPFCliDebtd/text()')]
    debtor_name: Annotated[Name, XmlPath(f'{PATH_R2}/NomCliDebtd/text()')]
    creditor_institution_ispb: Annotated[Ispb, XmlPath(f'{PATH_R2}/ISPBIFCredtd/text()')]
    creditor_branch: Annotated[Branch | None, XmlPath(f'{PATH_R2}/AgCredtd/text()')] = None
    creditor_account_type: Annotated[AccountType, XmlPath(f'{PATH_R2}/TpCtCredtd/text()')]
    creditor_account_number: Annotated[AccountNumber | None, XmlPath(f'{PATH_R2}/CtCredtd/text()')] = None
    creditor_payment_account_number: Annotated[AccountNumber | None, XmlPath(f'{PATH_R2}/CtPgtoCredtd/text()')] = None
    creditor_type: Annotated[PersonType, XmlPath(f'{PATH_R2}/TpPessoaCredtd/text()')]
    creditor_document: Annotated[Cnpj | Cpf, XmlPath(f'{PATH_R2}/CNPJ_CPFCliCredtd/text()')]
    creditor_name: Annotated[Name, XmlPath(f'{PATH_R2}/NomCliCredtd/text()')]
    amount: Annotated[Decimal, XmlPath(f'{PATH_R2}/VlrLanc/text()')]
    purpose: Annotated[CustomerPurpose, XmlPath(f'{PATH_R2}/FinlddCli/text()')]
    transaction_id: Annotated[TransactionId | None, XmlPath(f'{PATH_R2}/CodIdentdTransf/text()')] = None
    description: Annotated[Description | None, XmlPath(f'{PATH_R2}/Hist/text()')] = None
    settlement_date: Annotated[date, XmlPath(f'{PATH_R2}/DtMovto/text()')]
