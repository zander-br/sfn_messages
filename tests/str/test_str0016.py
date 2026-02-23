from datetime import date, datetime
from decimal import Decimal
from typing import Any

import pytest
from pydantic import ValidationError

from sfn_messages.str.str0016 import STR0016, STR0016E
from tests.conftest import extract_missing_fields, normalize_xml


def make_valid_str0016_params() -> dict[str, Any]:
    return {
        'from_ispb': '31680151',
        'operation_number': '31680151250908000000001',
        'system_domain': 'SPB01',
        'to_ispb': '00038166',
        'institution_ispb': '31680151',
        'participant_ispb': '31680151',
        'balance_type': '1',
        'balance': '1000.0',
        'vendor_timestamp': '2026-02-23T18:31:00',
        'settlement_date': '2026-02-23',
    }


def make_valid_str0016e_params(*, general_error: bool = False) -> dict[str, Any]:
    str0016e = {
        'from_ispb': '31680151',
        'operation_number': '31680151250908000000001',
        'system_domain': 'SPB01',
        'to_ispb': '00038166',
        'institution_ispb': '31680151',
        'participant_ispb': '31680151',
        'balance_type': '1',
        'balance': '1000.0',
        'vendor_timestamp': '2026-02-23T18:31:00',
        'settlement_date': '2026-02-23',
    }

    if general_error:
        str0016e['general_error_code'] = 'EGEN0050'
    else:
        str0016e['balance_error_code'] = 'EGEN0023'

    return str0016e


def test_str0016_model_valid() -> None:
    params = make_valid_str0016_params()
    message = STR0016.model_validate(params)
    assert isinstance(message, STR0016)
    assert message.from_ispb == '31680151'
    assert message.message_code == 'STR0016'
    assert message.operation_number == '31680151250908000000001'
    assert message.system_domain == 'SPB01'
    assert message.to_ispb == '00038166'
    assert message.participant_ispb == '31680151'
    assert message.balance_type == '1'
    assert message.balance == Decimal('1000.0')
    assert message.vendor_timestamp == datetime(2026, 2, 23, 18, 31)
    assert message.settlement_date == date(2026, 2, 23)


def test_str0016e_general_error_model_valid() -> None:
    params = make_valid_str0016e_params(general_error=True)
    message = STR0016E.model_validate(params)
    assert isinstance(message, STR0016E)
    assert message.from_ispb == '31680151'
    assert message.message_code == 'STR0016E'
    assert message.operation_number == '31680151250908000000001'
    assert message.system_domain == 'SPB01'
    assert message.to_ispb == '00038166'
    assert message.participant_ispb == '31680151'
    assert message.balance_type == '1'
    assert message.balance == Decimal('1000.0')
    assert message.vendor_timestamp == datetime(2026, 2, 23, 18, 31)
    assert message.settlement_date == date(2026, 2, 23)
    assert message.general_error_code == 'EGEN0050'


def test_str0016e_tag_error_model_valid() -> None:
    params = make_valid_str0016e_params()
    message = STR0016E.model_validate(params)
    assert isinstance(message, STR0016E)
    assert message.from_ispb == '31680151'
    assert message.message_code == 'STR0016E'
    assert message.operation_number == '31680151250908000000001'
    assert message.system_domain == 'SPB01'
    assert message.to_ispb == '00038166'
    assert message.participant_ispb == '31680151'
    assert message.balance_type == '1'
    assert message.balance == Decimal('1000.0')
    assert message.vendor_timestamp == datetime(2026, 2, 23, 18, 31)
    assert message.settlement_date == date(2026, 2, 23)
    assert message.balance_error_code == 'EGEN0023'


def test_str0016_missing_required_fields() -> None:
    with pytest.raises(ValidationError) as exc:
        STR0016.model_validate({})
    missing_fields = extract_missing_fields(exc.value)
    assert missing_fields == {
        'operation_number',
        'system_domain',
        'to_ispb',
        'from_ispb',
        'participant_ispb',
        'balance_type',
        'balance',
        'vendor_timestamp',
        'settlement_date',
    }


def test_str0016_to_xml() -> None:
    params = make_valid_str0016_params()
    message = STR0016.model_validate(params)
    xml = message.to_xml()

    expected_xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/SPB/STR0016.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>31680151250908000000001</NUOp>
        </BCMSG>
        <SISMSG>
            <STR0016>
                <CodMsg>STR0016</CodMsg>
                <ISPBPart>31680151</ISPBPart>
                <TpSld>1</TpSld>
                <SldRB_CL>1000.0</SldRB_CL>
                <DtHrBC>2026-02-23T18:31:00</DtHrBC>
                <DtMovto>2026-02-23</DtMovto>
            </STR0016>
        </SISMSG>
    </DOC>
    """

    assert normalize_xml(expected_xml) == normalize_xml(xml)


def test_str0016e_general_error_to_xml() -> None:
    params = make_valid_str0016e_params(general_error=True)
    message = STR0016E.model_validate(params)
    xml = message.to_xml()

    expected_xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/SPB/STR0016E.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>31680151250908000000001</NUOp>
        </BCMSG>
        <SISMSG>
            <STR0016 CodErro="EGEN0050">
                <CodMsg>STR0016E</CodMsg>
                <ISPBPart>31680151</ISPBPart>
                <TpSld>1</TpSld>
                <SldRB_CL>1000.0</SldRB_CL>
                <DtHrBC>2026-02-23T18:31:00</DtHrBC>
                <DtMovto>2026-02-23</DtMovto>
            </STR0016>
        </SISMSG>
    </DOC>
    """

    assert normalize_xml(expected_xml) == normalize_xml(xml)


