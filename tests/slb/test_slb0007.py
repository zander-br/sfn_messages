from datetime import UTC, date, datetime
from decimal import Decimal
from typing import Any

import pytest
from pydantic import ValidationError

from sfn_messages.core.types import Priority
from sfn_messages.slb.slb0007 import SLB0007, SLB0007R1
from sfn_messages.slb.types import SlbPurpose, SlbSettlementStatus
from tests.conftest import extract_missing_fields, normalize_xml


def make_valid_slb0007_params() -> dict[str, Any]:
    return {
        'from_ispb': '31680151',
        'to_ispb': '00038166',
        'system_domain': 'SPB01',
        'operation_number': '316801512509080000001',
        'message_code': 'SLB0007',
        'participant_institution_control_number': '123',
        'participant_ispb': '31680154',
        'original_slb_control_number': 'SLB20250101000000001',
        'partner_cnpj': '56369416000136',
        'slb_purpose': 'BCB_FX_PURCHASE_SPOT_CREDIT_REAIS_TO_FI',
        'amount': 199.58,
        'priority': 'HIGH',
        'description': 'Test description',
        'settlement_date': '2025-12-10',
    }


def make_valid_slb0007r1_params() -> dict[str, Any]:
    return {
        'from_ispb': '31680151',
        'to_ispb': '00038166',
        'system_domain': 'SPB01',
        'operation_number': '316801512509080000001',
        'message_code': 'SLB0007R1',
        'participant_institution_control_number': '123',
        'participant_ispb': '31680154',
        'original_slb_control_number': 'SLB20250101000000001',
        'str_control_number': 'STR20250101000000001',
        'slb_settlement_status': 'EFFECTED',
        'settlement_timestamp': '2025-12-10T17:22:00+00:00',
        'settlement_date': '2025-12-10',
    }


def test_slb0007_valid_model() -> None:
    params = make_valid_slb0007_params()
    slb0007 = SLB0007.model_validate(params)

    assert isinstance(slb0007, SLB0007)
    assert slb0007.from_ispb == '31680151'
    assert slb0007.to_ispb == '00038166'
    assert slb0007.system_domain == 'SPB01'
    assert slb0007.operation_number == '316801512509080000001'
    assert slb0007.message_code == 'SLB0007'
    assert slb0007.participant_institution_control_number == '123'
    assert slb0007.participant_ispb == '31680154'
    assert slb0007.original_slb_control_number == 'SLB20250101000000001'
    assert slb0007.partner_cnpj == '56369416000136'
    assert slb0007.slb_purpose == SlbPurpose.BCB_FX_PURCHASE_SPOT_CREDIT_REAIS_TO_FI
    assert slb0007.amount == Decimal('199.58')
    assert slb0007.priority == Priority.HIGH
    assert slb0007.description == 'Test description'
    assert slb0007.settlement_date == date(2025, 12, 10)


def test_slb0007r1_valid_model() -> None:
    params = make_valid_slb0007r1_params()
    slb0007r1 = SLB0007R1.model_validate(params)

    assert isinstance(slb0007r1, SLB0007R1)
    assert slb0007r1.from_ispb == '31680151'
    assert slb0007r1.to_ispb == '00038166'
    assert slb0007r1.system_domain == 'SPB01'
    assert slb0007r1.operation_number == '316801512509080000001'
    assert slb0007r1.message_code == 'SLB0007R1'
    assert slb0007r1.participant_institution_control_number == '123'
    assert slb0007r1.participant_ispb == '31680154'
    assert slb0007r1.original_slb_control_number == 'SLB20250101000000001'
    assert slb0007r1.str_control_number == 'STR20250101000000001'
    assert slb0007r1.slb_settlement_status == SlbSettlementStatus.EFFECTED
    assert slb0007r1.settlement_timestamp == datetime(2025, 12, 10, 17, 22, tzinfo=UTC)
    assert slb0007r1.settlement_date == date(2025, 12, 10)


