from datetime import UTC, date, datetime
from decimal import Decimal
from typing import Any

import pytest
from pydantic import ValidationError

from sfn_messages.core.types import AssetType, Priority, StrSettlementStatus
from sfn_messages.ltr.ltr0003 import LTR0003, LTR0003E, LTR0003R1, LTR0003R2, LTR0003R3
from tests.conftest import extract_missing_fields, normalize_xml


def make_valid_ltr0003_params() -> dict[str, Any]:
    return {
        'from_ispb': '31680151',
        'to_ispb': '00038166',
        'system_domain': 'SPB01',
        'operation_number': '316801512509080000001',
        'message_code': 'LTR0003',
        'institution_control_number': '123',
        'debtor_institution_ispb': '31680151',
        'creditor_institution_ispb': '31680152',
        'ltr_ispb': '31680153',
        'original_ltr_control_number': '321',
        'branch': '001',
        'account_number': '123456',
        'amount': 123.0,
        'sub_asset_type': 'INVESTMENT_PORTFOLIO_ASSETS',
        'asset_description': 'Test asset description',
        'description': 'Test description',
        'priority': 'MEDIUM',
        'settlement_date': '2025-12-04',
    }


def make_valid_ltr0003r1_params() -> dict[str, Any]:
    return {
        'from_ispb': '31680151',
        'to_ispb': '00038166',
        'system_domain': 'SPB01',
        'operation_number': '316801512509080000001',
        'message_code': 'LTR0003R1',
        'institution_control_number': '123',
        'institution_ispb': '31680151',
        'str_control_number': 'STR20250101000000001',
        'str_settlement_status': 'EFFECTIVE',
        'settlement_timestamp': '2025-12-04T13:21:00+00:00',
        'settlement_date': '2025-12-04',
    }


def make_valid_ltr0003r2_params() -> dict[str, Any]:
    return {
        'from_ispb': '31680151',
        'to_ispb': '00038166',
        'system_domain': 'SPB01',
        'operation_number': '316801512509080000001',
        'message_code': 'LTR0003R2',
        'str_control_number': 'STR20250101000000001',
        'debtor_institution_ispb': '31680151',
        'creditor_institution_ispb': '31680152',
        'ltr_ispb': '31680153',
        'original_ltr_control_number': '321',
        'branch': '001',
        'account_number': '123456',
        'amount': 123.0,
        'sub_asset_type': 'INVESTMENT_PORTFOLIO_ASSETS',
        'asset_description': 'Test asset description',
        'description': 'Test description',
        'priority': 'MEDIUM',
        'vendor_timestamp': '2025-12-04T13:22:00+00:00',
        'settlement_date': '2025-12-04',
    }


def make_valid_ltr0003r3_params() -> dict[str, Any]:
    return {
        'from_ispb': '31680151',
        'to_ispb': '00038166',
        'system_domain': 'SPB01',
        'operation_number': '316801512509080000001',
        'message_code': 'LTR0003R3',
        'str_control_number': 'STR20250101000000001',
        'debtor_institution_ispb': '31680151',
        'creditor_institution_ispb': '31680152',
        'ltr_ispb': '31680153',
        'original_ltr_control_number': '321',
        'branch': '001',
        'account_number': '123456',
        'amount': 123.0,
        'description': 'Test description',
        'vendor_timestamp': '2025-12-04T13:23:00+00:00',
        'settlement_date': '2025-12-04',
    }


def make_valid_ltr0003e_params(*, general_error: bool = False) -> dict[str, Any]:
    ltr0003e = {
        'from_ispb': '31680151',
        'to_ispb': '00038166',
        'system_domain': 'SPB01',
        'operation_number': '316801512509080000001',
        'message_code': 'LTR0003',
        'institution_control_number': '123',
        'debtor_institution_ispb': '31680151',
        'creditor_institution_ispb': '31680152',
        'ltr_ispb': '31680153',
        'original_ltr_control_number': '321',
        'branch': '001',
        'account_number': '123456',
        'amount': 123.0,
        'sub_asset_type': 'INVESTMENT_PORTFOLIO_ASSETS',
        'asset_description': 'Test asset description',
        'description': 'Test description',
        'priority': 'MEDIUM',
        'settlement_date': '2025-12-04',
    }

    if general_error:
        ltr0003e['general_error_code'] = 'EGEN0050'
    else:
        ltr0003e['ltr_ispb_error_code'] = 'EGEN0051'

    return ltr0003e


