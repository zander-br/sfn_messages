from typing import Any

import pytest
from pydantic import ValidationError
from xmlschema import XMLResource, XMLSchema

from sfn_messages.gen.gen0001 import GEN0001, GEN0001E, GEN0001R1
from tests.conftest import extract_missing_fields, normalize_xml


def make_valid_gen0001_params() -> dict[str, Any]:
    return {
        'from_ispb': '31680151',
        'to_ispb': '00038166',
        'system_domain': 'SPB01',
        'operation_number': '31680151250908000000001',
        'message_code': 'GEN0001',
        'issuing_ispb': '31680151',
        'recipient_ispb': '31680151',
        'message': 'Message test GEN0001',
    }


def make_valid_gen0001r1_params() -> dict[str, Any]:
    return {
        'from_ispb': '31680151',
        'to_ispb': '00038166',
        'system_domain': 'SPB01',
        'operation_number': '31680151250908000000001',
        'message_code': 'GEN0001R1',
        'issuing_ispb': '31680151',
        'recipient_ispb': '31680151',
        'message': 'Message test GEN0001R1',
    }


def make_valid_gen0001e_params(*, general_error: bool = False) -> dict[str, Any]:
    gen0001e = {
        'from_ispb': '31680151',
        'to_ispb': '00038166',
        'system_domain': 'SPB01',
        'operation_number': '31680151250908000000001',
        'message_code': 'GEN0001E',
        'issuing_ispb': '31680151',
        'recipient_ispb': '31680151',
        'message': 'Message test GEN0001',
    }

    if general_error:
        gen0001e['general_error_code'] = 'EGEN0050'
    else:
        gen0001e['issuing_ispb_error_code'] = 'EGEN0051'

    return gen0001e


def test_gen0001_valid_model() -> None:
    params = make_valid_gen0001_params()
    gen0001 = GEN0001.model_validate(params)

    assert isinstance(gen0001, GEN0001)
    assert gen0001.issuing_ispb == '31680151'
    assert gen0001.recipient_ispb == '31680151'
    assert gen0001.message == 'Message test GEN0001'


def test_gen0001r1_valid_model() -> None:
    params = make_valid_gen0001r1_params()
    gen0001r1 = GEN0001R1.model_validate(params)

    assert isinstance(gen0001r1, GEN0001R1)
    assert gen0001r1.issuing_ispb == '31680151'
    assert gen0001r1.recipient_ispb == '31680151'
    assert gen0001r1.message == 'Message test GEN0001R1'


def test_gen0001e_general_error_valid_model() -> None:
    params = make_valid_gen0001e_params(general_error=True)
    gen0001e = GEN0001E.model_validate(params)

    assert isinstance(gen0001e, GEN0001E)
    assert gen0001e.issuing_ispb == '31680151'
    assert gen0001e.recipient_ispb == '31680151'
    assert gen0001e.message == 'Message test GEN0001'
    assert gen0001e.general_error_code == 'EGEN0050'


def test_gen0001e_tag_error_valid_model() -> None:
    params = make_valid_gen0001e_params()
    gen0001e = GEN0001E.model_validate(params)

    assert isinstance(gen0001e, GEN0001E)
    assert gen0001e.issuing_ispb == '31680151'
    assert gen0001e.recipient_ispb == '31680151'
    assert gen0001e.message == 'Message test GEN0001'
    assert gen0001e.issuing_ispb_error_code == 'EGEN0051'


def test_gen0001_missing_required_fields() -> None:
    with pytest.raises(ValidationError) as exc:
        GEN0001.model_validate({})

    missing_fields = extract_missing_fields(exc.value)
    assert missing_fields == {
        'issuing_ispb',
        'from_ispb',
        'operation_number',
        'recipient_ispb',
        'message',
        'to_ispb',
        'system_domain',
    }


def test_gen0001r1_missing_required_fields() -> None:
    with pytest.raises(ValidationError) as exc:
        GEN0001R1.model_validate({})

    missing_fields = extract_missing_fields(exc.value)
    assert missing_fields == {
        'issuing_ispb',
        'from_ispb',
        'operation_number',
        'recipient_ispb',
        'message',
        'to_ispb',
        'system_domain',
    }


