from enum import Enum
from typing import ClassVar

import pytest
from _pytest.monkeypatch import MonkeyPatch
from pydantic import BaseModel, ValidationError
from validate_docbr import CNPJ, CPF

from sfn_messages.core.types import AccountType, PersonType
from sfn_messages.str.validations import PartyValidations


class DummyPurpose(Enum):
    SALARY = 'SALARY'
    OTHERS = 'OTHERS'


class DummyMessage(PartyValidations, BaseModel):
    document_parties: ClassVar[list[str]] = ['debtor', 'creditor']
    account_parties: ClassVar[list[str]] = ['debtor', 'creditor']
    others_enum_value: ClassVar[DummyPurpose | None] = DummyPurpose.OTHERS
    purpose_attr: ClassVar[str] = 'purpose'
    description_attr: ClassVar[str] = 'description'

    debtor_type: PersonType | None = None
    debtor_document: str | None = None
    debtor_account_type: AccountType | None = None
    debtor_branch: str | None = None
    debtor_account_number: str | None = None
    debtor_payment_account_number: str | None = None

    creditor_type: PersonType | None = None
    creditor_document: str | None = None
    creditor_account_type: AccountType | None = None
    creditor_branch: str | None = None
    creditor_account_number: str | None = None
    creditor_payment_account_number: str | None = None

    purpose: DummyPurpose | None = None
    description: str | None = None


class NoPartyMessage(PartyValidations, BaseModel):
    document_parties: ClassVar[list[str]] = []
    account_parties: ClassVar[list[str]] = []
    purpose: DummyPurpose | None = None
    description: str | None = None


def test_normalize_parties_none_returns_empty() -> None:
    assert PartyValidations.normalize_parties(None) == []


def test_normalize_parties_string_returns_singleton_list() -> None:
    assert PartyValidations.normalize_parties('debtor') == ['debtor']


def test_normalize_parties_iterable_returns_list_of_strings() -> None:
    result = PartyValidations.normalize_parties(['debtor', 'creditor'])
    assert result == ['debtor', 'creditor']


def test_normalize_parties_unsupported_type_raises_typeerror() -> None:
    with pytest.raises(TypeError, match='Parties must be a string or iterable of strings'):
        PartyValidations.normalize_parties(123)


def test_valid_business_and_individual_documents(monkeypatch: MonkeyPatch) -> None:
    monkeypatch.setattr(CNPJ, 'validate', lambda _self, _v: True, raising=False)
    monkeypatch.setattr(CPF, 'validate', lambda _self, _v: True, raising=False)

    msg = DummyMessage(
        debtor_type=PersonType.BUSINESS,
        debtor_document='qualquer',
        debtor_account_type=AccountType.PAYMENT,
        debtor_payment_account_number='123',
        creditor_type=PersonType.INDIVIDUAL,
        creditor_document='qualquer',
        creditor_account_type=AccountType.PAYMENT,
        creditor_payment_account_number='456',
        purpose=DummyPurpose.SALARY,
    )

    assert msg.debtor_type == PersonType.BUSINESS


def test_invalid_cnpj_for_business_raises(monkeypatch: MonkeyPatch) -> None:
    monkeypatch.setattr(CNPJ, 'validate', lambda _self, _v: False, raising=False)
    monkeypatch.setattr(CPF, 'validate', lambda _self, _v: True, raising=False)

    with pytest.raises(ValidationError) as exc:
        DummyMessage(
            debtor_type=PersonType.BUSINESS,
            debtor_document='invalid',
            debtor_account_type=AccountType.PAYMENT,
            debtor_payment_account_number='123',
        )
    msg = str(exc.value)
    assert 'Invalid CNPJ for debtor_type BUSINESS' in msg


def test_invalid_cpf_for_individual_raises(monkeypatch: MonkeyPatch) -> None:
    monkeypatch.setattr(CNPJ, 'validate', lambda _self, _v: True, raising=False)
    monkeypatch.setattr(CPF, 'validate', lambda _self, _v: False, raising=False)

    with pytest.raises(ValidationError) as exc:
        DummyMessage(
            creditor_type=PersonType.INDIVIDUAL,
            creditor_document='invalid',
            creditor_account_type=AccountType.PAYMENT,
            creditor_payment_account_number='123',
        )
    msg = str(exc.value)
    assert 'Invalid CPF for creditor_type INDIVIDUAL' in msg


def test_payment_requires_payment_account_number() -> None:
    with pytest.raises(ValidationError) as exc:
        DummyMessage(
            debtor_account_type=AccountType.PAYMENT,
            debtor_payment_account_number=None,
            creditor_account_type=AccountType.PAYMENT,
            creditor_payment_account_number='ok',
        )
    msg = str(exc.value)
    assert 'debtor_payment_account_number is required when debtor_account_type is PAYMENT' in msg


def test_non_payment_requires_branch_and_account_number() -> None:
    with pytest.raises(ValidationError) as exc:
        DummyMessage(
            debtor_account_type=AccountType.CURRENT,
            debtor_branch=None,
            debtor_account_number=None,
            creditor_account_type=AccountType.PAYMENT,
            creditor_payment_account_number='ok',
        )
    msg = str(exc.value)
    assert 'debtor_branch is required when debtor_account_type is not PAYMENT' in msg
    assert 'debtor_account_number is required when debtor_account_type is not PAYMENT' in msg


def test_non_payment_ok_when_branch_and_account_present() -> None:
    msg = DummyMessage(
        debtor_account_type=AccountType.CURRENT,
        debtor_branch='0001',
        debtor_account_number='123',
        creditor_account_type=AccountType.PAYMENT,
        creditor_payment_account_number='ok',
    )
    assert msg.debtor_branch == '0001'
    assert msg.debtor_account_number == '123'


def test_description_required_when_purpose_is_others() -> None:
    with pytest.raises(ValidationError) as exc:
        DummyMessage(
            debtor_account_type=AccountType.PAYMENT,
            debtor_payment_account_number='123',
            creditor_account_type=AccountType.PAYMENT,
            creditor_payment_account_number='456',
            purpose=DummyPurpose.OTHERS,
            description=None,
        )
    msg = str(exc.value)
    assert 'description is required when purpose is OTHERS' in msg


def test_description_not_required_when_purpose_not_others() -> None:
    msg = DummyMessage(
        debtor_account_type=AccountType.PAYMENT,
        debtor_payment_account_number='123',
        creditor_account_type=AccountType.PAYMENT,
        creditor_payment_account_number='456',
        purpose=DummyPurpose.SALARY,
        description=None,
    )
    assert msg.description is None


def test_no_parties_no_validations_run() -> None:
    msg = NoPartyMessage()
    assert msg.purpose is None
