from datetime import date, datetime, time
from decimal import Decimal
from typing import Any

import pytest
from pydantic import ValidationError

from sfn_messages.core.types import AccountType, CustomerPurpose, PersonType, Priority, StrSettlementStatus
from sfn_messages.str.str0034 import STR0034, STR0034E, STR0034R1, STR0034R2
from tests.conftest import extract_missing_fields, normalize_xml


def make_valid_str0034_params() -> dict[str, Any]:
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
        'investor_document': '56369416000136',
        'investor_name': 'Investor Corp',
        'investor_type': 'BUSINESS',
        'operation_number': '31680151250908000000001',
        'priority': 'MEDIUM',
        'purpose': 'CREDIT_IN_ACCOUNT',
        'scheduled_date': '2025-09-09',
        'scheduled_time': '15:30:00',
        'settlement_date': '2025-09-08',
        'system_domain': 'SPB01',
        'to_ispb': '00038166',
        'transaction_id': '0000000000000000000000001',
    }


def make_valid_str0034r1_params() -> dict[str, Any]:
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


def make_valid_str0034r2_params() -> dict[str, Any]:
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
        'investor_document': '56369416000136',
        'investor_name': 'Investor Corp',
        'investor_type': 'BUSINESS',
        'operation_number': '31680151250908000000001',
        'purpose': 'CREDIT_IN_ACCOUNT',
        'settlement_date': '2025-09-08',
        'system_domain': 'SPB01',
        'to_ispb': '00038166',
        'transaction_id': '0000000000000000000000001',
        'vendor_timestamp': '2025-11-20T15:30:00',
        'str_control_number': 'STR20250101000000001',
    }


def make_valid_str0034e_params(*, general_error: bool = False) -> dict[str, Any]:
    str0034e = {
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
        'investor_document': '56369416000136',
        'investor_name': 'Investor Corp',
        'investor_type': 'BUSINESS',
        'operation_number': '31680151250908000000001',
        'priority': 'MEDIUM',
        'purpose': 'CREDIT_IN_ACCOUNT',
        'scheduled_date': '2025-09-09',
        'scheduled_time': '15:30:00',
        'settlement_date': '2025-09-08',
        'system_domain': 'SPB01',
        'to_ispb': '00038166',
        'transaction_id': '0000000000000000000000001',
    }

    if general_error:
        str0034e['general_error_code'] = 'EGEN0050'
    else:
        str0034e['debtor_institution_ispb_error_code'] = 'EGEN0051'

    return str0034e


def test_str0034_valid_model() -> None:
    params = make_valid_str0034_params()
    str0034 = STR0034.model_validate(params)
    assert isinstance(str0034, STR0034)
    assert str0034.amount == Decimal('100.00')
    assert str0034.creditor_account_number == '123456'
    assert str0034.creditor_account_type == AccountType.DEPOSIT
    assert str0034.creditor_branch == '0001'
    assert str0034.creditor_document == '69327934075'
    assert str0034.creditor_institution_ispb == '60701190'
    assert str0034.creditor_name == 'Joe Doe'
    assert str0034.creditor_payment_account_number is None
    assert str0034.creditor_type == PersonType.INDIVIDUAL
    assert str0034.debtor_account_number == '654321'
    assert str0034.debtor_account_type == AccountType.CURRENT
    assert str0034.debtor_branch == '0002'
    assert str0034.debtor_document == '56369416000136'
    assert str0034.debtor_institution_ispb == '31680151'
    assert str0034.debtor_name == 'ACME Inc'
    assert str0034.debtor_payment_account_number is None
    assert str0034.debtor_type == PersonType.BUSINESS
    assert str0034.description == 'Payment for services'
    assert str0034.from_ispb == '31680151'
    assert str0034.institution_control_number == '31680151202509090425'
    assert str0034.investor_document == '56369416000136'
    assert str0034.investor_name == 'Investor Corp'
    assert str0034.investor_type == PersonType.BUSINESS
    assert str0034.operation_number == '31680151250908000000001'
    assert str0034.priority == Priority.MEDIUM
    assert str0034.purpose == CustomerPurpose.CREDIT_IN_ACCOUNT
    assert str0034.scheduled_date == date(2025, 9, 9)
    assert str0034.scheduled_time == time(15, 30)
    assert str0034.settlement_date == date(2025, 9, 8)
    assert str0034.system_domain == 'SPB01'
    assert str0034.to_ispb == '00038166'
    assert str0034.transaction_id == '0000000000000000000000001'


def test_str0034e_general_error_valid_model() -> None:
    params = make_valid_str0034e_params(general_error=True)
    str0034e = STR0034E.model_validate(params)
    assert isinstance(str0034e, STR0034E)
    assert str0034e.amount == Decimal('100.00')
    assert str0034e.creditor_account_number == '123456'
    assert str0034e.creditor_account_type == AccountType.DEPOSIT
    assert str0034e.creditor_branch == '0001'
    assert str0034e.creditor_document == '69327934075'
    assert str0034e.creditor_institution_ispb == '60701190'
    assert str0034e.creditor_name == 'Joe Doe'
    assert str0034e.creditor_payment_account_number is None
    assert str0034e.creditor_type == PersonType.INDIVIDUAL
    assert str0034e.debtor_account_number == '654321'
    assert str0034e.debtor_account_type == AccountType.CURRENT
    assert str0034e.debtor_branch == '0002'
    assert str0034e.debtor_document == '56369416000136'
    assert str0034e.debtor_institution_ispb == '31680151'
    assert str0034e.debtor_name == 'ACME Inc'
    assert str0034e.debtor_payment_account_number is None
    assert str0034e.debtor_type == PersonType.BUSINESS
    assert str0034e.description == 'Payment for services'
    assert str0034e.from_ispb == '31680151'
    assert str0034e.institution_control_number == '31680151202509090425'
    assert str0034e.investor_document == '56369416000136'
    assert str0034e.investor_name == 'Investor Corp'
    assert str0034e.investor_type == PersonType.BUSINESS
    assert str0034e.operation_number == '31680151250908000000001'
    assert str0034e.priority == Priority.MEDIUM
    assert str0034e.purpose == CustomerPurpose.CREDIT_IN_ACCOUNT
    assert str0034e.scheduled_date == date(2025, 9, 9)
    assert str0034e.scheduled_time == time(15, 30)
    assert str0034e.settlement_date == date(2025, 9, 8)
    assert str0034e.system_domain == 'SPB01'
    assert str0034e.to_ispb == '00038166'
    assert str0034e.transaction_id == '0000000000000000000000001'
    assert str0034e.general_error_code == 'EGEN0050'


