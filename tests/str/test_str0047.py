from datetime import date, datetime, time
from decimal import Decimal
from typing import Any

import pytest
from pydantic import ValidationError

from sfn_messages.core.types import Priority, StrSettlementStatus
from sfn_messages.str.str0047 import (
    STR0047,
    STR0047E,
    STR0047R1,
    STR0047R2,
    STR0047R3,
    FinancialAgentCreditorGroup,
    FinancialAgentCreditorGroupError,
    FinancialAgentCreditorR2Group,
    FinancialAgentCreditorR3Group,
    FinancialAgentDebitedGroup,
    FinancialAgentDebitedGroupError,
    FinancialAgentDebitedR2Group,
    FinancialAgentDebitedR3Group,
)
from tests.conftest import extract_missing_fields, normalize_xml


def make_valid_str0047_params() -> dict[str, Any]:
    return {
        'from_ispb': '31680151',
        'operation_number': '31680151250908000000001',
        'system_domain': 'SPB01',
        'to_ispb': '00038166',
        'message_code': 'STR0047',
        'institution_control_number': '31680151202509090425',
        'debtor_institution_ispb': '31680151',
        'debtor_branch': '0002',
        'financial_debit_group': {
            'debtor_account_number': '9876543',
            'debtor_document': '53480615000129',
            'debtor_name': 'Tiago Noah Julio Alves',
        },
        'creditor_institution_ispb': '00038166',
        'creditor_branch': '0001',
        'financial_credit_group': {
            'creditor_account_number': '123456',
            'creditor_document': '34161858000150',
            'creditor_name': 'Olivia Sandra Rosângela Gomes',
        },
        'amount': 125765.00,
        'portability_number': 'K7J2N9P1L0B5V4X3M8Z9A',
        'provider_ispb': '31680151',
        'description': 'Payment for services',
        'priority': 'MEDIUM',
        'scheduled_date': '2026-01-28',
        'scheduled_time': '17:30:00',
        'settlement_date': '2026-01-28',
    }


def make_valid_str0047r1_params() -> dict[str, Any]:
    return {
        'from_ispb': '31680151',
        'operation_number': '31680151250908000000001',
        'system_domain': 'SPB01',
        'to_ispb': '00038166',
        'message_code': 'STR0047R1',
        'institution_control_number': '31680151202509090425',
        'debtor_institution_ispb': '31680151',
        'str_control_number': 'STR20250101000000001',
        'str_settlement_status': 'EFFECTIVE',
        'settlement_timestamp': '2026-01-28T17:30:00',
        'settlement_date': '2026-01-28',
    }


def make_valid_str0047r2_params() -> dict[str, Any]:
    return {
        'from_ispb': '31680151',
        'operation_number': '31680151250908000000001',
        'system_domain': 'SPB01',
        'to_ispb': '00038166',
        'message_code': 'STR0047R2',
        'str_control_number': 'STR20250101000000001',
        'vendor_timestamp': '2026-01-28T17:26:50',
        'debtor_institution_ispb': '31680151',
        'debtor_branch': '0002',
        'financial_debit_group': {
            'debtor_account_number': '9876543',
            'debtor_document': '53480615000129',
            'debtor_name': 'Tiago Noah Julio Alves',
        },
        'creditor_institution_ispb': '00038166',
        'creditor_branch': '0001',
        'financial_credit_group': {
            'creditor_account_number': '123456',
            'creditor_document': '34161858000150',
            'creditor_name': 'Olivia Sandra Rosângela Gomes',
        },
        'amount': 125765.00,
        'portability_number': 'K7J2N9P1L0B5V4X3M8Z9A',
        'provider_ispb': '31680151',
        'description': 'Payment for services',
        'settlement_date': '2026-01-28',
    }


def make_valid_str0047r3_params() -> dict[str, Any]:
    return {
        'from_ispb': '31680151',
        'operation_number': '31680151250908000000001',
        'system_domain': 'SPB01',
        'to_ispb': '00038166',
        'message_code': 'STR0047R3',
        'str_control_number': 'STR20250101000000001',
        'vendor_timestamp': '2026-01-28T17:26:50',
        'debtor_institution_ispb': '31680151',
        'debtor_branch': '0002',
        'financial_debit_group': {
            'debtor_account_number': '9876543',
            'debtor_document': '53480615000129',
            'debtor_name': 'Tiago Noah Julio Alves',
        },
        'creditor_institution_ispb': '00038166',
        'creditor_branch': '0001',
        'financial_credit_group': {
            'creditor_account_number': '123456',
            'creditor_document': '34161858000150',
            'creditor_name': 'Olivia Sandra Rosângela Gomes',
        },
        'amount': 125765.00,
        'portability_number': 'K7J2N9P1L0B5V4X3M8Z9A',
        'provider_ispb': '31680151',
        'description': 'Payment for services',
        'settlement_date': '2026-01-28',
    }


def make_valid_str0047e_params(*, general_error: bool = False) -> dict[str, Any]:
    str0047e = {
        'from_ispb': '31680151',
        'operation_number': '31680151250908000000001',
        'system_domain': 'SPB01',
        'to_ispb': '00038166',
        'message_code': 'STR0047E',
        'institution_control_number': '31680151202509090425',
        'debtor_institution_ispb': '31680151',
        'debtor_branch': '0002',
        'financial_debit_group': {
            'debtor_account_number': '9876543',
            'debtor_document': '53480615000129',
            'debtor_name': 'Tiago Noah Julio Alves',
        },
        'creditor_institution_ispb': '00038166',
        'creditor_branch': '0001',
        'financial_credit_group': {
            'creditor_account_number': '123456',
            'creditor_document': '34161858000150',
            'creditor_name': 'Olivia Sandra Rosângela Gomes',
        },
        'amount': 125765.00,
        'portability_number': 'K7J2N9P1L0B5V4X3M8Z9A',
        'provider_ispb': '31680151',
        'description': 'Payment for services',
        'priority': 'MEDIUM',
        'scheduled_date': '2026-01-28',
        'scheduled_time': '17:30:00',
        'settlement_date': '2026-01-28',
    }

    if general_error:
        str0047e['general_error_code'] = 'EGEN0050'
    else:
        str0047e['creditor_branch_error_code'] = 'ESPE0051'

    return str0047e


