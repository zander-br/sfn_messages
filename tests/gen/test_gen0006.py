from datetime import date, datetime
from typing import Any

import pytest
from pydantic import ValidationError

from sfn_messages.core.types import SystemDomain
from sfn_messages.gen.gen0006 import GEN0006, GEN0006E, GEN0006R1
from sfn_messages.gen.types import CertificateIssue
from tests.conftest import extract_missing_fields, normalize_xml


def make_valid_gen0006_params() -> dict[str, Any]:
    return {
        'certificate_issue': 'SERPRO',
        'certificate_serial_number': 'A' * 32,
        'description': 'Test GEN0006',
        'from_ispb': '31680151',
        'institution_control_number': '123',
        'institution_ispb': '31680151',
        'operation_number': '31680151250908000000001',
        'settlement_date': '2025-11-20',
        'system_domain': 'SPB01',
        'to_ispb': '00038166',
    }


def make_valid_gen0006r1_params() -> dict[str, Any]:
    return {
        'from_ispb': '00638166',
        'institution_control_number': '123',
        'institution_ispb': '31680151',
        'operation_number': '31680151250908000000001',
        'vendor_timestamp': '2025-11-20T15:30:00',
        'settlement_date': '2025-11-20',
        'system_domain': 'SPB01',
        'to_ispb': '31680151',
    }


def make_valid_gen0006e_params(*, general_error: bool = False) -> dict[str, Any]:
    gen0006e = {
        'certificate_issue': 'SERPRO',
        'certificate_serial_number': 'A' * 32,
        'description': 'Test GEN0006',
        'from_ispb': '31680151',
        'institution_control_number': '123',
        'institution_ispb': '31680151',
        'operation_number': '31680151250908000000001',
        'settlement_date': '2025-11-20',
        'system_domain': 'SPB01',
        'to_ispb': '00038166',
    }

    if general_error:
        gen0006e['general_error_code'] = 'EGEN0050'
    else:
        gen0006e['institution_ispb_error_code'] = 'EGEN0051'

    return gen0006e


def test_gen0006_valid_model() -> None:
    params = make_valid_gen0006_params()
    gen0006 = GEN0006.model_validate(params)

    assert isinstance(gen0006, GEN0006)
    assert gen0006.certificate_issue == CertificateIssue.SERPRO
    assert gen0006.certificate_serial_number == 'A' * 32
    assert gen0006.description == 'Test GEN0006'
    assert gen0006.from_ispb == '31680151'
    assert gen0006.institution_control_number == '123'
    assert gen0006.institution_ispb == '31680151'
    assert gen0006.message_code == 'GEN0006'
    assert gen0006.operation_number == '31680151250908000000001'
    assert gen0006.settlement_date == date(2025, 11, 20)
    assert gen0006.system_domain == SystemDomain.SPB01
    assert gen0006.to_ispb == '00038166'


def test_gen0006e_general_error_valid_model() -> None:
    params = make_valid_gen0006e_params(general_error=True)
    gen0006e = GEN0006E.model_validate(params)

    assert isinstance(gen0006e, GEN0006E)
    assert gen0006e.certificate_issue == CertificateIssue.SERPRO
    assert gen0006e.certificate_serial_number == 'A' * 32
    assert gen0006e.description == 'Test GEN0006'
    assert gen0006e.from_ispb == '31680151'
    assert gen0006e.institution_control_number == '123'
    assert gen0006e.institution_ispb == '31680151'
    assert gen0006e.message_code == 'GEN0006E'
    assert gen0006e.operation_number == '31680151250908000000001'
    assert gen0006e.settlement_date == date(2025, 11, 20)
    assert gen0006e.system_domain == SystemDomain.SPB01
    assert gen0006e.to_ispb == '00038166'
    assert gen0006e.general_error_code == 'EGEN0050'


