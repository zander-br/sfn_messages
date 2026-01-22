from datetime import UTC, date, datetime
from decimal import Decimal
from typing import Any

import pytest
from pydantic import ValidationError

from sfn_messages.core.types import AssetType, StrSettlementStatus
from sfn_messages.ltr.ltr0004 import LTR0004, LTR0004E, LTR0004R1, LTR0004R2
from tests.conftest import extract_missing_fields, normalize_xml


def make_valid_ltr0004_params() -> dict[str, Any]:
    return {
        'from_ispb': '31680151',
        'to_ispb': '00038166',
        'system_domain': 'SPB01',
        'operation_number': '31680151250908000000001',
        'message_code': 'LTR0004',
        'institution_control_number': '123',
        'institution_ispb': '31680151',
        'ltr_ispb': '31680153',
        'original_ltr_control_number': '321',
        'amount': 123.0,
        'sub_asset_type': 'INVESTMENT_PORTFOLIO_ASSETS',
        'asset_description': 'Test asset description',
        'description': 'Test description',
        'settlement_date': '2025-12-04',
    }


def make_valid_ltr0004r1_params() -> dict[str, Any]:
    return {
        'from_ispb': '31680151',
        'to_ispb': '00038166',
        'system_domain': 'SPB01',
        'operation_number': '31680151250908000000001',
        'message_code': 'LTR0004R1',
        'institution_control_number': '123',
        'institution_ispb': '31680151',
        'str_control_number': 'STR20250101000000001',
        'str_settlement_status': 'EFFECTIVE',
        'settlement_timestamp': '2025-12-04T13:21:00+00:00',
        'settlement_date': '2025-12-04',
    }


def make_valid_ltr0004r2_params() -> dict[str, Any]:
    return {
        'from_ispb': '31680151',
        'to_ispb': '00038166',
        'system_domain': 'SPB01',
        'operation_number': '31680151250908000000001',
        'message_code': 'LTR0004R2',
        'str_control_number': 'STR20250101000000001',
        'institution_ispb': '31680151',
        'original_ltr_control_number': '321',
        'ltr_ispb': '31680153',
        'amount': 123.0,
        'sub_asset_type': 'INVESTMENT_PORTFOLIO_ASSETS',
        'asset_description': 'Test asset description',
        'description': 'Test description',
        'vendor_timestamp': '2025-12-04T14:11:00+00:00',
        'settlement_date': '2025-12-04',
    }


def make_valid_ltr0004e_params(*, general_error: bool = False) -> dict[str, Any]:
    ltr0004e = {
        'from_ispb': '31680151',
        'to_ispb': '00038166',
        'system_domain': 'SPB01',
        'operation_number': '31680151250908000000001',
        'message_code': 'LTR0004',
        'institution_control_number': '123',
        'institution_ispb': '31680151',
        'ltr_ispb': '31680153',
        'original_ltr_control_number': '321',
        'amount': 123.0,
        'sub_asset_type': 'INVESTMENT_PORTFOLIO_ASSETS',
        'asset_description': 'Test asset description',
        'description': 'Test description',
        'settlement_date': '2025-12-04',
    }

    if general_error:
        ltr0004e['general_error_code'] = 'EGEN0050'
    else:
        ltr0004e['ltr_ispb_error_code'] = 'ELTR0123'

    return ltr0004e


def test_ltr0004_valid_model() -> None:
    params = make_valid_ltr0004_params()
    ltr0004 = LTR0004.model_validate(params)

    assert isinstance(ltr0004, LTR0004)
    assert ltr0004.from_ispb == '31680151'
    assert ltr0004.to_ispb == '00038166'
    assert ltr0004.system_domain == 'SPB01'
    assert ltr0004.operation_number == '31680151250908000000001'
    assert ltr0004.message_code == 'LTR0004'
    assert ltr0004.institution_control_number == '123'
    assert ltr0004.institution_ispb == '31680151'
    assert ltr0004.ltr_ispb == '31680153'
    assert ltr0004.original_ltr_control_number == '321'
    assert ltr0004.amount == Decimal('123.0')
    assert ltr0004.sub_asset_type == AssetType.INVESTMENT_PORTFOLIO_ASSETS
    assert ltr0004.asset_description == 'Test asset description'
    assert ltr0004.description == 'Test description'
    assert ltr0004.settlement_date == date(2025, 12, 4)