def test_ltr0003_valid_model() -> None:
    params = make_valid_ltr0003_params()
    ltr0003 = LTR0003.model_validate(params)

    assert isinstance(ltr0003, LTR0003)
    assert ltr0003.from_ispb == '31680151'
    assert ltr0003.to_ispb == '00038166'
    assert ltr0003.system_domain == 'SPB01'
    assert ltr0003.operation_number == '316801512509080000001'
    assert ltr0003.message_code == 'LTR0003'
    assert ltr0003.institution_control_number == '123'
    assert ltr0003.debtor_institution_ispb == '31680151'
    assert ltr0003.creditor_institution_ispb == '31680152'
    assert ltr0003.ltr_ispb == '31680153'
    assert ltr0003.original_ltr_control_number == '321'
    assert ltr0003.branch == '001'
    assert ltr0003.account_number == '123456'
    assert ltr0003.amount == Decimal('123.0')
    assert ltr0003.sub_asset_type == AssetType.INVESTMENT_PORTFOLIO_ASSETS
    assert ltr0003.asset_description == 'Test asset description'
    assert ltr0003.description == 'Test description'
    assert ltr0003.priority == Priority.MEDIUM
    assert ltr0003.settlement_date == date(2025, 12, 4)


def test_ltr0003r1_valid_model() -> None:
    params = make_valid_ltr0003r1_params()
    ltr0003r1 = LTR0003R1.model_validate(params)

    assert isinstance(ltr0003r1, LTR0003R1)
    assert ltr0003r1.from_ispb == '31680151'
    assert ltr0003r1.to_ispb == '00038166'
    assert ltr0003r1.system_domain == 'SPB01'
    assert ltr0003r1.operation_number == '316801512509080000001'
    assert ltr0003r1.message_code == 'LTR0003R1'
    assert ltr0003r1.institution_control_number == '123'
    assert ltr0003r1.institution_ispb == '31680151'
    assert ltr0003r1.str_control_number == 'STR20250101000000001'
    assert ltr0003r1.str_settlement_status == StrSettlementStatus.EFFECTIVE
    assert ltr0003r1.settlement_timestamp == datetime(2025, 12, 4, 13, 21, tzinfo=UTC)
    assert ltr0003r1.settlement_date == date(2025, 12, 4)


def test_ltr0003r2_valid_model() -> None:
    params = make_valid_ltr0003r2_params()
    ltr0003r2 = LTR0003R2.model_validate(params)

    assert isinstance(ltr0003r2, LTR0003R2)
    assert ltr0003r2.from_ispb == '31680151'
    assert ltr0003r2.to_ispb == '00038166'
    assert ltr0003r2.system_domain == 'SPB01'
    assert ltr0003r2.operation_number == '316801512509080000001'
    assert ltr0003r2.message_code == 'LTR0003R2'
    assert ltr0003r2.str_control_number == 'STR20250101000000001'
    assert ltr0003r2.debtor_institution_ispb == '31680151'
    assert ltr0003r2.creditor_institution_ispb == '31680152'
    assert ltr0003r2.ltr_ispb == '31680153'
    assert ltr0003r2.original_ltr_control_number == '321'
    assert ltr0003r2.branch == '001'
    assert ltr0003r2.account_number == '123456'
    assert ltr0003r2.amount == Decimal('123.0')
    assert ltr0003r2.sub_asset_type == AssetType.INVESTMENT_PORTFOLIO_ASSETS
    assert ltr0003r2.asset_description == 'Test asset description'
    assert ltr0003r2.description == 'Test description'
    assert ltr0003r2.priority == Priority.MEDIUM
    assert ltr0003r2.vendor_timestamp == datetime(2025, 12, 4, 13, 22, tzinfo=UTC)
    assert ltr0003r2.settlement_date == date(2025, 12, 4)


def test_ltr0003r3_valid_model() -> None:
    params = make_valid_ltr0003r3_params()
    ltr0003r3 = LTR0003R3.model_validate(params)

    assert isinstance(ltr0003r3, LTR0003R3)
    assert ltr0003r3.from_ispb == '31680151'
    assert ltr0003r3.to_ispb == '00038166'
    assert ltr0003r3.system_domain == 'SPB01'
    assert ltr0003r3.operation_number == '316801512509080000001'
    assert ltr0003r3.message_code == 'LTR0003R3'
    assert ltr0003r3.str_control_number == 'STR20250101000000001'
    assert ltr0003r3.debtor_institution_ispb == '31680151'
    assert ltr0003r3.creditor_institution_ispb == '31680152'
    assert ltr0003r3.ltr_ispb == '31680153'
    assert ltr0003r3.original_ltr_control_number == '321'
    assert ltr0003r3.branch == '001'
    assert ltr0003r3.account_number == '123456'
    assert ltr0003r3.amount == Decimal('123.0')
    assert ltr0003r3.description == 'Test description'
    assert ltr0003r3.vendor_timestamp == datetime(2025, 12, 4, 13, 23, tzinfo=UTC)
    assert ltr0003r3.settlement_date == date(2025, 12, 4)


