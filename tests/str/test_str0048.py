from datetime import date, time
from decimal import Decimal
from typing import Any

import pytest
from pydantic import ValidationError

from sfn_messages.core.types import Priority
from sfn_messages.str.str0048 import STR0048
from sfn_messages.str.types import PortabilityReturnReason
from tests.conftest import extract_missing_fields, normalize_xml


def make_valid_str0048_params() -> dict[str, Any]:
    return {
        'from_ispb': '31680151',
        'operation_number': '316801512509080000001',
        'system_domain': 'SPB01',
        'to_ispb': '00038166',
        'institution_control_number': '31680151202509090425',
        'debtor_institution_ispb': '31680151',
        'creditor_institution_ispb': '00038166',
        'amount': 100.00,
        'portability_return_reason': 'DESTINATION_ACCOUNT_CLOSED',
        'original_str_control_number': 'STR20250101000000001',
        'provider_ispb': '31680151',
        'description': 'Payment for services',
        'scheduled_date': '2025-09-08',
        'scheduled_time': '15:30:00',
        'priority': 'MEDIUM',
        'settlement_date': '2025-09-08',
    }


def test_str0048_valid_params() -> None:
    params = make_valid_str0048_params()
    str0048 = STR0048.model_validate(params)
    assert isinstance(str0048, STR0048)
    assert str0048.from_ispb == '31680151'
    assert str0048.operation_number == '316801512509080000001'
    assert str0048.system_domain == 'SPB01'
    assert str0048.to_ispb == '00038166'
    assert str0048.institution_control_number == '31680151202509090425'
    assert str0048.debtor_institution_ispb == '31680151'
    assert str0048.creditor_institution_ispb == '00038166'
    assert str0048.amount == Decimal('100.00')
    assert str0048.portability_return_reason == PortabilityReturnReason.DESTINATION_ACCOUNT_CLOSED
    assert str0048.original_str_control_number == 'STR20250101000000001'
    assert str0048.provider_ispb == '31680151'
    assert str0048.description == 'Payment for services'
    assert str0048.scheduled_date == date(2025, 9, 8)
    assert str0048.scheduled_time == time(15, 30, 0)
    assert str0048.priority == Priority.MEDIUM
    assert str0048.settlement_date == date(2025, 9, 8)


def test_str0048_missing_required_fields() -> None:
    with pytest.raises(ValidationError) as exc:
        STR0048.model_validate({})

    missing_fields = extract_missing_fields(exc.value)
    assert missing_fields == {
        'institution_control_number',
        'from_ispb',
        'amount',
        'provider_ispb',
        'system_domain',
        'debtor_institution_ispb',
        'creditor_institution_ispb',
        'original_str_control_number',
        'operation_number',
        'settlement_date',
        'portability_return_reason',
        'to_ispb',
    }


def test_str0048_to_xml() -> None:
    params = make_valid_str0048_params()
    str0048 = STR0048.model_validate(params)
    xml = str0048.to_xml()

    expected_xml = """
    <DOC>
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>316801512509080000001</NUOp>
        </BCMSG>
        <SISMSG>
            <STR0008>
                <CodMsg>STR0048</CodMsg>
                <NumCtrlIF>31680151202509090425</NumCtrlIF>
                <ISPBIFDebtd>31680151</ISPBIFDebtd>
                <ISPBIFCredtd>00038166</ISPBIFCredtd>
                <VlrLanc>100.0</VlrLanc>
                <CodDevPortdd>1</CodDevPortdd>
                <NumCtrlSTROr>STR20250101000000001</NumCtrlSTROr>
                <ISPBPrestd>31680151</ISPBPrestd>
                <Hist>Payment for services</Hist>
                <DtAgendt>2025-09-08</DtAgendt>
                <HrAgendt>15:30:00</HrAgendt>
                <NivelPref>C</NivelPref>
                <DtMovto>2025-09-08</DtMovto>
            </STR0008>
        </SISMSG>
    </DOC>
    """

    assert normalize_xml(expected_xml) == normalize_xml(xml)


def test_str0048_to_xml_omit_optional_fields() -> None:
    params = make_valid_str0048_params()
    del params['description']
    del params['scheduled_date']
    del params['scheduled_time']
    del params['priority']

    str0048 = STR0048.model_validate(params)
    xml = str0048.to_xml()

    expected_xml = """
    <DOC>
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>316801512509080000001</NUOp>
        </BCMSG>
        <SISMSG>
            <STR0008>
                <CodMsg>STR0048</CodMsg>
                <NumCtrlIF>31680151202509090425</NumCtrlIF>
                <ISPBIFDebtd>31680151</ISPBIFDebtd>
                <ISPBIFCredtd>00038166</ISPBIFCredtd>
                <VlrLanc>100.0</VlrLanc>
                <CodDevPortdd>1</CodDevPortdd>
                <NumCtrlSTROr>STR20250101000000001</NumCtrlSTROr>
                <ISPBPrestd>31680151</ISPBPrestd>
                <DtMovto>2025-09-08</DtMovto>
            </STR0008>
        </SISMSG>
    </DOC>
    """

    assert normalize_xml(expected_xml) == normalize_xml(xml)


