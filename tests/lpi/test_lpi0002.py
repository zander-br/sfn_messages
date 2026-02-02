from datetime import date, datetime
from decimal import Decimal
from typing import Any

import pytest
from pydantic import ValidationError

from sfn_messages.core.types import StrSettlementStatus
from sfn_messages.lpi.lpi0002 import LPI0002, LPI0002E, LPI0002R1
from tests.conftest import extract_missing_fields, normalize_xml


def make_valid_lpi0002_params() -> dict[str, Any]:
    return {
        'from_ispb': '31680151',
        'to_ispb': '00038166',
        'system_domain': 'SPB01',
        'operation_number': '31680151250908000000001',
        'message_code': 'LPI0002',
        'ieme_control_number': '123',
        'ieme_ispb': '31680151',
        'amount': 123.0,
        'settlement_date': '2026-01-30',
    }


def make_valid_lpi0002r1_params() -> dict[str, Any]:
    return {
        'from_ispb': '31680151',
        'to_ispb': '00038166',
        'system_domain': 'SPB01',
        'operation_number': '31680151250908000000001',
        'message_code': 'LPI0002R1',
        'ieme_control_number': '123',
        'ieme_ispb': '31680151',
        'str_control_number': 'STR20250101000000001',
        'str_settlement_status': 'EFFECTIVE',
        'settlement_timestamp': '2026-01-30T17:40:12',
        'settlement_date': '2026-01-30',
    }


def make_valid_lpi0002e_params(*, general_error: bool = False) -> dict[str, Any]:
    lpi0002e = {
        'from_ispb': '31680151',
        'to_ispb': '00038166',
        'system_domain': 'SPB01',
        'operation_number': '31680151250908000000001',
        'message_code': 'LPI0002E',
        'ieme_control_number': '123',
        'ieme_ispb': '31680151',
        'amount': 123.0,
        'settlement_date': '2026-01-30',
    }

    if general_error:
        lpi0002e['general_error_code'] = 'EGEN0050'
    else:
        lpi0002e['ieme_ispb_error_code'] = 'EGEN0051'

    return lpi0002e


def test_lpi0002_valid_model() -> None:
    params = make_valid_lpi0002_params()
    lpi0002 = LPI0002.model_validate(params)

    assert isinstance(lpi0002, LPI0002)
    assert lpi0002.message_code == 'LPI0002'
    assert lpi0002.ieme_control_number == '123'
    assert lpi0002.ieme_ispb == '31680151'
    assert lpi0002.amount == Decimal('123.0')
    assert lpi0002.settlement_date == date(2026, 1, 30)


def test_lpi0002r1_valid_model() -> None:
    params = make_valid_lpi0002r1_params()
    lpi0002r1 = LPI0002R1.model_validate(params)

    assert isinstance(lpi0002r1, LPI0002R1)
    assert lpi0002r1.message_code == 'LPI0002R1'
    assert lpi0002r1.ieme_control_number == '123'
    assert lpi0002r1.ieme_ispb == '31680151'
    assert lpi0002r1.str_control_number == 'STR20250101000000001'
    assert lpi0002r1.str_settlement_status == StrSettlementStatus.EFFECTIVE
    assert lpi0002r1.settlement_timestamp == datetime(2026, 1, 30, 17, 40, 12)
    assert lpi0002r1.settlement_date == date(2026, 1, 30)


def test_lpi0002e_general_error_valid_model() -> None:
    params = make_valid_lpi0002e_params(general_error=True)
    lpi0002e = LPI0002E.model_validate(params)

    assert isinstance(lpi0002e, LPI0002E)
    assert lpi0002e.message_code == 'LPI0002E'
    assert lpi0002e.ieme_control_number == '123'
    assert lpi0002e.ieme_ispb == '31680151'
    assert lpi0002e.amount == Decimal('123.0')
    assert lpi0002e.settlement_date == date(2026, 1, 30)
    assert lpi0002e.general_error_code == 'EGEN0050'


def test_lpi0002e_tag_error_valid_model() -> None:
    params = make_valid_lpi0002e_params()
    lpi0002e = LPI0002E.model_validate(params)

    assert isinstance(lpi0002e, LPI0002E)
    assert lpi0002e.message_code == 'LPI0002E'
    assert lpi0002e.ieme_control_number == '123'
    assert lpi0002e.ieme_ispb == '31680151'
    assert lpi0002e.amount == Decimal('123.0')
    assert lpi0002e.settlement_date == date(2026, 1, 30)
    assert lpi0002e.ieme_ispb_error_code == 'EGEN0051'


