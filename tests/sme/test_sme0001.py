from datetime import date, datetime
from decimal import Decimal
from typing import Any

import pytest
from pydantic import ValidationError

from sfn_messages.core.types import StrSettlementStatus
from sfn_messages.sme.sme0001 import SME0001, SME0001E, SME0001R1, SME0001R2
from tests.conftest import extract_missing_fields, normalize_xml


def make_valid_sme0001_params() -> dict[str, Any]:
    return {
        'from_ispb': '31680151',
        'to_ispb': '00038166',
        'system_domain': 'SPB01',
        'operation_number': '31680151250908000000001',
        'message_code': 'SME0001',
        'institution_control_number': '123',
        'institution_ispb': '31680151',
        'ieme_ispb': '31680153',
        'amount': 120.00,
        'settlement_date': '2025-12-03',
    }


def make_valid_sme0001r1_params() -> dict[str, Any]:
    return {
        'from_ispb': '31680151',
        'to_ispb': '00038166',
        'system_domain': 'SPB01',
        'operation_number': '31680151250908000000001',
        'message_code': 'SME0001R1',
        'institution_control_number': '123',
        'institution_ispb': '31680151',
        'str_control_number': 'STR20250101000000001',
        'str_settlement_status': 'EFFECTIVE',
        'situation_timestamp': '2025-12-03T12:30:45',
        'settlement_date': '2025-12-03',
    }


def make_valid_sme0001r2_params() -> dict[str, Any]:
    return {
        'from_ispb': '31680151',
        'to_ispb': '00038166',
        'system_domain': 'SPB01',
        'operation_number': '31680151250908000000001',
        'message_code': 'SME0001R2',
        'str_control_number': 'STR20250101000000001',
        'vendor_timestamp': '2025-12-03T09:00:00',
        'institution_ispb': '31680151',
        'ieme_ispb': '31680153',
        'amount': 120.00,
        'settlement_date': '2025-12-03',
    }


def make_valid_sme0001e_params(*, general_error: bool = False) -> dict[str, Any]:
    sme0001e = {
        'from_ispb': '31680151',
        'to_ispb': '00038166',
        'system_domain': 'SPB01',
        'operation_number': '31680151250908000000001',
        'message_code': 'SME0001E',
        'institution_control_number': '123',
        'institution_ispb': '31680151',
        'ieme_ispb': '31680153',
        'amount': 120.00,
        'settlement_date': '2025-12-03',
    }

    if general_error:
        sme0001e['general_error_code'] = 'EGEN0050'
    else:
        sme0001e['ieme_ispb_error_code'] = 'EGEN0051'

    return sme0001e


def test_sme0001_valid_model() -> None:
    params = make_valid_sme0001_params()
    sme0001 = SME0001.model_validate(params)

    assert isinstance(sme0001, SME0001)
    assert sme0001.from_ispb == '31680151'
    assert sme0001.to_ispb == '00038166'
    assert sme0001.system_domain == 'SPB01'
    assert sme0001.operation_number == '31680151250908000000001'
    assert sme0001.message_code == 'SME0001'
    assert sme0001.institution_control_number == '123'
    assert sme0001.institution_ispb == '31680151'
    assert sme0001.ieme_ispb == '31680153'
    assert sme0001.amount == Decimal('120.00')
    assert sme0001.settlement_date == date(2025, 12, 3)


def test_sme0001r1_valid_model() -> None:
    params = make_valid_sme0001r1_params()
    sme0001r1 = SME0001R1.model_validate(params)

    assert isinstance(sme0001r1, SME0001R1)
    assert sme0001r1.from_ispb == '31680151'
    assert sme0001r1.to_ispb == '00038166'
    assert sme0001r1.system_domain == 'SPB01'
    assert sme0001r1.operation_number == '31680151250908000000001'
    assert sme0001r1.message_code == 'SME0001R1'
    assert sme0001r1.institution_control_number == '123'
    assert sme0001r1.institution_ispb == '31680151'
    assert sme0001r1.str_control_number == 'STR20250101000000001'
    assert sme0001r1.str_settlement_status == StrSettlementStatus.EFFECTIVE
    assert sme0001r1.settlement_date == date(2025, 12, 3)


