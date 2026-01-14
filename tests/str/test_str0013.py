from datetime import UTC, date, datetime
from decimal import Decimal
from typing import Any

import pytest
from pydantic import ValidationError

from sfn_messages.str.str0013 import STR0013, STR0013E, STR0013R1
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


def make_valid_str0013r1_params() -> dict[str, Any]:
    return {
        'from_ispb': '31680151',
        'operation_number': '316801512509080000001',
        'system_domain': 'SPB01',
        'to_ispb': '00038166',
        'institution_control_number': '31680151202509090425',
        'institution_ispb': '31680151',
        'settlement_date': date(2025, 11, 27),
        'balance': '100.50',
        'vendor_timestamp': '2025-11-20T15:30:00+00:00',
    }


def make_valid_str0013e_params(*, general_error: bool = False) -> dict[str, Any]:
    str0013e = {
        'from_ispb': '31680151',
        'operation_number': '316801512509080000001',
        'system_domain': 'SPB01',
        'to_ispb': '00038166',
        'institution_control_number': '31680151202509090425',
        'institution_ispb': '31680151',
        'settlement_date': date(2025, 11, 27),
    }

    if general_error:
        str0013e['general_error_code'] = 'EGEN0050'
    else:
        str0013e['institution_ispb_error_code'] = 'EGEN0051'

    return str0013e


def test_str0013_model_valid() -> None:
    params = make_valid_str0013_params()
    message = STR0013.model_validate(params)
    assert isinstance(message, STR0013)
    assert message.from_ispb == '31680151'
    assert message.institution_control_number == '31680151202509090425'
    assert message.settlement_date == date(2025, 11, 27)
    assert message.message_code == 'STR0013'
    assert message.institution_ispb == '31680151'
    assert message.operation_number == '316801512509080000001'
    assert message.system_domain == 'SPB01'
    assert message.to_ispb == '00038166'


def test_str0013e_general_error_model_valid() -> None:
    params = make_valid_str0013e_params(general_error=True)
    message = STR0013E.model_validate(params)
    assert isinstance(message, STR0013E)
    assert message.from_ispb == '31680151'
    assert message.institution_control_number == '31680151202509090425'
    assert message.settlement_date == date(2025, 11, 27)
    assert message.message_code == 'STR0013'
    assert message.institution_ispb == '31680151'
    assert message.operation_number == '316801512509080000001'
    assert message.system_domain == 'SPB01'
    assert message.to_ispb == '00038166'
    assert message.general_error_code == 'EGEN0050'


def test_str0013e_tag_error_model_valid() -> None:
    params = make_valid_str0013e_params()
    message = STR0013E.model_validate(params)
    assert isinstance(message, STR0013E)
    assert message.from_ispb == '31680151'
    assert message.institution_control_number == '31680151202509090425'
    assert message.settlement_date == date(2025, 11, 27)
    assert message.message_code == 'STR0013'
    assert message.institution_ispb == '31680151'
    assert message.operation_number == '316801512509080000001'
    assert message.system_domain == 'SPB01'
    assert message.to_ispb == '00038166'
    assert message.institution_ispb_error_code == 'EGEN0051'


def test_str0013_missing_required_fields() -> None:
    with pytest.raises(ValidationError) as exc:
        STR0013.model_validate({})
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
    str0013 = STR0013.model_validate(params)
    xml = str0013.to_xml()

    expected_xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/SPB/STR0013.xsd">
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


def test_str0013e_general_error_to_xml() -> None:
    params = make_valid_str0013e_params(general_error=True)
    str0013e = STR0013E.model_validate(params)
    xml = str0013e.to_xml()

    expected_xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/SPB/STR0013E.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>316801512509080000001</NUOp>
        </BCMSG>
        <SISMSG>
            <STR0013E CodErro="EGEN0050">
                <CodMsg>STR0013</CodMsg>
                <NumCtrlIF_LDL>31680151202509090425</NumCtrlIF_LDL>
                <ISPBIF_LDL>31680151</ISPBIF_LDL>
                <DtMovto>2025-11-27</DtMovto>
            </STR0013E>
        </SISMSG>
    </DOC>
    """

    assert normalize_xml(expected_xml) == normalize_xml(xml)


def test_str0013e_tag_error_to_xml() -> None:
    params = make_valid_str0013e_params()
    str0013e = STR0013E.model_validate(params)
    xml = str0013e.to_xml()

    expected_xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/SPB/STR0013E.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>316801512509080000001</NUOp>
        </BCMSG>
        <SISMSG>
            <STR0013E>
                <CodMsg>STR0013</CodMsg>
                <NumCtrlIF_LDL>31680151202509090425</NumCtrlIF_LDL>
                <ISPBIF_LDL CodErro="EGEN0051">31680151</ISPBIF_LDL>
                <DtMovto>2025-11-27</DtMovto>
            </STR0013E>
        </SISMSG>
    </DOC>
    """

    assert normalize_xml(expected_xml) == normalize_xml(xml)