def test_lpi0002_missing_required_fields() -> None:
    with pytest.raises(ValidationError) as exc:
        LPI0002.model_validate({})

    missing_fields = extract_missing_fields(exc.value)
    assert missing_fields == {
        'from_ispb',
        'to_ispb',
        'system_domain',
        'operation_number',
        'ieme_control_number',
        'amount',
        'settlement_date',
    }


def test_lpi0002r1_missing_required_fields() -> None:
    with pytest.raises(ValidationError) as exc:
        LPI0002R1.model_validate({})

    missing_fields = extract_missing_fields(exc.value)
    assert missing_fields == {
        'from_ispb',
        'to_ispb',
        'system_domain',
        'operation_number',
        'ieme_control_number',
        'str_control_number',
        'settlement_timestamp',
        'settlement_date',
    }


def test_lpi0002_to_xml() -> None:
    params = make_valid_lpi0002_params()
    lpi0002 = LPI0002.model_validate(params)

    xml = lpi0002.to_xml()

    expected_xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/SPB/LPI0002.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>31680151250908000000001</NUOp>
        </BCMSG>
        <SISMSG>
            <LPI0002>
                <CodMsg>LPI0002</CodMsg>
                <NumCtrlIEME>123</NumCtrlIEME>
                <ISPBIEME>31680151</ISPBIEME>
                <VlrLanc>123.0</VlrLanc>
                <DtMovto>2026-01-30</DtMovto>
            </LPI0002>
        </SISMSG>
    </DOC>
    """
    assert normalize_xml(expected_xml) == normalize_xml(xml)


def test_lpi0002r1_to_xml() -> None:
    params = make_valid_lpi0002r1_params()
    lpi0002r1 = LPI0002R1.model_validate(params)

    xml = lpi0002r1.to_xml()

    expected_xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/SPB/LPI0002.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>31680151250908000000001</NUOp>
        </BCMSG>
        <SISMSG>
            <LPI0002R1>
                <CodMsg>LPI0002R1</CodMsg>
                <NumCtrlIEME>123</NumCtrlIEME>
                <ISPBIEME>31680151</ISPBIEME>
                <NumCtrlSTR>STR20250101000000001</NumCtrlSTR>
                <SitLancSTR>1</SitLancSTR>
                <DtHrSit>2026-01-30T17:40:12</DtHrSit>
                <DtMovto>2026-01-30</DtMovto>
            </LPI0002R1>
        </SISMSG>
    </DOC>
    """
    assert normalize_xml(expected_xml) == normalize_xml(xml)


def test_lpi0002e_general_error_to_xml() -> None:
    params = make_valid_lpi0002e_params(general_error=True)
    lpi0002e = LPI0002E.model_validate(params)

    xml = lpi0002e.to_xml()

    expected_xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/SPB/LPI0002E.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>31680151250908000000001</NUOp>
        </BCMSG>
        <SISMSG>
            <LPI0002 CodErro="EGEN0050">
                <CodMsg>LPI0002E</CodMsg>
                <NumCtrlIEME>123</NumCtrlIEME>
                <ISPBIEME>31680151</ISPBIEME>
                <VlrLanc>123.0</VlrLanc>
                <DtMovto>2026-01-30</DtMovto>
            </LPI0002>
        </SISMSG>
    </DOC>
    """
    assert normalize_xml(expected_xml) == normalize_xml(xml)


def test_lpi0002e_tag_error_to_xml() -> None:
    params = make_valid_lpi0002e_params()
    lpi0002e = LPI0002E.model_validate(params)

    xml = lpi0002e.to_xml()

    expected_xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/SPB/LPI0002E.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>31680151250908000000001</NUOp>
        </BCMSG>
        <SISMSG>
            <LPI0002>
                <CodMsg>LPI0002E</CodMsg>
                <NumCtrlIEME>123</NumCtrlIEME>
                <ISPBIEME CodErro="EGEN0051">31680151</ISPBIEME>
                <VlrLanc>123.0</VlrLanc>
                <DtMovto>2026-01-30</DtMovto>
            </LPI0002>
        </SISMSG>
    </DOC>
    """
    assert normalize_xml(expected_xml) == normalize_xml(xml)


