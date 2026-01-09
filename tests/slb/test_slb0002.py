from datetime import UTC, date, datetime
from decimal import Decimal
from typing import Any

import pytest
from pydantic import ValidationError

from sfn_messages.core.types import Priority
from sfn_messages.slb.slb0002 import SLB0002, SLB0002E, SLB0002R1
from sfn_messages.slb.types import SlbSettlementStatus
from tests.conftest import extract_missing_fields, normalize_xml


def make_valid_slb0002_params() -> dict[str, Any]:
    return {
        'from_ispb': '31680151',
        'to_ispb': '00038166',
        'system_domain': 'SPB01',
        'operation_number': '316801512509080000001',
        'message_code': 'SLB0002',
        'participant_institution_control_number': '123',
        'participant_ispb': '31680153',
        'original_slb_control_number': 'SLB20250101000000001',
        'priority': 'HIGH',
        'amount': 139.0,
        'settlement_date': '2025-12-10',
    }


def make_valid_slb0002r1_params() -> dict[str, Any]:
    return {
        'from_ispb': '31680151',
        'to_ispb': '00038166',
        'system_domain': 'SPB01',
        'operation_number': '316801512509080000001',
        'message_code': 'SLB0002R1',
        'participant_institution_control_number': '123',
        'participant_ispb': '31680153',
        'str_control_number': 'STR20250101000000001',
        'slb_settlement_status': 'EFFECTED',
        'settlement_timestamp': '2025-12-10T17:09:00+00:00',
        'settlement_date': '2025-12-10',
    }


def make_valid_slb0002e_params(*, general_error: bool = False) -> dict[str, Any]:
    slb0002e = {
        'from_ispb': '31680151',
        'to_ispb': '00038166',
        'system_domain': 'SPB01',
        'operation_number': '316801512509080000001',
        'message_code': 'SLB0002',
        'participant_institution_control_number': '123',
        'participant_ispb': '31680153',
        'original_slb_control_number': 'SLB20250101000000001',
        'priority': 'HIGH',
        'amount': 139.0,
        'settlement_date': '2025-12-10',
    }

    if general_error:
        slb0002e['general_error_code'] = 'EGEN0050'
    else:
        slb0002e['original_slb_control_number_error_code'] = 'EPCN0100'

    return slb0002e


def test_slb0002_valid_model() -> None:
    params = make_valid_slb0002_params()
    slb0002 = SLB0002.model_validate(params)

    assert isinstance(slb0002, SLB0002)
    assert slb0002.from_ispb == '31680151'
    assert slb0002.to_ispb == '00038166'
    assert slb0002.system_domain == 'SPB01'
    assert slb0002.operation_number == '316801512509080000001'
    assert slb0002.message_code == 'SLB0002'
    assert slb0002.participant_institution_control_number == '123'
    assert slb0002.participant_ispb == '31680153'
    assert slb0002.original_slb_control_number == 'SLB20250101000000001'
    assert slb0002.priority == Priority.HIGH
    assert slb0002.amount == Decimal('139.0')
    assert slb0002.settlement_date == date(2025, 12, 10)


def test_slb0002r1_valid_model() -> None:
    params = make_valid_slb0002r1_params()
    slb0002r1 = SLB0002R1.model_validate(params)

    assert isinstance(slb0002r1, SLB0002R1)
    assert slb0002r1.from_ispb == '31680151'
    assert slb0002r1.to_ispb == '00038166'
    assert slb0002r1.system_domain == 'SPB01'
    assert slb0002r1.operation_number == '316801512509080000001'
    assert slb0002r1.message_code == 'SLB0002R1'
    assert slb0002r1.participant_institution_control_number == '123'
    assert slb0002r1.participant_ispb == '31680153'
    assert slb0002r1.str_control_number == 'STR20250101000000001'
    assert slb0002r1.slb_settlement_status == SlbSettlementStatus.EFFECTED
    assert slb0002r1.settlement_timestamp == datetime(2025, 12, 10, 17, 9, tzinfo=UTC)
    assert slb0002r1.settlement_date == date(2025, 12, 10)