def test_ltr0003e_general_error_valid_model() -> None:
    params = make_valid_ltr0003e_params(general_error=True)
    ltr0003e = LTR0003E.model_validate(params)

    assert isinstance(ltr0003e, LTR0003E)
    assert ltr0003e.from_ispb == '31680151'
    assert ltr0003e.to_ispb == '00038166'
    assert ltr0003e.system_domain == 'SPB01'
    assert ltr0003e.operation_number == '316801512509080000001'
    assert ltr0003e.message_code == 'LTR0003'
    assert ltr0003e.institution_control_number == '123'
    assert ltr0003e.debtor_institution_ispb == '31680151'
    assert ltr0003e.creditor_institution_ispb == '31680152'
    assert ltr0003e.ltr_ispb == '31680153'
    assert ltr0003e.original_ltr_control_number == '321'
    assert ltr0003e.branch == '001'
    assert ltr0003e.account_number == '123456'
    assert ltr0003e.amount == Decimal('123.0')
    assert ltr0003e.sub_asset_type == AssetType.INVESTMENT_PORTFOLIO_ASSETS
    assert ltr0003e.asset_description == 'Test asset description'
    assert ltr0003e.description == 'Test description'
    assert ltr0003e.priority == Priority.MEDIUM
    assert ltr0003e.settlement_date == date(2025, 12, 4)
    assert ltr0003e.general_error_code == 'EGEN0050'


def test_ltr0003e_tag_error_valid_model() -> None:
    params = make_valid_ltr0003e_params()
    ltr0003e = LTR0003E.model_validate(params)

    assert isinstance(ltr0003e, LTR0003E)
    assert ltr0003e.from_ispb == '31680151'
    assert ltr0003e.to_ispb == '00038166'
    assert ltr0003e.system_domain == 'SPB01'
    assert ltr0003e.operation_number == '316801512509080000001'
    assert ltr0003e.message_code == 'LTR0003'
    assert ltr0003e.institution_control_number == '123'
    assert ltr0003e.debtor_institution_ispb == '31680151'
    assert ltr0003e.creditor_institution_ispb == '31680152'
    assert ltr0003e.ltr_ispb == '31680153'
    assert ltr0003e.original_ltr_control_number == '321'
    assert ltr0003e.branch == '001'
    assert ltr0003e.account_number == '123456'
    assert ltr0003e.amount == Decimal('123.0')
    assert ltr0003e.sub_asset_type == AssetType.INVESTMENT_PORTFOLIO_ASSETS
    assert ltr0003e.asset_description == 'Test asset description'
    assert ltr0003e.description == 'Test description'
    assert ltr0003e.priority == Priority.MEDIUM
    assert ltr0003e.settlement_date == date(2025, 12, 4)
    assert ltr0003e.ltr_ispb_error_code == 'EGEN0051'


def test_ltr0003_missing_required_fields() -> None:
    with pytest.raises(ValidationError) as exc:
        LTR0003.model_validate({})

    missing_fields = extract_missing_fields(exc.value)
    assert missing_fields == {
        'from_ispb',
        'to_ispb',
        'system_domain',
        'operation_number',
        'institution_control_number',
        'debtor_institution_ispb',
        'creditor_institution_ispb',
        'ltr_ispb',
        'original_ltr_control_number',
        'amount',
        'sub_asset_type',
        'settlement_date',
    }


def test_ltr0003r1_missing_required_fields() -> None:
    with pytest.raises(ValidationError) as exc:
        LTR0003R1.model_validate({})

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


def test_ltr0003r2_missing_required_fields() -> None:
    with pytest.raises(ValidationError) as exc:
        LTR0003R2.model_validate({})

    missing_fields = extract_missing_fields(exc.value)
    assert missing_fields == {
        'from_ispb',
        'to_ispb',
        'system_domain',
        'operation_number',
        'str_control_number',
        'debtor_institution_ispb',
        'creditor_institution_ispb',
        'ltr_ispb',
        'original_ltr_control_number',
        'branch',
        'account_number',
        'amount',
        'sub_asset_type',
        'vendor_timestamp',
        'settlement_date',
    }


