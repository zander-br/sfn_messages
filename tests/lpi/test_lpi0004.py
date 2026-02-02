from datetime import date, datetime
from decimal import Decimal
from typing import Any

import pytest
from pydantic import ValidationError

from sfn_messages.core.types import StrSettlementStatus
from sfn_messages.lpi.lpi0004 import LPI0004, LPI0004E, LPI0004R1
from tests.conftest import extract_missing_fields, normalize_xml


def make_valid_lpi0004_params() -> dict[str, Any]:
    return {
        'from_ispb': '31680151',
        'to_ispb': '00038166',
        'system_domain': 'SPB01',
        'operation_number': '31680151250908000000001',
        'message_code': 'LPI0004',
        'pspi_control_number': '123',
        'pspi_ispb': '31680153',
        'amount': 223.50,
        'settlement_date': '2026-02-02',
    }


def make_valid_lpi0004r1_params() -> dict[str, Any]:
    return {
        'from_ispb': '31680151',
        'to_ispb': '00038166',
        'system_domain': 'SPB01',
        'operation_number': '31680151250908000000001',
        'message_code': 'LPI0004R1',
        'pspi_control_number': '123',
        'pspi_ispb': '31680151',
        'str_control_number': 'STR20250101000000001',
        'str_settlement_status': 'EFFECTIVE',
        'settlement_timestamp': '2026-02-02T11:11:11',
        'settlement_date': '2026-02-02',
    }


def make_valid_lpi0004e_params(*, general_error: bool = False) -> dict[str, Any]:
    lpi0004e = {
        'from_ispb': '31680151',
        'to_ispb': '00038166',
        'system_domain': 'SPB01',
        'operation_number': '31680151250908000000001',
        'message_code': 'LPI0004E',
        'pspi_control_number': '123',
        'pspi_ispb': '31680153',
        'amount': 223.50,
        'settlement_date': '2026-02-02',
    }

    if general_error:
        lpi0004e['general_error_code'] = 'EGEN0050'
    else:
        lpi0004e['pspi_ispb_error_code'] = 'EGEN0051'

    return lpi0004e


def test_lpi0004_valid_model() -> None:
    params = make_valid_lpi0004_params()
    lpi0004 = LPI0004.model_validate(params)

    assert isinstance(lpi0004, LPI0004)
    assert lpi0004.message_code == 'LPI0004'
    assert lpi0004.pspi_control_number == '123'
    assert lpi0004.pspi_ispb == '31680153'
    assert lpi0004.amount == Decimal('223.50')
    assert lpi0004.settlement_date == date(2026, 2, 2)


def test_lpi0004r1_valid_model() -> None:
    params = make_valid_lpi0004r1_params()
    lpi0004r1 = LPI0004R1.model_validate(params)

    assert isinstance(lpi0004r1, LPI0004R1)
    assert lpi0004r1.message_code == 'LPI0004R1'
    assert lpi0004r1.pspi_control_number == '123'
    assert lpi0004r1.pspi_ispb == '31680151'
    assert lpi0004r1.str_control_number == 'STR20250101000000001'
    assert lpi0004r1.str_settlement_status == StrSettlementStatus.EFFECTIVE
    assert lpi0004r1.settlement_timestamp == datetime(2026, 2, 2, 11, 11, 11)
    assert lpi0004r1.settlement_date == date(2026, 2, 2)


def test_lpi0004e_general_error_valid_model() -> None:
    params = make_valid_lpi0004e_params(general_error=True)
    lpi0004e = LPI0004E.model_validate(params)

    assert isinstance(lpi0004e, LPI0004E)
    assert lpi0004e.message_code == 'LPI0004E'
    assert lpi0004e.pspi_control_number == '123'
    assert lpi0004e.pspi_ispb == '31680153'
    assert lpi0004e.amount == Decimal('223.50')
    assert lpi0004e.settlement_date == date(2026, 2, 2)
    assert lpi0004e.general_error_code == 'EGEN0050'


def test_lpi0004e_tag_error_valid_model() -> None:
    params = make_valid_lpi0004e_params()
    lpi0004e = LPI0004E.model_validate(params)

    assert isinstance(lpi0004e, LPI0004E)
    assert lpi0004e.message_code == 'LPI0004E'
    assert lpi0004e.pspi_control_number == '123'
    assert lpi0004e.pspi_ispb == '31680153'
    assert lpi0004e.amount == Decimal('223.50')
    assert lpi0004e.settlement_date == date(2026, 2, 2)
    assert lpi0004e.pspi_ispb_error_code == 'EGEN0051'