def test_slb0007_missing_required_fields() -> None:
    with pytest.raises(ValidationError) as exc:
        SLB0007.model_validate({})

    missing_fields = extract_missing_fields(exc.value)
    assert missing_fields == {
        'from_ispb',
        'to_ispb',
        'system_domain',
        'operation_number',
        'participant_institution_control_number',
        'participant_ispb',
        'slb_purpose',
        'amount',
        'description',
        'settlement_date',
    }


def test_slb0007r1_missing_required_fields() -> None:
    with pytest.raises(ValidationError) as exc:
        SLB0007R1.model_validate({})

    missing_fields = extract_missing_fields(exc.value)
    assert missing_fields == {
        'from_ispb',
        'to_ispb',
        'system_domain',
        'operation_number',
        'participant_institution_control_number',
        'participant_ispb',
        'original_slb_control_number',
        'str_control_number',
        'slb_settlement_status',
        'settlement_timestamp',
        'settlement_date',
    }


def test_slb0007_to_xml() -> None:
    params = make_valid_slb0007_params()
    slb0007 = SLB0007.model_validate(params)

    xml = slb0007.to_xml()

    expected_xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/SLB/SLB0007.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>316801512509080000001</NUOp>
        </BCMSG>
        <SISMSG>
            <SLB0007>
                <CodMsg>SLB0007</CodMsg>
                <NumCtrlPart>123</NumCtrlPart>
                <ISPBPart>31680154</ISPBPart>
                <NumCtrlSLBOr>SLB20250101000000001</NumCtrlSLBOr>
                <CNPJConv>56369416000136</CNPJConv>
                <FinlddSLB>CAM060164</FinlddSLB>
                <VlrLanc>199.58</VlrLanc>
                <NivelPref>B</NivelPref>
                <Hist>Test description</Hist>
                <DtMovto>2025-12-10</DtMovto>
            </SLB0007>
        </SISMSG>
    </DOC>
    """
    assert normalize_xml(expected_xml) == normalize_xml(xml)


def test_slb0007r1_to_xml() -> None:
    params = make_valid_slb0007r1_params()
    slb0007r1 = SLB0007R1.model_validate(params)

    xml = slb0007r1.to_xml()

    expected_xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/SLB/SLB0007.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>316801512509080000001</NUOp>
        </BCMSG>
        <SISMSG>
            <SLB0007R1>
                <CodMsg>SLB0007R1</CodMsg>
                <NumCtrlPart>123</NumCtrlPart>
                <ISPBPart>31680154</ISPBPart>
                <NumCtrlSLB>SLB20250101000000001</NumCtrlSLB>
                <NumCtrlSTR>STR20250101000000001</NumCtrlSTR>
                <SitLancSLB>1</SitLancSLB>
                <DtHrSit>2025-12-10 17:22:00+00:00</DtHrSit>
                <DtMovto>2025-12-10</DtMovto>
            </SLB0007R1>
        </SISMSG>
    </DOC>
    """
    assert normalize_xml(expected_xml) == normalize_xml(xml)