def test_sme0001r2_valid_model() -> None:
    params = make_valid_sme0001r2_params()
    sme0001r2 = SME0001R2.model_validate(params)

    assert isinstance(sme0001r2, SME0001R2)
    assert sme0001r2.from_ispb == '31680151'
    assert sme0001r2.to_ispb == '00038166'
    assert sme0001r2.system_domain == 'SPB01'
    assert sme0001r2.operation_number == '31680151250908000000001'
    assert sme0001r2.message_code == 'SME0001R2'
    assert sme0001r2.str_control_number == 'STR20250101000000001'
    assert sme0001r2.vendor_timestamp == datetime(2025, 12, 3, 9, 0)
    assert sme0001r2.institution_ispb == '31680151'
    assert sme0001r2.ieme_ispb == '31680153'
    assert sme0001r2.amount == Decimal('120.00')
    assert sme0001r2.settlement_date == date(2025, 12, 3)


def test_sme0001e_general_error_valid_model() -> None:
    params = make_valid_sme0001e_params(general_error=True)
    sme0001e = SME0001E.model_validate(params)

    assert isinstance(sme0001e, SME0001E)
    assert sme0001e.from_ispb == '31680151'
    assert sme0001e.to_ispb == '00038166'
    assert sme0001e.system_domain == 'SPB01'
    assert sme0001e.operation_number == '31680151250908000000001'
    assert sme0001e.message_code == 'SME0001E'
    assert sme0001e.institution_control_number == '123'
    assert sme0001e.institution_ispb == '31680151'
    assert sme0001e.ieme_ispb == '31680153'
    assert sme0001e.amount == Decimal('120.00')
    assert sme0001e.settlement_date == date(2025, 12, 3)
    assert sme0001e.general_error_code == 'EGEN0050'


def test_sme0001e_tag_error_valid_model() -> None:
    params = make_valid_sme0001e_params()
    sme0001e = SME0001E.model_validate(params)

    assert isinstance(sme0001e, SME0001E)
    assert sme0001e.from_ispb == '31680151'
    assert sme0001e.to_ispb == '00038166'
    assert sme0001e.system_domain == 'SPB01'
    assert sme0001e.operation_number == '31680151250908000000001'
    assert sme0001e.message_code == 'SME0001E'
    assert sme0001e.institution_control_number == '123'
    assert sme0001e.institution_ispb == '31680151'
    assert sme0001e.ieme_ispb == '31680153'
    assert sme0001e.amount == Decimal('120.00')
    assert sme0001e.settlement_date == date(2025, 12, 3)
    assert sme0001e.ieme_ispb_error_code == 'EGEN0051'


def test_sme0001_missing_required_fields() -> None:
    with pytest.raises(ValidationError) as exc:
        SME0001.model_validate({})

    missing_fields = extract_missing_fields(exc.value)
    assert missing_fields == {
        'from_ispb',
        'to_ispb',
        'system_domain',
        'operation_number',
        'institution_control_number',
        'institution_ispb',
        'amount',
        'settlement_date',
    }


def test_sme0001r1_missing_required_fields() -> None:
    with pytest.raises(ValidationError) as exc:
        SME0001R1.model_validate({})

    missing_fields = extract_missing_fields(exc.value)
    assert missing_fields == {
        'from_ispb',
        'to_ispb',
        'system_domain',
        'operation_number',
        'institution_control_number',
        'institution_ispb',
        'str_control_number',
        'str_settlement_status',
        'situation_timestamp',
        'settlement_date',
    }


def test_sme0001r2_missing_required_fields() -> None:
    with pytest.raises(ValidationError) as exc:
        SME0001R2.model_validate({})

    missing_fields = extract_missing_fields(exc.value)
    assert missing_fields == {
        'from_ispb',
        'to_ispb',
        'system_domain',
        'operation_number',
        'str_control_number',
        'vendor_timestamp',
        'institution_ispb',
        'ieme_ispb',
        'amount',
        'settlement_date',
    }