def test_ltr0004r1_valid_model() -> None:
    params = make_valid_ltr0004r1_params()
    ltr0004r1 = LTR0004R1.model_validate(params)

    assert isinstance(ltr0004r1, LTR0004R1)
    assert ltr0004r1.from_ispb == '31680151'
    assert ltr0004r1.to_ispb == '00038166'
    assert ltr0004r1.system_domain == 'SPB01'
    assert ltr0004r1.operation_number == '31680151250908000000001'
    assert ltr0004r1.message_code == 'LTR0004R1'
    assert ltr0004r1.institution_control_number == '123'
    assert ltr0004r1.institution_ispb == '31680151'
    assert ltr0004r1.str_control_number == 'STR20250101000000001'
    assert ltr0004r1.str_settlement_status == StrSettlementStatus.EFFECTIVE
    assert ltr0004r1.settlement_timestamp == datetime(2025, 12, 4, 13, 21, tzinfo=UTC)
    assert ltr0004r1.settlement_date == date(2025, 12, 4)


def test_ltr0004r2_valid_model() -> None:
    params = make_valid_ltr0004r2_params()
    ltr0004r2 = LTR0004R2.model_validate(params)

    assert isinstance(ltr0004r2, LTR0004R2)
    assert ltr0004r2.from_ispb == '31680151'
    assert ltr0004r2.to_ispb == '00038166'
    assert ltr0004r2.system_domain == 'SPB01'
    assert ltr0004r2.operation_number == '31680151250908000000001'
    assert ltr0004r2.message_code == 'LTR0004R2'
    assert ltr0004r2.str_control_number == 'STR20250101000000001'
    assert ltr0004r2.institution_ispb == '31680151'
    assert ltr0004r2.original_ltr_control_number == '321'
    assert ltr0004r2.ltr_ispb == '31680153'
    assert ltr0004r2.amount == Decimal('123.0')
    assert ltr0004r2.sub_asset_type == AssetType.INVESTMENT_PORTFOLIO_ASSETS
    assert ltr0004r2.asset_description == 'Test asset description'
    assert ltr0004r2.description == 'Test description'
    assert ltr0004r2.vendor_timestamp == datetime(2025, 12, 4, 14, 11, tzinfo=UTC)
    assert ltr0004r2.settlement_date == date(2025, 12, 4)


def test_ltr0004e_valid_model() -> None:
    params = make_valid_ltr0004e_params()
    ltr0004e = LTR0004E.model_validate(params)

    assert isinstance(ltr0004e, LTR0004E)
    assert ltr0004e.from_ispb == '31680151'
    assert ltr0004e.to_ispb == '00038166'
    assert ltr0004e.system_domain == 'SPB01'
    assert ltr0004e.operation_number == '31680151250908000000001'
    assert ltr0004e.message_code == 'LTR0004'
    assert ltr0004e.institution_control_number == '123'
    assert ltr0004e.institution_ispb == '31680151'
    assert ltr0004e.ltr_ispb == '31680153'
    assert ltr0004e.original_ltr_control_number == '321'
    assert ltr0004e.amount == Decimal('123.0')
    assert ltr0004e.sub_asset_type == AssetType.INVESTMENT_PORTFOLIO_ASSETS
    assert ltr0004e.asset_description == 'Test asset description'
    assert ltr0004e.description == 'Test description'
    assert ltr0004e.settlement_date == date(2025, 12, 4)

    assert ltr0004e.ltr_ispb_error_code == 'ELTR0123'


def test_ltr0004e_general_error_valid_model() -> None:
    params = make_valid_ltr0004e_params(general_error=True)
    ltr0004e = LTR0004E.model_validate(params)

    assert isinstance(ltr0004e, LTR0004E)
    assert ltr0004e.from_ispb == '31680151'
    assert ltr0004e.to_ispb == '00038166'
    assert ltr0004e.system_domain == 'SPB01'
    assert ltr0004e.operation_number == '31680151250908000000001'
    assert ltr0004e.message_code == 'LTR0004'
    assert ltr0004e.institution_control_number == '123'
    assert ltr0004e.institution_ispb == '31680151'
    assert ltr0004e.ltr_ispb == '31680153'
    assert ltr0004e.original_ltr_control_number == '321'
    assert ltr0004e.amount == Decimal('123.0')
    assert ltr0004e.sub_asset_type == AssetType.INVESTMENT_PORTFOLIO_ASSETS
    assert ltr0004e.asset_description == 'Test asset description'
    assert ltr0004e.description == 'Test description'
    assert ltr0004e.settlement_date == date(2025, 12, 4)

    assert ltr0004e.general_error_code == 'EGEN0050'