def test_slb0002e_general_error_valid_model() -> None:
    params = make_valid_slb0002e_params(general_error=True)
    slb0002e = SLB0002E.model_validate(params)

    assert isinstance(slb0002e, SLB0002E)
    assert slb0002e.from_ispb == '31680151'
    assert slb0002e.to_ispb == '00038166'
    assert slb0002e.system_domain == 'SPB01'
    assert slb0002e.operation_number == '316801512509080000001'
    assert slb0002e.message_code == 'SLB0002'
    assert slb0002e.participant_institution_control_number == '123'
    assert slb0002e.participant_ispb == '31680153'
    assert slb0002e.original_slb_control_number == 'SLB20250101000000001'
    assert slb0002e.priority == Priority.HIGH
    assert slb0002e.amount == Decimal('139.0')
    assert slb0002e.settlement_date == date(2025, 12, 10)

    assert slb0002e.general_error_code == 'EGEN0050'


def test_slb0002e_tag_error_valid_model() -> None:
    params = make_valid_slb0002e_params()
    slb0002e = SLB0002E.model_validate(params)

    assert isinstance(slb0002e, SLB0002E)
    assert slb0002e.from_ispb == '31680151'
    assert slb0002e.to_ispb == '00038166'
    assert slb0002e.system_domain == 'SPB01'
    assert slb0002e.operation_number == '316801512509080000001'
    assert slb0002e.message_code == 'SLB0002'
    assert slb0002e.participant_institution_control_number == '123'
    assert slb0002e.participant_ispb == '31680153'
    assert slb0002e.original_slb_control_number == 'SLB20250101000000001'
    assert slb0002e.priority == Priority.HIGH
    assert slb0002e.amount == Decimal('139.0')
    assert slb0002e.settlement_date == date(2025, 12, 10)

    assert slb0002e.original_slb_control_number_error_code == 'EPCN0100'


def test_slb0002_missing_required_fields() -> None:
    with pytest.raises(ValidationError) as exc:
        SLB0002.model_validate({})

    missing_fields = extract_missing_fields(exc.value)
    assert missing_fields == {
        'from_ispb',
        'to_ispb',
        'system_domain',
        'operation_number',
        'participant_institution_control_number',
        'participant_ispb',
        'original_slb_control_number',
        'amount',
        'settlement_date',
    }


def test_slb0002r1_missing_required_fields() -> None:
    with pytest.raises(ValidationError) as exc:
        SLB0002R1.model_validate({})

    missing_fields = extract_missing_fields(exc.value)
    assert missing_fields == {
        'from_ispb',
        'to_ispb',
        'system_domain',
        'operation_number',
        'participant_institution_control_number',
        'participant_ispb',
        'slb_settlement_status',
        'settlement_timestamp',
        'settlement_date',
    }


def test_slb0002_to_xml() -> None:
    params = make_valid_slb0002_params()
    slb0002 = SLB0002.model_validate(params)

    xml = slb0002.to_xml()

    expected_xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/SLB/SLB0002.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>316801512509080000001</NUOp>
        </BCMSG>
        <SISMSG>
            <SLB0002>
                <CodMsg>SLB0002</CodMsg>
                <NumCtrlPart>123</NumCtrlPart>
                <ISPBPart>31680153</ISPBPart>
                <NumCtrlSLBOr>SLB20250101000000001</NumCtrlSLBOr>
                <NivelPref>B</NivelPref>
                <VlrLanc>139.0</VlrLanc>
                <DtMovto>2025-12-10</DtMovto>
            </SLB0002>
        </SISMSG>
    </DOC>
    """
    assert normalize_xml(expected_xml) == normalize_xml(xml)


def test_slb0002r1_to_xml() -> None:
    params = make_valid_slb0002r1_params()
    slb0002r1 = SLB0002R1.model_validate(params)

    xml = slb0002r1.to_xml()

    expected_xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/SLB/SLB0002.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>316801512509080000001</NUOp>
        </BCMSG>
        <SISMSG>
            <SLB0002R1>
                <CodMsg>SLB0002R1</CodMsg>
                <NumCtrlPart>123</NumCtrlPart>
                <ISPBPart>31680153</ISPBPart>
                <NumCtrlSTR>STR20250101000000001</NumCtrlSTR>
                <SitLancSLB>1</SitLancSLB>
                <DtHrSit>2025-12-10 17:09:00+00:00</DtHrSit>
                <DtMovto>2025-12-10</DtMovto>
            </SLB0002R1>
        </SISMSG>
    </DOC>
    """
    assert normalize_xml(expected_xml) == normalize_xml(xml)


