from datetime import date, time
from decimal import Decimal
from typing import Any

import pytest
from pydantic import ValidationError

from sfn_messages.core.types import TransferReturnReason
from sfn_messages.str.str0010 import STR0010
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
                <NumCtrlSTR>STR20250101000000001</NumCtrlSTR>
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
                <NumCtrlSTR>STR20250101000000001</NumCtrlSTR>
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
                <NumCtrlSTR>STR20250101000000001</NumCtrlSTR>
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
                <NumCtrlSTR>STR20250101000000001</NumCtrlSTR>
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