def test_str0047_valid_params() -> None:
    params = make_valid_str0047_params()
    str0047 = STR0047.model_validate(params)

    assert isinstance(str0047, STR0047)
    assert str0047.from_ispb == '31680151'
    assert str0047.operation_number == '31680151250908000000001'
    assert str0047.system_domain == 'SPB01'
    assert str0047.to_ispb == '00038166'
    assert str0047.message_code == 'STR0047'
    assert str0047.institution_control_number == '31680151202509090425'
    assert str0047.debtor_institution_ispb == '31680151'
    assert str0047.debtor_branch == '0002'
    assert str0047.creditor_institution_ispb == '00038166'
    assert str0047.creditor_branch == '0001'
    assert str0047.amount == Decimal('125765.00')
    assert str0047.portability_number == 'K7J2N9P1L0B5V4X3M8Z9A'
    assert str0047.provider_ispb == '31680151'
    assert str0047.description == 'Payment for services'
    assert str0047.priority == Priority.MEDIUM
    assert str0047.scheduled_date == date(2026, 1, 28)
    assert str0047.scheduled_time == time(17, 30)
    assert str0047.settlement_date == date(2026, 1, 28)

    debit = str0047.financial_debit_group
    assert isinstance(debit, FinancialAgentDebitedGroup)
    assert debit.debtor_account_number == '9876543'
    assert debit.debtor_document == '53480615000129'
    assert debit.debtor_name == 'Tiago Noah Julio Alves'

    credit = str0047.financial_credit_group
    assert isinstance(credit, FinancialAgentCreditorGroup)
    assert credit.creditor_account_number == '123456'
    assert credit.creditor_document == '34161858000150'
    assert credit.creditor_name == 'Olivia Sandra Rosângela Gomes'


def test_str0047r1_valid_params() -> None:
    params = make_valid_str0047r1_params()
    str0047r1 = STR0047R1.model_validate(params)

    assert isinstance(str0047r1, STR0047R1)
    assert str0047r1.institution_control_number == '31680151202509090425'
    assert str0047r1.message_code == 'STR0047R1'
    assert str0047r1.debtor_institution_ispb == '31680151'
    assert str0047r1.str_control_number == 'STR20250101000000001'
    assert str0047r1.str_settlement_status == StrSettlementStatus.EFFECTIVE
    assert str0047r1.settlement_timestamp == datetime(2026, 1, 28, 17, 30)
    assert str0047r1.settlement_date == date(2026, 1, 28)


def test_str0047r2_valid_params() -> None:
    params = make_valid_str0047r2_params()
    str0047r2 = STR0047R2.model_validate(params)

    assert isinstance(str0047r2, STR0047R2)
    assert str0047r2.message_code == 'STR0047R2'
    assert str0047r2.str_control_number == 'STR20250101000000001'
    assert str0047r2.vendor_timestamp == datetime(2026, 1, 28, 17, 26, 50)
    assert str0047r2.debtor_institution_ispb == '31680151'
    assert str0047r2.debtor_branch == '0002'
    assert str0047r2.creditor_institution_ispb == '00038166'
    assert str0047r2.creditor_branch == '0001'
    assert str0047r2.amount == Decimal('125765.00')
    assert str0047r2.portability_number == 'K7J2N9P1L0B5V4X3M8Z9A'
    assert str0047r2.provider_ispb == '31680151'
    assert str0047r2.description == 'Payment for services'
    assert str0047r2.settlement_date == date(2026, 1, 28)

    debit = str0047r2.financial_debit_group
    assert isinstance(debit, FinancialAgentDebitedR2Group)
    assert debit.debtor_account_number == '9876543'
    assert debit.debtor_document == '53480615000129'
    assert debit.debtor_name == 'Tiago Noah Julio Alves'

    credit = str0047r2.financial_credit_group
    assert isinstance(credit, FinancialAgentCreditorR2Group)
    assert credit.creditor_account_number == '123456'
    assert credit.creditor_document == '34161858000150'
    assert credit.creditor_name == 'Olivia Sandra Rosângela Gomes'


def test_str0047r3_valid_params() -> None:
    params = make_valid_str0047r3_params()
    str0047r3 = STR0047R3.model_validate(params)

    assert isinstance(str0047r3, STR0047R3)
    assert str0047r3.message_code == 'STR0047R3'
    assert str0047r3.str_control_number == 'STR20250101000000001'
    assert str0047r3.vendor_timestamp == datetime(2026, 1, 28, 17, 26, 50)
    assert str0047r3.debtor_institution_ispb == '31680151'
    assert str0047r3.debtor_branch == '0002'
    assert str0047r3.creditor_institution_ispb == '00038166'
    assert str0047r3.creditor_branch == '0001'
    assert str0047r3.amount == Decimal('125765.00')
    assert str0047r3.portability_number == 'K7J2N9P1L0B5V4X3M8Z9A'
    assert str0047r3.provider_ispb == '31680151'
    assert str0047r3.description == 'Payment for services'
    assert str0047r3.settlement_date == date(2026, 1, 28)

    debit = str0047r3.financial_debit_group
    assert isinstance(debit, FinancialAgentDebitedR3Group)
    assert debit.debtor_account_number == '9876543'
    assert debit.debtor_document == '53480615000129'
    assert debit.debtor_name == 'Tiago Noah Julio Alves'

    credit = str0047r3.financial_credit_group
    assert isinstance(credit, FinancialAgentCreditorR3Group)
    assert credit.creditor_account_number == '123456'
    assert credit.creditor_document == '34161858000150'
    assert credit.creditor_name == 'Olivia Sandra Rosângela Gomes'