def test_ltr0003r3_missing_required_fields() -> None:
    with pytest.raises(ValidationError) as exc:
        LTR0003R3.model_validate({})

    missing_fields = extract_missing_fields(exc.value)
    assert missing_fields == {
        'from_ispb',
        'to_ispb',
        'system_domain',
        'operation_number',
        'str_control_number',
        'debtor_institution_ispb',
        'creditor_institution_ispb',
        'ltr_ispb',
        'original_ltr_control_number',
        'branch',
        'account_number',
        'amount',
        'vendor_timestamp',
        'settlement_date',
    }


def test_ltr0003_to_xml() -> None:
    params = make_valid_ltr0003_params()
    ltr0003 = LTR0003.model_validate(params)

    xml = ltr0003.to_xml()

    expected_xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/LTR/LTR0003.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>316801512509080000001</NUOp>
        </BCMSG>
        <SISMSG>
            <LTR0003>
                <CodMsg>LTR0003</CodMsg>
                <NumCtrlIF>123</NumCtrlIF>
                <ISPBIFDebtd>31680151</ISPBIFDebtd>
                <ISPBIFCredtd>31680152</ISPBIFCredtd>
                <ISPBLTR>31680153</ISPBLTR>
                <NumCtrlLTROr>321</NumCtrlLTROr>
                <AgCredtd>001</AgCredtd>
                <CtCredtd>123456</CtCredtd>
                <VlrLanc>123.0</VlrLanc>
                <SubTpAtv>ACI</SubTpAtv>
                <DescAtv>Test asset description</DescAtv>
                <Hist>Test description</Hist>
                <NivelPref>C</NivelPref>
                <DtMovto>2025-12-04</DtMovto>
            </LTR0003>
        </SISMSG>
    </DOC>
    """
    assert normalize_xml(expected_xml) == normalize_xml(xml)


def test_ltr0003r1_to_xml() -> None:
    params = make_valid_ltr0003r1_params()
    ltr0003r1 = LTR0003R1.model_validate(params)

    xml = ltr0003r1.to_xml()

    expected_xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/LTR/LTR0003.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>316801512509080000001</NUOp>
        </BCMSG>
        <SISMSG>
            <LTR0003R1>
                <CodMsg>LTR0003R1</CodMsg>
                <NumCtrlIF>123</NumCtrlIF>
                <ISPBIF>31680151</ISPBIF>
                <NumCtrlSTR>STR20250101000000001</NumCtrlSTR>
                <SitLancSTR>1</SitLancSTR>
                <DtHrSit>2025-12-04 13:21:00+00:00</DtHrSit>
                <DtMovto>2025-12-04</DtMovto>
            </LTR0003R1>
        </SISMSG>
    </DOC>
    """
    assert normalize_xml(expected_xml) == normalize_xml(xml)


def test_ltr0003r2_to_xml() -> None:
    params = make_valid_ltr0003r2_params()
    ltr0003r2 = LTR0003R2.model_validate(params)

    xml = ltr0003r2.to_xml()

    expected_xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/LTR/LTR0003.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>316801512509080000001</NUOp>
        </BCMSG>
        <SISMSG>
            <LTR0003R2>
                <CodMsg>LTR0003R2</CodMsg>
                <NumCtrlSTR>STR20250101000000001</NumCtrlSTR>
                <ISPBIFDebtd>31680151</ISPBIFDebtd>
                <ISPBIFCredtd>31680152</ISPBIFCredtd>
                <ISPBLTR>31680153</ISPBLTR>
                <NumCtrlLTROr>321</NumCtrlLTROr>
                <AgCredtd>001</AgCredtd>
                <CtCredtd>123456</CtCredtd>
                <VlrLanc>123.0</VlrLanc>
                <SubTpAtv>ACI</SubTpAtv>
                <DescAtv>Test asset description</DescAtv>
                <Hist>Test description</Hist>
                <NivelPref>C</NivelPref>
                <DtHrBC>2025-12-04 13:22:00+00:00</DtHrBC>
                <DtMovto>2025-12-04</DtMovto>
            </LTR0003R2>
        </SISMSG>
    </DOC>
    """
    assert normalize_xml(expected_xml) == normalize_xml(xml)


def test_ltr0003r3_to_xml() -> None:
    params = make_valid_ltr0003r3_params()
    ltr0003r3 = LTR0003R3.model_validate(params)

    xml = ltr0003r3.to_xml()

    expected_xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/LTR/LTR0003.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>316801512509080000001</NUOp>
        </BCMSG>
        <SISMSG>
            <LTR0003R3>
                <CodMsg>LTR0003R3</CodMsg>
                <NumCtrlSTR>STR20250101000000001</NumCtrlSTR>
                <ISPBIFDebtd>31680151</ISPBIFDebtd>
                <ISPBIFCredtd>31680152</ISPBIFCredtd>
                <ISPBLTR>31680153</ISPBLTR>
                <NumCtrlLTROr>321</NumCtrlLTROr>
                <AgCredtd>001</AgCredtd>
                <CtCredtd>123456</CtCredtd>
                <VlrLanc>123.0</VlrLanc>
                <Hist>Test description</Hist>
                <DtHrBC>2025-12-04 13:23:00+00:00</DtHrBC>
                <DtMovto>2025-12-04</DtMovto>
            </LTR0003R3>
        </SISMSG>
    </DOC>
    """
    assert normalize_xml(expected_xml) == normalize_xml(xml)


