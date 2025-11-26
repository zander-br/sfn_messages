from datetime import UTC, date, datetime
from typing import Any

import pytest
from pydantic import ValidationError

from sfn_messages.str.str0011 import STR0011, STR0011R1
from tests.conftest import extract_missing_fields, normalize_xml


def make_valid_str0011_params() -> dict[str, Any]:
    return {
        'from_ispb': '31680151',
        'operation_number': '316801512509080000001',
        'system_domain': 'SPB01',
        'to_ispb': '00038166',
        'institution_control_number': '31680151202509090425',
        'institution_ispb': '31680151',
        'original_str_control_number': 'STR20250101000000001',
        'settlement_date': '2025-09-08',
    }


def make_valid_str0011r1_params() -> dict[str, Any]:
    return {
        'from_ispb': '31680151',
        'operation_number': '316801512509080000001',
        'system_domain': 'SPB01',
        'to_ispb': '00038166',
        'institution_control_number': '31680151202509090425',
        'institution_ispb': '31680151',
        'vendor_timestamp': '2025-11-20T15:30:00+00:00',
        'settlement_date': '2025-09-08',
    }


def test_str0011_valid_params() -> None:
    params = make_valid_str0011_params()
    str0011 = STR0011.model_validate(params)
    assert isinstance(str0011, STR0011)
    assert str0011.from_ispb == '31680151'
    assert str0011.operation_number == '316801512509080000001'
    assert str0011.system_domain == 'SPB01'
    assert str0011.to_ispb == '00038166'
    assert str0011.institution_control_number == '31680151202509090425'
    assert str0011.institution_ispb == '31680151'
    assert str0011.original_str_control_number == 'STR20250101000000001'
    assert str0011.settlement_date == date(2025, 9, 8)


def test_str0011_missing_required_fields() -> None:
    with pytest.raises(ValidationError) as exc:
        STR0011.model_validate({})

    missing_fields = extract_missing_fields(exc.value)
    assert missing_fields == {
        'institution_ispb',
        'settlement_date',
        'operation_number',
        'from_ispb',
        'institution_control_number',
        'original_str_control_number',
        'to_ispb',
        'system_domain',
    }


def test_str0011_to_xml() -> None:
    params = make_valid_str0011_params()
    str0011 = STR0011.model_validate(params)
    xml = str0011.to_xml()

    expected_xml = """
    <DOC>
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>316801512509080000001</NUOp>
        </BCMSG>
        <SISMSG>
            <STR0011>
                <CodMsg>STR0011</CodMsg>
                <NumCtrlIF>31680151202509090425</NumCtrlIF>
                <ISPBIF>31680151</ISPBIF>
                <NumCtrlSTR>STR20250101000000001</NumCtrlSTR>
                <DtMovto>2025-09-08</DtMovto>
            </STR0011>
        </SISMSG>
    </DOC>
    """

    assert normalize_xml(expected_xml) == normalize_xml(xml)


def test_str0011_from_xml() -> None:
    xml = """
    <DOC>
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>316801512509080000001</NUOp>
        </BCMSG>
        <SISMSG>
            <STR0011>
                <CodMsg>STR0011</CodMsg>
                <NumCtrlIF>31680151202509090425</NumCtrlIF>
                <ISPBIF>31680151</ISPBIF>
                <NumCtrlSTR>STR20250101000000001</NumCtrlSTR>
                <DtMovto>2025-09-08</DtMovto>
            </STR0011>
        </SISMSG>
    </DOC>
    """

    str0011 = STR0011.from_xml(xml)
    assert isinstance(str0011, STR0011)
    assert str0011.from_ispb == '31680151'
    assert str0011.operation_number == '316801512509080000001'
    assert str0011.system_domain == 'SPB01'
    assert str0011.to_ispb == '00038166'
    assert str0011.institution_control_number == '31680151202509090425'
    assert str0011.institution_ispb == '31680151'
    assert str0011.original_str_control_number == 'STR20250101000000001'
    assert str0011.settlement_date == date(2025, 9, 8)


def test_str0011_roundtrip() -> None:
    params = make_valid_str0011_params()
    str0011 = STR0011.model_validate(params)
    xml = str0011.to_xml()
    str0011_from_xml = STR0011.from_xml(xml)
    assert str0011 == str0011_from_xml


