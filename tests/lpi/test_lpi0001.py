from datetime import date, datetime
from decimal import Decimal
from typing import Any

import pytest
from pydantic import ValidationError

from sfn_messages.core.types import StrSettlementStatus
from sfn_messages.lpi.lpi0001 import LPI0001, LPI0001E, LPI0001R1, LPI0001R2
from tests.conftest import extract_missing_fields, normalize_xml


def make_valid_lpi0001_params() -> dict[str, Any]:
    return {
        'from_ispb': '31680151',
        'to_ispb': '00038166',
        'system_domain': 'SPB01',
        'operation_number': '31680151250908000000001',
        'message_code': 'LPI0001',
        'institution_control_number': '123',
        'institution_ispb': '31680151',
        'pspi_ispb': '31680153',
        'amount': 123.0,
        'settlement_date': '2026-01-30',
    }


def make_valid_lpi0001r1_params() -> dict[str, Any]:
    return {
        'from_ispb': '31680151',
        'to_ispb': '00038166',
        'system_domain': 'SPB01',
        'operation_number': '31680151250908000000001',
        'message_code': 'LPI0001R1',
        'institution_control_number': '123',
        'institution_ispb': '31680151',
        'str_control_number': 'STR20250101000000001',
        'str_settlement_status': 'EFFECTIVE',
        'settlement_timestamp': '2026-01-30T17:40:12',
        'settlement_date': '2026-01-30',
    }


def make_valid_lpi0001r2_params() -> dict[str, Any]:
    return {
        'from_ispb': '31680151',
        'to_ispb': '00038166',
        'system_domain': 'SPB01',
        'operation_number': '31680151250908000000001',
        'message_code': 'LPI0001R2',
        'str_control_number': 'STR20250101000000001',
        'vendor_timestamp': '2026-01-30T17:40:12',
        'institution_ispb': '31680151',
        'pspi_ispb': '31680153',
        'amount': 123.0,
        'settlement_date': '2026-01-30',
    }


def make_valid_lpi0001e_params(*, general_error: bool = False) -> dict[str, Any]:
    lpi0001e = {
        'from_ispb': '31680151',
        'to_ispb': '00038166',
        'system_domain': 'SPB01',
        'operation_number': '31680151250908000000001',
        'message_code': 'LPI0001E',
        'institution_control_number': '123',
        'institution_ispb': '31680151',
        'pspi_ispb': '31680153',
        'amount': 123.0,
        'settlement_date': '2026-01-30',
    }

    if general_error:
        lpi0001e['general_error_code'] = 'EGEN0050'
    else:
        lpi0001e['pspi_ispb_error_code'] = 'EGEN0051'

    return lpi0001e


def test_lpi0001_valid_model() -> None:
    params = make_valid_lpi0001_params()
    lpi0001 = LPI0001.model_validate(params)

    assert isinstance(lpi0001, LPI0001)
    assert lpi0001.message_code == 'LPI0001'
    assert lpi0001.institution_control_number == '123'
    assert lpi0001.institution_ispb == '31680151'
    assert lpi0001.pspi_ispb == '31680153'
    assert lpi0001.amount == Decimal('123.0')
    assert lpi0001.settlement_date == date(2026, 1, 30)


def test_lpi0001r1_valid_model() -> None:
    params = make_valid_lpi0001r1_params()
    lpi0001r1 = LPI0001R1.model_validate(params)

    assert isinstance(lpi0001r1, LPI0001R1)
    assert lpi0001r1.message_code == 'LPI0001R1'
    assert lpi0001r1.institution_control_number == '123'
    assert lpi0001r1.institution_ispb == '31680151'
    assert lpi0001r1.str_control_number == 'STR20250101000000001'
    assert lpi0001r1.str_settlement_status == StrSettlementStatus.EFFECTIVE
    assert lpi0001r1.settlement_timestamp == datetime(2026, 1, 30, 17, 40, 12)
    assert lpi0001r1.settlement_date == date(2026, 1, 30)


def test_lpi0001r2_valid_model() -> None:
    params = make_valid_lpi0001r2_params()
    lpi0001r2 = LPI0001R2.model_validate(params)

    assert isinstance(lpi0001r2, LPI0001R2)
    assert lpi0001r2.message_code == 'LPI0001R2'
    assert lpi0001r2.str_control_number == 'STR20250101000000001'
    assert lpi0001r2.institution_ispb == '31680151'
    assert lpi0001r2.pspi_ispb == '31680153'
    assert lpi0001r2.amount == Decimal('123.0')
    assert lpi0001r2.settlement_date == date(2026, 1, 30)


