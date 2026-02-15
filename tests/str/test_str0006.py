from datetime import date, datetime, time
from decimal import Decimal
from typing import Any

import pytest
from pydantic import ValidationError

from sfn_messages.core.types import AccountType, CustomerPurpose, PersonType, Priority, StrSettlementStatus
from sfn_messages.str.str0006 import STR0006, STR0006R1, STR0006R2
from tests.conftest import extract_missing_fields, normalize_xml


def make_valid_str0006_params() -> dict[str, Any]:
    return {
        'amount': 100.00,
        'creditor_account_number': '123456',
        'creditor_institution_ispb': '60701190',
        'creditor_branch': '0001',
        'recipient_document': '69327934075',
        'recipient_name': 'Joe Doe',
        'recipient_type': 'INDIVIDUAL',
        'debtor_account_number': '654321',
        'debtor_account_type': 'CURRENT',
        'debtor_institution_ispb': '31680151',
        'debtor_branch': '0002',
        'sender_document': '56369416000136',
        'sender_name': 'ACME Inc',
        'sender_type': 'BUSINESS',
        'description': 'Payment for services',
        'from_ispb': '31680151',
        'institution_control_number': '31680151202509090425',
        'operation_number': '31680151250908000000001',
        'priority': 'MEDIUM',
        'purpose': 'CREDIT_IN_ACCOUNT',
        'scheduled_date': '2025-09-09',
        'scheduled_time': '15:30:00',
        'settlement_date': '2025-09-08',
        'system_domain': 'SPB01',
        'to_ispb': '00038166',
        'credit_contract_number': '1234567890',
        'transaction_id': '0000000000000000000000001',
    }


def make_valid_str0006r1_params() -> dict[str, Any]:
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


def make_valid_str0006r2_params() -> dict[str, Any]:
    return {
        'amount': 100.00,
        'creditor_account_number': '123456',
        'creditor_institution_ispb': '60701190',
        'creditor_branch': '0001',
        'recipient_document': '69327934075',
        'recipient_name': 'Joe Doe',
        'recipient_type': 'INDIVIDUAL',
        'debtor_account_number': '654321',
        'debtor_account_type': 'CURRENT',
        'debtor_institution_ispb': '31680151',
        'debtor_branch': '0002',
        'sender_document': '56369416000136',
        'sender_name': 'ACME Inc',
        'sender_type': 'BUSINESS',
        'description': 'Payment for services',
        'from_ispb': '31680151',
        'operation_number': '31680151250908000000001',
        'purpose': 'CREDIT_IN_ACCOUNT',
        'settlement_date': '2025-09-08',
        'system_domain': 'SPB01',
        'to_ispb': '00038166',
        'transaction_id': '0000000000000000000000001',
        'vendor_timestamp': '2025-11-20T15:30:00',
        'credit_contract_number': '1234567890',
        'str_control_number': 'STR20250101000000001',
    }


def test_str0006_valid_model() -> None:
    params = make_valid_str0006_params()
    str0006 = STR0006.model_validate(params)
    assert isinstance(str0006, STR0006)
    assert str0006.amount == Decimal('100.00')
    assert str0006.creditor_account_number == '123456'
    assert str0006.creditor_institution_ispb == '60701190'
    assert str0006.creditor_branch == '0001'
    assert str0006.recipient_document == '69327934075'
    assert str0006.recipient_name == 'Joe Doe'
    assert str0006.recipient_type == PersonType.INDIVIDUAL
    assert str0006.debtor_account_number == '654321'
    assert str0006.debtor_account_type == AccountType.CURRENT
    assert str0006.debtor_branch == '0002'
    assert str0006.sender_document == '56369416000136'
    assert str0006.debtor_institution_ispb == '31680151'
    assert str0006.sender_name == 'ACME Inc'
    assert str0006.debtor_payment_account_number is None
    assert str0006.sender_type == PersonType.BUSINESS
    assert str0006.description == 'Payment for services'
    assert str0006.from_ispb == '31680151'
    assert str0006.institution_control_number == '31680151202509090425'
    assert str0006.operation_number == '31680151250908000000001'
    assert str0006.priority == Priority.MEDIUM
    assert str0006.purpose == CustomerPurpose.CREDIT_IN_ACCOUNT
    assert str0006.scheduled_date == date(2025, 9, 9)
    assert str0006.scheduled_time == time(15, 30)
    assert str0006.settlement_date == date(2025, 9, 8)
    assert str0006.system_domain == 'SPB01'
    assert str0006.to_ispb == '00038166'
    assert str0006.credit_contract_number == '1234567890'
    assert str0006.transaction_id == '0000000000000000000000001'