def test_gen0001_to_xml() -> None:
    params = make_valid_gen0001_params()

    gen0001 = GEN0001.model_validate(params)
    xml = gen0001.to_xml()

    expected_xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/GEN/GEN0001.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>31680151250908000000001</NUOp>
        </BCMSG>
        <SISMSG>
            <GEN0001>
                <CodMsg>GEN0001</CodMsg>
                <ISPBEmissor>31680151</ISPBEmissor>
                <ISPBDestinatario>31680151</ISPBDestinatario>
                <MsgECO>Message test GEN0001</MsgECO>
            </GEN0001>
        </SISMSG>
    </DOC>
    """

    XMLSchema('data/xsd/GEN/GEN0001.XSD').validate(XMLResource(xml))
    assert normalize_xml(expected_xml) == normalize_xml(xml)


def test_gen0001r1_to_xml() -> None:
    params = make_valid_gen0001r1_params()

    gen0001r1 = GEN0001R1.model_validate(params)
    xml = gen0001r1.to_xml()

    expected_xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/GEN/GEN0001.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>31680151250908000000001</NUOp>
        </BCMSG>
        <SISMSG>
            <GEN0001R1>
                <CodMsg>GEN0001R1</CodMsg>
                <ISPBEmissor>31680151</ISPBEmissor>
                <ISPBDestinatario>31680151</ISPBDestinatario>
                <MsgECO>Message test GEN0001R1</MsgECO>
            </GEN0001R1>
        </SISMSG>
    </DOC>
    """

    XMLSchema('data/xsd/GEN/GEN0001.XSD').validate(XMLResource(xml))
    assert normalize_xml(expected_xml) == normalize_xml(xml)


def test_gen0001e_general_error_to_xml() -> None:
    params = make_valid_gen0001e_params(general_error=True)

    gen0001e = GEN0001E.model_validate(params)
    xml = gen0001e.to_xml()

    expected_xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/GEN/GEN0001E.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>31680151250908000000001</NUOp>
        </BCMSG>
        <SISMSG>
            <GEN0001 CodErro="EGEN0050">
                <CodMsg>GEN0001E</CodMsg>
                <ISPBEmissor>31680151</ISPBEmissor>
                <ISPBDestinatario>31680151</ISPBDestinatario>
                <MsgECO>Message test GEN0001</MsgECO>
            </GEN0001>
        </SISMSG>
    </DOC>
    """

    XMLSchema('data/xsd/GEN/GEN0001E.XSD').validate(XMLResource(xml))
    assert normalize_xml(expected_xml) == normalize_xml(xml)


def test_gen0001e_tag_error_to_xml() -> None:
    params = make_valid_gen0001e_params()

    gen0001e = GEN0001E.model_validate(params)
    xml = gen0001e.to_xml()

    expected_xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/GEN/GEN0001E.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>31680151250908000000001</NUOp>
        </BCMSG>
        <SISMSG>
            <GEN0001>
                <CodMsg>GEN0001E</CodMsg>
                <ISPBEmissor CodErro="EGEN0051">31680151</ISPBEmissor>
                <ISPBDestinatario>31680151</ISPBDestinatario>
                <MsgECO>Message test GEN0001</MsgECO>
            </GEN0001>
        </SISMSG>
    </DOC>
    """

    assert normalize_xml(expected_xml) == normalize_xml(xml)


def test_gen0001_from_xml() -> None:
    xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/GEN/GEN0001.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>31680151250908000000001</NUOp>
        </BCMSG>
        <SISMSG>
            <GEN0001>
                <CodMsg>GEN0001</CodMsg>
                <ISPBEmissor>31680151</ISPBEmissor>
                <ISPBDestinatario>31680151</ISPBDestinatario>
                <MsgECO>Message test GEN0001</MsgECO>
            </GEN0001>
        </SISMSG>
    </DOC>
    """

    gen0001 = GEN0001.from_xml(xml)

    assert isinstance(gen0001, GEN0001)
    assert gen0001.issuing_ispb == '31680151'
    assert gen0001.recipient_ispb == '31680151'
    assert gen0001.message == 'Message test GEN0001'


def test_gen0001r1_from_xml() -> None:
    xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/GEN/GEN0001.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>31680151250908000000001</NUOp>
        </BCMSG>
        <SISMSG>
            <GEN0001R1>
                <CodMsg>GEN0001R1</CodMsg>
                <ISPBEmissor>31680151</ISPBEmissor>
                <ISPBDestinatario>31680151</ISPBDestinatario>
                <MsgECO>Message test GEN0001R1</MsgECO>
            </GEN0001R1>
        </SISMSG>
    </DOC>
    """

    gen0001r1 = GEN0001R1.from_xml(xml)

    assert isinstance(gen0001r1, GEN0001R1)
    assert gen0001r1.issuing_ispb == '31680151'
    assert gen0001r1.recipient_ispb == '31680151'
    assert gen0001r1.message == 'Message test GEN0001R1'


