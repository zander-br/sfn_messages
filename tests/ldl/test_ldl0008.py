from datetime import date, datetime
from decimal import Decimal
from typing import Any

import pytest
from pydantic import ValidationError

from sfn_messages.core.types import LdlSettlementStatus, PaymentType
from sfn_messages.ldl.ldl0008 import (
    LDL0008,
    LDL0008E,
    LDL0008R1,
    LDL0008R2,
    EmissionEventGroup,
    EmissionEventGroupError,
    EmissionEventGroupR2,
)
from tests.conftest import extract_missing_fields, normalize_xml

EMISSION_EVENT_SIZE = 2


def make_valid_ldl0008_params() -> dict[str, Any]:
    return {
        'from_ispb': '31680151',
        'to_ispb': '00038166',
        'system_domain': 'SPB01',
        'operation_number': '31680151250908000000001',
        'message_code': 'LDL0008',
        'institution_control_number': '123',
        'institution_ispb': '31680151',
        'original_ldl_control_number': '321',
        'ldl_ispb': '31680153',
        'amount': 933.00,
        'emission_event_group': [
            {
                'cnpj': '53753940000118',
                'amount': 312.0,
                'payment_type_ldl': 'REMUNERATION',
                'payment_number': '312',
                'participant_identifier': '55386424',
            },
            {
                'cnpj': '50214141000185',
                'amount': 621.0,
                'payment_type_ldl': 'EARNING',
                'payment_number': '222',
                'participant_identifier': '43075534',
            },
        ],
        'settlement_date': '2025-12-09',
    }


def make_valid_ldl0008r1_params() -> dict[str, Any]:
    return {
        'from_ispb': '31680151',
        'to_ispb': '00038166',
        'system_domain': 'SPB01',
        'operation_number': '31680151250908000000001',
        'message_code': 'LDL0008R1',
        'institution_control_number': '123',
        'institution_ispb': '31680151',
        'str_control_number': 'STR20250101000000001',
        'ldl_settlement_status': 'EFFECTIVE',
        'settlement_timestamp': '2025-12-09T10:02:00',
        'settlement_date': '2025-12-09',
    }


def make_valid_ldl0008r2_params() -> dict[str, Any]:
    return {
        'from_ispb': '31680151',
        'to_ispb': '00038166',
        'system_domain': 'SPB01',
        'operation_number': '31680151250908000000001',
        'message_code': 'LDL0008R2',
        'str_control_number': 'STR20250101000000001',
        'original_ldl_control_number': '321',
        'vendor_timestamp': '2025-12-09T10:02:00',
        'institution_ispb': '31680151',
        'ldl_ispb': '31680153',
        'amount': 933.0,
        'emission_event_group': [
            {
                'cnpj': '53753940000118',
                'amount': 312.0,
                'payment_type_ldl': 'REMUNERATION',
                'payment_number': '312',
                'participant_identifier': '55386424',
            },
            {
                'cnpj': '50214141000185',
                'amount': 621.0,
                'payment_type_ldl': 'EARNING',
                'payment_number': '222',
                'participant_identifier': '43075534',
            },
        ],
        'settlement_date': '2025-12-09',
    }


def make_valid_ldl0008e_params(*, general_error: bool = False) -> dict[str, Any]:
    ldl0008e: dict[str, Any] = {
        'from_ispb': '31680151',
        'to_ispb': '00038166',
        'system_domain': 'SPB01',
        'operation_number': '31680151250908000000001',
        'message_code': 'LDL0008E',
        'institution_control_number': '123',
        'institution_ispb': '31680151',
        'original_ldl_control_number': '321',
        'ldl_ispb': '31680153',
        'amount': 933.00,
        'emission_event_group': [
            {
                'cnpj': '53753940000118',
                'amount': 312.0,
                'payment_type_ldl': 'REMUNERATION',
                'payment_number': '312',
                'participant_identifier': '55386424',
            },
            {
                'cnpj': '50214141000185',
                'amount': 621.0,
                'payment_type_ldl': 'EARNING',
                'payment_number': '222',
                'participant_identifier': '43075534',
            },
        ],
        'settlement_date': '2025-12-09',
    }

    if general_error:
        ldl0008e['general_error_code'] = 'EGEN0050'
    else:
        ldl0008e['ldl_ispb_error_code'] = 'EGEN0051'
        ldl0008e['emission_event_group'][0]['payment_type_ldl_error_code'] = 'ELDL0019'

    return ldl0008e