def test_str0047e_general_error_valid_params() -> None:
    params = make_valid_str0047e_params(general_error=True)
    str0047e = STR0047E.model_validate(params)

    assert isinstance(str0047e, STR0047E)
    assert str0047e.from_ispb == '31680151'
    assert str0047e.operation_number == '31680151250908000000001'
    assert str0047e.system_domain == 'SPB01'
    assert str0047e.to_ispb == '00038166'
    assert str0047e.message_code == 'STR0047E'
    assert str0047e.institution_control_number == '31680151202509090425'
    assert str0047e.debtor_institution_ispb == '31680151'
    assert str0047e.debtor_branch == '0002'
    assert str0047e.creditor_institution_ispb == '00038166'
    assert str0047e.creditor_branch == '0001'
    assert str0047e.amount == Decimal('125765.00')
    assert str0047e.portability_number == 'K7J2N9P1L0B5V4X3M8Z9A'
    assert str0047e.provider_ispb == '31680151'
    assert str0047e.description == 'Payment for services'
    assert str0047e.priority == Priority.MEDIUM
    assert str0047e.scheduled_date == date(2026, 1, 28)
    assert str0047e.scheduled_time == time(17, 30)
    assert str0047e.settlement_date == date(2026, 1, 28)
    assert str0047e.general_error_code == 'EGEN0050'

    debit = str0047e.financial_debit_group
    assert isinstance(debit, FinancialAgentDebitedGroupError)
    assert debit.debtor_account_number == '9876543'
    assert debit.debtor_document == '53480615000129'
    assert debit.debtor_name == 'Tiago Noah Julio Alves'

    credit = str0047e.financial_credit_group
    assert isinstance(credit, FinancialAgentCreditorGroupError)
    assert credit.creditor_account_number == '123456'
    assert credit.creditor_document == '34161858000150'
    assert credit.creditor_name == 'Olivia Sandra Rosângela Gomes'


def test_str0047e_tag_error_valid_params() -> None:
    params = make_valid_str0047e_params()
    str0047e = STR0047E.model_validate(params)

    assert isinstance(str0047e, STR0047E)
    assert str0047e.from_ispb == '31680151'
    assert str0047e.operation_number == '31680151250908000000001'
    assert str0047e.system_domain == 'SPB01'
    assert str0047e.to_ispb == '00038166'
    assert str0047e.message_code == 'STR0047E'
    assert str0047e.institution_control_number == '31680151202509090425'
    assert str0047e.debtor_institution_ispb == '31680151'
    assert str0047e.debtor_branch == '0002'
    assert str0047e.creditor_institution_ispb == '00038166'
    assert str0047e.creditor_branch == '0001'
    assert str0047e.amount == Decimal('125765.00')
    assert str0047e.portability_number == 'K7J2N9P1L0B5V4X3M8Z9A'
    assert str0047e.provider_ispb == '31680151'
    assert str0047e.description == 'Payment for services'
    assert str0047e.priority == Priority.MEDIUM
    assert str0047e.scheduled_date == date(2026, 1, 28)
    assert str0047e.scheduled_time == time(17, 30)
    assert str0047e.settlement_date == date(2026, 1, 28)
    assert str0047e.creditor_branch_error_code == 'ESPE0051'

    debit = str0047e.financial_debit_group
    assert isinstance(debit, FinancialAgentDebitedGroupError)
    assert debit.debtor_account_number == '9876543'
    assert debit.debtor_document == '53480615000129'
    assert debit.debtor_name == 'Tiago Noah Julio Alves'

    credit = str0047e.financial_credit_group
    assert isinstance(credit, FinancialAgentCreditorGroupError)
    assert credit.creditor_account_number == '123456'
    assert credit.creditor_document == '34161858000150'
    assert credit.creditor_name == 'Olivia Sandra Rosângela Gomes'


def test_str0047_missing_required_fields() -> None:
    with pytest.raises(ValidationError) as exc:
        STR0047.model_validate({})

    missing_fields = extract_missing_fields(exc.value)
    assert missing_fields == {
        'from_ispb',
        'system_domain',
        'institution_control_number',
        'debtor_institution_ispb',
        'creditor_institution_ispb',
        'creditor_branch',
        'amount',
        'portability_number',
        'provider_ispb',
        'settlement_date',
        'to_ispb',
        'operation_number',
    }


def test_str0047r1_missing_required_fields() -> None:
    with pytest.raises(ValidationError) as exc:
        STR0047R1.model_validate({})

    missing_fields = extract_missing_fields(exc.value)
    assert missing_fields == {
        'from_ispb',
        'system_domain',
        'institution_control_number',
        'debtor_institution_ispb',
        'str_control_number',
        'str_settlement_status',
        'settlement_timestamp',
        'settlement_date',
        'to_ispb',
        'operation_number',
    }


def test_str0047r2_missing_required_fields() -> None:
    with pytest.raises(ValidationError) as exc:
        STR0047R2.model_validate({})

    missing_fields = extract_missing_fields(exc.value)
    assert missing_fields == {
        'from_ispb',
        'system_domain',
        'str_control_number',
        'vendor_timestamp',
        'debtor_institution_ispb',
        'creditor_institution_ispb',
        'creditor_branch',
        'amount',
        'portability_number',
        'provider_ispb',
        'settlement_date',
        'to_ispb',
        'operation_number',
    }


def test_str0047r3_missing_required_fields() -> None:
    with pytest.raises(ValidationError) as exc:
        STR0047R3.model_validate({})

    missing_fields = extract_missing_fields(exc.value)
    assert missing_fields == {
        'from_ispb',
        'system_domain',
        'str_control_number',
        'vendor_timestamp',
        'debtor_institution_ispb',
        'creditor_institution_ispb',
        'creditor_branch',
        'amount',
        'portability_number',
        'provider_ispb',
        'settlement_date',
        'to_ispb',
        'operation_number',
    }