def test_lpi0001e_general_error_valid_model() -> None:
    params = make_valid_lpi0001e_params(general_error=True)
    lpi0001e = LPI0001E.model_validate(params)

    assert isinstance(lpi0001e, LPI0001E)
    assert lpi0001e.message_code == 'LPI0001E'
    assert lpi0001e.institution_control_number == '123'
    assert lpi0001e.institution_ispb == '31680151'
    assert lpi0001e.pspi_ispb == '31680153'
    assert lpi0001e.amount == Decimal('123.0')
    assert lpi0001e.settlement_date == date(2026, 1, 30)
    assert lpi0001e.general_error_code == 'EGEN0050'


def test_lpi0001e_tag_error_valid_model() -> None:
    params = make_valid_lpi0001e_params()
    lpi0001e = LPI0001E.model_validate(params)

    assert isinstance(lpi0001e, LPI0001E)
    assert lpi0001e.message_code == 'LPI0001E'
    assert lpi0001e.institution_control_number == '123'
    assert lpi0001e.institution_ispb == '31680151'
    assert lpi0001e.pspi_ispb == '31680153'
    assert lpi0001e.amount == Decimal('123.0')
    assert lpi0001e.settlement_date == date(2026, 1, 30)
    assert lpi0001e.pspi_ispb_error_code == 'EGEN0051'


def test_lpi0001_missing_required_fields() -> None:
    with pytest.raises(ValidationError) as exc:
        LPI0001.model_validate({})

    missing_fields = extract_missing_fields(exc.value)
    assert missing_fields == {
        'from_ispb',
        'to_ispb',
        'system_domain',
        'operation_number',
        'institution_control_number',
        'institution_ispb',
        'pspi_ispb',
        'amount',
        'settlement_date',
    }


def test_lpi0001r1_missing_required_fields() -> None:
    with pytest.raises(ValidationError) as exc:
        LPI0001R1.model_validate({})

    missing_fields = extract_missing_fields(exc.value)
    assert missing_fields == {
        'from_ispb',
        'to_ispb',
        'system_domain',
        'operation_number',
        'institution_control_number',
        'institution_ispb',
        'str_control_number',
        'settlement_timestamp',
        'settlement_date',
    }


def test_lpi0001r2_missing_required_fields() -> None:
    with pytest.raises(ValidationError) as exc:
        LPI0001R2.model_validate({})

    missing_fields = extract_missing_fields(exc.value)
    assert missing_fields == {
        'from_ispb',
        'to_ispb',
        'system_domain',
        'operation_number',
        'str_control_number',
        'vendor_timestamp',
        'institution_ispb',
        'pspi_ispb',
        'amount',
        'settlement_date',
    }


def test_lpi0001_to_xml() -> None:
    params = make_valid_lpi0001_params()
    lpi0001 = LPI0001.model_validate(params)

    xml = lpi0001.to_xml()

    expected_xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/SPB/LPI0001.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>31680151250908000000001</NUOp>
        </BCMSG>
        <SISMSG>
            <LPI0001>
                <CodMsg>LPI0001</CodMsg>
                <NumCtrlIF>123</NumCtrlIF>
                <ISPBIF>31680151</ISPBIF>
                <ISPBPSPI>31680153</ISPBPSPI>
                <VlrLanc>123.0</VlrLanc>
                <DtMovto>2026-01-30</DtMovto>
            </LPI0001>
        </SISMSG>
    </DOC>
    """
    assert normalize_xml(expected_xml) == normalize_xml(xml)


def test_lpi0001r1_to_xml() -> None:
    params = make_valid_lpi0001r1_params()
    lpi0001r1 = LPI0001R1.model_validate(params)

    xml = lpi0001r1.to_xml()

    expected_xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/SPB/LPI0001.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>31680151250908000000001</NUOp>
        </BCMSG>
        <SISMSG>
            <LPI0001R1>
                <CodMsg>LPI0001R1</CodMsg>
                <NumCtrlIF>123</NumCtrlIF>
                <ISPBIF>31680151</ISPBIF>
                <NumCtrlSTR>STR20250101000000001</NumCtrlSTR>
                <SitLancSTR>1</SitLancSTR>
                <DtHrSit>2026-01-30T17:40:12</DtHrSit>
                <DtMovto>2026-01-30</DtMovto>
            </LPI0001R1>
        </SISMSG>
    </DOC>
    """
    assert normalize_xml(expected_xml) == normalize_xml(xml)