def test_ldl0008_valid_model() -> None:
    params = make_valid_ldl0008_params()
    ldl0008 = LDL0008.model_validate(params)

    assert isinstance(ldl0008, LDL0008)
    assert ldl0008.from_ispb == '31680151'
    assert ldl0008.to_ispb == '00038166'
    assert ldl0008.system_domain == 'SPB01'
    assert ldl0008.operation_number == '31680151250908000000001'
    assert ldl0008.message_code == 'LDL0008'
    assert ldl0008.institution_control_number == '123'
    assert ldl0008.institution_ispb == '31680151'
    assert ldl0008.original_ldl_control_number == '321'
    assert ldl0008.ldl_ispb == '31680153'
    assert ldl0008.amount == Decimal('933.00')
    assert ldl0008.settlement_date == date(2025, 12, 9)

    assert len(ldl0008.emission_event_group) == EMISSION_EVENT_SIZE
    event1 = ldl0008.emission_event_group[0]
    event2 = ldl0008.emission_event_group[1]
    assert isinstance(event1, EmissionEventGroup)
    assert event1.cnpj == '53753940000118'
    assert event1.amount == Decimal('312.0')
    assert event1.payment_type_ldl == PaymentType.REMUNERATION
    assert event1.payment_number == '312'
    assert event1.participant_identifier == '55386424'

    assert isinstance(event2, EmissionEventGroup)
    assert event2.cnpj == '50214141000185'
    assert event2.amount == Decimal('621.0')
    assert event2.payment_type_ldl == PaymentType.EARNING
    assert event2.payment_number == '222'
    assert event2.participant_identifier == '43075534'


def test_ldl0008r1_valid_model() -> None:
    params = make_valid_ldl0008r1_params()
    ldl0008r1 = LDL0008R1.model_validate(params)

    assert isinstance(ldl0008r1, LDL0008R1)
    assert ldl0008r1.from_ispb == '31680151'
    assert ldl0008r1.to_ispb == '00038166'
    assert ldl0008r1.system_domain == 'SPB01'
    assert ldl0008r1.operation_number == '31680151250908000000001'
    assert ldl0008r1.message_code == 'LDL0008R1'
    assert ldl0008r1.institution_control_number == '123'
    assert ldl0008r1.institution_ispb == '31680151'
    assert ldl0008r1.str_control_number == 'STR20250101000000001'
    assert ldl0008r1.ldl_settlement_status == LdlSettlementStatus.EFFECTIVE
    assert ldl0008r1.settlement_timestamp == datetime(2025, 12, 9, 10, 2)
    assert ldl0008r1.settlement_date == date(2025, 12, 9)


def test_ldl0008r2_valid_model() -> None:
    params = make_valid_ldl0008r2_params()
    ldl0008r2 = LDL0008R2.model_validate(params)

    assert isinstance(ldl0008r2, LDL0008R2)
    assert ldl0008r2.from_ispb == '31680151'
    assert ldl0008r2.to_ispb == '00038166'
    assert ldl0008r2.system_domain == 'SPB01'
    assert ldl0008r2.operation_number == '31680151250908000000001'
    assert ldl0008r2.message_code == 'LDL0008R2'
    assert ldl0008r2.str_control_number == 'STR20250101000000001'
    assert ldl0008r2.original_ldl_control_number == '321'
    assert ldl0008r2.vendor_timestamp == datetime(2025, 12, 9, 10, 2)
    assert ldl0008r2.institution_ispb == '31680151'
    assert ldl0008r2.ldl_ispb == '31680153'
    assert ldl0008r2.amount == Decimal('933.0')
    assert ldl0008r2.settlement_date == date(2025, 12, 9)

    assert len(ldl0008r2.emission_event_group) == EMISSION_EVENT_SIZE
    event1 = ldl0008r2.emission_event_group[0]
    event2 = ldl0008r2.emission_event_group[1]
    assert isinstance(event1, EmissionEventGroupR2)
    assert event1.cnpj == '53753940000118'
    assert event1.amount == Decimal('312.0')
    assert event1.payment_type_ldl == PaymentType.REMUNERATION
    assert event1.payment_number == '312'
    assert event1.participant_identifier == '55386424'

    assert isinstance(event2, EmissionEventGroupR2)
    assert event2.cnpj == '50214141000185'
    assert event2.amount == Decimal('621.0')
    assert event2.payment_type_ldl == PaymentType.EARNING
    assert event2.payment_number == '222'
    assert event2.participant_identifier == '43075534'


