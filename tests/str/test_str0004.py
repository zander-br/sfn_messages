from datetime import UTC, date, datetime, time
from decimal import Decimal
from typing import Any

import pytest
from pydantic import ValidationError

from sfn_messages.core.types import Priority, StrSettlementStatus
from sfn_messages.str.str0004 import STR0004, STR0004R1
from sfn_messages.str.types import InstitutionPurpose
from tests.conftest import extract_missing_fields, normalize_xml


def make_valid_str0004_params() -> dict[str, Any]:
    return {
        'from_ispb': '31680151',
        'operation_number': '316801512509080000001',
        'system_domain': 'SPB01',
        'to_ispb': '00038166',
        'institution_control_number': '31680151202509090425',
        'debtor_institution_ispb': '31680151',
        'creditor_institution_ispb': '60701190',
        'creditor_branch': '0001',
        'purpose': 'fx_interbank_market',
        'transaction_id': '0000000000000000000000001',
        'amount': 100.00,
        'description': 'Payment for services',
        'scheduled_date': '2025-09-09',
        'scheduled_time': '15:30:00',
        'priority': 'MEDIUM',
        'settlement_date': '2025-09-08',
    }


def make_valid_str0004r1_params() -> dict[str, Any]:
    return {
        'institution_control_number': '31680151202509090425',
        'from_ispb': '31680151',
        'debtor_institution_ispb': '31680151',
        'str_control_number': 'STR20250101000000001',
        'str_settlement_status': 'EFFECTIVE',
        'provider_timestamp': '2025-11-20T15:30:00+00:00',
        'settlement_date': '2025-09-08',
        'operation_number': '316801512509080000001',
        'to_ispb': '00038166',
        'system_domain': 'SPB01',
    }


def test_str0004_valid_params() -> None:
    params = make_valid_str0004_params()
    str0004 = STR0004.model_validate(params)
    assert isinstance(str0004, STR0004)
    assert str0004.from_ispb == '31680151'
    assert str0004.operation_number == '316801512509080000001'
    assert str0004.system_domain == 'SPB01'
    assert str0004.to_ispb == '00038166'
    assert str0004.institution_control_number == '31680151202509090425'
    assert str0004.debtor_institution_ispb == '31680151'
    assert str0004.creditor_institution_ispb == '60701190'
    assert str0004.creditor_branch == '0001'
    assert str0004.purpose == InstitutionPurpose.FX_INTERBANK_MARKET
    assert str0004.transaction_id == '0000000000000000000000001'
    assert str0004.amount == Decimal('100.00')
    assert str0004.description == 'Payment for services'
    assert str0004.scheduled_date == date(2025, 9, 9)
    assert str0004.scheduled_time == time(15, 30)
    assert str0004.priority == Priority.MEDIUM
    assert str0004.settlement_date == date(2025, 9, 8)


def test_str0004_missing_required_fields() -> None:
    with pytest.raises(ValidationError) as exc:
        STR0004.model_validate({})
    missing_fields = extract_missing_fields(exc.value)
    assert missing_fields == {
        'to_ispb',
        'amount',
        'debtor_institution_ispb',
        'institution_control_number',
        'from_ispb',
        'creditor_institution_ispb',
        'description',
        'purpose',
        'system_domain',
        'settlement_date',
        'operation_number',
    }


def test_str0004_to_xml() -> None:
    params = make_valid_str0004_params()
    str0004 = STR0004.model_validate(params)
    xml = str0004.to_xml()

    expected_xml = """
    <DOC>
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>316801512509080000001</NUOp>
        </BCMSG>
        <SISMSG>
            <STR0004>
                <CodMsg>STR0004</CodMsg>
                <NumCtrlIF>31680151202509090425</NumCtrlIF>
                <ISPBIFDebtd>31680151</ISPBIFDebtd>
                <ISPBIFCredtd>60701190</ISPBIFCredtd>
                <AgCredtd>0001</AgCredtd>
                <FinlddIF>1</FinlddIF>
                <CodIdentdTransf>0000000000000000000000001</CodIdentdTransf>
                <VlrLanc>100.0</VlrLanc>
                <Hist>Payment for services</Hist>
                <DtAgendt>2025-09-09</DtAgendt>
                <HrAgendt>15:30:00</HrAgendt>
                <NivelPref>C</NivelPref>
                <DtMovto>2025-09-08</DtMovto>
            </STR0004>
        </SISMSG>
    </DOC>
    """

    assert normalize_xml(expected_xml) == normalize_xml(xml)


def test_str0004_to_xml_omit_optional_fields() -> None:
    params = make_valid_str0004_params()
    del params['creditor_branch']
    del params['transaction_id']
    del params['scheduled_date']
    del params['scheduled_time']
    del params['priority']

    str0004 = STR0004.model_validate(params)
    xml = str0004.to_xml()

    expected_xml = """
    <DOC>
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>316801512509080000001</NUOp>
        </BCMSG>
        <SISMSG>
            <STR0004>
                <CodMsg>STR0004</CodMsg>
                <NumCtrlIF>31680151202509090425</NumCtrlIF>
                <ISPBIFDebtd>31680151</ISPBIFDebtd>
                <ISPBIFCredtd>60701190</ISPBIFCredtd>
                <FinlddIF>1</FinlddIF>
                <VlrLanc>100.0</VlrLanc>
                <Hist>Payment for services</Hist>
                <DtMovto>2025-09-08</DtMovto>
            </STR0004>
        </SISMSG>
    </DOC>
    """

    assert normalize_xml(expected_xml) == normalize_xml(xml)