def test_str0013_from_xml() -> None:
    xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/SPB/STR0013.xsd">
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

    str0013 = STR0013.from_xml(xml)

    assert isinstance(str0013, STR0013)
    assert str0013.message_code == 'STR0013'
    assert str0013.institution_control_number == '31680151202509090425'
    assert str0013.institution_ispb == '31680151'
    assert str0013.settlement_date == date(2025, 11, 27)
    assert str0013.from_ispb == '31680151'
    assert str0013.to_ispb == '00038166'
    assert str0013.system_domain == 'SPB01'
    assert str0013.operation_number == '316801512509080000001'


def test_str0013e_general_error_from_xml() -> None:
    xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/SPB/STR0013E.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>316801512509080000001</NUOp>
        </BCMSG>
        <SISMSG>
            <STR0013E CodErro="EGEN0050">
                <CodMsg>STR0013</CodMsg>
                <NumCtrlIF_LDL>31680151202509090425</NumCtrlIF_LDL>
                <ISPBIF_LDL>31680151</ISPBIF_LDL>
                <DtMovto>2025-11-27</DtMovto>
            </STR0013E>
        </SISMSG>
    </DOC>
    """

    str0013e = STR0013E.from_xml(xml)

    assert isinstance(str0013e, STR0013E)
    assert str0013e.message_code == 'STR0013'
    assert str0013e.institution_control_number == '31680151202509090425'
    assert str0013e.institution_ispb == '31680151'
    assert str0013e.settlement_date == date(2025, 11, 27)
    assert str0013e.from_ispb == '31680151'
    assert str0013e.to_ispb == '00038166'
    assert str0013e.system_domain == 'SPB01'
    assert str0013e.operation_number == '316801512509080000001'
    assert str0013e.general_error_code == 'EGEN0050'


def test_str0013e_tag_error_from_xml() -> None:
    xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/SPB/STR0013E.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>316801512509080000001</NUOp>
        </BCMSG>
        <SISMSG>
            <STR0013E>
                <CodMsg>STR0013</CodMsg>
                <NumCtrlIF_LDL>31680151202509090425</NumCtrlIF_LDL>
                <ISPBIF_LDL CodErro="EGEN0051">31680151</ISPBIF_LDL>
                <DtMovto>2025-11-27</DtMovto>
            </STR0013E>
        </SISMSG>
    </DOC>
    """

    str0013e = STR0013E.from_xml(xml)

    assert isinstance(str0013e, STR0013E)
    assert str0013e.message_code == 'STR0013'
    assert str0013e.institution_control_number == '31680151202509090425'
    assert str0013e.institution_ispb == '31680151'
    assert str0013e.settlement_date == date(2025, 11, 27)
    assert str0013e.from_ispb == '31680151'
    assert str0013e.to_ispb == '00038166'
    assert str0013e.system_domain == 'SPB01'
    assert str0013e.operation_number == '316801512509080000001'
    assert str0013e.institution_ispb_error_code == 'EGEN0051'


def test_str0013_roundtrip() -> None:
    params = make_valid_str0013_params()
    str0013 = STR0013.model_validate(params)
    xml = str0013.to_xml()
    str0013_from_xml = STR0013.from_xml(xml)
    assert str0013 == str0013_from_xml


