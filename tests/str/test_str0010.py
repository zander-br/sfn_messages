from datetime import UTC, date, datetime, time
from decimal import Decimal
from typing import Any

import pytest
from pydantic import ValidationError

from sfn_messages.core.types import StrSettlementStatus, TransferReturnReason
from sfn_messages.str.str0010 import STR0010, STR0010R1, STR0010R2
from tests.conftest import extract_missing_fields, normalize_xml


def make_valid_str0010_params() -> dict[str, Any]:
    return {
        'from_ispb': '31680151',
        'operation_number': '316801512509080000001',
        'system_domain': 'SPB01',
        'to_ispb': '00038166',
        'institution_control_number': '31680151202509090425',
        'debtor_institution_ispb': '31680151',
        'creditor_institution_ispb': '60701190',
        'amount': 100.00,
        'transfer_return_reason': 'DESTINATION_ACCOUNT_CLOSED',
        'original_str_control_number': 'STR20250101000000001',
        'description': 'Return Payment for services',
        'scheduled_date': '2025-09-09',
        'scheduled_time': '15:30:00',
        'priority': 'MEDIUM',
        'settlement_date': '2025-09-08',
    }


def make_valid_str0010r1_params() -> dict[str, Any]:
    return {
        'institution_control_number': '31680151202509090425',
        'from_ispb': '31680151',
        'debtor_institution_ispb': '31680151',
        'str_control_number': 'STR20250101000000001',
        'str_settlement_status': 'EFFECTIVE',
        'settlement_timestamp': '2025-11-20T15:30:00+00:00',
        'settlement_date': '2025-09-08',
        'operation_number': '316801512509080000001',
        'to_ispb': '00038166',
        'system_domain': 'SPB01',
    }


def make_valid_str0010r2_params() -> dict[str, Any]:
    return {
        'from_ispb': '31680151',
        'operation_number': '316801512509080000001',
        'system_domain': 'SPB01',
        'to_ispb': '00038166',
        'debtor_institution_ispb': '31680151',
        'creditor_institution_ispb': '60701190',
        'amount': 100.00,
        'transfer_return_reason': 'DESTINATION_ACCOUNT_CLOSED',
        'original_str_control_number': 'STR20250101000000001',
        'str_control_number': 'STR20250101000000002',
        'description': 'Return Payment for services',
        'settlement_date': '2025-09-08',
        'vendor_timestamp': '2025-11-20T15:30:00+00:00',
    }


def test_str0010_valid_params() -> None:
    params = make_valid_str0010_params()
    str0010 = STR0010.model_validate(params)
    assert isinstance(str0010, STR0010)
    assert str0010.from_ispb == '31680151'
    assert str0010.operation_number == '316801512509080000001'
    assert str0010.system_domain == 'SPB01'
    assert str0010.to_ispb == '00038166'
    assert str0010.institution_control_number == '31680151202509090425'
    assert str0010.debtor_institution_ispb == '31680151'
    assert str0010.creditor_institution_ispb == '60701190'
    assert str0010.amount == Decimal('100.00')
    assert str0010.transfer_return_reason == TransferReturnReason.DESTINATION_ACCOUNT_CLOSED
    assert str0010.original_str_control_number == 'STR20250101000000001'
    assert str0010.description == 'Return Payment for services'
    assert str0010.scheduled_date == date(2025, 9, 9)
    assert str0010.scheduled_time == time(15, 30, 0)
    assert str0010.priority == 'MEDIUM'
    assert str0010.settlement_date == date(2025, 9, 8)


def test_str0010_missing_required_fields() -> None:
    with pytest.raises(ValidationError) as exc:
        STR0010.model_validate({})

    missing_fields = extract_missing_fields(exc.value)
    assert missing_fields == {
        'settlement_date',
        'from_ispb',
        'operation_number',
        'transfer_return_reason',
        'creditor_institution_ispb',
        'amount',
        'original_str_control_number',
        'institution_control_number',
        'debtor_institution_ispb',
        'system_domain',
        'to_ispb',
    }