def test_slb0002e_general_error_to_xml() -> None:
    params = make_valid_slb0002e_params(general_error=True)
    slb0002e = SLB0002E.model_validate(params)

    xml = slb0002e.to_xml()

    expected_xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/SLB/SLB0002E.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>316801512509080000001</NUOp>
        </BCMSG>
        <SISMSG>
            <SLB0002E CodErro="EGEN0050">
                <CodMsg>SLB0002</CodMsg>
                <NumCtrlPart>123</NumCtrlPart>
                <ISPBPart>31680153</ISPBPart>
                <NumCtrlSLBOr>SLB20250101000000001</NumCtrlSLBOr>
                <NivelPref>B</NivelPref>
                <VlrLanc>139.0</VlrLanc>
                <DtMovto>2025-12-10</DtMovto>
            </SLB0002E>
        </SISMSG>
    </DOC>
    """
    assert normalize_xml(expected_xml) == normalize_xml(xml)


def test_slb0002e_tag_error_to_xml() -> None:
    params = make_valid_slb0002e_params()
    slb0002e = SLB0002E.model_validate(params)

    xml = slb0002e.to_xml()

    expected_xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/SLB/SLB0002E.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>316801512509080000001</NUOp>
        </BCMSG>
        <SISMSG>
            <SLB0002E>
                <CodMsg>SLB0002</CodMsg>
                <NumCtrlPart>123</NumCtrlPart>
                <ISPBPart>31680153</ISPBPart>
                <NumCtrlSLBOr CodErro="EPCN0100">SLB20250101000000001</NumCtrlSLBOr>
                <NivelPref>B</NivelPref>
                <VlrLanc>139.0</VlrLanc>
                <DtMovto>2025-12-10</DtMovto>
            </SLB0002E>
        </SISMSG>
    </DOC>
    """
    assert normalize_xml(expected_xml) == normalize_xml(xml)


def test_slb0002_from_xml() -> None:
    xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/SLB/SLB0002.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>316801512509080000001</NUOp>
        </BCMSG>
        <SISMSG>
            <SLB0002>
                <CodMsg>SLB0002</CodMsg>
                <NumCtrlPart>123</NumCtrlPart>
                <ISPBPart>31680153</ISPBPart>
                <NumCtrlSLBOr>SLB20250101000000001</NumCtrlSLBOr>
                <NivelPref>B</NivelPref>
                <VlrLanc>139.0</VlrLanc>
                <DtMovto>2025-12-10</DtMovto>
            </SLB0002>
        </SISMSG>
    </DOC>
    """

    slb0002 = SLB0002.from_xml(xml)

    assert isinstance(slb0002, SLB0002)
    assert slb0002.from_ispb == '31680151'
    assert slb0002.to_ispb == '00038166'
    assert slb0002.system_domain == 'SPB01'
    assert slb0002.operation_number == '316801512509080000001'
    assert slb0002.message_code == 'SLB0002'
    assert slb0002.participant_institution_control_number == '123'
    assert slb0002.participant_ispb == '31680153'
    assert slb0002.original_slb_control_number == 'SLB20250101000000001'
    assert slb0002.priority == Priority.HIGH
    assert slb0002.amount == Decimal('139.0')
    assert slb0002.settlement_date == date(2025, 12, 10)


def test_slb0002r1_from_xml() -> None:
    xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/SLB/SLB0002.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>316801512509080000001</NUOp>
        </BCMSG>
        <SISMSG>
            <SLB0002R1>
                <CodMsg>SLB0002R1</CodMsg>
                <NumCtrlPart>123</NumCtrlPart>
                <ISPBPart>31680153</ISPBPart>
                <NumCtrlSTR>STR20250101000000001</NumCtrlSTR>
                <SitLancSLB>1</SitLancSLB>
                <DtHrSit>2025-12-10 17:09:00+00:00</DtHrSit>
                <DtMovto>2025-12-10</DtMovto>
            </SLB0002R1>
        </SISMSG>
    </DOC>
    """

    slb0002r1 = SLB0002R1.from_xml(xml)

    assert isinstance(slb0002r1, SLB0002R1)
    assert slb0002r1.from_ispb == '31680151'
    assert slb0002r1.to_ispb == '00038166'
    assert slb0002r1.system_domain == 'SPB01'
    assert slb0002r1.operation_number == '316801512509080000001'
    assert slb0002r1.message_code == 'SLB0002R1'
    assert slb0002r1.participant_institution_control_number == '123'
    assert slb0002r1.participant_ispb == '31680153'
    assert slb0002r1.str_control_number == 'STR20250101000000001'
    assert slb0002r1.slb_settlement_status == SlbSettlementStatus.EFFECTED
    assert slb0002r1.settlement_timestamp == datetime(2025, 12, 10, 17, 9, tzinfo=UTC)
    assert slb0002r1.settlement_date == date(2025, 12, 10)


