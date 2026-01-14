from datetime import UTC, date, datetime, time
from decimal import Decimal
from typing import Any

import pytest
from pydantic import ValidationError

from sfn_messages.core.types import AccountType, PersonType, Priority, StrSettlementStatus
from sfn_messages.str.str0007 import STR0007, STR0007E, STR0007R1, STR0007R2
from sfn_messages.str.types import InstitutionPurpose
from tests.conftest import extract_missing_fields, normalize_xml


def make_valid_str0007_params() -> dict[str, Any]:
    return {
        'amount': 100.00,
        'creditor_account_number': '123456',
        'creditor_account_type': 'DEPOSIT',
        'creditor_institution_ispb': '60701190',
        'creditor_branch': '0001',
        'creditor_document': '69327934075',
        'credit_contract_number': 'CTR123456789',
        'creditor_name': 'Joe Doe',
        'creditor_type': 'INDIVIDUAL',
        'debtor_institution_ispb': '31680151',
        'sender_document': '56369416000136',
        'sender_name': 'ACME Inc',
        'sender_type': 'BUSINESS',
        'description': 'Payment for services',
        'from_ispb': '31680151',
        'institution_control_number': '31680151202509090425',
        'operation_number': '316801512509080000001',
        'priority': 'MEDIUM',
        'purpose': 'FX_INTERBANK_MARKET',
        'scheduled_date': '2025-09-09',
        'scheduled_time': '15:30:00',
        'settlement_date': '2025-09-08',
        'system_domain': 'SPB01',
        'to_ispb': '00038166',
        'transaction_id': '0000000000000000000000001',
    }


def make_valid_str0007r1_params() -> dict[str, Any]:
    return {
        'institution_control_number': '31680151202509090425',
        'from_ispb': '31680151',
        'debtor_institution_ispb': '31680151',
        'str_control_number': 'STR20250101000000001',
        'str_settlement_status': 'EFFECTIVE',
        'settlement_timestamp': '2025-11-20T15:30:00+00:00',
        'settlement_date': '2025-09-08',
        'operation_number': '316801512509080000001',
        'to_ispb': '00038166',
        'system_domain': 'SPB01',
    }


def make_valid_str0007r2_params() -> dict[str, Any]:
    return {
        'amount': 100.00,
        'creditor_account_number': '123456',
        'creditor_account_type': 'DEPOSIT',
        'creditor_institution_ispb': '60701190',
        'creditor_branch': '0001',
        'creditor_document': '69327934075',
        'credit_contract_number': 'CTR123456789',
        'creditor_name': 'Joe Doe',
        'creditor_type': 'INDIVIDUAL',
        'debtor_institution_ispb': '31680151',
        'sender_document': '56369416000136',
        'sender_name': 'ACME Inc',
        'sender_type': 'BUSINESS',
        'description': 'Payment for services',
        'from_ispb': '31680151',
        'str_control_number': 'STR20250101000000001',
        'vendor_timestamp': '2025-11-20T15:30:00+00:00',
        'operation_number': '316801512509080000001',
        'purpose': 'FX_INTERBANK_MARKET',
        'settlement_date': '2025-09-08',
        'system_domain': 'SPB01',
        'to_ispb': '00038166',
        'transaction_id': '0000000000000000000000001',
    }


def make_valid_str0007e_params(*, general_error: bool = False) -> dict[str, Any]:
    str0007e = {
        'amount': 100.00,
        'creditor_account_number': '123456',
        'creditor_account_type': 'DEPOSIT',
        'creditor_institution_ispb': '60701190',
        'creditor_branch': '0001',
        'creditor_document': '69327934075',
        'credit_contract_number': 'CTR123456789',
        'creditor_name': 'Joe Doe',
        'creditor_type': 'INDIVIDUAL',
        'debtor_institution_ispb': '31680151',
        'sender_document': '56369416000136',
        'sender_name': 'ACME Inc',
        'sender_type': 'BUSINESS',
        'description': 'Payment for services',
        'from_ispb': '31680151',
        'institution_control_number': '31680151202509090425',
        'operation_number': '316801512509080000001',
        'priority': 'MEDIUM',
        'purpose': 'FX_INTERBANK_MARKET',
        'scheduled_date': '2025-09-09',
        'scheduled_time': '15:30:00',
        'settlement_date': '2025-09-08',
        'system_domain': 'SPB01',
        'to_ispb': '00038166',
        'transaction_id': '0000000000000000000000001',
    }

    if general_error:
        str0007e['general_error_code'] = 'EGEN0050'
    else:
        str0007e['debtor_institution_ispb_error_code'] = 'EGEN0051'

    return str0007e


def test_str0007_model_valid() -> None:
    params = make_valid_str0007_params()
    message = STR0007.model_validate(params)
    assert message.amount == Decimal('100.00')
    assert message.creditor_account_number == '123456'
    assert message.creditor_account_type == AccountType.DEPOSIT
    assert message.creditor_institution_ispb == '60701190'
    assert message.creditor_branch == '0001'
    assert message.creditor_document == '69327934075'
    assert message.credit_contract_number == 'CTR123456789'
    assert message.creditor_name == 'Joe Doe'
    assert message.creditor_type == PersonType.INDIVIDUAL
    assert message.debtor_institution_ispb == '31680151'
    assert message.sender_document == '56369416000136'
    assert message.sender_name == 'ACME Inc'
    assert message.sender_type == PersonType.BUSINESS
    assert message.description == 'Payment for services'
    assert message.institution_control_number == '31680151202509090425'
    assert message.priority == Priority.MEDIUM
    assert message.purpose == InstitutionPurpose.FX_INTERBANK_MARKET
    assert message.scheduled_date == date(2025, 9, 9)
    assert message.scheduled_time == time(15, 30)
    assert message.settlement_date == date(2025, 9, 8)
    assert message.transaction_id == '0000000000000000000000001'