def test_str0034e_tag_error_valid_model() -> None:
    params = make_valid_str0034e_params()
    str0034e = STR0034E.model_validate(params)
    assert isinstance(str0034e, STR0034E)
    assert str0034e.amount == Decimal('100.00')
    assert str0034e.creditor_account_number == '123456'
    assert str0034e.creditor_account_type == AccountType.DEPOSIT
    assert str0034e.creditor_branch == '0001'
    assert str0034e.creditor_document == '69327934075'
    assert str0034e.creditor_institution_ispb == '60701190'
    assert str0034e.creditor_name == 'Joe Doe'
    assert str0034e.creditor_payment_account_number is None
    assert str0034e.creditor_type == PersonType.INDIVIDUAL
    assert str0034e.debtor_account_number == '654321'
    assert str0034e.debtor_account_type == AccountType.CURRENT
    assert str0034e.debtor_branch == '0002'
    assert str0034e.debtor_document == '56369416000136'
    assert str0034e.debtor_institution_ispb == '31680151'
    assert str0034e.debtor_name == 'ACME Inc'
    assert str0034e.debtor_payment_account_number is None
    assert str0034e.debtor_type == PersonType.BUSINESS
    assert str0034e.description == 'Payment for services'
    assert str0034e.from_ispb == '31680151'
    assert str0034e.institution_control_number == '31680151202509090425'
    assert str0034e.investor_document == '56369416000136'
    assert str0034e.investor_name == 'Investor Corp'
    assert str0034e.investor_type == PersonType.BUSINESS
    assert str0034e.operation_number == '31680151250908000000001'
    assert str0034e.priority == Priority.MEDIUM
    assert str0034e.purpose == CustomerPurpose.CREDIT_IN_ACCOUNT
    assert str0034e.scheduled_date == date(2025, 9, 9)
    assert str0034e.scheduled_time == time(15, 30)
    assert str0034e.settlement_date == date(2025, 9, 8)
    assert str0034e.system_domain == 'SPB01'
    assert str0034e.to_ispb == '00038166'
    assert str0034e.transaction_id == '0000000000000000000000001'
    assert str0034e.debtor_institution_ispb_error_code == 'EGEN0051'


def test_str0034_missing_required_fields() -> None:
    with pytest.raises(ValidationError) as exc:
        STR0034.model_validate({})
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
        'investor_type',
        'investor_document',
        'investor_name',
    }


def test_str0034_business_rules_invalid_documents() -> None:
    params = make_valid_str0034_params()
    params['debtor_type'] = 'INDIVIDUAL'
    params['debtor_document'] = '56369416000136'
    params['creditor_type'] = 'BUSINESS'
    params['creditor_document'] = '69327934075'

    with pytest.raises(ValidationError) as exc:
        STR0034.model_validate(params)
    error_message = str(exc.value)
    assert 'Invalid CPF for debtor_type INDIVIDUAL' in error_message
    assert 'Invalid CNPJ for creditor_type BUSINESS' in error_message


def test_str0034_business_rules_invalid_investor_document() -> None:
    params = make_valid_str0034_params()
    params['investor_type'] = 'INDIVIDUAL'
    params['investor_document'] = '56369416000136'

    with pytest.raises(ValidationError) as exc:
        STR0034.model_validate(params)
    error_message = str(exc.value)
    assert 'Invalid CPF for investor_type INDIVIDUAL' in error_message


def test_str0034_business_rules_missing_description_for_other_purpose() -> None:
    params = make_valid_str0034_params()
    params['purpose'] = 'OTHERS'
    del params['description']

    with pytest.raises(ValidationError) as exc:
        STR0034.model_validate(params)
    error_message = str(exc.value)
    assert 'description is required when purpose is OTHERS' in error_message


def test_str0034_business_rules_missing_debtor_branch_for_debtor_account_type_is_not_payment() -> None:
    params = make_valid_str0034_params()
    params['debtor_account_type'] = 'CURRENT'
    del params['debtor_branch']

    with pytest.raises(ValidationError) as exc:
        STR0034.model_validate(params)
    error_message = str(exc.value)
    assert 'debtor_branch is required when debtor_account_type is not PAYMENT' in error_message


def test_str0034_business_rules_missing_creditor_branch_for_creditor_account_type_is_not_payment() -> None:
    params = make_valid_str0034_params()
    params['creditor_account_type'] = 'CURRENT'
    del params['creditor_branch']

    with pytest.raises(ValidationError) as exc:
        STR0034.model_validate(params)
    error_message = str(exc.value)
    assert 'creditor_branch is required when creditor_account_type is not PAYMENT' in error_message


def test_str0034_business_rules_missing_debtor_payment_account_number_for_debtor_account_type_is_payment() -> None:
    params = make_valid_str0034_params()
    params['debtor_account_type'] = 'PAYMENT'

    with pytest.raises(ValidationError) as exc:
        STR0034.model_validate(params)
    error_message = str(exc.value)
    assert 'debtor_payment_account_number is required when debtor_account_type is PAYMENT' in error_message


def test_str0034_business_rules_missing_creditor_payment_account_number_for_creditor_account_type_is_payment() -> None:
    params = make_valid_str0034_params()
    params['creditor_account_type'] = 'PAYMENT'

    with pytest.raises(ValidationError) as exc:
        STR0034.model_validate(params)
    error_message = str(exc.value)
    assert 'creditor_payment_account_number is required when creditor_account_type is PAYMENT' in error_message


def test_str0034_business_rules_missing_debtor_account_number_for_debtor_account_type_is_not_payment() -> None:
    params = make_valid_str0034_params()
    params['debtor_account_type'] = 'CURRENT'
    del params['debtor_account_number']

    with pytest.raises(ValidationError) as exc:
        STR0034.model_validate(params)
    error_message = str(exc.value)
    assert 'debtor_account_number is required when debtor_account_type is not PAYMENT' in error_message