def test_str0006r1_valid_model() -> None:
    params = make_valid_str0006r1_params()
    str0006r1 = STR0006R1.model_validate(params)
    assert isinstance(str0006r1, STR0006R1)
    assert str0006r1.institution_control_number == '31680151202509090425'
    assert str0006r1.from_ispb == '31680151'
    assert str0006r1.debtor_institution_ispb == '31680151'
    assert str0006r1.str_control_number == 'STR20250101000000001'
    assert str0006r1.str_settlement_status == StrSettlementStatus.EFFECTIVE
    assert str0006r1.settlement_timestamp == datetime(2025, 11, 20, 15, 30)
    assert str0006r1.settlement_date == date(2025, 9, 8)
    assert str0006r1.operation_number == '31680151250908000000001'
    assert str0006r1.to_ispb == '00038166'
    assert str0006r1.system_domain == 'SPB01'


def test_str0006r2_valid_model() -> None:
    params = make_valid_str0006r2_params()
    str0006r2 = STR0006R2.model_validate(params)
    assert isinstance(str0006r2, STR0006R2)
    assert str0006r2.amount == Decimal('100.00')
    assert str0006r2.creditor_account_number == '123456'
    assert str0006r2.creditor_institution_ispb == '60701190'
    assert str0006r2.creditor_branch == '0001'
    assert str0006r2.recipient_document == '69327934075'
    assert str0006r2.recipient_name == 'Joe Doe'
    assert str0006r2.recipient_type == PersonType.INDIVIDUAL
    assert str0006r2.debtor_account_number == '654321'
    assert str0006r2.debtor_account_type == AccountType.CURRENT
    assert str0006r2.debtor_branch == '0002'
    assert str0006r2.sender_document == '56369416000136'
    assert str0006r2.debtor_institution_ispb == '31680151'
    assert str0006r2.sender_name == 'ACME Inc'
    assert str0006r2.debtor_payment_account_number is None
    assert str0006r2.sender_type == PersonType.BUSINESS
    assert str0006r2.description == 'Payment for services'
    assert str0006r2.from_ispb == '31680151'
    assert str0006r2.operation_number == '31680151250908000000001'
    assert str0006r2.purpose == CustomerPurpose.CREDIT_IN_ACCOUNT
    assert str0006r2.settlement_date == date(2025, 9, 8)
    assert str0006r2.system_domain == 'SPB01'
    assert str0006r2.to_ispb == '00038166'
    assert str0006r2.transaction_id == '0000000000000000000000001'
    assert str0006r2.vendor_timestamp == datetime(2025, 11, 20, 15, 30)
    assert str0006r2.credit_contract_number == '1234567890'
    assert str0006r2.str_control_number == 'STR20250101000000001'


def test_str0006_missing_required_fields() -> None:
    with pytest.raises(ValidationError) as exc:
        STR0006.model_validate({})
    missing_fields = extract_missing_fields(exc.value)
    assert missing_fields == {
        'debtor_institution_ispb',
        'to_ispb',
        'purpose',
        'settlement_date',
        'amount',
        'creditor_institution_ispb',
        'debtor_account_type',
        'institution_control_number',
        'from_ispb',
        'operation_number',
        'system_domain',
    }