def test_str0004_from_xml() -> None:
    xml = """
    <DOC>
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>316801512509080000001</NUOp>
        </BCMSG>
        <SISMSG>
            <STR0004>
                <CodMsg>STR0004</CodMsg>
                <NumCtrlIF>31680151202509090425</NumCtrlIF>
                <ISPBIFDebtd>31680151</ISPBIFDebtd>
                <ISPBIFCredtd>60701190</ISPBIFCredtd>
                <AgCredtd>0001</AgCredtd>
                <FinlddIF>1</FinlddIF>
                <CodIdentdTransf>0000000000000000000000001</CodIdentdTransf>
                <VlrLanc>100.0</VlrLanc>
                <Hist>Payment for services</Hist>
                <DtAgendt>2025-09-09</DtAgendt>
                <HrAgendt>15:30:00</HrAgendt>
                <NivelPref>C</NivelPref>
                <DtMovto>2025-09-08</DtMovto>
            </STR0004>
        </SISMSG>
    </DOC>
    """

    str0004 = STR0004.from_xml(xml)

    assert isinstance(str0004, STR0004)
    assert str0004.from_ispb == '31680151'
    assert str0004.operation_number == '316801512509080000001'
    assert str0004.system_domain == 'SPB01'
    assert str0004.to_ispb == '00038166'
    assert str0004.institution_control_number == '31680151202509090425'
    assert str0004.debtor_institution_ispb == '31680151'
    assert str0004.creditor_institution_ispb == '60701190'
    assert str0004.creditor_branch == '0001'
    assert str0004.purpose == InstitutionPurpose.FX_INTERBANK_MARKET
    assert str0004.transaction_id == '0000000000000000000000001'
    assert str0004.amount == Decimal('100.0')
    assert str0004.description == 'Payment for services'
    assert str0004.scheduled_date == date(2025, 9, 9)
    assert str0004.scheduled_time == time(15, 30)
    assert str0004.priority == Priority.MEDIUM
    assert str0004.settlement_date == date(2025, 9, 8)


def test_str0004_from_xml_missing_optional_fields() -> None:
    xml = """
    <DOC>
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>316801512509080000001</NUOp>
        </BCMSG>
        <SISMSG>
            <STR0004>
                <CodMsg>STR0004</CodMsg>
                <NumCtrlIF>31680151202509090425</NumCtrlIF>
                <ISPBIFDebtd>31680151</ISPBIFDebtd>
                <ISPBIFCredtd>60701190</ISPBIFCredtd>
                <FinlddIF>1</FinlddIF>
                <VlrLanc>100.0</VlrLanc>
                <Hist>Payment for services</Hist>
                <DtMovto>2025-09-08</DtMovto>
            </STR0004>
        </SISMSG>
    </DOC>
    """

    str0004 = STR0004.from_xml(xml)

    assert isinstance(str0004, STR0004)
    assert str0004.from_ispb == '31680151'
    assert str0004.operation_number == '316801512509080000001'
    assert str0004.system_domain == 'SPB01'
    assert str0004.to_ispb == '00038166'
    assert str0004.institution_control_number == '31680151202509090425'
    assert str0004.debtor_institution_ispb == '31680151'
    assert str0004.creditor_institution_ispb == '60701190'
    assert str0004.creditor_branch is None
    assert str0004.purpose == InstitutionPurpose.FX_INTERBANK_MARKET
    assert str0004.transaction_id is None
    assert str0004.amount == Decimal('100.00')
    assert str0004.description == 'Payment for services'
    assert str0004.scheduled_date is None
    assert str0004.scheduled_time is None
    assert str0004.priority is None
    assert str0004.settlement_date == date(2025, 9, 8)


def test_str0004_roundtrip() -> None:
    params = make_valid_str0004_params()
    str0004 = STR0004.model_validate(params)
    xml = str0004.to_xml()
    str0004_from_xml = STR0004.from_xml(xml)
    assert str0004 == str0004_from_xml


def test_str0004_from_xml_missing_required_fields() -> None:
    xml = """
    <DOC>
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>316801512509080000001</NUOp>
        </BCMSG>
        <SISMSG>
            <STR0004>
                <CodMsg>STR0004</CodMsg>
            </STR0004>
        </SISMSG>
    </DOC>
    """

    with pytest.raises(ValidationError) as exc:
        STR0004.from_xml(xml)
    missing_fields = extract_missing_fields(exc.value)
    assert missing_fields == {
        'settlement_date',
        'creditor_institution_ispb',
        'description',
        'debtor_institution_ispb',
        'amount',
        'institution_control_number',
        'purpose',
    }


