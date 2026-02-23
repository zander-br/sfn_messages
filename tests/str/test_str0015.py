from datetime import date, datetime
from typing import Any

import pytest
from pydantic import ValidationError

from sfn_messages.str.str0015 import STR0015, STR0015E
from tests.conftest import extract_missing_fields, normalize_xml


def make_valid_str0015_params() -> dict[str, Any]:
    return {
        'from_ispb': '31680151',
        'operation_number': '31680151250908000000001',
        'system_domain': 'SPB01',
        'to_ispb': '00038166',
        'institution_ispb': '31680151',
        'closing_timestamp': '2026-02-23T18:30:00',
        'vendor_timestamp': '2026-02-23T18:31:00',
        'settlement_date': '2026-02-23',
    }


def make_valid_str0015e_params(*, general_error: bool = False) -> dict[str, Any]:
    str0015e = {
        'from_ispb': '31680151',
        'operation_number': '31680151250908000000001',
        'system_domain': 'SPB01',
        'to_ispb': '00038166',
        'institution_ispb': '31680151',
        'closing_timestamp': '2026-02-23T18:30:00',
        'vendor_timestamp': '2026-02-23T18:31:00',
        'settlement_date': '2026-02-23',
    }

    if general_error:
        str0015e['general_error_code'] = 'EGEN0050'
    else:
        str0015e['closing_timestamp_error_code'] = 'EGEN0023'

    return str0015e


def test_str0015_model_valid() -> None:
    params = make_valid_str0015_params()
    message = STR0015.model_validate(params)
    assert isinstance(message, STR0015)
    assert message.from_ispb == '31680151'
    assert message.settlement_date == date(2026, 2, 23)
    assert message.closing_timestamp == datetime(2026, 2, 23, 18, 30)
    assert message.vendor_timestamp == datetime(2026, 2, 23, 18, 31)
    assert message.message_code == 'STR0015'
    assert message.operation_number == '31680151250908000000001'
    assert message.system_domain == 'SPB01'
    assert message.to_ispb == '00038166'


def test_str0015e_general_error_model_valid() -> None:
    params = make_valid_str0015e_params(general_error=True)
    message = STR0015E.model_validate(params)
    assert isinstance(message, STR0015E)
    assert message.from_ispb == '31680151'
    assert message.settlement_date == date(2026, 2, 23)
    assert message.closing_timestamp == datetime(2026, 2, 23, 18, 30)
    assert message.vendor_timestamp == datetime(2026, 2, 23, 18, 31)
    assert message.message_code == 'STR0015E'
    assert message.operation_number == '31680151250908000000001'
    assert message.system_domain == 'SPB01'
    assert message.to_ispb == '00038166'
    assert message.general_error_code == 'EGEN0050'


def test_str0015e_tag_error_model_valid() -> None:
    params = make_valid_str0015e_params()
    message = STR0015E.model_validate(params)
    assert isinstance(message, STR0015E)
    assert message.from_ispb == '31680151'
    assert message.settlement_date == date(2026, 2, 23)
    assert message.closing_timestamp == datetime(2026, 2, 23, 18, 30)
    assert message.vendor_timestamp == datetime(2026, 2, 23, 18, 31)
    assert message.message_code == 'STR0015E'
    assert message.operation_number == '31680151250908000000001'
    assert message.system_domain == 'SPB01'
    assert message.to_ispb == '00038166'
    assert message.closing_timestamp_error_code == 'EGEN0023'


def test_str0015_missing_required_fields() -> None:
    with pytest.raises(ValidationError) as exc:
        STR0015.model_validate({})
    missing_fields = extract_missing_fields(exc.value)
    assert missing_fields == {
        'settlement_date',
        'operation_number',
        'closing_timestamp',
        'system_domain',
        'to_ispb',
        'vendor_timestamp',
        'from_ispb',
    }


def test_str0015_to_xml() -> None:
    params = make_valid_str0015_params()
    message = STR0015.model_validate(params)
    xml = message.to_xml()

    expected_xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/SPB/STR0015.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>31680151250908000000001</NUOp>
        </BCMSG>
        <SISMSG>
            <STR0015>
                <CodMsg>STR0015</CodMsg>
                <DtHrFcht>2026-02-23T18:30:00</DtHrFcht>
                <DtHrBC>2026-02-23T18:31:00</DtHrBC>
                <DtMovto>2026-02-23</DtMovto>
            </STR0015>
        </SISMSG>
    </DOC>
    """

    assert normalize_xml(expected_xml) == normalize_xml(xml)


def test_str0015e_general_error_to_xml() -> None:
    params = make_valid_str0015e_params(general_error=True)
    message = STR0015E.model_validate(params)
    xml = message.to_xml()

    expected_xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/SPB/STR0015E.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>31680151250908000000001</NUOp>
        </BCMSG>
        <SISMSG>
            <STR0015 CodErro="EGEN0050">
                <CodMsg>STR0015E</CodMsg>
                <DtHrFcht>2026-02-23T18:30:00</DtHrFcht>
                <DtHrBC>2026-02-23T18:31:00</DtHrBC>
                <DtMovto>2026-02-23</DtMovto>
            </STR0015>
        </SISMSG>
    </DOC>
    """

    assert normalize_xml(expected_xml) == normalize_xml(xml)