def test_lpi0001r2_to_xml() -> None:
    params = make_valid_lpi0001r2_params()
    lpi0001r2 = LPI0001R2.model_validate(params)

    xml = lpi0001r2.to_xml()

    expected_xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/SPB/LPI0001.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>31680151250908000000001</NUOp>
        </BCMSG>
        <SISMSG>
            <LPI0001R2>
                <CodMsg>LPI0001R2</CodMsg>
                <NumCtrlSTR>STR20250101000000001</NumCtrlSTR>
                <DtHrBC>2026-01-30T17:40:12</DtHrBC>
                <ISPBIF>31680151</ISPBIF>
                <ISPBPSPI>31680153</ISPBPSPI>
                <VlrLanc>123.0</VlrLanc>
                <DtMovto>2026-01-30</DtMovto>
            </LPI0001R2>
        </SISMSG>
    </DOC>
    """
    assert normalize_xml(expected_xml) == normalize_xml(xml)


def test_lpi0001e_general_error_to_xml() -> None:
    params = make_valid_lpi0001e_params(general_error=True)
    lpi0001e = LPI0001E.model_validate(params)

    xml = lpi0001e.to_xml()

    expected_xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/SPB/LPI0001E.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>31680151250908000000001</NUOp>
        </BCMSG>
        <SISMSG>
            <LPI0001 CodErro="EGEN0050">
                <CodMsg>LPI0001E</CodMsg>
                <NumCtrlIF>123</NumCtrlIF>
                <ISPBIF>31680151</ISPBIF>
                <ISPBPSPI>31680153</ISPBPSPI>
                <VlrLanc>123.0</VlrLanc>
                <DtMovto>2026-01-30</DtMovto>
            </LPI0001>
        </SISMSG>
    </DOC>
    """
    assert normalize_xml(expected_xml) == normalize_xml(xml)


def test_lpi0001e_tag_error_to_xml() -> None:
    params = make_valid_lpi0001e_params()
    lpi0001e = LPI0001E.model_validate(params)

    xml = lpi0001e.to_xml()

    expected_xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/SPB/LPI0001E.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>31680151250908000000001</NUOp>
        </BCMSG>
        <SISMSG>
            <LPI0001>
                <CodMsg>LPI0001E</CodMsg>
                <NumCtrlIF>123</NumCtrlIF>
                <ISPBIF>31680151</ISPBIF>
                <ISPBPSPI CodErro="EGEN0051">31680153</ISPBPSPI>
                <VlrLanc>123.0</VlrLanc>
                <DtMovto>2026-01-30</DtMovto>
            </LPI0001>
        </SISMSG>
    </DOC>
    """
    assert normalize_xml(expected_xml) == normalize_xml(xml)


def test_lpi0001_from_xml() -> None:
    xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/SPB/LPI0001.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>31680151250908000000001</NUOp>
        </BCMSG>
        <SISMSG>
            <LPI0001>
                <CodMsg>LPI0001</CodMsg>
                <NumCtrlIF>123</NumCtrlIF>
                <ISPBIF>31680151</ISPBIF>
                <ISPBPSPI>31680153</ISPBPSPI>
                <VlrLanc>123.0</VlrLanc>
                <DtMovto>2026-01-30</DtMovto>
            </LPI0001>
        </SISMSG>
    </DOC>
    """

    lpi0001 = LPI0001.from_xml(xml)

    assert isinstance(lpi0001, LPI0001)
    assert lpi0001.message_code == 'LPI0001'
    assert lpi0001.institution_control_number == '123'
    assert lpi0001.institution_ispb == '31680151'
    assert lpi0001.pspi_ispb == '31680153'
    assert lpi0001.amount == Decimal('123.0')
    assert lpi0001.settlement_date == date(2026, 1, 30)


def test_lpi0001r1_from_xml() -> None:
    xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/SPB/LPI0001.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>31680151250908000000001</NUOp>
        </BCMSG>
        <SISMSG>
            <LPI0001R1>
                <CodMsg>LPI0001R1</CodMsg>
                <NumCtrlIF>123</NumCtrlIF>
                <ISPBIF>31680151</ISPBIF>
                <NumCtrlSTR>STR20250101000000001</NumCtrlSTR>
                <SitLancSTR>1</SitLancSTR>
                <DtHrSit>2026-01-30T17:40:12</DtHrSit>
                <DtMovto>2026-01-30</DtMovto>
            </LPI0001R1>
        </SISMSG>
    </DOC>
    """

    lpi0001r1 = LPI0001R1.from_xml(xml)

    assert isinstance(lpi0001r1, LPI0001R1)
    assert lpi0001r1.message_code == 'LPI0001R1'
    assert lpi0001r1.institution_control_number == '123'
    assert lpi0001r1.institution_ispb == '31680151'
    assert lpi0001r1.str_control_number == 'STR20250101000000001'
    assert lpi0001r1.str_settlement_status == StrSettlementStatus.EFFECTIVE
    assert lpi0001r1.settlement_timestamp == datetime(2026, 1, 30, 17, 40, 12)
    assert lpi0001r1.settlement_date == date(2026, 1, 30)


def test_lpi0001r2_from_xml() -> None:
    xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/SPB/LPI0001.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>31680151250908000000001</NUOp>
        </BCMSG>
        <SISMSG>
            <LPI0001R2>
                <CodMsg>LPI0001R2</CodMsg>
                <NumCtrlSTR>STR20250101000000001</NumCtrlSTR>
                <DtHrBC>2026-01-30T17:40:12</DtHrBC>
                <ISPBIF>31680151</ISPBIF>
                <ISPBPSPI>31680153</ISPBPSPI>
                <VlrLanc>123.0</VlrLanc>
                <DtMovto>2026-01-30</DtMovto>
            </LPI0001R2>
        </SISMSG>
    </DOC>
    """

    lpi0001r2 = LPI0001R2.from_xml(xml)

    assert isinstance(lpi0001r2, LPI0001R2)
    assert lpi0001r2.message_code == 'LPI0001R2'
    assert lpi0001r2.str_control_number == 'STR20250101000000001'
    assert lpi0001r2.institution_ispb == '31680151'
    assert lpi0001r2.pspi_ispb == '31680153'
    assert lpi0001r2.amount == Decimal('123.0')
    assert lpi0001r2.settlement_date == date(2026, 1, 30)