def test_str0007e_general_error_model_valid() -> None:
    params = make_valid_str0007e_params(general_error=True)
    message = STR0007E.model_validate(params)
    assert message.amount == Decimal('100.00')
    assert message.creditor_account_number == '123456'
    assert message.creditor_account_type == AccountType.DEPOSIT
    assert message.creditor_institution_ispb == '60701190'
    assert message.creditor_branch == '0001'
    assert message.creditor_document == '69327934075'
    assert message.credit_contract_number == 'CTR123456789'
    assert message.creditor_name == 'Joe Doe'
    assert message.creditor_type == PersonType.INDIVIDUAL
    assert message.debtor_institution_ispb == '31680151'
    assert message.sender_document == '56369416000136'
    assert message.sender_name == 'ACME Inc'
    assert message.sender_type == PersonType.BUSINESS
    assert message.description == 'Payment for services'
    assert message.institution_control_number == '31680151202509090425'
    assert message.priority == Priority.MEDIUM
    assert message.purpose == InstitutionPurpose.FX_INTERBANK_MARKET
    assert message.scheduled_date == date(2025, 9, 9)
    assert message.scheduled_time == time(15, 30)
    assert message.settlement_date == date(2025, 9, 8)
    assert message.transaction_id == '0000000000000000000000001'
    assert message.general_error_code == 'EGEN0050'


def test_str0007e_tag_error_model_valid() -> None:
    params = make_valid_str0007e_params()
    message = STR0007E.model_validate(params)
    assert message.amount == Decimal('100.00')
    assert message.creditor_account_number == '123456'
    assert message.creditor_account_type == AccountType.DEPOSIT
    assert message.creditor_institution_ispb == '60701190'
    assert message.creditor_branch == '0001'
    assert message.creditor_document == '69327934075'
    assert message.credit_contract_number == 'CTR123456789'
    assert message.creditor_name == 'Joe Doe'
    assert message.creditor_type == PersonType.INDIVIDUAL
    assert message.debtor_institution_ispb == '31680151'
    assert message.sender_document == '56369416000136'
    assert message.sender_name == 'ACME Inc'
    assert message.sender_type == PersonType.BUSINESS
    assert message.description == 'Payment for services'
    assert message.institution_control_number == '31680151202509090425'
    assert message.priority == Priority.MEDIUM
    assert message.purpose == InstitutionPurpose.FX_INTERBANK_MARKET
    assert message.scheduled_date == date(2025, 9, 9)
    assert message.scheduled_time == time(15, 30)
    assert message.settlement_date == date(2025, 9, 8)
    assert message.transaction_id == '0000000000000000000000001'
    assert message.debtor_institution_ispb_error_code == 'EGEN0051'


def test_str0007_missing_required_fields() -> None:
    with pytest.raises(ValidationError) as exc:
        STR0007.model_validate({})
    missing_fields = extract_missing_fields(exc.value)
    assert missing_fields == {
        'creditor_name',
        'operation_number',
        'creditor_document',
        'to_ispb',
        'purpose',
        'from_ispb',
        'system_domain',
        'debtor_institution_ispb',
        'amount',
        'institution_control_number',
        'settlement_date',
        'creditor_account_type',
        'creditor_institution_ispb',
        'creditor_type',
    }


def test_str0007_business_rules_invalid_documents() -> None:
    params = make_valid_str0007_params()
    params['sender_type'] = 'INDIVIDUAL'
    params['sender_document'] = '56369416000136'
    params['creditor_type'] = 'BUSINESS'
    params['creditor_document'] = '69327934075'

    with pytest.raises(ValidationError) as exc:
        STR0007.model_validate(params)
    error_message = str(exc.value)
    assert 'Invalid CPF for sender_type INDIVIDUAL' in error_message
    assert 'Invalid CNPJ for creditor_type BUSINESS' in error_message


def test_str0007_business_rules_missing_description_for_other_purpose() -> None:
    params = make_valid_str0007_params()
    params['purpose'] = 'OTHERS'
    del params['description']

    with pytest.raises(ValidationError) as exc:
        STR0007.model_validate(params)
    error_message = str(exc.value)
    assert 'description is required when purpose is OTHERS' in error_message


def test_str0007_business_rules_missing_creditor_branch_for_creditor_account_type_is_not_payment() -> None:
    params = make_valid_str0007_params()
    params['creditor_account_type'] = 'CURRENT'
    del params['creditor_branch']

    with pytest.raises(ValidationError) as exc:
        STR0007.model_validate(params)
    error_message = str(exc.value)
    assert 'creditor_branch is required when creditor_account_type is not PAYMENT' in error_message


def test_str0007_business_rules_missing_creditor_payment_account_number_for_creditor_account_type_is_payment() -> None:
    params = make_valid_str0007_params()
    params['creditor_account_type'] = 'PAYMENT'

    with pytest.raises(ValidationError) as exc:
        STR0007.model_validate(params)
    error_message = str(exc.value)
    assert 'creditor_payment_account_number is required when creditor_account_type is PAYMENT' in error_message


def test_str0007_business_rules_missing_creditor_account_number_for_creditor_account_type_is_not_payment() -> None:
    params = make_valid_str0007_params()
    params['creditor_account_type'] = 'CURRENT'
    del params['creditor_account_number']

    with pytest.raises(ValidationError) as exc:
        STR0007.model_validate(params)
    error_message = str(exc.value)
    assert 'creditor_account_number is required when creditor_account_type is not PAYMENT' in error_message


