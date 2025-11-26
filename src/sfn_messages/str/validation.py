from collections.abc import Sequence
from typing import Any, ClassVar

from pydantic import model_validator
from validate_docbr import CNPJ, CPF

from sfn_messages.core.types import (
    AccountNumber,
    AccountType,
    Branch,
    PersonType,
)


class StrPartyValidation:
    _document_parties: ClassVar[Sequence[str]] = ()
    _account_parties: ClassVar[Sequence[str]] = ()
    _others_enum_value: ClassVar[Any | None] = None
    _purpose_attr: ClassVar[str] = 'purpose'
    _description_attr: ClassVar[str] = 'description'

    @model_validator(mode='after')
    def _validate_business_rules_mixin(self) -> StrPartyValidation:
        errors: list[str] = []

        for party in self._document_parties:
            self._validate_party_document(party=party, errors=errors)

        for party in self._account_parties:
            self._validate_account_requirements(party=party, errors=errors)

        if self._others_enum_value is not None:
            purpose = getattr(self, self._purpose_attr, None)
            description = getattr(self, self._description_attr, None)
            if purpose == self._others_enum_value and not description:
                errors.append(f'{self._description_attr} is required when {self._purpose_attr} is OTHERS')

        if errors:
            raise ValueError('; '.join(errors))

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