def test_sme0001_to_xml() -> None:
    params = make_valid_sme0001_params()
    sme0001 = SME0001.model_validate(params)

    xml = sme0001.to_xml()

    expected_xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/SPB/SME0001.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>31680151250908000000001</NUOp>
        </BCMSG>
        <SISMSG>
            <SME0001>
                <CodMsg>SME0001</CodMsg>
                <NumCtrlIF>123</NumCtrlIF>
                <ISPBIF>31680151</ISPBIF>
                <ISPBIEME>31680153</ISPBIEME>
                <VlrLanc>120.0</VlrLanc>
                <DtMovto>2025-12-03</DtMovto>
            </SME0001>
        </SISMSG>
    </DOC>
    """
    assert normalize_xml(expected_xml) == normalize_xml(xml)


def test_sme0001r1_to_xml() -> None:
    params = make_valid_sme0001r1_params()
    sme0001r1 = SME0001R1.model_validate(params)

    xml = sme0001r1.to_xml()

    expected_xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/SPB/SME0001.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>31680151250908000000001</NUOp>
        </BCMSG>
        <SISMSG>
            <SME0001R1>
                <CodMsg>SME0001R1</CodMsg>
                <NumCtrlIF>123</NumCtrlIF>
                <ISPBIF>31680151</ISPBIF>
                <NumCtrlSTR>STR20250101000000001</NumCtrlSTR>
                <SitLancSTR>1</SitLancSTR>
                <DtHrSit>2025-12-03T12:30:45</DtHrSit>
                <DtMovto>2025-12-03</DtMovto>
            </SME0001R1>
        </SISMSG>
    </DOC>
    """
    assert normalize_xml(expected_xml) == normalize_xml(xml)


def test_sme0001r2_to_xml() -> None:
    params = make_valid_sme0001r2_params()
    sme0001r2 = SME0001R2.model_validate(params)

    xml = sme0001r2.to_xml()

    expected_xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/SPB/SME0001.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>31680151250908000000001</NUOp>
        </BCMSG>
        <SISMSG>
            <SME0001R2>
                <CodMsg>SME0001R2</CodMsg>
                <NumCtrlSTR>STR20250101000000001</NumCtrlSTR>
                <DtHrBC>2025-12-03T09:00:00</DtHrBC>
                <ISPBIF>31680151</ISPBIF>
                <ISPBIEME>31680153</ISPBIEME>
                <VlrLanc>120.0</VlrLanc>
                <DtMovto>2025-12-03</DtMovto>
            </SME0001R2>
        </SISMSG>
    </DOC>
    """
    assert normalize_xml(expected_xml) == normalize_xml(xml)


def test_sme0001e_general_error_to_xml() -> None:
    params = make_valid_sme0001e_params(general_error=True)
    sme0001e = SME0001E.model_validate(params)

    xml = sme0001e.to_xml()

    expected_xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/SPB/SME0001E.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>31680151250908000000001</NUOp>
        </BCMSG>
        <SISMSG>
            <SME0001 CodErro="EGEN0050">
                <CodMsg>SME0001E</CodMsg>
                <NumCtrlIF>123</NumCtrlIF>
                <ISPBIF>31680151</ISPBIF>
                <ISPBIEME>31680153</ISPBIEME>
                <VlrLanc>120.0</VlrLanc>
                <DtMovto>2025-12-03</DtMovto>
            </SME0001>
        </SISMSG>
    </DOC>
    """
    assert normalize_xml(expected_xml) == normalize_xml(xml)


