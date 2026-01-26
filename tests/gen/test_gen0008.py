from datetime import date, datetime
from typing import Any

import pytest
from pydantic import ValidationError

from sfn_messages.gen.gen0008 import GEN0008, GEN0008E, GEN0008R1
from tests.conftest import extract_missing_fields, normalize_xml


def make_valid_gen0008_params() -> dict[str, Any]:
    return {
        'from_ispb': '31680151',
        'to_ispb': '00038166',
        'system_domain': 'SPB01',
        'operation_number': '31680151250908000000001',
        'message_code': 'GEN0008',
        'institution_control_number': '123',
        'institution_ispb': '31680151',
        'instituition_certificate': '31680151',
        'settlement_date': '2025-11-26',
    }


def make_valid_gen0008r1_params() -> dict[str, Any]:
    return {
        'from_ispb': '31680151',
        'to_ispb': '00038166',
        'system_domain': 'SPB01',
        'operation_number': '31680151250908000000001',
        'message_code': 'GEN0008R1',
        'institution_control_number': '123',
        'institution_ispb': '31680151',
        'instituition_certificate': '31680151',
        'settlement_date': '2025-11-26',
        'vendor_timestamp': '2025-11-26T14:02:00',
    }


def make_valid_gen0008e_params(*, general_error: bool = False) -> dict[str, Any]:
    gen0008e = {
        'from_ispb': '31680151',
        'to_ispb': '00038166',
        'system_domain': 'SPB01',
        'operation_number': '31680151250908000000001',
        'message_code': 'GEN0008E',
        'institution_control_number': '123',
        'institution_ispb': '31680151',
        'instituition_certificate': '31680151',
        'settlement_date': '2025-11-26',
    }

    if general_error:
        gen0008e['general_error_code'] = 'EGEN0050'
    else:
        gen0008e['institution_ispb_error_code'] = 'EGEN0051'

    return gen0008e


def test_gen0008_valid_model() -> None:
    params = make_valid_gen0008_params()
    gen0008 = GEN0008.model_validate(params)

    assert isinstance(gen0008, GEN0008)
    assert gen0008.from_ispb == '31680151'
    assert gen0008.to_ispb == '00038166'
    assert gen0008.message_code == 'GEN0008'
    assert gen0008.instituition_certificate == '31680151'
    assert gen0008.settlement_date == date(2025, 11, 26)


def test_gen0008r1_valid_model() -> None:
    params = make_valid_gen0008r1_params()
    gen0008r1 = GEN0008R1.model_validate(params)

    assert isinstance(gen0008r1, GEN0008R1)
    assert gen0008r1.from_ispb == '31680151'
    assert gen0008r1.to_ispb == '00038166'
    assert gen0008r1.message_code == 'GEN0008R1'
    assert gen0008r1.instituition_certificate == '31680151'
    assert gen0008r1.settlement_date == date(2025, 11, 26)
    assert gen0008r1.vendor_timestamp == datetime(2025, 11, 26, 14, 2)


def test_gen0008e_general_error_valid_model() -> None:
    params = make_valid_gen0008e_params(general_error=True)
    gen0008e = GEN0008E.model_validate(params)

    assert isinstance(gen0008e, GEN0008E)
    assert gen0008e.from_ispb == '31680151'
    assert gen0008e.to_ispb == '00038166'
    assert gen0008e.message_code == 'GEN0008E'
    assert gen0008e.instituition_certificate == '31680151'
    assert gen0008e.settlement_date == date(2025, 11, 26)
    assert gen0008e.general_error_code == 'EGEN0050'


def test_gen0008e_tag_error_valid_model() -> None:
    params = make_valid_gen0008e_params()
    gen0008e = GEN0008E.model_validate(params)

    assert isinstance(gen0008e, GEN0008E)
    assert gen0008e.from_ispb == '31680151'
    assert gen0008e.to_ispb == '00038166'
    assert gen0008e.message_code == 'GEN0008E'
    assert gen0008e.instituition_certificate == '31680151'
    assert gen0008e.settlement_date == date(2025, 11, 26)
    assert gen0008e.institution_ispb_error_code == 'EGEN0051'


def test_gen0008_missing_required_fields() -> None:
    with pytest.raises(ValidationError) as exc:
        GEN0008.model_validate({})

    missing_fields = extract_missing_fields(exc.value)
    assert missing_fields == {
        'from_ispb',
        'to_ispb',
        'system_domain',
        'operation_number',
        'institution_control_number',
        'institution_ispb',
        'instituition_certificate',
        'settlement_date',
    }


def test_gen0008r1_missing_required_fields() -> None:
    with pytest.raises(ValidationError) as exc:
        GEN0008R1.model_validate({})

    missing_fields = extract_missing_fields(exc.value)
    assert missing_fields == {
        'from_ispb',
        'to_ispb',
        'system_domain',
        'operation_number',
        'institution_control_number',
        'institution_ispb',
        'instituition_certificate',
        'vendor_timestamp',
    }


