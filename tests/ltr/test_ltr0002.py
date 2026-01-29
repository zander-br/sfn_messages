from datetime import date, datetime
from typing import Any

import pytest
from pydantic import ValidationError

from sfn_messages.core.types import ReconciliationType
from sfn_messages.ltr.ltr0002 import LTR0002, LTR0002E, LTR0002R1
from tests.conftest import extract_missing_fields, normalize_xml


def make_valid_ltr0002_params() -> dict[str, Any]:
    return {
        'from_ispb': '31680151',
        'to_ispb': '00038166',
        'system_domain': 'SPB01',
        'operation_number': '31680151250908000000001',
        'message_code': 'LTR0002',
        'institution_control_number': '123',
        'institution_ispb': '31680151',
        'original_ltr_control_number': '321',
        'ltr_ispb': '31680153',
        'institution_datetime': '2026-01-28T14:12:00',
        'reconciliation_type': 'CONFIRM',
        'settlement_date': '2026-01-28',
    }


def make_valid_ltr0002r1_params() -> dict[str, Any]:
    return {
        'from_ispb': '31680151',
        'to_ispb': '00038166',
        'system_domain': 'SPB01',
        'operation_number': '31680151250908000000001',
        'message_code': 'LTR0002R1',
        'institution_control_number': '123',
        'ltr_ispb': '31680153',
        'ltr_datetime': '2026-01-28T14:14:00',
        'settlement_date': '2026-01-28',
    }


def make_valid_ltr0002e_params(*, general_error: bool = False) -> dict[str, Any]:
    ltr0002e = {
        'from_ispb': '31680151',
        'to_ispb': '00038166',
        'system_domain': 'SPB01',
        'operation_number': '31680151250908000000001',
        'message_code': 'LTR0002E',
        'institution_control_number': '123',
        'institution_ispb': '31680151',
        'original_ltr_control_number': '321',
        'ltr_ispb': '31680153',
        'institution_datetime': '2026-01-28T14:12:00',
        'reconciliation_type': 'CONFIRM',
        'settlement_date': '2026-01-28',
    }

    if general_error:
        ltr0002e['general_error_code'] = 'EGEN0050'
    else:
        ltr0002e['ltr_ispb_error_code'] = 'EGEN0051'

    return ltr0002e


def test_ltr0002_valid_model() -> None:
    params = make_valid_ltr0002_params()
    ltr0002 = LTR0002.model_validate(params)

    assert isinstance(ltr0002, LTR0002)
    assert ltr0002.from_ispb == '31680151'
    assert ltr0002.to_ispb == '00038166'
    assert ltr0002.system_domain == 'SPB01'
    assert ltr0002.operation_number == '31680151250908000000001'
    assert ltr0002.message_code == 'LTR0002'
    assert ltr0002.institution_control_number == '123'
    assert ltr0002.institution_ispb == '31680151'
    assert ltr0002.original_ltr_control_number == '321'
    assert ltr0002.ltr_ispb == '31680153'
    assert ltr0002.institution_datetime == datetime(2026, 1, 28, 14, 12)
    assert ltr0002.reconciliation_type == ReconciliationType.CONFIRM
    assert ltr0002.settlement_date == date(2026, 1, 28)


def test_ltr0002r1_valid_model() -> None:
    params = make_valid_ltr0002r1_params()
    ltr0002r1 = LTR0002R1.model_validate(params)

    assert isinstance(ltr0002r1, LTR0002R1)
    assert ltr0002r1.from_ispb == '31680151'
    assert ltr0002r1.to_ispb == '00038166'
    assert ltr0002r1.system_domain == 'SPB01'
    assert ltr0002r1.operation_number == '31680151250908000000001'
    assert ltr0002r1.message_code == 'LTR0002R1'
    assert ltr0002r1.institution_control_number == '123'
    assert ltr0002r1.ltr_ispb == '31680153'
    assert ltr0002r1.ltr_datetime == datetime(2026, 1, 28, 14, 14)
    assert ltr0002r1.settlement_date == date(2026, 1, 28)