def test_ldl0008e_general_error_valid_model() -> None:
    params = make_valid_ldl0008e_params(general_error=True)
    ldl0008e = LDL0008E.model_validate(params)

    assert isinstance(ldl0008e, LDL0008E)
    assert ldl0008e.from_ispb == '31680151'
    assert ldl0008e.to_ispb == '00038166'
    assert ldl0008e.system_domain == 'SPB01'
    assert ldl0008e.operation_number == '31680151250908000000001'
    assert ldl0008e.message_code == 'LDL0008E'
    assert ldl0008e.institution_control_number == '123'
    assert ldl0008e.institution_ispb == '31680151'
    assert ldl0008e.original_ldl_control_number == '321'
    assert ldl0008e.ldl_ispb == '31680153'
    assert ldl0008e.amount == Decimal('933.00')
    assert ldl0008e.settlement_date == date(2025, 12, 9)
    assert ldl0008e.general_error_code == 'EGEN0050'

    assert len(ldl0008e.emission_event_group) == EMISSION_EVENT_SIZE
    event1 = ldl0008e.emission_event_group[0]
    event2 = ldl0008e.emission_event_group[1]
    assert isinstance(event1, EmissionEventGroupError)
    assert event1.cnpj == '53753940000118'
    assert event1.amount == Decimal('312.0')
    assert event1.payment_type_ldl == PaymentType.REMUNERATION
    assert event1.payment_number == '312'
    assert event1.participant_identifier == '55386424'

    assert isinstance(event2, EmissionEventGroupError)
    assert event2.cnpj == '50214141000185'
    assert event2.amount == Decimal('621.0')
    assert event2.payment_type_ldl == PaymentType.EARNING
    assert event2.payment_number == '222'
    assert event2.participant_identifier == '43075534'


def test_ldl0008e_tag_error_valid_model() -> None:
    params = make_valid_ldl0008e_params()
    ldl0008 = LDL0008E.model_validate(params)

    assert isinstance(ldl0008, LDL0008E)
    assert ldl0008.from_ispb == '31680151'
    assert ldl0008.to_ispb == '00038166'
    assert ldl0008.system_domain == 'SPB01'
    assert ldl0008.operation_number == '31680151250908000000001'
    assert ldl0008.message_code == 'LDL0008E'
    assert ldl0008.institution_control_number == '123'
    assert ldl0008.institution_ispb == '31680151'
    assert ldl0008.original_ldl_control_number == '321'
    assert ldl0008.ldl_ispb == '31680153'
    assert ldl0008.amount == Decimal('933.00')
    assert ldl0008.settlement_date == date(2025, 12, 9)
    assert ldl0008.ldl_ispb_error_code == 'EGEN0051'

    assert len(ldl0008.emission_event_group) == EMISSION_EVENT_SIZE
    event1 = ldl0008.emission_event_group[0]
    event2 = ldl0008.emission_event_group[1]
    assert isinstance(event1, EmissionEventGroupError)
    assert event1.cnpj == '53753940000118'
    assert event1.amount == Decimal('312.0')
    assert event1.payment_type_ldl == PaymentType.REMUNERATION
    assert event1.payment_number == '312'
    assert event1.participant_identifier == '55386424'
    assert event1.payment_type_ldl_error_code == 'ELDL0019'

    assert isinstance(event2, EmissionEventGroupError)
    assert event2.cnpj == '50214141000185'
    assert event2.amount == Decimal('621.0')
    assert event2.payment_type_ldl == PaymentType.EARNING
    assert event2.payment_number == '222'
    assert event2.participant_identifier == '43075534'


def test_ldl0008_missing_required_fields() -> None:
    with pytest.raises(ValidationError) as exc:
        LDL0008.model_validate({})

    missing_fields = extract_missing_fields(exc.value)
    assert missing_fields == {
        'from_ispb',
        'to_ispb',
        'system_domain',
        'operation_number',
        'institution_control_number',
        'institution_ispb',
        'original_ldl_control_number',
        'ldl_ispb',
        'amount',
        'settlement_date',
    }


def test_ldl0008r1_missing_required_fields() -> None:
    with pytest.raises(ValidationError) as exc:
        LDL0008R1.model_validate({})

    missing_fields = extract_missing_fields(exc.value)
    assert missing_fields == {
        'from_ispb',
        'to_ispb',
        'system_domain',
        'operation_number',
        'institution_control_number',
        'institution_ispb',
        'str_control_number',
        'ldl_settlement_status',
        'settlement_timestamp',
        'settlement_date',
    }


def test_ldl0008r2_missing_required_fields() -> None:
    with pytest.raises(ValidationError) as exc:
        LDL0008R2.model_validate({})

    missing_fields = extract_missing_fields(exc.value)
    assert missing_fields == {
        'from_ispb',
        'to_ispb',
        'system_domain',
        'operation_number',
        'str_control_number',
        'original_ldl_control_number',
        'vendor_timestamp',
        'institution_ispb',
        'ldl_ispb',
        'amount',
        'settlement_date',
    }