def test_ltr0003e_general_error_to_xml() -> None:
    params = make_valid_ltr0003e_params(general_error=True)
    ltr0003e = LTR0003E.model_validate(params)

    xml = ltr0003e.to_xml()

    expected_xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/LTR/LTR0003E.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>316801512509080000001</NUOp>
        </BCMSG>
        <SISMSG>
            <LTR0003E CodErro="EGEN0050">
                <CodMsg>LTR0003</CodMsg>
                <NumCtrlIF>123</NumCtrlIF>
                <ISPBIFDebtd>31680151</ISPBIFDebtd>
                <ISPBIFCredtd>31680152</ISPBIFCredtd>
                <ISPBLTR>31680153</ISPBLTR>
                <NumCtrlLTROr>321</NumCtrlLTROr>
                <AgCredtd>001</AgCredtd>
                <CtCredtd>123456</CtCredtd>
                <VlrLanc>123.0</VlrLanc>
                <SubTpAtv>ACI</SubTpAtv>
                <DescAtv>Test asset description</DescAtv>
                <Hist>Test description</Hist>
                <NivelPref>C</NivelPref>
                <DtMovto>2025-12-04</DtMovto>
            </LTR0003E>
        </SISMSG>
    </DOC>
    """
    assert normalize_xml(expected_xml) == normalize_xml(xml)


def test_ltr0003e_tag_error_to_xml() -> None:
    params = make_valid_ltr0003e_params()
    ltr0003e = LTR0003E.model_validate(params)

    xml = ltr0003e.to_xml()

    expected_xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/LTR/LTR0003E.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>316801512509080000001</NUOp>
        </BCMSG>
        <SISMSG>
            <LTR0003E>
                <CodMsg>LTR0003</CodMsg>
                <NumCtrlIF>123</NumCtrlIF>
                <ISPBIFDebtd>31680151</ISPBIFDebtd>
                <ISPBIFCredtd>31680152</ISPBIFCredtd>
                <ISPBLTR CodErro="EGEN0051">31680153</ISPBLTR>
                <NumCtrlLTROr>321</NumCtrlLTROr>
                <AgCredtd>001</AgCredtd>
                <CtCredtd>123456</CtCredtd>
                <VlrLanc>123.0</VlrLanc>
                <SubTpAtv>ACI</SubTpAtv>
                <DescAtv>Test asset description</DescAtv>
                <Hist>Test description</Hist>
                <NivelPref>C</NivelPref>
                <DtMovto>2025-12-04</DtMovto>
            </LTR0003E>
        </SISMSG>
    </DOC>
    """
    assert normalize_xml(expected_xml) == normalize_xml(xml)


