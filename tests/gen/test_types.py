import pytest
from pydantic import BaseModel, ValidationError

from sfn_messages.gen.types import CertificateIssue, CertificateSerialNumber, Message


class CertificateSerialNumberModel(BaseModel):
    serial_number: CertificateSerialNumber


class MessageModel(BaseModel):
    message: Message


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


@pytest.mark.parametrize(
    ('input_value', 'expected_enum'),
    [
        (CertificateIssue.SERPRO, '1'),
        (CertificateIssue.CERTISIGN, '2'),
        (CertificateIssue.SERASA, '4'),
        (CertificateIssue.AC_CAIXA, '5'),
        (CertificateIssue.AC_VALIDA, '6'),
        (CertificateIssue.AC_SOLUTI, '7'),
    ],
)
def test_certificate_issue_to_xml_value(input_value: CertificateIssue, expected_enum: str) -> None:
    assert input_value.to_xml_value() == expected_enum


@pytest.mark.parametrize(
    ('input_value', 'expected_enum'),
    [
        ('1', CertificateIssue.SERPRO),
        ('2', CertificateIssue.CERTISIGN),
        ('4', CertificateIssue.SERASA),
        ('5', CertificateIssue.AC_CAIXA),
        ('6', CertificateIssue.AC_VALIDA),
        ('7', CertificateIssue.AC_SOLUTI),
    ],
)
def test_certificate_issue_accepts_xml_value(input_value: str, expected_enum: CertificateIssue) -> None:
    assert CertificateIssue.from_xml_value(input_value) is expected_enum


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


@pytest.mark.parametrize(
    'message',
    [
        'A' * 1,
        'This is a valid message.',
        'A' * 50,
    ],
)
def test_message_accepts_valid_values(message: str) -> None:
    model = MessageModel(message=message)
    assert model.message == message


def test_message_accepts_whitespace() -> None:
    model = MessageModel(message='  Valid message.  ')
    assert model.message == 'Valid message.'


@pytest.mark.parametrize(
    'message',
    [
        'A' * 51,  # Too long
    ],
)
def test_message_rejects_invalid_values(message: str) -> None:
    with pytest.raises(ValidationError) as exc:
        MessageModel(message=message)
    assert 'String should have at most 50 characters' in str(exc.value)