def test_str0047_to_xml() -> None:
    params = make_valid_str0047_params()
    str0047 = STR0047.model_validate(params)
    xml = str0047.to_xml()

    expected_xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/SPB/STR0047.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>31680151250908000000001</NUOp>
        </BCMSG>
        <SISMSG>
            <STR0047>
                <CodMsg>STR0047</CodMsg>
                <NumCtrlIF>31680151202509090425</NumCtrlIF>
                <ISPBIFDebtd>31680151</ISPBIFDebtd>
                <AgDebtd>0002</AgDebtd>
                <Grupo_STR0047_AgtFinancDebtd>
                    <CtDebtd>9876543</CtDebtd>
                    <CNPJ_CPFCliDebtd>53480615000129</CNPJ_CPFCliDebtd>
                    <NomeCliDebtd>Tiago Noah Julio Alves</NomeCliDebtd>
                </Grupo_STR0047_AgtFinancDebtd>
                <ISPBIFCredtd>00038166</ISPBIFCredtd>
                <AgCredtd>0001</AgCredtd>
                <Grupo_STR0047_AgtFinancCredtd>
                    <CtCredtd>123456</CtCredtd>
                    <CNPJCliCredtd>34161858000150</CNPJCliCredtd>
                    <NomCliCredtd>Olivia Sandra Rosângela Gomes</NomCliCredtd>
                </Grupo_STR0047_AgtFinancCredtd>
                <VlrLanc>125765.0</VlrLanc>
                <NUPortdd>K7J2N9P1L0B5V4X3M8Z9A</NUPortdd>
                <ISPBPrestd>31680151</ISPBPrestd>
                <Hist>Payment for services</Hist>
                <NivelPref>C</NivelPref>
                <DtAgendt>2026-01-28</DtAgendt>
                <HrAgendt>17:30:00</HrAgendt>
                <DtMovto>2026-01-28</DtMovto>
            </STR0047>
        </SISMSG>
    </DOC>
    """

    assert normalize_xml(expected_xml) == normalize_xml(xml)


def test_str0047r1_to_xml() -> None:
    params = make_valid_str0047r1_params()
    str0047r1 = STR0047R1.model_validate(params)
    xml = str0047r1.to_xml()

    expected_xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/SPB/STR0047.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>31680151250908000000001</NUOp>
        </BCMSG>
        <SISMSG>
            <STR0047R1>
                <CodMsg>STR0047R1</CodMsg>
                <NumCtrlIF>31680151202509090425</NumCtrlIF>
                <ISPBIFDebtd>31680151</ISPBIFDebtd>
                <NumCtrlSTR>STR20250101000000001</NumCtrlSTR>
                <SitLancSTR>1</SitLancSTR>
                <DtHrSit>2026-01-28T17:30:00</DtHrSit>
                <DtMovto>2026-01-28</DtMovto>
            </STR0047R1>
        </SISMSG>
    </DOC>
    """

    assert normalize_xml(expected_xml) == normalize_xml(xml)


def test_str0047r2_to_xml() -> None:
    params = make_valid_str0047r2_params()
    str0047r2 = STR0047R2.model_validate(params)
    xml = str0047r2.to_xml()

    expected_xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/SPB/STR0047.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>31680151250908000000001</NUOp>
        </BCMSG>
        <SISMSG>
            <STR0047R2>
                <CodMsg>STR0047R2</CodMsg>
                <NumCtrlSTR>STR20250101000000001</NumCtrlSTR>
                <DtHrBC>2026-01-28T17:26:50</DtHrBC>
                <ISPBIFDebtd>31680151</ISPBIFDebtd>
                <AgDebtd>0002</AgDebtd>
                <Grupo_STR0047R2_AgtFinancDebtd>
                    <CtDebtd>9876543</CtDebtd>
                    <CNPJ_CPFCliDebtd>53480615000129</CNPJ_CPFCliDebtd>
                    <NomeCliDebtd>Tiago Noah Julio Alves</NomeCliDebtd>
                </Grupo_STR0047R2_AgtFinancDebtd>
                <ISPBIFCredtd>00038166</ISPBIFCredtd>
                <AgCredtd>0001</AgCredtd>
                <Grupo_STR0047R2_AgtFinancCredtd>
                    <CtCredtd>123456</CtCredtd>
                    <CNPJCliCredtd>34161858000150</CNPJCliCredtd>
                    <NomCliCredtd>Olivia Sandra Rosângela Gomes</NomCliCredtd>
                </Grupo_STR0047R2_AgtFinancCredtd>
                <VlrLanc>125765.0</VlrLanc>
                <NUPortdd>K7J2N9P1L0B5V4X3M8Z9A</NUPortdd>
                <ISPBPrestd>31680151</ISPBPrestd>
                <Hist>Payment for services</Hist>
                <DtMovto>2026-01-28</DtMovto>
            </STR0047R2>
        </SISMSG>
    </DOC>
    """

    assert normalize_xml(expected_xml) == normalize_xml(xml)


def test_str0047r3_to_xml() -> None:
    params = make_valid_str0047r3_params()
    str0047r3 = STR0047R3.model_validate(params)
    xml = str0047r3.to_xml()

    expected_xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/SPB/STR0047.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>31680151250908000000001</NUOp>
        </BCMSG>
        <SISMSG>
            <STR0047R3>
                <CodMsg>STR0047R3</CodMsg>
                <NumCtrlSTR>STR20250101000000001</NumCtrlSTR>
                <DtHrBC>2026-01-28T17:26:50</DtHrBC>
                <ISPBIFDebtd>31680151</ISPBIFDebtd>
                <AgDebtd>0002</AgDebtd>
                <Grupo_STR0047R3_AgtFinancDebtd>
                    <CtDebtd>9876543</CtDebtd>
                    <CNPJ_CPFCliDebtd>53480615000129</CNPJ_CPFCliDebtd>
                    <NomeCliDebtd>Tiago Noah Julio Alves</NomeCliDebtd>
                </Grupo_STR0047R3_AgtFinancDebtd>
                <ISPBIFCredtd>00038166</ISPBIFCredtd>
                <AgCredtd>0001</AgCredtd>
                <Grupo_STR0047R3_AgtFinancCredtd>
                    <CtCredtd>123456</CtCredtd>
                    <CNPJCliCredtd>34161858000150</CNPJCliCredtd>
                    <NomCliCredtd>Olivia Sandra Rosângela Gomes</NomCliCredtd>
                </Grupo_STR0047R3_AgtFinancCredtd>
                <VlrLanc>125765.0</VlrLanc>
                <NUPortdd>K7J2N9P1L0B5V4X3M8Z9A</NUPortdd>
                <ISPBPrestd>31680151</ISPBPrestd>
                <Hist>Payment for services</Hist>
                <DtMovto>2026-01-28</DtMovto>
            </STR0047R3>
        </SISMSG>
    </DOC>
    """

    assert normalize_xml(expected_xml) == normalize_xml(xml)