def test_gen0006e_tag_error_valid_model() -> None:
    params = make_valid_gen0006e_params()
    gen0006e = GEN0006E.model_validate(params)

    assert isinstance(gen0006e, GEN0006E)
    assert gen0006e.certificate_issue == CertificateIssue.SERPRO
    assert gen0006e.certificate_serial_number == 'A' * 32
    assert gen0006e.description == 'Test GEN0006'
    assert gen0006e.from_ispb == '31680151'
    assert gen0006e.institution_control_number == '123'
    assert gen0006e.institution_ispb == '31680151'
    assert gen0006e.message_code == 'GEN0006E'
    assert gen0006e.operation_number == '31680151250908000000001'
    assert gen0006e.settlement_date == date(2025, 11, 20)
    assert gen0006e.system_domain == SystemDomain.SPB01
    assert gen0006e.to_ispb == '00038166'
    assert gen0006e.institution_ispb_error_code == 'EGEN0051'


def test_gen0006_missing_required_fields() -> None:
    with pytest.raises(ValidationError) as exc:
        GEN0006.model_validate({})

    missing_fields = extract_missing_fields(exc.value)
    assert missing_fields == {
        'operation_number',
        'certificate_issue',
        'from_ispb',
        'institution_control_number',
        'institution_ispb',
        'system_domain',
        'to_ispb',
        'settlement_date',
        'certificate_serial_number',
    }


def test_gen0006_to_xml() -> None:
    params = make_valid_gen0006_params()

    gen0006 = GEN0006.model_validate(params)
    xml = gen0006.to_xml()

    expected_xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/GEN/GEN0006.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>31680151250908000000001</NUOp>
        </BCMSG>
        <SISMSG>
            <GEN0006>
                <CodMsg>GEN0006</CodMsg>
                <NumCtrlIF>123</NumCtrlIF>
                <ISPBIF>31680151</ISPBIF>
                <CodCertifrAtv>1</CodCertifrAtv>
                <CertifAtv>AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA</CertifAtv>
                <Hist>Test GEN0006</Hist>
                <DtMovto>2025-11-20</DtMovto>
            </GEN0006>
        </SISMSG>
    </DOC>
    """
    assert normalize_xml(expected_xml) == normalize_xml(xml)


def test_gen0006_to_xml_omit_optional_fields() -> None:
    params = make_valid_gen0006_params()
    del params['description']

    gen0006 = GEN0006.model_validate(params)
    xml = gen0006.to_xml()

    expected_xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/GEN/GEN0006.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>31680151250908000000001</NUOp>
        </BCMSG>
        <SISMSG>
            <GEN0006>
                <CodMsg>GEN0006</CodMsg>
                <NumCtrlIF>123</NumCtrlIF>
                <ISPBIF>31680151</ISPBIF>
                <CodCertifrAtv>1</CodCertifrAtv>
                <CertifAtv>AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA</CertifAtv>
                <DtMovto>2025-11-20</DtMovto>
            </GEN0006>
        </SISMSG>
    </DOC>
    """
    assert normalize_xml(expected_xml) == normalize_xml(xml)


def test_gen0006e_general_error_to_xml() -> None:
    params = make_valid_gen0006e_params(general_error=True)

    gen0006e = GEN0006E.model_validate(params)
    xml = gen0006e.to_xml()

    expected_xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/GEN/GEN0006E.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>31680151250908000000001</NUOp>
        </BCMSG>
        <SISMSG>
            <GEN0006 CodErro="EGEN0050">
                <CodMsg>GEN0006E</CodMsg>
                <NumCtrlIF>123</NumCtrlIF>
                <ISPBIF>31680151</ISPBIF>
                <CodCertifrAtv>1</CodCertifrAtv>
                <CertifAtv>AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA</CertifAtv>
                <Hist>Test GEN0006</Hist>
                <DtMovto>2025-11-20</DtMovto>
            </GEN0006>
        </SISMSG>
    </DOC>
    """
    assert normalize_xml(expected_xml) == normalize_xml(xml)


def test_gen0006e_tag_error_to_xml() -> None:
    params = make_valid_gen0006e_params()

    gen0006e = GEN0006E.model_validate(params)
    xml = gen0006e.to_xml()

    expected_xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/GEN/GEN0006E.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>31680151250908000000001</NUOp>
        </BCMSG>
        <SISMSG>
            <GEN0006>
                <CodMsg>GEN0006E</CodMsg>
                <NumCtrlIF>123</NumCtrlIF>
                <ISPBIF CodErro="EGEN0051">31680151</ISPBIF>
                <CodCertifrAtv>1</CodCertifrAtv>
                <CertifAtv>AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA</CertifAtv>
                <Hist>Test GEN0006</Hist>
                <DtMovto>2025-11-20</DtMovto>
            </GEN0006>
        </SISMSG>
    </DOC>
    """
    assert normalize_xml(expected_xml) == normalize_xml(xml)


