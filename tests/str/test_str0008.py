from datetime import UTC, date, datetime, time
from decimal import Decimal
from typing import Any

import pytest
from pydantic import ValidationError

from sfn_messages.core.types import AccountType, CustomerPurpose, PersonType, Priority, StrSettlementStatus
from sfn_messages.str.str0008 import STR0008, STR0008R1
from tests.conftest import extract_missing_fields, normalize_xml


def make_valid_str0008_params() -> dict[str, Any]:
    return {
        'amount': 100.00,
        'creditor_account_number': '123456',
        'creditor_account_type': 'DEPOSIT',
        'creditor_institution_ispb': '60701190',
        'creditor_branch': '0001',
        'creditor_document': '69327934075',
        'creditor_name': 'Joe Doe',
        'creditor_type': 'INDIVIDUAL',
        'debtor_account_number': '654321',
        'debtor_account_type': 'CURRENT',
        'debtor_institution_ispb': '31680151',
        'debtor_branch': '0002',
        'debtor_document': '56369416000136',
        'debtor_name': 'ACME Inc',
        'debtor_type': 'BUSINESS',
        'description': 'Payment for services',
        'from_ispb': '31680151',
        'institution_control_number': '31680151202509090425',
        'operation_number': '316801512509080000001',
        'priority': 'MEDIUM',
        'purpose': 'CREDIT_IN_ACCOUNT',
        'scheduled_date': '2025-09-09',
        'scheduled_time': '15:30:00',
        'settlement_date': '2025-09-08',
        'system_domain': 'SPB01',
        'to_ispb': '00038166',
        'transaction_id': '0000000000000000000000001',
    }


def make_valid_str0008r1_params() -> dict[str, Any]:
    return {
        'institution_control_number': '31680151202509090425',
        'from_ispb': '31680151',
        'debtor_institution_ispb': '31680151',
        'str_control_number': 'STR20250101000000001',
        'str_settlement_status': 'EFFECTIVE',
        'provider_timestamp': '2025-11-20T15:30:00+00:00',
        'settlement_date': '2025-09-08',
        'operation_number': '316801512509080000001',
        'to_ispb': '00038166',
        'system_domain': 'SPB01',
    }


def test_str0008_valid_model() -> None:
    params = make_valid_str0008_params()
    str0008 = STR0008.model_validate(params)
    assert isinstance(str0008, STR0008)
    assert str0008.amount == Decimal('100.00')
    assert str0008.creditor_account_number == '123456'
    assert str0008.creditor_account_type == AccountType.DEPOSIT
    assert str0008.creditor_branch == '0001'
    assert str0008.creditor_document == '69327934075'
    assert str0008.creditor_institution_ispb == '60701190'
    assert str0008.creditor_name == 'Joe Doe'
    assert str0008.creditor_payment_account_number is None
    assert str0008.creditor_type == PersonType.INDIVIDUAL
    assert str0008.debtor_account_number == '654321'
    assert str0008.debtor_account_type == AccountType.CURRENT
    assert str0008.debtor_branch == '0002'
    assert str0008.debtor_document == '56369416000136'
    assert str0008.debtor_institution_ispb == '31680151'
    assert str0008.debtor_name == 'ACME Inc'
    assert str0008.debtor_payment_account_number is None
    assert str0008.debtor_type == PersonType.BUSINESS
    assert str0008.description == 'Payment for services'
    assert str0008.from_ispb == '31680151'
    assert str0008.institution_control_number == '31680151202509090425'
    assert str0008.operation_number == '316801512509080000001'
    assert str0008.priority == Priority.MEDIUM
    assert str0008.purpose == CustomerPurpose.CREDIT_IN_ACCOUNT
    assert str0008.scheduled_date == date(2025, 9, 9)
    assert str0008.scheduled_time == time(15, 30)
    assert str0008.settlement_date == date(2025, 9, 8)
    assert str0008.system_domain == 'SPB01'
    assert str0008.to_ispb == '00038166'
    assert str0008.transaction_id == '0000000000000000000000001'