def test_sme0001e_tag_error_to_xml() -> None:
    params = make_valid_sme0001e_params()
    sme0001e = SME0001E.model_validate(params)

    xml = sme0001e.to_xml()

    expected_xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/SPB/SME0001E.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>31680151250908000000001</NUOp>
        </BCMSG>
        <SISMSG>
            <SME0001>
                <CodMsg>SME0001E</CodMsg>
                <NumCtrlIF>123</NumCtrlIF>
                <ISPBIF>31680151</ISPBIF>
                <ISPBIEME CodErro="EGEN0051">31680153</ISPBIEME>
                <VlrLanc>120.0</VlrLanc>
                <DtMovto>2025-12-03</DtMovto>
            </SME0001>
        </SISMSG>
    </DOC>
    """
    assert normalize_xml(expected_xml) == normalize_xml(xml)


def test_sme0001_from_xml() -> None:
    xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/SPB/SME0001.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>31680151250908000000001</NUOp>
        </BCMSG>
        <SISMSG>
            <SME0001>
                <CodMsg>SME0001</CodMsg>
                <NumCtrlIF>123</NumCtrlIF>
                <ISPBIF>31680151</ISPBIF>
                <ISPBIEME>31680153</ISPBIEME>
                <VlrLanc>120.0</VlrLanc>
                <DtMovto>2025-12-03</DtMovto>
            </SME0001>
        </SISMSG>
    </DOC>
    """

    sme0001 = SME0001.from_xml(xml)

    assert isinstance(sme0001, SME0001)
    assert sme0001.from_ispb == '31680151'
    assert sme0001.to_ispb == '00038166'
    assert sme0001.system_domain == 'SPB01'
    assert sme0001.operation_number == '31680151250908000000001'
    assert sme0001.message_code == 'SME0001'
    assert sme0001.institution_control_number == '123'
    assert sme0001.institution_ispb == '31680151'
    assert sme0001.ieme_ispb == '31680153'
    assert sme0001.amount == Decimal('120.00')
    assert sme0001.settlement_date == date(2025, 12, 3)


def test_sme0001r1_from_xml() -> None:
    xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/SPB/SME0001.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>31680151250908000000001</NUOp>
        </BCMSG>
        <SISMSG>
            <SME0001R1>
                <CodMsg>SME0001R1</CodMsg>
                <NumCtrlIF>123</NumCtrlIF>
                <ISPBIF>31680151</ISPBIF>
                <NumCtrlSTR>STR20250101000000001</NumCtrlSTR>
                <SitLancSTR>1</SitLancSTR>
                <DtHrSit>2025-12-03T12:30:45</DtHrSit>
                <DtMovto>2025-12-03</DtMovto>
            </SME0001R1>
        </SISMSG>
    </DOC>
    """

    sme0001r1 = SME0001R1.from_xml(xml)

    assert isinstance(sme0001r1, SME0001R1)
    assert sme0001r1.from_ispb == '31680151'
    assert sme0001r1.to_ispb == '00038166'
    assert sme0001r1.system_domain == 'SPB01'
    assert sme0001r1.operation_number == '31680151250908000000001'
    assert sme0001r1.message_code == 'SME0001R1'
    assert sme0001r1.institution_control_number == '123'
    assert sme0001r1.institution_ispb == '31680151'
    assert sme0001r1.str_control_number == 'STR20250101000000001'
    assert sme0001r1.str_settlement_status == StrSettlementStatus.EFFECTIVE
    assert sme0001r1.settlement_date == date(2025, 12, 3)


def test_sme0001r2_from_xml() -> None:
    xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/SPB/SME0001.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>31680151250908000000001</NUOp>
        </BCMSG>
        <SISMSG>
            <SME0001R2>
                <CodMsg>SME0001R2</CodMsg>
                <NumCtrlSTR>STR20250101000000001</NumCtrlSTR>
                <DtHrBC>2025-12-03T09:00:00</DtHrBC>
                <ISPBIF>31680151</ISPBIF>
                <ISPBIEME>31680153</ISPBIEME>
                <VlrLanc>120.0</VlrLanc>
                <DtMovto>2025-12-03</DtMovto>
            </SME0001R2>
        </SISMSG>
    </DOC>
    """

    sme0001r2 = SME0001R2.from_xml(xml)

    assert isinstance(sme0001r2, SME0001R2)
    assert sme0001r2.from_ispb == '31680151'
    assert sme0001r2.to_ispb == '00038166'
    assert sme0001r2.system_domain == 'SPB01'
    assert sme0001r2.operation_number == '31680151250908000000001'
    assert sme0001r2.message_code == 'SME0001R2'
    assert sme0001r2.str_control_number == 'STR20250101000000001'
    assert sme0001r2.vendor_timestamp == datetime(2025, 12, 3, 9, 0)
    assert sme0001r2.institution_ispb == '31680151'
    assert sme0001r2.ieme_ispb == '31680153'
    assert sme0001r2.amount == Decimal('120.00')
    assert sme0001r2.settlement_date == date(2025, 12, 3)


