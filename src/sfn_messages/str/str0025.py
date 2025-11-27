from datetime import date, time
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
    InstitutionControlNumber,
    Ispb,
    Name,
    PersonType,
    Priority,
)

from .validations import PartyValidations

PATH = 'DOC/SISMSG/STR0025'


class STR0025(PartyValidations, BaseMessage):
    document_parties: ClassVar[list[str]] = ['creditor']
    account_parties: ClassVar[list[str]] = ['debtor']

    message_code: Annotated[Literal['STR0025'], XmlPath(f'{PATH}/CodMsg/text()')] = 'STR0025'
    institution_control_number: Annotated[InstitutionControlNumber, XmlPath(f'{PATH}/NumCtrlIF/text()')]
    debtor_institution_ispb: Annotated[Ispb, XmlPath(f'{PATH}/ISPBIFDebtd/text()')]
    debtor_branch: Annotated[Branch | None, XmlPath(f'{PATH}/AgDebtd/text()')] = None
    debtor_account_type: Annotated[AccountType | None, XmlPath(f'{PATH}/TpCtDebtd/text()')] = None
    debtor_account_number: Annotated[AccountNumber | None, XmlPath(f'{PATH}/CtDebtd/text()')] = None
    debtor_payment_account_number: Annotated[AccountNumber | None, XmlPath(f'{PATH}/CtPgtoDebtd/text()')] = None
    creditor_name: Annotated[Name, XmlPath(f'{PATH}/NomCliCredtd/text()')]
    creditor_type: Annotated[PersonType, XmlPath(f'{PATH}/TpPessoaCredtd/text()')]
    creditor_document: Annotated[Cnpj | Cpf, XmlPath(f'{PATH}/CNPJ_CPFCliCredtd/text()')]
    creditor_institution_ispb: Annotated[Ispb, XmlPath(f'{PATH}/ISPBIFCredtd/text()')]
    amount: Annotated[Decimal, XmlPath(f'{PATH}/VlrLanc/text()')]
    priority: Annotated[Priority | None, XmlPath(f'{PATH}/NivelPref/text()')] = None
    deposit_identifier: Annotated[DepositIdentifier, XmlPath(f'{PATH}/IdentcDep/text()')]
    scheduled_date: Annotated[date | None, XmlPath(f'{PATH}/DtAgendt/text()')] = None
    scheduled_time: Annotated[time | None, XmlPath(f'{PATH}/HrAgendt/text()')] = None
    settlement_date: Annotated[date, XmlPath(f'{PATH}/DtMovto/text()')]