def test_ltr0003_from_xml() -> None:
    xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/LTR/LTR0003.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>316801512509080000001</NUOp>
        </BCMSG>
        <SISMSG>
            <LTR0003>
                <CodMsg>LTR0003</CodMsg>
                <NumCtrlIF>123</NumCtrlIF>
                <ISPBIFDebtd>31680151</ISPBIFDebtd>
                <ISPBIFCredtd>31680152</ISPBIFCredtd>
                <ISPBLTR>31680153</ISPBLTR>
                <NumCtrlLTROr>321</NumCtrlLTROr>
                <AgCredtd>001</AgCredtd>
                <CtCredtd>123456</CtCredtd>
                <VlrLanc>123.0</VlrLanc>
                <SubTpAtv>ACI</SubTpAtv>
                <DescAtv>Test asset description</DescAtv>
                <Hist>Test description</Hist>
                <NivelPref>C</NivelPref>
                <DtMovto>2025-12-04</DtMovto>
            </LTR0003>
        </SISMSG>
    </DOC>
    """

    ltr0003 = LTR0003.from_xml(xml)

    assert isinstance(ltr0003, LTR0003)
    assert ltr0003.from_ispb == '31680151'
    assert ltr0003.to_ispb == '00038166'
    assert ltr0003.system_domain == 'SPB01'
    assert ltr0003.operation_number == '316801512509080000001'
    assert ltr0003.message_code == 'LTR0003'
    assert ltr0003.institution_control_number == '123'
    assert ltr0003.debtor_institution_ispb == '31680151'
    assert ltr0003.creditor_institution_ispb == '31680152'
    assert ltr0003.ltr_ispb == '31680153'
    assert ltr0003.original_ltr_control_number == '321'
    assert ltr0003.branch == '001'
    assert ltr0003.account_number == '123456'
    assert ltr0003.amount == Decimal('123.0')
    assert ltr0003.sub_asset_type == AssetType.INVESTMENT_PORTFOLIO_ASSETS
    assert ltr0003.asset_description == 'Test asset description'
    assert ltr0003.description == 'Test description'
    assert ltr0003.priority == Priority.MEDIUM
    assert ltr0003.settlement_date == date(2025, 12, 4)


def test_ltr0003r1_from_xml() -> None:
    xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/LTR/LTR0003.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>316801512509080000001</NUOp>
        </BCMSG>
        <SISMSG>
            <LTR0003R1>
                <CodMsg>LTR0003R1</CodMsg>
                <NumCtrlIF>123</NumCtrlIF>
                <ISPBIF>31680151</ISPBIF>
                <NumCtrlSTR>STR20250101000000001</NumCtrlSTR>
                <SitLancSTR>1</SitLancSTR>
                <DtHrSit>2025-12-04 13:21:00+00:00</DtHrSit>
                <DtMovto>2025-12-04</DtMovto>
            </LTR0003R1>
        </SISMSG>
    </DOC>
    """

    ltr0003r1 = LTR0003R1.from_xml(xml)

    assert isinstance(ltr0003r1, LTR0003R1)
    assert ltr0003r1.from_ispb == '31680151'
    assert ltr0003r1.to_ispb == '00038166'
    assert ltr0003r1.system_domain == 'SPB01'
    assert ltr0003r1.operation_number == '316801512509080000001'
    assert ltr0003r1.message_code == 'LTR0003R1'
    assert ltr0003r1.institution_control_number == '123'
    assert ltr0003r1.institution_ispb == '31680151'
    assert ltr0003r1.str_control_number == 'STR20250101000000001'
    assert ltr0003r1.str_settlement_status == StrSettlementStatus.EFFECTIVE
    assert ltr0003r1.settlement_timestamp == datetime(2025, 12, 4, 13, 21, tzinfo=UTC)
    assert ltr0003r1.settlement_date == date(2025, 12, 4)


