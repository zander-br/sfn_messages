from datetime import UTC, datetime
from typing import Any

import pytest
from pydantic import ValidationError

from sfn_messages.gen.gen0003 import GEN0003, GEN0003E, GEN0003R1
from tests.conftest import extract_missing_fields, normalize_xml


def make_valid_gen0003_params() -> dict[str, Any]:
    return {
        'from_ispb': '31680151',
        'to_ispb': '00038166',
        'system_domain': 'SPB01',
        'operation_number': '31680151250908000000001',
        'message_code': 'GEN0003',
        'institution_control_number': '123',
        'issuing_ispb': '31680151',
        'recipient_ispb': '31680151',
    }


def make_valid_gen0003r1_params() -> dict[str, Any]:
    return {
        'from_ispb': '31680151',
        'to_ispb': '00038166',
        'system_domain': 'SPB01',
        'operation_number': '31680151250908000000001',
        'message_code': 'GEN0003R1',
        'institution_control_number': '123',
        'issuing_ispb': '31680151',
        'recipient_ispb': '31680151',
        'last_number_operation': '00316801512509080000001',
        'last_message_datetime': '2025-11-25T17:02:00+00:00',
        'participant_datetime': '2025-11-25T17:02:00+00:00',
    }


def make_valid_gen0003e_params(*, general_error: bool = False) -> dict[str, Any]:
    gen0003e = {
        'from_ispb': '31680151',
        'to_ispb': '00038166',
        'system_domain': 'SPB01',
        'operation_number': '31680151250908000000001',
        'message_code': 'GEN0003',
        'institution_control_number': '123',
        'issuing_ispb': '31680151',
        'recipient_ispb': '31680151',
    }

    if general_error:
        gen0003e['general_error_code'] = 'EGEN0050'
    else:
        gen0003e['issuing_ispb_error_code'] = 'EGEN0051'

    return gen0003e


def test_gen0003_valid_model() -> None:
    params = make_valid_gen0003_params()
    gen0003 = GEN0003.model_validate(params)

    assert isinstance(gen0003, GEN0003)
    assert gen0003.message_code == 'GEN0003'
    assert gen0003.institution_control_number == '123'
    assert gen0003.issuing_ispb == '31680151'
    assert gen0003.recipient_ispb == '31680151'


def test_gen0003r1_valid_model() -> None:
    params = make_valid_gen0003r1_params()
    gen0003r1 = GEN0003R1.model_validate(params)

    assert isinstance(gen0003r1, GEN0003R1)
    assert gen0003r1.institution_control_number == '123'
    assert gen0003r1.last_message_datetime == datetime(2025, 11, 25, 17, 2, tzinfo=UTC)
    assert gen0003r1.participant_datetime == datetime(2025, 11, 25, 17, 2, tzinfo=UTC)
    assert gen0003r1.last_number_operation == '00316801512509080000001'
    assert gen0003r1.issuing_ispb == '31680151'
    assert gen0003r1.recipient_ispb == '31680151'


def test_gen0003e_general_error_valid_model() -> None:
    params = make_valid_gen0003e_params(general_error=True)
    gen0003e = GEN0003E.model_validate(params)

    assert isinstance(gen0003e, GEN0003E)
    assert gen0003e.message_code == 'GEN0003'
    assert gen0003e.institution_control_number == '123'
    assert gen0003e.issuing_ispb == '31680151'
    assert gen0003e.recipient_ispb == '31680151'
    assert gen0003e.general_error_code == 'EGEN0050'


def test_gen0003e_tag_error_valid_model() -> None:
    params = make_valid_gen0003e_params()
    gen0003e = GEN0003E.model_validate(params)

    assert isinstance(gen0003e, GEN0003E)
    assert gen0003e.message_code == 'GEN0003'
    assert gen0003e.institution_control_number == '123'
    assert gen0003e.issuing_ispb == '31680151'
    assert gen0003e.recipient_ispb == '31680151'
    assert gen0003e.issuing_ispb_error_code == 'EGEN0051'


def test_gen0003_missing_required_fields() -> None:
    with pytest.raises(ValidationError) as exc:
        GEN0003.model_validate({})

    missing_fields = extract_missing_fields(exc.value)
    assert missing_fields == {
        'from_ispb',
        'to_ispb',
        'system_domain',
        'operation_number',
        'institution_control_number',
        'issuing_ispb',
        'recipient_ispb',
    }


def test_gen0003r1_missing_required_fields() -> None:
    with pytest.raises(ValidationError) as exc:
        GEN0003R1.model_validate({})

    missing_fields = extract_missing_fields(exc.value)
    assert missing_fields == {
        'from_ispb',
        'to_ispb',
        'system_domain',
        'operation_number',
        'institution_control_number',
        'issuing_ispb',
        'recipient_ispb',
        'last_number_operation',
        'last_message_datetime',
        'participant_datetime',
    }