def test_gen0006_from_xml() -> None:
    xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/GEN/GEN0006.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>31680151250908000000001</NUOp>
        </BCMSG>
        <SISMSG>
            <GEN0006>
                <CodMsg>GEN0006</CodMsg>
                <NumCtrlIF>123</NumCtrlIF>
                <ISPBIF>31680151</ISPBIF>
                <CodCertifrAtv>1</CodCertifrAtv>
                <CertifAtv>AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA</CertifAtv>
                <Hist>Test GEN0006</Hist>
                <DtMovto>2025-11-20</DtMovto>
            </GEN0006>
        </SISMSG>
    </DOC>
    """

    gen0006 = GEN0006.from_xml(xml)

    assert isinstance(gen0006, GEN0006)
    assert gen0006.certificate_issue == CertificateIssue.SERPRO
    assert gen0006.certificate_serial_number == 'A' * 32
    assert gen0006.description == 'Test GEN0006'
    assert gen0006.from_ispb == '31680151'
    assert gen0006.institution_control_number == '123'
    assert gen0006.institution_ispb == '31680151'
    assert gen0006.message_code == 'GEN0006'
    assert gen0006.operation_number == '31680151250908000000001'
    assert gen0006.settlement_date == date(2025, 11, 20)
    assert gen0006.system_domain == SystemDomain.SPB01
    assert gen0006.to_ispb == '00038166'


def test_gen0006e_general_error_from_xml() -> None:
    xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/GEN/GEN0006E.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>31680151250908000000001</NUOp>
        </BCMSG>
        <SISMSG>
            <GEN0006 CodErro="EGEN0050">
                <CodMsg>GEN0006E</CodMsg>
                <NumCtrlIF>123</NumCtrlIF>
                <ISPBIF>31680151</ISPBIF>
                <CodCertifrAtv>1</CodCertifrAtv>
                <CertifAtv>AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA</CertifAtv>
                <Hist>Test GEN0006</Hist>
                <DtMovto>2025-11-20</DtMovto>
            </GEN0006>
        </SISMSG>
    </DOC>
    """

    gen0006e = GEN0006E.from_xml(xml)

    assert isinstance(gen0006e, GEN0006E)
    assert gen0006e.certificate_issue == CertificateIssue.SERPRO
    assert gen0006e.certificate_serial_number == 'A' * 32
    assert gen0006e.description == 'Test GEN0006'
    assert gen0006e.from_ispb == '31680151'
    assert gen0006e.institution_control_number == '123'
    assert gen0006e.institution_ispb == '31680151'
    assert gen0006e.message_code == 'GEN0006E'
    assert gen0006e.operation_number == '31680151250908000000001'
    assert gen0006e.settlement_date == date(2025, 11, 20)
    assert gen0006e.system_domain == SystemDomain.SPB01
    assert gen0006e.to_ispb == '00038166'
    assert gen0006e.general_error_code == 'EGEN0050'