def test_str0007_to_xml() -> None:
    params = make_valid_str0007_params()
    str0007 = STR0007.model_validate(params)
    xml = str0007.to_xml()

    expected_xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/SPB/STR0007.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>316801512509080000001</NUOp>
        </BCMSG>
        <SISMSG>
            <STR0007>
                <CodMsg>STR0007</CodMsg>
                <NumCtrlIF>31680151202509090425</NumCtrlIF>
                <ISPBIFDebtd>31680151</ISPBIFDebtd>
                <TpPessoaRemet>J</TpPessoaRemet>
                <CNPJ_CPFRemet>56369416000136</CNPJ_CPFRemet>
                <NomRemet>ACME Inc</NomRemet>
                <ISPBIFCredtd>60701190</ISPBIFCredtd>
                <AgCredtd>0001</AgCredtd>
                <TpCtCredtd>CD</TpCtCredtd>
                <CtCredtd>123456</CtCredtd>
                <TpPessoaCredtd>F</TpPessoaCredtd>
                <CNPJ_CPFCliCredtd>69327934075</CNPJ_CPFCliCredtd>
                <NomCliCredtd>Joe Doe</NomCliCredtd>
                <NumCtrdCredtd>CTR123456789</NumCtrdCredtd>
                <VlrLanc>100.0</VlrLanc>
                <FinlddIF>1</FinlddIF>
                <CodIdentdTransf>0000000000000000000000001</CodIdentdTransf>
                <Hist>Payment for services</Hist>
                <DtAgendt>2025-09-09</DtAgendt>
                <HrAgendt>15:30:00</HrAgendt>
                <NivelPref>C</NivelPref>
                <DtMovto>2025-09-08</DtMovto>
            </STR0007>
        </SISMSG>
    </DOC>
    """

    assert normalize_xml(expected_xml) == normalize_xml(xml)


def test_str0007e_general_error_to_xml() -> None:
    params = make_valid_str0007e_params(general_error=True)
    str0007e = STR0007E.model_validate(params)
    xml = str0007e.to_xml()

    expected_xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/SPB/STR0007E.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>316801512509080000001</NUOp>
        </BCMSG>
        <SISMSG>
            <STR0007E CodErro="EGEN0050">
                <CodMsg>STR0007</CodMsg>
                <NumCtrlIF>31680151202509090425</NumCtrlIF>
                <ISPBIFDebtd>31680151</ISPBIFDebtd>
                <TpPessoaRemet>J</TpPessoaRemet>
                <CNPJ_CPFRemet>56369416000136</CNPJ_CPFRemet>
                <NomRemet>ACME Inc</NomRemet>
                <ISPBIFCredtd>60701190</ISPBIFCredtd>
                <AgCredtd>0001</AgCredtd>
                <TpCtCredtd>CD</TpCtCredtd>
                <CtCredtd>123456</CtCredtd>
                <TpPessoaCredtd>F</TpPessoaCredtd>
                <CNPJ_CPFCliCredtd>69327934075</CNPJ_CPFCliCredtd>
                <NomCliCredtd>Joe Doe</NomCliCredtd>
                <NumCtrdCredtd>CTR123456789</NumCtrdCredtd>
                <VlrLanc>100.0</VlrLanc>
                <FinlddIF>1</FinlddIF>
                <CodIdentdTransf>0000000000000000000000001</CodIdentdTransf>
                <Hist>Payment for services</Hist>
                <DtAgendt>2025-09-09</DtAgendt>
                <HrAgendt>15:30:00</HrAgendt>
                <NivelPref>C</NivelPref>
                <DtMovto>2025-09-08</DtMovto>
            </STR0007E>
        </SISMSG>
    </DOC>
    """

    assert normalize_xml(expected_xml) == normalize_xml(xml)


def test_str0007e_tag_error_to_xml() -> None:
    params = make_valid_str0007e_params()
    str0007e = STR0007E.model_validate(params)
    xml = str0007e.to_xml()

    expected_xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/SPB/STR0007E.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>316801512509080000001</NUOp>
        </BCMSG>
        <SISMSG>
            <STR0007E>
                <CodMsg>STR0007</CodMsg>
                <NumCtrlIF>31680151202509090425</NumCtrlIF>
                <ISPBIFDebtd CodErro="EGEN0051">31680151</ISPBIFDebtd>
                <TpPessoaRemet>J</TpPessoaRemet>
                <CNPJ_CPFRemet>56369416000136</CNPJ_CPFRemet>
                <NomRemet>ACME Inc</NomRemet>
                <ISPBIFCredtd>60701190</ISPBIFCredtd>
                <AgCredtd>0001</AgCredtd>
                <TpCtCredtd>CD</TpCtCredtd>
                <CtCredtd>123456</CtCredtd>
                <TpPessoaCredtd>F</TpPessoaCredtd>
                <CNPJ_CPFCliCredtd>69327934075</CNPJ_CPFCliCredtd>
                <NomCliCredtd>Joe Doe</NomCliCredtd>
                <NumCtrdCredtd>CTR123456789</NumCtrdCredtd>
                <VlrLanc>100.0</VlrLanc>
                <FinlddIF>1</FinlddIF>
                <CodIdentdTransf>0000000000000000000000001</CodIdentdTransf>
                <Hist>Payment for services</Hist>
                <DtAgendt>2025-09-09</DtAgendt>
                <HrAgendt>15:30:00</HrAgendt>
                <NivelPref>C</NivelPref>
                <DtMovto>2025-09-08</DtMovto>
            </STR0007E>
        </SISMSG>
    </DOC>
    """

    assert normalize_xml(expected_xml) == normalize_xml(xml)


def test_str0007_to_xml_omit_optional_fields() -> None:
    params = make_valid_str0007_params()
    del params['sender_type']
    del params['sender_document']
    del params['sender_name']
    del params['credit_contract_number']
    del params['transaction_id']
    del params['description']
    del params['scheduled_date']
    del params['scheduled_time']
    del params['priority']

    str0007 = STR0007.model_validate(params)
    xml = str0007.to_xml()

    expected_xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/SPB/STR0007.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>316801512509080000001</NUOp>
        </BCMSG>
        <SISMSG>
            <STR0007>
                <CodMsg>STR0007</CodMsg>
                <NumCtrlIF>31680151202509090425</NumCtrlIF>
                <ISPBIFDebtd>31680151</ISPBIFDebtd>
                <ISPBIFCredtd>60701190</ISPBIFCredtd>
                <AgCredtd>0001</AgCredtd>
                <TpCtCredtd>CD</TpCtCredtd>
                <CtCredtd>123456</CtCredtd>
                <TpPessoaCredtd>F</TpPessoaCredtd>
                <CNPJ_CPFCliCredtd>69327934075</CNPJ_CPFCliCredtd>
                <NomCliCredtd>Joe Doe</NomCliCredtd>
                <VlrLanc>100.0</VlrLanc>
                <FinlddIF>1</FinlddIF>
                <DtMovto>2025-09-08</DtMovto>
            </STR0007>
        </SISMSG>
    </DOC>
    """

    assert normalize_xml(expected_xml) == normalize_xml(xml)