def test_str0010_to_xml() -> None:
    params = make_valid_str0010_params()
    str0010 = STR0010.model_validate(params)
    xml = str0010.to_xml()

    expected_xml = """
    <DOC>
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>316801512509080000001</NUOp>
        </BCMSG>
        <SISMSG>
            <STR0010>
                <CodMsg>STR0010</CodMsg>
                <NumCtrlIF>31680151202509090425</NumCtrlIF>
                <ISPBIFDebtd>31680151</ISPBIFDebtd>
                <ISPBIFCredtd>60701190</ISPBIFCredtd>
                <VlrLanc>100.0</VlrLanc>
                <CodDevTransf>1</CodDevTransf>
                <NumCtrlSTROr>STR20250101000000001</NumCtrlSTROr>
                <Hist>Return Payment for services</Hist>
                <DtAgendt>2025-09-09</DtAgendt>
                <HrAgendt>15:30:00</HrAgendt>
                <NivelPref>C</NivelPref>
                <DtMovto>2025-09-08</DtMovto>
            </STR0010>
        </SISMSG>
    </DOC>
    """

    assert normalize_xml(expected_xml) == normalize_xml(xml)


def test_str0010_to_xml_omit_optional_fields() -> None:
    params = make_valid_str0010_params()
    del params['description']
    del params['scheduled_date']
    del params['scheduled_time']
    del params['priority']
    str0010 = STR0010.model_validate(params)
    xml = str0010.to_xml()

    expected_xml = """
    <DOC>
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>316801512509080000001</NUOp>
        </BCMSG>
        <SISMSG>
            <STR0010>
                <CodMsg>STR0010</CodMsg>
                <NumCtrlIF>31680151202509090425</NumCtrlIF>
                <ISPBIFDebtd>31680151</ISPBIFDebtd>
                <ISPBIFCredtd>60701190</ISPBIFCredtd>
                <VlrLanc>100.0</VlrLanc>
                <CodDevTransf>1</CodDevTransf>
                <NumCtrlSTROr>STR20250101000000001</NumCtrlSTROr>
                <DtMovto>2025-09-08</DtMovto>
            </STR0010>
        </SISMSG>
    </DOC>
    """

    assert normalize_xml(expected_xml) == normalize_xml(xml)


def test_str0010_from_xml() -> None:
    xml = """
    <DOC>
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>316801512509080000001</NUOp>
        </BCMSG>
        <SISMSG>
            <STR0010>
                <CodMsg>STR0010</CodMsg>
                <NumCtrlIF>31680151202509090425</NumCtrlIF>
                <ISPBIFDebtd>31680151</ISPBIFDebtd>
                <ISPBIFCredtd>60701190</ISPBIFCredtd>
                <VlrLanc>100.0</VlrLanc>
                <CodDevTransf>1</CodDevTransf>
                <NumCtrlSTROr>STR20250101000000001</NumCtrlSTROr>
                <Hist>Return Payment for services</Hist>
                <DtAgendt>2025-09-09</DtAgendt>
                <HrAgendt>15:30:00</HrAgendt>
                <NivelPref>C</NivelPref>
                <DtMovto>2025-09-08</DtMovto>
            </STR0010>
        </SISMSG>
    </DOC>
    """

    str0010 = STR0010.from_xml(xml)
    assert isinstance(str0010, STR0010)
    assert str0010.from_ispb == '31680151'
    assert str0010.operation_number == '316801512509080000001'
    assert str0010.system_domain == 'SPB01'
    assert str0010.to_ispb == '00038166'
    assert str0010.institution_control_number == '31680151202509090425'
    assert str0010.debtor_institution_ispb == '31680151'
    assert str0010.creditor_institution_ispb == '60701190'
    assert str0010.amount == Decimal('100.0')
    assert str0010.transfer_return_reason == TransferReturnReason.DESTINATION_ACCOUNT_CLOSED
    assert str0010.original_str_control_number == 'STR20250101000000001'
    assert str0010.description == 'Return Payment for services'
    assert str0010.scheduled_date == date(2025, 9, 9)
    assert str0010.scheduled_time == time(15, 30, 0)
    assert str0010.priority == 'MEDIUM'
    assert str0010.settlement_date == date(2025, 9, 8)