def test_gen0001e_general_error_from_xml() -> None:
    xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/GEN/GEN0001E.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>31680151250908000000001</NUOp>
        </BCMSG>
        <SISMSG>
            <GEN0001 CodErro="EGEN0050">
                <CodMsg>GEN0001E</CodMsg>
                <ISPBEmissor>31680151</ISPBEmissor>
                <ISPBDestinatario>31680151</ISPBDestinatario>
                <MsgECO>Message test GEN0001</MsgECO>
            </GEN0001>
        </SISMSG>
    </DOC>
    """

    gen0001e = GEN0001E.from_xml(xml)

    assert isinstance(gen0001e, GEN0001E)
    assert gen0001e.issuing_ispb == '31680151'
    assert gen0001e.recipient_ispb == '31680151'
    assert gen0001e.message == 'Message test GEN0001'
    assert gen0001e.general_error_code == 'EGEN0050'


def test_gen0001e_tag_error_from_xml() -> None:
    xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/GEN/GEN0001E.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>31680151250908000000001</NUOp>
        </BCMSG>
        <SISMSG>
            <GEN0001>
                <CodMsg>GEN0001E</CodMsg>
                <ISPBEmissor CodErro="EGEN0051">31680151</ISPBEmissor>
                <ISPBDestinatario>31680151</ISPBDestinatario>
                <MsgECO>Message test GEN0001</MsgECO>
            </GEN0001>
        </SISMSG>
    </DOC>
    """

    gen0001e = GEN0001E.from_xml(xml)

    assert isinstance(gen0001e, GEN0001E)
    assert gen0001e.issuing_ispb == '31680151'
    assert gen0001e.recipient_ispb == '31680151'
    assert gen0001e.message == 'Message test GEN0001'
    assert gen0001e.issuing_ispb_error_code == 'EGEN0051'


def test_gen0001_roundtrip() -> None:
    params = make_valid_gen0001_params()

    gen0001 = GEN0001.model_validate(params)
    xml = gen0001.to_xml()
    gen0001_from_xml = GEN0001.from_xml(xml)

    assert gen0001 == gen0001_from_xml


def test_gen0001r1_roundtrip() -> None:
    params = make_valid_gen0001r1_params()

    gen0001r1 = GEN0001R1.model_validate(params)
    xml = gen0001r1.to_xml()
    gen0001r1_from_xml = GEN0001R1.from_xml(xml)

    assert gen0001r1 == gen0001r1_from_xml


def test_gen0001_from_xml_missing_required_fields() -> None:
    xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/GEN/GEN0001.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>31680151250908000000001</NUOp>
        </BCMSG>
        <SISMSG>
            <GEN0001>
                <CodMsg>GEN0001</CodMsg>
                <MsgECO>Message test GEN0001</MsgECO>
            </GEN0001>
        </SISMSG>
    </DOC>
    """

    with pytest.raises(ValidationError) as exc:
        GEN0001.from_xml(xml)

    missing_fields = extract_missing_fields(exc.value)
    assert missing_fields == {'issuing_ispb', 'recipient_ispb'}


def test_gen0001r1_from_xml_missing_required_fields() -> None:
    xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/GEN/GEN0001.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>31680151250908000000001</NUOp>
        </BCMSG>
        <SISMSG>
            <GEN0001R1>
                <CodMsg>GEN0001R1</CodMsg>
                <MsgECO>Message test GEN0001R1</MsgECO>
            </GEN0001R1>
        </SISMSG>
    </DOC>
    """

    with pytest.raises(ValidationError) as exc:
        GEN0001R1.from_xml(xml)

    missing_fields = extract_missing_fields(exc.value)
    assert missing_fields == {'issuing_ispb', 'recipient_ispb'}
