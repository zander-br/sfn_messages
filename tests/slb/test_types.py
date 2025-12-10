import pytest
from pydantic import BaseModel, ValidationError

from sfn_messages.slb.types import SlbControlNumber


class SlbControlNumberModel(BaseModel):
    slb_control_number: SlbControlNumber


@pytest.mark.parametrize(
    'slb_control_number',
    ['SLB20240101011111111'],
)
def test_slb_control_number_accepts_valid_values(slb_control_number: str) -> None:
    model = SlbControlNumberModel(slb_control_number=slb_control_number)
    assert model.slb_control_number == slb_control_number.upper()


def test_slb_control_number_accepts_whitespace() -> None:
    model = SlbControlNumberModel(slb_control_number='  SLB20240101011111111  ')
    assert model.slb_control_number == 'SLB20240101011111111'


@pytest.mark.parametrize(
    'slb_control_number',
    [
        'A' * 31,  # Too short
        'A' * 33,  # Too long
        'G' * 32,  # Invalid character
    ],
)
def test_sme_control_number_rejects_invalid_values(slb_control_number: str) -> None:
    with pytest.raises(ValidationError) as exc:
        SlbControlNumberModel(slb_control_number=slb_control_number)
    assert r'^SLB\d{4}(0[1-9]|1[0-2])(0[1-9]|[12]\d|3[01])\d{9}$' in str(exc.value)