def test_str0010_from_xml_omit_optional_fields() -> None:
    xml = """
    <DOC>
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>316801512509080000001</NUOp>
        </BCMSG>
        <SISMSG>
            <STR0010>
                <CodMsg>STR0010</CodMsg>
                <NumCtrlIF>31680151202509090425</NumCtrlIF>
                <ISPBIFDebtd>31680151</ISPBIFDebtd>
                <ISPBIFCredtd>60701190</ISPBIFCredtd>
                <VlrLanc>100.0</VlrLanc>
                <CodDevTransf>1</CodDevTransf>
                <NumCtrlSTROr>STR20250101000000001</NumCtrlSTROr>
                <DtMovto>2025-09-08</DtMovto>
            </STR0010>
        </SISMSG>
    </DOC>
    """

    str0010 = STR0010.from_xml(xml)
    assert isinstance(str0010, STR0010)
    assert str0010.from_ispb == '31680151'
    assert str0010.operation_number == '316801512509080000001'
    assert str0010.system_domain == 'SPB01'
    assert str0010.to_ispb == '00038166'
    assert str0010.institution_control_number == '31680151202509090425'
    assert str0010.debtor_institution_ispb == '31680151'
    assert str0010.creditor_institution_ispb == '60701190'
    assert str0010.amount == Decimal('100.0')
    assert str0010.transfer_return_reason == TransferReturnReason.DESTINATION_ACCOUNT_CLOSED
    assert str0010.original_str_control_number == 'STR20250101000000001'
    assert str0010.description is None
    assert str0010.scheduled_date is None
    assert str0010.scheduled_time is None
    assert str0010.priority is None
    assert str0010.settlement_date == date(2025, 9, 8)


def test_str0010_roundtrip() -> None:
    params = make_valid_str0010_params()
    str0010 = STR0010.model_validate(params)
    xml = str0010.to_xml()
    str0010_from_xml = STR0010.from_xml(xml)
    assert str0010 == str0010_from_xml


def test_str0010_from_xml_missing_required_fields() -> None:
    xml = """
    <DOC>
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>316801512509080000001</NUOp>
        </BCMSG>
        <SISMSG>
            <STR0010>
                <CodMsg>STR0010</CodMsg>
            </STR0010>
        </SISMSG>
    </DOC>
    """

    with pytest.raises(ValidationError) as exc:
        STR0010.from_xml(xml)

    missing_fields = extract_missing_fields(exc.value)
    assert missing_fields == {
        'settlement_date',
        'institution_control_number',
        'debtor_institution_ispb',
        'creditor_institution_ispb',
        'amount',
        'transfer_return_reason',
        'original_str_control_number',
    }


def test_str0010r1_valid_model() -> None:
    params = make_valid_str0010r1_params()
    str0010r1 = STR0010R1.model_validate(params)
    assert isinstance(str0010r1, STR0010R1)
    assert str0010r1.debtor_institution_ispb == '31680151'
    assert str0010r1.from_ispb == '31680151'
    assert str0010r1.institution_control_number == '31680151202509090425'
    assert str0010r1.message_code == 'STR0010R1'
    assert str0010r1.operation_number == '316801512509080000001'
    assert str0010r1.settlement_date == date(2025, 9, 8)
    assert str0010r1.settlement_timestamp == datetime(2025, 11, 20, 15, 30, tzinfo=UTC)
    assert str0010r1.str_control_number == 'STR20250101000000001'
    assert str0010r1.str_settlement_status == StrSettlementStatus.EFFECTIVE
    assert str0010r1.to_ispb == '00038166'
    assert str0010r1.system_domain == 'SPB01'


def test_str0010r1_missing_required_fields() -> None:
    with pytest.raises(ValidationError) as exc:
        STR0010R1.model_validate({})
    missing_fields = extract_missing_fields(exc.value)
    assert missing_fields == {
        'to_ispb',
        'str_control_number',
        'settlement_timestamp',
        'str_settlement_status',
        'institution_control_number',
        'debtor_institution_ispb',
        'system_domain',
        'operation_number',
        'from_ispb',
        'settlement_date',
    }