def test_ldl0008_to_xml() -> None:
    params = make_valid_ldl0008_params()
    ldl0008 = LDL0008.model_validate(params)

    xml = ldl0008.to_xml()

    expected_xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/SPB/LDL0008.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>31680151250908000000001</NUOp>
        </BCMSG>
        <SISMSG>
            <LDL0008>
                <CodMsg>LDL0008</CodMsg>
                <NumCtrlIF>123</NumCtrlIF>
                <ISPBIF>31680151</ISPBIF>
                <NumCtrlLDLOr>321</NumCtrlLDLOr>
                <ISPBLDL>31680153</ISPBLDL>
                <VlrLanc>933.0</VlrLanc>
                <Grupo_LDL0008_EvtEms>
                    <CNPJNLiqdant>53753940000118</CNPJNLiqdant>
                    <VlrNLiqdant>312.0</VlrNLiqdant>
                    <TpPgtoLDL>10</TpPgtoLDL>
                    <NumPgtoLDL>312</NumPgtoLDL>
                    <IdentdPartCamr>55386424</IdentdPartCamr>
                </Grupo_LDL0008_EvtEms>
                <Grupo_LDL0008_EvtEms>
                    <CNPJNLiqdant>50214141000185</CNPJNLiqdant>
                    <VlrNLiqdant>621.0</VlrNLiqdant>
                    <TpPgtoLDL>11</TpPgtoLDL>
                    <NumPgtoLDL>222</NumPgtoLDL>
                    <IdentdPartCamr>43075534</IdentdPartCamr>
                </Grupo_LDL0008_EvtEms>
                <DtMovto>2025-12-09</DtMovto>
            </LDL0008>
        </SISMSG>
    </DOC>
    """
    assert normalize_xml(expected_xml) == normalize_xml(xml)


def test_ldl0008r1_to_xml() -> None:
    params = make_valid_ldl0008r1_params()
    ldl0008r1 = LDL0008R1.model_validate(params)

    xml = ldl0008r1.to_xml()

    expected_xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/SPB/LDL0008.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>31680151250908000000001</NUOp>
        </BCMSG>
        <SISMSG>
            <LDL0008R1>
                <CodMsg>LDL0008R1</CodMsg>
                <NumCtrlIF>123</NumCtrlIF>
                <ISPBIF>31680151</ISPBIF>
                <NumCtrlSTR>STR20250101000000001</NumCtrlSTR>
                <SitLancLDL>1</SitLancLDL>
                <DtHrSit>2025-12-09T10:02:00</DtHrSit>
                <DtMovto>2025-12-09</DtMovto>
            </LDL0008R1>
        </SISMSG>
    </DOC>
    """
    assert normalize_xml(expected_xml) == normalize_xml(xml)


def test_ldl0008r2_to_xml() -> None:
    params = make_valid_ldl0008r2_params()
    ldl0008r2 = LDL0008R2.model_validate(params)

    xml = ldl0008r2.to_xml()

    expected_xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/SPB/LDL0008.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>31680151250908000000001</NUOp>
        </BCMSG>
        <SISMSG>
            <LDL0008R2>
                <CodMsg>LDL0008R2</CodMsg>
                <NumCtrlSTR>STR20250101000000001</NumCtrlSTR>
                <NumCtrlLDLOr>321</NumCtrlLDLOr>
                <DtHrBC>2025-12-09T10:02:00</DtHrBC>
                <ISPBIF>31680151</ISPBIF>
                <ISPBLDL>31680153</ISPBLDL>
                <VlrLanc>933.0</VlrLanc>
                <Grupo_LDL0008R2_EvtEms>
                    <CNPJNLiqdant>53753940000118</CNPJNLiqdant>
                    <VlrNLiqdant>312.0</VlrNLiqdant>
                    <TpPgtoLDL>10</TpPgtoLDL>
                    <NumPgtoLDL>312</NumPgtoLDL>
                    <IdentdPartCamr>55386424</IdentdPartCamr>
                </Grupo_LDL0008R2_EvtEms>
                <Grupo_LDL0008R2_EvtEms>
                <CNPJNLiqdant>50214141000185</CNPJNLiqdant>
                    <VlrNLiqdant>621.0</VlrNLiqdant>
                    <TpPgtoLDL>11</TpPgtoLDL>
                    <NumPgtoLDL>222</NumPgtoLDL>
                    <IdentdPartCamr>43075534</IdentdPartCamr>
                </Grupo_LDL0008R2_EvtEms>
                <DtMovto>2025-12-09</DtMovto>
            </LDL0008R2>
        </SISMSG>
    </DOC>
    """
    assert normalize_xml(expected_xml) == normalize_xml(xml)


def test_ldl0008e_general_error_to_xml() -> None:
    params = make_valid_ldl0008e_params(general_error=True)
    ldl0008e = LDL0008E.model_validate(params)

    xml = ldl0008e.to_xml()

    expected_xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/SPB/LDL0008E.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>31680151250908000000001</NUOp>
        </BCMSG>
        <SISMSG>
            <LDL0008 CodErro="EGEN0050">
                <CodMsg>LDL0008E</CodMsg>
                <NumCtrlIF>123</NumCtrlIF>
                <ISPBIF>31680151</ISPBIF>
                <NumCtrlLDLOr>321</NumCtrlLDLOr>
                <ISPBLDL>31680153</ISPBLDL>
                <VlrLanc>933.0</VlrLanc>
                <Grupo_LDL0008_EvtEms>
                    <CNPJNLiqdant>53753940000118</CNPJNLiqdant>
                    <VlrNLiqdant>312.0</VlrNLiqdant>
                    <TpPgtoLDL>10</TpPgtoLDL>
                    <NumPgtoLDL>312</NumPgtoLDL>
                    <IdentdPartCamr>55386424</IdentdPartCamr>
                </Grupo_LDL0008_EvtEms>
                <Grupo_LDL0008_EvtEms>
                    <CNPJNLiqdant>50214141000185</CNPJNLiqdant>
                    <VlrNLiqdant>621.0</VlrNLiqdant>
                    <TpPgtoLDL>11</TpPgtoLDL>
                    <NumPgtoLDL>222</NumPgtoLDL>
                    <IdentdPartCamr>43075534</IdentdPartCamr>
                </Grupo_LDL0008_EvtEms>
                <DtMovto>2025-12-09</DtMovto>
            </LDL0008>
        </SISMSG>
    </DOC>
    """
    assert normalize_xml(expected_xml) == normalize_xml(xml)