def test_str0034_business_rules_missing_creditor_account_number_for_creditor_account_type_is_not_payment() -> None:
    params = make_valid_str0034_params()
    params['creditor_account_type'] = 'CURRENT'
    del params['creditor_account_number']

    with pytest.raises(ValidationError) as exc:
        STR0034.model_validate(params)
    error_message = str(exc.value)
    assert 'creditor_account_number is required when creditor_account_type is not PAYMENT' in error_message


def test_str0034_to_xml() -> None:
    params = make_valid_str0034_params()
    str0034 = STR0034.model_validate(params)
    xml = str0034.to_xml()

    expected_xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/SPB/STR0034.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>31680151250908000000001</NUOp>
        </BCMSG>
        <SISMSG>
            <STR0034>
                <CodMsg>STR0034</CodMsg>
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
                <CodCli>0000000000000000000000001</CodCli>
                <TpPessoaInvest>J</TpPessoaInvest>
                <CNPJ_CPFInvest>56369416000136</CNPJ_CPFInvest>
                <Nom_RzSocInvest>Investor Corp</Nom_RzSocInvest>
                <Hist>Payment for services</Hist>
                <NivelPref>C</NivelPref>
                <DtAgendt>2025-09-09</DtAgendt>
                <HrAgendt>15:30:00</HrAgendt>
                <DtMovto>2025-09-08</DtMovto>
            </STR0034>
        </SISMSG>
    </DOC>
    """

    assert normalize_xml(expected_xml) == normalize_xml(xml)


def test_str0034e_general_error_to_xml() -> None:
    params = make_valid_str0034e_params(general_error=True)
    str0034e = STR0034E.model_validate(params)
    xml = str0034e.to_xml()

    expected_xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/SPB/STR0034E.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>31680151250908000000001</NUOp>
        </BCMSG>
        <SISMSG>
            <STR0034 CodErro="EGEN0050">
                <CodMsg>STR0034E</CodMsg>
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
                <CodCli>0000000000000000000000001</CodCli>
                <TpPessoaInvest>J</TpPessoaInvest>
                <CNPJ_CPFInvest>56369416000136</CNPJ_CPFInvest>
                <Nom_RzSocInvest>Investor Corp</Nom_RzSocInvest>
                <Hist>Payment for services</Hist>
                <NivelPref>C</NivelPref>
                <DtAgendt>2025-09-09</DtAgendt>
                <HrAgendt>15:30:00</HrAgendt>
                <DtMovto>2025-09-08</DtMovto>
            </STR0034>
        </SISMSG>
    </DOC>
    """

    assert normalize_xml(expected_xml) == normalize_xml(xml)


def test_str0034e_tag_error_to_xml() -> None:
    params = make_valid_str0034e_params()
    str0034e = STR0034E.model_validate(params)
    xml = str0034e.to_xml()

    expected_xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/SPB/STR0034E.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>31680151250908000000001</NUOp>
        </BCMSG>
        <SISMSG>
            <STR0034>
                <CodMsg>STR0034E</CodMsg>
                <NumCtrlIF>31680151202509090425</NumCtrlIF>
                <ISPBIFDebtd CodErro="EGEN0051">31680151</ISPBIFDebtd>
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
                <CodCli>0000000000000000000000001</CodCli>
                <TpPessoaInvest>J</TpPessoaInvest>
                <CNPJ_CPFInvest>56369416000136</CNPJ_CPFInvest>
                <Nom_RzSocInvest>Investor Corp</Nom_RzSocInvest>
                <Hist>Payment for services</Hist>
                <NivelPref>C</NivelPref>
                <DtAgendt>2025-09-09</DtAgendt>
                <HrAgendt>15:30:00</HrAgendt>
                <DtMovto>2025-09-08</DtMovto>
            </STR0034>
        </SISMSG>
    </DOC>
    """

    assert normalize_xml(expected_xml) == normalize_xml(xml)


def test_str0034_to_xml_omit_optional_fields() -> None:
    params = make_valid_str0034_params()
    del params['description']
    del params['scheduled_date']
    del params['scheduled_time']
    del params['priority']
    del params['transaction_id']

    str0034 = STR0034.model_validate(params)
    xml = str0034.to_xml()

    expected_xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/SPB/STR0034.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>31680151250908000000001</NUOp>
        </BCMSG>
        <SISMSG>
            <STR0034>
                <CodMsg>STR0034</CodMsg>
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
                <TpPessoaInvest>J</TpPessoaInvest>
                <CNPJ_CPFInvest>56369416000136</CNPJ_CPFInvest>
                <Nom_RzSocInvest>Investor Corp</Nom_RzSocInvest>
                <DtMovto>2025-09-08</DtMovto>
            </STR0034>
        </SISMSG>
    </DOC>
    """

    assert normalize_xml(expected_xml) == normalize_xml(xml)