def test_slb0007_from_xml() -> None:
    xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/SLB/SLB0007.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>316801512509080000001</NUOp>
        </BCMSG>
        <SISMSG>
            <SLB0007>
                <CodMsg>SLB0007</CodMsg>
                <NumCtrlPart>123</NumCtrlPart>
                <ISPBPart>31680154</ISPBPart>
                <NumCtrlSLBOr>SLB20250101000000001</NumCtrlSLBOr>
                <CNPJConv>56369416000136</CNPJConv>
                <FinlddSLB>CAM060164</FinlddSLB>
                <VlrLanc>199.58</VlrLanc>
                <NivelPref>B</NivelPref>
                <Hist>Test description</Hist>
                <DtMovto>2025-12-10</DtMovto>
            </SLB0007>
        </SISMSG>
    </DOC>
    """

    slb0007 = SLB0007.from_xml(xml)

    assert isinstance(slb0007, SLB0007)
    assert slb0007.from_ispb == '31680151'
    assert slb0007.to_ispb == '00038166'
    assert slb0007.system_domain == 'SPB01'
    assert slb0007.operation_number == '316801512509080000001'
    assert slb0007.message_code == 'SLB0007'
    assert slb0007.participant_institution_control_number == '123'
    assert slb0007.participant_ispb == '31680154'
    assert slb0007.original_slb_control_number == 'SLB20250101000000001'
    assert slb0007.partner_cnpj == '56369416000136'
    assert slb0007.slb_purpose == SlbPurpose.BCB_FX_PURCHASE_SPOT_CREDIT_REAIS_TO_FI
    assert slb0007.amount == Decimal('199.58')
    assert slb0007.priority == Priority.HIGH
    assert slb0007.description == 'Test description'
    assert slb0007.settlement_date == date(2025, 12, 10)


def test_slb0007r1_from_xml() -> None:
    xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/SLB/SLB0007.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>316801512509080000001</NUOp>
        </BCMSG>
        <SISMSG>
            <SLB0007R1>
                <CodMsg>SLB0007R1</CodMsg>
                <NumCtrlPart>123</NumCtrlPart>
                <ISPBPart>31680154</ISPBPart>
                <NumCtrlSLB>SLB20250101000000001</NumCtrlSLB>
                <NumCtrlSTR>STR20250101000000001</NumCtrlSTR>
                <SitLancSLB>1</SitLancSLB>
                <DtHrSit>2025-12-10 17:22:00+00:00</DtHrSit>
                <DtMovto>2025-12-10</DtMovto>
            </SLB0007R1>
        </SISMSG>
    </DOC>
    """

    slb0007r1 = SLB0007R1.from_xml(xml)

    assert isinstance(slb0007r1, SLB0007R1)
    assert slb0007r1.from_ispb == '31680151'
    assert slb0007r1.to_ispb == '00038166'
    assert slb0007r1.system_domain == 'SPB01'
    assert slb0007r1.operation_number == '316801512509080000001'
    assert slb0007r1.message_code == 'SLB0007R1'
    assert slb0007r1.participant_institution_control_number == '123'
    assert slb0007r1.participant_ispb == '31680154'
    assert slb0007r1.original_slb_control_number == 'SLB20250101000000001'
    assert slb0007r1.str_control_number == 'STR20250101000000001'
    assert slb0007r1.slb_settlement_status == SlbSettlementStatus.EFFECTED
    assert slb0007r1.settlement_timestamp == datetime(2025, 12, 10, 17, 22, tzinfo=UTC)
    assert slb0007r1.settlement_date == date(2025, 12, 10)


def test_slb0007_roundtrip() -> None:
    params = make_valid_slb0007_params()

    slb0007 = SLB0007.model_validate(params)
    xml = slb0007.to_xml()
    slb0007_from_xml = SLB0007.from_xml(xml)

    assert slb0007 == slb0007_from_xml


def test_slb0007r1_roundtrip() -> None:
    params = make_valid_slb0007r1_params()

    slb0007r1 = SLB0007R1.model_validate(params)
    xml = slb0007r1.to_xml()
    slb0007r1_from_xml = SLB0007R1.from_xml(xml)

    assert slb0007r1 == slb0007r1_from_xml


def test_slb0007_from_xml_missing_required_fields() -> None:
    xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/SLB/SLB0007.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>316801512509080000001</NUOp>
        </BCMSG>
        <SISMSG>
            <SLB0007>
                <CodMsg>SLB0007</CodMsg>
            </SLB0007>
        </SISMSG>
    </DOC>
    """

    with pytest.raises(ValidationError) as exc:
        SLB0007.from_xml(xml)

    missing_fields = extract_missing_fields(exc.value)
    assert missing_fields == {
        'participant_institution_control_number',
        'participant_ispb',
        'slb_purpose',
        'amount',
        'description',
        'settlement_date',
    }