def test_ldl0008e_tag_error_to_xml() -> None:
    params = make_valid_ldl0008e_params()
    ldl0008e = LDL0008E.model_validate(params)

    xml = ldl0008e.to_xml()

    expected_xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/SPB/LDL0008E.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>31680151250908000000001</NUOp>
        </BCMSG>
        <SISMSG>
            <LDL0008>
                <CodMsg>LDL0008E</CodMsg>
                <NumCtrlIF>123</NumCtrlIF>
                <ISPBIF>31680151</ISPBIF>
                <NumCtrlLDLOr>321</NumCtrlLDLOr>
                <ISPBLDL CodErro="EGEN0051">31680153</ISPBLDL>
                <VlrLanc>933.0</VlrLanc>
                <Grupo_LDL0008_EvtEms>
                    <CNPJNLiqdant>53753940000118</CNPJNLiqdant>
                    <VlrNLiqdant>312.0</VlrNLiqdant>
                    <TpPgtoLDL CodErro="ELDL0019">10</TpPgtoLDL>
                    <NumPgtoLDL>312</NumPgtoLDL>
                    <IdentdPartCamr>55386424</IdentdPartCamr>
                </Grupo_LDL0008_EvtEms>
                <Grupo_LDL0008_EvtEms>
                    <CNPJNLiqdant>50214141000185</CNPJNLiqdant>
                    <VlrNLiqdant>621.0</VlrNLiqdant>
                    <TpPgtoLDL>11</TpPgtoLDL>
                    <NumPgtoLDL>222</NumPgtoLDL>
                    <IdentdPartCamr>43075534</IdentdPartCamr>
                </Grupo_LDL0008_EvtEms>
                <DtMovto>2025-12-09</DtMovto>
            </LDL0008>
        </SISMSG>
    </DOC>
    """
    assert normalize_xml(expected_xml) == normalize_xml(xml)


def test_ldl0008_from_xml() -> None:
    xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/SPB/LDL0008.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>31680151250908000000001</NUOp>
        </BCMSG>
        <SISMSG>
            <LDL0008>
                <CodMsg>LDL0008</CodMsg>
                <NumCtrlIF>123</NumCtrlIF>
                <ISPBIF>31680151</ISPBIF>
                <NumCtrlLDLOr>321</NumCtrlLDLOr>
                <ISPBLDL>31680153</ISPBLDL>
                <VlrLanc>933.0</VlrLanc>
                <Grupo_LDL0008_EvtEms>
                    <CNPJNLiqdant>53753940000118</CNPJNLiqdant>
                    <VlrNLiqdant>312.0</VlrNLiqdant>
                    <TpPgtoLDL>10</TpPgtoLDL>
                    <NumPgtoLDL>312</NumPgtoLDL>
                    <IdentdPartCamr>55386424</IdentdPartCamr>
                </Grupo_LDL0008_EvtEms>
                <Grupo_LDL0008_EvtEms>
                    <CNPJNLiqdant>50214141000185</CNPJNLiqdant>
                    <VlrNLiqdant>621.0</VlrNLiqdant>
                    <TpPgtoLDL>11</TpPgtoLDL>
                    <NumPgtoLDL>222</NumPgtoLDL>
                    <IdentdPartCamr>43075534</IdentdPartCamr>
                </Grupo_LDL0008_EvtEms>
                <DtMovto>2025-12-09</DtMovto>
            </LDL0008>
        </SISMSG>
    </DOC>
    """

    ldl0008 = LDL0008.from_xml(xml)

    assert isinstance(ldl0008, LDL0008)
    assert ldl0008.from_ispb == '31680151'
    assert ldl0008.to_ispb == '00038166'
    assert ldl0008.system_domain == 'SPB01'
    assert ldl0008.operation_number == '31680151250908000000001'
    assert ldl0008.message_code == 'LDL0008'
    assert ldl0008.institution_control_number == '123'
    assert ldl0008.institution_ispb == '31680151'
    assert ldl0008.original_ldl_control_number == '321'
    assert ldl0008.ldl_ispb == '31680153'
    assert ldl0008.amount == Decimal('933.00')
    assert ldl0008.settlement_date == date(2025, 12, 9)

    assert len(ldl0008.emission_event_group) == EMISSION_EVENT_SIZE
    event1 = ldl0008.emission_event_group[0]
    event2 = ldl0008.emission_event_group[1]
    assert isinstance(event1, EmissionEventGroup)
    assert event1.cnpj == '53753940000118'
    assert event1.amount == Decimal('312.0')
    assert event1.payment_type_ldl == PaymentType.REMUNERATION
    assert event1.payment_number == '312'
    assert event1.participant_identifier == '55386424'

    assert isinstance(event2, EmissionEventGroup)
    assert event2.cnpj == '50214141000185'
    assert event2.amount == Decimal('621.0')
    assert event2.payment_type_ldl == PaymentType.EARNING
    assert event2.payment_number == '222'
    assert event2.participant_identifier == '43075534'


