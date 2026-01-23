from datetime import date, datetime
from typing import Any

import pytest
from pydantic import ValidationError

from sfn_messages.str.str0017 import STR0017, STR0017E
from tests.conftest import extract_missing_fields, normalize_xml


def make_valid_str0017_params() -> dict[str, Any]:
    return {
        'from_ispb': '31680151',
        'operation_number': '31680151250908000000001',
        'system_domain': 'SPB01',
        'to_ispb': '00038166',
        'institution_ispb': '31680151',
        'settlement_date': date(2025, 11, 27),
        'opening_timestamp': '2025-11-20T10:00:00',
        'vendor_timestamp': '2025-11-20T15:30:00',
    }


def make_valid_str0017e_params(*, general_error: bool = False) -> dict[str, Any]:
    str0017e = {
        'from_ispb': '31680151',
        'operation_number': '31680151250908000000001',
        'system_domain': 'SPB01',
        'to_ispb': '00038166',
        'institution_ispb': '31680151',
        'settlement_date': date(2025, 11, 27),
        'opening_timestamp': '2025-11-20T10:00:00',
        'vendor_timestamp': '2025-11-20T15:30:00',
    }

    if general_error:
        str0017e['general_error_code'] = 'EGEN0050'
    else:
        str0017e['opening_timestamp_error_code'] = 'EGEN0023'

    return str0017e


def test_str0017_model_valid() -> None:
    params = make_valid_str0017_params()
    message = STR0017.model_validate(params)
    assert isinstance(message, STR0017)
    assert message.from_ispb == '31680151'
    assert message.settlement_date == date(2025, 11, 27)
    assert message.opening_timestamp == datetime(2025, 11, 20, 10, 0)
    assert message.vendor_timestamp == datetime(2025, 11, 20, 15, 30)
    assert message.message_code == 'STR0017'
    assert message.operation_number == '31680151250908000000001'
    assert message.system_domain == 'SPB01'
    assert message.to_ispb == '00038166'


def test_str0017e_general_error_model_valid() -> None:
    params = make_valid_str0017e_params(general_error=True)
    message = STR0017E.model_validate(params)
    assert isinstance(message, STR0017E)
    assert message.from_ispb == '31680151'
    assert message.settlement_date == date(2025, 11, 27)
    assert message.opening_timestamp == datetime(2025, 11, 20, 10, 0)
    assert message.vendor_timestamp == datetime(2025, 11, 20, 15, 30)
    assert message.message_code == 'STR0017E'
    assert message.operation_number == '31680151250908000000001'
    assert message.system_domain == 'SPB01'
    assert message.to_ispb == '00038166'
    assert message.general_error_code == 'EGEN0050'


def test_str0017e_tag_error_model_valid() -> None:
    params = make_valid_str0017e_params()
    message = STR0017E.model_validate(params)
    assert isinstance(message, STR0017E)
    assert message.from_ispb == '31680151'
    assert message.settlement_date == date(2025, 11, 27)
    assert message.opening_timestamp == datetime(2025, 11, 20, 10, 0)
    assert message.vendor_timestamp == datetime(2025, 11, 20, 15, 30)
    assert message.message_code == 'STR0017E'
    assert message.operation_number == '31680151250908000000001'
    assert message.system_domain == 'SPB01'
    assert message.to_ispb == '00038166'
    assert message.opening_timestamp_error_code == 'EGEN0023'


def test_str0017_missing_required_fields() -> None:
    with pytest.raises(ValidationError) as exc:
        STR0017.model_validate({})
    missing_fields = extract_missing_fields(exc.value)
    assert missing_fields == {
        'settlement_date',
        'operation_number',
        'opening_timestamp',
        'system_domain',
        'to_ispb',
        'vendor_timestamp',
        'from_ispb',
    }


def test_str0017_to_xml() -> None:
    params = make_valid_str0017_params()
    message = STR0017.model_validate(params)
    xml = message.to_xml()

    expected_xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/SPB/STR0017.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>31680151250908000000001</NUOp>
        </BCMSG>
        <SISMSG>
            <STR0017>
                <CodMsg>STR0017</CodMsg>
                <DtHrAbert>2025-11-20T10:00:00</DtHrAbert>
                <DtHrBC>2025-11-20T15:30:00</DtHrBC>
                <DtMovto>2025-11-27</DtMovto>
            </STR0017>
        </SISMSG>
    </DOC>
    """

    assert normalize_xml(expected_xml) == normalize_xml(xml)


def test_str0017e_general_error_to_xml() -> None:
    params = make_valid_str0017e_params(general_error=True)
    message = STR0017E.model_validate(params)
    xml = message.to_xml()

    expected_xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/SPB/STR0017E.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>31680151250908000000001</NUOp>
        </BCMSG>
        <SISMSG>
            <STR0017 CodErro="EGEN0050">
                <CodMsg>STR0017E</CodMsg>
                <DtHrAbert>2025-11-20T10:00:00</DtHrAbert>
                <DtHrBC>2025-11-20T15:30:00</DtHrBC>
                <DtMovto>2025-11-27</DtMovto>
            </STR0017>
        </SISMSG>
    </DOC>
    """

    assert normalize_xml(expected_xml) == normalize_xml(xml)