def test_ltr0002e_general_error_valid_model() -> None:
    params = make_valid_ltr0002e_params(general_error=True)
    ltr0002e = LTR0002E.model_validate(params)

    assert isinstance(ltr0002e, LTR0002E)
    assert ltr0002e.from_ispb == '31680151'
    assert ltr0002e.to_ispb == '00038166'
    assert ltr0002e.system_domain == 'SPB01'
    assert ltr0002e.operation_number == '31680151250908000000001'
    assert ltr0002e.message_code == 'LTR0002E'
    assert ltr0002e.institution_control_number == '123'
    assert ltr0002e.institution_ispb == '31680151'
    assert ltr0002e.original_ltr_control_number == '321'
    assert ltr0002e.ltr_ispb == '31680153'
    assert ltr0002e.institution_datetime == datetime(2026, 1, 28, 14, 12)
    assert ltr0002e.reconciliation_type == ReconciliationType.CONFIRM
    assert ltr0002e.settlement_date == date(2026, 1, 28)
    assert ltr0002e.general_error_code == 'EGEN0050'


def test_ltr0002e_tag_error_valid_model() -> None:
    params = make_valid_ltr0002e_params()
    ltr0002e = LTR0002E.model_validate(params)

    assert isinstance(ltr0002e, LTR0002E)
    assert ltr0002e.from_ispb == '31680151'
    assert ltr0002e.to_ispb == '00038166'
    assert ltr0002e.system_domain == 'SPB01'
    assert ltr0002e.operation_number == '31680151250908000000001'
    assert ltr0002e.message_code == 'LTR0002E'
    assert ltr0002e.institution_control_number == '123'
    assert ltr0002e.institution_ispb == '31680151'
    assert ltr0002e.original_ltr_control_number == '321'
    assert ltr0002e.ltr_ispb == '31680153'
    assert ltr0002e.institution_datetime == datetime(2026, 1, 28, 14, 12)
    assert ltr0002e.reconciliation_type == ReconciliationType.CONFIRM
    assert ltr0002e.settlement_date == date(2026, 1, 28)
    assert ltr0002e.ltr_ispb_error_code == 'EGEN0051'


def test_ltr0002_missing_required_fields() -> None:
    with pytest.raises(ValidationError) as exc:
        LTR0002.model_validate({})

    missing_fields = extract_missing_fields(exc.value)
    assert missing_fields == {
        'from_ispb',
        'to_ispb',
        'system_domain',
        'operation_number',
        'institution_control_number',
        'institution_ispb',
        'original_ltr_control_number',
        'ltr_ispb',
        'institution_datetime',
        'reconciliation_type',
        'settlement_date',
    }


def test_ltr0002r1_missing_required_fields() -> None:
    with pytest.raises(ValidationError) as exc:
        LTR0002R1.model_validate({})

    missing_fields = extract_missing_fields(exc.value)
    assert missing_fields == {
        'from_ispb',
        'to_ispb',
        'system_domain',
        'operation_number',
        'institution_control_number',
        'ltr_ispb',
        'ltr_datetime',
        'settlement_date',
    }


def test_ltr0002_to_xml() -> None:
    params = make_valid_ltr0002_params()
    ltr0002 = LTR0002.model_validate(params)

    xml = ltr0002.to_xml()

    expected_xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/SPB/LTR0002.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>31680151250908000000001</NUOp>
        </BCMSG>
        <SISMSG>
            <LTR0002>
                <CodMsg>LTR0002</CodMsg>
                <NumCtrlIF>123</NumCtrlIF>
                <ISPBIF>31680151</ISPBIF>
                <NumCtrlLTROr>321</NumCtrlLTROr>
                <ISPBLTR>31680153</ISPBLTR>
                <DtHrIF>2026-01-28T14:12:00</DtHrIF>
                <TpConf_Divg>C</TpConf_Divg>
                <DtMovto>2026-01-28</DtMovto>
            </LTR0002>
        </SISMSG>
    </DOC>
    """
    assert normalize_xml(expected_xml) == normalize_xml(xml)


def test_ltr0002r1_to_xml() -> None:
    params = make_valid_ltr0002r1_params()
    ltr0002r1 = LTR0002R1.model_validate(params)

    xml = ltr0002r1.to_xml()

    expected_xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/SPB/LTR0002.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>31680151250908000000001</NUOp>
        </BCMSG>
        <SISMSG>
            <LTR0002R1>
                <CodMsg>LTR0002R1</CodMsg>
                <NumCtrlIF>123</NumCtrlIF>
                <ISPBLTR>31680153</ISPBLTR>
                <DtHrLTR>2026-01-28T14:14:00</DtHrLTR>
                <DtMovto>2026-01-28</DtMovto>
            </LTR0002R1>
        </SISMSG>
    </DOC>
    """
    assert normalize_xml(expected_xml) == normalize_xml(xml)


