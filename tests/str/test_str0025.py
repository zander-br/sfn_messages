from datetime import date, time
from decimal import Decimal
from typing import Any

import pytest
from pydantic import ValidationError

from sfn_messages.core.types import AccountType, PersonType, Priority
from sfn_messages.str.str0025 import STR0025
from tests.conftest import extract_missing_fields, normalize_xml


def make_valid_str0025_params() -> dict[str, Any]:
    return {
        'from_ispb': '31680151',
        'operation_number': '316801512509080000001',
        'system_domain': 'SPB01',
        'to_ispb': '00038166',
        'institution_control_number': '31680151202509090425',
        'debtor_institution_ispb': '31680151',
        'debtor_branch': '0001',
        'debtor_account_type': 'CURRENT',
        'debtor_account_number': '12345678',
        'creditor_name': 'John Doe',
        'creditor_type': 'INDIVIDUAL',
        'creditor_document': '69327934075',
        'creditor_institution_ispb': '00038166',
        'amount': 100.00,
        'priority': 'MEDIUM',
        'deposit_identifier': '012345678901234567',
        'scheduled_date': '2025-09-09',
        'scheduled_time': '15:30:00',
        'settlement_date': '2025-09-08',
    }


def test_str0025_valid_model() -> None:
    params = make_valid_str0025_params()
    str0025 = STR0025.model_validate(params)
    assert isinstance(str0025, STR0025)
    assert str0025.institution_control_number == '31680151202509090425'
    assert str0025.debtor_institution_ispb == '31680151'
    assert str0025.debtor_branch == '0001'
    assert str0025.debtor_account_type == AccountType.CURRENT
    assert str0025.debtor_account_number == '12345678'
    assert str0025.creditor_name == 'John Doe'
    assert str0025.creditor_type == PersonType.INDIVIDUAL
    assert str0025.creditor_document == '69327934075'
    assert str0025.creditor_institution_ispb == '00038166'
    assert str0025.amount == Decimal('100.00')
    assert str0025.priority == Priority.MEDIUM
    assert str0025.deposit_identifier == '012345678901234567'
    assert str0025.scheduled_date == date(2025, 9, 9)
    assert str0025.scheduled_time == time(15, 30)
    assert str0025.settlement_date == date(2025, 9, 8)
    assert str0025.message_code == 'STR0025'


def test_str0025_missing_required_fields() -> None:
    with pytest.raises(ValidationError) as exc:
        STR0025.model_validate({})
    missing_fields = extract_missing_fields(exc.value)
    assert missing_fields == {
        'from_ispb',
        'amount',
        'creditor_name',
        'creditor_type',
        'deposit_identifier',
        'operation_number',
        'system_domain',
        'to_ispb',
        'creditor_document',
        'settlement_date',
        'creditor_institution_ispb',
        'debtor_institution_ispb',
        'institution_control_number',
    }


def test_str0025_business_rules_invalid_documents() -> None:
    params = make_valid_str0025_params()
    params['creditor_type'] = 'BUSINESS'
    params['creditor_document'] = '69327934075'

    with pytest.raises(ValidationError) as exc:
        STR0025.model_validate(params)
    error_message = str(exc.value)
    assert 'Invalid CNPJ for creditor_type BUSINESS' in error_message


def test_str0025_business_rules_missing_debtor_branch_for_debtor_account_type_is_not_payment() -> None:
    params = make_valid_str0025_params()
    params['debtor_account_type'] = 'CURRENT'
    del params['debtor_branch']

    with pytest.raises(ValidationError) as exc:
        STR0025.model_validate(params)
    error_message = str(exc.value)
    assert 'debtor_branch is required when debtor_account_type is not PAYMENT' in error_message


def test_str0025_business_rules_missing_debtor_payment_account_number_for_debtor_account_type_is_payment() -> None:
    params = make_valid_str0025_params()
    params['debtor_account_type'] = 'PAYMENT'

    with pytest.raises(ValidationError) as exc:
        STR0025.model_validate(params)
    error_message = str(exc.value)
    assert 'debtor_payment_account_number is required when debtor_account_type is PAYMENT' in error_message


