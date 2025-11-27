from collections.abc import Iterable
from typing import Any, ClassVar, Self

from pydantic import model_validator
from validate_docbr import CNPJ, CPF

from sfn_messages.core.types import AccountNumber, AccountType, Branch, PersonType


class PartyValidations:
    document_parties: ClassVar[list[str]] = []
    account_parties: ClassVar[list[str]] = []
    others_enum_value: ClassVar[Any | None] = None
    purpose_attr: ClassVar[str] = 'purpose'
    description_attr: ClassVar[str] = 'description'

    @classmethod
    def normalize_parties(cls, value: object) -> list[str]:
        if value is None:
            return []
        if isinstance(value, str):
            return [value]
        if isinstance(value, Iterable):
            return [str(v) for v in value]
        msg = 'Parties must be a string or iterable of strings.'
        raise TypeError(msg)

    @model_validator(mode='after')
    def validate_business_rules_mixin(self) -> Self:
        errors: list[str] = []

        doc_parties = self.normalize_parties(self.document_parties)
        acc_parties = self.normalize_parties(self.account_parties)

        for party in doc_parties:
            self._validate_party_document(party=party, errors=errors)

        for party in acc_parties:
            self._validate_account_requirements(party=party, errors=errors)

        if self.others_enum_value is not None:
            purpose = getattr(self, self.purpose_attr, None)
            description = getattr(self, self.description_attr, None)
            if purpose == self.others_enum_value and not description:
                errors.append(f'{self.description_attr} is required when {self.purpose_attr} is OTHERS')

        if errors:
            msg = '; '.join(errors)
            raise ValueError(msg)

        return self

    def _validate_party_document(self, party: str, errors: list[str]) -> None:
        prefix = f'{party}_'

        person_type: PersonType | None = getattr(self, prefix + 'type', None)
        document: str | None = getattr(self, prefix + 'document', None)

        if not person_type or not document:
            return

        if person_type == PersonType.BUSINESS and not CNPJ().validate(document):
            errors.append(f'Invalid CNPJ for {party}_type BUSINESS')
        if person_type == PersonType.INDIVIDUAL and not CPF().validate(document):
            errors.append(f'Invalid CPF for {party}_type INDIVIDUAL')

    def _validate_account_requirements(self, party: str, errors: list[str]) -> None:
        prefix = f'{party}_'

        account_type: AccountType | None = getattr(self, prefix + 'account_type', None)
        branch: Branch | None = getattr(self, prefix + 'branch', None)
        account_number: AccountNumber | None = getattr(self, prefix + 'account_number', None)
        payment_account_number: AccountNumber | None = getattr(self, prefix + 'payment_account_number', None)

        if account_type is None:
            return

        if account_type == AccountType.PAYMENT:
            if payment_account_number is None:
                errors.append(f'{party}_payment_account_number is required when {party}_account_type is PAYMENT')
            return

        if branch is None:
            errors.append(f'{party}_branch is required when {party}_account_type is not PAYMENT')

        if account_number is None:
            errors.append(f'{party}_account_number is required when {party}_account_type is not PAYMENT')