def test_str0016e_tag_error_to_xml() -> None:
    params = make_valid_str0016e_params()
    message = STR0016E.model_validate(params)
    xml = message.to_xml()

    expected_xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/SPB/STR0016E.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>31680151250908000000001</NUOp>
        </BCMSG>
        <SISMSG>
            <STR0016>
                <CodMsg>STR0016E</CodMsg>
                <ISPBPart>31680151</ISPBPart>
                <TpSld>1</TpSld>
                <SldRB_CL CodErro="EGEN0023">1000.0</SldRB_CL>
                <DtHrBC>2026-02-23T18:31:00</DtHrBC>
                <DtMovto>2026-02-23</DtMovto>
            </STR0016>
        </SISMSG>
    </DOC>
    """

    assert normalize_xml(expected_xml) == normalize_xml(xml)


def test_str0016_from_xml() -> None:
    xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/SPB/STR0016.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>31680151250908000000001</NUOp>
        </BCMSG>
        <SISMSG>
            <STR0016>
                <CodMsg>STR0016</CodMsg>
                <ISPBPart>31680151</ISPBPart>
                <TpSld>1</TpSld>
                <SldRB_CL>1000.0</SldRB_CL>
                <DtHrBC>2026-02-23T18:31:00</DtHrBC>
                <DtMovto>2026-02-23</DtMovto>
            </STR0016>
        </SISMSG>
    </DOC>
    """

    message = STR0016.from_xml(xml)
    assert isinstance(message, STR0016)
    assert message.from_ispb == '31680151'
    assert message.message_code == 'STR0016'
    assert message.operation_number == '31680151250908000000001'
    assert message.system_domain == 'SPB01'
    assert message.to_ispb == '00038166'
    assert message.participant_ispb == '31680151'
    assert message.balance_type == '1'
    assert message.balance == Decimal('1000.0')
    assert message.vendor_timestamp == datetime(2026, 2, 23, 18, 31)
    assert message.settlement_date == date(2026, 2, 23)


def test_str0016e_general_error_from_xml() -> None:
    xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/SPB/STR0016E.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>31680151250908000000001</NUOp>
        </BCMSG>
        <SISMSG>
            <STR0016 CodErro="EGEN0050">
                <CodMsg>STR0016E</CodMsg>
                <ISPBPart>31680151</ISPBPart>
                <TpSld>1</TpSld>
                <SldRB_CL>1000.0</SldRB_CL>
                <DtHrBC>2026-02-23T18:31:00</DtHrBC>
                <DtMovto>2026-02-23</DtMovto>
            </STR0016>
        </SISMSG>
    </DOC>
    """

    message = STR0016E.from_xml(xml)
    assert isinstance(message, STR0016E)
    assert message.from_ispb == '31680151'
    assert message.message_code == 'STR0016E'
    assert message.operation_number == '31680151250908000000001'
    assert message.system_domain == 'SPB01'
    assert message.to_ispb == '00038166'
    assert message.participant_ispb == '31680151'
    assert message.balance_type == '1'
    assert message.balance == Decimal('1000.0')
    assert message.vendor_timestamp == datetime(2026, 2, 23, 18, 31)
    assert message.settlement_date == date(2026, 2, 23)
    assert message.general_error_code == 'EGEN0050'


def test_str0016e_tag_error_from_xml() -> None:
    xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/SPB/STR0016E.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>31680151250908000000001</NUOp>
        </BCMSG>
        <SISMSG>
            <STR0016>
                <CodMsg>STR0016E</CodMsg>
                <ISPBPart>31680151</ISPBPart>
                <TpSld>1</TpSld>
                <SldRB_CL CodErro="EGEN0023">1000.0</SldRB_CL>
                <DtHrBC>2026-02-23T18:31:00</DtHrBC>
                <DtMovto>2026-02-23</DtMovto>
            </STR0016>
        </SISMSG>
    </DOC>
    """

    message = STR0016E.from_xml(xml)
    assert isinstance(message, STR0016E)
    assert message.from_ispb == '31680151'
    assert message.message_code == 'STR0016E'
    assert message.operation_number == '31680151250908000000001'
    assert message.system_domain == 'SPB01'
    assert message.to_ispb == '00038166'
    assert message.participant_ispb == '31680151'
    assert message.balance_type == '1'
    assert message.balance == Decimal('1000.0')
    assert message.vendor_timestamp == datetime(2026, 2, 23, 18, 31)
    assert message.settlement_date == date(2026, 2, 23)
    assert message.balance_error_code == 'EGEN0023'


def test_str0016_roundtrip() -> None:
    params = make_valid_str0016_params()
    message = STR0016.model_validate(params)
    xml = message.to_xml()
    message_from_xml = STR0016.from_xml(xml)
    assert message == message_from_xml


def test_str0016_from_xml_missing_required_fields() -> None:
    xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/SPB/STR0016.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>31680151250908000000001</NUOp>
        </BCMSG>
        <SISMSG>
            <STR0016>
                <CodMsg>STR0016</CodMsg>
            </STR0016>
        </SISMSG>
    </DOC>
    """

    with pytest.raises(ValidationError) as exc:
        STR0016.from_xml(xml)
    missing_fields = extract_missing_fields(exc.value)
    assert missing_fields == {
        'participant_ispb',
        'balance_type',
        'balance',
        'vendor_timestamp',
        'settlement_date',
    }