def test_str0013_from_xml_missing_required_fields() -> None:
    xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/SPB/STR0013.xsd">
        <SISMSG>
            <STR0013>
                <CodMsg>STR0013</CodMsg>
            </STR0013>
        </SISMSG>
    </DOC>
    """

    with pytest.raises(ValidationError) as exc:
        STR0013.from_xml(xml)
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


def test_str0013r1_model_valid() -> None:
    params = make_valid_str0013r1_params()
    message = STR0013R1.model_validate(params)
    assert isinstance(message, STR0013R1)
    assert message.from_ispb == '31680151'
    assert message.institution_control_number == '31680151202509090425'
    assert message.settlement_date == date(2025, 11, 27)
    assert message.message_code == 'STR0013R1'
    assert message.institution_ispb == '31680151'
    assert message.operation_number == '316801512509080000001'
    assert message.system_domain == 'SPB01'
    assert message.to_ispb == '00038166'
    assert message.balance == Decimal('100.50')
    assert message.vendor_timestamp == datetime(2025, 11, 20, 15, 30, 0, tzinfo=UTC)


def test_str0013r1_missing_required_fields() -> None:
    with pytest.raises(ValidationError) as exc:
        STR0013R1.model_validate({})
    missing_fields = extract_missing_fields(exc.value)
    assert missing_fields == {
        'institution_ispb',
        'from_ispb',
        'to_ispb',
        'vendor_timestamp',
        'settlement_date',
        'operation_number',
        'system_domain',
        'institution_control_number',
        'balance',
    }


def test_str0013r1_to_xml() -> None:
    params = make_valid_str0013r1_params()
    str0013r1 = STR0013R1.model_validate(params)
    xml = str0013r1.to_xml()

    expected_xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/SPB/STR0013.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>316801512509080000001</NUOp>
        </BCMSG>
        <SISMSG>
            <STR0013R1>
                <CodMsg>STR0013R1</CodMsg>
                <NumCtrlIF_LDL>31680151202509090425</NumCtrlIF_LDL>
                <ISPBIF_LDL>31680151</ISPBIF_LDL>
                <SldRB_CL>100.50</SldRB_CL>
                <DtHrBC>2025-11-20 15:30:00+00:00</DtHrBC>
                <DtMovto>2025-11-27</DtMovto>
            </STR0013R1>
        </SISMSG>
    </DOC>
    """

    assert normalize_xml(expected_xml) == normalize_xml(xml)


def test_str0013r1_from_xml() -> None:
    xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/SPB/STR0013.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>316801512509080000001</NUOp>
        </BCMSG>
        <SISMSG>
            <STR0013R1>
                <CodMsg>STR0013R1</CodMsg>
                <NumCtrlIF_LDL>31680151202509090425</NumCtrlIF_LDL>
                <ISPBIF_LDL>31680151</ISPBIF_LDL>
                <SldRB_CL>100.50</SldRB_CL>
                <DtHrBC>2025-11-20 15:30:00+00:00</DtHrBC>
                <DtMovto>2025-11-27</DtMovto>
            </STR0013R1>
        </SISMSG>
    </DOC>
    """

    str0013r1 = STR0013R1.from_xml(xml)
    assert isinstance(str0013r1, STR0013R1)
    assert str0013r1.message_code == 'STR0013R1'
    assert str0013r1.institution_control_number == '31680151202509090425'
    assert str0013r1.institution_ispb == '31680151'
    assert str0013r1.settlement_date == date(2025, 11, 27)
    assert str0013r1.from_ispb == '31680151'
    assert str0013r1.to_ispb == '00038166'
    assert str0013r1.system_domain == 'SPB01'
    assert str0013r1.operation_number == '316801512509080000001'
    assert str0013r1.balance == Decimal('100.50')
    assert str0013r1.vendor_timestamp == datetime(2025, 11, 20, 15, 30, 0, tzinfo=UTC)


def test_str0013r1_roundtrip() -> None:
    params = make_valid_str0013r1_params()
    str0013r1 = STR0013R1.model_validate(params)
    xml = str0013r1.to_xml()
    str0013r1_from_xml = STR0013R1.from_xml(xml)
    assert str0013r1 == str0013r1_from_xml


def test_str0013r1_from_xml_missing_required_fields() -> None:
    xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/SPB/STR0013.xsd">
        <SISMSG>
            <STR0013R1>
                <CodMsg>STR0013R1</CodMsg>
            </STR0013R1>
        </SISMSG>
    </DOC>
    """

    with pytest.raises(ValidationError) as exc:
        STR0013R1.from_xml(xml)
    missing_fields = extract_missing_fields(exc.value)
    assert missing_fields == {
        'system_domain',
        'to_ispb',
        'vendor_timestamp',
        'settlement_date',
        'operation_number',
        'institution_control_number',
        'balance',
        'from_ispb',
        'institution_ispb',
    }