def test_lpi0001e_general_error_from_xml() -> None:
    xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/SPB/LPI0001E.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>31680151250908000000001</NUOp>
        </BCMSG>
        <SISMSG>
            <LPI0001 CodErro="EGEN0050">
                <CodMsg>LPI0001E</CodMsg>
                <NumCtrlIF>123</NumCtrlIF>
                <ISPBIF>31680151</ISPBIF>
                <ISPBPSPI>31680153</ISPBPSPI>
                <VlrLanc>123.0</VlrLanc>
                <DtMovto>2026-01-30</DtMovto>
            </LPI0001>
        </SISMSG>
    </DOC>
    """

    lpi0001e = LPI0001E.from_xml(xml)

    assert isinstance(lpi0001e, LPI0001E)
    assert lpi0001e.message_code == 'LPI0001E'
    assert lpi0001e.institution_control_number == '123'
    assert lpi0001e.institution_ispb == '31680151'
    assert lpi0001e.pspi_ispb == '31680153'
    assert lpi0001e.amount == Decimal('123.0')
    assert lpi0001e.settlement_date == date(2026, 1, 30)
    assert lpi0001e.general_error_code == 'EGEN0050'


def test_lpi0001e_tag_error_from_xml() -> None:
    xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/SPB/LPI0001E.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>31680151250908000000001</NUOp>
        </BCMSG>
        <SISMSG>
            <LPI0001>
                <CodMsg>LPI0001E</CodMsg>
                <NumCtrlIF>123</NumCtrlIF>
                <ISPBIF>31680151</ISPBIF>
                <ISPBPSPI CodErro="EGEN0051">31680153</ISPBPSPI>
                <VlrLanc>123.0</VlrLanc>
                <DtMovto>2026-01-30</DtMovto>
            </LPI0001>
        </SISMSG>
    </DOC>
    """

    lpi0001e = LPI0001E.from_xml(xml)

    assert isinstance(lpi0001e, LPI0001E)
    assert lpi0001e.message_code == 'LPI0001E'
    assert lpi0001e.institution_control_number == '123'
    assert lpi0001e.institution_ispb == '31680151'
    assert lpi0001e.pspi_ispb == '31680153'
    assert lpi0001e.amount == Decimal('123.0')
    assert lpi0001e.settlement_date == date(2026, 1, 30)
    assert lpi0001e.pspi_ispb_error_code == 'EGEN0051'


def test_lpi0001_roundtrip() -> None:
    params = make_valid_lpi0001_params()

    lpi0001 = LPI0001.model_validate(params)
    xml = lpi0001.to_xml()
    lpi0001_from_xml = LPI0001.from_xml(xml)

    assert lpi0001 == lpi0001_from_xml


def test_lpi0001r1_roundtrip() -> None:
    params = make_valid_lpi0001r1_params()

    lpi0001r1 = LPI0001R1.model_validate(params)
    xml = lpi0001r1.to_xml()
    lpi0001r1_from_xml = LPI0001R1.from_xml(xml)

    assert lpi0001r1 == lpi0001r1_from_xml


def test_lpi0001r2_roundtrip() -> None:
    params = make_valid_lpi0001r2_params()

    lpi0001r2 = LPI0001R2.model_validate(params)
    xml = lpi0001r2.to_xml()
    lpi0001r2_from_xml = LPI0001R2.from_xml(xml)

    assert lpi0001r2 == lpi0001r2_from_xml