def test_ldl0008r1_from_xml() -> None:
    xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/SPB/LDL0008.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>31680151250908000000001</NUOp>
        </BCMSG>
        <SISMSG>
            <LDL0008R1>
                <CodMsg>LDL0008R1</CodMsg>
                <NumCtrlIF>123</NumCtrlIF>
                <ISPBIF>31680151</ISPBIF>
                <NumCtrlSTR>STR20250101000000001</NumCtrlSTR>
                <SitLancLDL>1</SitLancLDL>
                <DtHrSit>2025-12-09T10:02:00</DtHrSit>
                <DtMovto>2025-12-09</DtMovto>
            </LDL0008R1>
        </SISMSG>
    </DOC>
    """

    ldl0008r1 = LDL0008R1.from_xml(xml)

    assert isinstance(ldl0008r1, LDL0008R1)
    assert ldl0008r1.from_ispb == '31680151'
    assert ldl0008r1.to_ispb == '00038166'
    assert ldl0008r1.system_domain == 'SPB01'
    assert ldl0008r1.operation_number == '31680151250908000000001'
    assert ldl0008r1.message_code == 'LDL0008R1'
    assert ldl0008r1.institution_control_number == '123'
    assert ldl0008r1.institution_ispb == '31680151'
    assert ldl0008r1.str_control_number == 'STR20250101000000001'
    assert ldl0008r1.ldl_settlement_status == LdlSettlementStatus.EFFECTIVE
    assert ldl0008r1.settlement_timestamp == datetime(2025, 12, 9, 10, 2)
    assert ldl0008r1.settlement_date == date(2025, 12, 9)


def test_ldl0008r2_from_xml() -> None:
    xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/SPB/LDL0008.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>31680151250908000000001</NUOp>
        </BCMSG>
        <SISMSG>
            <LDL0008R2>
                <CodMsg>LDL0008R2</CodMsg>
                <NumCtrlSTR>STR20250101000000001</NumCtrlSTR>
                <NumCtrlLDLOr>321</NumCtrlLDLOr>
                <DtHrBC>2025-12-09T10:02:00</DtHrBC>
                <ISPBIF>31680151</ISPBIF>
                <ISPBLDL>31680153</ISPBLDL>
                <VlrLanc>933.0</VlrLanc>
                <Grupo_LDL0008R2_EvtEms>
                    <CNPJNLiqdant>53753940000118</CNPJNLiqdant>
                    <VlrNLiqdant>312.0</VlrNLiqdant>
                    <TpPgtoLDL>10</TpPgtoLDL>
                    <NumPgtoLDL>312</NumPgtoLDL>
                    <IdentdPartCamr>55386424</IdentdPartCamr>
                </Grupo_LDL0008R2_EvtEms>
                <Grupo_LDL0008R2_EvtEms>
                <CNPJNLiqdant>50214141000185</CNPJNLiqdant>
                    <VlrNLiqdant>621.0</VlrNLiqdant>
                    <TpPgtoLDL>11</TpPgtoLDL>
                    <NumPgtoLDL>222</NumPgtoLDL>
                    <IdentdPartCamr>43075534</IdentdPartCamr>
                </Grupo_LDL0008R2_EvtEms>
                <DtMovto>2025-12-09</DtMovto>
            </LDL0008R2>
        </SISMSG>
    </DOC>
    """

    ldl0008r2 = LDL0008R2.from_xml(xml)

    assert isinstance(ldl0008r2, LDL0008R2)
    assert ldl0008r2.from_ispb == '31680151'
    assert ldl0008r2.to_ispb == '00038166'
    assert ldl0008r2.system_domain == 'SPB01'
    assert ldl0008r2.operation_number == '31680151250908000000001'
    assert ldl0008r2.message_code == 'LDL0008R2'
    assert ldl0008r2.str_control_number == 'STR20250101000000001'
    assert ldl0008r2.original_ldl_control_number == '321'
    assert ldl0008r2.vendor_timestamp == datetime(2025, 12, 9, 10, 2)
    assert ldl0008r2.institution_ispb == '31680151'
    assert ldl0008r2.ldl_ispb == '31680153'
    assert ldl0008r2.amount == Decimal('933.0')
    assert ldl0008r2.settlement_date == date(2025, 12, 9)

    assert len(ldl0008r2.emission_event_group) == EMISSION_EVENT_SIZE
    event1 = ldl0008r2.emission_event_group[0]
    event2 = ldl0008r2.emission_event_group[1]
    assert isinstance(event1, EmissionEventGroupR2)
    assert event1.cnpj == '53753940000118'
    assert event1.amount == Decimal('312.0')
    assert event1.payment_type_ldl == PaymentType.REMUNERATION
    assert event1.payment_number == '312'
    assert event1.participant_identifier == '55386424'

    assert isinstance(event2, EmissionEventGroupR2)
    assert event2.cnpj == '50214141000185'
    assert event2.amount == Decimal('621.0')
    assert event2.payment_type_ldl == PaymentType.EARNING
    assert event2.payment_number == '222'
    assert event2.participant_identifier == '43075534'