def test_str0007_from_xml() -> None:
    xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/SPB/STR0007.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>316801512509080000001</NUOp>
        </BCMSG>
        <SISMSG>
            <STR0007>
                <CodMsg>STR0007</CodMsg>
                <NumCtrlIF>31680151202509090425</NumCtrlIF>
                <ISPBIFDebtd>31680151</ISPBIFDebtd>
                <TpPessoaRemet>J</TpPessoaRemet>
                <CNPJ_CPFRemet>56369416000136</CNPJ_CPFRemet>
                <NomRemet>ACME Inc</NomRemet>
                <ISPBIFCredtd>60701190</ISPBIFCredtd>
                <AgCredtd>0001</AgCredtd>
                <TpCtCredtd>CD</TpCtCredtd>
                <CtCredtd>123456</CtCredtd>
                <TpPessoaCredtd>F</TpPessoaCredtd>
                <CNPJ_CPFCliCredtd>69327934075</CNPJ_CPFCliCredtd>
                <NomCliCredtd>Joe Doe</NomCliCredtd>
                <NumCtrdCredtd>CTR123456789</NumCtrdCredtd>
                <VlrLanc>100.0</VlrLanc>
                <FinlddIF>1</FinlddIF>
                <CodIdentdTransf>0000000000000000000000001</CodIdentdTransf>
                <Hist>Payment for services</Hist>
                <DtAgendt>2025-09-09</DtAgendt>
                <HrAgendt>15:30:00</HrAgendt>
                <NivelPref>C</NivelPref>
                <DtMovto>2025-09-08</DtMovto>
            </STR0007>
        </SISMSG>
    </DOC>
    """

    str0007 = STR0007.from_xml(xml)
    assert isinstance(str0007, STR0007)
    assert str0007.amount == Decimal('100.0')
    assert str0007.creditor_account_number == '123456'
    assert str0007.creditor_account_type == AccountType.DEPOSIT
    assert str0007.creditor_institution_ispb == '60701190'
    assert str0007.creditor_branch == '0001'
    assert str0007.creditor_document == '69327934075'
    assert str0007.credit_contract_number == 'CTR123456789'
    assert str0007.creditor_name == 'Joe Doe'
    assert str0007.creditor_type == PersonType.INDIVIDUAL
    assert str0007.debtor_institution_ispb == '31680151'
    assert str0007.sender_document == '56369416000136'
    assert str0007.sender_name == 'ACME Inc'
    assert str0007.sender_type == PersonType.BUSINESS
    assert str0007.description == 'Payment for services'
    assert str0007.institution_control_number == '31680151202509090425'
    assert str0007.priority == Priority.MEDIUM
    assert str0007.purpose == InstitutionPurpose.FX_INTERBANK_MARKET
    assert str0007.scheduled_date == date(2025, 9, 9)
    assert str0007.scheduled_time == time(15, 30)
    assert str0007.settlement_date == date(2025, 9, 8)
    assert str0007.transaction_id == '0000000000000000000000001'


def test_str0007e_general_error_from_xml() -> None:
    xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/SPB/STR0007E.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>316801512509080000001</NUOp>
        </BCMSG>
        <SISMSG>
            <STR0007E CodErro="EGEN0050">
                <CodMsg>STR0007</CodMsg>
                <NumCtrlIF>31680151202509090425</NumCtrlIF>
                <ISPBIFDebtd>31680151</ISPBIFDebtd>
                <TpPessoaRemet>J</TpPessoaRemet>
                <CNPJ_CPFRemet>56369416000136</CNPJ_CPFRemet>
                <NomRemet>ACME Inc</NomRemet>
                <ISPBIFCredtd>60701190</ISPBIFCredtd>
                <AgCredtd>0001</AgCredtd>
                <TpCtCredtd>CD</TpCtCredtd>
                <CtCredtd>123456</CtCredtd>
                <TpPessoaCredtd>F</TpPessoaCredtd>
                <CNPJ_CPFCliCredtd>69327934075</CNPJ_CPFCliCredtd>
                <NomCliCredtd>Joe Doe</NomCliCredtd>
                <NumCtrdCredtd>CTR123456789</NumCtrdCredtd>
                <VlrLanc>100.0</VlrLanc>
                <FinlddIF>1</FinlddIF>
                <CodIdentdTransf>0000000000000000000000001</CodIdentdTransf>
                <Hist>Payment for services</Hist>
                <DtAgendt>2025-09-09</DtAgendt>
                <HrAgendt>15:30:00</HrAgendt>
                <NivelPref>C</NivelPref>
                <DtMovto>2025-09-08</DtMovto>
            </STR0007E>
        </SISMSG>
    </DOC>
    """

    str0007e = STR0007E.from_xml(xml)
    assert isinstance(str0007e, STR0007E)
    assert str0007e.amount == Decimal('100.0')
    assert str0007e.creditor_account_number == '123456'
    assert str0007e.creditor_account_type == AccountType.DEPOSIT
    assert str0007e.creditor_institution_ispb == '60701190'
    assert str0007e.creditor_branch == '0001'
    assert str0007e.creditor_document == '69327934075'
    assert str0007e.credit_contract_number == 'CTR123456789'
    assert str0007e.creditor_name == 'Joe Doe'
    assert str0007e.creditor_type == PersonType.INDIVIDUAL
    assert str0007e.debtor_institution_ispb == '31680151'
    assert str0007e.sender_document == '56369416000136'
    assert str0007e.sender_name == 'ACME Inc'
    assert str0007e.sender_type == PersonType.BUSINESS
    assert str0007e.description == 'Payment for services'
    assert str0007e.institution_control_number == '31680151202509090425'
    assert str0007e.priority == Priority.MEDIUM
    assert str0007e.purpose == InstitutionPurpose.FX_INTERBANK_MARKET
    assert str0007e.scheduled_date == date(2025, 9, 9)
    assert str0007e.scheduled_time == time(15, 30)
    assert str0007e.settlement_date == date(2025, 9, 8)
    assert str0007e.transaction_id == '0000000000000000000000001'
    assert str0007e.general_error_code == 'EGEN0050'