def test_str0008_missing_required_fields() -> None:
    with pytest.raises(ValidationError) as exc:
        STR0008.model_validate({})
    missing_fields = extract_missing_fields(exc.value)
    assert missing_fields == {
        'debtor_institution_ispb',
        'creditor_name',
        'to_ispb',
        'purpose',
        'settlement_date',
        'amount',
        'creditor_institution_ispb',
        'debtor_name',
        'creditor_account_type',
        'system_domain',
        'debtor_type',
        'debtor_document',
        'debtor_account_type',
        'creditor_type',
        'institution_control_number',
        'from_ispb',
        'operation_number',
        'creditor_document',
    }


def test_str0008_business_rules_invalid_documents() -> None:
    params = make_valid_str0008_params()
    params['debtor_type'] = 'INDIVIDUAL'
    params['debtor_document'] = '56369416000136'
    params['creditor_type'] = 'BUSINESS'
    params['creditor_document'] = '69327934075'

    with pytest.raises(ValidationError) as exc:
        STR0008.model_validate(params)
    error_message = str(exc.value)
    assert 'Invalid CPF for debtor_type INDIVIDUAL' in error_message
    assert 'Invalid CNPJ for creditor_type BUSINESS' in error_message


def test_str0008_business_rules_missing_description_for_other_purpose() -> None:
    params = make_valid_str0008_params()
    params['purpose'] = 'OTHERS'
    del params['description']

    with pytest.raises(ValidationError) as exc:
        STR0008.model_validate(params)
    error_message = str(exc.value)
    assert 'description is required when purpose is OTHER' in error_message


def test_str0008_business_rules_missing_debtor_branch_for_debtor_account_type_is_not_payment() -> None:
    params = make_valid_str0008_params()
    params['debtor_account_type'] = 'CURRENT'
    del params['debtor_branch']

    with pytest.raises(ValidationError) as exc:
        STR0008.model_validate(params)
    error_message = str(exc.value)
    assert 'debtor_branch is required when debtor_account_type is not PAYMENT' in error_message


def test_str0008_business_rules_missing_creditor_branch_for_creditor_account_type_is_not_payment() -> None:
    params = make_valid_str0008_params()
    params['creditor_account_type'] = 'CURRENT'
    del params['creditor_branch']

    with pytest.raises(ValidationError) as exc:
        STR0008.model_validate(params)
    error_message = str(exc.value)
    assert 'creditor_branch is required when creditor_account_type is not PAYMENT' in error_message


def test_str0008_business_rules_missing_debtor_payment_account_number_for_debtor_account_type_is_payment() -> None:
    params = make_valid_str0008_params()
    params['debtor_account_type'] = 'PAYMENT'

    with pytest.raises(ValidationError) as exc:
        STR0008.model_validate(params)
    error_message = str(exc.value)
    assert 'debtor_payment_account_number is required when debtor_account_type is PAYMENT' in error_message


def test_str0008_business_rules_missing_creditor_payment_account_number_for_creditor_account_type_is_payment() -> None:
    params = make_valid_str0008_params()
    params['creditor_account_type'] = 'PAYMENT'

    with pytest.raises(ValidationError) as exc:
        STR0008.model_validate(params)
    error_message = str(exc.value)
    assert 'creditor_payment_account_number is required when creditor_account_type is PAYMENT' in error_message


def test_str0008_business_rules_missing_debtor_account_number_for_debtor_account_type_is_not_payment() -> None:
    params = make_valid_str0008_params()
    params['debtor_account_type'] = 'CURRENT'
    del params['debtor_account_number']

    with pytest.raises(ValidationError) as exc:
        STR0008.model_validate(params)
    error_message = str(exc.value)
    assert 'debtor_account_number is required when debtor_account_type is not PAYMENT' in error_message


def test_str0008_business_rules_missing_creditor_account_number_for_creditor_account_type_is_not_payment() -> None:
    params = make_valid_str0008_params()
    params['creditor_account_type'] = 'CURRENT'
    del params['creditor_account_number']

    with pytest.raises(ValidationError) as exc:
        STR0008.model_validate(params)
    error_message = str(exc.value)
    assert 'creditor_account_number is required when creditor_account_type is not PAYMENT' in error_message