def test_ldl0008e_general_error_from_xml() -> None:
    xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/SPB/LDL0008E.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>31680151250908000000001</NUOp>
        </BCMSG>
        <SISMSG>
            <LDL0008 CodErro="EGEN0050">
                <CodMsg>LDL0008E</CodMsg>
                <NumCtrlIF>123</NumCtrlIF>
                <ISPBIF>31680151</ISPBIF>
                <NumCtrlLDLOr>321</NumCtrlLDLOr>
                <ISPBLDL>31680153</ISPBLDL>
                <VlrLanc>933.0</VlrLanc>
                <Grupo_LDL0008_EvtEms>
                    <CNPJNLiqdant>53753940000118</CNPJNLiqdant>
                    <VlrNLiqdant>312.0</VlrNLiqdant>
                    <TpPgtoLDL>10</TpPgtoLDL>
                    <NumPgtoLDL>312</NumPgtoLDL>
                    <IdentdPartCamr>55386424</IdentdPartCamr>
                </Grupo_LDL0008_EvtEms>
                <Grupo_LDL0008_EvtEms>
                    <CNPJNLiqdant>50214141000185</CNPJNLiqdant>
                    <VlrNLiqdant>621.0</VlrNLiqdant>
                    <TpPgtoLDL>11</TpPgtoLDL>
                    <NumPgtoLDL>222</NumPgtoLDL>
                    <IdentdPartCamr>43075534</IdentdPartCamr>
                </Grupo_LDL0008_EvtEms>
                <DtMovto>2025-12-09</DtMovto>
            </LDL0008>
        </SISMSG>
    </DOC>
    """

    ldl0008e = LDL0008E.from_xml(xml)

    assert isinstance(ldl0008e, LDL0008E)
    assert ldl0008e.from_ispb == '31680151'
    assert ldl0008e.to_ispb == '00038166'
    assert ldl0008e.system_domain == 'SPB01'
    assert ldl0008e.operation_number == '31680151250908000000001'
    assert ldl0008e.message_code == 'LDL0008E'
    assert ldl0008e.institution_control_number == '123'
    assert ldl0008e.institution_ispb == '31680151'
    assert ldl0008e.original_ldl_control_number == '321'
    assert ldl0008e.ldl_ispb == '31680153'
    assert ldl0008e.amount == Decimal('933.00')
    assert ldl0008e.settlement_date == date(2025, 12, 9)
    assert ldl0008e.general_error_code == 'EGEN0050'

    assert len(ldl0008e.emission_event_group) == EMISSION_EVENT_SIZE
    event1 = ldl0008e.emission_event_group[0]
    event2 = ldl0008e.emission_event_group[1]
    assert isinstance(event1, EmissionEventGroupError)
    assert event1.cnpj == '53753940000118'
    assert event1.amount == Decimal('312.0')
    assert event1.payment_type_ldl == PaymentType.REMUNERATION
    assert event1.payment_number == '312'
    assert event1.participant_identifier == '55386424'

    assert isinstance(event2, EmissionEventGroupError)
    assert event2.cnpj == '50214141000185'
    assert event2.amount == Decimal('621.0')
    assert event2.payment_type_ldl == PaymentType.EARNING
    assert event2.payment_number == '222'
    assert event2.participant_identifier == '43075534'


def test_ldl0008e_tag_error_from_xml() -> None:
    xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/SPB/LDL0008E.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>31680151250908000000001</NUOp>
        </BCMSG>
        <SISMSG>
            <LDL0008>
                <CodMsg>LDL0008E</CodMsg>
                <NumCtrlIF>123</NumCtrlIF>
                <ISPBIF>31680151</ISPBIF>
                <NumCtrlLDLOr>321</NumCtrlLDLOr>
                <ISPBLDL CodErro="EGEN0051">31680153</ISPBLDL>
                <VlrLanc>933.0</VlrLanc>
                <Grupo_LDL0008_EvtEms>
                    <CNPJNLiqdant>53753940000118</CNPJNLiqdant>
                    <VlrNLiqdant>312.0</VlrNLiqdant>
                    <TpPgtoLDL CodErro="ELDL0019">10</TpPgtoLDL>
                    <NumPgtoLDL>312</NumPgtoLDL>
                    <IdentdPartCamr>55386424</IdentdPartCamr>
                </Grupo_LDL0008_EvtEms>
                <Grupo_LDL0008_EvtEms>
                    <CNPJNLiqdant>50214141000185</CNPJNLiqdant>
                    <VlrNLiqdant>621.0</VlrNLiqdant>
                    <TpPgtoLDL>11</TpPgtoLDL>
                    <NumPgtoLDL>222</NumPgtoLDL>
                    <IdentdPartCamr>43075534</IdentdPartCamr>
                </Grupo_LDL0008_EvtEms>
                <DtMovto>2025-12-09</DtMovto>
            </LDL0008>
        </SISMSG>
    </DOC>
    """

    ldl0008e = LDL0008E.from_xml(xml)

    assert isinstance(ldl0008e, LDL0008E)
    assert ldl0008e.from_ispb == '31680151'
    assert ldl0008e.to_ispb == '00038166'
    assert ldl0008e.system_domain == 'SPB01'
    assert ldl0008e.operation_number == '31680151250908000000001'
    assert ldl0008e.message_code == 'LDL0008E'
    assert ldl0008e.institution_control_number == '123'
    assert ldl0008e.institution_ispb == '31680151'
    assert ldl0008e.original_ldl_control_number == '321'
    assert ldl0008e.ldl_ispb == '31680153'
    assert ldl0008e.amount == Decimal('933.00')
    assert ldl0008e.settlement_date == date(2025, 12, 9)
    assert ldl0008e.ldl_ispb_error_code == 'EGEN0051'

    assert len(ldl0008e.emission_event_group) == EMISSION_EVENT_SIZE
    event1 = ldl0008e.emission_event_group[0]
    event2 = ldl0008e.emission_event_group[1]
    assert isinstance(event1, EmissionEventGroupError)
    assert event1.cnpj == '53753940000118'
    assert event1.amount == Decimal('312.0')
    assert event1.payment_type_ldl == PaymentType.REMUNERATION
    assert event1.payment_number == '312'
    assert event1.participant_identifier == '55386424'
    assert event1.payment_type_ldl_error_code == 'ELDL0019'

    assert isinstance(event2, EmissionEventGroupError)
    assert event2.cnpj == '50214141000185'
    assert event2.amount == Decimal('621.0')
    assert event2.payment_type_ldl == PaymentType.EARNING
    assert event2.payment_number == '222'
    assert event2.participant_identifier == '43075534'