def test_str0007e_tag_error_from_xml() -> None:
    xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/SPB/STR0007E.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>316801512509080000001</NUOp>
        </BCMSG>
        <SISMSG>
            <STR0007E>
                <CodMsg>STR0007</CodMsg>
                <NumCtrlIF>31680151202509090425</NumCtrlIF>
                <ISPBIFDebtd CodErro="EGEN0051">31680151</ISPBIFDebtd>
                <TpPessoaRemet>J</TpPessoaRemet>
                <CNPJ_CPFRemet>56369416000136</CNPJ_CPFRemet>
                <NomRemet>ACME Inc</NomRemet>
                <ISPBIFCredtd>60701190</ISPBIFCredtd>
                <AgCredtd>0001</AgCredtd>
                <TpCtCredtd>CD</TpCtCredtd>
                <CtCredtd>123456</CtCredtd>
                <TpPessoaCredtd>F</TpPessoaCredtd>
                <CNPJ_CPFCliCredtd>69327934075</CNPJ_CPFCliCredtd>
                <NomCliCredtd>Joe Doe</NomCliCredtd>
                <NumCtrdCredtd>CTR123456789</NumCtrdCredtd>
                <VlrLanc>100.0</VlrLanc>
                <FinlddIF>1</FinlddIF>
                <CodIdentdTransf>0000000000000000000000001</CodIdentdTransf>
                <Hist>Payment for services</Hist>
                <DtAgendt>2025-09-09</DtAgendt>
                <HrAgendt>15:30:00</HrAgendt>
                <NivelPref>C</NivelPref>
                <DtMovto>2025-09-08</DtMovto>
            </STR0007E>
        </SISMSG>
    </DOC>
    """

    str0007e = STR0007E.from_xml(xml)
    assert isinstance(str0007e, STR0007E)
    assert str0007e.amount == Decimal('100.0')
    assert str0007e.creditor_account_number == '123456'
    assert str0007e.creditor_account_type == AccountType.DEPOSIT
    assert str0007e.creditor_institution_ispb == '60701190'
    assert str0007e.creditor_branch == '0001'
    assert str0007e.creditor_document == '69327934075'
    assert str0007e.credit_contract_number == 'CTR123456789'
    assert str0007e.creditor_name == 'Joe Doe'
    assert str0007e.creditor_type == PersonType.INDIVIDUAL
    assert str0007e.debtor_institution_ispb == '31680151'
    assert str0007e.sender_document == '56369416000136'
    assert str0007e.sender_name == 'ACME Inc'
    assert str0007e.sender_type == PersonType.BUSINESS
    assert str0007e.description == 'Payment for services'
    assert str0007e.institution_control_number == '31680151202509090425'
    assert str0007e.priority == Priority.MEDIUM
    assert str0007e.purpose == InstitutionPurpose.FX_INTERBANK_MARKET
    assert str0007e.scheduled_date == date(2025, 9, 9)
    assert str0007e.scheduled_time == time(15, 30)
    assert str0007e.settlement_date == date(2025, 9, 8)
    assert str0007e.transaction_id == '0000000000000000000000001'
    assert str0007e.debtor_institution_ispb_error_code == 'EGEN0051'


def test_str0007_from_xml_missing_optional_fields() -> None:
    xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/SPB/STR0007.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>316801512509080000001</NUOp>
        </BCMSG>
        <SISMSG>
            <STR0007>
                <CodMsg>STR0007</CodMsg>
                <NumCtrlIF>31680151202509090425</NumCtrlIF>
                <ISPBIFDebtd>31680151</ISPBIFDebtd>
                <ISPBIFCredtd>60701190</ISPBIFCredtd>
                <AgCredtd>0001</AgCredtd>
                <TpCtCredtd>CD</TpCtCredtd>
                <CtCredtd>123456</CtCredtd>
                <TpPessoaCredtd>F</TpPessoaCredtd>
                <CNPJ_CPFCliCredtd>69327934075</CNPJ_CPFCliCredtd>
                <NomCliCredtd>Joe Doe</NomCliCredtd>
                <VlrLanc>100.0</VlrLanc>
                <FinlddIF>1</FinlddIF>
                <DtMovto>2025-09-08</DtMovto>
            </STR0007>
        </SISMSG>
    </DOC>
    """

    str0007 = STR0007.from_xml(xml)
    assert isinstance(str0007, STR0007)
    assert str0007.amount == Decimal('100.0')
    assert str0007.creditor_account_number == '123456'
    assert str0007.creditor_account_type == AccountType.DEPOSIT
    assert str0007.creditor_institution_ispb == '60701190'
    assert str0007.creditor_branch == '0001'
    assert str0007.creditor_document == '69327934075'
    assert str0007.creditor_name == 'Joe Doe'
    assert str0007.creditor_type == PersonType.INDIVIDUAL
    assert str0007.debtor_institution_ispb == '31680151'
    assert str0007.sender_document is None
    assert str0007.sender_name is None
    assert str0007.sender_type is None
    assert str0007.description is None
    assert str0007.institution_control_number == '31680151202509090425'
    assert str0007.priority is None
    assert str0007.purpose == InstitutionPurpose.FX_INTERBANK_MARKET
    assert str0007.scheduled_date is None
    assert str0007.scheduled_time is None
    assert str0007.settlement_date == date(2025, 9, 8)
    assert str0007.transaction_id is None
    assert str0007.credit_contract_number is None


def test_str0007_roundtrip() -> None:
    params = make_valid_str0007_params()
    str0007 = STR0007.model_validate(params)
    xml = str0007.to_xml()
    str0007_from_xml = STR0007.from_xml(xml)
    assert str0007 == str0007_from_xml