def test_str0006r1_missing_required_fields() -> None:
    with pytest.raises(ValidationError) as exc:
        STR0006R1.model_validate({})
    missing_fields = extract_missing_fields(exc.value)
    assert missing_fields == {
        'institution_control_number',
        'from_ispb',
        'debtor_institution_ispb',
        'str_control_number',
        'str_settlement_status',
        'settlement_timestamp',
        'settlement_date',
        'operation_number',
        'to_ispb',
        'system_domain',
    }


def test_str0006r2_missing_required_fields() -> None:
    with pytest.raises(ValidationError) as exc:
        STR0006R2.model_validate({})
    missing_fields = extract_missing_fields(exc.value)
    assert missing_fields == {
        'amount',
        'creditor_institution_ispb',
        'debtor_account_type',
        'debtor_institution_ispb',
        'from_ispb',
        'operation_number',
        'purpose',
        'settlement_date',
        'str_control_number',
        'system_domain',
        'to_ispb',
        'vendor_timestamp',
    }


def test_str0006_business_rules_invalid_documents() -> None:
    params = make_valid_str0006_params()
    params['sender_type'] = 'INDIVIDUAL'
    params['sender_document'] = '56369416000136'
    params['recipient_type'] = 'BUSINESS'
    params['recipient_document'] = '69327934075'

    with pytest.raises(ValidationError) as exc:
        STR0006.model_validate(params)
    error_message = str(exc.value)
    assert 'Invalid CPF for sender_type INDIVIDUAL' in error_message
    assert 'Invalid CNPJ for recipient_type BUSINESS' in error_message


def test_str0006_business_rules_missing_description_for_other_purpose() -> None:
    params = make_valid_str0006_params()
    params['purpose'] = 'OTHERS'
    del params['description']

    with pytest.raises(ValidationError) as exc:
        STR0006.model_validate(params)
    error_message = str(exc.value)
    assert 'description is required when purpose is OTHERS' in error_message


def test_str0006_business_rules_missing_debtor_branch_for_debtor_account_type_is_not_payment() -> None:
    params = make_valid_str0006_params()
    params['debtor_account_type'] = 'CURRENT'
    del params['debtor_branch']

    with pytest.raises(ValidationError) as exc:
        STR0006.model_validate(params)
    error_message = str(exc.value)
    assert 'debtor_branch is required when debtor_account_type is not PAYMENT' in error_message


def test_str0006_business_rules_missing_debtor_payment_account_number_for_debtor_account_type_is_payment() -> None:
    params = make_valid_str0006_params()
    params['debtor_account_type'] = 'PAYMENT'

    with pytest.raises(ValidationError) as exc:
        STR0006.model_validate(params)
    error_message = str(exc.value)
    assert 'debtor_payment_account_number is required when debtor_account_type is PAYMENT' in error_message


def test_str0006_business_rules_missing_debtor_account_number_for_debtor_account_type_is_not_payment() -> None:
    params = make_valid_str0006_params()
    params['debtor_account_type'] = 'CURRENT'
    del params['debtor_account_number']

    with pytest.raises(ValidationError) as exc:
        STR0006.model_validate(params)
    error_message = str(exc.value)
    assert 'debtor_account_number is required when debtor_account_type is not PAYMENT' in error_message