def test_ltr0002e_general_error_to_xml() -> None:
    params = make_valid_ltr0002e_params(general_error=True)
    ltr0002e = LTR0002E.model_validate(params)

    xml = ltr0002e.to_xml()

    expected_xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/SPB/LTR0002E.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>31680151250908000000001</NUOp>
        </BCMSG>
        <SISMSG>
            <LTR0002 CodErro="EGEN0050">
                <CodMsg>LTR0002E</CodMsg>
                <NumCtrlIF>123</NumCtrlIF>
                <ISPBIF>31680151</ISPBIF>
                <NumCtrlLTROr>321</NumCtrlLTROr>
                <ISPBLTR>31680153</ISPBLTR>
                <DtHrIF>2026-01-28T14:12:00</DtHrIF>
                <TpConf_Divg>C</TpConf_Divg>
                <DtMovto>2026-01-28</DtMovto>
            </LTR0002>
        </SISMSG>
    </DOC>
    """
    assert normalize_xml(expected_xml) == normalize_xml(xml)


def test_ltr0002e_tag_error_to_xml() -> None:
    params = make_valid_ltr0002e_params()
    ltr0002e = LTR0002E.model_validate(params)

    xml = ltr0002e.to_xml()

    expected_xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/SPB/LTR0002E.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>31680151250908000000001</NUOp>
        </BCMSG>
        <SISMSG>
            <LTR0002>
                <CodMsg>LTR0002E</CodMsg>
                <NumCtrlIF>123</NumCtrlIF>
                <ISPBIF>31680151</ISPBIF>
                <NumCtrlLTROr>321</NumCtrlLTROr>
                <ISPBLTR CodErro="EGEN0051">31680153</ISPBLTR>
                <DtHrIF>2026-01-28T14:12:00</DtHrIF>
                <TpConf_Divg>C</TpConf_Divg>
                <DtMovto>2026-01-28</DtMovto>
            </LTR0002>
        </SISMSG>
    </DOC>
    """
    assert normalize_xml(expected_xml) == normalize_xml(xml)


def test_ltr0002_from_xml() -> None:
    xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/SPB/LTR0002.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>31680151250908000000001</NUOp>
        </BCMSG>
        <SISMSG>
            <LTR0002>
                <CodMsg>LTR0002</CodMsg>
                <NumCtrlIF>123</NumCtrlIF>
                <ISPBIF>31680151</ISPBIF>
                <NumCtrlLTROr>321</NumCtrlLTROr>
                <ISPBLTR>31680153</ISPBLTR>
                <DtHrIF>2026-01-28T14:12:00</DtHrIF>
                <TpConf_Divg>C</TpConf_Divg>
                <DtMovto>2026-01-28</DtMovto>
            </LTR0002>
        </SISMSG>
    </DOC>
    """

    ltr0002 = LTR0002.from_xml(xml)

    assert isinstance(ltr0002, LTR0002)
    assert ltr0002.from_ispb == '31680151'
    assert ltr0002.to_ispb == '00038166'
    assert ltr0002.system_domain == 'SPB01'
    assert ltr0002.operation_number == '31680151250908000000001'
    assert ltr0002.message_code == 'LTR0002'
    assert ltr0002.institution_control_number == '123'
    assert ltr0002.institution_ispb == '31680151'
    assert ltr0002.original_ltr_control_number == '321'
    assert ltr0002.ltr_ispb == '31680153'
    assert ltr0002.institution_datetime == datetime(2026, 1, 28, 14, 12)
    assert ltr0002.reconciliation_type == ReconciliationType.CONFIRM
    assert ltr0002.settlement_date == date(2026, 1, 28)


def test_ltr0002r1_from_xml() -> None:
    xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/SPB/LTR0002.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>31680151250908000000001</NUOp>
        </BCMSG>
        <SISMSG>
            <LTR0002R1>
                <CodMsg>LTR0002R1</CodMsg>
                <NumCtrlIF>123</NumCtrlIF>
                <ISPBLTR>31680153</ISPBLTR>
                <DtHrLTR>2026-01-28T14:14:00</DtHrLTR>
                <DtMovto>2026-01-28</DtMovto>
            </LTR0002R1>
        </SISMSG>
    </DOC>
    """

    ltr0002r1 = LTR0002R1.from_xml(xml)

    assert isinstance(ltr0002r1, LTR0002R1)
    assert ltr0002r1.from_ispb == '31680151'
    assert ltr0002r1.to_ispb == '00038166'
    assert ltr0002r1.system_domain == 'SPB01'
    assert ltr0002r1.operation_number == '31680151250908000000001'
    assert ltr0002r1.message_code == 'LTR0002R1'
    assert ltr0002r1.institution_control_number == '123'
    assert ltr0002r1.ltr_ispb == '31680153'
    assert ltr0002r1.ltr_datetime == datetime(2026, 1, 28, 14, 14)
    assert ltr0002r1.settlement_date == date(2026, 1, 28)