def test_ldl0008_roundtrip() -> None:
    params = make_valid_ldl0008_params()

    ldl0008 = LDL0008.model_validate(params)
    xml = ldl0008.to_xml()
    ldl0008_from_xml = LDL0008.from_xml(xml)

    assert ldl0008 == ldl0008_from_xml


def test_ldl0008r1_roundtrip() -> None:
    params = make_valid_ldl0008r1_params()

    ldl0008r1 = LDL0008R1.model_validate(params)
    xml = ldl0008r1.to_xml()
    ldl0008r1_from_xml = LDL0008R1.from_xml(xml)

    assert ldl0008r1 == ldl0008r1_from_xml


def test_ldl0008r2_roundtrip() -> None:
    params = make_valid_ldl0008r2_params()

    ldl0008r2 = LDL0008R2.model_validate(params)
    xml = ldl0008r2.to_xml()
    ldl0008r2_from_xml = LDL0008R2.from_xml(xml)

    assert ldl0008r2 == ldl0008r2_from_xml


def test_ldl0008_from_xml_missing_required_fields() -> None:
    xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/SPB/LDL0008.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>31680151250908000000001</NUOp>
        </BCMSG>
        <SISMSG>
            <LDL0008>
                <CodMsg>LDL0008</CodMsg>
            </LDL0008>
        </SISMSG>
    </DOC>
    """

    with pytest.raises(ValidationError) as exc:
        LDL0008.from_xml(xml)

    missing_fields = extract_missing_fields(exc.value)
    assert missing_fields == {
        'institution_control_number',
        'institution_ispb',
        'original_ldl_control_number',
        'ldl_ispb',
        'amount',
        'settlement_date',
    }