def test_str0006_to_xml() -> None:
    params = make_valid_str0006_params()
    str0006 = STR0006.model_validate(params)
    xml = str0006.to_xml()

    expected_xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/SPB/STR0006.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>31680151250908000000001</NUOp>
        </BCMSG>
        <SISMSG>
            <STR0006>
                <CodMsg>STR0006</CodMsg>
                <NumCtrlIF>31680151202509090425</NumCtrlIF>
                <ISPBIFDebtd>31680151</ISPBIFDebtd>
                <AgDebtd>0002</AgDebtd>
                <Grupo_STR0006_CtDebtd>
                    <TpCtDebtd>CC</TpCtDebtd>
                    <CtDebtd>654321</CtDebtd>
                </Grupo_STR0006_CtDebtd>
                <TpPessoaDebtd_Remet>J</TpPessoaDebtd_Remet>
                <CNPJ_CPFCliDebtd_Remet>56369416000136</CNPJ_CPFCliDebtd_Remet>
                <NomCliDebtd_Remet>ACME Inc</NomCliDebtd_Remet>
                <ISPBIFCredtd>60701190</ISPBIFCredtd>
                <AgCredtd>0001</AgCredtd>
                <CtCredtd>123456</CtCredtd>
                <TpPessoaDestinatario>F</TpPessoaDestinatario>
                <CNPJ_CPFDestinatario>69327934075</CNPJ_CPFDestinatario>
                <NomDestinatario>Joe Doe</NomDestinatario>
                <NumContrtoOpCred>1234567890</NumContrtoOpCred>
                <VlrLanc>100.0</VlrLanc>
                <FinlddCli>10</FinlddCli>
                <CodIdentdTransf>0000000000000000000000001</CodIdentdTransf>
                <Hist>Payment for services</Hist>
                <DtAgendt>2025-09-09</DtAgendt>
                <HrAgendt>15:30:00</HrAgendt>
                <NivelPref>C</NivelPref>
                <DtMovto>2025-09-08</DtMovto>
            </STR0006>
        </SISMSG>
    </DOC>
    """

    assert normalize_xml(expected_xml) == normalize_xml(xml)


def test_str0006_to_xml_omit_optional_fields() -> None:
    params = make_valid_str0006_params()
    del params['description']
    del params['scheduled_date']
    del params['scheduled_time']
    del params['priority']
    del params['transaction_id']
    del params['credit_contract_number']

    str0006 = STR0006.model_validate(params)
    xml = str0006.to_xml()

    expected_xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/SPB/STR0006.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>31680151250908000000001</NUOp>
        </BCMSG>
        <SISMSG>
            <STR0006>
                <CodMsg>STR0006</CodMsg>
                <NumCtrlIF>31680151202509090425</NumCtrlIF>
                <ISPBIFDebtd>31680151</ISPBIFDebtd>
                <AgDebtd>0002</AgDebtd>
                <Grupo_STR0006_CtDebtd>
                    <TpCtDebtd>CC</TpCtDebtd>
                    <CtDebtd>654321</CtDebtd>
                </Grupo_STR0006_CtDebtd>
                <TpPessoaDebtd_Remet>J</TpPessoaDebtd_Remet>
                <CNPJ_CPFCliDebtd_Remet>56369416000136</CNPJ_CPFCliDebtd_Remet>
                <NomCliDebtd_Remet>ACME Inc</NomCliDebtd_Remet>
                <ISPBIFCredtd>60701190</ISPBIFCredtd>
                <AgCredtd>0001</AgCredtd>
                <CtCredtd>123456</CtCredtd>
                <TpPessoaDestinatario>F</TpPessoaDestinatario>
                <CNPJ_CPFDestinatario>69327934075</CNPJ_CPFDestinatario>
                <NomDestinatario>Joe Doe</NomDestinatario>
                <VlrLanc>100.0</VlrLanc>
                <FinlddCli>10</FinlddCli>
                <DtMovto>2025-09-08</DtMovto>
            </STR0006>
        </SISMSG>
    </DOC>
    """

    assert normalize_xml(expected_xml) == normalize_xml(xml)