def test_str0010r1_to_xml() -> None:
    params = make_valid_str0010r1_params()
    str0010r1 = STR0010R1.model_validate(params)
    xml = str0010r1.to_xml()

    expected_xml = """<?xml version="1.0"?>
    <DOC>
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>316801512509080000001</NUOp>
        </BCMSG>
        <SISMSG>
            <STR0010R1>
                <CodMsg>STR0010R1</CodMsg>
                <NumCtrlIF>31680151202509090425</NumCtrlIF>
                <ISPBIFDebtd>31680151</ISPBIFDebtd>
                <NumCtrlSTR>STR20250101000000001</NumCtrlSTR>
                <SitLancSTR>1</SitLancSTR>
                <DtHrSit>2025-11-20 15:30:00+00:00</DtHrSit>
                <DtMovto>2025-09-08</DtMovto>
            </STR0010R1>
        </SISMSG>
    </DOC>
    """

    assert normalize_xml(expected_xml) == normalize_xml(xml)


def test_str0010r1_from_xml() -> None:
    xml = """<?xml version="1.0"?>
    <DOC>
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>316801512509080000001</NUOp>
        </BCMSG>
        <SISMSG>
            <STR0010R1>
                <CodMsg>STR0010R1</CodMsg>
                <NumCtrlIF>31680151202509090425</NumCtrlIF>
                <ISPBIFDebtd>31680151</ISPBIFDebtd>
                <NumCtrlSTR>STR20250101000000001</NumCtrlSTR>
                <SitLancSTR>1</SitLancSTR>
                <DtHrSit>2025-11-20 15:30:00+00:00</DtHrSit>
                <DtMovto>2025-09-08</DtMovto>
            </STR0010R1>
        </SISMSG>
    </DOC>
    """

    str0010r1 = STR0010R1.from_xml(xml)
    assert isinstance(str0010r1, STR0010R1)
    assert str0010r1.debtor_institution_ispb == '31680151'
    assert str0010r1.from_ispb == '31680151'
    assert str0010r1.institution_control_number == '31680151202509090425'
    assert str0010r1.message_code == 'STR0010R1'
    assert str0010r1.operation_number == '316801512509080000001'
    assert str0010r1.settlement_date == date(2025, 9, 8)
    assert str0010r1.settlement_timestamp == datetime(2025, 11, 20, 15, 30, tzinfo=UTC)
    assert str0010r1.str_control_number == 'STR20250101000000001'
    assert str0010r1.str_settlement_status == StrSettlementStatus.EFFECTIVE
    assert str0010r1.to_ispb == '00038166'
    assert str0010r1.system_domain == 'SPB01'


def test_str0010r1_roundtrip() -> None:
    params = make_valid_str0010r1_params()
    str0010r1 = STR0010R1.model_validate(params)
    xml = str0010r1.to_xml()
    str0010r1_from_xml = STR0010R1.from_xml(xml)
    assert str0010r1 == str0010r1_from_xml


def test_str0010r1_from_xml_missing_required_fields() -> None:
    xml = """<?xml version="1.0"?>
    <DOC>
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>316801512509080000001</NUOp>
        </BCMSG>
        <SISMSG>
            <STR0010R1>
                <CodMsg>STR0010R1</CodMsg>
            </STR0010R1>
        </SISMSG>
    </DOC>
    """

    with pytest.raises(ValidationError) as exc:
        STR0010R1.from_xml(xml)
    missing_fields = extract_missing_fields(exc.value)
    assert missing_fields == {
        'settlement_date',
        'debtor_institution_ispb',
        'str_settlement_status',
        'str_control_number',
        'institution_control_number',
        'settlement_timestamp',
    }


def test_str0010r2_valid_params() -> None:
    params = make_valid_str0010r2_params()
    str0010r2 = STR0010R2.model_validate(params)
    assert isinstance(str0010r2, STR0010R2)
    assert str0010r2.from_ispb == '31680151'
    assert str0010r2.operation_number == '316801512509080000001'
    assert str0010r2.system_domain == 'SPB01'
    assert str0010r2.to_ispb == '00038166'
    assert str0010r2.debtor_institution_ispb == '31680151'
    assert str0010r2.creditor_institution_ispb == '60701190'
    assert str0010r2.amount == Decimal('100.00')
    assert str0010r2.transfer_return_reason == TransferReturnReason.DESTINATION_ACCOUNT_CLOSED
    assert str0010r2.original_str_control_number == 'STR20250101000000001'
    assert str0010r2.str_control_number == 'STR20250101000000002'
    assert str0010r2.vendor_timestamp == datetime(2025, 11, 20, 15, 30, tzinfo=UTC)
    assert str0010r2.description == 'Return Payment for services'
    assert str0010r2.settlement_date == date(2025, 9, 8)


