from datetime import UTC, date, datetime
from typing import Any

import pytest
from pydantic import ValidationError

from sfn_messages.gen.gen0007 import GEN0007, GEN0007E
from sfn_messages.gen.types import CertificateIssue
from tests.conftest import extract_missing_fields, normalize_xml


def make_valid_gen0007_params() -> dict[str, Any]:
    return {
        'from_ispb': '31680151',
        'to_ispb': '00038166',
        'system_domain': 'SPB01',
        'operation_number': '316801512509080000001',
        'message_code': 'GEN0007',
        'instituition_certificate': '31680151',
        'certificate': 'A' * 32,
        'certificate_issue': 'AC_SOLUTI',
        'certificate_serial_number': 'A' * 32,
        'vendor_timestamp': '2025-11-27T13:00:00+00:00',
        'settlement_date': '2025-11-27',
    }


def make_valid_gen0007e_params(*, general_error: bool = False) -> dict[str, Any]:
    gen0007e = {
        'from_ispb': '31680151',
        'to_ispb': '00038166',
        'system_domain': 'SPB01',
        'operation_number': '316801512509080000001',
        'message_code': 'GEN0007',
        'instituition_certificate': '31680151',
        'certificate': 'A' * 32,
        'certificate_issue': 'AC_SOLUTI',
        'certificate_serial_number': 'A' * 32,
        'vendor_timestamp': '2025-11-27T13:00:00+00:00',
        'settlement_date': '2025-11-27',
    }

    if general_error:
        gen0007e['general_error_code'] = 'EGEN0050'
    else:
        gen0007e['certificate_serial_number_error_code'] = 'EGEN1017'

    return gen0007e


def test_gen0007_valid_model() -> None:
    params = make_valid_gen0007_params()
    gen0007 = GEN0007.model_validate(params)

    assert isinstance(gen0007, GEN0007)
    assert gen0007.from_ispb == '31680151'
    assert gen0007.to_ispb == '00038166'
    assert gen0007.message_code == 'GEN0007'
    assert gen0007.instituition_certificate == '31680151'
    assert gen0007.certificate == 'A' * 32
    assert gen0007.certificate_issue == CertificateIssue.AC_SOLUTI
    assert gen0007.certificate_serial_number == 'A' * 32
    assert gen0007.vendor_timestamp == datetime(2025, 11, 27, 13, 0, tzinfo=UTC)
    assert gen0007.settlement_date == date(2025, 11, 27)


def test_gen0007e_general_error_valid_model() -> None:
    params = make_valid_gen0007e_params(general_error=True)
    gen0007e = GEN0007E.model_validate(params)

    assert isinstance(gen0007e, GEN0007E)
    assert gen0007e.from_ispb == '31680151'
    assert gen0007e.to_ispb == '00038166'
    assert gen0007e.message_code == 'GEN0007'
    assert gen0007e.instituition_certificate == '31680151'
    assert gen0007e.certificate == 'A' * 32
    assert gen0007e.certificate_issue == CertificateIssue.AC_SOLUTI
    assert gen0007e.certificate_serial_number == 'A' * 32
    assert gen0007e.vendor_timestamp == datetime(2025, 11, 27, 13, 0, tzinfo=UTC)
    assert gen0007e.settlement_date == date(2025, 11, 27)
    assert gen0007e.general_error_code == 'EGEN0050'


def test_gen0007e_tag_error_valid_model() -> None:
    params = make_valid_gen0007e_params()
    gen0007e = GEN0007E.model_validate(params)

    assert isinstance(gen0007e, GEN0007E)
    assert gen0007e.from_ispb == '31680151'
    assert gen0007e.to_ispb == '00038166'
    assert gen0007e.message_code == 'GEN0007'
    assert gen0007e.instituition_certificate == '31680151'
    assert gen0007e.certificate == 'A' * 32
    assert gen0007e.certificate_issue == CertificateIssue.AC_SOLUTI
    assert gen0007e.certificate_serial_number == 'A' * 32
    assert gen0007e.vendor_timestamp == datetime(2025, 11, 27, 13, 0, tzinfo=UTC)
    assert gen0007e.settlement_date == date(2025, 11, 27)
    assert gen0007e.certificate_serial_number_error_code == 'EGEN1017'