def test_gen0008_to_xml() -> None:
    params = make_valid_gen0008_params()
    gen0008 = GEN0008.model_validate(params)

    xml = gen0008.to_xml()

    expected_xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/GEN/GEN0008.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>31680151250908000000001</NUOp>
        </BCMSG>
        <SISMSG>
            <GEN0008>
                <CodMsg>GEN0008</CodMsg>
                <NumCtrlIF>123</NumCtrlIF>
                <ISPBIF>31680151</ISPBIF>
                <ISPBIFCertif>31680151</ISPBIFCertif>
                <DtMovto>2025-11-26</DtMovto>
            </GEN0008>
        </SISMSG>
    </DOC>
    """
    assert normalize_xml(expected_xml) == normalize_xml(xml)


def test_gen0008r1_to_xml() -> None:
    params = make_valid_gen0008r1_params()
    gen0008r1 = GEN0008R1.model_validate(params)

    xml = gen0008r1.to_xml()

    expected_xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/GEN/GEN0008.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>31680151250908000000001</NUOp>
        </BCMSG>
        <SISMSG>
            <GEN0008R1>
                <CodMsg>GEN0008R1</CodMsg>
                <NumCtrlIF>123</NumCtrlIF>
                <ISPBIF>31680151</ISPBIF>
                <ISPBIFCertif>31680151</ISPBIFCertif>
                <DtMovto>2025-11-26</DtMovto>
                <DtHrBC>2025-11-26T14:02:00</DtHrBC>
            </GEN0008R1>
        </SISMSG>
    </DOC>
    """
    assert normalize_xml(expected_xml) == normalize_xml(xml)


def test_gen0008e_general_error_to_xml() -> None:
    params = make_valid_gen0008e_params(general_error=True)
    gen0008e = GEN0008E.model_validate(params)

    xml = gen0008e.to_xml()

    expected_xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/GEN/GEN0008E.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>31680151250908000000001</NUOp>
        </BCMSG>
        <SISMSG>
            <GEN0008 CodErro="EGEN0050">
                <CodMsg>GEN0008E</CodMsg>
                <NumCtrlIF>123</NumCtrlIF>
                <ISPBIF>31680151</ISPBIF>
                <ISPBIFCertif>31680151</ISPBIFCertif>
                <DtMovto>2025-11-26</DtMovto>
            </GEN0008>
        </SISMSG>
    </DOC>
    """
    assert normalize_xml(expected_xml) == normalize_xml(xml)


def test_gen0008e_tag_error_to_xml() -> None:
    params = make_valid_gen0008e_params()
    gen0008e = GEN0008E.model_validate(params)

    xml = gen0008e.to_xml()

    expected_xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/GEN/GEN0008E.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>31680151250908000000001</NUOp>
        </BCMSG>
        <SISMSG>
            <GEN0008>
                <CodMsg>GEN0008E</CodMsg>
                <NumCtrlIF>123</NumCtrlIF>
                <ISPBIF CodErro="EGEN0051">31680151</ISPBIF>
                <ISPBIFCertif>31680151</ISPBIFCertif>
                <DtMovto>2025-11-26</DtMovto>
            </GEN0008>
        </SISMSG>
    </DOC>
    """
    assert normalize_xml(expected_xml) == normalize_xml(xml)


def test_gen0008_from_xml() -> None:
    xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/GEN/GEN0008.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>31680151250908000000001</NUOp>
        </BCMSG>
        <SISMSG>
            <GEN0008>
                <CodMsg>GEN0008</CodMsg>
                <NumCtrlIF>123</NumCtrlIF>
                <ISPBIF>31680151</ISPBIF>
                <ISPBIFCertif>31680151</ISPBIFCertif>
                <DtMovto>2025-11-26</DtMovto>
            </GEN0008>
        </SISMSG>
    </DOC>
    """

    gen0008 = GEN0008.from_xml(xml)

    assert isinstance(gen0008, GEN0008)
    assert gen0008.from_ispb == '31680151'
    assert gen0008.to_ispb == '00038166'
    assert gen0008.message_code == 'GEN0008'
    assert gen0008.instituition_certificate == '31680151'
    assert gen0008.settlement_date == date(2025, 11, 26)


def test_gen0008r1_from_xml() -> None:
    xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/GEN/GEN0008.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>31680151250908000000001</NUOp>
        </BCMSG>
        <SISMSG>
            <GEN0008R1>
                <CodMsg>GEN0008R1</CodMsg>
                <NumCtrlIF>123</NumCtrlIF>
                <ISPBIF>31680151</ISPBIF>
                <ISPBIFCertif>31680151</ISPBIFCertif>
                <DtMovto>2025-11-26</DtMovto>
                <DtHrBC>2025-11-26T14:02:00</DtHrBC>
            </GEN0008R1>
        </SISMSG>
    </DOC>
    """

    gen0008r1 = GEN0008R1.from_xml(xml)

    assert isinstance(gen0008r1, GEN0008R1)
    assert gen0008r1.from_ispb == '31680151'
    assert gen0008r1.to_ispb == '00038166'
    assert gen0008r1.message_code == 'GEN0008R1'
    assert gen0008r1.instituition_certificate == '31680151'
    assert gen0008r1.settlement_date == date(2025, 11, 26)
    assert gen0008r1.vendor_timestamp == datetime(2025, 11, 26, 14, 2)