def test_ltr0003r2_from_xml() -> None:
    xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/LTR/LTR0003.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>316801512509080000001</NUOp>
        </BCMSG>
        <SISMSG>
            <LTR0003R2>
                <CodMsg>LTR0003R2</CodMsg>
                <NumCtrlSTR>STR20250101000000001</NumCtrlSTR>
                <ISPBIFDebtd>31680151</ISPBIFDebtd>
                <ISPBIFCredtd>31680152</ISPBIFCredtd>
                <ISPBLTR>31680153</ISPBLTR>
                <NumCtrlLTROr>321</NumCtrlLTROr>
                <AgCredtd>001</AgCredtd>
                <CtCredtd>123456</CtCredtd>
                <VlrLanc>123.0</VlrLanc>
                <SubTpAtv>ACI</SubTpAtv>
                <DescAtv>Test asset description</DescAtv>
                <Hist>Test description</Hist>
                <NivelPref>C</NivelPref>
                <DtHrBC>2025-12-04 13:22:00+00:00</DtHrBC>
                <DtMovto>2025-12-04</DtMovto>
            </LTR0003R2>
        </SISMSG>
    </DOC>
    """

    ltr0003r2 = LTR0003R2.from_xml(xml)

    assert isinstance(ltr0003r2, LTR0003R2)
    assert ltr0003r2.from_ispb == '31680151'
    assert ltr0003r2.to_ispb == '00038166'
    assert ltr0003r2.system_domain == 'SPB01'
    assert ltr0003r2.operation_number == '316801512509080000001'
    assert ltr0003r2.message_code == 'LTR0003R2'
    assert ltr0003r2.str_control_number == 'STR20250101000000001'
    assert ltr0003r2.debtor_institution_ispb == '31680151'
    assert ltr0003r2.creditor_institution_ispb == '31680152'
    assert ltr0003r2.ltr_ispb == '31680153'
    assert ltr0003r2.original_ltr_control_number == '321'
    assert ltr0003r2.branch == '001'
    assert ltr0003r2.account_number == '123456'
    assert ltr0003r2.amount == Decimal('123.0')
    assert ltr0003r2.sub_asset_type == AssetType.INVESTMENT_PORTFOLIO_ASSETS
    assert ltr0003r2.asset_description == 'Test asset description'
    assert ltr0003r2.description == 'Test description'
    assert ltr0003r2.priority == Priority.MEDIUM
    assert ltr0003r2.vendor_timestamp == datetime(2025, 12, 4, 13, 22, tzinfo=UTC)
    assert ltr0003r2.settlement_date == date(2025, 12, 4)


def test_ltr0003r3_from_xml() -> None:
    xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/LTR/LTR0003.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>316801512509080000001</NUOp>
        </BCMSG>
        <SISMSG>
            <LTR0003R3>
                <CodMsg>LTR0003R3</CodMsg>
                <NumCtrlSTR>STR20250101000000001</NumCtrlSTR>
                <ISPBIFDebtd>31680151</ISPBIFDebtd>
                <ISPBIFCredtd>31680152</ISPBIFCredtd>
                <ISPBLTR>31680153</ISPBLTR>
                <NumCtrlLTROr>321</NumCtrlLTROr>
                <AgCredtd>001</AgCredtd>
                <CtCredtd>123456</CtCredtd>
                <VlrLanc>123.0</VlrLanc>
                <Hist>Test description</Hist>
                <DtHrBC>2025-12-04T13:23:00+00:00</DtHrBC>
                <DtMovto>2025-12-04</DtMovto>
            </LTR0003R3>
        </SISMSG>
    </DOC>
    """

    ltr0003r3 = LTR0003R3.from_xml(xml)

    assert isinstance(ltr0003r3, LTR0003R3)
    assert ltr0003r3.from_ispb == '31680151'
    assert ltr0003r3.to_ispb == '00038166'
    assert ltr0003r3.system_domain == 'SPB01'
    assert ltr0003r3.operation_number == '316801512509080000001'
    assert ltr0003r3.message_code == 'LTR0003R3'
    assert ltr0003r3.str_control_number == 'STR20250101000000001'
    assert ltr0003r3.debtor_institution_ispb == '31680151'
    assert ltr0003r3.creditor_institution_ispb == '31680152'
    assert ltr0003r3.ltr_ispb == '31680153'
    assert ltr0003r3.original_ltr_control_number == '321'
    assert ltr0003r3.branch == '001'
    assert ltr0003r3.account_number == '123456'
    assert ltr0003r3.amount == Decimal('123.0')
    assert ltr0003r3.description == 'Test description'
    assert ltr0003r3.vendor_timestamp == datetime(2025, 12, 4, 13, 23, tzinfo=UTC)
    assert ltr0003r3.settlement_date == date(2025, 12, 4)