def test_lpi0002_from_xml() -> None:
    xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/SPB/LPI0002.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>31680151250908000000001</NUOp>
        </BCMSG>
        <SISMSG>
            <LPI0002>
                <CodMsg>LPI0002</CodMsg>
                <NumCtrlIEME>123</NumCtrlIEME>
                <ISPBIEME>31680151</ISPBIEME>
                <VlrLanc>123.0</VlrLanc>
                <DtMovto>2026-01-30</DtMovto>
            </LPI0002>
        </SISMSG>
    </DOC>
    """

    lpi0002 = LPI0002.from_xml(xml)

    assert isinstance(lpi0002, LPI0002)
    assert lpi0002.message_code == 'LPI0002'
    assert lpi0002.ieme_control_number == '123'
    assert lpi0002.ieme_ispb == '31680151'
    assert lpi0002.amount == Decimal('123.0')
    assert lpi0002.settlement_date == date(2026, 1, 30)


def test_ltr0002r1_from_xml() -> None:
    xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/SPB/LPI0002.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>31680151250908000000001</NUOp>
        </BCMSG>
        <SISMSG>
            <LPI0002R1>
                <CodMsg>LPI0002R1</CodMsg>
                <NumCtrlIEME>123</NumCtrlIEME>
                <ISPBIEME>31680151</ISPBIEME>
                <NumCtrlSTR>STR20250101000000001</NumCtrlSTR>
                <SitLancSTR>1</SitLancSTR>
                <DtHrSit>2026-01-30T17:40:12</DtHrSit>
                <DtMovto>2026-01-30</DtMovto>
            </LPI0002R1>
        </SISMSG>
    </DOC>
    """

    lpi0002r1 = LPI0002R1.from_xml(xml)

    assert isinstance(lpi0002r1, LPI0002R1)
    assert lpi0002r1.message_code == 'LPI0002R1'
    assert lpi0002r1.ieme_control_number == '123'
    assert lpi0002r1.ieme_ispb == '31680151'
    assert lpi0002r1.str_control_number == 'STR20250101000000001'
    assert lpi0002r1.str_settlement_status == StrSettlementStatus.EFFECTIVE
    assert lpi0002r1.settlement_timestamp == datetime(2026, 1, 30, 17, 40, 12)
    assert lpi0002r1.settlement_date == date(2026, 1, 30)


def test_ltr0002e_general_error_from_xml() -> None:
    xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/SPB/LPI0002E.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>31680151250908000000001</NUOp>
        </BCMSG>
        <SISMSG>
            <LPI0002 CodErro="EGEN0050">
                <CodMsg>LPI0002E</CodMsg>
                <NumCtrlIEME>123</NumCtrlIEME>
                <ISPBIEME>31680151</ISPBIEME>
                <VlrLanc>123.0</VlrLanc>
                <DtMovto>2026-01-30</DtMovto>
            </LPI0002>
        </SISMSG>
    </DOC>
    """

    lpi0002e = LPI0002E.from_xml(xml)

    assert isinstance(lpi0002e, LPI0002E)
    assert lpi0002e.message_code == 'LPI0002E'
    assert lpi0002e.ieme_control_number == '123'
    assert lpi0002e.ieme_ispb == '31680151'
    assert lpi0002e.amount == Decimal('123.0')
    assert lpi0002e.settlement_date == date(2026, 1, 30)
    assert lpi0002e.general_error_code == 'EGEN0050'


def test_ltr0002e_tag_error_from_xml() -> None:
    xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/SPB/LPI0002E.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>31680151250908000000001</NUOp>
        </BCMSG>
        <SISMSG>
            <LPI0002>
                <CodMsg>LPI0002E</CodMsg>
                <NumCtrlIEME>123</NumCtrlIEME>
                <ISPBIEME CodErro="EGEN0051">31680151</ISPBIEME>
                <VlrLanc>123.0</VlrLanc>
                <DtMovto>2026-01-30</DtMovto>
            </LPI0002>
        </SISMSG>
    </DOC>
    """

    lpi0002e = LPI0002E.from_xml(xml)

    assert isinstance(lpi0002e, LPI0002E)
    assert lpi0002e.message_code == 'LPI0002E'
    assert lpi0002e.ieme_control_number == '123'
    assert lpi0002e.ieme_ispb == '31680151'
    assert lpi0002e.amount == Decimal('123.0')
    assert lpi0002e.settlement_date == date(2026, 1, 30)
    assert lpi0002e.ieme_ispb_error_code == 'EGEN0051'


def test_lpi0002_roundtrip() -> None:
    params = make_valid_lpi0002_params()

    lpi0002 = LPI0002.model_validate(params)
    xml = lpi0002.to_xml()
    lpi0002_from_xml = LPI0002.from_xml(xml)

    assert lpi0002 == lpi0002_from_xml


def test_lpi0002r1_roundtrip() -> None:
    params = make_valid_lpi0002r1_params()

    lpi0002r1 = LPI0002R1.model_validate(params)
    xml = lpi0002r1.to_xml()
    lpi0002r1_from_xml = LPI0002R1.from_xml(xml)

    assert lpi0002r1 == lpi0002r1_from_xml