def test_gen0008e_general_error_from_xml() -> None:
    xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/GEN/GEN0008E.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>31680151250908000000001</NUOp>
        </BCMSG>
        <SISMSG>
            <GEN0008 CodErro="EGEN0050">
                <CodMsg>GEN0008E</CodMsg>
                <NumCtrlIF>123</NumCtrlIF>
                <ISPBIF>31680151</ISPBIF>
                <ISPBIFCertif>31680151</ISPBIFCertif>
                <DtMovto>2025-11-26</DtMovto>
            </GEN0008>
        </SISMSG>
    </DOC>
    """

    gen0008e = GEN0008E.from_xml(xml)

    assert isinstance(gen0008e, GEN0008E)
    assert gen0008e.from_ispb == '31680151'
    assert gen0008e.to_ispb == '00038166'
    assert gen0008e.message_code == 'GEN0008E'
    assert gen0008e.instituition_certificate == '31680151'
    assert gen0008e.settlement_date == date(2025, 11, 26)
    assert gen0008e.general_error_code == 'EGEN0050'


def test_gen0008e_tag_error_from_xml() -> None:
    xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/GEN/GEN0008E.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>31680151250908000000001</NUOp>
        </BCMSG>
        <SISMSG>
            <GEN0008>
                <CodMsg>GEN0008E</CodMsg>
                <NumCtrlIF>123</NumCtrlIF>
                <ISPBIF CodErro="EGEN0051">31680151</ISPBIF>
                <ISPBIFCertif>31680151</ISPBIFCertif>
                <DtMovto>2025-11-26</DtMovto>
            </GEN0008>
        </SISMSG>
    </DOC>
    """

    gen0008e = GEN0008E.from_xml(xml)

    assert isinstance(gen0008e, GEN0008E)
    assert gen0008e.from_ispb == '31680151'
    assert gen0008e.to_ispb == '00038166'
    assert gen0008e.message_code == 'GEN0008E'
    assert gen0008e.instituition_certificate == '31680151'
    assert gen0008e.settlement_date == date(2025, 11, 26)
    assert gen0008e.institution_ispb_error_code == 'EGEN0051'


def test_gen0008_roundtrip() -> None:
    params = make_valid_gen0008_params()

    gen0008 = GEN0008.model_validate(params)
    xml = gen0008.to_xml()
    gen0008_from_xml = GEN0008.from_xml(xml)

    assert gen0008 == gen0008_from_xml


def test_gen0008r1_roundtrip() -> None:
    params = make_valid_gen0008r1_params()

    gen0008r1 = GEN0008R1.model_validate(params)
    xml = gen0008r1.to_xml()
    gen0008r1_from_xml = GEN0008R1.from_xml(xml)

    assert gen0008r1 == gen0008r1_from_xml


def test_gen0008_from_xml_missing_required_fields() -> None:
    xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/GEN/GEN0008.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>31680151250908000000001</NUOp>
        </BCMSG>
        <SISMSG>
            <GEN0008>
                <CodMsg>GEN0008</CodMsg>
            </GEN0008>
        </SISMSG>
    </DOC>
    """

    with pytest.raises(ValidationError) as exc:
        GEN0008.from_xml(xml)

    missing_fields = extract_missing_fields(exc.value)
    assert missing_fields == {
        'institution_control_number',
        'institution_ispb',
        'instituition_certificate',
        'settlement_date',
    }


def test_gen0008r1_from_xml_missing_required_fields() -> None:
    xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/GEN/GEN0008.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>31680151250908000000001</NUOp>
        </BCMSG>
        <SISMSG>
            <GEN0008R1>
                <CodMsg>GEN0008R1</CodMsg>
            </GEN0008R1>
        </SISMSG>
    </DOC>
    """

    with pytest.raises(ValidationError) as exc:
        GEN0008R1.from_xml(xml)

    missing_fields = extract_missing_fields(exc.value)
    assert missing_fields == {
        'institution_control_number',
        'institution_ispb',
        'instituition_certificate',
        'vendor_timestamp',
    }