def test_str0007_from_xml_missing_required_fields() -> None:
    xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/SPB/STR0007.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>316801512509080000001</NUOp>
        </BCMSG>
        <SISMSG>
            <STR0007>
                <CodMsg>STR0007</CodMsg>
            </STR0007>
        </SISMSG>
    </DOC>
    """

    with pytest.raises(ValidationError) as exc:
        STR0007.from_xml(xml)
    missing_fields = extract_missing_fields(exc.value)
    assert missing_fields == {
        'amount',
        'creditor_type',
        'settlement_date',
        'debtor_institution_ispb',
        'creditor_account_type',
        'purpose',
        'creditor_document',
        'institution_control_number',
        'creditor_institution_ispb',
        'creditor_name',
    }


def test_str0007r1_valid_model() -> None:
    params = make_valid_str0007r1_params()
    str0007r1 = STR0007R1.model_validate(params)
    assert isinstance(str0007r1, STR0007R1)
    assert str0007r1.debtor_institution_ispb == '31680151'
    assert str0007r1.from_ispb == '31680151'
    assert str0007r1.institution_control_number == '31680151202509090425'
    assert str0007r1.message_code == 'STR0007R1'
    assert str0007r1.operation_number == '316801512509080000001'
    assert str0007r1.settlement_date == date(2025, 9, 8)
    assert str0007r1.settlement_timestamp == datetime(2025, 11, 20, 15, 30, tzinfo=UTC)
    assert str0007r1.str_control_number == 'STR20250101000000001'
    assert str0007r1.str_settlement_status == StrSettlementStatus.EFFECTIVE
    assert str0007r1.to_ispb == '00038166'
    assert str0007r1.system_domain == 'SPB01'


def test_str0007r1_missing_required_fields() -> None:
    with pytest.raises(ValidationError) as exc:
        STR0007R1.model_validate({})
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


def test_str0007r1_to_xml() -> None:
    params = make_valid_str0007r1_params()
    str0007r1 = STR0007R1.model_validate(params)
    xml = str0007r1.to_xml()

    expected_xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/SPB/STR0007.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>316801512509080000001</NUOp>
        </BCMSG>
        <SISMSG>
            <STR0007R1>
                <CodMsg>STR0007R1</CodMsg>
                <NumCtrlIF>31680151202509090425</NumCtrlIF>
                <ISPBIFDebtd>31680151</ISPBIFDebtd>
                <NumCtrlSTR>STR20250101000000001</NumCtrlSTR>
                <SitLancSTR>1</SitLancSTR>
                <DtHrSit>2025-11-20 15:30:00+00:00</DtHrSit>
                <DtMovto>2025-09-08</DtMovto>
            </STR0007R1>
        </SISMSG>
    </DOC>
    """

    assert normalize_xml(expected_xml) == normalize_xml(xml)


def test_str0007r1_from_xml() -> None:
    xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/SPB/STR0007.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>316801512509080000001</NUOp>
        </BCMSG>
        <SISMSG>
            <STR0007R1>
                <CodMsg>STR0007R1</CodMsg>
                <NumCtrlIF>31680151202509090425</NumCtrlIF>
                <ISPBIFDebtd>31680151</ISPBIFDebtd>
                <NumCtrlSTR>STR20250101000000001</NumCtrlSTR>
                <SitLancSTR>1</SitLancSTR>
                <DtHrSit>2025-11-20 15:30:00+00:00</DtHrSit>
                <DtMovto>2025-09-08</DtMovto>
            </STR0007R1>
        </SISMSG>
    </DOC>
    """
    str0007r1 = STR0007R1.from_xml(xml)
    assert isinstance(str0007r1, STR0007R1)
    assert str0007r1.debtor_institution_ispb == '31680151'
    assert str0007r1.from_ispb == '31680151'
    assert str0007r1.institution_control_number == '31680151202509090425'
    assert str0007r1.message_code == 'STR0007R1'
    assert str0007r1.operation_number == '316801512509080000001'
    assert str0007r1.settlement_date == date(2025, 9, 8)
    assert str0007r1.settlement_timestamp == datetime(2025, 11, 20, 15, 30, tzinfo=UTC)
    assert str0007r1.str_control_number == 'STR20250101000000001'
    assert str0007r1.str_settlement_status == StrSettlementStatus.EFFECTIVE
    assert str0007r1.to_ispb == '00038166'
    assert str0007r1.system_domain == 'SPB01'


def test_str0007r1_roundtrip() -> None:
    params = make_valid_str0007r1_params()
    str0007r1 = STR0007R1.model_validate(params)
    xml = str0007r1.to_xml()
    str0007r1_from_xml = STR0007R1.from_xml(xml)
    assert str0007r1 == str0007r1_from_xml


def test_str0007r1_from_xml_missing_required_fields() -> None:
    xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/SPB/STR0007.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>316801512509080000001</NUOp>
        </BCMSG>
        <SISMSG>
            <STR0007R1>
                <CodMsg>STR0007R1</CodMsg>
            </STR0007R1>
        </SISMSG>
    </DOC>
    """

    with pytest.raises(ValidationError) as exc:
        STR0007R1.from_xml(xml)
    missing_fields = extract_missing_fields(exc.value)
    assert missing_fields == {
        'settlement_date',
        'debtor_institution_ispb',
        'str_settlement_status',
        'str_control_number',
        'institution_control_number',
        'settlement_timestamp',
    }


def test_str0007r2_model_valid() -> None:
    params = make_valid_str0007r2_params()
    message = STR0007R2.model_validate(params)
    assert message.amount == Decimal('100.00')
    assert message.creditor_account_number == '123456'
    assert message.creditor_account_type == AccountType.DEPOSIT
    assert message.creditor_institution_ispb == '60701190'
    assert message.creditor_branch == '0001'
    assert message.creditor_document == '69327934075'
    assert message.credit_contract_number == 'CTR123456789'
    assert message.creditor_name == 'Joe Doe'
    assert message.creditor_type == PersonType.INDIVIDUAL
    assert message.debtor_institution_ispb == '31680151'
    assert message.sender_document == '56369416000136'
    assert message.sender_name == 'ACME Inc'
    assert message.sender_type == PersonType.BUSINESS
    assert message.description == 'Payment for services'
    assert message.str_control_number == 'STR20250101000000001'
    assert message.purpose == InstitutionPurpose.FX_INTERBANK_MARKET
    assert message.settlement_date == date(2025, 9, 8)
    assert message.transaction_id == '0000000000000000000000001'
    assert message.vendor_timestamp == datetime(2025, 11, 20, 15, 30, tzinfo=UTC)