def test_str0015e_tag_error_to_xml() -> None:
    params = make_valid_str0015e_params()
    message = STR0015E.model_validate(params)
    xml = message.to_xml()

    expected_xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/SPB/STR0015E.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>31680151250908000000001</NUOp>
        </BCMSG>
        <SISMSG>
            <STR0015>
                <CodMsg>STR0015E</CodMsg>
                <DtHrFcht CodErro="EGEN0023">2026-02-23T18:30:00</DtHrFcht>
                <DtHrBC>2026-02-23T18:31:00</DtHrBC>
                <DtMovto>2026-02-23</DtMovto>
            </STR0015>
        </SISMSG>
    </DOC>
    """

    assert normalize_xml(expected_xml) == normalize_xml(xml)


def test_str0015_from_xml() -> None:
    xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/SPB/STR0015.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>31680151250908000000001</NUOp>
        </BCMSG>
        <SISMSG>
            <STR0015>
                <CodMsg>STR0015</CodMsg>
                <DtHrFcht>2026-02-23T18:30:00</DtHrFcht>
                <DtHrBC>2026-02-23T18:31:00</DtHrBC>
                <DtMovto>2026-02-23</DtMovto>
            </STR0015>
        </SISMSG>
    </DOC>
    """

    message = STR0015.from_xml(xml)
    assert isinstance(message, STR0015)
    assert message.from_ispb == '31680151'
    assert message.settlement_date == date(2026, 2, 23)
    assert message.closing_timestamp == datetime(2026, 2, 23, 18, 30)
    assert message.vendor_timestamp == datetime(2026, 2, 23, 18, 31)
    assert message.message_code == 'STR0015'
    assert message.operation_number == '31680151250908000000001'
    assert message.system_domain == 'SPB01'
    assert message.to_ispb == '00038166'


def test_str0015e_general_error_from_xml() -> None:
    xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/SPB/STR0015E.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>31680151250908000000001</NUOp>
        </BCMSG>
        <SISMSG>
            <STR0015 CodErro="EGEN0050">
                <CodMsg>STR0015E</CodMsg>
                <DtHrFcht>2026-02-23T18:30:00</DtHrFcht>
                <DtHrBC>2026-02-23T18:31:00</DtHrBC>
                <DtMovto>2026-02-23</DtMovto>
            </STR0015>
        </SISMSG>
    </DOC>
    """

    message = STR0015E.from_xml(xml)
    assert isinstance(message, STR0015E)
    assert message.from_ispb == '31680151'
    assert message.settlement_date == date(2026, 2, 23)
    assert message.closing_timestamp == datetime(2026, 2, 23, 18, 30)
    assert message.vendor_timestamp == datetime(2026, 2, 23, 18, 31)
    assert message.message_code == 'STR0015E'
    assert message.operation_number == '31680151250908000000001'
    assert message.system_domain == 'SPB01'
    assert message.to_ispb == '00038166'
    assert message.general_error_code == 'EGEN0050'


def test_str0015e_tag_error_from_xml() -> None:
    xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/SPB/STR0015E.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>31680151250908000000001</NUOp>
        </BCMSG>
        <SISMSG>
            <STR0015>
                <CodMsg>STR0015E</CodMsg>
                <DtHrFcht CodErro="EGEN0023">2026-02-23T18:30:00</DtHrFcht>
                <DtHrBC>2026-02-23T18:31:00</DtHrBC>
                <DtMovto>2026-02-23</DtMovto>
            </STR0015>
        </SISMSG>
    </DOC>
    """

    message = STR0015E.from_xml(xml)
    assert isinstance(message, STR0015E)
    assert message.from_ispb == '31680151'
    assert message.settlement_date == date(2026, 2, 23)
    assert message.closing_timestamp == datetime(2026, 2, 23, 18, 30)
    assert message.vendor_timestamp == datetime(2026, 2, 23, 18, 31)
    assert message.message_code == 'STR0015E'
    assert message.operation_number == '31680151250908000000001'
    assert message.system_domain == 'SPB01'
    assert message.to_ispb == '00038166'
    assert message.closing_timestamp_error_code == 'EGEN0023'


def test_str0015_roundtrip() -> None:
    params = make_valid_str0015_params()
    message = STR0015.model_validate(params)
    xml = message.to_xml()
    message_from_xml = STR0015.from_xml(xml)
    assert message == message_from_xml


def test_str0015_from_xml_missing_required_fields() -> None:
    xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/SPB/STR0015.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>31680151250908000000001</NUOp>
        </BCMSG>
        <SISMSG>
            <STR0015>
                <CodMsg>STR0015</CodMsg>
            </STR0015>
        </SISMSG>
    </DOC>
    """

    with pytest.raises(ValidationError) as exc:
        STR0015.from_xml(xml)
    missing_fields = extract_missing_fields(exc.value)
    assert missing_fields == {
        'settlement_date',
        'closing_timestamp',
        'vendor_timestamp',
    }
