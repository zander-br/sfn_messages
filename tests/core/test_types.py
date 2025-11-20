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


def test_description_accepts_valid_values() -> None:
    valid_descriptions = [
        'A' * 1,
        'This is a valid description.',
        'A' * 200,
    ]
    for description in valid_descriptions:
        model = DescriptionModel(description=description)
        assert model.description == description


def test_description_accepts_whitespace() -> None:
    model = DescriptionModel(description='  Valid description with spaces.  ')
    assert model.description == 'Valid description with spaces.'


def test_description_rejects_invalid_values() -> None:
    invalid_descriptions = [
        'A' * 201,  # Too long
    ]
    for description in invalid_descriptions:
        with pytest.raises(ValidationError) as exc:
            DescriptionModel(description=description)
        assert 'String should have at most 200 characters' in str(exc.value)


def test_institution_control_number_accepts_valid_values() -> None:
    valid_control_numbers = [
        'A',
        '1234567890',
        'ABCDEFGHIJ',
        'A1B2C3D4E5F6G7H8I9J0',
    ]
    for control_number in valid_control_numbers:
        model = InstitutionControlNumberModel(institution_control_number=control_number)
        assert model.institution_control_number == control_number


def test_institution_control_number_accepts_whitespace() -> None:
    model = InstitutionControlNumberModel(institution_control_number='  ABC123  ')
    assert model.institution_control_number == 'ABC123'


def test_institution_control_number_rejects_invalid_values() -> None:
    invalid_control_numbers = [
        '',  # Too short
        'A' * 21,  # Too long
        '  ',  # Only whitespace
    ]
    for control_number in invalid_control_numbers:
        with pytest.raises(ValidationError) as exc:
            InstitutionControlNumberModel(institution_control_number=control_number)
        assert 'String should have at least 1 character' in str(
            exc.value
        ) or 'String should have at most 20 characters' in str(exc.value)


def test_ispb_accepts_valid_values() -> None:
    valid_ispbs = [
        '12345678',
        'ABCDEFGH',
        'A1B2C3D4',
        '87654321',
        'HGFEDCBA',
        '4D3C2B1A',
    ]
    for ispb in valid_ispbs:
        model = IspbModel(ispb=ispb)
        assert model.ispb == ispb


def test_ispb_accepts_whitespace_and_case_insensitivity() -> None:
    model = IspbModel(ispb='  a1b2c3d4  ')
    assert model.ispb == 'A1B2C3D4'


def test_ispb_rejects_invalid_values() -> None:
    invalid_ispbs = [
        '1234567',  # Too short
        '123456789',  # Too long
        '1234 5678',  # Contains space
        '1234-5678',  # Contains special character
        '1234567!',  # Contains special character
        '12345@678',  # Contains special character
        '1234\n5678',  # Contains newline
    ]
    for ispb in invalid_ispbs:
        with pytest.raises(ValidationError) as exc:
            IspbModel(ispb=ispb)
        assert "String should match pattern '^[0-9A-Za-z]{8}$'" in str(exc.value)


def test_operation_number_accepts_valid_values() -> None:
    valid_operation_numbers = [
        'ABCDEFGH1234567890123',
        '1234567A1234567890123',
        'A1B2C3D41234567890123',
        'HGFEDCBA9876543210123',
        '4D3C2B1A0000000000000',
    ]
    for operation_number in valid_operation_numbers:
        model = OperationNumberModel(operation_number=operation_number)
        assert model.operation_number == operation_number


def test_operation_number_accepts_whitespace() -> None:
    model = OperationNumberModel(operation_number='  ABCDEFGH1234567890123  ')
    assert model.operation_number == 'ABCDEFGH1234567890123'


def test_operation_number_rejects_invalid_values() -> None:
    invalid_operation_numbers = [
        'ABCDEFGH123456789012',  # Too short
        'ABCDEFGH12345678901234',  # Too long
        'ABCDEFGH 1234567890123',  # Contains space
        'ABCDEFGH-1234567890123',  # Contains special character
        'ABCDEFGH12345!67890123',  # Contains special character
        'ABCDEFGH1234@67890123',  # Contains special character
        'ABCDEFGH1234\n67890123',  # Contains newline
    ]
    for operation_number in invalid_operation_numbers:
        with pytest.raises(ValidationError) as exc:
            OperationNumberModel(operation_number=operation_number)
        assert "String should match pattern '^[0-9A-Z]{8}[0-9]{13}$'" in str(exc.value)


def test_system_domain_accepts_exact_values() -> None:
    assert SystemDomain('SPB01') is SystemDomain.SPB01
    assert SystemDomain('SPB02') is SystemDomain.SPB02
    assert SystemDomain('MES01') is SystemDomain.MES01
    assert SystemDomain('MES02') is SystemDomain.MES02
    assert SystemDomain('MES03') is SystemDomain.MES03


def test_system_domain_accepts_case_insensitive_values() -> None:
    assert SystemDomain('spb01') is SystemDomain.SPB01
    assert SystemDomain('SpB02') is SystemDomain.SPB02
    assert SystemDomain('mes01') is SystemDomain.MES01
    assert SystemDomain('MeS02') is SystemDomain.MES02
    assert SystemDomain('MES03') is SystemDomain.MES03


def test_system_domain_rejects_invalid_value() -> None:
    with pytest.raises(ValueError, match='SPB03'):
        SystemDomain('SPB03')

    with pytest.raises(ValueError, match='UNKNOWN'):
        SystemDomain('UNKNOWN')
