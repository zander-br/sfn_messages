from datetime import date, datetime
from typing import Any

import pytest
from pydantic import ValidationError

from sfn_messages.str.str0043 import STR0043, STR0043E, STR0043R1
from tests.conftest import extract_missing_fields, normalize_xml


def make_valid_str0043_params() -> dict[str, Any]:
    return {
        'from_ispb': '31680151',
        'to_ispb': '00038166',
        'system_domain': 'SPB01',
        'operation_number': '31680151250908000000001',
        'message_code': 'STR0043',
        'participant_institution_control_number': '31680151202509090425',
        'participant_ispb': '31680151',
        'start_timestamp': '2026-01-28T09:30:00',
        'settlement_date': '2026-01-28',
    }


def make_valid_str0043r1_params() -> dict[str, Any]:
    return {
        'from_ispb': '31680151',
        'to_ispb': '00038166',
        'system_domain': 'SPB01',
        'operation_number': '31680151250908000000001',
        'message_code': 'STR0043R1',
        'participant_institution_control_number': '31680151202509090425',
        'participant_ispb': '31680151',
        'str_control_number': 'STR20250101000000001',
        'vendor_timestamp': '2026-01-28T09:15:00',
        'settlement_date': '2026-01-28',
    }


def make_valid_str0043e_params(*, general_error: bool = False) -> dict[str, Any]:
    str0043e = {
        'from_ispb': '31680151',
        'to_ispb': '00038166',
        'system_domain': 'SPB01',
        'operation_number': '31680151250908000000001',
        'message_code': 'STR0043E',
        'participant_institution_control_number': '31680151202509090425',
        'participant_ispb': '31680151',
        'start_timestamp': '2026-01-28T09:30:00',
        'settlement_date': '2026-01-28',
    }

    if general_error:
        str0043e['general_error_code'] = 'EGEN0050'
    else:
        str0043e['start_timestamp_error_code'] = 'EIDT0001'

    return str0043e


def test_str0043_valid_params() -> None:
    params = make_valid_str0043_params()
    str0043 = STR0043.model_validate(params)

    assert isinstance(str0043, STR0043)
    assert str0043.from_ispb == '31680151'
    assert str0043.operation_number == '31680151250908000000001'
    assert str0043.system_domain == 'SPB01'
    assert str0043.to_ispb == '00038166'
    assert str0043.message_code == 'STR0043'
    assert str0043.participant_institution_control_number == '31680151202509090425'
    assert str0043.participant_ispb == '31680151'
    assert str0043.start_timestamp == datetime(2026, 1, 28, 9, 30, 0)
    assert str0043.settlement_date == date(2026, 1, 28)


def test_str0043r1_valid_params() -> None:
    params = make_valid_str0043r1_params()
    str0043r1 = STR0043R1.model_validate(params)

    assert isinstance(str0043r1, STR0043R1)
    assert str0043r1.from_ispb == '31680151'
    assert str0043r1.operation_number == '31680151250908000000001'
    assert str0043r1.system_domain == 'SPB01'
    assert str0043r1.to_ispb == '00038166'
    assert str0043r1.message_code == 'STR0043R1'
    assert str0043r1.participant_institution_control_number == '31680151202509090425'
    assert str0043r1.participant_ispb == '31680151'
    assert str0043r1.str_control_number == 'STR20250101000000001'
    assert str0043r1.vendor_timestamp == datetime(2026, 1, 28, 9, 15, 0)
    assert str0043r1.settlement_date == date(2026, 1, 28)


def test_str0043e_general_error_valid_params() -> None:
    params = make_valid_str0043e_params(general_error=True)
    str0043e = STR0043E.model_validate(params)

    assert isinstance(str0043e, STR0043E)
    assert str0043e.from_ispb == '31680151'
    assert str0043e.operation_number == '31680151250908000000001'
    assert str0043e.system_domain == 'SPB01'
    assert str0043e.to_ispb == '00038166'
    assert str0043e.message_code == 'STR0043E'
    assert str0043e.participant_institution_control_number == '31680151202509090425'
    assert str0043e.participant_ispb == '31680151'
    assert str0043e.start_timestamp == datetime(2026, 1, 28, 9, 30, 0)
    assert str0043e.settlement_date == date(2026, 1, 28)
    assert str0043e.general_error_code == 'EGEN0050'