def test_str0008_to_xml() -> None:
    params = make_valid_str0008_params()
    str0008 = STR0008.model_validate(params)
    xml = str0008.to_xml()

    expected_xml = """<?xml version="1.0"?>
    <DOC>
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>316801512509080000001</NUOp>
        </BCMSG>
        <SISMSG>
            <STR0008>
                <CodMsg>STR0008</CodMsg>
                <NumCtrlIF>31680151202509090425</NumCtrlIF>
                <ISPBIFDebtd>31680151</ISPBIFDebtd>
                <AgDebtd>0002</AgDebtd>
                <TpCtDebtd>CC</TpCtDebtd>
                <CtDebtd>654321</CtDebtd>
                <TpPessoaDebtd>J</TpPessoaDebtd>
                <CNPJ_CPFCliDebtd>56369416000136</CNPJ_CPFCliDebtd>
                <NomCliDebtd>ACME Inc</NomCliDebtd>
                <ISPBIFCredtd>60701190</ISPBIFCredtd>
                <AgCredtd>0001</AgCredtd>
                <TpCtCredtd>CD</TpCtCredtd>
                <CtCredtd>123456</CtCredtd>
                <TpPessoaCredtd>F</TpPessoaCredtd>
                <CNPJ_CPFCliCredtd>69327934075</CNPJ_CPFCliCredtd>
                <NomCliCredtd>Joe Doe</NomCliCredtd>
                <VlrLanc>100.0</VlrLanc>
                <FinlddCli>10</FinlddCli>
                <CodIdentdTransf>0000000000000000000000001</CodIdentdTransf>
                <Hist>Payment for services</Hist>
                <DtAgendt>2025-09-09</DtAgendt>
                <HrAgendt>15:30:00</HrAgendt>
                <NivelPref>C</NivelPref>
                <DtMovto>2025-09-08</DtMovto>
            </STR0008>
        </SISMSG>
    </DOC>
    """

    assert normalize_xml(expected_xml) == normalize_xml(xml)


def test_str0008_to_xml_omit_optional_fields() -> None:
    params = make_valid_str0008_params()
    del params['description']
    del params['scheduled_date']
    del params['scheduled_time']
    del params['priority']
    del params['transaction_id']

    str0008 = STR0008.model_validate(params)
    xml = str0008.to_xml()

    expected_xml = """<?xml version="1.0"?>
    <DOC>
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>316801512509080000001</NUOp>
        </BCMSG>
        <SISMSG>
            <STR0008>
                <CodMsg>STR0008</CodMsg>
                <NumCtrlIF>31680151202509090425</NumCtrlIF>
                <ISPBIFDebtd>31680151</ISPBIFDebtd>
                <AgDebtd>0002</AgDebtd>
                <TpCtDebtd>CC</TpCtDebtd>
                <CtDebtd>654321</CtDebtd>
                <TpPessoaDebtd>J</TpPessoaDebtd>
                <CNPJ_CPFCliDebtd>56369416000136</CNPJ_CPFCliDebtd>
                <NomCliDebtd>ACME Inc</NomCliDebtd>
                <ISPBIFCredtd>60701190</ISPBIFCredtd>
                <AgCredtd>0001</AgCredtd>
                <TpCtCredtd>CD</TpCtCredtd>
                <CtCredtd>123456</CtCredtd>
                <TpPessoaCredtd>F</TpPessoaCredtd>
                <CNPJ_CPFCliCredtd>69327934075</CNPJ_CPFCliCredtd>
                <NomCliCredtd>Joe Doe</NomCliCredtd>
                <VlrLanc>100.0</VlrLanc>
                <FinlddCli>10</FinlddCli>
                <DtMovto>2025-09-08</DtMovto>
            </STR0008>
        </SISMSG>
    </DOC>
    """

    assert normalize_xml(expected_xml) == normalize_xml(xml)


