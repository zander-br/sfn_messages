from datetime import date
from typing import Any

import pytest
from pydantic import ValidationError

from sfn_messages.gen.gen0020 import GEN0020
from tests.conftest import extract_missing_fields, normalize_xml


def make_valid_gen0020_params() -> dict[str, Any]:
    return {
        'from_ispb': '31680151',
        'to_ispb': '00038166',
        'system_domain': 'SPB01',
        'operation_number': '316801512509080000001',
        'message_code': 'GEN0020',
        'participant_institution_control_number': '123',
        'participant_ispb': '31680151',
        'parcitipant_consulted_ispb': '00038166',
        'settlement_date': '2025-11-27',
    }


def test_gen0020_valid_model() -> None:
    params = make_valid_gen0020_params()
    gen0020 = GEN0020.model_validate(params)

    assert isinstance(gen0020, GEN0020)
    assert gen0020.from_ispb == '31680151'
    assert gen0020.to_ispb == '00038166'
    assert gen0020.system_domain == 'SPB01'
    assert gen0020.operation_number == '316801512509080000001'
    assert gen0020.message_code == 'GEN0020'
    assert gen0020.participant_institution_control_number == '123'
    assert gen0020.participant_ispb == '31680151'
    assert gen0020.parcitipant_consulted_ispb == '00038166'
    assert gen0020.settlement_date == date(2025, 11, 27)


def test_gen0020_missing_required_fields() -> None:
    with pytest.raises(ValidationError) as exc:
        GEN0020.model_validate({})

    missing_fields = extract_missing_fields(exc.value)
    assert missing_fields == {
        'from_ispb',
        'to_ispb',
        'system_domain',
        'operation_number',
        'participant_institution_control_number',
        'participant_ispb',
        'parcitipant_consulted_ispb',
        'settlement_date',
    }


def test_gen0020_to_xml() -> None:
    params = make_valid_gen0020_params()
    gen0020 = GEN0020.model_validate(params)

    xml = gen0020.to_xml()

    expected_xml = """<?xml version="1.0"?>
    <DOC>
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>316801512509080000001</NUOp>
        </BCMSG>
        <SISMSG>
            <GEN0020>
                <CodMsg>GEN0020</CodMsg>
                <NumCtrlPart>123</NumCtrlPart>
                <ISPBPart>31680151</ISPBPart>
                <ISPBPartConsd>00038166</ISPBPartConsd>
                <DtMovto>2025-11-27</DtMovto>
            </GEN0020>
        </SISMSG>
    </DOC>
    """
    assert normalize_xml(expected_xml) == normalize_xml(xml)


def test_gen0020_from_xml() -> None:
    xml = """<?xml version="1.0"?>
    <DOC>
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>316801512509080000001</NUOp>
        </BCMSG>
        <SISMSG>
            <GEN0020>
                <CodMsg>GEN0020</CodMsg>
                <NumCtrlPart>123</NumCtrlPart>
                <ISPBPart>31680151</ISPBPart>
                <ISPBPartConsd>00038166</ISPBPartConsd>
                <DtMovto>2025-11-27</DtMovto>
            </GEN0020>
        </SISMSG>
    </DOC>
    """

    gen0020 = GEN0020.from_xml(xml)

    assert isinstance(gen0020, GEN0020)
    assert gen0020.from_ispb == '31680151'
    assert gen0020.to_ispb == '00038166'
    assert gen0020.system_domain == 'SPB01'
    assert gen0020.operation_number == '316801512509080000001'
    assert gen0020.message_code == 'GEN0020'
    assert gen0020.participant_institution_control_number == '123'
    assert gen0020.participant_ispb == '31680151'
    assert gen0020.parcitipant_consulted_ispb == '00038166'
    assert gen0020.settlement_date == date(2025, 11, 27)


def test_gen0020_roundtrip() -> None:
    params = make_valid_gen0020_params()

    gen0020 = GEN0020.model_validate(params)
    xml = gen0020.to_xml()
    gen0020_from_xml = GEN0020.from_xml(xml)

    assert gen0020 == gen0020_from_xml


def test_gen0020_from_xml_missing_required_fields() -> None:
    xml = """<?xml version="1.0"?>
    <DOC>
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>316801512509080000001</NUOp>
        </BCMSG>
        <SISMSG>
            <GEN0020>
                <CodMsg>GEN0020</CodMsg>
            </GEN0020>
        </SISMSG>
    </DOC>
    """

    with pytest.raises(ValidationError) as exc:
        GEN0020.from_xml(xml)

    missing_fields = extract_missing_fields(exc.value)
    assert missing_fields == {
        'participant_institution_control_number',
        'participant_ispb',
        'parcitipant_consulted_ispb',
        'settlement_date',
    }