def test_str0034_from_xml() -> None:
    xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/SPB/STR0034.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>31680151250908000000001</NUOp>
        </BCMSG>
        <SISMSG>
            <STR0034>
                <CodMsg>STR0034</CodMsg>
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
                <CodCli>0000000000000000000000001</CodCli>
                <TpPessoaInvest>J</TpPessoaInvest>
                <CNPJ_CPFInvest>56369416000136</CNPJ_CPFInvest>
                <Nom_RzSocInvest>Investor Corp</Nom_RzSocInvest>
                <Hist>Payment for services</Hist>
                <NivelPref>C</NivelPref>
                <DtAgendt>2025-09-09</DtAgendt>
                <HrAgendt>15:30:00</HrAgendt>
                <DtMovto>2025-09-08</DtMovto>
            </STR0034>
        </SISMSG>
    </DOC>
    """

    str0034 = STR0034.from_xml(xml)
    assert isinstance(str0034, STR0034)
    assert str0034.amount == Decimal('100.0')
    assert str0034.creditor_account_number == '123456'
    assert str0034.creditor_account_type == AccountType.DEPOSIT
    assert str0034.creditor_branch == '0001'
    assert str0034.creditor_document == '69327934075'
    assert str0034.creditor_institution_ispb == '60701190'
    assert str0034.creditor_name == 'Joe Doe'
    assert str0034.creditor_payment_account_number is None
    assert str0034.creditor_type == PersonType.INDIVIDUAL
    assert str0034.debtor_account_number == '654321'
    assert str0034.debtor_account_type == AccountType.CURRENT
    assert str0034.debtor_branch == '0002'
    assert str0034.debtor_document == '56369416000136'
    assert str0034.debtor_institution_ispb == '31680151'
    assert str0034.debtor_name == 'ACME Inc'
    assert str0034.debtor_payment_account_number is None
    assert str0034.debtor_type == PersonType.BUSINESS
    assert str0034.description == 'Payment for services'
    assert str0034.from_ispb == '31680151'
    assert str0034.institution_control_number == '31680151202509090425'
    assert str0034.investor_document == '56369416000136'
    assert str0034.investor_name == 'Investor Corp'
    assert str0034.investor_type == PersonType.BUSINESS
    assert str0034.operation_number == '31680151250908000000001'
    assert str0034.purpose == CustomerPurpose.CREDIT_IN_ACCOUNT
    assert str0034.priority == Priority.MEDIUM
    assert str0034.scheduled_date == date(2025, 9, 9)
    assert str0034.scheduled_time == time(15, 30)
    assert str0034.settlement_date == date(2025, 9, 8)
    assert str0034.system_domain == 'SPB01'
    assert str0034.to_ispb == '00038166'
    assert str0034.transaction_id == '0000000000000000000000001'


def test_str0034e_general_error_from_xml() -> None:
    xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/SPB/STR0034E.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>31680151250908000000001</NUOp>
        </BCMSG>
        <SISMSG>
            <STR0034 CodErro="EGEN0050">
                <CodMsg>STR0034E</CodMsg>
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
                <CodCli>0000000000000000000000001</CodCli>
                <TpPessoaInvest>J</TpPessoaInvest>
                <CNPJ_CPFInvest>56369416000136</CNPJ_CPFInvest>
                <Nom_RzSocInvest>Investor Corp</Nom_RzSocInvest>
                <Hist>Payment for services</Hist>
                <NivelPref>C</NivelPref>
                <DtAgendt>2025-09-09</DtAgendt>
                <HrAgendt>15:30:00</HrAgendt>
                <DtMovto>2025-09-08</DtMovto>
            </STR0034>
        </SISMSG>
    </DOC>
    """

    str0034e = STR0034E.from_xml(xml)
    assert isinstance(str0034e, STR0034E)
    assert str0034e.amount == Decimal('100.0')
    assert str0034e.creditor_account_number == '123456'
    assert str0034e.creditor_account_type == AccountType.DEPOSIT
    assert str0034e.creditor_branch == '0001'
    assert str0034e.creditor_document == '69327934075'
    assert str0034e.creditor_institution_ispb == '60701190'
    assert str0034e.creditor_name == 'Joe Doe'
    assert str0034e.creditor_payment_account_number is None
    assert str0034e.creditor_type == PersonType.INDIVIDUAL
    assert str0034e.debtor_account_number == '654321'
    assert str0034e.debtor_account_type == AccountType.CURRENT
    assert str0034e.debtor_branch == '0002'
    assert str0034e.debtor_document == '56369416000136'
    assert str0034e.debtor_institution_ispb == '31680151'
    assert str0034e.debtor_name == 'ACME Inc'
    assert str0034e.debtor_payment_account_number is None
    assert str0034e.debtor_type == PersonType.BUSINESS
    assert str0034e.description == 'Payment for services'
    assert str0034e.from_ispb == '31680151'
    assert str0034e.institution_control_number == '31680151202509090425'
    assert str0034e.investor_document == '56369416000136'
    assert str0034e.investor_name == 'Investor Corp'
    assert str0034e.investor_type == PersonType.BUSINESS
    assert str0034e.operation_number == '31680151250908000000001'
    assert str0034e.purpose == CustomerPurpose.CREDIT_IN_ACCOUNT
    assert str0034e.priority == Priority.MEDIUM
    assert str0034e.scheduled_date == date(2025, 9, 9)
    assert str0034e.scheduled_time == time(15, 30)
    assert str0034e.settlement_date == date(2025, 9, 8)
    assert str0034e.system_domain == 'SPB01'
    assert str0034e.to_ispb == '00038166'
    assert str0034e.transaction_id == '0000000000000000000000001'
    assert str0034e.general_error_code == 'EGEN0050'