def test_ltr0004_missing_required_fields() -> None:
    with pytest.raises(ValidationError) as exc:
        LTR0004.model_validate({})

    missing_fields = extract_missing_fields(exc.value)
    assert missing_fields == {
        'from_ispb',
        'to_ispb',
        'system_domain',
        'operation_number',
        'institution_control_number',
        'institution_ispb',
        'ltr_ispb',
        'original_ltr_control_number',
        'amount',
        'sub_asset_type',
        'settlement_date',
    }


def test_ltr0004r1_missing_required_fields() -> None:
    with pytest.raises(ValidationError) as exc:
        LTR0004R1.model_validate({})

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
        'settlement_timestamp',
        'settlement_date',
    }


def test_ltr0004r2_missing_required_fields() -> None:
    with pytest.raises(ValidationError) as exc:
        LTR0004R2.model_validate({})

    missing_fields = extract_missing_fields(exc.value)
    assert missing_fields == {
        'from_ispb',
        'to_ispb',
        'system_domain',
        'operation_number',
        'str_control_number',
        'institution_ispb',
        'original_ltr_control_number',
        'ltr_ispb',
        'amount',
        'sub_asset_type',
        'vendor_timestamp',
        'settlement_date',
    }


def test_ltr0004_to_xml() -> None:
    params = make_valid_ltr0004_params()
    ltr0004 = LTR0004.model_validate(params)

    xml = ltr0004.to_xml()

    expected_xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/LTR/LTR0004.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>31680151250908000000001</NUOp>
        </BCMSG>
        <SISMSG>
            <LTR0004>
                <CodMsg>LTR0004</CodMsg>
                <NumCtrlIF>123</NumCtrlIF>
                <ISPBIF>31680151</ISPBIF>
                <ISPBLTR>31680153</ISPBLTR>
                <NumCtrlLTROr>321</NumCtrlLTROr>
                <VlrLanc>123.0</VlrLanc>
                <SubTpAtv>ACI</SubTpAtv>
                <DescAtv>Test asset description</DescAtv>
                <Hist>Test description</Hist>
                <DtMovto>2025-12-04</DtMovto>
            </LTR0004>
        </SISMSG>
    </DOC>
    """
    assert normalize_xml(expected_xml) == normalize_xml(xml)


def test_ltr0004r1_to_xml() -> None:
    params = make_valid_ltr0004r1_params()
    ltr0004r1 = LTR0004R1.model_validate(params)

    xml = ltr0004r1.to_xml()

    expected_xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/LTR/LTR0004.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>31680151250908000000001</NUOp>
        </BCMSG>
        <SISMSG>
            <LTR0004R1>
                <CodMsg>LTR0004R1</CodMsg>
                <NumCtrlIF>123</NumCtrlIF>
                <ISPBIF>31680151</ISPBIF>
                <NumCtrlSTR>STR20250101000000001</NumCtrlSTR>
                <SitLancSTR>1</SitLancSTR>
                <DtHrSit>2025-12-04 13:21:00+00:00</DtHrSit>
                <DtMovto>2025-12-04</DtMovto>
            </LTR0004R1>
        </SISMSG>
    </DOC>
    """
    assert normalize_xml(expected_xml) == normalize_xml(xml)


