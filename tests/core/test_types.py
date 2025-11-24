import pytest
from pydantic import BaseModel, ValidationError

from sfn_messages.core.types import (
    Description,
    InstitutionControlNumber,
    Ispb,
    OperationNumber,
    SystemDomain,
)


class DescriptionModel(BaseModel):
    description: Description


class InstitutionControlNumberModel(BaseModel):
    institution_control_number: InstitutionControlNumber


class IspbModel(BaseModel):
    ispb: Ispb


class OperationNumberModel(BaseModel):
    operation_number: OperationNumber


@pytest.mark.parametrize(
    'description',
    [
        'A' * 1,
        'This is a valid description.',
        'A' * 200,
    ],
)
def test_description_accepts_valid_values(description: str) -> None:
    model = DescriptionModel(description=description)
    assert model.description == description


def test_description_accepts_whitespace() -> None:
    model = DescriptionModel(description='  Valid description with spaces.  ')
    assert model.description == 'Valid description with spaces.'


@pytest.mark.parametrize(
    'description',
    [
        'A' * 201,  # Too long
    ],
)
def test_description_rejects_invalid_values(description: str) -> None:
    with pytest.raises(ValidationError) as exc:
        DescriptionModel(description=description)
    assert 'String should have at most 200 characters' in str(exc.value)


@pytest.mark.parametrize(
    'institution_control_number',
    [
        'A' * 1,
        '1234567890',
        'ABCDEFGHIJ',
        'A1B2C3D4E5F6G7H8I9J0',
    ],
)
def test_institution_control_number_accepts_valid_values(institution_control_number: str) -> None:
    model = InstitutionControlNumberModel(institution_control_number=institution_control_number)
    assert model.institution_control_number == institution_control_number


def test_institution_control_number_accepts_whitespace() -> None:
    model = InstitutionControlNumberModel(institution_control_number='  ABC123  ')
    assert model.institution_control_number == 'ABC123'


@pytest.mark.parametrize(
    'control_number',
    [
        '',  # Too short
        'A' * 21,  # Too long,
        '  ',  # Only whitespace
    ],
)
def test_institution_control_number_rejects_invalid_values(control_number: str) -> None:
    with pytest.raises(ValidationError) as exc:
        InstitutionControlNumberModel(institution_control_number=control_number)
    assert 'String should have at least 1 character' in str(
        exc.value
    ) or 'String should have at most 20 characters' in str(exc.value)


@pytest.mark.parametrize(
    'ispb',
    [
        '12345678',
        'ABCDEFGH',
        'A1B2C3D4',
        '87654321',
        'HGFEDCBA',
        '4D3C2B1A',
    ],
)
def test_ispb_accepts_valid_values(ispb: str) -> None:
    model = IspbModel(ispb=ispb)
    assert model.ispb == ispb


def test_ispb_accepts_whitespace_and_case_insensitivity() -> None:
    model = IspbModel(ispb='  a1b2c3d4  ')
    assert model.ispb == 'A1B2C3D4'


@pytest.mark.parametrize(
    'ispb',
    [
        '1234567',  # Too short
        '123456789',  # Too long
        '1234 5678',  # Contains space
        '1234-5678',  # Contains special character
        '1234567!',  # Contains special character
        '12345@678',  # Contains special character
        '1234\n5678',  # Contains newline
    ],
)
def test_ispb_rejects_invalid_values(ispb: str) -> None:
    with pytest.raises(ValidationError) as exc:
        IspbModel(ispb=ispb)
    assert "String should match pattern '^[0-9A-Za-z]{8}$'" in str(exc.value)


@pytest.mark.parametrize(
    'operation_number',
    [
        'ABCDEFGH1234567890123',
        '1234567A1234567890123',
        'A1B2C3D41234567890123',
        'HGFEDCBA9876543210123',
        '4D3C2B1A0000000000000',
    ],
)
def test_operation_number_accepts_valid_values(operation_number: str) -> None:
    model = OperationNumberModel(operation_number=operation_number)
    assert model.operation_number == operation_number


def test_operation_number_accepts_whitespace() -> None:
    model = OperationNumberModel(operation_number='  ABCDEFGH1234567890123  ')
    assert model.operation_number == 'ABCDEFGH1234567890123'


@pytest.mark.parametrize(
    'operation_number',
    [
        'ABCDEFGH123456789012',  # Too short
        'ABCDEFGH12345678901234',  # Too long
        'ABCDEFGH 1234567890123',  # Contains space
        'ABCDEFGH-1234567890123',  # Contains special character
        'ABCDEFGH12345!67890123',  # Contains special character
        'ABCDEFGH1234@67890123',  # Contains special character
        'ABCDEFGH1234\n67890123',  # Contains newline
    ],
)
def test_operation_number_rejects_invalid_values(operation_number: str) -> None:
    with pytest.raises(ValidationError) as exc:
        OperationNumberModel(operation_number=operation_number)
    assert "String should match pattern '^[0-9A-Z]{8}[0-9]{13}$'" in str(exc.value)


@pytest.mark.parametrize(
    ('input_value', 'expected_enum'),
    [
        ('SPB01', SystemDomain.SPB01),
        ('SPB02', SystemDomain.SPB02),
        ('MES01', SystemDomain.MES01),
        ('MES02', SystemDomain.MES02),
        ('MES03', SystemDomain.MES03),
    ],
)
def test_system_domain_accepts_exact_values(input_value: str, expected_enum: SystemDomain) -> None:
    assert SystemDomain(input_value) is expected_enum


@pytest.mark.parametrize(
    ('input_value', 'expected_enum'),
    [
        ('spb01', SystemDomain.SPB01),
        ('spb02', SystemDomain.SPB02),
        ('mes01', SystemDomain.MES01),
        ('mes02', SystemDomain.MES02),
        ('mes03', SystemDomain.MES03),
    ],
)
def test_system_domain_accepts_case_insensitive_values(input_value: str, expected_enum: SystemDomain) -> None:
    assert SystemDomain(input_value) is expected_enum


@pytest.mark.parametrize(
    'invalid_value',
    [
        'SPB0',  # Too short
        'SPB001',  # Too long
        'MES04',  # Invalid MES code
        'ABC01',  # Invalid prefix
    ],
)
def test_system_domain_rejects_invalid_value(invalid_value: str) -> None:
    with pytest.raises(ValueError, match=invalid_value):
        SystemDomain(invalid_value)