def test_str0011_from_xml_missing_required_fields() -> None:
    xml = """
    <DOC>
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>316801512509080000001</NUOp>
        </BCMSG>
        <SISMSG>
            <STR0011>
                <CodMsg>STR0011</CodMsg>
            </STR0011>
        </SISMSG>
    </DOC>
    """

    with pytest.raises(ValidationError) as exc:
        STR0011.from_xml(xml)

    missing_fields = extract_missing_fields(exc.value)
    assert missing_fields == {
        'institution_ispb',
        'settlement_date',
        'institution_control_number',
        'original_str_control_number',
    }


def test_str0011r1_valid_params() -> None:
    params = make_valid_str0011r1_params()
    str0011r1 = STR0011R1.model_validate(params)
    assert isinstance(str0011r1, STR0011R1)
    assert str0011r1.from_ispb == '31680151'
    assert str0011r1.operation_number == '316801512509080000001'
    assert str0011r1.system_domain == 'SPB01'
    assert str0011r1.to_ispb == '00038166'
    assert str0011r1.institution_control_number == '31680151202509090425'
    assert str0011r1.institution_ispb == '31680151'
    assert str0011r1.settlement_date == date(2025, 9, 8)
    assert str0011r1.vendor_timestamp == datetime(2025, 11, 20, 15, 30, 0, tzinfo=UTC)


def test_str0011r1_missing_required_fields() -> None:
    with pytest.raises(ValidationError) as exc:
        STR0011R1.model_validate({})

    missing_fields = extract_missing_fields(exc.value)
    assert missing_fields == {
        'institution_ispb',
        'settlement_date',
        'operation_number',
        'from_ispb',
        'institution_control_number',
        'vendor_timestamp',
        'to_ispb',
        'system_domain',
    }


def test_str0011r1_to_xml() -> None:
    params = make_valid_str0011r1_params()
    str0011r1 = STR0011R1.model_validate(params)
    xml = str0011r1.to_xml()

    expected_xml = """
    <DOC>
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>316801512509080000001</NUOp>
        </BCMSG>
        <SISMSG>
            <STR0011R1>
                <CodMsg>STR0011</CodMsg>
                <NumCtrlIF>31680151202509090425</NumCtrlIF>
                <ISPBIF>31680151</ISPBIF>
                <DtHrBC>2025-11-20 15:30:00+00:00</DtHrBC>
                <DtMovto>2025-09-08</DtMovto>
            </STR0011R1>
        </SISMSG>
    </DOC>
    """

    assert normalize_xml(expected_xml) == normalize_xml(xml)


def test_str0011r1_from_xml() -> None:
    xml = """
    <DOC>
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>316801512509080000001</NUOp>
        </BCMSG>
        <SISMSG>
            <STR0011R1>
                <CodMsg>STR0011</CodMsg>
                <NumCtrlIF>31680151202509090425</NumCtrlIF>
                <ISPBIF>31680151</ISPBIF>
                <DtHrBC>2025-11-20 15:30:00+00:00</DtHrBC>
                <DtMovto>2025-09-08</DtMovto>
            </STR0011R1>
        </SISMSG>
    </DOC>
    """
    str0011r1 = STR0011R1.from_xml(xml)
    assert isinstance(str0011r1, STR0011R1)
    assert str0011r1.from_ispb == '31680151'
    assert str0011r1.operation_number == '316801512509080000001'
    assert str0011r1.system_domain == 'SPB01'
    assert str0011r1.to_ispb == '00038166'
    assert str0011r1.institution_control_number == '31680151202509090425'
    assert str0011r1.institution_ispb == '31680151'
    assert str0011r1.settlement_date == date(2025, 9, 8)
    assert str0011r1.vendor_timestamp == datetime(2025, 11, 20, 15, 30, 0, tzinfo=UTC)


def test_str0011r1_roundtrip() -> None:
    params = make_valid_str0011r1_params()
    str0011r1 = STR0011R1.model_validate(params)
    xml = str0011r1.to_xml()
    str0011r1_from_xml = STR0011R1.from_xml(xml)
    assert str0011r1 == str0011r1_from_xml


def test_str0011r1_from_xml_missing_required_fields() -> None:
    xml = """
    <DOC>
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>316801512509080000001</NUOp>
        </BCMSG>
        <SISMSG>
            <STR0011R1>
                <CodMsg>STR0011</CodMsg>
            </STR0011R1>
        </SISMSG>
    </DOC>
    """

    with pytest.raises(ValidationError) as exc:
        STR0011R1.from_xml(xml)

    missing_fields = extract_missing_fields(exc.value)
    assert missing_fields == {
        'institution_ispb',
        'settlement_date',
        'institution_control_number',
        'vendor_timestamp',
    }