def test_ltr0004r2_to_xml() -> None:
    params = make_valid_ltr0004r2_params()
    ltr0004r2 = LTR0004R2.model_validate(params)

    xml = ltr0004r2.to_xml()

    expected_xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/LTR/LTR0004.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>31680151250908000000001</NUOp>
        </BCMSG>
        <SISMSG>
            <LTR0004R2>
                <CodMsg>LTR0004R2</CodMsg>
                <NumCtrlSTR>STR20250101000000001</NumCtrlSTR>
                <ISPBIF>31680151</ISPBIF>
                <NumCtrlLTROr>321</NumCtrlLTROr>
                <ISPBLTR>31680153</ISPBLTR>
                <VlrLanc>123.0</VlrLanc>
                <SubTpAtv>ACI</SubTpAtv>
                <DescAtv>Test asset description</DescAtv>
                <Hist>Test description</Hist>
                <DtHrBC>2025-12-04 14:11:00+00:00</DtHrBC>
                <DtMovto>2025-12-04</DtMovto>
            </LTR0004R2>
        </SISMSG>
    </DOC>
    """
    assert normalize_xml(expected_xml) == normalize_xml(xml)


def test_ltr0004e_general_error_to_xml() -> None:
    params = make_valid_ltr0004e_params(general_error=True)
    ltr0004e = LTR0004E.model_validate(params)

    xml = ltr0004e.to_xml()

    expected_xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/LTR/LTR0004E.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>31680151250908000000001</NUOp>
        </BCMSG>
        <SISMSG>
            <LTR0004E CodErro="EGEN0050">
                <CodMsg>LTR0004</CodMsg>
                <NumCtrlIF>123</NumCtrlIF>
                <ISPBIF>31680151</ISPBIF>
                <ISPBLTR>31680153</ISPBLTR>
                <NumCtrlLTROr>321</NumCtrlLTROr>
                <VlrLanc>123.0</VlrLanc>
                <SubTpAtv>ACI</SubTpAtv>
                <DescAtv>Test asset description</DescAtv>
                <Hist>Test description</Hist>
                <DtMovto>2025-12-04</DtMovto>
            </LTR0004E>
        </SISMSG>
    </DOC>
    """
    assert normalize_xml(expected_xml) == normalize_xml(xml)


def test_ltr0004e_tag_error_to_xml() -> None:
    params = make_valid_ltr0004e_params()
    ltr0004e = LTR0004E.model_validate(params)

    xml = ltr0004e.to_xml()

    expected_xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/LTR/LTR0004E.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>31680151250908000000001</NUOp>
        </BCMSG>
        <SISMSG>
            <LTR0004E>
                <CodMsg>LTR0004</CodMsg>
                <NumCtrlIF>123</NumCtrlIF>
                <ISPBIF>31680151</ISPBIF>
                <ISPBLTR CodErro="ELTR0123">31680153</ISPBLTR>
                <NumCtrlLTROr>321</NumCtrlLTROr>
                <VlrLanc>123.0</VlrLanc>
                <SubTpAtv>ACI</SubTpAtv>
                <DescAtv>Test asset description</DescAtv>
                <Hist>Test description</Hist>
                <DtMovto>2025-12-04</DtMovto>
            </LTR0004E>
        </SISMSG>
    </DOC>
    """
    assert normalize_xml(expected_xml) == normalize_xml(xml)


def test_ltr0004_from_xml() -> None:
    xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/LTR/LTR0004.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>31680151250908000000001</NUOp>
        </BCMSG>
        <SISMSG>
            <LTR0004>
                <CodMsg>LTR0004</CodMsg>
                <NumCtrlIF>123</NumCtrlIF>
                <ISPBIF>31680151</ISPBIF>
                <ISPBLTR>31680153</ISPBLTR>
                <NumCtrlLTROr>321</NumCtrlLTROr>
                <VlrLanc>123.0</VlrLanc>
                <SubTpAtv>ACI</SubTpAtv>
                <DescAtv>Test asset description</DescAtv>
                <Hist>Test description</Hist>
                <DtMovto>2025-12-04</DtMovto>
            </LTR0004>
        </SISMSG>
    </DOC>
    """

    ltr0004 = LTR0004.from_xml(xml)

    assert isinstance(ltr0004, LTR0004)
    assert ltr0004.from_ispb == '31680151'
    assert ltr0004.to_ispb == '00038166'
    assert ltr0004.system_domain == 'SPB01'
    assert ltr0004.operation_number == '31680151250908000000001'
    assert ltr0004.message_code == 'LTR0004'
    assert ltr0004.institution_control_number == '123'
    assert ltr0004.institution_ispb == '31680151'
    assert ltr0004.ltr_ispb == '31680153'
    assert ltr0004.original_ltr_control_number == '321'
    assert ltr0004.amount == Decimal('123.0')
    assert ltr0004.sub_asset_type == AssetType.INVESTMENT_PORTFOLIO_ASSETS
    assert ltr0004.asset_description == 'Test asset description'
    assert ltr0004.description == 'Test description'
    assert ltr0004.settlement_date == date(2025, 12, 4)