def test_str0007r2_missing_required_fields() -> None:
    with pytest.raises(ValidationError) as exc:
        STR0007R2.model_validate({})
    missing_fields = extract_missing_fields(exc.value)
    assert missing_fields == {
        'operation_number',
        'creditor_name',
        'system_domain',
        'debtor_institution_ispb',
        'amount',
        'settlement_date',
        'creditor_document',
        'from_ispb',
        'vendor_timestamp',
        'creditor_institution_ispb',
        'creditor_type',
        'purpose',
        'str_control_number',
        'creditor_account_type',
        'to_ispb',
    }


def test_str0007r2_business_rules_invalid_documents() -> None:
    params = make_valid_str0007r2_params()
    params['sender_type'] = 'INDIVIDUAL'
    params['sender_document'] = '56369416000136'
    params['creditor_type'] = 'BUSINESS'
    params['creditor_document'] = '69327934075'

    with pytest.raises(ValidationError) as exc:
        STR0007R2.model_validate(params)
    error_message = str(exc.value)
    assert 'Invalid CPF for sender_type INDIVIDUAL' in error_message
    assert 'Invalid CNPJ for creditor_type BUSINESS' in error_message


def test_str0007r2_business_rules_missing_description_for_other_purpose() -> None:
    params = make_valid_str0007r2_params()
    params['purpose'] = 'OTHERS'
    del params['description']

    with pytest.raises(ValidationError) as exc:
        STR0007R2.model_validate(params)
    error_message = str(exc.value)
    assert 'description is required when purpose is OTHERS' in error_message


def test_str0007r2_business_rules_missing_creditor_branch_for_creditor_account_type_is_not_payment() -> None:
    params = make_valid_str0007r2_params()
    params['creditor_account_type'] = 'CURRENT'
    del params['creditor_branch']

    with pytest.raises(ValidationError) as exc:
        STR0007R2.model_validate(params)
    error_message = str(exc.value)
    assert 'creditor_branch is required when creditor_account_type is not PAYMENT' in error_message


def test_str0007r2_business_rules_missing_creditor_payment_account_number_for_creditor_account_type_is_payment() -> (
    None
):
    params = make_valid_str0007r2_params()
    params['creditor_account_type'] = 'PAYMENT'

    with pytest.raises(ValidationError) as exc:
        STR0007R2.model_validate(params)
    error_message = str(exc.value)
    assert 'creditor_payment_account_number is required when creditor_account_type is PAYMENT' in error_message


def test_str0007r2_business_rules_missing_creditor_account_number_for_creditor_account_type_is_not_payment() -> None:
    params = make_valid_str0007r2_params()
    params['creditor_account_type'] = 'CURRENT'
    del params['creditor_account_number']

    with pytest.raises(ValidationError) as exc:
        STR0007R2.model_validate(params)
    error_message = str(exc.value)
    assert 'creditor_account_number is required when creditor_account_type is not PAYMENT' in error_message


def test_str0007r2_to_xml() -> None:
    params = make_valid_str0007r2_params()
    str0007 = STR0007R2.model_validate(params)
    xml = str0007.to_xml()

    expected_xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/SPB/STR0007.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>316801512509080000001</NUOp>
        </BCMSG>
        <SISMSG>
            <STR0007R2>
                <CodMsg>STR0007R2</CodMsg>
                <NumCtrlSTR>STR20250101000000001</NumCtrlSTR>
                <DtHrBC>2025-11-20 15:30:00+00:00</DtHrBC>
                <ISPBIFDebtd>31680151</ISPBIFDebtd>
                <TpPessoaRemet>J</TpPessoaRemet>
                <CNPJ_CPFRemet>56369416000136</CNPJ_CPFRemet>
                <NomRemet>ACME Inc</NomRemet>
                <ISPBIFCredtd>60701190</ISPBIFCredtd>
                <AgCredtd>0001</AgCredtd>
                <TpCtCredtd>CD</TpCtCredtd>
                <CtCredtd>123456</CtCredtd>
                <TpPessoaCredtd>F</TpPessoaCredtd>
                <CNPJ_CPFCliCredtd>69327934075</CNPJ_CPFCliCredtd>
                <NomCliCredtd>Joe Doe</NomCliCredtd>
                <NumCtrdCredtd>CTR123456789</NumCtrdCredtd>
                <VlrLanc>100.0</VlrLanc>
                <FinlddIF>1</FinlddIF>
                <CodIdentdTransf>0000000000000000000000001</CodIdentdTransf>
                <Hist>Payment for services</Hist>
                <DtMovto>2025-09-08</DtMovto>
            </STR0007R2>
        </SISMSG>
    </DOC>
    """

    assert normalize_xml(expected_xml) == normalize_xml(xml)


def test_str0007r2_to_xml_omit_optional_fields() -> None:
    params = make_valid_str0007r2_params()
    del params['sender_type']
    del params['sender_document']
    del params['sender_name']
    del params['credit_contract_number']
    del params['description']

    str0007 = STR0007R2.model_validate(params)
    xml = str0007.to_xml()

    expected_xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/SPB/STR0007.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>316801512509080000001</NUOp>
        </BCMSG>
        <SISMSG>
            <STR0007R2>
                <CodMsg>STR0007R2</CodMsg>
                <NumCtrlSTR>STR20250101000000001</NumCtrlSTR>
                <DtHrBC>2025-11-20 15:30:00+00:00</DtHrBC>
                <ISPBIFDebtd>31680151</ISPBIFDebtd>
                <ISPBIFCredtd>60701190</ISPBIFCredtd>
                <AgCredtd>0001</AgCredtd>
                <TpCtCredtd>CD</TpCtCredtd>
                <CtCredtd>123456</CtCredtd>
                <TpPessoaCredtd>F</TpPessoaCredtd>
                <CNPJ_CPFCliCredtd>69327934075</CNPJ_CPFCliCredtd>
                <NomCliCredtd>Joe Doe</NomCliCredtd>
                <VlrLanc>100.0</VlrLanc>
                <FinlddIF>1</FinlddIF>
                <CodIdentdTransf>0000000000000000000000001</CodIdentdTransf>
                <DtMovto>2025-09-08</DtMovto>
            </STR0007R2>
        </SISMSG>
    </DOC>
    """

    assert normalize_xml(expected_xml) == normalize_xml(xml)