def test_str0047e_general_error_to_xml() -> None:
    params = make_valid_str0047e_params(general_error=True)
    str0047e = STR0047E.model_validate(params)
    xml = str0047e.to_xml()

    expected_xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/SPB/STR0047E.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>31680151250908000000001</NUOp>
        </BCMSG>
        <SISMSG>
            <STR0047 CodErro="EGEN0050">
                <CodMsg>STR0047E</CodMsg>
                <NumCtrlIF>31680151202509090425</NumCtrlIF>
                <ISPBIFDebtd>31680151</ISPBIFDebtd>
                <AgDebtd>0002</AgDebtd>
                <Grupo_STR0047_AgtFinancDebtd>
                    <CtDebtd>9876543</CtDebtd>
                    <CNPJ_CPFCliDebtd>53480615000129</CNPJ_CPFCliDebtd>
                    <NomeCliDebtd>Tiago Noah Julio Alves</NomeCliDebtd>
                </Grupo_STR0047_AgtFinancDebtd>
                <ISPBIFCredtd>00038166</ISPBIFCredtd>
                <AgCredtd>0001</AgCredtd>
                <Grupo_STR0047_AgtFinancCredtd>
                    <CtCredtd>123456</CtCredtd>
                    <CNPJCliCredtd>34161858000150</CNPJCliCredtd>
                    <NomCliCredtd>Olivia Sandra Rosângela Gomes</NomCliCredtd>
                </Grupo_STR0047_AgtFinancCredtd>
                <VlrLanc>125765.0</VlrLanc>
                <NUPortdd>K7J2N9P1L0B5V4X3M8Z9A</NUPortdd>
                <ISPBPrestd>31680151</ISPBPrestd>
                <Hist>Payment for services</Hist>
                <NivelPref>C</NivelPref>
                <DtAgendt>2026-01-28</DtAgendt>
                <HrAgendt>17:30:00</HrAgendt>
                <DtMovto>2026-01-28</DtMovto>
            </STR0047>
        </SISMSG>
    </DOC>
    """

    assert normalize_xml(expected_xml) == normalize_xml(xml)


def test_str0047e_tag_error_to_xml() -> None:
    params = make_valid_str0047e_params()
    str0047e = STR0047E.model_validate(params)
    xml = str0047e.to_xml()

    expected_xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/SPB/STR0047E.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>31680151250908000000001</NUOp>
        </BCMSG>
        <SISMSG>
            <STR0047>
                <CodMsg>STR0047E</CodMsg>
                <NumCtrlIF>31680151202509090425</NumCtrlIF>
                <ISPBIFDebtd>31680151</ISPBIFDebtd>
                <AgDebtd>0002</AgDebtd>
                <Grupo_STR0047_AgtFinancDebtd>
                    <CtDebtd>9876543</CtDebtd>
                    <CNPJ_CPFCliDebtd>53480615000129</CNPJ_CPFCliDebtd>
                    <NomeCliDebtd>Tiago Noah Julio Alves</NomeCliDebtd>
                </Grupo_STR0047_AgtFinancDebtd>
                <ISPBIFCredtd>00038166</ISPBIFCredtd>
                <AgCredtd CodErro="ESPE0051">0001</AgCredtd>
                <Grupo_STR0047_AgtFinancCredtd>
                    <CtCredtd>123456</CtCredtd>
                    <CNPJCliCredtd>34161858000150</CNPJCliCredtd>
                    <NomCliCredtd>Olivia Sandra Rosângela Gomes</NomCliCredtd>
                </Grupo_STR0047_AgtFinancCredtd>
                <VlrLanc>125765.0</VlrLanc>
                <NUPortdd>K7J2N9P1L0B5V4X3M8Z9A</NUPortdd>
                <ISPBPrestd>31680151</ISPBPrestd>
                <Hist>Payment for services</Hist>
                <NivelPref>C</NivelPref>
                <DtAgendt>2026-01-28</DtAgendt>
                <HrAgendt>17:30:00</HrAgendt>
                <DtMovto>2026-01-28</DtMovto>
            </STR0047>
        </SISMSG>
    </DOC>
    """

    assert normalize_xml(expected_xml) == normalize_xml(xml)