def test_str0048_from_xml() -> None:
    xml = """
    <DOC>
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>316801512509080000001</NUOp>
        </BCMSG>
        <SISMSG>
            <STR0008>
                <CodMsg>STR0048</CodMsg>
                <NumCtrlIF>31680151202509090425</NumCtrlIF>
                <ISPBIFDebtd>31680151</ISPBIFDebtd>
                <ISPBIFCredtd>00038166</ISPBIFCredtd>
                <VlrLanc>100.0</VlrLanc>
                <CodDevPortdd>1</CodDevPortdd>
                <NumCtrlSTROr>STR20250101000000001</NumCtrlSTROr>
                <ISPBPrestd>31680151</ISPBPrestd>
                <Hist>Payment for services</Hist>
                <DtAgendt>2025-09-08</DtAgendt>
                <HrAgendt>15:30:00</HrAgendt>
                <NivelPref>C</NivelPref>
                <DtMovto>2025-09-08</DtMovto>
            </STR0008>
        </SISMSG>
    </DOC>
    """

    str0048 = STR0048.from_xml(xml)
    assert isinstance(str0048, STR0048)
    assert str0048.from_ispb == '31680151'
    assert str0048.operation_number == '316801512509080000001'
    assert str0048.system_domain == 'SPB01'
    assert str0048.to_ispb == '00038166'
    assert str0048.institution_control_number == '31680151202509090425'
    assert str0048.debtor_institution_ispb == '31680151'
    assert str0048.creditor_institution_ispb == '00038166'
    assert str0048.amount == Decimal('100.00')
    assert str0048.portability_return_reason == PortabilityReturnReason.DESTINATION_ACCOUNT_CLOSED
    assert str0048.original_str_control_number == 'STR20250101000000001'
    assert str0048.provider_ispb == '31680151'
    assert str0048.description == 'Payment for services'
    assert str0048.scheduled_date == date(2025, 9, 8)
    assert str0048.scheduled_time == time(15, 30, 0)
    assert str0048.priority == Priority.MEDIUM
    assert str0048.settlement_date == date(2025, 9, 8)


def test_str0048_from_xml_missing_optional_fields() -> None:
    xml = """
    <DOC>
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>316801512509080000001</NUOp>
        </BCMSG>
        <SISMSG>
            <STR0008>
                <CodMsg>STR0048</CodMsg>
                <NumCtrlIF>31680151202509090425</NumCtrlIF>
                <ISPBIFDebtd>31680151</ISPBIFDebtd>
                <ISPBIFCredtd>00038166</ISPBIFCredtd>
                <VlrLanc>100.0</VlrLanc>
                <CodDevPortdd>1</CodDevPortdd>
                <NumCtrlSTROr>STR20250101000000001</NumCtrlSTROr>
                <ISPBPrestd>31680151</ISPBPrestd>
                <DtMovto>2025-09-08</DtMovto>
            </STR0008>
        </SISMSG>
    </DOC>
    """

    str0048 = STR0048.from_xml(xml)
    assert isinstance(str0048, STR0048)
    assert str0048.from_ispb == '31680151'
    assert str0048.operation_number == '316801512509080000001'
    assert str0048.system_domain == 'SPB01'
    assert str0048.to_ispb == '00038166'
    assert str0048.institution_control_number == '31680151202509090425'
    assert str0048.debtor_institution_ispb == '31680151'
    assert str0048.creditor_institution_ispb == '00038166'
    assert str0048.amount == Decimal('100.00')
    assert str0048.portability_return_reason == PortabilityReturnReason.DESTINATION_ACCOUNT_CLOSED
    assert str0048.original_str_control_number == 'STR20250101000000001'
    assert str0048.provider_ispb == '31680151'
    assert str0048.description is None
    assert str0048.scheduled_date is None
    assert str0048.scheduled_time is None
    assert str0048.priority is None
    assert str0048.settlement_date == date(2025, 9, 8)


def test_str0048_roundtrip() -> None:
    params = make_valid_str0048_params()
    str0004 = STR0048.model_validate(params)
    xml = str0004.to_xml()
    str0004_from_xml = STR0048.from_xml(xml)
    assert str0004 == str0004_from_xml


def test_str0048_from_xml_missing_required_fields() -> None:
    xml = """
    <DOC>
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>316801512509080000001</NUOp>
        </BCMSG>
        <SISMSG>
            <STR0008>
                <CodMsg>STR0048</CodMsg>
            </STR0008>
        </SISMSG>
    </DOC>
    """

    with pytest.raises(ValidationError) as exc:
        STR0048.from_xml(xml)

    missing_fields = extract_missing_fields(exc.value)
    assert missing_fields == {
        'debtor_institution_ispb',
        'provider_ispb',
        'creditor_institution_ispb',
        'amount',
        'settlement_date',
        'original_str_control_number',
        'institution_control_number',
        'portability_return_reason',
    }