def test_gen0007_missing_required_fields() -> None:
    with pytest.raises(ValidationError) as exc:
        GEN0007.model_validate({})

    missing_fields = extract_missing_fields(exc.value)
    assert missing_fields == {
        'from_ispb',
        'to_ispb',
        'system_domain',
        'operation_number',
        'instituition_certificate',
        'certificate',
        'certificate_issue',
        'certificate_serial_number',
        'vendor_timestamp',
        'settlement_date',
    }


def test_gen0007_to_xml() -> None:
    params = make_valid_gen0007_params()
    gen0007 = GEN0007.model_validate(params)

    xml = gen0007.to_xml()

    expected_xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/GEN/GEN0007.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>316801512509080000001</NUOp>
        </BCMSG>
        <SISMSG>
            <GEN0007>
                <CodMsg>GEN0007</CodMsg>
                <ISPBIFCertif>31680151</ISPBIFCertif>
                <CertifDig>AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA</CertifDig>
                <CodCertifrAtv>7</CodCertifrAtv>
                <CertifAtv>AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA</CertifAtv>
                <DtHrBC>2025-11-27 13:00:00+00:00</DtHrBC>
                <DtMovto>2025-11-27</DtMovto>
            </GEN0007>
        </SISMSG>
    </DOC>
    """
    assert normalize_xml(expected_xml) == normalize_xml(xml)


def test_gen0007e_general_error_to_xml() -> None:
    params = make_valid_gen0007e_params(general_error=True)
    gen0007e = GEN0007E.model_validate(params)

    xml = gen0007e.to_xml()

    expected_xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/GEN/GEN0007E.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>316801512509080000001</NUOp>
        </BCMSG>
        <SISMSG>
            <GEN0007E CodErro="EGEN0050">
                <CodMsg>GEN0007</CodMsg>
                <ISPBIFCertif>31680151</ISPBIFCertif>
                <CertifDig>AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA</CertifDig>
                <CodCertifrAtv>7</CodCertifrAtv>
                <CertifAtv>AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA</CertifAtv>
                <DtHrBC>2025-11-27 13:00:00+00:00</DtHrBC>
                <DtMovto>2025-11-27</DtMovto>
            </GEN0007E>
        </SISMSG>
    </DOC>
    """
    assert normalize_xml(expected_xml) == normalize_xml(xml)


def test_gen0007e_tag_error_to_xml() -> None:
    params = make_valid_gen0007e_params()
    gen0007e = GEN0007E.model_validate(params)

    xml = gen0007e.to_xml()

    expected_xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/GEN/GEN0007E.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>316801512509080000001</NUOp>
        </BCMSG>
        <SISMSG>
            <GEN0007E>
                <CodMsg>GEN0007</CodMsg>
                <ISPBIFCertif>31680151</ISPBIFCertif>
                <CertifDig>AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA</CertifDig>
                <CodCertifrAtv>7</CodCertifrAtv>
                <CertifAtv CodErro="EGEN1017">AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA</CertifAtv>
                <DtHrBC>2025-11-27 13:00:00+00:00</DtHrBC>
                <DtMovto>2025-11-27</DtMovto>
            </GEN0007E>
        </SISMSG>
    </DOC>
    """
    assert normalize_xml(expected_xml) == normalize_xml(xml)


def test_gen0007_from_xml() -> None:
    xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/GEN/GEN0007.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>316801512509080000001</NUOp>
        </BCMSG>
        <SISMSG>
            <GEN0007>
                <CodMsg>GEN0007</CodMsg>
                <ISPBIFCertif>31680151</ISPBIFCertif>
                <CertifDig>AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA</CertifDig>
                <CodCertifrAtv>7</CodCertifrAtv>
                <CertifAtv>AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA</CertifAtv>
                <DtHrBC>2025-11-27 13:00:00+00:00</DtHrBC>
                <DtMovto>2025-11-27</DtMovto>
            </GEN0007>
        </SISMSG>
    </DOC>
    """

    gen0007 = GEN0007.from_xml(xml)

    assert isinstance(gen0007, GEN0007)
    assert gen0007.from_ispb == '31680151'
    assert gen0007.to_ispb == '00038166'
    assert gen0007.message_code == 'GEN0007'
    assert gen0007.instituition_certificate == '31680151'
    assert gen0007.certificate == 'A' * 32
    assert gen0007.certificate_issue == CertificateIssue.AC_SOLUTI
    assert gen0007.certificate_serial_number == 'A' * 32
    assert gen0007.vendor_timestamp == datetime(2025, 11, 27, 13, 0, tzinfo=UTC)
    assert gen0007.settlement_date == date(2025, 11, 27)