def test_str0034e_tag_error_from_xml() -> None:
    xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/SPB/STR0034E.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>31680151250908000000001</NUOp>
        </BCMSG>
        <SISMSG>
            <STR0034>
                <CodMsg>STR0034E</CodMsg>
                <NumCtrlIF>31680151202509090425</NumCtrlIF>
                <ISPBIFDebtd CodErro="EGEN0051">31680151</ISPBIFDebtd>
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
                <CodCli>0000000000000000000000001</CodCli>
                <TpPessoaInvest>J</TpPessoaInvest>
                <CNPJ_CPFInvest>56369416000136</CNPJ_CPFInvest>
                <Nom_RzSocInvest>Investor Corp</Nom_RzSocInvest>
                <Hist>Payment for services</Hist>
                <NivelPref>C</NivelPref>
                <DtAgendt>2025-09-09</DtAgendt>
                <HrAgendt>15:30:00</HrAgendt>
                <DtMovto>2025-09-08</DtMovto>
            </STR0034>
        </SISMSG>
    </DOC>
    """

    str0034e = STR0034E.from_xml(xml)
    assert isinstance(str0034e, STR0034E)
    assert str0034e.amount == Decimal('100.0')
    assert str0034e.creditor_account_number == '123456'
    assert str0034e.creditor_account_type == AccountType.DEPOSIT
    assert str0034e.creditor_branch == '0001'
    assert str0034e.creditor_document == '69327934075'
    assert str0034e.creditor_institution_ispb == '60701190'
    assert str0034e.creditor_name == 'Joe Doe'
    assert str0034e.creditor_payment_account_number is None
    assert str0034e.creditor_type == PersonType.INDIVIDUAL
    assert str0034e.debtor_account_number == '654321'
    assert str0034e.debtor_account_type == AccountType.CURRENT
    assert str0034e.debtor_branch == '0002'
    assert str0034e.debtor_document == '56369416000136'
    assert str0034e.debtor_institution_ispb == '31680151'
    assert str0034e.debtor_name == 'ACME Inc'
    assert str0034e.debtor_payment_account_number is None
    assert str0034e.debtor_type == PersonType.BUSINESS
    assert str0034e.description == 'Payment for services'
    assert str0034e.from_ispb == '31680151'
    assert str0034e.institution_control_number == '31680151202509090425'
    assert str0034e.investor_document == '56369416000136'
    assert str0034e.investor_name == 'Investor Corp'
    assert str0034e.investor_type == PersonType.BUSINESS
    assert str0034e.operation_number == '31680151250908000000001'
    assert str0034e.purpose == CustomerPurpose.CREDIT_IN_ACCOUNT
    assert str0034e.priority == Priority.MEDIUM
    assert str0034e.scheduled_date == date(2025, 9, 9)
    assert str0034e.scheduled_time == time(15, 30)
    assert str0034e.settlement_date == date(2025, 9, 8)
    assert str0034e.system_domain == 'SPB01'
    assert str0034e.to_ispb == '00038166'
    assert str0034e.transaction_id == '0000000000000000000000001'
    assert str0034e.debtor_institution_ispb_error_code == 'EGEN0051'


def test_str0034_from_xml_omit_optional_fields() -> None:
    xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/SPB/STR0034.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>31680151250908000000001</NUOp>
        </BCMSG>
        <SISMSG>
            <STR0034>
                <CodMsg>STR0034</CodMsg>
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
                <TpPessoaInvest>J</TpPessoaInvest>
                <CNPJ_CPFInvest>56369416000136</CNPJ_CPFInvest>
                <Nom_RzSocInvest>Investor Corp</Nom_RzSocInvest>
                <DtMovto>2025-09-08</DtMovto>
            </STR0034>
        </SISMSG>
    </DOC>
    """

    str0034 = STR0034.from_xml(xml)
    assert isinstance(str0034, STR0034)
    assert str0034.amount == Decimal('100.0')
    assert str0034.creditor_account_number == '123456'
    assert str0034.creditor_account_type == AccountType.DEPOSIT
    assert str0034.creditor_branch == '0001'
    assert str0034.creditor_document == '69327934075'
    assert str0034.creditor_institution_ispb == '60701190'
    assert str0034.creditor_name == 'Joe Doe'
    assert str0034.creditor_payment_account_number is None
    assert str0034.creditor_type == PersonType.INDIVIDUAL
    assert str0034.debtor_account_number == '654321'
    assert str0034.debtor_account_type == AccountType.CURRENT
    assert str0034.debtor_branch == '0002'
    assert str0034.debtor_document == '56369416000136'
    assert str0034.debtor_institution_ispb == '31680151'
    assert str0034.debtor_name == 'ACME Inc'
    assert str0034.debtor_payment_account_number is None
    assert str0034.debtor_type == PersonType.BUSINESS
    assert str0034.description is None
    assert str0034.from_ispb == '31680151'
    assert str0034.institution_control_number == '31680151202509090425'
    assert str0034.investor_document == '56369416000136'
    assert str0034.investor_name == 'Investor Corp'
    assert str0034.investor_type == PersonType.BUSINESS
    assert str0034.operation_number == '31680151250908000000001'
    assert str0034.purpose == CustomerPurpose.CREDIT_IN_ACCOUNT
    assert str0034.priority is None
    assert str0034.scheduled_date is None
    assert str0034.scheduled_time is None
    assert str0034.settlement_date == date(2025, 9, 8)
    assert str0034.system_domain == 'SPB01'
    assert str0034.to_ispb == '00038166'
    assert str0034.transaction_id is None


def test_str0034_roundtrip() -> None:
    params = make_valid_str0034_params()
    del params['priority']
    str0034 = STR0034.model_validate(params)
    xml = str0034.to_xml()
    str0034_from_xml = STR0034.from_xml(xml)
    assert str0034 == str0034_from_xml


def test_str0034_from_xml_missing_required_fields() -> None:
    xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/SPB/STR0034.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>31680151250908000000001</NUOp>
        </BCMSG>
        <SISMSG>
            <STR0034>
                <CodMsg>STR0034</CodMsg>
            </STR0034>
        </SISMSG>
    </DOC>
    """

    with pytest.raises(ValidationError) as exc:
        STR0034.from_xml(xml)
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
        'investor_type',
        'investor_document',
        'investor_name',
    }


def test_str0034r1_valid_model() -> None:
    params = make_valid_str0034r1_params()
    str0034r1 = STR0034R1.model_validate(params)
    assert isinstance(str0034r1, STR0034R1)
    assert str0034r1.debtor_institution_ispb == '31680151'
    assert str0034r1.from_ispb == '31680151'
    assert str0034r1.institution_control_number == '31680151202509090425'
    assert str0034r1.message_code == 'STR0034R1'
    assert str0034r1.operation_number == '31680151250908000000001'
    assert str0034r1.settlement_date == date(2025, 9, 8)
    assert str0034r1.settlement_timestamp == datetime(2025, 11, 20, 15, 30)
    assert str0034r1.str_control_number == 'STR20250101000000001'
    assert str0034r1.str_settlement_status == StrSettlementStatus.EFFECTIVE
    assert str0034r1.to_ispb == '00038166'
    assert str0034r1.system_domain == 'SPB01'


def test_str0034r1_missing_required_fields() -> None:
    with pytest.raises(ValidationError) as exc:
        STR0034R1.model_validate({})
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


def test_str0034r1_to_xml() -> None:
    params = make_valid_str0034r1_params()
    str0034r1 = STR0034R1.model_validate(params)
    xml = str0034r1.to_xml()

    expected_xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/SPB/STR0034.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>31680151250908000000001</NUOp>
        </BCMSG>
        <SISMSG>
            <STR0034R1>
                <CodMsg>STR0034R1</CodMsg>
                <NumCtrlIF>31680151202509090425</NumCtrlIF>
                <ISPBIFDebtd>31680151</ISPBIFDebtd>
                <NumCtrlSTR>STR20250101000000001</NumCtrlSTR>
                <SitLancSTR>1</SitLancSTR>
                <DtHrSit>2025-11-20T15:30:00</DtHrSit>
                <DtMovto>2025-09-08</DtMovto>
            </STR0034R1>
        </SISMSG>
    </DOC>
    """

    assert normalize_xml(expected_xml) == normalize_xml(xml)