def test_sme0001e_general_error_from_xml() -> None:
    xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/SPB/SME0001E.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>31680151250908000000001</NUOp>
        </BCMSG>
        <SISMSG>
            <SME0001 CodErro="EGEN0050">
                <CodMsg>SME0001E</CodMsg>
                <NumCtrlIF>123</NumCtrlIF>
                <ISPBIF>31680151</ISPBIF>
                <ISPBIEME>31680153</ISPBIEME>
                <VlrLanc>120.0</VlrLanc>
                <DtMovto>2025-12-03</DtMovto>
            </SME0001>
        </SISMSG>
    </DOC>
    """

    sme0001e = SME0001E.from_xml(xml)

    assert isinstance(sme0001e, SME0001E)
    assert sme0001e.from_ispb == '31680151'
    assert sme0001e.to_ispb == '00038166'
    assert sme0001e.system_domain == 'SPB01'
    assert sme0001e.operation_number == '31680151250908000000001'
    assert sme0001e.message_code == 'SME0001E'
    assert sme0001e.institution_control_number == '123'
    assert sme0001e.institution_ispb == '31680151'
    assert sme0001e.ieme_ispb == '31680153'
    assert sme0001e.amount == Decimal('120.00')
    assert sme0001e.settlement_date == date(2025, 12, 3)
    assert sme0001e.general_error_code == 'EGEN0050'


def test_sme0001e_tag_error_from_xml() -> None:
    xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/SPB/SME0001E.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>31680151250908000000001</NUOp>
        </BCMSG>
        <SISMSG>
            <SME0001>
                <CodMsg>SME0001E</CodMsg>
                <NumCtrlIF>123</NumCtrlIF>
                <ISPBIF>31680151</ISPBIF>
                <ISPBIEME CodErro="EGEN0051">31680153</ISPBIEME>
                <VlrLanc>120.0</VlrLanc>
                <DtMovto>2025-12-03</DtMovto>
            </SME0001>
        </SISMSG>
    </DOC>
    """

    sme0001e = SME0001E.from_xml(xml)

    assert isinstance(sme0001e, SME0001E)
    assert sme0001e.from_ispb == '31680151'
    assert sme0001e.to_ispb == '00038166'
    assert sme0001e.system_domain == 'SPB01'
    assert sme0001e.operation_number == '31680151250908000000001'
    assert sme0001e.message_code == 'SME0001E'
    assert sme0001e.institution_control_number == '123'
    assert sme0001e.institution_ispb == '31680151'
    assert sme0001e.ieme_ispb == '31680153'
    assert sme0001e.amount == Decimal('120.00')
    assert sme0001e.settlement_date == date(2025, 12, 3)
    assert sme0001e.ieme_ispb_error_code == 'EGEN0051'


def test_sme0001_roundtrip() -> None:
    params = make_valid_sme0001_params()

    sme0001 = SME0001.model_validate(params)
    xml = sme0001.to_xml()
    sme0001_from_xml = SME0001.from_xml(xml)

    assert sme0001 == sme0001_from_xml


def test_sme0001r1_roundtrip() -> None:
    params = make_valid_sme0001r1_params()

    sme0001r1 = SME0001R1.model_validate(params)
    xml = sme0001r1.to_xml()
    sme0001r1_from_xml = SME0001R1.from_xml(xml)

    assert sme0001r1 == sme0001r1_from_xml


def test_sme0001r2_roundtrip() -> None:
    params = make_valid_sme0001r2_params()

    sme0001r2 = SME0001R2.model_validate(params)
    xml = sme0001r2.to_xml()
    sme0001r2_from_xml = SME0001R2.from_xml(xml)

    assert sme0001r2 == sme0001r2_from_xml


def test_sme0001_from_xml_missing_required_fields() -> None:
    xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/SPB/SME0001.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>31680151250908000000001</NUOp>
        </BCMSG>
        <SISMSG>
            <SME0001>
                <CodMsg>SME0001</CodMsg>
                <ISPBIEME>31680153</ISPBIEME>
            </SME0001>
        </SISMSG>
    </DOC>
    """

    with pytest.raises(ValidationError) as exc:
        SME0001.from_xml(xml)

    missing_fields = extract_missing_fields(exc.value)
    assert missing_fields == {'institution_control_number', 'institution_ispb', 'amount', 'settlement_date'}
