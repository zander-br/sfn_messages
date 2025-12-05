import pytest
from pydantic import BaseModel, ValidationError

from sfn_messages.sme.types import SmeControlNumber


class SmeControlNumberModel(BaseModel):
    sme_control_number: SmeControlNumber


@pytest.mark.parametrize(
    'sme_control_number',
    ['SYS20240101011111111'],
)
def test_sme_control_number_accepts_valid_values(sme_control_number: str) -> None:
    model = SmeControlNumberModel(sme_control_number=sme_control_number)
    assert model.sme_control_number == sme_control_number.upper()


def test_sme_control_number_accepts_whitespace() -> None:
    model = SmeControlNumberModel(sme_control_number='  SYS20240101011111111  ')
    assert model.sme_control_number == 'SYS20240101011111111'


@pytest.mark.parametrize(
    'sme_control_number',
    [
        'A' * 31,  # Too short
        'A' * 33,  # Too long
        'G' * 32,  # Invalid character
    ],
)
def test_sme_control_number_rejects_invalid_values(sme_control_number: str) -> None:
    with pytest.raises(ValidationError) as exc:
        SmeControlNumberModel(sme_control_number=sme_control_number)
    assert r'[A-Z]{3}(19|20)\d{2}(0[1-9]|1[0-2])(0[1-9]|[12]\d|3[01])\d{9}$' in str(exc.value)