def test_str0034r1_from_xml() -> None:
    xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/SPB/STR0034.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>31680151250908000000001</NUOp>
        </BCMSG>
        <SISMSG>
            <STR0034R1>
                <CodMsg>STR0034R1</CodMsg>
                <NumCtrlIF>31680151202509090425</NumCtrlIF>
                <ISPBIFDebtd>31680151</ISPBIFDebtd>
                <NumCtrlSTR>STR20250101000000001</NumCtrlSTR>
                <SitLancSTR>1</SitLancSTR>
                <DtHrSit>2025-11-20T15:30:00</DtHrSit>
                <DtMovto>2025-09-08</DtMovto>
            </STR0034R1>
        </SISMSG>
    </DOC>
    """
    str0034r1 = STR0034R1.from_xml(xml)
    assert isinstance(str0034r1, STR0034R1)
    assert str0034r1.debtor_institution_ispb == '31680151'
    assert str0034r1.from_ispb == '31680151'
    assert str0034r1.institution_control_number == '31680151202509090425'
    assert str0034r1.message_code == 'STR0034R1'
    assert str0034r1.operation_number == '31680151250908000000001'
    assert str0034r1.settlement_date == date(2025, 9, 8)
    assert str0034r1.settlement_timestamp == datetime(2025, 11, 20, 15, 30)
    assert str0034r1.str_control_number == 'STR20250101000000001'
    assert str0034r1.str_settlement_status == StrSettlementStatus.EFFECTIVE
    assert str0034r1.to_ispb == '00038166'
    assert str0034r1.system_domain == 'SPB01'


def test_str0034r1_roundtrip() -> None:
    params = make_valid_str0034r1_params()
    str0034r1 = STR0034R1.model_validate(params)
    xml = str0034r1.to_xml()
    str0034r1_from_xml = STR0034R1.from_xml(xml)
    assert str0034r1 == str0034r1_from_xml


def test_str0034r1_from_xml_missing_required_fields() -> None:
    xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/SPB/STR0034.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>31680151250908000000001</NUOp>
        </BCMSG>
        <SISMSG>
            <STR0034R1>
                <CodMsg>STR0034R1</CodMsg>
            </STR0034R1>
        </SISMSG>
    </DOC>
    """

    with pytest.raises(ValidationError) as exc:
        STR0034R1.from_xml(xml)
    missing_fields = extract_missing_fields(exc.value)
    assert missing_fields == {
        'settlement_date',
        'debtor_institution_ispb',
        'str_settlement_status',
        'str_control_number',
        'institution_control_number',
        'settlement_timestamp',
    }


def test_str0034r2_valid_model() -> None:
    params = make_valid_str0034r2_params()
    str0034r2 = STR0034R2.model_validate(params)
    assert isinstance(str0034r2, STR0034R2)
    assert str0034r2.amount == Decimal('100.00')
    assert str0034r2.creditor_account_number == '123456'
    assert str0034r2.creditor_account_type == AccountType.DEPOSIT
    assert str0034r2.creditor_branch == '0001'
    assert str0034r2.creditor_document == '69327934075'
    assert str0034r2.creditor_institution_ispb == '60701190'
    assert str0034r2.creditor_name == 'Joe Doe'
    assert str0034r2.creditor_payment_account_number is None
    assert str0034r2.creditor_type == PersonType.INDIVIDUAL
    assert str0034r2.debtor_account_number == '654321'
    assert str0034r2.debtor_account_type == AccountType.CURRENT
    assert str0034r2.debtor_branch == '0002'
    assert str0034r2.debtor_document == '56369416000136'
    assert str0034r2.debtor_institution_ispb == '31680151'
    assert str0034r2.debtor_name == 'ACME Inc'
    assert str0034r2.debtor_payment_account_number is None
    assert str0034r2.debtor_type == PersonType.BUSINESS
    assert str0034r2.description == 'Payment for services'
    assert str0034r2.from_ispb == '31680151'
    assert str0034r2.investor_document == '56369416000136'
    assert str0034r2.investor_name == 'Investor Corp'
    assert str0034r2.investor_type == PersonType.BUSINESS
    assert str0034r2.operation_number == '31680151250908000000001'
    assert str0034r2.purpose == CustomerPurpose.CREDIT_IN_ACCOUNT
    assert str0034r2.settlement_date == date(2025, 9, 8)
    assert str0034r2.system_domain == 'SPB01'
    assert str0034r2.to_ispb == '00038166'
    assert str0034r2.transaction_id == '0000000000000000000000001'
    assert str0034r2.vendor_timestamp == datetime(2025, 11, 20, 15, 30)
    assert str0034r2.str_control_number == 'STR20250101000000001'


def test_str0034r2_missing_required_fields() -> None:
    with pytest.raises(ValidationError) as exc:
        STR0034R2.model_validate({})
    missing_fields = extract_missing_fields(exc.value)
    assert missing_fields == {
        'amount',
        'creditor_institution_ispb',
        'system_domain',
        'creditor_account_type',
        'str_control_number',
        'debtor_document',
        'creditor_type',
        'to_ispb',
        'debtor_name',
        'operation_number',
        'settlement_date',
        'debtor_institution_ispb',
        'creditor_document',
        'from_ispb',
        'creditor_name',
        'purpose',
        'debtor_account_type',
        'vendor_timestamp',
        'debtor_type',
        'investor_type',
        'investor_document',
        'investor_name',
    }


def test_str0034r2_business_rules_invalid_documents() -> None:
    params = make_valid_str0034r2_params()
    params['debtor_type'] = 'INDIVIDUAL'
    params['debtor_document'] = '56369416000136'
    params['creditor_type'] = 'BUSINESS'
    params['creditor_document'] = '69327934075'

    with pytest.raises(ValidationError) as exc:
        STR0034R2.model_validate(params)
    error_message = str(exc.value)
    assert 'Invalid CPF for debtor_type INDIVIDUAL' in error_message
    assert 'Invalid CNPJ for creditor_type BUSINESS' in error_message