def test_str0025_business_rules_missing_debtor_account_number_for_debtor_account_type_is_not_payment() -> None:
    params = make_valid_str0025_params()
    params['debtor_account_type'] = 'CURRENT'
    del params['debtor_account_number']

    with pytest.raises(ValidationError) as exc:
        STR0025.model_validate(params)
    error_message = str(exc.value)
    assert 'debtor_account_number is required when debtor_account_type is not PAYMENT' in error_message


def test_str0025_to_xml() -> None:
    params = make_valid_str0025_params()
    str0025 = STR0025.model_validate(params)
    xml = str0025.to_xml()

    expected_xml = """<?xml version="1.0"?>
    <DOC>
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>316801512509080000001</NUOp>
        </BCMSG>
        <SISMSG>
            <STR0025>
                <CodMsg>STR0025</CodMsg>
                <NumCtrlIF>31680151202509090425</NumCtrlIF>
                <ISPBIFDebtd>31680151</ISPBIFDebtd>
                <AgDebtd>0001</AgDebtd>
                <TpCtDebtd>CC</TpCtDebtd>
                <CtDebtd>12345678</CtDebtd>
                <NomCliCredtd>John Doe</NomCliCredtd>
                <TpPessoaCredtd>F</TpPessoaCredtd>
                <CNPJ_CPFCliCredtd>69327934075</CNPJ_CPFCliCredtd>
                <ISPBIFCredtd>00038166</ISPBIFCredtd>
                <VlrLanc>100.0</VlrLanc>
                <NivelPref>C</NivelPref>
                <IdentcDep>012345678901234567</IdentcDep>
                <DtAgendt>2025-09-09</DtAgendt>
                <HrAgendt>15:30:00</HrAgendt>
                <DtMovto>2025-09-08</DtMovto>
            </STR0025>
        </SISMSG>
    </DOC>
    """

    assert normalize_xml(expected_xml) == normalize_xml(xml)


def test_str0025_to_xml_omit_optional_fields() -> None:
    params = make_valid_str0025_params()
    del params['priority']
    del params['scheduled_date']
    del params['scheduled_time']

    str0025 = STR0025.model_validate(params)
    xml = str0025.to_xml()

    expected_xml = """<?xml version="1.0"?>
    <DOC>
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>316801512509080000001</NUOp>
        </BCMSG>
        <SISMSG>
            <STR0025>
                <CodMsg>STR0025</CodMsg>
                <NumCtrlIF>31680151202509090425</NumCtrlIF>
                <ISPBIFDebtd>31680151</ISPBIFDebtd>
                <AgDebtd>0001</AgDebtd>
                <TpCtDebtd>CC</TpCtDebtd>
                <CtDebtd>12345678</CtDebtd>
                <NomCliCredtd>John Doe</NomCliCredtd>
                <TpPessoaCredtd>F</TpPessoaCredtd>
                <CNPJ_CPFCliCredtd>69327934075</CNPJ_CPFCliCredtd>
                <ISPBIFCredtd>00038166</ISPBIFCredtd>
                <VlrLanc>100.0</VlrLanc>
                <IdentcDep>012345678901234567</IdentcDep>
                <DtMovto>2025-09-08</DtMovto>
            </STR0025>
        </SISMSG>
    </DOC>
    """

    assert normalize_xml(expected_xml) == normalize_xml(xml)