def test_lpi0004_missing_required_fields() -> None:
    with pytest.raises(ValidationError) as exc:
        LPI0004.model_validate({})

    missing_fields = extract_missing_fields(exc.value)
    assert missing_fields == {
        'from_ispb',
        'to_ispb',
        'system_domain',
        'operation_number',
        'pspi_control_number',
        'pspi_ispb',
        'amount',
        'settlement_date',
    }


def test_lpi0004r1_missing_required_fields() -> None:
    with pytest.raises(ValidationError) as exc:
        LPI0004R1.model_validate({})

    missing_fields = extract_missing_fields(exc.value)
    assert missing_fields == {
        'from_ispb',
        'to_ispb',
        'system_domain',
        'operation_number',
        'pspi_control_number',
        'pspi_ispb',
        'str_control_number',
        'settlement_timestamp',
        'settlement_date',
    }


def test_lpi0004_to_xml() -> None:
    params = make_valid_lpi0004_params()
    lpi0004 = LPI0004.model_validate(params)

    xml = lpi0004.to_xml()

    expected_xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/SPB/LPI0004.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>31680151250908000000001</NUOp>
        </BCMSG>
        <SISMSG>
            <LPI0004>
                <CodMsg>LPI0004</CodMsg>
                <NumCtrlPSPI>123</NumCtrlPSPI>
                <ISPBPSPI>31680153</ISPBPSPI>
                <VlrLanc>223.5</VlrLanc>
                <DtMovto>2026-02-02</DtMovto>
            </LPI0004>
        </SISMSG>
    </DOC>
    """
    assert normalize_xml(expected_xml) == normalize_xml(xml)


def test_lpi0004r1_to_xml() -> None:
    params = make_valid_lpi0004r1_params()
    lpi0004r1 = LPI0004R1.model_validate(params)

    xml = lpi0004r1.to_xml()

    expected_xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/SPB/LPI0004.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>31680151250908000000001</NUOp>
        </BCMSG>
        <SISMSG>
            <LPI0004R1>
                <CodMsg>LPI0004R1</CodMsg>
                <NumCtrlPSPI>123</NumCtrlPSPI>
                <ISPBPSPI>31680151</ISPBPSPI>
                <NumCtrlSTR>STR20250101000000001</NumCtrlSTR>
                <SitLancSTR>1</SitLancSTR>
                <DtHrSit>2026-02-02T11:11:11</DtHrSit>
                <DtMovto>2026-02-02</DtMovto>
            </LPI0004R1>
        </SISMSG>
    </DOC>
    """
    assert normalize_xml(expected_xml) == normalize_xml(xml)


def test_lpi0004e_general_error_to_xml() -> None:
    params = make_valid_lpi0004e_params(general_error=True)
    lpi0004e = LPI0004E.model_validate(params)

    xml = lpi0004e.to_xml()

    expected_xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/SPB/LPI0004E.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>31680151250908000000001</NUOp>
        </BCMSG>
        <SISMSG>
            <LPI0004 CodErro="EGEN0050">
                <CodMsg>LPI0004E</CodMsg>
                <NumCtrlPSPI>123</NumCtrlPSPI>
                <ISPBPSPI>31680153</ISPBPSPI>
                <VlrLanc>223.5</VlrLanc>
                <DtMovto>2026-02-02</DtMovto>
            </LPI0004>
        </SISMSG>
    </DOC>
    """
    assert normalize_xml(expected_xml) == normalize_xml(xml)


def test_lpi0004e_tag_error_to_xml() -> None:
    params = make_valid_lpi0004e_params()
    lpi0004e = LPI0004E.model_validate(params)

    xml = lpi0004e.to_xml()

    expected_xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/SPB/LPI0004E.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>31680151250908000000001</NUOp>
        </BCMSG>
        <SISMSG>
            <LPI0004>
                <CodMsg>LPI0004E</CodMsg>
                <NumCtrlPSPI>123</NumCtrlPSPI>
                <ISPBPSPI CodErro="EGEN0051">31680153</ISPBPSPI>
                <VlrLanc>223.5</VlrLanc>
                <DtMovto>2026-02-02</DtMovto>
            </LPI0004>
        </SISMSG>
    </DOC>
    """
    assert normalize_xml(expected_xml) == normalize_xml(xml)


