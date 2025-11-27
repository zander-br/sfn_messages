from datetime import date
from typing import Any

import pytest
from pydantic import ValidationError

from sfn_messages.str.str0013 import STR013
from tests.conftest import extract_missing_fields, normalize_xml


def make_valid_str0013_params() -> dict[str, Any]:
    return {
        'from_ispb': '31680151',
        'operation_number': '316801512509080000001',
        'system_domain': 'SPB01',
        'to_ispb': '00038166',
        'institution_control_number': '31680151202509090425',
        'institution_ispb': '31680151',
        'settlement_date': date(2025, 11, 27),
    }


def test_str0013_model_valid() -> None:
    params = make_valid_str0013_params()
    message = STR013.model_validate(params)
    assert isinstance(message, STR013)
    assert message.from_ispb == '31680151'
    assert message.institution_control_number == '31680151202509090425'
    assert message.settlement_date == date(2025, 11, 27)
    assert message.message_code == 'STR0013'
    assert message.institution_ispb == '31680151'
    assert message.operation_number == '316801512509080000001'
    assert message.system_domain == 'SPB01'
    assert message.to_ispb == '00038166'


def test_str0013_missing_required_fields() -> None:
    with pytest.raises(ValidationError) as exc:
        STR013.model_validate({})
    missing_fields = extract_missing_fields(exc.value)
    assert missing_fields == {
        'settlement_date',
        'system_domain',
        'institution_ispb',
        'operation_number',
        'institution_control_number',
        'from_ispb',
        'to_ispb',
    }


def test_str0013_to_xml() -> None:
    params = make_valid_str0013_params()
    str0013 = STR013.model_validate(params)
    xml = str0013.to_xml()

    expected_xml = """<?xml version="1.0"?>
    <DOC>
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>316801512509080000001</NUOp>
        </BCMSG>
        <SISMSG>
            <STR0013>
                <CodMsg>STR0013</CodMsg>
                <NumCtrlIF_LDL>31680151202509090425</NumCtrlIF_LDL>
                <ISPBIF_LDL>31680151</ISPBIF_LDL>
                <DtMovto>2025-11-27</DtMovto>
            </STR0013>
        </SISMSG>
    </DOC>
    """

    assert normalize_xml(expected_xml) == normalize_xml(xml)


def test_str0013_from_xml() -> None:
    xml = """<?xml version="1.0"?>
    <DOC>
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>316801512509080000001</NUOp>
        </BCMSG>
        <SISMSG>
            <STR0013>
                <CodMsg>STR0013</CodMsg>
                <NumCtrlIF_LDL>31680151202509090425</NumCtrlIF_LDL>
                <ISPBIF_LDL>31680151</ISPBIF_LDL>
                <DtMovto>2025-11-27</DtMovto>
            </STR0013>
        </SISMSG>
    </DOC>
    """

    str0013 = STR013.from_xml(xml)

    assert isinstance(str0013, STR013)
    assert str0013.message_code == 'STR0013'
    assert str0013.institution_control_number == '31680151202509090425'
    assert str0013.institution_ispb == '31680151'
    assert str0013.settlement_date == date(2025, 11, 27)
    assert str0013.from_ispb == '31680151'
    assert str0013.to_ispb == '00038166'
    assert str0013.system_domain == 'SPB01'
    assert str0013.operation_number == '316801512509080000001'


def test_str0013_roundtrip() -> None:
    params = make_valid_str0013_params()
    str0013 = STR013.model_validate(params)
    xml = str0013.to_xml()
    str0013_from_xml = STR013.from_xml(xml)
    assert str0013 == str0013_from_xml


def test_str0013_from_xml_missing_required_fields() -> None:
    xml = """<?xml version="1.0"?>
    <DOC>
        <SISMSG>
            <STR0013>
                <CodMsg>STR0013</CodMsg>
            </STR0013>
        </SISMSG>
    </DOC>
    """

    with pytest.raises(ValidationError) as exc:
        STR013.from_xml(xml)
    missing_fields = extract_missing_fields(exc.value)
    assert missing_fields == {
        'system_domain',
        'to_ispb',
        'operation_number',
        'institution_control_number',
        'settlement_date',
        'from_ispb',
        'institution_ispb',
    }