def test_str0047_from_xml() -> None:
    xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/SPB/STR0047.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>31680151250908000000001</NUOp>
        </BCMSG>
        <SISMSG>
            <STR0047>
                <CodMsg>STR0047</CodMsg>
                <NumCtrlIF>31680151202509090425</NumCtrlIF>
                <ISPBIFDebtd>31680151</ISPBIFDebtd>
                <AgDebtd>0002</AgDebtd>
                <Grupo_STR0047_AgtFinancDebtd>
                    <CtDebtd>9876543</CtDebtd>
                    <CNPJ_CPFCliDebtd>53480615000129</CNPJ_CPFCliDebtd>
                    <NomeCliDebtd>Tiago Noah Julio Alves</NomeCliDebtd>
                </Grupo_STR0047_AgtFinancDebtd>
                <ISPBIFCredtd>00038166</ISPBIFCredtd>
                <AgCredtd>0001</AgCredtd>
                <Grupo_STR0047_AgtFinancCredtd>
                    <CtCredtd>123456</CtCredtd>
                    <CNPJCliCredtd>34161858000150</CNPJCliCredtd>
                    <NomCliCredtd>Olivia Sandra Rosângela Gomes</NomCliCredtd>
                </Grupo_STR0047_AgtFinancCredtd>
                <VlrLanc>125765.0</VlrLanc>
                <NUPortdd>K7J2N9P1L0B5V4X3M8Z9A</NUPortdd>
                <ISPBPrestd>31680151</ISPBPrestd>
                <Hist>Payment for services</Hist>
                <NivelPref>C</NivelPref>
                <DtAgendt>2026-01-28</DtAgendt>
                <HrAgendt>17:30:00</HrAgendt>
                <DtMovto>2026-01-28</DtMovto>
            </STR0047>
        </SISMSG>
    </DOC>
    """

    str0047 = STR0047.from_xml(xml)

    assert isinstance(str0047, STR0047)
    assert str0047.from_ispb == '31680151'
    assert str0047.operation_number == '31680151250908000000001'
    assert str0047.system_domain == 'SPB01'
    assert str0047.to_ispb == '00038166'
    assert str0047.message_code == 'STR0047'
    assert str0047.institution_control_number == '31680151202509090425'
    assert str0047.debtor_institution_ispb == '31680151'
    assert str0047.debtor_branch == '0002'
    assert str0047.creditor_institution_ispb == '00038166'
    assert str0047.creditor_branch == '0001'
    assert str0047.amount == Decimal('125765.00')
    assert str0047.portability_number == 'K7J2N9P1L0B5V4X3M8Z9A'
    assert str0047.provider_ispb == '31680151'
    assert str0047.description == 'Payment for services'
    assert str0047.priority == Priority.MEDIUM
    assert str0047.scheduled_date == date(2026, 1, 28)
    assert str0047.scheduled_time == time(17, 30)
    assert str0047.settlement_date == date(2026, 1, 28)

    debit = str0047.financial_debit_group
    assert isinstance(debit, FinancialAgentDebitedGroup)
    assert debit.debtor_account_number == '9876543'
    assert debit.debtor_document == '53480615000129'
    assert debit.debtor_name == 'Tiago Noah Julio Alves'

    credit = str0047.financial_credit_group
    assert isinstance(credit, FinancialAgentCreditorGroup)
    assert credit.creditor_account_number == '123456'
    assert credit.creditor_document == '34161858000150'
    assert credit.creditor_name == 'Olivia Sandra Rosângela Gomes'


def test_str0047r1_from_xml() -> None:
    xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/SPB/STR0047.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>31680151250908000000001</NUOp>
        </BCMSG>
        <SISMSG>
            <STR0047R1>
                <CodMsg>STR0047R1</CodMsg>
                <NumCtrlIF>31680151202509090425</NumCtrlIF>
                <ISPBIFDebtd>31680151</ISPBIFDebtd>
                <NumCtrlSTR>STR20250101000000001</NumCtrlSTR>
                <SitLancSTR>1</SitLancSTR>
                <DtHrSit>2026-01-28T17:30:00</DtHrSit>
                <DtMovto>2026-01-28</DtMovto>
            </STR0047R1>
        </SISMSG>
    </DOC>
    """

    str0047r1 = STR0047R1.from_xml(xml)

    assert isinstance(str0047r1, STR0047R1)
    assert str0047r1.institution_control_number == '31680151202509090425'
    assert str0047r1.message_code == 'STR0047R1'
    assert str0047r1.debtor_institution_ispb == '31680151'
    assert str0047r1.str_control_number == 'STR20250101000000001'
    assert str0047r1.str_settlement_status == StrSettlementStatus.EFFECTIVE
    assert str0047r1.settlement_timestamp == datetime(2026, 1, 28, 17, 30)
    assert str0047r1.settlement_date == date(2026, 1, 28)


def test_str0047r2_from_xml() -> None:
    xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/SPB/STR0047.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>31680151250908000000001</NUOp>
        </BCMSG>
        <SISMSG>
            <STR0047R2>
                <CodMsg>STR0047R2</CodMsg>
                <NumCtrlSTR>STR20250101000000001</NumCtrlSTR>
                <DtHrBC>2026-01-28T17:26:50</DtHrBC>
                <ISPBIFDebtd>31680151</ISPBIFDebtd>
                <AgDebtd>0002</AgDebtd>
                <Grupo_STR0047R2_AgtFinancDebtd>
                    <CtDebtd>9876543</CtDebtd>
                    <CNPJ_CPFCliDebtd>53480615000129</CNPJ_CPFCliDebtd>
                    <NomeCliDebtd>Tiago Noah Julio Alves</NomeCliDebtd>
                </Grupo_STR0047R2_AgtFinancDebtd>
                <ISPBIFCredtd>00038166</ISPBIFCredtd>
                <AgCredtd>0001</AgCredtd>
                <Grupo_STR0047R2_AgtFinancCredtd>
                    <CtCredtd>123456</CtCredtd>
                    <CNPJCliCredtd>34161858000150</CNPJCliCredtd>
                    <NomCliCredtd>Olivia Sandra Rosângela Gomes</NomCliCredtd>
                </Grupo_STR0047R2_AgtFinancCredtd>
                <VlrLanc>125765.00</VlrLanc>
                <NUPortdd>K7J2N9P1L0B5V4X3M8Z9A</NUPortdd>
                <ISPBPrestd>31680151</ISPBPrestd>
                <Hist>Payment for services</Hist>
                <DtMovto>2026-01-28</DtMovto>
            </STR0047R2>
        </SISMSG>
    </DOC>
    """

    str0047r2 = STR0047R2.from_xml(xml)

    assert isinstance(str0047r2, STR0047R2)
    assert str0047r2.message_code == 'STR0047R2'
    assert str0047r2.str_control_number == 'STR20250101000000001'
    assert str0047r2.vendor_timestamp == datetime(2026, 1, 28, 17, 26, 50)
    assert str0047r2.debtor_institution_ispb == '31680151'
    assert str0047r2.debtor_branch == '0002'
    assert str0047r2.creditor_institution_ispb == '00038166'
    assert str0047r2.creditor_branch == '0001'
    assert str0047r2.amount == Decimal('125765.00')
    assert str0047r2.portability_number == 'K7J2N9P1L0B5V4X3M8Z9A'
    assert str0047r2.provider_ispb == '31680151'
    assert str0047r2.description == 'Payment for services'
    assert str0047r2.settlement_date == date(2026, 1, 28)

    debit = str0047r2.financial_debit_group
    assert isinstance(debit, FinancialAgentDebitedR2Group)
    assert debit.debtor_account_number == '9876543'
    assert debit.debtor_document == '53480615000129'
    assert debit.debtor_name == 'Tiago Noah Julio Alves'

    credit = str0047r2.financial_credit_group
    assert isinstance(credit, FinancialAgentCreditorR2Group)
    assert credit.creditor_account_number == '123456'
    assert credit.creditor_document == '34161858000150'
    assert credit.creditor_name == 'Olivia Sandra Rosângela Gomes'


def test_str0047r3_from_xml() -> None:
    xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/SPB/STR0047.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>31680151250908000000001</NUOp>
        </BCMSG>
        <SISMSG>
            <STR0047R3>
                <CodMsg>STR0047R3</CodMsg>
                <NumCtrlSTR>STR20250101000000001</NumCtrlSTR>
                <DtHrBC>2026-01-28T17:26:50</DtHrBC>
                <ISPBIFDebtd>31680151</ISPBIFDebtd>
                <AgDebtd>0002</AgDebtd>
                <Grupo_STR0047R3_AgtFinancDebtd>
                    <CtDebtd>9876543</CtDebtd>
                    <CNPJ_CPFCliDebtd>53480615000129</CNPJ_CPFCliDebtd>
                    <NomeCliDebtd>Tiago Noah Julio Alves</NomeCliDebtd>
                </Grupo_STR0047R3_AgtFinancDebtd>
                <ISPBIFCredtd>00038166</ISPBIFCredtd>
                <AgCredtd>0001</AgCredtd>
                <Grupo_STR0047R3_AgtFinancCredtd>
                    <CtCredtd>123456</CtCredtd>
                    <CNPJCliCredtd>34161858000150</CNPJCliCredtd>
                    <NomCliCredtd>Olivia Sandra Rosângela Gomes</NomCliCredtd>
                </Grupo_STR0047R3_AgtFinancCredtd>
                <VlrLanc>125765.00</VlrLanc>
                <NUPortdd>K7J2N9P1L0B5V4X3M8Z9A</NUPortdd>
                <ISPBPrestd>31680151</ISPBPrestd>
                <Hist>Payment for services</Hist>
                <DtMovto>2026-01-28</DtMovto>
            </STR0047R3>
        </SISMSG>
    </DOC>
    """

    str0047r3 = STR0047R3.from_xml(xml)

    assert isinstance(str0047r3, STR0047R3)
    assert str0047r3.message_code == 'STR0047R3'
    assert str0047r3.str_control_number == 'STR20250101000000001'
    assert str0047r3.vendor_timestamp == datetime(2026, 1, 28, 17, 26, 50)
    assert str0047r3.debtor_institution_ispb == '31680151'
    assert str0047r3.debtor_branch == '0002'
    assert str0047r3.creditor_institution_ispb == '00038166'
    assert str0047r3.creditor_branch == '0001'
    assert str0047r3.amount == Decimal('125765.00')
    assert str0047r3.portability_number == 'K7J2N9P1L0B5V4X3M8Z9A'
    assert str0047r3.provider_ispb == '31680151'
    assert str0047r3.description == 'Payment for services'
    assert str0047r3.settlement_date == date(2026, 1, 28)

    debit = str0047r3.financial_debit_group
    assert isinstance(debit, FinancialAgentDebitedR3Group)
    assert debit.debtor_account_number == '9876543'
    assert debit.debtor_document == '53480615000129'
    assert debit.debtor_name == 'Tiago Noah Julio Alves'

    credit = str0047r3.financial_credit_group
    assert isinstance(credit, FinancialAgentCreditorR3Group)
    assert credit.creditor_account_number == '123456'
    assert credit.creditor_document == '34161858000150'
    assert credit.creditor_name == 'Olivia Sandra Rosângela Gomes'