def test_str0034r2_business_rules_invalid_investor_document() -> None:
    params = make_valid_str0034r2_params()
    params['investor_type'] = 'INDIVIDUAL'
    params['investor_document'] = '56369416000136'

    with pytest.raises(ValidationError) as exc:
        STR0034R2.model_validate(params)
    error_message = str(exc.value)
    assert 'Invalid CPF for investor_type INDIVIDUAL' in error_message


def test_str0034r2_business_rules_missing_description_for_other_purpose() -> None:
    params = make_valid_str0034r2_params()
    params['purpose'] = 'OTHERS'
    del params['description']

    with pytest.raises(ValidationError) as exc:
        STR0034R2.model_validate(params)
    error_message = str(exc.value)
    assert 'description is required when purpose is OTHERS' in error_message


def test_str0034r2_business_rules_missing_debtor_branch_for_debtor_account_type_is_not_payment() -> None:
    params = make_valid_str0034r2_params()
    params['debtor_account_type'] = 'CURRENT'
    del params['debtor_branch']

    with pytest.raises(ValidationError) as exc:
        STR0034R2.model_validate(params)
    error_message = str(exc.value)
    assert 'debtor_branch is required when debtor_account_type is not PAYMENT' in error_message


def test_str0034r2_business_rules_missing_creditor_branch_for_creditor_account_type_is_not_payment() -> None:
    params = make_valid_str0034r2_params()
    params['creditor_account_type'] = 'CURRENT'
    del params['creditor_branch']

    with pytest.raises(ValidationError) as exc:
        STR0034R2.model_validate(params)
    error_message = str(exc.value)
    assert 'creditor_branch is required when creditor_account_type is not PAYMENT' in error_message


def test_str0034r2_business_rules_missing_debtor_payment_account_number_for_debtor_account_type_is_payment() -> None:
    params = make_valid_str0034r2_params()
    params['debtor_account_type'] = 'PAYMENT'

    with pytest.raises(ValidationError) as exc:
        STR0034R2.model_validate(params)
    error_message = str(exc.value)
    assert 'debtor_payment_account_number is required when debtor_account_type is PAYMENT' in error_message


def test_str0034r2_business_rules_missing_creditor_payment_account_number_for_creditor_account_type_is_payment() -> (
    None
):
    params = make_valid_str0034r2_params()
    params['creditor_account_type'] = 'PAYMENT'

    with pytest.raises(ValidationError) as exc:
        STR0034R2.model_validate(params)
    error_message = str(exc.value)
    assert 'creditor_payment_account_number is required when creditor_account_type is PAYMENT' in error_message


def test_str0034r2_business_rules_missing_debtor_account_number_for_debtor_account_type_is_not_payment() -> None:
    params = make_valid_str0034r2_params()
    params['debtor_account_type'] = 'CURRENT'
    del params['debtor_account_number']

    with pytest.raises(ValidationError) as exc:
        STR0034R2.model_validate(params)
    error_message = str(exc.value)
    assert 'debtor_account_number is required when debtor_account_type is not PAYMENT' in error_message


def test_str0034r2_business_rules_missing_creditor_account_number_for_creditor_account_type_is_not_payment() -> None:
    params = make_valid_str0034r2_params()
    params['creditor_account_type'] = 'CURRENT'
    del params['creditor_account_number']

    with pytest.raises(ValidationError) as exc:
        STR0034R2.model_validate(params)
    error_message = str(exc.value)
    assert 'creditor_account_number is required when creditor_account_type is not PAYMENT' in error_message


def test_str0034r2_to_xml() -> None:
    params = make_valid_str0034r2_params()
    str0034r2 = STR0034R2.model_validate(params)
    xml = str0034r2.to_xml()

    expected_xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/SPB/STR0034.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>31680151250908000000001</NUOp>
        </BCMSG>
        <SISMSG>
            <STR0034R2>
                <CodMsg>STR0034R2</CodMsg>
                <NumCtrlSTR>STR20250101000000001</NumCtrlSTR>
                <DtHrBC>2025-11-20T15:30:00</DtHrBC>
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
                <CodCli>0000000000000000000000001</CodCli>
                <TpPessoaInvest>J</TpPessoaInvest>
                <CNPJ_CPFInvest>56369416000136</CNPJ_CPFInvest>
                <Nom_RzSocInvest>Investor Corp</Nom_RzSocInvest>
                <Hist>Payment for services</Hist>
                <DtMovto>2025-09-08</DtMovto>
            </STR0034R2>
        </SISMSG>
    </DOC>
    """

    assert normalize_xml(expected_xml) == normalize_xml(xml)


def test_str0034r2_to_xml_omit_optional_fields() -> None:
    params = make_valid_str0034r2_params()
    del params['description']
    del params['transaction_id']

    str0034r2 = STR0034R2.model_validate(params)
    xml = str0034r2.to_xml()

    expected_xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/SPB/STR0034.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>31680151250908000000001</NUOp>
        </BCMSG>
        <SISMSG>
            <STR0034R2>
                <CodMsg>STR0034R2</CodMsg>
                <NumCtrlSTR>STR20250101000000001</NumCtrlSTR>
                <DtHrBC>2025-11-20T15:30:00</DtHrBC>
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
                <TpPessoaInvest>J</TpPessoaInvest>
                <CNPJ_CPFInvest>56369416000136</CNPJ_CPFInvest>
                <Nom_RzSocInvest>Investor Corp</Nom_RzSocInvest>
                <DtMovto>2025-09-08</DtMovto>
            </STR0034R2>
        </SISMSG>
    </DOC>
    """

    assert normalize_xml(expected_xml) == normalize_xml(xml)