def test_str0017e_tag_error_to_xml() -> None:
    params = make_valid_str0017e_params()
    message = STR0017E.model_validate(params)
    xml = message.to_xml()

    expected_xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/SPB/STR0017E.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>31680151250908000000001</NUOp>
        </BCMSG>
        <SISMSG>
            <STR0017>
                <CodMsg>STR0017E</CodMsg>
                <DtHrAbert CodErro="EGEN0023">2025-11-20T10:00:00</DtHrAbert>
                <DtHrBC>2025-11-20T15:30:00</DtHrBC>
                <DtMovto>2025-11-27</DtMovto>
            </STR0017>
        </SISMSG>
    </DOC>
    """

    assert normalize_xml(expected_xml) == normalize_xml(xml)


def test_str0017_from_xml() -> None:
    xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/SPB/STR0017.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>31680151250908000000001</NUOp>
        </BCMSG>
        <SISMSG>
            <STR0017>
                <CodMsg>STR0017</CodMsg>
                <DtHrAbert>2025-11-20T10:00:00</DtHrAbert>
                <DtHrBC>2025-11-20T15:30:00</DtHrBC>
                <DtMovto>2025-11-27</DtMovto>
            </STR0017>
        </SISMSG>
    </DOC>
    """

    message = STR0017.from_xml(xml)
    assert isinstance(message, STR0017)
    assert message.from_ispb == '31680151'
    assert message.settlement_date == date(2025, 11, 27)
    assert message.opening_timestamp == datetime(2025, 11, 20, 10, 0)
    assert message.vendor_timestamp == datetime(2025, 11, 20, 15, 30)
    assert message.message_code == 'STR0017'
    assert message.operation_number == '31680151250908000000001'
    assert message.system_domain == 'SPB01'
    assert message.to_ispb == '00038166'


def test_str0017e_general_error_from_xml() -> None:
    xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/SPB/STR0017E.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>31680151250908000000001</NUOp>
        </BCMSG>
        <SISMSG>
            <STR0017 CodErro="EGEN0050">
                <CodMsg>STR0017E</CodMsg>
                <DtHrAbert>2025-11-20T10:00:00</DtHrAbert>
                <DtHrBC>2025-11-20T15:30:00</DtHrBC>
                <DtMovto>2025-11-27</DtMovto>
            </STR0017>
        </SISMSG>
    </DOC>
    """

    message = STR0017E.from_xml(xml)
    assert isinstance(message, STR0017E)
    assert message.from_ispb == '31680151'
    assert message.settlement_date == date(2025, 11, 27)
    assert message.opening_timestamp == datetime(2025, 11, 20, 10, 0)
    assert message.vendor_timestamp == datetime(2025, 11, 20, 15, 30)
    assert message.message_code == 'STR0017E'
    assert message.operation_number == '31680151250908000000001'
    assert message.system_domain == 'SPB01'
    assert message.to_ispb == '00038166'
    assert message.general_error_code == 'EGEN0050'


def test_str0017e_tag_error_from_xml() -> None:
    xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/SPB/STR0017E.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>31680151250908000000001</NUOp>
        </BCMSG>
        <SISMSG>
            <STR0017>
                <CodMsg>STR0017E</CodMsg>
                <DtHrAbert CodErro="EGEN0023">2025-11-20T10:00:00</DtHrAbert>
                <DtHrBC>2025-11-20T15:30:00</DtHrBC>
                <DtMovto>2025-11-27</DtMovto>
            </STR0017>
        </SISMSG>
    </DOC>
    """

    message = STR0017E.from_xml(xml)
    assert isinstance(message, STR0017E)
    assert message.from_ispb == '31680151'
    assert message.settlement_date == date(2025, 11, 27)
    assert message.opening_timestamp == datetime(2025, 11, 20, 10, 0)
    assert message.vendor_timestamp == datetime(2025, 11, 20, 15, 30)
    assert message.message_code == 'STR0017E'
    assert message.operation_number == '31680151250908000000001'
    assert message.system_domain == 'SPB01'
    assert message.to_ispb == '00038166'
    assert message.opening_timestamp_error_code == 'EGEN0023'


def test_str0017_roundtrip() -> None:
    params = make_valid_str0017_params()
    message = STR0017.model_validate(params)
    xml = message.to_xml()
    message_from_xml = STR0017.from_xml(xml)
    assert message == message_from_xml


def test_str0017_from_xml_missing_required_fields() -> None:
    xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/SPB/STR0017.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>31680151250908000000001</NUOp>
        </BCMSG>
        <SISMSG>
            <STR0017>
                <CodMsg>STR0017</CodMsg>
            </STR0017>
        </SISMSG>
    </DOC>
    """

    with pytest.raises(ValidationError) as exc:
        STR0017.from_xml(xml)
    missing_fields = extract_missing_fields(exc.value)
    assert missing_fields == {
        'settlement_date',
        'opening_timestamp',
        'vendor_timestamp',
    }
