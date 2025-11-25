from datetime import date, time
from decimal import Decimal
from typing import Annotated, Literal

from pydantic import model_validator
from validate_docbr import CNPJ, CPF

from sfn_messages.core.models import BaseMessage, XmlPath
from sfn_messages.core.types import (
    AccountNumber,
    AccountType,
    Branch,
    Cnpj,
    Cpf,
    CreditorName,
    CustomerPurpose,
    DebtorName,
    Description,
    InstitutionControlNumber,
    Ispb,
    PersonType,
    Priority,
    TransactionId,
)

PATH = 'DOC/SISMSG/STR0008'


class STR0008(BaseMessage):
    message_code: Annotated[Literal['STR0008'], XmlPath(f'{PATH}/CodMsg/text()')] = 'STR0008'
    institution_control_number: Annotated[InstitutionControlNumber, XmlPath(f'{PATH}/NumCtrlIF/text()')]
    debtor_institution_ispb: Annotated[Ispb, XmlPath(f'{PATH}/ISPBIFDebtd/text()')]
    debtor_branch: Annotated[Branch | None, XmlPath(f'{PATH}/AgDebtd/text()')] = None
    debtor_account_type: Annotated[AccountType, XmlPath(f'{PATH}/TpCtDebtd/text()')]
    debtor_account_number: Annotated[AccountNumber | None, XmlPath(f'{PATH}/CtDebtd/text()')] = None
    debtor_payment_account_number: Annotated[AccountNumber | None, XmlPath(f'{PATH}/CtPgtoDebtd/text()')] = None
    debtor_type: Annotated[PersonType, XmlPath(f'{PATH}/TpPessoaDebtd/text()')]
    debtor_document: Annotated[Cnpj | Cpf, XmlPath(f'{PATH}/CNPJ_CPFCliDebtd/text()')]
    debtor_name: Annotated[DebtorName, XmlPath(f'{PATH}/NomCliDebtd/text()')]
    creditor_institution_ispb: Annotated[Ispb, XmlPath(f'{PATH}/ISPBIFCredtd/text()')]
    creditor_branch: Annotated[Branch | None, XmlPath(f'{PATH}/AgCredtd/text()')] = None
    creditor_account_type: Annotated[AccountType, XmlPath(f'{PATH}/TpCtCredtd/text()')]
    creditor_account_number: Annotated[AccountNumber | None, XmlPath(f'{PATH}/CtCredtd/text()')] = None
    creditor_payment_account_number: Annotated[AccountNumber | None, XmlPath(f'{PATH}/CtPgtoCredtd/text()')] = None
    creditor_type: Annotated[PersonType, XmlPath(f'{PATH}/TpPessoaCredtd/text()')]
    creditor_document: Annotated[Cnpj | Cpf, XmlPath(f'{PATH}/CNPJ_CPFCliCredtd/text()')]
    creditor_name: Annotated[CreditorName, XmlPath(f'{PATH}/NomCliCredtd/text()')]
    amount: Annotated[Decimal, XmlPath(f'{PATH}/VlrLanc/text()')]
    purpose: Annotated[CustomerPurpose, XmlPath(f'{PATH}/FinlddCli/text()')]
    transaction_id: Annotated[TransactionId | None, XmlPath(f'{PATH}/CodIdentdTransf/text()')] = None
    description: Annotated[Description | None, XmlPath(f'{PATH}/Hist/text()')] = None
    scheduled_date: Annotated[date | None, XmlPath(f'{PATH}/DtAgendt/text()')] = None
    scheduled_time: Annotated[time | None, XmlPath(f'{PATH}/HrAgendt/text()')] = None
    priority: Annotated[Priority | None, XmlPath(f'{PATH}/NivelPref/text()')] = None
    settlement_date: Annotated[date, XmlPath(f'{PATH}/DtMovto/text()')]

    @model_validator(mode='after')
    def validate_business_rules(self) -> STR0008:
        errors: list[str] = []
        self._validate_party_document(party='debtor', errors=errors)
        self._validate_party_document(party='creditor', errors=errors)
        self._validate_account_requirements(party='debtor', errors=errors)
        self._validate_account_requirements(party='creditor', errors=errors)

        if self.purpose == CustomerPurpose.OTHERS and not self.description:
            errors.append('description is required when purpose is OTHER')

        if errors:
            raise ValueError('; '.join(errors))

        return self

    def _validate_party_document(self, party: str, errors: list[str]) -> None:
        prefix = f'{party}_'

        person_type = getattr(self, prefix + 'type')
        document = getattr(self, prefix + 'document')

        if person_type == PersonType.BUSINESS and not CNPJ().validate(document):
            errors.append(f'Invalid CNPJ for {party}_type BUSINESS')
        if person_type == PersonType.INDIVIDUAL and not CPF().validate(document):
            errors.append(f'Invalid CPF for {party}_type INDIVIDUAL')

    def _validate_account_requirements(self, party: str, errors: list[str]) -> None:
        prefix = f'{party}_'

        account_type = getattr(self, prefix + 'account_type')
        branch = getattr(self, prefix + 'branch')
        account_number = getattr(self, prefix + 'account_number')
        payment_account_number = getattr(self, prefix + 'payment_account_number')

        if account_type == AccountType.PAYMENT:
            if payment_account_number is None:
                errors.append(f'{party}_payment_account_number is required when {party}_account_type is PAYMENT')
            return

        if branch is None:
            errors.append(f'{party}_branch is required when {party}_account_type is not PAYMENT')

        if account_number is None:
            errors.append(f'{party}_account_number is required when {party}_account_type is not PAYMENT')
