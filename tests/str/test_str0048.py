from datetime import date, datetime, time
from decimal import Decimal
from typing import Any

import pytest
from pydantic import ValidationError

from sfn_messages.core.types import Priority, StrSettlementStatus
from sfn_messages.str.str0048 import STR0048, STR0048E, STR0048R1, STR0048R2
from sfn_messages.str.types import PortabilityReturnReason
from tests.conftest import extract_missing_fields, normalize_xml


def make_valid_str0048_params() -> dict[str, Any]:
    return {
        'from_ispb': '31680151',
        'operation_number': '31680151250908000000001',
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


def make_valid_str0048r1_params() -> dict[str, Any]:
    return {
        'institution_control_number': '31680151202509090425',
        'from_ispb': '31680151',
        'debtor_institution_ispb': '31680151',
        'str_control_number': 'STR20250101000000001',
        'str_settlement_status': 'EFFECTIVE',
        'settlement_timestamp': '2025-11-20T15:30:00',
        'settlement_date': '2025-09-08',
        'operation_number': '31680151250908000000001',
        'to_ispb': '00038166',
        'system_domain': 'SPB01',
    }


def make_valid_str0048r2_params() -> dict[str, Any]:
    return {
        'from_ispb': '31680151',
        'operation_number': '31680151250908000000001',
        'system_domain': 'SPB01',
        'to_ispb': '00038166',
        'str_control_number': 'STR20250101000000002',
        'vendor_timestamp': '2025-11-20T15:30:00',
        'debtor_institution_ispb': '31680151',
        'creditor_institution_ispb': '00038166',
        'amount': 100.00,
        'portability_return_reason': 'DESTINATION_ACCOUNT_CLOSED',
        'original_str_control_number': 'STR20250101000000001',
        'provider_ispb': '31680151',
        'description': 'Payment for services',
        'settlement_date': '2025-09-08',
    }


def make_valid_str0048e_params(*, general_error: bool = False) -> dict[str, Any]:
    str0048e = {
        'from_ispb': '31680151',
        'operation_number': '31680151250908000000001',
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

    if general_error:
        str0048e['general_error_code'] = 'EGEN0050'
    else:
        str0048e['provider_ispb_error_code'] = 'ESPE0051'

    return str0048e


def test_str0048_valid_params() -> None:
    params = make_valid_str0048_params()
    str0048 = STR0048.model_validate(params)
    assert isinstance(str0048, STR0048)
    assert str0048.from_ispb == '31680151'
    assert str0048.operation_number == '31680151250908000000001'
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


def test_str0048e_general_error_valid_params() -> None:
    params = make_valid_str0048e_params(general_error=True)
    str0048e = STR0048E.model_validate(params)
    assert isinstance(str0048e, STR0048E)
    assert str0048e.from_ispb == '31680151'
    assert str0048e.operation_number == '31680151250908000000001'
    assert str0048e.system_domain == 'SPB01'
    assert str0048e.to_ispb == '00038166'
    assert str0048e.institution_control_number == '31680151202509090425'
    assert str0048e.debtor_institution_ispb == '31680151'
    assert str0048e.creditor_institution_ispb == '00038166'
    assert str0048e.amount == Decimal('100.00')
    assert str0048e.portability_return_reason == PortabilityReturnReason.DESTINATION_ACCOUNT_CLOSED
    assert str0048e.original_str_control_number == 'STR20250101000000001'
    assert str0048e.provider_ispb == '31680151'
    assert str0048e.description == 'Payment for services'
    assert str0048e.scheduled_date == date(2025, 9, 8)
    assert str0048e.scheduled_time == time(15, 30, 0)
    assert str0048e.priority == Priority.MEDIUM
    assert str0048e.settlement_date == date(2025, 9, 8)
    assert str0048e.general_error_code == 'EGEN0050'


def test_str0048e_tag_error_valid_params() -> None:
    params = make_valid_str0048e_params()
    str0048e = STR0048E.model_validate(params)
    assert isinstance(str0048e, STR0048E)
    assert str0048e.from_ispb == '31680151'
    assert str0048e.operation_number == '31680151250908000000001'
    assert str0048e.system_domain == 'SPB01'
    assert str0048e.to_ispb == '00038166'
    assert str0048e.institution_control_number == '31680151202509090425'
    assert str0048e.debtor_institution_ispb == '31680151'
    assert str0048e.creditor_institution_ispb == '00038166'
    assert str0048e.amount == Decimal('100.00')
    assert str0048e.portability_return_reason == PortabilityReturnReason.DESTINATION_ACCOUNT_CLOSED
    assert str0048e.original_str_control_number == 'STR20250101000000001'
    assert str0048e.provider_ispb == '31680151'
    assert str0048e.description == 'Payment for services'
    assert str0048e.scheduled_date == date(2025, 9, 8)
    assert str0048e.scheduled_time == time(15, 30, 0)
    assert str0048e.priority == Priority.MEDIUM
    assert str0048e.settlement_date == date(2025, 9, 8)
    assert str0048e.provider_ispb_error_code == 'ESPE0051'


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

    expected_xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/SPB/STR0048.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>31680151250908000000001</NUOp>
        </BCMSG>
        <SISMSG>
            <STR0048>
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
            </STR0048>
        </SISMSG>
    </DOC>
    """

    assert normalize_xml(expected_xml) == normalize_xml(xml)


def test_str0048e_general_error_to_xml() -> None:
    params = make_valid_str0048e_params(general_error=True)
    str0048e = STR0048E.model_validate(params)
    xml = str0048e.to_xml()

    expected_xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/SPB/STR0048E.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>31680151250908000000001</NUOp>
        </BCMSG>
        <SISMSG>
            <STR0048 CodErro="EGEN0050">
                <CodMsg>STR0048E</CodMsg>
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
            </STR0048>
        </SISMSG>
    </DOC>
    """

    assert normalize_xml(expected_xml) == normalize_xml(xml)


def test_str0048e_tag_error_to_xml() -> None:
    params = make_valid_str0048e_params()
    str0048e = STR0048E.model_validate(params)
    xml = str0048e.to_xml()

    expected_xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/SPB/STR0048E.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>31680151250908000000001</NUOp>
        </BCMSG>
        <SISMSG>
            <STR0048>
                <CodMsg>STR0048E</CodMsg>
                <NumCtrlIF>31680151202509090425</NumCtrlIF>
                <ISPBIFDebtd>31680151</ISPBIFDebtd>
                <ISPBIFCredtd>00038166</ISPBIFCredtd>
                <VlrLanc>100.0</VlrLanc>
                <CodDevPortdd>1</CodDevPortdd>
                <NumCtrlSTROr>STR20250101000000001</NumCtrlSTROr>
                <ISPBPrestd CodErro="ESPE0051">31680151</ISPBPrestd>
                <Hist>Payment for services</Hist>
                <DtAgendt>2025-09-08</DtAgendt>
                <HrAgendt>15:30:00</HrAgendt>
                <NivelPref>C</NivelPref>
                <DtMovto>2025-09-08</DtMovto>
            </STR0048>
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

    expected_xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/SPB/STR0048.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>31680151250908000000001</NUOp>
        </BCMSG>
        <SISMSG>
            <STR0048>
                <CodMsg>STR0048</CodMsg>
                <NumCtrlIF>31680151202509090425</NumCtrlIF>
                <ISPBIFDebtd>31680151</ISPBIFDebtd>
                <ISPBIFCredtd>00038166</ISPBIFCredtd>
                <VlrLanc>100.0</VlrLanc>
                <CodDevPortdd>1</CodDevPortdd>
                <NumCtrlSTROr>STR20250101000000001</NumCtrlSTROr>
                <ISPBPrestd>31680151</ISPBPrestd>
                <DtMovto>2025-09-08</DtMovto>
            </STR0048>
        </SISMSG>
    </DOC>
    """

    assert normalize_xml(expected_xml) == normalize_xml(xml)


def test_str0048_from_xml() -> None:
    xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/SPB/STR0048.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>31680151250908000000001</NUOp>
        </BCMSG>
        <SISMSG>
            <STR0048>
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
            </STR0048>
        </SISMSG>
    </DOC>
    """

    str0048 = STR0048.from_xml(xml)
    assert isinstance(str0048, STR0048)
    assert str0048.from_ispb == '31680151'
    assert str0048.operation_number == '31680151250908000000001'
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


def test_str0048e_general_error_from_xml() -> None:
    xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/SPB/STR0048E.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>31680151250908000000001</NUOp>
        </BCMSG>
        <SISMSG>
            <STR0048 CodErro="EGEN0050">
                <CodMsg>STR0048E</CodMsg>
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
            </STR0048>
        </SISMSG>
    </DOC>
    """

    str0048e = STR0048E.from_xml(xml)
    assert isinstance(str0048e, STR0048E)
    assert str0048e.from_ispb == '31680151'
    assert str0048e.operation_number == '31680151250908000000001'
    assert str0048e.system_domain == 'SPB01'
    assert str0048e.to_ispb == '00038166'
    assert str0048e.institution_control_number == '31680151202509090425'
    assert str0048e.debtor_institution_ispb == '31680151'
    assert str0048e.creditor_institution_ispb == '00038166'
    assert str0048e.amount == Decimal('100.00')
    assert str0048e.portability_return_reason == PortabilityReturnReason.DESTINATION_ACCOUNT_CLOSED
    assert str0048e.original_str_control_number == 'STR20250101000000001'
    assert str0048e.provider_ispb == '31680151'
    assert str0048e.description == 'Payment for services'
    assert str0048e.scheduled_date == date(2025, 9, 8)
    assert str0048e.scheduled_time == time(15, 30, 0)
    assert str0048e.priority == Priority.MEDIUM
    assert str0048e.settlement_date == date(2025, 9, 8)
    assert str0048e.general_error_code == 'EGEN0050'


def test_str0048e_tag_error_from_xml() -> None:
    xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/SPB/STR0048E.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>31680151250908000000001</NUOp>
        </BCMSG>
        <SISMSG>
            <STR0048>
                <CodMsg>STR0048E</CodMsg>
                <NumCtrlIF>31680151202509090425</NumCtrlIF>
                <ISPBIFDebtd>31680151</ISPBIFDebtd>
                <ISPBIFCredtd>00038166</ISPBIFCredtd>
                <VlrLanc>100.0</VlrLanc>
                <CodDevPortdd>1</CodDevPortdd>
                <NumCtrlSTROr>STR20250101000000001</NumCtrlSTROr>
                <ISPBPrestd CodErro="ESPE0051">31680151</ISPBPrestd>
                <Hist>Payment for services</Hist>
                <DtAgendt>2025-09-08</DtAgendt>
                <HrAgendt>15:30:00</HrAgendt>
                <NivelPref>C</NivelPref>
                <DtMovto>2025-09-08</DtMovto>
            </STR0048>
        </SISMSG>
    </DOC>
    """

    str0048e = STR0048E.from_xml(xml)
    assert isinstance(str0048e, STR0048E)
    assert str0048e.from_ispb == '31680151'
    assert str0048e.operation_number == '31680151250908000000001'
    assert str0048e.system_domain == 'SPB01'
    assert str0048e.to_ispb == '00038166'
    assert str0048e.institution_control_number == '31680151202509090425'
    assert str0048e.debtor_institution_ispb == '31680151'
    assert str0048e.creditor_institution_ispb == '00038166'
    assert str0048e.amount == Decimal('100.00')
    assert str0048e.portability_return_reason == PortabilityReturnReason.DESTINATION_ACCOUNT_CLOSED
    assert str0048e.original_str_control_number == 'STR20250101000000001'
    assert str0048e.provider_ispb == '31680151'
    assert str0048e.description == 'Payment for services'
    assert str0048e.scheduled_date == date(2025, 9, 8)
    assert str0048e.scheduled_time == time(15, 30, 0)
    assert str0048e.priority == Priority.MEDIUM
    assert str0048e.settlement_date == date(2025, 9, 8)
    assert str0048e.provider_ispb_error_code == 'ESPE0051'


def test_str0048_from_xml_missing_optional_fields() -> None:
    xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/SPB/STR0048.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>31680151250908000000001</NUOp>
        </BCMSG>
        <SISMSG>
            <STR0048>
                <CodMsg>STR0048</CodMsg>
                <NumCtrlIF>31680151202509090425</NumCtrlIF>
                <ISPBIFDebtd>31680151</ISPBIFDebtd>
                <ISPBIFCredtd>00038166</ISPBIFCredtd>
                <VlrLanc>100.0</VlrLanc>
                <CodDevPortdd>1</CodDevPortdd>
                <NumCtrlSTROr>STR20250101000000001</NumCtrlSTROr>
                <ISPBPrestd>31680151</ISPBPrestd>
                <DtMovto>2025-09-08</DtMovto>
            </STR0048>
        </SISMSG>
    </DOC>
    """

    str0048 = STR0048.from_xml(xml)
    assert isinstance(str0048, STR0048)
    assert str0048.from_ispb == '31680151'
    assert str0048.operation_number == '31680151250908000000001'
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
    xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/SPB/STR0048.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>31680151250908000000001</NUOp>
        </BCMSG>
        <SISMSG>
            <STR0048>
                <CodMsg>STR0048</CodMsg>
            </STR0048>
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


def test_str0048r1_valid_params() -> None:
    params = make_valid_str0048r1_params()
    str0048r1 = STR0048R1.model_validate(params)
    assert isinstance(str0048r1, STR0048R1)
    assert str0048r1.institution_control_number == '31680151202509090425'
    assert str0048r1.debtor_institution_ispb == '31680151'
    assert str0048r1.str_control_number == 'STR20250101000000001'
    assert str0048r1.str_settlement_status == 'EFFECTIVE'
    assert str0048r1.settlement_timestamp == datetime(2025, 11, 20, 15, 30)
    assert str0048r1.settlement_date == date(2025, 9, 8)


def test_str0048r1_missing_required_fields() -> None:
    with pytest.raises(ValidationError) as exc:
        STR0048R1.model_validate({})

    missing_fields = extract_missing_fields(exc.value)
    assert missing_fields == {
        'institution_control_number',
        'from_ispb',
        'debtor_institution_ispb',
        'str_control_number',
        'str_settlement_status',
        'settlement_timestamp',
        'settlement_date',
        'to_ispb',
        'system_domain',
        'operation_number',
    }


def test_str0048r1_to_xml() -> None:
    params = make_valid_str0048r1_params()
    str0048r1 = STR0048R1.model_validate(params)
    xml = str0048r1.to_xml()

    expected_xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/SPB/STR0048.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>31680151250908000000001</NUOp>
        </BCMSG>
        <SISMSG>
            <STR0048R1>
                <CodMsg>STR0048R1</CodMsg>
                <NumCtrlIF>31680151202509090425</NumCtrlIF>
                <ISPBIFDebtd>31680151</ISPBIFDebtd>
                <NumCtrlSTR>STR20250101000000001</NumCtrlSTR>
                <SitLancSTR>1</SitLancSTR>
                <DtHrSit>2025-11-20T15:30:00</DtHrSit>
                <DtMovto>2025-09-08</DtMovto>
            </STR0048R1>
        </SISMSG>
    </DOC>
    """

    assert normalize_xml(expected_xml) == normalize_xml(xml)


def test_str0048r1_from_xml() -> None:
    xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/SPB/STR0048.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>31680151250908000000001</NUOp>
        </BCMSG>
        <SISMSG>
            <STR0048R1>
                <CodMsg>STR0048R1</CodMsg>
                <NumCtrlIF>31680151202509090425</NumCtrlIF>
                <ISPBIFDebtd>31680151</ISPBIFDebtd>
                <NumCtrlSTR>STR20250101000000001</NumCtrlSTR>
                <SitLancSTR>1</SitLancSTR>
                <DtHrSit>2025-11-20T15:30:00</DtHrSit>
                <DtMovto>2025-09-08</DtMovto>
            </STR0048R1>
        </SISMSG>
    </DOC>
    """

    str0048r1 = STR0048R1.from_xml(xml)
    assert isinstance(str0048r1, STR0048R1)
    assert str0048r1.institution_control_number == '31680151202509090425'
    assert str0048r1.debtor_institution_ispb == '31680151'
    assert str0048r1.str_control_number == 'STR20250101000000001'
    assert str0048r1.str_settlement_status == StrSettlementStatus.EFFECTIVE
    assert str0048r1.settlement_timestamp == datetime(2025, 11, 20, 15, 30)
    assert str0048r1.settlement_date == date(2025, 9, 8)


def test_str0048r1_roundtrip() -> None:
    params = make_valid_str0048r1_params()
    str0048r1 = STR0048R1.model_validate(params)
    xml = str0048r1.to_xml()
    str0048r1_from_xml = STR0048R1.from_xml(xml)
    assert str0048r1 == str0048r1_from_xml


def test_str0048r1_from_xml_missing_required_fields() -> None:
    xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/SPB/STR0048.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>31680151250908000000001</NUOp>
        </BCMSG>
        <SISMSG>
            <STR0048R1>
                <CodMsg>STR0048R1</CodMsg>
            </STR0048R1>
        </SISMSG>
    </DOC>
    """

    with pytest.raises(ValidationError) as exc:
        STR0048R1.from_xml(xml)

    missing_fields = extract_missing_fields(exc.value)
    assert missing_fields == {
        'debtor_institution_ispb',
        'str_control_number',
        'str_settlement_status',
        'institution_control_number',
        'settlement_timestamp',
        'settlement_date',
    }


def test_str0048r2_valid_params() -> None:
    params = make_valid_str0048r2_params()
    str0048r2 = STR0048R2.model_validate(params)
    assert isinstance(str0048r2, STR0048R2)
    assert str0048r2.str_control_number == 'STR20250101000000002'
    assert str0048r2.vendor_timestamp == datetime(2025, 11, 20, 15, 30)
    assert str0048r2.debtor_institution_ispb == '31680151'
    assert str0048r2.creditor_institution_ispb == '00038166'
    assert str0048r2.amount == Decimal('100.00')
    assert str0048r2.portability_return_reason == PortabilityReturnReason.DESTINATION_ACCOUNT_CLOSED
    assert str0048r2.original_str_control_number == 'STR20250101000000001'
    assert str0048r2.provider_ispb == '31680151'
    assert str0048r2.description == 'Payment for services'
    assert str0048r2.settlement_date == date(2025, 9, 8)


def test_str0048r2_missing_required_fields() -> None:
    with pytest.raises(ValidationError) as exc:
        STR0048R2.model_validate({})

    missing_fields = extract_missing_fields(exc.value)
    assert missing_fields == {
        'from_ispb',
        'to_ispb',
        'str_control_number',
        'vendor_timestamp',
        'debtor_institution_ispb',
        'creditor_institution_ispb',
        'amount',
        'portability_return_reason',
        'original_str_control_number',
        'provider_ispb',
        'settlement_date',
        'operation_number',
        'system_domain',
    }


def test_str0048r2_to_xml() -> None:
    params = make_valid_str0048r2_params()
    str0048r2 = STR0048R2.model_validate(params)
    xml = str0048r2.to_xml()

    expected_xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/SPB/STR0048.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>31680151250908000000001</NUOp>
        </BCMSG>
        <SISMSG>
            <STR0048R2>
                <CodMsg>STR0048R2</CodMsg>
                <NumCtrlSTR>STR20250101000000002</NumCtrlSTR>
                <DtHrBC>2025-11-20T15:30:00</DtHrBC>
                <ISPBIFDebtd>31680151</ISPBIFDebtd>
                <ISPBIFCredtd>00038166</ISPBIFCredtd>
                <VlrLanc>100.0</VlrLanc>
                <CodDevPortdd>1</CodDevPortdd>
                <NumCtrlSTROr>STR20250101000000001</NumCtrlSTROr>
                <ISPBPrestd>31680151</ISPBPrestd>
                <Hist>Payment for services</Hist>
                <DtMovto>2025-09-08</DtMovto>
            </STR0048R2>
        </SISMSG>
    </DOC>
    """

    assert normalize_xml(expected_xml) == normalize_xml(xml)


def test_str0048r2_to_xml_omit_optional_fields() -> None:
    params = make_valid_str0048r2_params()
    del params['description']

    str0048r2 = STR0048R2.model_validate(params)
    xml = str0048r2.to_xml()

    expected_xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/SPB/STR0048.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>31680151250908000000001</NUOp>
        </BCMSG>
        <SISMSG>
            <STR0048R2>
                <CodMsg>STR0048R2</CodMsg>
                <NumCtrlSTR>STR20250101000000002</NumCtrlSTR>
                <DtHrBC>2025-11-20T15:30:00</DtHrBC>
                <ISPBIFDebtd>31680151</ISPBIFDebtd>
                <ISPBIFCredtd>00038166</ISPBIFCredtd>
                <VlrLanc>100.0</VlrLanc>
                <CodDevPortdd>1</CodDevPortdd>
                <NumCtrlSTROr>STR20250101000000001</NumCtrlSTROr>
                <ISPBPrestd>31680151</ISPBPrestd>
                <DtMovto>2025-09-08</DtMovto>
            </STR0048R2>
        </SISMSG>
    </DOC>
    """

    assert normalize_xml(expected_xml) == normalize_xml(xml)


def test_str0048r2_from_xml() -> None:
    xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/SPB/STR0048.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>31680151250908000000001</NUOp>
        </BCMSG>
        <SISMSG>
            <STR0048R2>
                <CodMsg>STR0048R2</CodMsg>
                <NumCtrlSTR>STR20250101000000002</NumCtrlSTR>
                <DtHrBC>2025-11-20T15:30:00</DtHrBC>
                <ISPBIFDebtd>31680151</ISPBIFDebtd>
                <ISPBIFCredtd>00038166</ISPBIFCredtd>
                <VlrLanc>100.0</VlrLanc>
                <CodDevPortdd>1</CodDevPortdd>
                <NumCtrlSTROr>STR20250101000000001</NumCtrlSTROr>
                <ISPBPrestd>31680151</ISPBPrestd>
                <Hist>Payment for services</Hist>
                <DtMovto>2025-09-08</DtMovto>
            </STR0048R2>
        </SISMSG>
    </DOC>
    """

    str0048r2 = STR0048R2.from_xml(xml)
    assert isinstance(str0048r2, STR0048R2)
    assert str0048r2.str_control_number == 'STR20250101000000002'
    assert str0048r2.vendor_timestamp == datetime(2025, 11, 20, 15, 30)
    assert str0048r2.debtor_institution_ispb == '31680151'
    assert str0048r2.creditor_institution_ispb == '00038166'
    assert str0048r2.amount == Decimal('100.00')
    assert str0048r2.portability_return_reason == PortabilityReturnReason.DESTINATION_ACCOUNT_CLOSED
    assert str0048r2.original_str_control_number == 'STR20250101000000001'
    assert str0048r2.provider_ispb == '31680151'
    assert str0048r2.description == 'Payment for services'
    assert str0048r2.settlement_date == date(2025, 9, 8)


def test_str0048r2_from_xml_missing_optional_fields() -> None:
    xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/SPB/STR0048.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>31680151250908000000001</NUOp>
        </BCMSG>
        <SISMSG>
            <STR0048R2>
                <CodMsg>STR0048R2</CodMsg>
                <NumCtrlSTR>STR20250101000000002</NumCtrlSTR>
                <DtHrBC>2025-11-20T15:30:00</DtHrBC>
                <ISPBIFDebtd>31680151</ISPBIFDebtd>
                <ISPBIFCredtd>00038166</ISPBIFCredtd>
                <VlrLanc>100.0</VlrLanc>
                <CodDevPortdd>1</CodDevPortdd>
                <NumCtrlSTROr>STR20250101000000001</NumCtrlSTROr>
                <ISPBPrestd>31680151</ISPBPrestd>
                <DtMovto>2025-09-08</DtMovto>
            </STR0048R2>
        </SISMSG>
    </DOC>
    """

    str0048r2 = STR0048R2.from_xml(xml)
    assert isinstance(str0048r2, STR0048R2)
    assert str0048r2.str_control_number == 'STR20250101000000002'
    assert str0048r2.vendor_timestamp == datetime(2025, 11, 20, 15, 30)
    assert str0048r2.debtor_institution_ispb == '31680151'
    assert str0048r2.creditor_institution_ispb == '00038166'
    assert str0048r2.amount == Decimal('100.00')
    assert str0048r2.portability_return_reason == PortabilityReturnReason.DESTINATION_ACCOUNT_CLOSED
    assert str0048r2.original_str_control_number == 'STR20250101000000001'
    assert str0048r2.provider_ispb == '31680151'
    assert str0048r2.description is None
    assert str0048r2.settlement_date == date(2025, 9, 8)


def test_str0048r2_roundtrip() -> None:
    params = make_valid_str0048r2_params()
    str0048r2 = STR0048R2.model_validate(params)
    xml = str0048r2.to_xml()
    str0048r2_from_xml = STR0048R2.from_xml(xml)
    assert str0048r2 == str0048r2_from_xml


def test_str0048r2_from_xml_missing_required_fields() -> None:
    xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/SPB/STR0048.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>31680151250908000000001</NUOp>
        </BCMSG>
        <SISMSG>
            <STR0048R2>
                <CodMsg>STR0048R2</CodMsg>
            </STR0048R2>
        </SISMSG>
    </DOC>
    """

    with pytest.raises(ValidationError) as exc:
        STR0048R2.from_xml(xml)

    missing_fields = extract_missing_fields(exc.value)
    assert missing_fields == {
        'settlement_date',
        'debtor_institution_ispb',
        'creditor_institution_ispb',
        'portability_return_reason',
        'vendor_timestamp',
        'amount',
        'str_control_number',
        'original_str_control_number',
        'provider_ispb',
    }