def test_str0008_from_xml() -> None:
    xml = """<?xml version="1.0"?>
    <DOC>
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>316801512509080000001</NUOp>
        </BCMSG>
        <SISMSG>
            <STR0008>
                <CodMsg>STR0008</CodMsg>
                <NumCtrlIF>31680151202509090425</NumCtrlIF>
                <ISPBIFDebtd>31680151</ISPBIFDebtd>
                <AgDebtd>0002</AgDebtd>
                <TpCtDebtd>CC</TpCtDebtd>
                <CtDebtd>654321</CtDebtd>
                <TpPessoaDebtd>J</TpPessoaDebtd>
                <CNPJ_CPFCliDebtd>56369416000136</CNPJ_CPFCliDebtd>
                <NomCliDebtd>ACME Inc</NomCliDebtd>
                <ISPBIFCredtd>60701190</ISPBIFCredtd>
                <AgCredtd>0001</AgCredtd>
                <TpCtCredtd>CD</TpCtCredtd>
                <CtCredtd>123456</CtCredtd>
                <TpPessoaCredtd>F</TpPessoaCredtd>
                <CNPJ_CPFCliCredtd>69327934075</CNPJ_CPFCliCredtd>
                <NomCliCredtd>Joe Doe</NomCliCredtd>
                <VlrLanc>100.0</VlrLanc>
                <FinlddCli>10</FinlddCli>
                <CodIdentdTransf>0000000000000000000000001</CodIdentdTransf>
                <Hist>Payment for services</Hist>
                <DtAgendt>2025-09-09</DtAgendt>
                <HrAgendt>15:30:00</HrAgendt>
                <DtMovto>2025-09-08</DtMovto>
            </STR0008>
        </SISMSG>
    </DOC>
    """

    str0008 = STR0008.from_xml(xml)
    assert isinstance(str0008, STR0008)
    assert str0008.amount == Decimal('100.0')
    assert str0008.creditor_account_number == '123456'
    assert str0008.creditor_account_type == AccountType.DEPOSIT
    assert str0008.creditor_branch == '0001'
    assert str0008.creditor_document == '69327934075'
    assert str0008.creditor_institution_ispb == '60701190'
    assert str0008.creditor_name == 'Joe Doe'
    assert str0008.creditor_payment_account_number is None
    assert str0008.creditor_type == PersonType.INDIVIDUAL
    assert str0008.debtor_account_number == '654321'
    assert str0008.debtor_account_type == AccountType.CURRENT
    assert str0008.debtor_branch == '0002'
    assert str0008.debtor_document == '56369416000136'
    assert str0008.debtor_institution_ispb == '31680151'
    assert str0008.debtor_name == 'ACME Inc'
    assert str0008.debtor_payment_account_number is None
    assert str0008.debtor_type == PersonType.BUSINESS
    assert str0008.description == 'Payment for services'
    assert str0008.from_ispb == '31680151'
    assert str0008.institution_control_number == '31680151202509090425'
    assert str0008.operation_number == '316801512509080000001'
    assert str0008.purpose == CustomerPurpose.CREDIT_IN_ACCOUNT
    assert str0008.scheduled_date == date(2025, 9, 9)
    assert str0008.scheduled_time == time(15, 30)
    assert str0008.settlement_date == date(2025, 9, 8)
    assert str0008.system_domain == 'SPB01'
    assert str0008.to_ispb == '00038166'
    assert str0008.transaction_id == '0000000000000000000000001'