def test_str0006_from_xml() -> None:
    xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/SPB/STR0006.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>31680151250908000000001</NUOp>
        </BCMSG>
        <SISMSG>
            <STR0006>
                <CodMsg>STR0006</CodMsg>
                <NumCtrlIF>31680151202509090425</NumCtrlIF>
                <ISPBIFDebtd>31680151</ISPBIFDebtd>
                <AgDebtd>0002</AgDebtd>
                <Grupo_STR0006_CtDebtd>
                    <TpCtDebtd>CC</TpCtDebtd>
                    <CtDebtd>654321</CtDebtd>
                </Grupo_STR0006_CtDebtd>
                <TpPessoaDebtd_Remet>J</TpPessoaDebtd_Remet>
                <CNPJ_CPFCliDebtd_Remet>56369416000136</CNPJ_CPFCliDebtd_Remet>
                <NomCliDebtd_Remet>ACME Inc</NomCliDebtd_Remet>
                <ISPBIFCredtd>60701190</ISPBIFCredtd>
                <AgCredtd>0001</AgCredtd>
                <CtCredtd>123456</CtCredtd>
                <TpPessoaDestinatario>F</TpPessoaDestinatario>
                <CNPJ_CPFDestinatario>69327934075</CNPJ_CPFDestinatario>
                <NomDestinatario>Joe Doe</NomDestinatario>
                <NumContrtoOpCred>1234567890</NumContrtoOpCred>
                <VlrLanc>100.0</VlrLanc>
                <FinlddCli>10</FinlddCli>
                <CodIdentdTransf>0000000000000000000000001</CodIdentdTransf>
                <Hist>Payment for services</Hist>
                <DtAgendt>2025-09-09</DtAgendt>
                <HrAgendt>15:30:00</HrAgendt>
                <NivelPref>C</NivelPref>
                <DtMovto>2025-09-08</DtMovto>
            </STR0006>
        </SISMSG>
    </DOC>
    """

    str0006 = STR0006.from_xml(xml)
    assert isinstance(str0006, STR0006)
    assert str0006.amount == Decimal('100.0')
    assert str0006.creditor_account_number == '123456'
    assert str0006.creditor_institution_ispb == '60701190'
    assert str0006.creditor_branch == '0001'
    assert str0006.recipient_document == '69327934075'
    assert str0006.recipient_name == 'Joe Doe'
    assert str0006.recipient_type == PersonType.INDIVIDUAL
    assert str0006.debtor_account_number == '654321'
    assert str0006.debtor_account_type == AccountType.CURRENT
    assert str0006.debtor_branch == '0002'
    assert str0006.sender_document == '56369416000136'
    assert str0006.debtor_institution_ispb == '31680151'
    assert str0006.sender_name == 'ACME Inc'
    assert str0006.debtor_payment_account_number is None
    assert str0006.sender_type == PersonType.BUSINESS
    assert str0006.description == 'Payment for services'
    assert str0006.from_ispb == '31680151'
    assert str0006.institution_control_number == '31680151202509090425'
    assert str0006.operation_number == '31680151250908000000001'
    assert str0006.purpose == CustomerPurpose.CREDIT_IN_ACCOUNT
    assert str0006.priority == Priority.MEDIUM
    assert str0006.scheduled_date == date(2025, 9, 9)
    assert str0006.scheduled_time == time(15, 30)
    assert str0006.settlement_date == date(2025, 9, 8)
    assert str0006.system_domain == 'SPB01'
    assert str0006.to_ispb == '00038166'
    assert str0006.credit_contract_number == '1234567890'
    assert str0006.transaction_id == '0000000000000000000000001'


def test_str0006r1_from_xml() -> None:
    xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/SPB/STR0006.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>31680151250908000000001</NUOp>
        </BCMSG>
        <SISMSG>
            <STR0006R1>
                <CodMsg>STR0006R1</CodMsg>
                <NumCtrlIF>31680151202509090425</NumCtrlIF>
                <ISPBIFDebtd>31680151</ISPBIFDebtd>
                <NumCtrlSTR>STR20250101000000001</NumCtrlSTR>
                <SitLancSTR>1</SitLancSTR>
                <DtHrSit>2025-11-20T15:30:00</DtHrSit>
                <DtMovto>2025-09-08</DtMovto>
            </STR0006R1>
        </SISMSG>
    </DOC>
    """
    str0006r1 = STR0006R1.from_xml(xml)
    assert isinstance(str0006r1, STR0006R1)
    assert str0006r1.institution_control_number == '31680151202509090425'
    assert str0006r1.from_ispb == '31680151'
    assert str0006r1.debtor_institution_ispb == '31680151'
    assert str0006r1.str_control_number == 'STR20250101000000001'
    assert str0006r1.str_settlement_status == StrSettlementStatus.EFFECTIVE
    assert str0006r1.settlement_timestamp == datetime(2025, 11, 20, 15, 30)
    assert str0006r1.settlement_date == date(2025, 9, 8)
    assert str0006r1.operation_number == '31680151250908000000001'
    assert str0006r1.to_ispb == '00038166'
    assert str0006r1.system_domain == 'SPB01'