def test_str0043e_tag_error_valid_params() -> None:
    params = make_valid_str0043e_params()
    str0043e = STR0043E.model_validate(params)

    assert isinstance(str0043e, STR0043E)
    assert str0043e.from_ispb == '31680151'
    assert str0043e.operation_number == '31680151250908000000001'
    assert str0043e.system_domain == 'SPB01'
    assert str0043e.to_ispb == '00038166'
    assert str0043e.message_code == 'STR0043E'
    assert str0043e.participant_institution_control_number == '31680151202509090425'
    assert str0043e.participant_ispb == '31680151'
    assert str0043e.start_timestamp == datetime(2026, 1, 28, 9, 30, 0)
    assert str0043e.settlement_date == date(2026, 1, 28)
    assert str0043e.start_timestamp_error_code == 'EIDT0001'


def test_str0043_missing_required_fields() -> None:
    with pytest.raises(ValidationError) as exc:
        STR0043.model_validate({})
    missing_fields = extract_missing_fields(exc.value)
    assert missing_fields == {
        'from_ispb',
        'to_ispb',
        'system_domain',
        'operation_number',
        'participant_institution_control_number',
        'participant_ispb',
        'start_timestamp',
        'settlement_date',
    }


def test_str0043r1_missing_required_fields() -> None:
    with pytest.raises(ValidationError) as exc:
        STR0043R1.model_validate({})
    missing_fields = extract_missing_fields(exc.value)
    assert missing_fields == {
        'from_ispb',
        'to_ispb',
        'system_domain',
        'operation_number',
        'participant_institution_control_number',
        'participant_ispb',
        'str_control_number',
        'vendor_timestamp',
        'settlement_date',
    }


def test_str0043_to_xml() -> None:
    params = make_valid_str0043_params()
    str0043 = STR0043.model_validate(params)
    xml = str0043.to_xml()

    expected_xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/SPB/STR0043.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>31680151250908000000001</NUOp>
        </BCMSG>
        <SISMSG>
            <STR0043>
                <CodMsg>STR0043</CodMsg>
                <NumCtrlPart>31680151202509090425</NumCtrlPart>
                <ISPBPart>31680151</ISPBPart>
                <DtHrIniTeste>2026-01-28T09:30:00</DtHrIniTeste>
                <DtMovto>2026-01-28</DtMovto>
            </STR0043>
        </SISMSG>
    </DOC>
    """

    assert normalize_xml(expected_xml) == normalize_xml(xml)


def test_str0043r1_to_xml() -> None:
    params = make_valid_str0043r1_params()
    str0043r1 = STR0043R1.model_validate(params)
    xml = str0043r1.to_xml()

    expected_xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/SPB/STR0043.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>31680151250908000000001</NUOp>
        </BCMSG>
        <SISMSG>
            <STR0043R1>
                <CodMsg>STR0043R1</CodMsg>
                <NumCtrlPart>31680151202509090425</NumCtrlPart>
                <ISPBPart>31680151</ISPBPart>
                <NumCtrlSTR>STR20250101000000001</NumCtrlSTR>
                <DtHrBC>2026-01-28T09:15:00</DtHrBC>
                <DtMovto>2026-01-28</DtMovto>
            </STR0043R1>
        </SISMSG>
    </DOC>
    """

    assert normalize_xml(expected_xml) == normalize_xml(xml)


