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
    CreditContractNumber,
    CreditorName,
    Description,
    InstitutionControlNumber,
    Ispb,
    PersonType,
    Priority,
    SenderName,
    TransactionId,
)

from .types import InstitutionPurpose

PATH = 'DOC/SISMSG/STR0007'


class STR0007(BaseMessage):
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

    @model_validator(mode='after')
    def validate_business_rules(self) -> STR0007:
        errors: list[str] = []
        self._validate_party_document(party='sender', errors=errors)
        self._validate_party_document(party='creditor', errors=errors)
        self._validate_account_requirements(party='creditor', errors=errors)

        if self.purpose == InstitutionPurpose.OTHERS and not self.description:
            errors.append('description is required when purpose is OTHERS')

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
