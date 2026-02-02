import pytest

from sfn_messages.lpi.types import LpiPurpose


@pytest.mark.parametrize(
    ('input_value', 'expected_enum'),
    [
        ('OWN_MOVEMENT_OR_TO_SETTLER_ACCOUNT_ON_STR', LpiPurpose.OWN_MOVEMENT_OR_TO_SETTLER_ACCOUNT_ON_STR),
        ('RETURN_OF_IMPROPERLY_RECEIVED_CONTRIBUTION', LpiPurpose.RETURN_OF_IMPROPERLY_RECEIVED_CONTRIBUTION),
    ],
)
def test_lpi_purpose_accepts_exact_values(input_value: str, expected_enum: LpiPurpose) -> None:
    assert LpiPurpose(input_value) is expected_enum


@pytest.mark.parametrize(
    ('input_value', 'expected_enum'),
    [
        (LpiPurpose.OWN_MOVEMENT_OR_TO_SETTLER_ACCOUNT_ON_STR, '1'),
        (LpiPurpose.RETURN_OF_IMPROPERLY_RECEIVED_CONTRIBUTION, '2'),
    ],
)
def test_lpi_purpose_values_to_xml_value(input_value: LpiPurpose, expected_enum: str) -> None:
    assert input_value.to_xml_value() == expected_enum


@pytest.mark.parametrize(
    ('input_value', 'expected_enum'),
    [
        ('1', LpiPurpose.OWN_MOVEMENT_OR_TO_SETTLER_ACCOUNT_ON_STR),
        ('2', LpiPurpose.RETURN_OF_IMPROPERLY_RECEIVED_CONTRIBUTION),
    ],
)
def test_lpi_purpose_values_from_xml_value(input_value: str, expected_enum: LpiPurpose) -> None:
    assert LpiPurpose.from_xml_value(input_value) == expected_enum


@pytest.mark.parametrize(
    ('input_value', 'expected_enum'),
    [
        ('own_movement_or_to_settler_account_on_str', LpiPurpose.OWN_MOVEMENT_OR_TO_SETTLER_ACCOUNT_ON_STR),
        ('return_of_improperly_received_contribution', LpiPurpose.RETURN_OF_IMPROPERLY_RECEIVED_CONTRIBUTION),
    ],
)
def test_lpi_purpose_accepts_case_insensitive_values(input_value: str, expected_enum: LpiPurpose) -> None:
    assert LpiPurpose(input_value) is expected_enum