def test_str0034r2_from_xml() -> None:
    xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/SPB/STR0034.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>31680151250908000000001</NUOp>
        </BCMSG>
        <SISMSG>
            <STR0034R2>
                <CodMsg>STR0034R2</CodMsg>
                <NumCtrlSTR>STR20250101000000001</NumCtrlSTR>
                <DtHrBC>2025-11-20T15:30:00</DtHrBC>
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
                <CodCli>0000000000000000000000001</CodCli>
                <TpPessoaInvest>J</TpPessoaInvest>
                <CNPJ_CPFInvest>56369416000136</CNPJ_CPFInvest>
                <Nom_RzSocInvest>Investor Corp</Nom_RzSocInvest>
                <Hist>Payment for services</Hist>
                <DtMovto>2025-09-08</DtMovto>
            </STR0034R2>
        </SISMSG>
    </DOC>
    """

    str0034r2 = STR0034R2.from_xml(xml)
    assert isinstance(str0034r2, STR0034R2)
    assert str0034r2.amount == Decimal('100.0')
    assert str0034r2.creditor_account_number == '123456'
    assert str0034r2.creditor_account_type == AccountType.DEPOSIT
    assert str0034r2.creditor_branch == '0001'
    assert str0034r2.creditor_document == '69327934075'
    assert str0034r2.creditor_institution_ispb == '60701190'
    assert str0034r2.creditor_name == 'Joe Doe'
    assert str0034r2.creditor_payment_account_number is None
    assert str0034r2.creditor_type == PersonType.INDIVIDUAL
    assert str0034r2.debtor_account_number == '654321'
    assert str0034r2.debtor_account_type == AccountType.CURRENT
    assert str0034r2.debtor_branch == '0002'
    assert str0034r2.debtor_document == '56369416000136'
    assert str0034r2.debtor_institution_ispb == '31680151'
    assert str0034r2.debtor_name == 'ACME Inc'
    assert str0034r2.debtor_payment_account_number is None
    assert str0034r2.debtor_type == PersonType.BUSINESS
    assert str0034r2.description == 'Payment for services'
    assert str0034r2.from_ispb == '31680151'
    assert str0034r2.investor_document == '56369416000136'
    assert str0034r2.investor_name == 'Investor Corp'
    assert str0034r2.investor_type == PersonType.BUSINESS
    assert str0034r2.operation_number == '31680151250908000000001'
    assert str0034r2.purpose == CustomerPurpose.CREDIT_IN_ACCOUNT
    assert str0034r2.settlement_date == date(2025, 9, 8)
    assert str0034r2.system_domain == 'SPB01'
    assert str0034r2.to_ispb == '00038166'
    assert str0034r2.transaction_id == '0000000000000000000000001'
    assert str0034r2.vendor_timestamp == datetime(2025, 11, 20, 15, 30)


def test_str0034r2_from_xml_omit_optional_fields() -> None:
    xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/SPB/STR0034.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>31680151250908000000001</NUOp>
        </BCMSG>
        <SISMSG>
            <STR0034R2>
                <CodMsg>STR0034R2</CodMsg>
                <NumCtrlSTR>STR20250101000000001</NumCtrlSTR>
                <DtHrBC>2025-11-20T15:30:00</DtHrBC>
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
                <TpPessoaInvest>J</TpPessoaInvest>
                <CNPJ_CPFInvest>56369416000136</CNPJ_CPFInvest>
                <Nom_RzSocInvest>Investor Corp</Nom_RzSocInvest>
                <DtMovto>2025-09-08</DtMovto>
            </STR0034R2>
        </SISMSG>
    </DOC>
    """

    str0034r2 = STR0034R2.from_xml(xml)
    assert isinstance(str0034r2, STR0034R2)
    assert str0034r2.amount == Decimal('100.0')
    assert str0034r2.creditor_account_number == '123456'
    assert str0034r2.creditor_account_type == AccountType.DEPOSIT
    assert str0034r2.creditor_branch == '0001'
    assert str0034r2.creditor_document == '69327934075'
    assert str0034r2.creditor_institution_ispb == '60701190'
    assert str0034r2.creditor_name == 'Joe Doe'
    assert str0034r2.creditor_payment_account_number is None
    assert str0034r2.creditor_type == PersonType.INDIVIDUAL
    assert str0034r2.debtor_account_number == '654321'
    assert str0034r2.debtor_account_type == AccountType.CURRENT
    assert str0034r2.debtor_branch == '0002'
    assert str0034r2.debtor_document == '56369416000136'
    assert str0034r2.debtor_institution_ispb == '31680151'
    assert str0034r2.debtor_name == 'ACME Inc'
    assert str0034r2.debtor_payment_account_number is None
    assert str0034r2.debtor_type == PersonType.BUSINESS
    assert str0034r2.description is None
    assert str0034r2.from_ispb == '31680151'
    assert str0034r2.investor_document == '56369416000136'
    assert str0034r2.investor_name == 'Investor Corp'
    assert str0034r2.investor_type == PersonType.BUSINESS
    assert str0034r2.operation_number == '31680151250908000000001'
    assert str0034r2.purpose == CustomerPurpose.CREDIT_IN_ACCOUNT
    assert str0034r2.settlement_date == date(2025, 9, 8)
    assert str0034r2.system_domain == 'SPB01'
    assert str0034r2.to_ispb == '00038166'
    assert str0034r2.transaction_id is None
    assert str0034r2.vendor_timestamp == datetime(2025, 11, 20, 15, 30)


def test_str0034r2_roundtrip() -> None:
    params = make_valid_str0034r2_params()
    str0034r2 = STR0034R2.model_validate(params)
    xml = str0034r2.to_xml()
    str0034r2_from_xml = STR0034R2.from_xml(xml)
    assert str0034r2 == str0034r2_from_xml


def test_str0034r2_from_xml_missing_required_fields() -> None:
    xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/SPB/STR0034.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>31680151250908000000001</NUOp>
        </BCMSG>
        <SISMSG>
            <STR0034R2>
                <CodMsg>STR0034R2</CodMsg>
            </STR0034R2>
        </SISMSG>
    </DOC>
    """

    with pytest.raises(ValidationError) as exc:
        STR0034R2.from_xml(xml)
    missing_fields = extract_missing_fields(exc.value)
    assert missing_fields == {
        'debtor_document',
        'str_control_number',
        'debtor_type',
        'debtor_name',
        'creditor_document',
        'creditor_institution_ispb',
        'creditor_account_type',
        'settlement_date',
        'vendor_timestamp',
        'purpose',
        'debtor_account_type',
        'amount',
        'debtor_institution_ispb',
        'creditor_name',
        'creditor_type',
        'investor_type',
        'investor_document',
        'investor_name',
    }