def test_ltr0003e_general_error_from_xml() -> None:
    xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/LTR/LTR0003E.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>316801512509080000001</NUOp>
        </BCMSG>
        <SISMSG>
            <LTR0003E CodErro="EGEN0050">
                <CodMsg>LTR0003</CodMsg>
                <NumCtrlIF>123</NumCtrlIF>
                <ISPBIFDebtd>31680151</ISPBIFDebtd>
                <ISPBIFCredtd>31680152</ISPBIFCredtd>
                <ISPBLTR>31680153</ISPBLTR>
                <NumCtrlLTROr>321</NumCtrlLTROr>
                <AgCredtd>001</AgCredtd>
                <CtCredtd>123456</CtCredtd>
                <VlrLanc>123.0</VlrLanc>
                <SubTpAtv>ACI</SubTpAtv>
                <DescAtv>Test asset description</DescAtv>
                <Hist>Test description</Hist>
                <NivelPref>C</NivelPref>
                <DtMovto>2025-12-04</DtMovto>
            </LTR0003E>
        </SISMSG>
    </DOC>
    """

    ltr0003e = LTR0003E.from_xml(xml)

    assert isinstance(ltr0003e, LTR0003E)
    assert ltr0003e.from_ispb == '31680151'
    assert ltr0003e.to_ispb == '00038166'
    assert ltr0003e.system_domain == 'SPB01'
    assert ltr0003e.operation_number == '316801512509080000001'
    assert ltr0003e.message_code == 'LTR0003'
    assert ltr0003e.institution_control_number == '123'
    assert ltr0003e.debtor_institution_ispb == '31680151'
    assert ltr0003e.creditor_institution_ispb == '31680152'
    assert ltr0003e.ltr_ispb == '31680153'
    assert ltr0003e.original_ltr_control_number == '321'
    assert ltr0003e.branch == '001'
    assert ltr0003e.account_number == '123456'
    assert ltr0003e.amount == Decimal('123.0')
    assert ltr0003e.sub_asset_type == AssetType.INVESTMENT_PORTFOLIO_ASSETS
    assert ltr0003e.asset_description == 'Test asset description'
    assert ltr0003e.description == 'Test description'
    assert ltr0003e.priority == Priority.MEDIUM
    assert ltr0003e.settlement_date == date(2025, 12, 4)
    assert ltr0003e.general_error_code == 'EGEN0050'


def test_ltr0003e_tag_error_from_xml() -> None:
    xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/LTR/LTR0003E.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>316801512509080000001</NUOp>
        </BCMSG>
        <SISMSG>
            <LTR0003E>
                <CodMsg>LTR0003</CodMsg>
                <NumCtrlIF>123</NumCtrlIF>
                <ISPBIFDebtd>31680151</ISPBIFDebtd>
                <ISPBIFCredtd>31680152</ISPBIFCredtd>
                <ISPBLTR CodErro="EGEN0051">31680153</ISPBLTR>
                <NumCtrlLTROr>321</NumCtrlLTROr>
                <AgCredtd>001</AgCredtd>
                <CtCredtd>123456</CtCredtd>
                <VlrLanc>123.0</VlrLanc>
                <SubTpAtv>ACI</SubTpAtv>
                <DescAtv>Test asset description</DescAtv>
                <Hist>Test description</Hist>
                <NivelPref>C</NivelPref>
                <DtMovto>2025-12-04</DtMovto>
            </LTR0003E>
        </SISMSG>
    </DOC>
    """

    ltr0003e = LTR0003E.from_xml(xml)

    assert isinstance(ltr0003e, LTR0003E)
    assert ltr0003e.from_ispb == '31680151'
    assert ltr0003e.to_ispb == '00038166'
    assert ltr0003e.system_domain == 'SPB01'
    assert ltr0003e.operation_number == '316801512509080000001'
    assert ltr0003e.message_code == 'LTR0003'
    assert ltr0003e.institution_control_number == '123'
    assert ltr0003e.debtor_institution_ispb == '31680151'
    assert ltr0003e.creditor_institution_ispb == '31680152'
    assert ltr0003e.ltr_ispb == '31680153'
    assert ltr0003e.original_ltr_control_number == '321'
    assert ltr0003e.branch == '001'
    assert ltr0003e.account_number == '123456'
    assert ltr0003e.amount == Decimal('123.0')
    assert ltr0003e.sub_asset_type == AssetType.INVESTMENT_PORTFOLIO_ASSETS
    assert ltr0003e.asset_description == 'Test asset description'
    assert ltr0003e.description == 'Test description'
    assert ltr0003e.priority == Priority.MEDIUM
    assert ltr0003e.settlement_date == date(2025, 12, 4)
    assert ltr0003e.ltr_ispb_error_code == 'EGEN0051'


def test_ltr0003_roundtrip() -> None:
    params = make_valid_ltr0003_params()

    ltr0003 = LTR0003.model_validate(params)
    xml = ltr0003.to_xml()
    ltr0003_from_xml = LTR0003.from_xml(xml)

    assert ltr0003 == ltr0003_from_xml


def test_ltr0003r1_roundtrip() -> None:
    params = make_valid_ltr0003r1_params()

    ltr0003r1 = LTR0003R1.model_validate(params)
    xml = ltr0003r1.to_xml()
    ltr0003r1_from_xml = LTR0003R1.from_xml(xml)

    assert ltr0003r1 == ltr0003r1_from_xml


def test_ltr0003r2_roundtrip() -> None:
    params = make_valid_ltr0003r2_params()

    ltr0003r2 = LTR0003R2.model_validate(params)
    xml = ltr0003r2.to_xml()
    ltr0003r2_from_xml = LTR0003R2.from_xml(xml)

    assert ltr0003r2 == ltr0003r2_from_xml


def test_ltr0003r3_roundtrip() -> None:
    params = make_valid_ltr0003r3_params()

    ltr0003r3 = LTR0003R3.model_validate(params)
    xml = ltr0003r3.to_xml()
    ltr0003r3_from_xml = LTR0003R3.from_xml(xml)

    assert ltr0003r3 == ltr0003r3_from_xml