def test_ltr0004r1_from_xml() -> None:
    xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/LTR/LTR0004.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>31680151250908000000001</NUOp>
        </BCMSG>
        <SISMSG>
            <LTR0004R1>
                <CodMsg>LTR0004R1</CodMsg>
                <NumCtrlIF>123</NumCtrlIF>
                <ISPBIF>31680151</ISPBIF>
                <NumCtrlSTR>STR20250101000000001</NumCtrlSTR>
                <SitLancSTR>1</SitLancSTR>
                <DtHrSit>2025-12-04 13:21:00+00:00</DtHrSit>
                <DtMovto>2025-12-04</DtMovto>
            </LTR0004R1>
        </SISMSG>
    </DOC>
    """

    ltr0004r1 = LTR0004R1.from_xml(xml)

    assert isinstance(ltr0004r1, LTR0004R1)
    assert ltr0004r1.from_ispb == '31680151'
    assert ltr0004r1.to_ispb == '00038166'
    assert ltr0004r1.system_domain == 'SPB01'
    assert ltr0004r1.operation_number == '31680151250908000000001'
    assert ltr0004r1.message_code == 'LTR0004R1'
    assert ltr0004r1.institution_control_number == '123'
    assert ltr0004r1.institution_ispb == '31680151'
    assert ltr0004r1.str_control_number == 'STR20250101000000001'
    assert ltr0004r1.str_settlement_status == StrSettlementStatus.EFFECTIVE
    assert ltr0004r1.settlement_timestamp == datetime(2025, 12, 4, 13, 21, tzinfo=UTC)
    assert ltr0004r1.settlement_date == date(2025, 12, 4)


def test_ltr0004r2_from_xml() -> None:
    xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/LTR/LTR0004.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>31680151250908000000001</NUOp>
        </BCMSG>
        <SISMSG>
            <LTR0004R2>
                <CodMsg>LTR0004R2</CodMsg>
                <NumCtrlSTR>STR20250101000000001</NumCtrlSTR>
                <ISPBIF>31680151</ISPBIF>
                <NumCtrlLTROr>321</NumCtrlLTROr>
                <ISPBLTR>31680153</ISPBLTR>
                <VlrLanc>123.0</VlrLanc>
                <SubTpAtv>ACI</SubTpAtv>
                <DescAtv>Test asset description</DescAtv>
                <Hist>Test description</Hist>
                <DtHrBC>2025-12-04 14:11:00+00:00</DtHrBC>
                <DtMovto>2025-12-04</DtMovto>
            </LTR0004R2>
        </SISMSG>
    </DOC>
    """

    ltr0004r2 = LTR0004R2.from_xml(xml)

    assert isinstance(ltr0004r2, LTR0004R2)
    assert ltr0004r2.from_ispb == '31680151'
    assert ltr0004r2.to_ispb == '00038166'
    assert ltr0004r2.system_domain == 'SPB01'
    assert ltr0004r2.operation_number == '31680151250908000000001'
    assert ltr0004r2.message_code == 'LTR0004R2'
    assert ltr0004r2.str_control_number == 'STR20250101000000001'
    assert ltr0004r2.institution_ispb == '31680151'
    assert ltr0004r2.original_ltr_control_number == '321'
    assert ltr0004r2.ltr_ispb == '31680153'
    assert ltr0004r2.amount == Decimal('123.0')
    assert ltr0004r2.sub_asset_type == AssetType.INVESTMENT_PORTFOLIO_ASSETS
    assert ltr0004r2.asset_description == 'Test asset description'
    assert ltr0004r2.description == 'Test description'
    assert ltr0004r2.vendor_timestamp == datetime(2025, 12, 4, 14, 11, tzinfo=UTC)
    assert ltr0004r2.settlement_date == date(2025, 12, 4)