def test_str0043e_general_error_to_xml() -> None:
    params = make_valid_str0043e_params(general_error=True)
    str0043e = STR0043E.model_validate(params)
    xml = str0043e.to_xml()

    expected_xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/SPB/STR0043E.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>31680151250908000000001</NUOp>
        </BCMSG>
        <SISMSG>
            <STR0043 CodErro="EGEN0050">
                <CodMsg>STR0043E</CodMsg>
                <NumCtrlPart>31680151202509090425</NumCtrlPart>
                <ISPBPart>31680151</ISPBPart>
                <DtHrIniTeste>2026-01-28T09:30:00</DtHrIniTeste>
                <DtMovto>2026-01-28</DtMovto>
            </STR0043>
        </SISMSG>
    </DOC>
    """

    assert normalize_xml(expected_xml) == normalize_xml(xml)


def test_str0043e_tag_error_to_xml() -> None:
    params = make_valid_str0043e_params()
    str0043e = STR0043E.model_validate(params)
    xml = str0043e.to_xml()

    expected_xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/SPB/STR0043E.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>31680151250908000000001</NUOp>
        </BCMSG>
        <SISMSG>
            <STR0043>
                <CodMsg>STR0043E</CodMsg>
                <NumCtrlPart>31680151202509090425</NumCtrlPart>
                <ISPBPart>31680151</ISPBPart>
                <DtHrIniTeste CodErro="EIDT0001">2026-01-28T09:30:00</DtHrIniTeste>
                <DtMovto>2026-01-28</DtMovto>
            </STR0043>
        </SISMSG>
    </DOC>
    """

    assert normalize_xml(expected_xml) == normalize_xml(xml)


def test_str0043_from_xml() -> None:
    xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/SPB/STR0043.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>31680151250908000000001</NUOp>
        </BCMSG>
        <SISMSG>
            <STR0043>
                <CodMsg>STR0043</CodMsg>
                <NumCtrlPart>31680151202509090425</NumCtrlPart>
                <ISPBPart>31680151</ISPBPart>
                <DtHrIniTeste>2026-01-28T09:30:00</DtHrIniTeste>
                <DtMovto>2026-01-28</DtMovto>
            </STR0043>
        </SISMSG>
    </DOC>
    """

    str0043 = STR0043.from_xml(xml)

    assert isinstance(str0043, STR0043)
    assert str0043.from_ispb == '31680151'
    assert str0043.operation_number == '31680151250908000000001'
    assert str0043.system_domain == 'SPB01'
    assert str0043.to_ispb == '00038166'
    assert str0043.message_code == 'STR0043'
    assert str0043.participant_institution_control_number == '31680151202509090425'
    assert str0043.participant_ispb == '31680151'
    assert str0043.start_timestamp == datetime(2026, 1, 28, 9, 30, 0)
    assert str0043.settlement_date == date(2026, 1, 28)


def test_str0043r1_from_xml() -> None:
    xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/SPB/STR0043.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>31680151250908000000001</NUOp>
        </BCMSG>
        <SISMSG>
            <STR0043R1>
                <CodMsg>STR0043R1</CodMsg>
                <NumCtrlPart>31680151202509090425</NumCtrlPart>
                <ISPBPart>31680151</ISPBPart>
                <NumCtrlSTR>STR20250101000000001</NumCtrlSTR>
                <DtHrBC>2026-01-28T09:15:00</DtHrBC>
                <DtMovto>2026-01-28</DtMovto>
            </STR0043R1>
        </SISMSG>
    </DOC>
    """

    str0043r1 = STR0043R1.from_xml(xml)

    assert isinstance(str0043r1, STR0043R1)
    assert str0043r1.from_ispb == '31680151'
    assert str0043r1.operation_number == '31680151250908000000001'
    assert str0043r1.system_domain == 'SPB01'
    assert str0043r1.to_ispb == '00038166'
    assert str0043r1.message_code == 'STR0043R1'
    assert str0043r1.participant_institution_control_number == '31680151202509090425'
    assert str0043r1.participant_ispb == '31680151'
    assert str0043r1.str_control_number == 'STR20250101000000001'
    assert str0043r1.vendor_timestamp == datetime(2026, 1, 28, 9, 15, 0)
    assert str0043r1.settlement_date == date(2026, 1, 28)


