import pytest
from pydantic import BaseModel, ValidationError

from sfn_messages.gen.types import CertificateIssue, CertificateSerialNumber


class CertificateSerialNumberModel(BaseModel):
    serial_number: CertificateSerialNumber


def test_certificate_issue_accepts_name_case_insensitive() -> None:
    assert CertificateIssue('SERPRO') is CertificateIssue.SERPRO
    assert CertificateIssue('certisign') is CertificateIssue.CERTISIGN
    assert CertificateIssue('SeRaSa') is CertificateIssue.SERASA
    assert CertificateIssue('AC_caixa') is CertificateIssue.AC_CAIXA
    assert CertificateIssue('ac_valida') is CertificateIssue.AC_VALIDA
    assert CertificateIssue('Ac_SoLuTi') is CertificateIssue.AC_SOLUTI


def test_certificate_issue_rejects_invalid_value() -> None:
    with pytest.raises(ValueError, match='UNKNOWN'):
        CertificateIssue('UNKNOWN')


def test_certificate_serial_number_accepts_valid_values() -> None:
    valid_serial_numbers = [
        'A' * 32,
        '1234567890ABCDEF1234567890abcdef',
        '0' * 32,
        'F' * 32,
    ]
    for serial_number in valid_serial_numbers:
        model = CertificateSerialNumberModel(serial_number=serial_number)
        assert model.serial_number == serial_number.upper()


def test_certificate_serial_number_accepts_whitespace() -> None:
    model = CertificateSerialNumberModel(serial_number='  A1B2C3D4E5F6A7B8C9D0E1F2A3B4C5D6  ')
    assert model.serial_number == 'A1B2C3D4E5F6A7B8C9D0E1F2A3B4C5D6'


def test_certificate_serial_number_rejects_invalid_values() -> None:
    invalid_serial_numbers = [
        'A' * 31,  # Too short
        'A' * 33,  # Too long
        'G' * 32,  # Invalid character
    ]
    for serial_number in invalid_serial_numbers:
        with pytest.raises(ValidationError) as exc:
            CertificateSerialNumberModel(serial_number=serial_number)
        assert "String should match pattern '^[0-9A-Fa-f]{32}$'" in str(exc.value)