def test_ltr0004e_general_error_from_xml() -> None:
    xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/LTR/LTR0004E.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>31680151250908000000001</NUOp>
        </BCMSG>
        <SISMSG>
            <LTR0004E CodErro="EGEN0050">
                <CodMsg>LTR0004</CodMsg>
                <NumCtrlIF>123</NumCtrlIF>
                <ISPBIF>31680151</ISPBIF>
                <ISPBLTR>31680153</ISPBLTR>
                <NumCtrlLTROr>321</NumCtrlLTROr>
                <VlrLanc>123.0</VlrLanc>
                <SubTpAtv>ACI</SubTpAtv>
                <DescAtv>Test asset description</DescAtv>
                <Hist>Test description</Hist>
                <DtMovto>2025-12-04</DtMovto>
            </LTR0004E>
        </SISMSG>
    </DOC>
    """

    ltr0004e = LTR0004E.from_xml(xml)

    assert isinstance(ltr0004e, LTR0004E)
    assert ltr0004e.from_ispb == '31680151'
    assert ltr0004e.to_ispb == '00038166'
    assert ltr0004e.system_domain == 'SPB01'
    assert ltr0004e.operation_number == '31680151250908000000001'
    assert ltr0004e.message_code == 'LTR0004'
    assert ltr0004e.institution_control_number == '123'
    assert ltr0004e.institution_ispb == '31680151'
    assert ltr0004e.ltr_ispb == '31680153'
    assert ltr0004e.original_ltr_control_number == '321'
    assert ltr0004e.amount == Decimal('123.0')
    assert ltr0004e.sub_asset_type == AssetType.INVESTMENT_PORTFOLIO_ASSETS
    assert ltr0004e.asset_description == 'Test asset description'
    assert ltr0004e.description == 'Test description'
    assert ltr0004e.settlement_date == date(2025, 12, 4)

    assert ltr0004e.general_error_code == 'EGEN0050'


def test_ltr0004e_tag_error_from_xml() -> None:
    xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/LTR/LTR0004E.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>31680151250908000000001</NUOp>
        </BCMSG>
        <SISMSG>
            <LTR0004E>
                <CodMsg>LTR0004</CodMsg>
                <NumCtrlIF>123</NumCtrlIF>
                <ISPBIF>31680151</ISPBIF>
                <ISPBLTR CodErro="ELTR0123">31680153</ISPBLTR>
                <NumCtrlLTROr>321</NumCtrlLTROr>
                <VlrLanc>123.0</VlrLanc>
                <SubTpAtv>ACI</SubTpAtv>
                <DescAtv>Test asset description</DescAtv>
                <Hist>Test description</Hist>
                <DtMovto>2025-12-04</DtMovto>
            </LTR0004E>
        </SISMSG>
    </DOC>
    """

    ltr0004e = LTR0004E.from_xml(xml)

    assert isinstance(ltr0004e, LTR0004E)
    assert ltr0004e.from_ispb == '31680151'
    assert ltr0004e.to_ispb == '00038166'
    assert ltr0004e.system_domain == 'SPB01'
    assert ltr0004e.operation_number == '31680151250908000000001'
    assert ltr0004e.message_code == 'LTR0004'
    assert ltr0004e.institution_control_number == '123'
    assert ltr0004e.institution_ispb == '31680151'
    assert ltr0004e.ltr_ispb == '31680153'
    assert ltr0004e.original_ltr_control_number == '321'
    assert ltr0004e.amount == Decimal('123.0')
    assert ltr0004e.sub_asset_type == AssetType.INVESTMENT_PORTFOLIO_ASSETS
    assert ltr0004e.asset_description == 'Test asset description'
    assert ltr0004e.description == 'Test description'
    assert ltr0004e.settlement_date == date(2025, 12, 4)

    assert ltr0004e.ltr_ispb_error_code == 'ELTR0123'


def test_ltr0004_roundtrip() -> None:
    params = make_valid_ltr0004_params()

    ltr0004 = LTR0004.model_validate(params)
    xml = ltr0004.to_xml()
    ltr0004_from_xml = LTR0004.from_xml(xml)

    assert ltr0004 == ltr0004_from_xml


def test_ltr0004r1_roundtrip() -> None:
    params = make_valid_ltr0004r1_params()

    ltr0004r1 = LTR0004R1.model_validate(params)
    xml = ltr0004r1.to_xml()
    ltr0004r1_from_xml = LTR0004R1.from_xml(xml)

    assert ltr0004r1 == ltr0004r1_from_xml


def test_ltr0004r2_roundtrip() -> None:
    params = make_valid_ltr0004r2_params()

    ltr0004r2 = LTR0004R2.model_validate(params)
    xml = ltr0004r2.to_xml()
    ltr0004r2_from_xml = LTR0004R2.from_xml(xml)

    assert ltr0004r2 == ltr0004r2_from_xml