def test_slb0002e_general_error_from_xml() -> None:
    xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/SLB/SLB0002.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>316801512509080000001</NUOp>
        </BCMSG>
        <SISMSG>
            <SLB0002E CodErro="EGEN0050">
                <CodMsg>SLB0002</CodMsg>
                <NumCtrlPart>123</NumCtrlPart>
                <ISPBPart>31680153</ISPBPart>
                <NumCtrlSLBOr>SLB20250101000000001</NumCtrlSLBOr>
                <NivelPref>B</NivelPref>
                <VlrLanc>139.0</VlrLanc>
                <DtMovto>2025-12-10</DtMovto>
            </SLB0002E>
        </SISMSG>
    </DOC>
    """

    slb0002e = SLB0002E.from_xml(xml)

    assert isinstance(slb0002e, SLB0002E)
    assert slb0002e.from_ispb == '31680151'
    assert slb0002e.to_ispb == '00038166'
    assert slb0002e.system_domain == 'SPB01'
    assert slb0002e.operation_number == '316801512509080000001'
    assert slb0002e.message_code == 'SLB0002'
    assert slb0002e.participant_institution_control_number == '123'
    assert slb0002e.participant_ispb == '31680153'
    assert slb0002e.original_slb_control_number == 'SLB20250101000000001'
    assert slb0002e.priority == Priority.HIGH
    assert slb0002e.amount == Decimal('139.0')
    assert slb0002e.settlement_date == date(2025, 12, 10)

    assert slb0002e.general_error_code == 'EGEN0050'


def test_slb0002e_tag_error_from_xml() -> None:
    xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/SLB/SLB0002E.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>316801512509080000001</NUOp>
        </BCMSG>
        <SISMSG>
            <SLB0002E>
                <CodMsg>SLB0002</CodMsg>
                <NumCtrlPart>123</NumCtrlPart>
                <ISPBPart>31680153</ISPBPart>
                <NumCtrlSLBOr CodErro="EPCN0100">SLB20250101000000001</NumCtrlSLBOr>
                <NivelPref>B</NivelPref>
                <VlrLanc>139.0</VlrLanc>
                <DtMovto>2025-12-10</DtMovto>
            </SLB0002E>
        </SISMSG>
    </DOC>
    """

    slb0002e = SLB0002E.from_xml(xml)

    assert isinstance(slb0002e, SLB0002E)
    assert slb0002e.from_ispb == '31680151'
    assert slb0002e.to_ispb == '00038166'
    assert slb0002e.system_domain == 'SPB01'
    assert slb0002e.operation_number == '316801512509080000001'
    assert slb0002e.message_code == 'SLB0002'
    assert slb0002e.participant_institution_control_number == '123'
    assert slb0002e.participant_ispb == '31680153'
    assert slb0002e.original_slb_control_number == 'SLB20250101000000001'
    assert slb0002e.priority == Priority.HIGH
    assert slb0002e.amount == Decimal('139.0')
    assert slb0002e.settlement_date == date(2025, 12, 10)

    assert slb0002e.original_slb_control_number_error_code == 'EPCN0100'


def test_slb0002_roundtrip() -> None:
    params = make_valid_slb0002_params()

    slb0002 = SLB0002.model_validate(params)
    xml = slb0002.to_xml()
    slb0002_from_xml = SLB0002.from_xml(xml)

    assert slb0002 == slb0002_from_xml


def test_slb0002r1_roundtrip() -> None:
    params = make_valid_slb0002r1_params()

    slb0002r1 = SLB0002R1.model_validate(params)
    xml = slb0002r1.to_xml()
    slb0002r1_from_xml = SLB0002R1.from_xml(xml)

    assert slb0002r1 == slb0002r1_from_xml


def test_slb0002_from_xml_missing_required_fields() -> None:
    xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/SLB/SLB0002.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>316801512509080000001</NUOp>
        </BCMSG>
        <SISMSG>
            <SLB0002>
                <CodMsg>SLB0002</CodMsg>
                <NivelPref>B</NivelPref>
            </SLB0002>
        </SISMSG>
    </DOC>
    """

    with pytest.raises(ValidationError) as exc:
        SLB0002.from_xml(xml)

    missing_fields = extract_missing_fields(exc.value)
    assert missing_fields == {
        'participant_institution_control_number',
        'participant_ispb',
        'original_slb_control_number',
        'amount',
        'settlement_date',
    }
