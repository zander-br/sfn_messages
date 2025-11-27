from datetime import UTC, date, datetime
from typing import Any

import pytest
from pydantic import ValidationError

from sfn_messages.gen.gen0012 import GEN0012, GEN0012R1
from sfn_messages.gen.types import TransmissionType
from tests.conftest import extract_missing_fields, normalize_xml


def make_valid_gen0012_params() -> dict[str, Any]:
    return {
        'from_ispb': '31680151',
        'to_ispb': '00038166',
        'system_domain': 'SPB01',
        'operation_number': '316801512509080000001',
        'message_code': 'GEN0012',
        'institution_control_number': '123',
        'institution_ispb': '31680151',
        'recipient_ispb': '31680151',
        'transmission_type': 'EXTERNAL',
        'institution_origin_control_number': '123',
        'original_operation_number': '316801512509080000001',
        'settlement_date': '2025-11-26',
    }


def make_valid_gen0012r1_params() -> dict[str, Any]:
    return {
        'from_ispb': '31680151',
        'to_ispb': '00038166',
        'system_domain': 'SPB01',
        'operation_number': '316801512509080000001',
        'message_code': 'GEN0012R1',
        'institution_control_number': '123',
        'institution_ispb': '31680151',
        'file_identifier': 'A' * 32,
        'participant_datetime': '2025-11-26T17:02:00+00:00',
        'settlement_date': '2025-11-26',
    }


def test_gen0012_valid_model() -> None:
    params = make_valid_gen0012_params()
    gen0012 = GEN0012.model_validate(params)

    assert isinstance(gen0012, GEN0012)
    assert gen0012.from_ispb == '31680151'
    assert gen0012.to_ispb == '00038166'
    assert gen0012.message_code == 'GEN0012'
    assert gen0012.institution_control_number == '123'
    assert gen0012.institution_ispb == '31680151'
    assert gen0012.recipient_ispb == '31680151'
    assert gen0012.transmission_type == TransmissionType.EXTERNAL
    assert gen0012.institution_origin_control_number == '123'
    assert gen0012.original_operation_number == '316801512509080000001'
    assert gen0012.settlement_date == date(2025, 11, 26)


def test_gen0012r1_valid_model() -> None:
    params = make_valid_gen0012r1_params()
    gen0012r1 = GEN0012R1.model_validate(params)

    assert isinstance(gen0012r1, GEN0012R1)
    assert gen0012r1.from_ispb == '31680151'
    assert gen0012r1.to_ispb == '00038166'
    assert gen0012r1.message_code == 'GEN0012R1'
    assert gen0012r1.institution_control_number == '123'
    assert gen0012r1.institution_ispb == '31680151'
    assert gen0012r1.file_identifier == 'A' * 32
    assert gen0012r1.participant_datetime == datetime(2025, 11, 26, 17, 2, tzinfo=UTC)
    assert gen0012r1.settlement_date == date(2025, 11, 26)


def test_gen0012_missing_required_fields() -> None:
    with pytest.raises(ValidationError) as exc:
        GEN0012.model_validate({})

    missing_fields = extract_missing_fields(exc.value)
    assert missing_fields == {
        'from_ispb',
        'to_ispb',
        'system_domain',
        'operation_number',
        'institution_control_number',
        'institution_ispb',
        'recipient_ispb',
        'transmission_type',
        'institution_origin_control_number',
        'original_operation_number',
        'settlement_date',
    }


def test_gen0012r1_missing_required_fields() -> None:
    with pytest.raises(ValidationError) as exc:
        GEN0012R1.model_validate({})

    missing_fields = extract_missing_fields(exc.value)
    assert missing_fields == {
        'from_ispb',
        'to_ispb',
        'system_domain',
        'operation_number',
        'institution_control_number',
        'institution_ispb',
        'file_identifier',
        'participant_datetime',
        'settlement_date',
    }


def test_gen0012_to_xml() -> None:
    params = make_valid_gen0012_params()
    gen0012 = GEN0012.model_validate(params)

    xml = gen0012.to_xml()

    expected_xml = """<?xml version="1.0"?>
    <DOC>
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>316801512509080000001</NUOp>
        </BCMSG>
        <SISMSG>
            <GEN0012>
                <CodMsg>GEN0012</CodMsg>
                <NumCtrlIF>123</NumCtrlIF>
                <ISPBIF>31680151</ISPBIF>
                <ISPBDestinatario>31680151</ISPBDestinatario>
                <TpTransm>E</TpTransm>
                <NumCtrlSistOr>123</NumCtrlSistOr>
                <NUOpOr>316801512509080000001</NUOpOr>
                <DtMovto>2025-11-26</DtMovto>
            </GEN0012>
        </SISMSG>
    </DOC>
    """
    assert normalize_xml(expected_xml) == normalize_xml(xml)