def test_str0025_from_xml() -> None:
    xml = """<?xml version="1.0"?>
    <DOC>
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>316801512509080000001</NUOp>
        </BCMSG>
        <SISMSG>
            <STR0025>
                <CodMsg>STR0025</CodMsg>
                <NumCtrlIF>31680151202509090425</NumCtrlIF>
                <ISPBIFDebtd>31680151</ISPBIFDebtd>
                <AgDebtd>0001</AgDebtd>
                <TpCtDebtd>CC</TpCtDebtd>
                <CtDebtd>12345678</CtDebtd>
                <NomCliCredtd>John Doe</NomCliCredtd>
                <TpPessoaCredtd>F</TpPessoaCredtd>
                <CNPJ_CPFCliCredtd>69327934075</CNPJ_CPFCliCredtd>
                <ISPBIFCredtd>00038166</ISPBIFCredtd>
                <VlrLanc>100.0</VlrLanc>
                <NivelPref>C</NivelPref>
                <IdentcDep>012345678901234567</IdentcDep>
                <DtAgendt>2025-09-09</DtAgendt>
                <HrAgendt>15:30:00</HrAgendt>
                <DtMovto>2025-09-08</DtMovto>
            </STR0025>
        </SISMSG>
    </DOC>
    """

    str0025 = STR0025.from_xml(xml)
    assert isinstance(str0025, STR0025)
    assert str0025.institution_control_number == '31680151202509090425'
    assert str0025.debtor_institution_ispb == '31680151'
    assert str0025.debtor_branch == '0001'
    assert str0025.debtor_account_type == AccountType.CURRENT
    assert str0025.debtor_account_number == '12345678'
    assert str0025.creditor_name == 'John Doe'
    assert str0025.creditor_type == PersonType.INDIVIDUAL
    assert str0025.creditor_document == '69327934075'
    assert str0025.creditor_institution_ispb == '00038166'
    assert str0025.amount == Decimal('100.0')
    assert str0025.priority == Priority.MEDIUM
    assert str0025.deposit_identifier == '012345678901234567'
    assert str0025.scheduled_date == date(2025, 9, 9)
    assert str0025.scheduled_time == time(15, 30)
    assert str0025.settlement_date == date(2025, 9, 8)
    assert str0025.message_code == 'STR0025'


def test_str0025_from_xml_omit_optional_fields() -> None:
    xml = """<?xml version="1.0"?>
    <DOC>
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>316801512509080000001</NUOp>
        </BCMSG>
        <SISMSG>
            <STR0025>
                <CodMsg>STR0025</CodMsg>
                <NumCtrlIF>31680151202509090425</NumCtrlIF>
                <ISPBIFDebtd>31680151</ISPBIFDebtd>
                <AgDebtd>0001</AgDebtd>
                <TpCtDebtd>CC</TpCtDebtd>
                <CtDebtd>12345678</CtDebtd>
                <NomCliCredtd>John Doe</NomCliCredtd>
                <TpPessoaCredtd>F</TpPessoaCredtd>
                <CNPJ_CPFCliCredtd>69327934075</CNPJ_CPFCliCredtd>
                <ISPBIFCredtd>00038166</ISPBIFCredtd>
                <VlrLanc>100.0</VlrLanc>
                <IdentcDep>012345678901234567</IdentcDep>
                <DtMovto>2025-09-08</DtMovto>
            </STR0025>
        </SISMSG>
    </DOC>
    """

    str0025 = STR0025.from_xml(xml)
    assert isinstance(str0025, STR0025)
    assert str0025.institution_control_number == '31680151202509090425'
    assert str0025.debtor_institution_ispb == '31680151'
    assert str0025.debtor_branch == '0001'
    assert str0025.debtor_account_type == AccountType.CURRENT
    assert str0025.debtor_account_number == '12345678'
    assert str0025.creditor_name == 'John Doe'
    assert str0025.creditor_type == PersonType.INDIVIDUAL
    assert str0025.creditor_document == '69327934075'
    assert str0025.creditor_institution_ispb == '00038166'
    assert str0025.amount == Decimal('100.0')
    assert str0025.priority is None
    assert str0025.deposit_identifier == '012345678901234567'
    assert str0025.scheduled_date is None
    assert str0025.scheduled_time is None
    assert str0025.settlement_date == date(2025, 9, 8)
    assert str0025.message_code == 'STR0025'


def test_str0025_roundtrip() -> None:
    params = make_valid_str0025_params()
    del params['priority']
    str0025 = STR0025.model_validate(params)
    xml = str0025.to_xml()
    str0025_from_xml = STR0025.from_xml(xml)
    assert str0025 == str0025_from_xml


def test_str0025_from_xml_missing_required_fields() -> None:
    xml = """<?xml version="1.0"?>
    <DOC>
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>316801512509080000001</NUOp>
        </BCMSG>
        <SISMSG>
            <STR0025>
                <CodMsg>STR0025</CodMsg>
            </STR0025>
        </SISMSG>
    </DOC>
    """

    with pytest.raises(ValidationError) as exc:
        STR0025.from_xml(xml)
    missing_fields = extract_missing_fields(exc.value)
    assert missing_fields == {
        'amount',
        'creditor_name',
        'creditor_type',
        'deposit_identifier',
        'institution_control_number',
        'debtor_institution_ispb',
        'creditor_document',
        'creditor_institution_ispb',
        'settlement_date',
    }
