import pytest
from pydantic import BaseModel, ValidationError

from sfn_messages.gen.types import CertificateIssue, CertificateSerialNumber


class CertificateSerialNumberModel(BaseModel):
    serial_number: CertificateSerialNumber


@pytest.mark.parametrize(
    ('input_value', 'expected_enum'),
    [
        ('SERPRO', CertificateIssue.SERPRO),
        ('certisign', CertificateIssue.CERTISIGN),
        ('SeRaSa', CertificateIssue.SERASA),
        ('AC_caixa', CertificateIssue.AC_CAIXA),
        ('ac_valida', CertificateIssue.AC_VALIDA),
        ('Ac_SoLuTi', CertificateIssue.AC_SOLUTI),
    ],
)
def test_certificate_issue_accepts_name_case_insensitive(input_value: str, expected_enum: CertificateIssue) -> None:
    assert CertificateIssue(input_value) is expected_enum


def test_certificate_issue_rejects_invalid_value() -> None:
    with pytest.raises(ValueError, match='UNKNOWN'):
        CertificateIssue('UNKNOWN')


@pytest.mark.parametrize(
    'serial_number',
    [
        'A' * 32,
        '1234567890ABCDEF1234567890abcdef',
        '0' * 32,
        'F' * 32,
    ],
)
def test_certificate_serial_number_accepts_valid_values(serial_number: str) -> None:
    model = CertificateSerialNumberModel(serial_number=serial_number)
    assert model.serial_number == serial_number.upper()


def test_certificate_serial_number_accepts_whitespace() -> None:
    model = CertificateSerialNumberModel(serial_number='  A1B2C3D4E5F6A7B8C9D0E1F2A3B4C5D6  ')
    assert model.serial_number == 'A1B2C3D4E5F6A7B8C9D0E1F2A3B4C5D6'


@pytest.mark.parametrize(
    'serial_number',
    [
        'A' * 31,  # Too short
        'A' * 33,  # Too long
        'G' * 32,  # Invalid character
    ],
)
def test_certificate_serial_number_rejects_invalid_values(serial_number: str) -> None:
    with pytest.raises(ValidationError) as exc:
        CertificateSerialNumberModel(serial_number=serial_number)
    assert "String should match pattern '^[0-9A-Fa-f]{32}$'" in str(exc.value)