def test_gen0003_to_xml() -> None:
    params = make_valid_gen0003_params()

    gen0003 = GEN0003.model_validate(params)
    xml = gen0003.to_xml()

    expected_xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/GEN/GEN0003.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>31680151250908000000001</NUOp>
        </BCMSG>
        <SISMSG>
            <GEN0003>
                <CodMsg>GEN0003</CodMsg>
                <NumCtrlIF>123</NumCtrlIF>
                <ISPBEmissor>31680151</ISPBEmissor>
                <ISPBDestinatario>31680151</ISPBDestinatario>
            </GEN0003>
        </SISMSG>
    </DOC>
    """

    assert normalize_xml(expected_xml) == normalize_xml(xml)


def test_gen0003r1_to_xml() -> None:
    params = make_valid_gen0003r1_params()

    gen0003r1 = GEN0003R1.model_validate(params)
    xml = gen0003r1.to_xml()

    expected_xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/GEN/GEN0003.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>31680151250908000000001</NUOp>
        </BCMSG>
        <SISMSG>
            <GEN0003R1>
                <CodMsg>GEN0003R1</CodMsg>
                <NumCtrlIF>123</NumCtrlIF>
                <ISPBEmissor>31680151</ISPBEmissor>
                <ISPBDestinatario>31680151</ISPBDestinatario>
                <NumUltOp>00316801512509080000001</NumUltOp>
                <DtHrUltMsg>2025-11-25 17:02:00+00:00</DtHrUltMsg>
                <DtHrPart>2025-11-25 17:02:00+00:00</DtHrPart>
            </GEN0003R1>
        </SISMSG>
    </DOC>
    """

    assert normalize_xml(expected_xml) == normalize_xml(xml)


def test_gen0003e_general_error_to_xml() -> None:
    params = make_valid_gen0003e_params(general_error=True)

    gen0003e = GEN0003E.model_validate(params)
    xml = gen0003e.to_xml()

    expected_xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/GEN/GEN0003E.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>31680151250908000000001</NUOp>
        </BCMSG>
        <SISMSG>
            <GEN0003E CodErro="EGEN0050">
                <CodMsg>GEN0003</CodMsg>
                <NumCtrlIF>123</NumCtrlIF>
                <ISPBEmissor>31680151</ISPBEmissor>
                <ISPBDestinatario>31680151</ISPBDestinatario>
            </GEN0003E>
        </SISMSG>
    </DOC>
    """

    assert normalize_xml(expected_xml) == normalize_xml(xml)


def test_gen0003e_tag_error_to_xml() -> None:
    params = make_valid_gen0003e_params()

    gen0003e = GEN0003E.model_validate(params)
    xml = gen0003e.to_xml()

    expected_xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/GEN/GEN0003E.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>31680151250908000000001</NUOp>
        </BCMSG>
        <SISMSG>
            <GEN0003E>
                <CodMsg>GEN0003</CodMsg>
                <NumCtrlIF>123</NumCtrlIF>
                <ISPBEmissor CodErro="EGEN0051">31680151</ISPBEmissor>
                <ISPBDestinatario>31680151</ISPBDestinatario>
            </GEN0003E>
        </SISMSG>
    </DOC>
    """

    assert normalize_xml(expected_xml) == normalize_xml(xml)


def test_gen0003_from_xml() -> None:
    xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/GEN/GEN0003.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>31680151250908000000001</NUOp>
        </BCMSG>
        <SISMSG>
            <GEN0003>
                <CodMsg>GEN0003</CodMsg>
                <NumCtrlIF>123</NumCtrlIF>
                <ISPBEmissor>31680151</ISPBEmissor>
                <ISPBDestinatario>31680151</ISPBDestinatario>
            </GEN0003>
        </SISMSG>
    </DOC>
    """

    gen0003 = GEN0003.from_xml(xml)

    assert isinstance(gen0003, GEN0003)
    assert gen0003.issuing_ispb == '31680151'
    assert gen0003.recipient_ispb == '31680151'
    assert gen0003.institution_control_number == '123'


def test_gen0003r1_from_xml() -> None:
    xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/GEN/GEN0003.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>31680151250908000000001</NUOp>
        </BCMSG>
        <SISMSG>
            <GEN0003R1>
                <CodMsg>GEN0003R1</CodMsg>
                <NumCtrlIF>123</NumCtrlIF>
                <ISPBEmissor>31680151</ISPBEmissor>
                <ISPBDestinatario>31680151</ISPBDestinatario>
                <NumUltOp>00316801512509080000001</NumUltOp>
                <DtHrUltMsg>2025-11-25 17:02:00+00:00</DtHrUltMsg>
                <DtHrPart>2025-11-25 17:02:00+00:00</DtHrPart>
            </GEN0003R1>
        </SISMSG>
    </DOC>
    """

    gen0003r1 = GEN0003R1.from_xml(xml)

    assert isinstance(gen0003r1, GEN0003R1)
    assert gen0003r1.institution_control_number == '123'
    assert gen0003r1.last_message_datetime == datetime(2025, 11, 25, 17, 2, tzinfo=UTC)
    assert gen0003r1.participant_datetime == datetime(2025, 11, 25, 17, 2, tzinfo=UTC)
    assert gen0003r1.last_number_operation == '00316801512509080000001'
    assert gen0003r1.issuing_ispb == '31680151'
    assert gen0003r1.recipient_ispb == '31680151'