def test_ltr0002e_general_error_from_xml() -> None:
    xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/SPB/LTR0002E.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>31680151250908000000001</NUOp>
        </BCMSG>
        <SISMSG>
            <LTR0002 CodErro="EGEN0050">
                <CodMsg>LTR0002E</CodMsg>
                <NumCtrlIF>123</NumCtrlIF>
                <ISPBIF>31680151</ISPBIF>
                <NumCtrlLTROr>321</NumCtrlLTROr>
                <ISPBLTR>31680153</ISPBLTR>
                <DtHrIF>2026-01-28T14:12:00</DtHrIF>
                <TpConf_Divg>C</TpConf_Divg>
                <DtMovto>2026-01-28</DtMovto>
            </LTR0002>
        </SISMSG>
    </DOC>
    """

    ltr0002e = LTR0002E.from_xml(xml)

    assert isinstance(ltr0002e, LTR0002E)
    assert ltr0002e.from_ispb == '31680151'
    assert ltr0002e.to_ispb == '00038166'
    assert ltr0002e.system_domain == 'SPB01'
    assert ltr0002e.operation_number == '31680151250908000000001'
    assert ltr0002e.message_code == 'LTR0002E'
    assert ltr0002e.institution_control_number == '123'
    assert ltr0002e.institution_ispb == '31680151'
    assert ltr0002e.original_ltr_control_number == '321'
    assert ltr0002e.ltr_ispb == '31680153'
    assert ltr0002e.institution_datetime == datetime(2026, 1, 28, 14, 12)
    assert ltr0002e.reconciliation_type == ReconciliationType.CONFIRM
    assert ltr0002e.settlement_date == date(2026, 1, 28)
    assert ltr0002e.general_error_code == 'EGEN0050'


def test_ltr0002e_tag_error_from_xml() -> None:
    xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/SPB/LTR0002E.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>31680151250908000000001</NUOp>
        </BCMSG>
        <SISMSG>
            <LTR0002>
                <CodMsg>LTR0002E</CodMsg>
                <NumCtrlIF>123</NumCtrlIF>
                <ISPBIF>31680151</ISPBIF>
                <NumCtrlLTROr>321</NumCtrlLTROr>
                <ISPBLTR CodErro="EGEN0051">31680153</ISPBLTR>
                <DtHrIF>2026-01-28T14:12:00</DtHrIF>
                <TpConf_Divg>C</TpConf_Divg>
                <DtMovto>2026-01-28</DtMovto>
            </LTR0002>
        </SISMSG>
    </DOC>
    """

    ltr0002e = LTR0002E.from_xml(xml)

    assert isinstance(ltr0002e, LTR0002E)
    assert ltr0002e.from_ispb == '31680151'
    assert ltr0002e.to_ispb == '00038166'
    assert ltr0002e.system_domain == 'SPB01'
    assert ltr0002e.operation_number == '31680151250908000000001'
    assert ltr0002e.message_code == 'LTR0002E'
    assert ltr0002e.institution_control_number == '123'
    assert ltr0002e.institution_ispb == '31680151'
    assert ltr0002e.original_ltr_control_number == '321'
    assert ltr0002e.ltr_ispb == '31680153'
    assert ltr0002e.institution_datetime == datetime(2026, 1, 28, 14, 12)
    assert ltr0002e.reconciliation_type == ReconciliationType.CONFIRM
    assert ltr0002e.settlement_date == date(2026, 1, 28)
    assert ltr0002e.ltr_ispb_error_code == 'EGEN0051'


def test_ltr0002_roundtrip() -> None:
    params = make_valid_ltr0002_params()

    ltr0002 = LTR0002.model_validate(params)
    xml = ltr0002.to_xml()
    ltr0002_from_xml = LTR0002.from_xml(xml)

    assert ltr0002 == ltr0002_from_xml


def test_ltr0002r1_roundtrip() -> None:
    params = make_valid_ltr0002r1_params()

    ltr0002r1 = LTR0002R1.model_validate(params)
    xml = ltr0002r1.to_xml()
    ltr0002r1_from_xml = LTR0002R1.from_xml(xml)

    assert ltr0002r1 == ltr0002r1_from_xml
