from datetime import date, datetime, time
from decimal import Decimal
from typing import Any

import pytest
from pydantic import ValidationError

from sfn_messages.core.types import AccountType, PersonType, Priority, StrSettlementStatus
from sfn_messages.str.str0025 import STR0025, STR0025E, STR0025R1, STR0025R2
from tests.conftest import extract_missing_fields, normalize_xml


def make_valid_str0025_params() -> dict[str, Any]:
    return {
        'from_ispb': '31680151',
        'operation_number': '31680151250908000000001',
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


def make_valid_str0025r1_params() -> dict[str, Any]:
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


def make_valid_str0025r2_params() -> dict[str, Any]:
    return {
        'from_ispb': '31680151',
        'operation_number': '31680151250908000000001',
        'system_domain': 'SPB01',
        'to_ispb': '00038166',
        'debtor_institution_ispb': '31680151',
        'debtor_branch': '0001',
        'debtor_account_type': 'CURRENT',
        'debtor_account_number': '12345678',
        'creditor_name': 'John Doe',
        'creditor_type': 'INDIVIDUAL',
        'creditor_document': '69327934075',
        'creditor_institution_ispb': '00038166',
        'amount': 100.00,
        'deposit_identifier': '012345678901234567',
        'settlement_date': '2025-09-08',
        'vendor_timestamp': '2025-11-20T15:30:00',
        'str_control_number': 'STR20250101000000001',
    }


def make_valid_str0025e_params(*, general_error: bool = False) -> dict[str, Any]:
    str0025e = {
        'from_ispb': '31680151',
        'operation_number': '31680151250908000000001',
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

    if general_error:
        str0025e['general_error_code'] = 'EGEN0050'
    else:
        str0025e['debtor_institution_ispb_error_code'] = 'EGEN0051'

    return str0025e


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


def test_str0025e_general_error_valid_model() -> None:
    params = make_valid_str0025e_params(general_error=True)
    str0025e = STR0025E.model_validate(params)
    assert isinstance(str0025e, STR0025E)
    assert str0025e.institution_control_number == '31680151202509090425'
    assert str0025e.debtor_institution_ispb == '31680151'
    assert str0025e.debtor_branch == '0001'
    assert str0025e.debtor_account_type == AccountType.CURRENT
    assert str0025e.debtor_account_number == '12345678'
    assert str0025e.creditor_name == 'John Doe'
    assert str0025e.creditor_type == PersonType.INDIVIDUAL
    assert str0025e.creditor_document == '69327934075'
    assert str0025e.creditor_institution_ispb == '00038166'
    assert str0025e.amount == Decimal('100.00')
    assert str0025e.priority == Priority.MEDIUM
    assert str0025e.deposit_identifier == '012345678901234567'
    assert str0025e.scheduled_date == date(2025, 9, 9)
    assert str0025e.scheduled_time == time(15, 30)
    assert str0025e.settlement_date == date(2025, 9, 8)
    assert str0025e.message_code == 'STR0025E'
    assert str0025e.general_error_code == 'EGEN0050'


def test_str0025e_tag_error_valid_model() -> None:
    params = make_valid_str0025e_params()
    str0025e = STR0025E.model_validate(params)
    assert isinstance(str0025e, STR0025E)
    assert str0025e.institution_control_number == '31680151202509090425'
    assert str0025e.debtor_institution_ispb == '31680151'
    assert str0025e.debtor_branch == '0001'
    assert str0025e.debtor_account_type == AccountType.CURRENT
    assert str0025e.debtor_account_number == '12345678'
    assert str0025e.creditor_name == 'John Doe'
    assert str0025e.creditor_type == PersonType.INDIVIDUAL
    assert str0025e.creditor_document == '69327934075'
    assert str0025e.creditor_institution_ispb == '00038166'
    assert str0025e.amount == Decimal('100.00')
    assert str0025e.priority == Priority.MEDIUM
    assert str0025e.deposit_identifier == '012345678901234567'
    assert str0025e.scheduled_date == date(2025, 9, 9)
    assert str0025e.scheduled_time == time(15, 30)
    assert str0025e.settlement_date == date(2025, 9, 8)
    assert str0025e.message_code == 'STR0025E'
    assert str0025e.debtor_institution_ispb_error_code == 'EGEN0051'


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
    <DOC xmlns="http://www.bcb.gov.br/SPB/STR0025.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>31680151250908000000001</NUOp>
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


def test_str0025e_general_error_to_xml() -> None:
    params = make_valid_str0025e_params(general_error=True)
    str0025e = STR0025E.model_validate(params)
    xml = str0025e.to_xml()

    expected_xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/SPB/STR0025E.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>31680151250908000000001</NUOp>
        </BCMSG>
        <SISMSG>
            <STR0025 CodErro="EGEN0050">
                <CodMsg>STR0025E</CodMsg>
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


def test_str0025e_tag_error_to_xml() -> None:
    params = make_valid_str0025e_params()
    str0025e = STR0025E.model_validate(params)
    xml = str0025e.to_xml()

    expected_xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/SPB/STR0025E.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>31680151250908000000001</NUOp>
        </BCMSG>
        <SISMSG>
            <STR0025>
                <CodMsg>STR0025E</CodMsg>
                <NumCtrlIF>31680151202509090425</NumCtrlIF>
                <ISPBIFDebtd CodErro="EGEN0051">31680151</ISPBIFDebtd>
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
    <DOC xmlns="http://www.bcb.gov.br/SPB/STR0025.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>31680151250908000000001</NUOp>
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
    <DOC xmlns="http://www.bcb.gov.br/SPB/STR0025.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>31680151250908000000001</NUOp>
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


def test_str0025e_general_error_from_xml() -> None:
    xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/SPB/STR0025E.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>31680151250908000000001</NUOp>
        </BCMSG>
        <SISMSG>
            <STR0025 CodErro="EGEN0050">
                <CodMsg>STR0025E</CodMsg>
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

    str0025e = STR0025E.from_xml(xml)
    assert isinstance(str0025e, STR0025E)
    assert str0025e.institution_control_number == '31680151202509090425'
    assert str0025e.debtor_institution_ispb == '31680151'
    assert str0025e.debtor_branch == '0001'
    assert str0025e.debtor_account_type == AccountType.CURRENT
    assert str0025e.debtor_account_number == '12345678'
    assert str0025e.creditor_name == 'John Doe'
    assert str0025e.creditor_type == PersonType.INDIVIDUAL
    assert str0025e.creditor_document == '69327934075'
    assert str0025e.creditor_institution_ispb == '00038166'
    assert str0025e.amount == Decimal('100.0')
    assert str0025e.priority == Priority.MEDIUM
    assert str0025e.deposit_identifier == '012345678901234567'
    assert str0025e.scheduled_date == date(2025, 9, 9)
    assert str0025e.scheduled_time == time(15, 30)
    assert str0025e.settlement_date == date(2025, 9, 8)
    assert str0025e.message_code == 'STR0025E'
    assert str0025e.general_error_code == 'EGEN0050'


def test_str0025e_tag_error_from_xml() -> None:
    xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/SPB/STR0025E.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>31680151250908000000001</NUOp>
        </BCMSG>
        <SISMSG>
            <STR0025>
                <CodMsg>STR0025E</CodMsg>
                <NumCtrlIF>31680151202509090425</NumCtrlIF>
                <ISPBIFDebtd CodErro="EGEN0051">31680151</ISPBIFDebtd>
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

    str0025e = STR0025E.from_xml(xml)
    assert isinstance(str0025e, STR0025E)
    assert str0025e.institution_control_number == '31680151202509090425'
    assert str0025e.debtor_institution_ispb == '31680151'
    assert str0025e.debtor_branch == '0001'
    assert str0025e.debtor_account_type == AccountType.CURRENT
    assert str0025e.debtor_account_number == '12345678'
    assert str0025e.creditor_name == 'John Doe'
    assert str0025e.creditor_type == PersonType.INDIVIDUAL
    assert str0025e.creditor_document == '69327934075'
    assert str0025e.creditor_institution_ispb == '00038166'
    assert str0025e.amount == Decimal('100.0')
    assert str0025e.priority == Priority.MEDIUM
    assert str0025e.deposit_identifier == '012345678901234567'
    assert str0025e.scheduled_date == date(2025, 9, 9)
    assert str0025e.scheduled_time == time(15, 30)
    assert str0025e.settlement_date == date(2025, 9, 8)
    assert str0025e.message_code == 'STR0025E'
    assert str0025e.debtor_institution_ispb_error_code == 'EGEN0051'


def test_str0025_from_xml_omit_optional_fields() -> None:
    xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/SPB/STR0025.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>31680151250908000000001</NUOp>
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
    str0025 = STR0025.model_validate(params)
    xml = str0025.to_xml()
    str0025_from_xml = STR0025.from_xml(xml)
    assert str0025 == str0025_from_xml


def test_str0025_from_xml_missing_required_fields() -> None:
    xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/SPB/STR0025.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>31680151250908000000001</NUOp>
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


def test_str0025r1_valid_model() -> None:
    params = make_valid_str0025r1_params()
    str0025r1 = STR0025R1.model_validate(params)
    assert isinstance(str0025r1, STR0025R1)
    assert str0025r1.debtor_institution_ispb == '31680151'
    assert str0025r1.from_ispb == '31680151'
    assert str0025r1.institution_control_number == '31680151202509090425'
    assert str0025r1.message_code == 'STR0025R1'
    assert str0025r1.operation_number == '31680151250908000000001'
    assert str0025r1.settlement_date == date(2025, 9, 8)
    assert str0025r1.settlement_timestamp == datetime(2025, 11, 20, 15, 30)
    assert str0025r1.str_control_number == 'STR20250101000000001'
    assert str0025r1.str_settlement_status == StrSettlementStatus.EFFECTIVE
    assert str0025r1.to_ispb == '00038166'
    assert str0025r1.system_domain == 'SPB01'


def test_str0025r1_missing_required_fields() -> None:
    with pytest.raises(ValidationError) as exc:
        STR0025R1.model_validate({})
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


def test_str0025r1_to_xml() -> None:
    params = make_valid_str0025r1_params()
    str0025r1 = STR0025R1.model_validate(params)
    xml = str0025r1.to_xml()

    expected_xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/SPB/STR0025.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>31680151250908000000001</NUOp>
        </BCMSG>
        <SISMSG>
            <STR0025R1>
                <CodMsg>STR0025R1</CodMsg>
                <NumCtrlIF>31680151202509090425</NumCtrlIF>
                <ISPBIFDebtd>31680151</ISPBIFDebtd>
                <NumCtrlSTR>STR20250101000000001</NumCtrlSTR>
                <SitLancSTR>1</SitLancSTR>
                <DtHrSit>2025-11-20T15:30:00</DtHrSit>
                <DtMovto>2025-09-08</DtMovto>
            </STR0025R1>
        </SISMSG>
    </DOC>
    """

    assert normalize_xml(expected_xml) == normalize_xml(xml)


def test_str0025r1_from_xml() -> None:
    xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/SPB/STR0025.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>31680151250908000000001</NUOp>
        </BCMSG>
        <SISMSG>
            <STR0025R1>
                <CodMsg>STR0025R1</CodMsg>
                <NumCtrlIF>31680151202509090425</NumCtrlIF>
                <ISPBIFDebtd>31680151</ISPBIFDebtd>
                <NumCtrlSTR>STR20250101000000001</NumCtrlSTR>
                <SitLancSTR>1</SitLancSTR>
                <DtHrSit>2025-11-20T15:30:00</DtHrSit>
                <DtMovto>2025-09-08</DtMovto>
            </STR0025R1>
        </SISMSG>
    </DOC>
    """
    str0025r1 = STR0025R1.from_xml(xml)
    assert isinstance(str0025r1, STR0025R1)
    assert str0025r1.debtor_institution_ispb == '31680151'
    assert str0025r1.from_ispb == '31680151'
    assert str0025r1.institution_control_number == '31680151202509090425'
    assert str0025r1.message_code == 'STR0025R1'
    assert str0025r1.operation_number == '31680151250908000000001'
    assert str0025r1.settlement_date == date(2025, 9, 8)
    assert str0025r1.settlement_timestamp == datetime(2025, 11, 20, 15, 30)
    assert str0025r1.str_control_number == 'STR20250101000000001'
    assert str0025r1.str_settlement_status == StrSettlementStatus.EFFECTIVE
    assert str0025r1.to_ispb == '00038166'
    assert str0025r1.system_domain == 'SPB01'


def test_str0025r1_roundtrip() -> None:
    params = make_valid_str0025r1_params()
    str0025r1 = STR0025R1.model_validate(params)
    xml = str0025r1.to_xml()
    str0025r1_from_xml = STR0025R1.from_xml(xml)
    assert str0025r1 == str0025r1_from_xml


def test_str0025r1_from_xml_missing_required_fields() -> None:
    xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/SPB/STR0025.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>31680151250908000000001</NUOp>
        </BCMSG>
        <SISMSG>
            <STR0025R1>
                <CodMsg>STR0025R1</CodMsg>
            </STR0025R1>
        </SISMSG>
    </DOC>
    """

    with pytest.raises(ValidationError) as exc:
        STR0025R1.from_xml(xml)
    missing_fields = extract_missing_fields(exc.value)
    assert missing_fields == {
        'settlement_date',
        'debtor_institution_ispb',
        'str_settlement_status',
        'str_control_number',
        'institution_control_number',
        'settlement_timestamp',
    }


def test_str0025r2_valid_model() -> None:
    params = make_valid_str0025r2_params()
    str0025r2 = STR0025R2.model_validate(params)
    assert isinstance(str0025r2, STR0025R2)
    assert str0025r2.debtor_institution_ispb == '31680151'
    assert str0025r2.debtor_branch == '0001'
    assert str0025r2.debtor_account_type == AccountType.CURRENT
    assert str0025r2.debtor_account_number == '12345678'
    assert str0025r2.creditor_name == 'John Doe'
    assert str0025r2.creditor_type == PersonType.INDIVIDUAL
    assert str0025r2.creditor_document == '69327934075'
    assert str0025r2.creditor_institution_ispb == '00038166'
    assert str0025r2.amount == Decimal('100.00')
    assert str0025r2.deposit_identifier == '012345678901234567'
    assert str0025r2.settlement_date == date(2025, 9, 8)
    assert str0025r2.message_code == 'STR0025R2'
    assert str0025r2.from_ispb == '31680151'
    assert str0025r2.operation_number == '31680151250908000000001'
    assert str0025r2.system_domain == 'SPB01'
    assert str0025r2.to_ispb == '00038166'
    assert str0025r2.vendor_timestamp == datetime(2025, 11, 20, 15, 30)
    assert str0025r2.str_control_number == 'STR20250101000000001'


def test_str0025r2_missing_required_fields() -> None:
    with pytest.raises(ValidationError) as exc:
        STR0025R2.model_validate({})
    missing_fields = extract_missing_fields(exc.value)
    assert missing_fields == {
        'settlement_date',
        'vendor_timestamp',
        'amount',
        'deposit_identifier',
        'creditor_institution_ispb',
        'str_control_number',
        'to_ispb',
        'from_ispb',
        'operation_number',
        'creditor_type',
        'system_domain',
        'creditor_document',
        'debtor_institution_ispb',
        'creditor_name',
    }


def test_str0025r2_business_rules_invalid_documents() -> None:
    params = make_valid_str0025r2_params()
    params['creditor_type'] = 'BUSINESS'
    params['creditor_document'] = '69327934075'

    with pytest.raises(ValidationError) as exc:
        STR0025R2.model_validate(params)
    error_message = str(exc.value)
    assert 'Invalid CNPJ for creditor_type BUSINESS' in error_message


def test_str0025r2_business_rules_missing_debtor_branch_for_debtor_account_type_is_not_payment() -> None:
    params = make_valid_str0025r2_params()
    params['debtor_account_type'] = 'CURRENT'
    del params['debtor_branch']

    with pytest.raises(ValidationError) as exc:
        STR0025R2.model_validate(params)
    error_message = str(exc.value)
    assert 'debtor_branch is required when debtor_account_type is not PAYMENT' in error_message


def test_str0025r2_business_rules_missing_debtor_payment_account_number_for_debtor_account_type_is_payment() -> None:
    params = make_valid_str0025r2_params()
    params['debtor_account_type'] = 'PAYMENT'

    with pytest.raises(ValidationError) as exc:
        STR0025R2.model_validate(params)
    error_message = str(exc.value)
    assert 'debtor_payment_account_number is required when debtor_account_type is PAYMENT' in error_message


def test_str0025r2_business_rules_missing_debtor_account_number_for_debtor_account_type_is_not_payment() -> None:
    params = make_valid_str0025r2_params()
    params['debtor_account_type'] = 'CURRENT'
    del params['debtor_account_number']

    with pytest.raises(ValidationError) as exc:
        STR0025R2.model_validate(params)
    error_message = str(exc.value)
    assert 'debtor_account_number is required when debtor_account_type is not PAYMENT' in error_message


def test_str0025r2_to_xml() -> None:
    params = make_valid_str0025r2_params()
    str0025r2 = STR0025R2.model_validate(params)
    xml = str0025r2.to_xml()

    expected_xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/SPB/STR0025.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>31680151250908000000001</NUOp>
        </BCMSG>
        <SISMSG>
            <STR0025R2>
                <CodMsg>STR0025R2</CodMsg>
                <NumCtrlSTR>STR20250101000000001</NumCtrlSTR>
                <DtHrBC>2025-11-20T15:30:00</DtHrBC>
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
            </STR0025R2>
        </SISMSG>
    </DOC>
    """

    assert normalize_xml(expected_xml) == normalize_xml(xml)


def test_str0025r2_from_xml() -> None:
    xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/SPB/STR0025.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>31680151250908000000001</NUOp>
        </BCMSG>
        <SISMSG>
            <STR0025R2>
                <CodMsg>STR0025R2</CodMsg>
                <NumCtrlSTR>STR20250101000000001</NumCtrlSTR>
                <DtHrBC>2025-11-20T15:30:00</DtHrBC>
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
            </STR0025R2>
        </SISMSG>
    </DOC>
    """

    str0025r2 = STR0025R2.from_xml(xml)
    assert isinstance(str0025r2, STR0025R2)
    assert str0025r2.debtor_institution_ispb == '31680151'
    assert str0025r2.debtor_branch == '0001'
    assert str0025r2.debtor_account_type == AccountType.CURRENT
    assert str0025r2.debtor_account_number == '12345678'
    assert str0025r2.creditor_name == 'John Doe'
    assert str0025r2.creditor_type == PersonType.INDIVIDUAL
    assert str0025r2.creditor_document == '69327934075'
    assert str0025r2.creditor_institution_ispb == '00038166'
    assert str0025r2.amount == Decimal('100.0')
    assert str0025r2.deposit_identifier == '012345678901234567'
    assert str0025r2.settlement_date == date(2025, 9, 8)
    assert str0025r2.message_code == 'STR0025R2'
    assert str0025r2.from_ispb == '31680151'
    assert str0025r2.operation_number == '31680151250908000000001'
    assert str0025r2.system_domain == 'SPB01'
    assert str0025r2.to_ispb == '00038166'
    assert str0025r2.vendor_timestamp == datetime(2025, 11, 20, 15, 30)
    assert str0025r2.str_control_number == 'STR20250101000000001'


def test_str0025r2_roundtrip() -> None:
    params = make_valid_str0025r2_params()
    str0025r2 = STR0025R2.model_validate(params)
    xml = str0025r2.to_xml()
    str0025r2_from_xml = STR0025R2.from_xml(xml)
    assert str0025r2 == str0025r2_from_xml


def test_str0025r2_from_xml_missing_required_fields() -> None:
    xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/SPB/STR0025.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>31680151250908000000001</NUOp>
        </BCMSG>
        <SISMSG>
            <STR0025R2>
                <CodMsg>STR0025R2</CodMsg>
            </STR0025R2>
        </SISMSG>
    </DOC>
    """

    with pytest.raises(ValidationError) as exc:
        STR0025R2.from_xml(xml)
    missing_fields = extract_missing_fields(exc.value)
    assert missing_fields == {
        'creditor_type',
        'settlement_date',
        'debtor_institution_ispb',
        'vendor_timestamp',
        'amount',
        'str_control_number',
        'creditor_name',
        'creditor_document',
        'deposit_identifier',
        'creditor_institution_ispb',
    }