def test_gen0007e_general_error_from_xml() -> None:
    xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/GEN/GEN0007E.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>316801512509080000001</NUOp>
        </BCMSG>
        <SISMSG>
            <GEN0007E CodErro="EGEN0050">
                <CodMsg>GEN0007</CodMsg>
                <ISPBIFCertif>31680151</ISPBIFCertif>
                <CertifDig>AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA</CertifDig>
                <CodCertifrAtv>7</CodCertifrAtv>
                <CertifAtv>AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA</CertifAtv>
                <DtHrBC>2025-11-27 13:00:00+00:00</DtHrBC>
                <DtMovto>2025-11-27</DtMovto>
            </GEN0007E>
        </SISMSG>
    </DOC>
    """

    gen0007e = GEN0007E.from_xml(xml)

    assert isinstance(gen0007e, GEN0007E)
    assert gen0007e.from_ispb == '31680151'
    assert gen0007e.to_ispb == '00038166'
    assert gen0007e.message_code == 'GEN0007'
    assert gen0007e.instituition_certificate == '31680151'
    assert gen0007e.certificate == 'A' * 32
    assert gen0007e.certificate_issue == CertificateIssue.AC_SOLUTI
    assert gen0007e.certificate_serial_number == 'A' * 32
    assert gen0007e.vendor_timestamp == datetime(2025, 11, 27, 13, 0, tzinfo=UTC)
    assert gen0007e.settlement_date == date(2025, 11, 27)
    assert gen0007e.general_error_code == 'EGEN0050'


def test_gen0007e_tag_error_from_xml() -> None:
    xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/GEN/GEN0007E.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>316801512509080000001</NUOp>
        </BCMSG>
        <SISMSG>
            <GEN0007E>
                <CodMsg>GEN0007</CodMsg>
                <ISPBIFCertif>31680151</ISPBIFCertif>
                <CertifDig>AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA</CertifDig>
                <CodCertifrAtv>7</CodCertifrAtv>
                <CertifAtv CodErro="EGEN1017">AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA</CertifAtv>
                <DtHrBC>2025-11-27 13:00:00+00:00</DtHrBC>
                <DtMovto>2025-11-27</DtMovto>
            </GEN0007E>
        </SISMSG>
    </DOC>
    """

    gen0007e = GEN0007E.from_xml(xml)

    assert isinstance(gen0007e, GEN0007E)
    assert gen0007e.from_ispb == '31680151'
    assert gen0007e.to_ispb == '00038166'
    assert gen0007e.message_code == 'GEN0007'
    assert gen0007e.instituition_certificate == '31680151'
    assert gen0007e.certificate == 'A' * 32
    assert gen0007e.certificate_issue == CertificateIssue.AC_SOLUTI
    assert gen0007e.certificate_serial_number == 'A' * 32
    assert gen0007e.vendor_timestamp == datetime(2025, 11, 27, 13, 0, tzinfo=UTC)
    assert gen0007e.settlement_date == date(2025, 11, 27)
    assert gen0007e.certificate_serial_number_error_code == 'EGEN1017'


def test_gen0007_roundtrip() -> None:
    params = make_valid_gen0007_params()

    gen0007 = GEN0007.model_validate(params)
    xml = gen0007.to_xml()
    gen0007_from_xml = GEN0007.from_xml(xml)

    assert gen0007 == gen0007_from_xml


def test_gen0007_from_xml_missing_required_fields() -> None:
    xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/GEN/GEN0007.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>316801512509080000001</NUOp>
        </BCMSG>
        <SISMSG>
            <GEN0007>
                <CodMsg>GEN0007</CodMsg>
            </GEN0007>
        </SISMSG>
    </DOC>
    """

    with pytest.raises(ValidationError) as exc:
        GEN0007.from_xml(xml)

    missing_fields = extract_missing_fields(exc.value)
    assert missing_fields == {
        'instituition_certificate',
        'certificate',
        'certificate_issue',
        'certificate_serial_number',
        'vendor_timestamp',
        'settlement_date',
    }