def test_str0008_from_xml_omit_optional_fields() -> None:
    xml = """<?xml version="1.0"?>
    <DOC>
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>316801512509080000001</NUOp>
        </BCMSG>
        <SISMSG>
            <STR0008>
                <CodMsg>STR0008</CodMsg>
                <NumCtrlIF>31680151202509090425</NumCtrlIF>
                <ISPBIFDebtd>31680151</ISPBIFDebtd>
                <AgDebtd>0002</AgDebtd>
                <TpCtDebtd>CC</TpCtDebtd>
                <CtDebtd>654321</CtDebtd>
                <TpPessoaDebtd>J</TpPessoaDebtd>
                <CNPJ_CPFCliDebtd>56369416000136</CNPJ_CPFCliDebtd>
                <NomCliDebtd>ACME Inc</NomCliDebtd>
                <ISPBIFCredtd>60701190</ISPBIFCredtd>
                <AgCredtd>0001</AgCredtd>
                <TpCtCredtd>CD</TpCtCredtd>
                <CtCredtd>123456</CtCredtd>
                <TpPessoaCredtd>F</TpPessoaCredtd>
                <CNPJ_CPFCliCredtd>69327934075</CNPJ_CPFCliCredtd>
                <NomCliCredtd>Joe Doe</NomCliCredtd>
                <VlrLanc>100.0</VlrLanc>
                <FinlddCli>10</FinlddCli>
                <DtMovto>2025-09-08</DtMovto>
            </STR0008>
        </SISMSG>
    </DOC>
    """

    str0008 = STR0008.from_xml(xml)
    assert isinstance(str0008, STR0008)
    assert str0008.amount == Decimal('100.0')
    assert str0008.creditor_account_number == '123456'
    assert str0008.creditor_account_type == AccountType.DEPOSIT
    assert str0008.creditor_branch == '0001'
    assert str0008.creditor_document == '69327934075'
    assert str0008.creditor_institution_ispb == '60701190'
    assert str0008.creditor_name == 'Joe Doe'
    assert str0008.creditor_payment_account_number is None
    assert str0008.creditor_type == PersonType.INDIVIDUAL
    assert str0008.debtor_account_number == '654321'
    assert str0008.debtor_account_type == AccountType.CURRENT
    assert str0008.debtor_branch == '0002'
    assert str0008.debtor_document == '56369416000136'
    assert str0008.debtor_institution_ispb == '31680151'
    assert str0008.debtor_name == 'ACME Inc'
    assert str0008.debtor_payment_account_number is None
    assert str0008.debtor_type == PersonType.BUSINESS
    assert str0008.description is None
    assert str0008.from_ispb == '31680151'
    assert str0008.institution_control_number == '31680151202509090425'
    assert str0008.operation_number == '316801512509080000001'
    assert str0008.purpose == CustomerPurpose.CREDIT_IN_ACCOUNT
    assert str0008.priority is None
    assert str0008.scheduled_date is None
    assert str0008.scheduled_time is None
    assert str0008.settlement_date == date(2025, 9, 8)
    assert str0008.system_domain == 'SPB01'
    assert str0008.to_ispb == '00038166'
    assert str0008.transaction_id is None


def test_str0008_roundtrip() -> None:
    params = make_valid_str0008_params()
    del params['priority']
    str0008 = STR0008.model_validate(params)
    xml = str0008.to_xml()
    str0008_from_xml = STR0008.from_xml(xml)
    assert str0008 == str0008_from_xml


def test_str0008_from_xml_missing_required_fields() -> None:
    xml = """<?xml version="1.0"?>
    <DOC>
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>316801512509080000001</NUOp>
        </BCMSG>
        <SISMSG>
            <STR0008>
                <CodMsg>STR0008</CodMsg>
            </STR0008>
        </SISMSG>
    </DOC>
    """

    with pytest.raises(ValidationError) as exc:
        STR0008.from_xml(xml)
    missing_fields = extract_missing_fields(exc.value)
    assert missing_fields == {
        'creditor_type',
        'debtor_document',
        'settlement_date',
        'creditor_name',
        'amount',
        'debtor_institution_ispb',
        'debtor_name',
        'creditor_institution_ispb',
        'creditor_account_type',
        'creditor_document',
        'institution_control_number',
        'purpose',
        'debtor_account_type',
        'debtor_type',
    }


def test_str0008r1_valid_model() -> None:
    params = make_valid_str0008r1_params()
    str0008r1 = STR0008R1.model_validate(params)
    assert isinstance(str0008r1, STR0008R1)
    assert str0008r1.debtor_institution_ispb == '31680151'
    assert str0008r1.from_ispb == '31680151'
    assert str0008r1.institution_control_number == '31680151202509090425'
    assert str0008r1.message_code == 'STR0008R1'
    assert str0008r1.operation_number == '316801512509080000001'
    assert str0008r1.settlement_date == date(2025, 9, 8)
    assert str0008r1.provider_timestamp == datetime(2025, 11, 20, 15, 30, tzinfo=UTC)
    assert str0008r1.str_control_number == 'STR20250101000000001'
    assert str0008r1.str_settlement_status == StrSettlementStatus.EFFECTIVE
    assert str0008r1.to_ispb == '00038166'
    assert str0008r1.system_domain == 'SPB01'