def test_str0008r1_valid_model() -> None:
    params = make_valid_str0004r1_params()
    str0004r1 = STR0004R1.model_validate(params)
    assert isinstance(str0004r1, STR0004R1)
    assert str0004r1.debtor_institution_ispb == '31680151'
    assert str0004r1.from_ispb == '31680151'
    assert str0004r1.institution_control_number == '31680151202509090425'
    assert str0004r1.message_code == 'STR0004R1'
    assert str0004r1.operation_number == '316801512509080000001'
    assert str0004r1.settlement_date == date(2025, 9, 8)
    assert str0004r1.provider_timestamp == datetime(2025, 11, 20, 15, 30, tzinfo=UTC)
    assert str0004r1.str_control_number == 'STR20250101000000001'
    assert str0004r1.str_settlement_status == StrSettlementStatus.EFFECTIVE
    assert str0004r1.to_ispb == '00038166'
    assert str0004r1.system_domain == 'SPB01'


def test_str0004r1_missing_required_fields() -> None:
    with pytest.raises(ValidationError) as exc:
        STR0004R1.model_validate({})
    missing_fields = extract_missing_fields(exc.value)
    assert missing_fields == {
        'to_ispb',
        'str_control_number',
        'provider_timestamp',
        'str_settlement_status',
        'institution_control_number',
        'debtor_institution_ispb',
        'system_domain',
        'operation_number',
        'from_ispb',
        'settlement_date',
    }


def test_str0004r1_to_xml() -> None:
    params = make_valid_str0004r1_params()
    str0004r1 = STR0004R1.model_validate(params)
    xml = str0004r1.to_xml()

    expected_xml = """<?xml version="1.0"?>
    <DOC>
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>316801512509080000001</NUOp>
        </BCMSG>
        <SISMSG>
            <STR0004R1>
                <CodMsg>STR0004R1</CodMsg>
                <NumCtrlIF>31680151202509090425</NumCtrlIF>
                <ISPBIFDebtd>31680151</ISPBIFDebtd>
                <NumCtrlSTR>STR20250101000000001</NumCtrlSTR>
                <SitLancSTR>1</SitLancSTR>
                <DtHrSit>2025-11-20 15:30:00+00:00</DtHrSit>
                <DtMovto>2025-09-08</DtMovto>
            </STR0004R1>
        </SISMSG>
    </DOC>
    """

    assert normalize_xml(expected_xml) == normalize_xml(xml)


def test_str0008r1_from_xml() -> None:
    xml = """<?xml version="1.0"?>
    <DOC>
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>316801512509080000001</NUOp>
        </BCMSG>
        <SISMSG>
            <STR0004R1>
                <CodMsg>STR0004R1</CodMsg>
                <NumCtrlIF>31680151202509090425</NumCtrlIF>
                <ISPBIFDebtd>31680151</ISPBIFDebtd>
                <NumCtrlSTR>STR20250101000000001</NumCtrlSTR>
                <SitLancSTR>1</SitLancSTR>
                <DtHrSit>2025-11-20 15:30:00+00:00</DtHrSit>
                <DtMovto>2025-09-08</DtMovto>
            </STR0004R1>
        </SISMSG>
    </DOC>
    """

    str0004r1 = STR0004R1.from_xml(xml)
    assert isinstance(str0004r1, STR0004R1)
    assert str0004r1.debtor_institution_ispb == '31680151'
    assert str0004r1.from_ispb == '31680151'
    assert str0004r1.institution_control_number == '31680151202509090425'
    assert str0004r1.message_code == 'STR0004R1'
    assert str0004r1.operation_number == '316801512509080000001'
    assert str0004r1.settlement_date == date(2025, 9, 8)
    assert str0004r1.provider_timestamp == datetime(2025, 11, 20, 15, 30, tzinfo=UTC)
    assert str0004r1.str_control_number == 'STR20250101000000001'
    assert str0004r1.str_settlement_status == StrSettlementStatus.EFFECTIVE
    assert str0004r1.to_ispb == '00038166'
    assert str0004r1.system_domain == 'SPB01'


def test_str0004r1_roundtrip() -> None:
    params = make_valid_str0004r1_params()
    str0004r1 = STR0004R1.model_validate(params)
    xml = str0004r1.to_xml()
    str0008r1_from_xml = STR0004R1.from_xml(xml)
    assert str0004r1 == str0008r1_from_xml


def test_str0004r1_from_xml_missing_required_fields() -> None:
    xml = """<?xml version="1.0"?>
    <DOC>
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>316801512509080000001</NUOp>
        </BCMSG>
        <SISMSG>
            <STR0004R1>
                <CodMsg>STR0004R1</CodMsg>
            </STR0004R1>
        </SISMSG>
    </DOC>
    """

    with pytest.raises(ValidationError) as exc:
        STR0004R1.from_xml(xml)
    missing_fields = extract_missing_fields(exc.value)
    assert missing_fields == {
        'settlement_date',
        'debtor_institution_ispb',
        'str_settlement_status',
        'str_control_number',
        'institution_control_number',
        'provider_timestamp',
    }