def test_str0047e_general_error_from_xml() -> None:
    xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/SPB/STR0047E.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>31680151250908000000001</NUOp>
        </BCMSG>
        <SISMSG>
            <STR0047 CodErro="EGEN0050">
                <CodMsg>STR0047E</CodMsg>
                <NumCtrlIF>31680151202509090425</NumCtrlIF>
                <ISPBIFDebtd>31680151</ISPBIFDebtd>
                <AgDebtd>0002</AgDebtd>
                <Grupo_STR0047_AgtFinancDebtd>
                    <CtDebtd>9876543</CtDebtd>
                    <CNPJ_CPFCliDebtd>53480615000129</CNPJ_CPFCliDebtd>
                    <NomeCliDebtd>Tiago Noah Julio Alves</NomeCliDebtd>
                </Grupo_STR0047_AgtFinancDebtd>
                <ISPBIFCredtd>00038166</ISPBIFCredtd>
                <AgCredtd>0001</AgCredtd>
                <Grupo_STR0047_AgtFinancCredtd>
                    <CtCredtd>123456</CtCredtd>
                    <CNPJCliCredtd>34161858000150</CNPJCliCredtd>
                    <NomCliCredtd>Olivia Sandra Rosângela Gomes</NomCliCredtd>
                </Grupo_STR0047_AgtFinancCredtd>
                <VlrLanc>125765.00</VlrLanc>
                <NUPortdd>K7J2N9P1L0B5V4X3M8Z9A</NUPortdd>
                <ISPBPrestd>31680151</ISPBPrestd>
                <Hist>Payment for services</Hist>
                <NivelPref>C</NivelPref>
                <DtAgendt>2026-01-28</DtAgendt>
                <HrAgendt>17:30:00</HrAgendt>
                <DtMovto>2026-01-28</DtMovto>
            </STR0047>
        </SISMSG>
    </DOC>
    """

    str0047e = STR0047E.from_xml(xml)

    assert isinstance(str0047e, STR0047E)
    assert str0047e.from_ispb == '31680151'
    assert str0047e.operation_number == '31680151250908000000001'
    assert str0047e.system_domain == 'SPB01'
    assert str0047e.to_ispb == '00038166'
    assert str0047e.message_code == 'STR0047E'
    assert str0047e.institution_control_number == '31680151202509090425'
    assert str0047e.debtor_institution_ispb == '31680151'
    assert str0047e.debtor_branch == '0002'
    assert str0047e.creditor_institution_ispb == '00038166'
    assert str0047e.creditor_branch == '0001'
    assert str0047e.amount == Decimal('125765.00')
    assert str0047e.portability_number == 'K7J2N9P1L0B5V4X3M8Z9A'
    assert str0047e.provider_ispb == '31680151'
    assert str0047e.description == 'Payment for services'
    assert str0047e.priority == Priority.MEDIUM
    assert str0047e.scheduled_date == date(2026, 1, 28)
    assert str0047e.scheduled_time == time(17, 30)
    assert str0047e.settlement_date == date(2026, 1, 28)
    assert str0047e.general_error_code == 'EGEN0050'

    debit = str0047e.financial_debit_group
    assert isinstance(debit, FinancialAgentDebitedGroupError)
    assert debit.debtor_account_number == '9876543'
    assert debit.debtor_document == '53480615000129'
    assert debit.debtor_name == 'Tiago Noah Julio Alves'

    credit = str0047e.financial_credit_group
    assert isinstance(credit, FinancialAgentCreditorGroupError)
    assert credit.creditor_account_number == '123456'
    assert credit.creditor_document == '34161858000150'
    assert credit.creditor_name == 'Olivia Sandra Rosângela Gomes'


def test_str0047e_tag_error_from_xml() -> None:
    xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/SPB/STR0047E.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>31680151250908000000001</NUOp>
        </BCMSG>
        <SISMSG>
            <STR0047>
                <CodMsg>STR0047E</CodMsg>
                <NumCtrlIF>31680151202509090425</NumCtrlIF>
                <ISPBIFDebtd>31680151</ISPBIFDebtd>
                <AgDebtd>0002</AgDebtd>
                <Grupo_STR0047_AgtFinancDebtd>
                    <CtDebtd>9876543</CtDebtd>
                    <CNPJ_CPFCliDebtd>53480615000129</CNPJ_CPFCliDebtd>
                    <NomeCliDebtd>Tiago Noah Julio Alves</NomeCliDebtd>
                </Grupo_STR0047_AgtFinancDebtd>
                <ISPBIFCredtd>00038166</ISPBIFCredtd>
                <AgCredtd CodErro="ESPE0051">0001</AgCredtd>
                <Grupo_STR0047_AgtFinancCredtd>
                    <CtCredtd>123456</CtCredtd>
                    <CNPJCliCredtd>34161858000150</CNPJCliCredtd>
                    <NomCliCredtd>Olivia Sandra Rosângela Gomes</NomCliCredtd>
                </Grupo_STR0047_AgtFinancCredtd>
                <VlrLanc>125765.00</VlrLanc>
                <NUPortdd>K7J2N9P1L0B5V4X3M8Z9A</NUPortdd>
                <ISPBPrestd>31680151</ISPBPrestd>
                <Hist>Payment for services</Hist>
                <NivelPref>C</NivelPref>
                <DtAgendt>2026-01-28</DtAgendt>
                <HrAgendt>17:30:00</HrAgendt>
                <DtMovto>2026-01-28</DtMovto>
            </STR0047>
        </SISMSG>
    </DOC>
    """

    str0047e = STR0047E.from_xml(xml)

    assert isinstance(str0047e, STR0047E)
    assert str0047e.from_ispb == '31680151'
    assert str0047e.operation_number == '31680151250908000000001'
    assert str0047e.system_domain == 'SPB01'
    assert str0047e.to_ispb == '00038166'
    assert str0047e.message_code == 'STR0047E'
    assert str0047e.institution_control_number == '31680151202509090425'
    assert str0047e.debtor_institution_ispb == '31680151'
    assert str0047e.debtor_branch == '0002'
    assert str0047e.creditor_institution_ispb == '00038166'
    assert str0047e.creditor_branch == '0001'
    assert str0047e.amount == Decimal('125765.00')
    assert str0047e.portability_number == 'K7J2N9P1L0B5V4X3M8Z9A'
    assert str0047e.provider_ispb == '31680151'
    assert str0047e.description == 'Payment for services'
    assert str0047e.priority == Priority.MEDIUM
    assert str0047e.scheduled_date == date(2026, 1, 28)
    assert str0047e.scheduled_time == time(17, 30)
    assert str0047e.settlement_date == date(2026, 1, 28)
    assert str0047e.creditor_branch_error_code == 'ESPE0051'

    debit = str0047e.financial_debit_group
    assert isinstance(debit, FinancialAgentDebitedGroupError)
    assert debit.debtor_account_number == '9876543'
    assert debit.debtor_document == '53480615000129'
    assert debit.debtor_name == 'Tiago Noah Julio Alves'

    credit = str0047e.financial_credit_group
    assert isinstance(credit, FinancialAgentCreditorGroupError)
    assert credit.creditor_account_number == '123456'
    assert credit.creditor_document == '34161858000150'
    assert credit.creditor_name == 'Olivia Sandra Rosângela Gomes'