def test_lpi0004_from_xml() -> None:
    xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/SPB/LPI0004.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>31680151250908000000001</NUOp>
        </BCMSG>
        <SISMSG>
            <LPI0004>
                <CodMsg>LPI0004</CodMsg>
                <NumCtrlPSPI>123</NumCtrlPSPI>
                <ISPBPSPI>31680153</ISPBPSPI>
                <VlrLanc>223.5</VlrLanc>
                <DtMovto>2026-02-02</DtMovto>
            </LPI0004>
        </SISMSG>
    </DOC>
    """

    lpi0004 = LPI0004.from_xml(xml)

    assert isinstance(lpi0004, LPI0004)
    assert lpi0004.message_code == 'LPI0004'
    assert lpi0004.pspi_control_number == '123'
    assert lpi0004.pspi_ispb == '31680153'
    assert lpi0004.amount == Decimal('223.50')
    assert lpi0004.settlement_date == date(2026, 2, 2)


def test_ltr0004r1_from_xml() -> None:
    xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/SPB/LPI0004.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>31680151250908000000001</NUOp>
        </BCMSG>
        <SISMSG>
            <LPI0004R1>
                <CodMsg>LPI0004R1</CodMsg>
                <NumCtrlPSPI>123</NumCtrlPSPI>
                <ISPBPSPI>31680151</ISPBPSPI>
                <NumCtrlSTR>STR20250101000000001</NumCtrlSTR>
                <SitLancSTR>1</SitLancSTR>
                <DtHrSit>2026-02-02T11:11:11</DtHrSit>
                <DtMovto>2026-02-02</DtMovto>
            </LPI0004R1>
        </SISMSG>
    </DOC>
    """

    lpi0004r1 = LPI0004R1.from_xml(xml)

    assert isinstance(lpi0004r1, LPI0004R1)
    assert lpi0004r1.message_code == 'LPI0004R1'
    assert lpi0004r1.pspi_control_number == '123'
    assert lpi0004r1.pspi_ispb == '31680151'
    assert lpi0004r1.str_control_number == 'STR20250101000000001'
    assert lpi0004r1.str_settlement_status == StrSettlementStatus.EFFECTIVE
    assert lpi0004r1.settlement_timestamp == datetime(2026, 2, 2, 11, 11, 11)
    assert lpi0004r1.settlement_date == date(2026, 2, 2)


def test_ltr0004e_general_error_from_xml() -> None:
    xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/SPB/LPI0004E.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>31680151250908000000001</NUOp>
        </BCMSG>
        <SISMSG>
            <LPI0004 CodErro="EGEN0050">
                <CodMsg>LPI0004E</CodMsg>
                <NumCtrlPSPI>123</NumCtrlPSPI>
                <ISPBPSPI>31680153</ISPBPSPI>
                <VlrLanc>223.5</VlrLanc>
                <DtMovto>2026-02-02</DtMovto>
            </LPI0004>
        </SISMSG>
    </DOC>
    """

    lpi0004e = LPI0004E.from_xml(xml)

    assert isinstance(lpi0004e, LPI0004E)
    assert lpi0004e.message_code == 'LPI0004E'
    assert lpi0004e.pspi_control_number == '123'
    assert lpi0004e.pspi_ispb == '31680153'
    assert lpi0004e.amount == Decimal('223.50')
    assert lpi0004e.settlement_date == date(2026, 2, 2)
    assert lpi0004e.general_error_code == 'EGEN0050'


def test_ltr0004e_tag_error_from_xml() -> None:
    xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/SPB/LPI0004E.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>31680151250908000000001</NUOp>
        </BCMSG>
        <SISMSG>
            <LPI0004>
                <CodMsg>LPI0004E</CodMsg>
                <NumCtrlPSPI>123</NumCtrlPSPI>
                <ISPBPSPI CodErro="EGEN0051">31680153</ISPBPSPI>
                <VlrLanc>223.5</VlrLanc>
                <DtMovto>2026-02-02</DtMovto>
            </LPI0004>
        </SISMSG>
    </DOC>
    """

    lpi0004e = LPI0004E.from_xml(xml)

    assert isinstance(lpi0004e, LPI0004E)
    assert lpi0004e.message_code == 'LPI0004E'
    assert lpi0004e.pspi_control_number == '123'
    assert lpi0004e.pspi_ispb == '31680153'
    assert lpi0004e.amount == Decimal('223.5')
    assert lpi0004e.settlement_date == date(2026, 2, 2)
    assert lpi0004e.pspi_ispb_error_code == 'EGEN0051'


def test_lpi0004_roundtrip() -> None:
    params = make_valid_lpi0004_params()

    lpi0004 = LPI0004.model_validate(params)
    xml = lpi0004.to_xml()
    lpi0004_from_xml = LPI0004.from_xml(xml)

    assert lpi0004 == lpi0004_from_xml


def test_lpi0004r1_roundtrip() -> None:
    params = make_valid_lpi0004r1_params()

    lpi0004r1 = LPI0004R1.model_validate(params)
    xml = lpi0004r1.to_xml()
    lpi0004r1_from_xml = LPI0004R1.from_xml(xml)

    assert lpi0004r1 == lpi0004r1_from_xml