def test_str0010r2_missing_required_fields() -> None:
    with pytest.raises(ValidationError) as exc:
        STR0010R2.model_validate({})
    missing_fields = extract_missing_fields(exc.value)
    assert missing_fields == {
        'to_ispb',
        'str_control_number',
        'vendor_timestamp',
        'debtor_institution_ispb',
        'system_domain',
        'operation_number',
        'from_ispb',
        'settlement_date',
        'creditor_institution_ispb',
        'amount',
        'transfer_return_reason',
        'original_str_control_number',
    }


def test_str0010r2_to_xml() -> None:
    params = make_valid_str0010r2_params()
    str0010r2 = STR0010R2.model_validate(params)
    xml = str0010r2.to_xml()

    expected_xml = """<?xml version="1.0"?>
    <DOC>
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>316801512509080000001</NUOp>
        </BCMSG>
        <SISMSG>
            <STR0010R2>
                <CodMsg>STR0010R2</CodMsg>
                <NumCtrlSTR>STR20250101000000002</NumCtrlSTR>
                <DtHrBC>2025-11-20 15:30:00+00:00</DtHrBC>
                <ISPBIFDebtd>31680151</ISPBIFDebtd>
                <ISPBIFCredtd>60701190</ISPBIFCredtd>
                <VlrLanc>100.0</VlrLanc>
                <CodDevTransf>1</CodDevTransf>
                <NumCtrlSTROr>STR20250101000000001</NumCtrlSTROr>
                <Hist>Return Payment for services</Hist>
                <DtMovto>2025-09-08</DtMovto>
            </STR0010R2>
        </SISMSG>
    </DOC>
    """

    assert normalize_xml(expected_xml) == normalize_xml(xml)


def test_str0010r2_to_xml_omit_optional_fields() -> None:
    params = make_valid_str0010r2_params()
    del params['description']
    str0010r2 = STR0010R2.model_validate(params)
    xml = str0010r2.to_xml()

    expected_xml = """<?xml version="1.0"?>
    <DOC>
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>316801512509080000001</NUOp>
        </BCMSG>
        <SISMSG>
            <STR0010R2>
                <CodMsg>STR0010R2</CodMsg>
                <NumCtrlSTR>STR20250101000000002</NumCtrlSTR>
                <DtHrBC>2025-11-20 15:30:00+00:00</DtHrBC>
                <ISPBIFDebtd>31680151</ISPBIFDebtd>
                <ISPBIFCredtd>60701190</ISPBIFCredtd>
                <VlrLanc>100.0</VlrLanc>
                <CodDevTransf>1</CodDevTransf>
                <NumCtrlSTROr>STR20250101000000001</NumCtrlSTROr>
                <DtMovto>2025-09-08</DtMovto>
            </STR0010R2>
        </SISMSG>
    </DOC>
    """

    assert normalize_xml(expected_xml) == normalize_xml(xml)