def test_str0047_roundtrip() -> None:
    params = make_valid_str0047_params()
    str0047 = STR0047.model_validate(params)
    xml = str0047.to_xml()
    str0047_from_xml = STR0047.from_xml(xml)
    assert str0047 == str0047_from_xml


def test_str0047r1_roundtrip() -> None:
    params = make_valid_str0047r1_params()
    str0047r1 = STR0047R1.model_validate(params)
    xml = str0047r1.to_xml()
    str0047r1_from_xml = STR0047R1.from_xml(xml)
    assert str0047r1 == str0047r1_from_xml


def test_str0047r2_roundtrip() -> None:
    params = make_valid_str0047r2_params()
    str0047r2 = STR0047R2.model_validate(params)
    xml = str0047r2.to_xml()
    str0047r2_from_xml = STR0047R2.from_xml(xml)
    assert str0047r2 == str0047r2_from_xml


def test_str0047r3_roundtrip() -> None:
    params = make_valid_str0047r3_params()
    str0047r3 = STR0047R3.model_validate(params)
    xml = str0047r3.to_xml()
    str0047r3_from_xml = STR0047R3.from_xml(xml)
    assert str0047r3 == str0047r3_from_xml


def test_str0047_from_xml_missing_required_fields() -> None:
    xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/SPB/STR0047.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>31680151250908000000001</NUOp>
        </BCMSG>
        <SISMSG>
            <STR0047>
                <CodMsg>STR0047</CodMsg>
                <Grupo_STR0047_AgtFinancDebtd></Grupo_STR0047_AgtFinancDebtd>
                <Grupo_STR0047_AgtFinancCredtd></Grupo_STR0047_AgtFinancCredtd>
            </STR0047>
        </SISMSG>
    </DOC>
    """

    with pytest.raises(ValidationError) as exc:
        STR0047.from_xml(xml)

    missing_fields = extract_missing_fields(exc.value)
    assert missing_fields == {
        'institution_control_number',
        'debtor_institution_ispb',
        'creditor_institution_ispb',
        'creditor_branch',
        'amount',
        'portability_number',
        'provider_ispb',
        'settlement_date',
    }