def test_gen0012r1_to_xml() -> None:
    params = make_valid_gen0012r1_params()
    gen0012r1 = GEN0012R1.model_validate(params)

    xml = gen0012r1.to_xml()

    expected_xml = """<?xml version="1.0"?>
    <DOC>
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>316801512509080000001</NUOp>
        </BCMSG>
        <SISMSG>
            <GEN0012R1>
                <CodMsg>GEN0012R1</CodMsg>
                <NumCtrlIF>123</NumCtrlIF>
                <ISPBIF>31680151</ISPBIF>
                <IdentdArq>AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA</IdentdArq>
                <DtHrPart>2025-11-26 17:02:00+00:00</DtHrPart>
                <DtMovto>2025-11-26</DtMovto>
            </GEN0012R1>
        </SISMSG>
    </DOC>
    """
    assert normalize_xml(expected_xml) == normalize_xml(xml)


def test_gen0012_from_xml() -> None:
    xml = """<?xml version="1.0"?>
    <DOC>
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>316801512509080000001</NUOp>
        </BCMSG>
        <SISMSG>
            <GEN0012>
                <CodMsg>GEN0012</CodMsg>
                <NumCtrlIF>123</NumCtrlIF>
                <ISPBIF>31680151</ISPBIF>
                <ISPBDestinatario>31680151</ISPBDestinatario>
                <TpTransm>E</TpTransm>
                <NumCtrlSistOr>123</NumCtrlSistOr>
                <NUOpOr>316801512509080000001</NUOpOr>
                <DtMovto>2025-11-26</DtMovto>
            </GEN0012>
        </SISMSG>
    </DOC>
    """

    gen0012 = GEN0012.from_xml(xml)

    assert isinstance(gen0012, GEN0012)
    assert gen0012.from_ispb == '31680151'
    assert gen0012.to_ispb == '00038166'
    assert gen0012.message_code == 'GEN0012'
    assert gen0012.institution_control_number == '123'
    assert gen0012.institution_ispb == '31680151'
    assert gen0012.recipient_ispb == '31680151'
    assert gen0012.transmission_type == TransmissionType.EXTERNAL
    assert gen0012.institution_origin_control_number == '123'
    assert gen0012.original_operation_number == '316801512509080000001'
    assert gen0012.settlement_date == date(2025, 11, 26)


def test_gen0012r1_from_xml() -> None:
    xml = """<?xml version="1.0"?>
    <DOC>
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>316801512509080000001</NUOp>
        </BCMSG>
        <SISMSG>
            <GEN0012R1>
                <CodMsg>GEN0012R1</CodMsg>
                <NumCtrlIF>123</NumCtrlIF>
                <ISPBIF>31680151</ISPBIF>
                <IdentdArq>AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA</IdentdArq>
                <DtHrPart>2025-11-26 17:02:00+00:00</DtHrPart>
                <DtMovto>2025-11-26</DtMovto>
            </GEN0012R1>
        </SISMSG>
    </DOC>
    """

    gen0012r1 = GEN0012R1.from_xml(xml)

    assert isinstance(gen0012r1, GEN0012R1)
    assert gen0012r1.from_ispb == '31680151'
    assert gen0012r1.to_ispb == '00038166'
    assert gen0012r1.message_code == 'GEN0012R1'
    assert gen0012r1.institution_control_number == '123'
    assert gen0012r1.institution_ispb == '31680151'
    assert gen0012r1.file_identifier == 'A' * 32
    assert gen0012r1.participant_datetime == datetime(2025, 11, 26, 17, 2, tzinfo=UTC)
    assert gen0012r1.settlement_date == date(2025, 11, 26)


def test_gen0012_roundtrip() -> None:
    params = make_valid_gen0012_params()

    gen0012 = GEN0012.model_validate(params)
    xml = gen0012.to_xml()
    gen0012_from_xml = GEN0012.from_xml(xml)

    assert gen0012 == gen0012_from_xml


def test_gen0012r1_roundtrip() -> None:
    params = make_valid_gen0012r1_params()

    gen0012r1 = GEN0012R1.model_validate(params)
    xml = gen0012r1.to_xml()
    gen0012r1_from_xml = GEN0012R1.from_xml(xml)

    assert gen0012r1 == gen0012r1_from_xml


def test_gen0012_from_xml_missing_required_fields() -> None:
    xml = """<?xml version="1.0"?>
    <DOC>
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>316801512509080000001</NUOp>
        </BCMSG>
        <SISMSG>
            <GEN0012>
                <CodMsg>GEN0012</CodMsg>
            </GEN0012>
        </SISMSG>
    </DOC>
    """

    with pytest.raises(ValidationError) as exc:
        GEN0012.from_xml(xml)

    missing_fields = extract_missing_fields(exc.value)
    assert missing_fields == {
        'institution_control_number',
        'institution_ispb',
        'recipient_ispb',
        'transmission_type',
        'institution_origin_control_number',
        'original_operation_number',
        'settlement_date',
    }


def test_gen0012r1_from_xml_missing_required_fields() -> None:
    xml = """<?xml version="1.0"?>
    <DOC>
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>316801512509080000001</NUOp>
        </BCMSG>
        <SISMSG>
            <GEN0012R1>
                <CodMsg>GEN0012R1</CodMsg>
            </GEN0012R1>
        </SISMSG>
    </DOC>
    """

    with pytest.raises(ValidationError) as exc:
        GEN0012R1.from_xml(xml)

    missing_fields = extract_missing_fields(exc.value)
    assert missing_fields == {
        'institution_control_number',
        'institution_ispb',
        'file_identifier',
        'participant_datetime',
        'settlement_date',
    }