def test_str0007r2_from_xml() -> None:
    xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/SPB/STR0007.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>316801512509080000001</NUOp>
        </BCMSG>
        <SISMSG>
            <STR0007R2>
                <CodMsg>STR0007R2</CodMsg>
                <NumCtrlSTR>STR20250101000000001</NumCtrlSTR>
                <DtHrBC>2025-11-20 15:30:00+00:00</DtHrBC>
                <ISPBIFDebtd>31680151</ISPBIFDebtd>
                <TpPessoaRemet>J</TpPessoaRemet>
                <CNPJ_CPFRemet>56369416000136</CNPJ_CPFRemet>
                <NomRemet>ACME Inc</NomRemet>
                <ISPBIFCredtd>60701190</ISPBIFCredtd>
                <AgCredtd>0001</AgCredtd>
                <TpCtCredtd>CD</TpCtCredtd>
                <CtCredtd>123456</CtCredtd>
                <TpPessoaCredtd>F</TpPessoaCredtd>
                <CNPJ_CPFCliCredtd>69327934075</CNPJ_CPFCliCredtd>
                <NomCliCredtd>Joe Doe</NomCliCredtd>
                <NumCtrdCredtd>CTR123456789</NumCtrdCredtd>
                <VlrLanc>100.0</VlrLanc>
                <FinlddIF>1</FinlddIF>
                <CodIdentdTransf>0000000000000000000000001</CodIdentdTransf>
                <Hist>Payment for services</Hist>
                <DtMovto>2025-09-08</DtMovto>
            </STR0007R2>
        </SISMSG>
    </DOC>
    """

    str0007 = STR0007R2.from_xml(xml)
    assert isinstance(str0007, STR0007R2)
    assert str0007.amount == Decimal('100.0')
    assert str0007.creditor_account_number == '123456'
    assert str0007.creditor_account_type == AccountType.DEPOSIT
    assert str0007.creditor_institution_ispb == '60701190'
    assert str0007.creditor_branch == '0001'
    assert str0007.creditor_document == '69327934075'
    assert str0007.credit_contract_number == 'CTR123456789'
    assert str0007.creditor_name == 'Joe Doe'
    assert str0007.creditor_type == PersonType.INDIVIDUAL
    assert str0007.debtor_institution_ispb == '31680151'
    assert str0007.sender_document == '56369416000136'
    assert str0007.sender_name == 'ACME Inc'
    assert str0007.sender_type == PersonType.BUSINESS
    assert str0007.description == 'Payment for services'
    assert str0007.str_control_number == 'STR20250101000000001'
    assert str0007.purpose == InstitutionPurpose.FX_INTERBANK_MARKET
    assert str0007.settlement_date == date(2025, 9, 8)
    assert str0007.transaction_id == '0000000000000000000000001'
    assert str0007.vendor_timestamp == datetime(2025, 11, 20, 15, 30, tzinfo=UTC)


def test_str0007r2_from_xml_missing_optional_fields() -> None:
    xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/SPB/STR0007.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>316801512509080000001</NUOp>
        </BCMSG>
        <SISMSG>
            <STR0007R2>
                <CodMsg>STR0007R2</CodMsg>
                <NumCtrlSTR>STR20250101000000001</NumCtrlSTR>
                <DtHrBC>2025-11-20 15:30:00+00:00</DtHrBC>
                <ISPBIFDebtd>31680151</ISPBIFDebtd>
                <ISPBIFCredtd>60701190</ISPBIFCredtd>
                <AgCredtd>0001</AgCredtd>
                <TpCtCredtd>CD</TpCtCredtd>
                <CtCredtd>123456</CtCredtd>
                <TpPessoaCredtd>F</TpPessoaCredtd>
                <CNPJ_CPFCliCredtd>69327934075</CNPJ_CPFCliCredtd>
                <NomCliCredtd>Joe Doe</NomCliCredtd>
                <VlrLanc>100.0</VlrLanc>
                <FinlddIF>1</FinlddIF>
                <DtMovto>2025-09-08</DtMovto>
            </STR0007R2>
        </SISMSG>
    </DOC>
    """

    str0007 = STR0007R2.from_xml(xml)
    assert isinstance(str0007, STR0007R2)
    assert str0007.amount == Decimal('100.0')
    assert str0007.creditor_account_number == '123456'
    assert str0007.creditor_account_type == AccountType.DEPOSIT
    assert str0007.creditor_institution_ispb == '60701190'
    assert str0007.creditor_branch == '0001'
    assert str0007.creditor_document == '69327934075'
    assert str0007.credit_contract_number is None
    assert str0007.creditor_name == 'Joe Doe'
    assert str0007.creditor_type == PersonType.INDIVIDUAL
    assert str0007.debtor_institution_ispb == '31680151'
    assert str0007.sender_document is None
    assert str0007.sender_name is None
    assert str0007.sender_type is None
    assert str0007.description is None
    assert str0007.str_control_number == 'STR20250101000000001'
    assert str0007.purpose == InstitutionPurpose.FX_INTERBANK_MARKET
    assert str0007.settlement_date == date(2025, 9, 8)
    assert str0007.transaction_id is None
    assert str0007.vendor_timestamp == datetime(2025, 11, 20, 15, 30, tzinfo=UTC)


def test_str0007r2_roundtrip() -> None:
    params = make_valid_str0007r2_params()
    str0007r2 = STR0007R2.model_validate(params)
    xml = str0007r2.to_xml()
    str0007r2_from_xml = STR0007R2.from_xml(xml)
    assert str0007r2 == str0007r2_from_xml


def test_str0007r2_from_xml_missing_required_fields() -> None:
    xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/SPB/STR0007.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>316801512509080000001</NUOp>
        </BCMSG>
        <SISMSG>
            <STR0007R2>
                <CodMsg>STR0007R2</CodMsg>
            </STR0007R2>
        </SISMSG>
    </DOC>
    """

    with pytest.raises(ValidationError) as exc:
        STR0007R2.from_xml(xml)
    missing_fields = extract_missing_fields(exc.value)
    assert missing_fields == {
        'debtor_institution_ispb',
        'creditor_document',
        'creditor_name',
        'amount',
        'creditor_type',
        'purpose',
        'creditor_institution_ispb',
        'vendor_timestamp',
        'creditor_account_type',
        'str_control_number',
        'settlement_date',
    }