def test_gen0006e_tag_error_from_xml() -> None:
    xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/GEN/GEN0006E.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>31680151250908000000001</NUOp>
        </BCMSG>
        <SISMSG>
            <GEN0006>
                <CodMsg>GEN0006E</CodMsg>
                <NumCtrlIF>123</NumCtrlIF>
                <ISPBIF CodErro="EGEN0051">31680151</ISPBIF>
                <CodCertifrAtv>1</CodCertifrAtv>
                <CertifAtv>AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA</CertifAtv>
                <Hist>Test GEN0006</Hist>
                <DtMovto>2025-11-20</DtMovto>
            </GEN0006>
        </SISMSG>
    </DOC>
    """

    gen0006e = GEN0006E.from_xml(xml)

    assert isinstance(gen0006e, GEN0006E)
    assert gen0006e.certificate_issue == CertificateIssue.SERPRO
    assert gen0006e.certificate_serial_number == 'A' * 32
    assert gen0006e.description == 'Test GEN0006'
    assert gen0006e.from_ispb == '31680151'
    assert gen0006e.institution_control_number == '123'
    assert gen0006e.institution_ispb == '31680151'
    assert gen0006e.message_code == 'GEN0006E'
    assert gen0006e.operation_number == '31680151250908000000001'
    assert gen0006e.settlement_date == date(2025, 11, 20)
    assert gen0006e.system_domain == SystemDomain.SPB01
    assert gen0006e.to_ispb == '00038166'
    assert gen0006e.institution_ispb_error_code == 'EGEN0051'


def test_gen0006_from_xml_missing_optional_fields() -> None:
    xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/GEN/GEN0006.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>31680151250908000000001</NUOp>
        </BCMSG>
        <SISMSG>
            <GEN0006>
                <CodMsg>GEN0006</CodMsg>
                <NumCtrlIF>123</NumCtrlIF>
                <ISPBIF>31680151</ISPBIF>
                <CodCertifrAtv>1</CodCertifrAtv>
                <CertifAtv>AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA</CertifAtv>
                <DtMovto>2025-11-20</DtMovto>
            </GEN0006>
        </SISMSG>
    </DOC>
    """

    gen0006 = GEN0006.from_xml(xml)

    assert isinstance(gen0006, GEN0006)
    assert gen0006.description is None


def test_gen0006_roundtrip() -> None:
    params = make_valid_gen0006_params()

    gen0006 = GEN0006.model_validate(params)
    xml = gen0006.to_xml()
    gen0006_from_xml = GEN0006.from_xml(xml)

    assert gen0006 == gen0006_from_xml


def test_gen0006_from_xml_missing_required_fields() -> None:
    xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/GEN/GEN0006.xsd">
      <BCMSG>
        <IdentdEmissor>31680151</IdentdEmissor>
        <IdentdDestinatario>00038166</IdentdDestinatario>
        <DomSist>SPB01</DomSist>
        <NUOp>31680151250908000000001</NUOp>
      </BCMSG>
      <SISMSG>
        <GEN0006>
          <CodMsg>GEN0006</CodMsg>
          <NumCtrlIF>123</NumCtrlIF>
          <ISPBIF>31680151</ISPBIF>
          <DtMovto>2025-11-20</DtMovto>
        </GEN0006>
      </SISMSG>
    </DOC>
    """

    with pytest.raises(ValidationError) as exc:
        GEN0006.from_xml(xml)

    missing_fields = extract_missing_fields(exc.value)
    assert missing_fields == {
        'certificate_issue',
        'certificate_serial_number',
    }


def test_gen0006r1_valid_model() -> None:
    params = make_valid_gen0006r1_params()
    gen0006r1 = GEN0006R1.model_validate(params)

    assert isinstance(gen0006r1, GEN0006R1)
    assert gen0006r1.from_ispb == '00638166'
    assert gen0006r1.institution_control_number == '123'
    assert gen0006r1.institution_ispb == '31680151'
    assert gen0006r1.message_code == 'GEN0006R1'
    assert gen0006r1.operation_number == '31680151250908000000001'
    assert gen0006r1.vendor_timestamp == datetime(2025, 11, 20, 15, 30)
    assert gen0006r1.settlement_date == date(2025, 11, 20)
    assert gen0006r1.system_domain == SystemDomain.SPB01
    assert gen0006r1.to_ispb == '31680151'


def test_gen0006r1_missing_required_fields() -> None:
    with pytest.raises(ValidationError) as exc:
        GEN0006R1.model_validate({})

    missing_fields = extract_missing_fields(exc.value)
    assert missing_fields == {
        'system_domain',
        'institution_ispb',
        'operation_number',
        'to_ispb',
        'vendor_timestamp',
        'from_ispb',
        'institution_control_number',
        'settlement_date',
    }


def test_gen0006r1_to_xml() -> None:
    params = make_valid_gen0006r1_params()

    gen0006r1 = GEN0006R1.model_validate(params)
    xml = gen0006r1.to_xml()

    expected_xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/GEN/GEN0006.xsd">
        <BCMSG>
            <IdentdEmissor>00638166</IdentdEmissor>
            <IdentdDestinatario>31680151</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>31680151250908000000001</NUOp>
        </BCMSG>
        <SISMSG>
            <GEN0006R1>
                <CodMsg>GEN0006R1</CodMsg>
                <NumCtrlIF>123</NumCtrlIF>
                <ISPBIF>31680151</ISPBIF>
                <DtHrBC>2025-11-20T15:30:00</DtHrBC>
                <DtMovto>2025-11-20</DtMovto>
            </GEN0006R1>
        </SISMSG>
    </DOC>
    """
    assert normalize_xml(expected_xml) == normalize_xml(xml)