def test_gen0003e_general_error_from_xml() -> None:
    xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/GEN/GEN0003E.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>31680151250908000000001</NUOp>
        </BCMSG>
        <SISMSG>
            <GEN0003E CodErro="EGEN0050">
                <CodMsg>GEN0003</CodMsg>
                <NumCtrlIF>123</NumCtrlIF>
                <ISPBEmissor>31680151</ISPBEmissor>
                <ISPBDestinatario>31680151</ISPBDestinatario>
            </GEN0003E>
        </SISMSG>
    </DOC>
    """

    gen0003e = GEN0003E.from_xml(xml)

    assert isinstance(gen0003e, GEN0003E)
    assert gen0003e.issuing_ispb == '31680151'
    assert gen0003e.recipient_ispb == '31680151'
    assert gen0003e.institution_control_number == '123'
    assert gen0003e.general_error_code == 'EGEN0050'


def test_gen0003e_tag_error_from_xml() -> None:
    xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/GEN/GEN0003E.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>31680151250908000000001</NUOp>
        </BCMSG>
        <SISMSG>
            <GEN0003E>
                <CodMsg>GEN0003</CodMsg>
                <NumCtrlIF>123</NumCtrlIF>
                <ISPBEmissor CodErro="EGEN0051">31680151</ISPBEmissor>
                <ISPBDestinatario>31680151</ISPBDestinatario>
            </GEN0003E>
        </SISMSG>
    </DOC>
    """

    gen0003e = GEN0003E.from_xml(xml)

    assert isinstance(gen0003e, GEN0003E)
    assert gen0003e.issuing_ispb == '31680151'
    assert gen0003e.recipient_ispb == '31680151'
    assert gen0003e.institution_control_number == '123'
    assert gen0003e.issuing_ispb_error_code == 'EGEN0051'


def test_gen0003_roundtrip() -> None:
    params = make_valid_gen0003_params()

    gen0003 = GEN0003.model_validate(params)
    xml = gen0003.to_xml()
    gen0003_from_xml = GEN0003.from_xml(xml)

    assert gen0003 == gen0003_from_xml


def test_gen0003r1_roundtrip() -> None:
    params = make_valid_gen0003r1_params()

    gen0003r1 = GEN0003R1.model_validate(params)
    xml = gen0003r1.to_xml()
    gen0003r1_from_xml = GEN0003R1.from_xml(xml)

    assert gen0003r1 == gen0003r1_from_xml


def test_gen0003_from_xml_missing_required_fields() -> None:
    xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/GEN/GEN0003.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>31680151250908000000001</NUOp>
        </BCMSG>
        <SISMSG>
            <GEN0003>
                <CodMsg>GEN0003</CodMsg>
            </GEN0003>
        </SISMSG>
    </DOC>
    """

    with pytest.raises(ValidationError) as exc:
        GEN0003.from_xml(xml)

    missing_fields = extract_missing_fields(exc.value)
    assert missing_fields == {'issuing_ispb', 'recipient_ispb', 'institution_control_number'}


def test_gen0003r1_from_xml_missing_required_fields() -> None:
    xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/GEN/GEN0003.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>31680151250908000000001</NUOp>
        </BCMSG>
        <SISMSG>
            <GEN0003R1>
                <CodMsg>GEN0003R1</CodMsg>
            </GEN0003R1>
        </SISMSG>
    </DOC>
    """

    with pytest.raises(ValidationError) as exc:
        GEN0003R1.from_xml(xml)

    missing_fields = extract_missing_fields(exc.value)
    assert missing_fields == {
        'issuing_ispb',
        'recipient_ispb',
        'institution_control_number',
        'last_number_operation',
        'last_message_datetime',
        'participant_datetime',
    }