def test_str0010r2_from_xml() -> None:
    xml = """<?xml version="1.0"?>
    <DOC>
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>316801512509080000001</NUOp>
        </BCMSG>
        <SISMSG>
            <STR0010R2>
                <CodMsg>STR0010R2</CodMsg>
                <NumCtrlSTR>STR20250101000000002</NumCtrlSTR>
                <DtHrBC>2025-11-20 15:30:00+00:00</DtHrBC>
                <ISPBIFDebtd>31680151</ISPBIFDebtd>
                <ISPBIFCredtd>60701190</ISPBIFCredtd>
                <VlrLanc>100.0</VlrLanc>
                <CodDevTransf>1</CodDevTransf>
                <NumCtrlSTROr>STR20250101000000001</NumCtrlSTROr>
                <Hist>Return Payment for services</Hist>
                <DtMovto>2025-09-08</DtMovto>
            </STR0010R2>
        </SISMSG>
    </DOC>
    """

    str0010r2 = STR0010R2.from_xml(xml)
    assert isinstance(str0010r2, STR0010R2)
    assert str0010r2.from_ispb == '31680151'
    assert str0010r2.operation_number == '316801512509080000001'
    assert str0010r2.system_domain == 'SPB01'
    assert str0010r2.to_ispb == '00038166'
    assert str0010r2.debtor_institution_ispb == '31680151'
    assert str0010r2.creditor_institution_ispb == '60701190'
    assert str0010r2.amount == Decimal('100.0')
    assert str0010r2.transfer_return_reason == TransferReturnReason.DESTINATION_ACCOUNT_CLOSED
    assert str0010r2.original_str_control_number == 'STR20250101000000001'
    assert str0010r2.str_control_number == 'STR20250101000000002'
    assert str0010r2.vendor_timestamp == datetime(2025, 11, 20, 15, 30, tzinfo=UTC)
    assert str0010r2.description == 'Return Payment for services'
    assert str0010r2.settlement_date == date(2025, 9, 8)


def test_str0010r2_from_xml_omit_optional_fields() -> None:
    xml = """<?xml version="1.0"?>
    <DOC>
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>316801512509080000001</NUOp>
        </BCMSG>
        <SISMSG>
            <STR0010R2>
                <CodMsg>STR0010R2</CodMsg>
                <NumCtrlSTR>STR20250101000000002</NumCtrlSTR>
                <DtHrBC>2025-11-20 15:30:00+00:00</DtHrBC>
                <ISPBIFDebtd>31680151</ISPBIFDebtd>
                <ISPBIFCredtd>60701190</ISPBIFCredtd>
                <VlrLanc>100.0</VlrLanc>
                <CodDevTransf>1</CodDevTransf>
                <NumCtrlSTROr>STR20250101000000001</NumCtrlSTROr>
                <DtMovto>2025-09-08</DtMovto>
            </STR0010R2>
        </SISMSG>
    </DOC>
    """
    str0010r2 = STR0010R2.from_xml(xml)
    assert isinstance(str0010r2, STR0010R2)
    assert str0010r2.from_ispb == '31680151'
    assert str0010r2.operation_number == '316801512509080000001'
    assert str0010r2.system_domain == 'SPB01'
    assert str0010r2.to_ispb == '00038166'
    assert str0010r2.debtor_institution_ispb == '31680151'
    assert str0010r2.creditor_institution_ispb == '60701190'
    assert str0010r2.amount == Decimal('100.0')
    assert str0010r2.transfer_return_reason == TransferReturnReason.DESTINATION_ACCOUNT_CLOSED
    assert str0010r2.original_str_control_number == 'STR20250101000000001'
    assert str0010r2.str_control_number == 'STR20250101000000002'
    assert str0010r2.vendor_timestamp == datetime(2025, 11, 20, 15, 30, tzinfo=UTC)
    assert str0010r2.description is None
    assert str0010r2.settlement_date == date(2025, 9, 8)


def test_str0010r2_roundtrip() -> None:
    params = make_valid_str0010r2_params()
    str0010r2 = STR0010R2.model_validate(params)
    xml = str0010r2.to_xml()
    str0010r2_from_xml = STR0010R2.from_xml(xml)
    assert str0010r2 == str0010r2_from_xml


def test_str0010r2_from_xml_missing_required_fields() -> None:
    xml = """<?xml version="1.0"?>
    <DOC>
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>316801512509080000001</NUOp>
        </BCMSG>
        <SISMSG>
            <STR0010R2>
                <CodMsg>STR0010R2</CodMsg>
            </STR0010R2>
        </SISMSG>
    </DOC>
    """

    with pytest.raises(ValidationError) as exc:
        STR0010R2.from_xml(xml)

    missing_fields = extract_missing_fields(exc.value)
    assert missing_fields == {
        'creditor_institution_ispb',
        'transfer_return_reason',
        'vendor_timestamp',
        'original_str_control_number',
        'amount',
        'debtor_institution_ispb',
        'settlement_date',
        'str_control_number',
    }