def test_str0006r2_from_xml() -> None:
    xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/SPB/STR0006.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>31680151250908000000001</NUOp>
        </BCMSG>
        <SISMSG>
            <STR0006R2>
                <CodMsg>STR0006R2</CodMsg>
                <NumCtrlSTR>STR20250101000000001</NumCtrlSTR>
                <DtHrBC>2025-11-20T15:30:00</DtHrBC>
                <ISPBIFDebtd>31680151</ISPBIFDebtd>
                <AgDebtd>0002</AgDebtd>
                <Grupo_STR0006R2_CtDebtd>
                    <TpCtDebtd>CC</TpCtDebtd>
                    <CtDebtd>654321</CtDebtd>
                </Grupo_STR0006R2_CtDebtd>
                <TpPessoaDebtd_Remet>J</TpPessoaDebtd_Remet>
                <CNPJ_CPFCliDebtd_Remet>56369416000136</CNPJ_CPFCliDebtd_Remet>
                <NomCliDebtd_Remet>ACME Inc</NomCliDebtd_Remet>
                <ISPBIFCredtd>60701190</ISPBIFCredtd>
                <AgCredtd>0001</AgCredtd>
                <CtCredtd>123456</CtCredtd>
                <TpPessoaDestinatario>F</TpPessoaDestinatario>
                <CNPJ_CPFDestinatario>69327934075</CNPJ_CPFDestinatario>
                <NomDestinatario>Joe Doe</NomDestinatario>
                <NumContrtoOpCred>1234567890</NumContrtoOpCred>
                <VlrLanc>100.0</VlrLanc>
                <FinlddCli>10</FinlddCli>
                <CodIdentdTransf>0000000000000000000000001</CodIdentdTransf>
                <Hist>Payment for services</Hist>
                <DtMovto>2025-09-08</DtMovto>
            </STR0006R2>
        </SISMSG>
    </DOC>
    """
    str0006r2 = STR0006R2.from_xml(xml)
    assert isinstance(str0006r2, STR0006R2)
    assert str0006r2.amount == Decimal('100.0')
    assert str0006r2.creditor_account_number == '123456'
    assert str0006r2.creditor_institution_ispb == '60701190'
    assert str0006r2.creditor_branch == '0001'
    assert str0006r2.recipient_document == '69327934075'
    assert str0006r2.recipient_name == 'Joe Doe'
    assert str0006r2.recipient_type == PersonType.INDIVIDUAL
    assert str0006r2.debtor_account_number == '654321'
    assert str0006r2.debtor_account_type == AccountType.CURRENT
    assert str0006r2.debtor_branch == '0002'
    assert str0006r2.sender_document == '56369416000136'
    assert str0006r2.debtor_institution_ispb == '31680151'
    assert str0006r2.sender_name == 'ACME Inc'
    assert str0006r2.debtor_payment_account_number is None
    assert str0006r2.sender_type == PersonType.BUSINESS
    assert str0006r2.description == 'Payment for services'
    assert str0006r2.from_ispb == '31680151'
    assert str0006r2.operation_number == '31680151250908000000001'
    assert str0006r2.purpose == CustomerPurpose.CREDIT_IN_ACCOUNT
    assert str0006r2.settlement_date == date(2025, 9, 8)
    assert str0006r2.system_domain == 'SPB01'
    assert str0006r2.to_ispb == '00038166'
    assert str0006r2.transaction_id == '0000000000000000000000001'
    assert str0006r2.vendor_timestamp == datetime(2025, 11, 20, 15, 30)
    assert str0006r2.credit_contract_number == '1234567890'
    assert str0006r2.str_control_number == 'STR20250101000000001'
