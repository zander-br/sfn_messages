from datetime import datetime
from typing import Any

import pytest
from pydantic import ValidationError

from sfn_messages.gen.gen0004 import GEN0004
from tests.conftest import extract_missing_fields, normalize_xml


def make_valid_gen0004_params() -> dict[str, Any]:
    return {
        'from_ispb': '31680151',
        'to_ispb': '00038166',
        'system_domain': 'SPB01',
        'operation_number': '31680151250908000000001',
        'message_code': 'GEN0004',
        'generic_error': 'EGEN0050',
        'issuing_ispb': '31680151',
        'recipient_ispb': '00038166',
        'mq_number': '0123456789ABCDEF000000000123456789ABCDEF00000000',
        'unique_operation_number': '31680151250908000000001',
        'original_protocol_sta_number': '123456789012345678',
        'description': 'Generic error description',
        'participant_datetime': '2026-01-12T10:30:00',
    }


def test_gen0004_valid_model() -> None:
    params = make_valid_gen0004_params()
    gen0004 = GEN0004.model_validate(params)

    assert isinstance(gen0004, GEN0004)
    assert gen0004.message_code == 'GEN0004'
    assert gen0004.generic_error == 'EGEN0050'
    assert gen0004.issuing_ispb == '31680151'
    assert gen0004.recipient_ispb == '00038166'
    assert gen0004.mq_number == '0123456789ABCDEF000000000123456789ABCDEF00000000'
    assert gen0004.unique_operation_number == '31680151250908000000001'
    assert gen0004.original_protocol_sta_number == '123456789012345678'
    assert gen0004.description == 'Generic error description'
    assert gen0004.participant_datetime == datetime(2026, 1, 12, 10, 30)


def test_gen0004_missing_required_fields() -> None:
    with pytest.raises(ValidationError) as exc:
        GEN0004.model_validate({})

    missing_fields = extract_missing_fields(exc.value)
    assert missing_fields == {
        'from_ispb',
        'to_ispb',
        'system_domain',
        'operation_number',
        'generic_error',
        'issuing_ispb',
        'recipient_ispb',
        'participant_datetime',
    }


def test_gen0004_to_xml() -> None:
    params = make_valid_gen0004_params()

    gen0004 = GEN0004.model_validate(params)
    xml = gen0004.to_xml()

    expected_xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/GEN/GEN0004.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>31680151250908000000001</NUOp>
        </BCMSG>
        <SISMSG>
            <GEN0004>
                <CodMsg>GEN0004</CodMsg>
                <ErroGEN>EGEN0050</ErroGEN>
                <ISPBEmissor>31680151</ISPBEmissor>
                <ISPBDestinatario>00038166</ISPBDestinatario>
                <NumMQ>0123456789ABCDEF000000000123456789ABCDEF00000000</NumMQ>
                <NUOpOr>31680151250908000000001</NUOpOr>
                <NumProtSTAOr>123456789012345678</NumProtSTAOr>
                <Hist>Generic error description</Hist>
                <DtHrPart>2026-01-12T10:30:00</DtHrPart>
            </GEN0004>
        </SISMSG>
    </DOC>
    """

    assert normalize_xml(expected_xml) == normalize_xml(xml)


def test_gen0004_from_xml() -> None:
    xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/GEN/GEN0004.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>31680151250908000000001</NUOp>
        </BCMSG>
        <SISMSG>
            <GEN0004>
                <CodMsg>GEN0004</CodMsg>
                <ErroGEN>EGEN0050</ErroGEN>
                <ISPBEmissor>31680151</ISPBEmissor>
                <ISPBDestinatario>00038166</ISPBDestinatario>
                <NumMQ>0123456789ABCDEF000000000123456789ABCDEF00000000</NumMQ>
                <NUOpOr>31680151250908000000001</NUOpOr>
                <NumProtSTAOr>123456789012345678</NumProtSTAOr>
                <Hist>Generic error description</Hist>
                <DtHrPart>2026-01-12T10:30:00</DtHrPart>
            </GEN0004>
        </SISMSG>
    </DOC>
    """

    gen0004 = GEN0004.from_xml(xml)

    assert isinstance(gen0004, GEN0004)
    assert gen0004.message_code == 'GEN0004'
    assert gen0004.generic_error == 'EGEN0050'
    assert gen0004.issuing_ispb == '31680151'
    assert gen0004.recipient_ispb == '00038166'
    assert gen0004.mq_number == '0123456789ABCDEF000000000123456789ABCDEF00000000'
    assert gen0004.unique_operation_number == '31680151250908000000001'
    assert gen0004.original_protocol_sta_number == '123456789012345678'
    assert gen0004.description == 'Generic error description'
    assert gen0004.participant_datetime == datetime(2026, 1, 12, 10, 30)


def test_gen0004_roundtrip() -> None:
    params = make_valid_gen0004_params()

    gen0004 = GEN0004.model_validate(params)
    xml = gen0004.to_xml()
    gen0004_from_xml = GEN0004.from_xml(xml)

    assert gen0004 == gen0004_from_xml


def test_gen0004_from_xml_missing_required_fields() -> None:
    xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/GEN/GEN0004.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>31680151250908000000001</NUOp>
        </BCMSG>
        <SISMSG>
            <GEN0004>
                <CodMsg>GEN0004</CodMsg>
            </GEN0004>
        </SISMSG>
    </DOC>
    """

    with pytest.raises(ValidationError) as exc:
        GEN0004.from_xml(xml)

    missing_fields = extract_missing_fields(exc.value)
    assert missing_fields == {'generic_error', 'issuing_ispb', 'recipient_ispb', 'participant_datetime'}