def test_gen0006r1_from_xml() -> None:
    xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/GEN/GEN0006.xsd">
        <BCMSG>
            <IdentdEmissor>00638166</IdentdEmissor>
            <IdentdDestinatario>31680151</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>31680151250908000000001</NUOp>
        </BCMSG>
        <SISMSG>
            <GEN0006R1>
                <CodMsg>GEN0006R1</CodMsg>
                <NumCtrlIF>123</NumCtrlIF>
                <ISPBIF>31680151</ISPBIF>
                <DtHrBC>2025-11-20T15:30:00</DtHrBC>
                <DtMovto>2025-11-20</DtMovto>
            </GEN0006R1>
        </SISMSG>
    </DOC>
    """

    gen0006r1 = GEN0006R1.from_xml(xml)

    assert isinstance(gen0006r1, GEN0006R1)
    assert gen0006r1.from_ispb == '00638166'
    assert gen0006r1.institution_control_number == '123'
    assert gen0006r1.institution_ispb == '31680151'
    assert gen0006r1.message_code == 'GEN0006R1'
    assert gen0006r1.operation_number == '31680151250908000000001'
    assert gen0006r1.vendor_timestamp == datetime(2025, 11, 20, 15, 30)
    assert gen0006r1.settlement_date == date(2025, 11, 20)
    assert gen0006r1.system_domain == SystemDomain.SPB01
    assert gen0006r1.to_ispb == '31680151'


def test_gen0006r1_roundtrip() -> None:
    params = make_valid_gen0006r1_params()

    gen0006r1 = GEN0006R1.model_validate(params)
    xml = gen0006r1.to_xml()
    gen0006r1_from_xml = GEN0006R1.from_xml(xml)

    assert gen0006r1 == gen0006r1_from_xml


def test_gen0006r1_from_xml_missing_required_fields() -> None:
    xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/GEN/GEN0006.xsd">
        <BCMSG>
            <IdentdEmissor>00638166</IdentdEmissor>
            <IdentdDestinatario>31680151</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>31680151250908000000001</NUOp>
        </BCMSG>
        <SISMSG>
            <GEN0006R1>
                <CodMsg>GEN0006R1</CodMsg>
                <NumCtrlIF>123</NumCtrlIF>
                <DtMovto>2025-11-20</DtMovto>
            </GEN0006R1>
        </SISMSG>
    </DOC>
    """

    with pytest.raises(ValidationError) as exc:
        GEN0006R1.from_xml(xml)

    missing_fields = extract_missing_fields(exc.value)
    assert missing_fields == {
        'vendor_timestamp',
        'institution_ispb',
    }