def test_str0043e_general_error_from_xml() -> None:
    xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/SPB/STR0043E.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>31680151250908000000001</NUOp>
        </BCMSG>
        <SISMSG>
            <STR0043 CodErro="EGEN0050">
                <CodMsg>STR0043E</CodMsg>
                <NumCtrlPart>31680151202509090425</NumCtrlPart>
                <ISPBPart>31680151</ISPBPart>
                <DtHrIniTeste>2026-01-28T09:30:00</DtHrIniTeste>
                <DtMovto>2026-01-28</DtMovto>
            </STR0043>
        </SISMSG>
    </DOC>
    """

    str0043e = STR0043E.from_xml(xml)

    assert isinstance(str0043e, STR0043E)
    assert str0043e.from_ispb == '31680151'
    assert str0043e.operation_number == '31680151250908000000001'
    assert str0043e.system_domain == 'SPB01'
    assert str0043e.to_ispb == '00038166'
    assert str0043e.message_code == 'STR0043E'
    assert str0043e.participant_institution_control_number == '31680151202509090425'
    assert str0043e.participant_ispb == '31680151'
    assert str0043e.start_timestamp == datetime(2026, 1, 28, 9, 30, 0)
    assert str0043e.settlement_date == date(2026, 1, 28)
    assert str0043e.general_error_code == 'EGEN0050'


def test_str0043e_tag_error_from_xml() -> None:
    xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/SPB/STR0043E.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>31680151250908000000001</NUOp>
        </BCMSG>
        <SISMSG>
            <STR0043>
                <CodMsg>STR0043E</CodMsg>
                <NumCtrlPart>31680151202509090425</NumCtrlPart>
                <ISPBPart>31680151</ISPBPart>
                <DtHrIniTeste CodErro="EIDT0001">2026-01-28T09:30:00</DtHrIniTeste>
                <DtMovto>2026-01-28</DtMovto>
            </STR0043>
        </SISMSG>
    </DOC>
    """

    str0043e = STR0043E.from_xml(xml)

    assert isinstance(str0043e, STR0043E)
    assert str0043e.from_ispb == '31680151'
    assert str0043e.operation_number == '31680151250908000000001'
    assert str0043e.system_domain == 'SPB01'
    assert str0043e.to_ispb == '00038166'
    assert str0043e.message_code == 'STR0043E'
    assert str0043e.participant_institution_control_number == '31680151202509090425'
    assert str0043e.participant_ispb == '31680151'
    assert str0043e.start_timestamp == datetime(2026, 1, 28, 9, 30, 0)
    assert str0043e.settlement_date == date(2026, 1, 28)
    assert str0043e.start_timestamp_error_code == 'EIDT0001'


def test_str0043_roundtrip() -> None:
    params = make_valid_str0043_params()
    str0043 = STR0043.model_validate(params)
    xml = str0043.to_xml()
    str0043_from_xml = STR0043.from_xml(xml)
    assert str0043 == str0043_from_xml


def test_str0043r1_roundtrip() -> None:
    params = make_valid_str0043r1_params()
    str0043r1 = STR0043R1.model_validate(params)
    xml = str0043r1.to_xml()
    str0043r1_from_xml = STR0043R1.from_xml(xml)
    assert str0043r1 == str0043r1_from_xml


def test_str0043_from_xml_missing_required_fields() -> None:
    xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/SPB/STR0043.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>31680151250908000000001</NUOp>
        </BCMSG>
        <SISMSG>
            <STR0043>
                <CodMsg>STR0043</CodMsg>
            </STR0043>
        </SISMSG>
    </DOC>
    """

    with pytest.raises(ValidationError) as exc:
        STR0043.from_xml(xml)

    missing_fields = extract_missing_fields(exc.value)
    assert missing_fields == {
        'participant_institution_control_number',
        'participant_ispb',
        'start_timestamp',
        'settlement_date',
    }


def test_str0043r1_from_xml_missing_required_fields() -> None:
    xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/SPB/STR0043.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>31680151250908000000001</NUOp>
        </BCMSG>
        <SISMSG>
            <STR0043>
                <CodMsg>STR0043</CodMsg>
            </STR0043>
        </SISMSG>
    </DOC>
    """

    with pytest.raises(ValidationError) as exc:
        STR0043R1.from_xml(xml)

    missing_fields = extract_missing_fields(exc.value)
    assert missing_fields == {
        'participant_institution_control_number',
        'participant_ispb',
        'str_control_number',
        'vendor_timestamp',
        'settlement_date',
    }