def test_str0008r1_missing_required_fields() -> None:
    with pytest.raises(ValidationError) as exc:
        STR0008R1.model_validate({})
    missing_fields = extract_missing_fields(exc.value)
    assert missing_fields == {
        'to_ispb',
        'str_control_number',
        'provider_timestamp',
        'str_settlement_status',
        'institution_control_number',
        'debtor_institution_ispb',
        'system_domain',
        'operation_number',
        'from_ispb',
        'settlement_date',
    }


def test_str0008r1_to_xml() -> None:
    params = make_valid_str0008r1_params()
    str0008r1 = STR0008R1.model_validate(params)
    xml = str0008r1.to_xml()

    expected_xml = """<?xml version="1.0"?>
    <DOC>
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>316801512509080000001</NUOp>
        </BCMSG>
        <SISMSG>
            <STR0008R1>
                <CodMsg>STR0008R1</CodMsg>
                <NumCtrlIF>31680151202509090425</NumCtrlIF>
                <ISPBIFDebtd>31680151</ISPBIFDebtd>
                <NumCtrlSTR>STR20250101000000001</NumCtrlSTR>
                <SitLancSTR>1</SitLancSTR>
                <DtHrSit>2025-11-20 15:30:00+00:00</DtHrSit>
                <DtMovto>2025-09-08</DtMovto>
            </STR0008R1>
        </SISMSG>
    </DOC>
    """

    assert normalize_xml(expected_xml) == normalize_xml(xml)


def test_str0008r1_from_xml() -> None:
    xml = """<?xml version="1.0"?>
    <DOC>
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>316801512509080000001</NUOp>
        </BCMSG>
        <SISMSG>
            <STR0008R1>
                <CodMsg>STR0008R1</CodMsg>
                <NumCtrlIF>31680151202509090425</NumCtrlIF>
                <ISPBIFDebtd>31680151</ISPBIFDebtd>
                <NumCtrlSTR>STR20250101000000001</NumCtrlSTR>
                <SitLancSTR>1</SitLancSTR>
                <DtHrSit>2025-11-20 15:30:00+00:00</DtHrSit>
                <DtMovto>2025-09-08</DtMovto>
            </STR0008R1>
        </SISMSG>
    </DOC>
    """
    str0008r1 = STR0008R1.from_xml(xml)
    assert isinstance(str0008r1, STR0008R1)
    assert str0008r1.debtor_institution_ispb == '31680151'
    assert str0008r1.from_ispb == '31680151'
    assert str0008r1.institution_control_number == '31680151202509090425'
    assert str0008r1.message_code == 'STR0008R1'
    assert str0008r1.operation_number == '316801512509080000001'
    assert str0008r1.settlement_date == date(2025, 9, 8)
    assert str0008r1.provider_timestamp == datetime(2025, 11, 20, 15, 30, tzinfo=UTC)
    assert str0008r1.str_control_number == 'STR20250101000000001'
    assert str0008r1.str_settlement_status == StrSettlementStatus.EFFECTIVE
    assert str0008r1.to_ispb == '00038166'
    assert str0008r1.system_domain == 'SPB01'


def test_str0008r1_roundtrip() -> None:
    params = make_valid_str0008r1_params()
    str0008r1 = STR0008R1.model_validate(params)
    xml = str0008r1.to_xml()
    str0008r1_from_xml = STR0008R1.from_xml(xml)
    assert str0008r1 == str0008r1_from_xml


def test_str0008r1_from_xml_missing_required_fields() -> None:
    xml = """<?xml version="1.0"?>
    <DOC>
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>316801512509080000001</NUOp>
        </BCMSG>
        <SISMSG>
            <STR0008R1>
                <CodMsg>STR0008R1</CodMsg>
            </STR0008R1>
        </SISMSG>
    </DOC>
    """

    with pytest.raises(ValidationError) as exc:
        STR0008R1.from_xml(xml)
    missing_fields = extract_missing_fields(exc.value)
    assert missing_fields == {
        'settlement_date',
        'debtor_institution_ispb',
        'str_settlement_status',
        'str_control_number',
        'institution_control_number',
        'provider_timestamp',
    }
