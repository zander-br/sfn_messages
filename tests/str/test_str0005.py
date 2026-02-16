from datetime import date, datetime, time
from decimal import Decimal
from typing import Any

import pytest
from pydantic import ValidationError

from sfn_messages.core.types import AccountType, CustomerPurpose, PersonType, Priority, StrSettlementStatus
from sfn_messages.str.str0005 import STR0005, STR0005E, STR0005R1, STR0005R2
from tests.conftest import extract_missing_fields, normalize_xml


def make_valid_str0005_params() -> dict[str, Any]:
    return {
        'amount': 100.00,
        'creditor_account_number': '123456',
        'creditor_account_type': 'CURRENT',
        'creditor_branch': '0001',
        'creditor_institution_ispb': '60701190',
        'debtor_branch': '0002',
        'debtor_institution_ispb': '31680151',
        'description': 'Payment for services',
        'from_ispb': '31680151',
        'institution_control_number': '31680151202509090425',
        'operation_number': '31680151250908000000001',
        'priority': 'HIGHEST',
        'purpose': 'CREDIT_IN_ACCOUNT',
        'recipient_document': '69327934075',
        'recipient_name': 'Joe Doe',
        'recipient_type': 'INDIVIDUAL',
        'scheduled_date': '2025-09-09',
        'scheduled_time': '15:30:00',
        'sender_document': '56369416000136',
        'sender_name': 'ACME Inc',
        'sender_type': 'BUSINESS',
        'settlement_date': '2025-09-08',
        'system_domain': 'SPB01',
        'to_ispb': '00038166',
    }


def make_valid_str0005r1_params() -> dict[str, Any]:
    return {
        'debtor_institution_ispb': '31680151',
        'from_ispb': '31680151',
        'institution_control_number': '31680151202509090425',
        'operation_number': '31680151250908000000001',
        'settlement_date': '2025-09-08',
        'settlement_timestamp': '2025-11-20T15:30:00',
        'str_control_number': 'STR20250101000000001',
        'str_settlement_status': 'EFFECTIVE',
        'system_domain': 'SPB01',
        'to_ispb': '00038166',
    }


def make_valid_str0005r2_params() -> dict[str, Any]:
    return {
        'amount': 100.00,
        'creditor_account_number': '123456',
        'creditor_account_type': 'CURRENT',
        'creditor_branch': '0001',
        'creditor_institution_ispb': '60701190',
        'debtor_branch': '0002',
        'debtor_institution_ispb': '31680151',
        'description': 'Payment for services',
        'from_ispb': '31680151',
        'operation_number': '31680151250908000000001',
        'purpose': 'CREDIT_IN_ACCOUNT',
        'recipient_document': '69327934075',
        'recipient_name': 'Joe Doe',
        'recipient_type': 'INDIVIDUAL',
        'sender_document': '56369416000136',
        'sender_name': 'ACME Inc',
        'sender_type': 'BUSINESS',
        'settlement_date': '2025-09-08',
        'str_control_number': 'STR20250101000000001',
        'system_domain': 'SPB01',
        'to_ispb': '00038166',
        'vendor_timestamp': '2025-11-20T15:30:00',
    }


def make_valid_str0005e_params(*, general_error: bool = False) -> dict[str, Any]:
    str0005e = {
        'amount': 100.00,
        'creditor_account_number': '123456',
        'creditor_account_type': 'CURRENT',
        'creditor_branch': '0001',
        'creditor_institution_ispb': '60701190',
        'debtor_branch': '0002',
        'debtor_institution_ispb': '31680151',
        'description': 'Payment for services',
        'from_ispb': '31680151',
        'institution_control_number': '31680151202509090425',
        'operation_number': '31680151250908000000001',
        'priority': 'HIGHEST',
        'purpose': 'CREDIT_IN_ACCOUNT',
        'recipient_document': '69327934075',
        'recipient_name': 'Joe Doe',
        'recipient_type': 'INDIVIDUAL',
        'scheduled_date': '2025-09-09',
        'scheduled_time': '15:30:00',
        'sender_document': '56369416000136',
        'sender_name': 'ACME Inc',
        'sender_type': 'BUSINESS',
        'settlement_date': '2025-09-08',
        'system_domain': 'SPB01',
        'to_ispb': '00038166',
    }

    if general_error:
        str0005e['general_error_code'] = 'EGEN0050'
    else:
        str0005e['debtor_institution_ispb_error_code'] = 'EGEN0051'

    return str0005e


def test_str0005_valid_model() -> None:
    params = make_valid_str0005_params()
    str0005 = STR0005.model_validate(params)
    assert isinstance(str0005, STR0005)
    assert str0005.amount == Decimal('100.00')
    assert str0005.creditor_account_number == '123456'
    assert str0005.creditor_account_type == AccountType.CURRENT
    assert str0005.creditor_branch == '0001'
    assert str0005.creditor_institution_ispb == '60701190'
    assert str0005.creditor_payment_account_number is None
    assert str0005.debtor_branch == '0002'
    assert str0005.debtor_institution_ispb == '31680151'
    assert str0005.description == 'Payment for services'
    assert str0005.from_ispb == '31680151'
    assert str0005.institution_control_number == '31680151202509090425'
    assert str0005.message_code == 'STR0005'
    assert str0005.operation_number == '31680151250908000000001'
    assert str0005.priority == Priority.HIGHEST
    assert str0005.purpose == CustomerPurpose.CREDIT_IN_ACCOUNT
    assert str0005.recipient_document == '69327934075'
    assert str0005.recipient_name == 'Joe Doe'
    assert str0005.recipient_type == PersonType.INDIVIDUAL
    assert str0005.scheduled_date == date(2025, 9, 9)
    assert str0005.scheduled_time == time(15, 30)
    assert str0005.sender_document == '56369416000136'
    assert str0005.sender_name == 'ACME Inc'
    assert str0005.sender_type == PersonType.BUSINESS
    assert str0005.settlement_date == date(2025, 9, 8)
    assert str0005.system_domain == 'SPB01'
    assert str0005.to_ispb == '00038166'


def test_str0005e_general_error_valid_model() -> None:
    params = make_valid_str0005e_params(general_error=True)
    str0005e = STR0005E.model_validate(params)
    assert isinstance(str0005e, STR0005E)
    assert str0005e.amount == Decimal('100.00')
    assert str0005e.creditor_account_number == '123456'
    assert str0005e.creditor_account_type == AccountType.CURRENT
    assert str0005e.creditor_branch == '0001'
    assert str0005e.creditor_institution_ispb == '60701190'
    assert str0005e.creditor_payment_account_number is None
    assert str0005e.debtor_branch == '0002'
    assert str0005e.debtor_institution_ispb == '31680151'
    assert str0005e.description == 'Payment for services'
    assert str0005e.from_ispb == '31680151'
    assert str0005e.institution_control_number == '31680151202509090425'
    assert str0005e.message_code == 'STR0005E'
    assert str0005e.operation_number == '31680151250908000000001'
    assert str0005e.priority == Priority.HIGHEST
    assert str0005e.purpose == CustomerPurpose.CREDIT_IN_ACCOUNT
    assert str0005e.recipient_document == '69327934075'
    assert str0005e.recipient_name == 'Joe Doe'
    assert str0005e.recipient_type == PersonType.INDIVIDUAL
    assert str0005e.scheduled_date == date(2025, 9, 9)
    assert str0005e.scheduled_time == time(15, 30)
    assert str0005e.sender_document == '56369416000136'
    assert str0005e.sender_name == 'ACME Inc'
    assert str0005e.sender_type == PersonType.BUSINESS
    assert str0005e.settlement_date == date(2025, 9, 8)
    assert str0005e.system_domain == 'SPB01'
    assert str0005e.to_ispb == '00038166'
    assert str0005e.general_error_code == 'EGEN0050'


def test_str0005e_tag_error_valid_model() -> None:
    params = make_valid_str0005e_params()
    str0005e = STR0005E.model_validate(params)
    assert isinstance(str0005e, STR0005E)
    assert str0005e.amount == Decimal('100.00')
    assert str0005e.creditor_account_number == '123456'
    assert str0005e.creditor_account_type == AccountType.CURRENT
    assert str0005e.creditor_branch == '0001'
    assert str0005e.creditor_institution_ispb == '60701190'
    assert str0005e.creditor_payment_account_number is None
    assert str0005e.debtor_branch == '0002'
    assert str0005e.debtor_institution_ispb == '31680151'
    assert str0005e.description == 'Payment for services'
    assert str0005e.from_ispb == '31680151'
    assert str0005e.institution_control_number == '31680151202509090425'
    assert str0005e.message_code == 'STR0005E'
    assert str0005e.operation_number == '31680151250908000000001'
    assert str0005e.priority == Priority.HIGHEST
    assert str0005e.purpose == CustomerPurpose.CREDIT_IN_ACCOUNT
    assert str0005e.recipient_document == '69327934075'
    assert str0005e.recipient_name == 'Joe Doe'
    assert str0005e.recipient_type == PersonType.INDIVIDUAL
    assert str0005e.scheduled_date == date(2025, 9, 9)
    assert str0005e.scheduled_time == time(15, 30)
    assert str0005e.sender_document == '56369416000136'
    assert str0005e.sender_name == 'ACME Inc'
    assert str0005e.sender_type == PersonType.BUSINESS
    assert str0005e.settlement_date == date(2025, 9, 8)
    assert str0005e.system_domain == 'SPB01'
    assert str0005e.to_ispb == '00038166'
    assert str0005e.debtor_institution_ispb_error_code == 'EGEN0051'


def test_str0005_missing_required_fields() -> None:
    with pytest.raises(ValidationError) as exc:
        STR0005.model_validate({})
    missing_fields = extract_missing_fields(exc.value)
    assert missing_fields == {
        'amount',
        'creditor_institution_ispb',
        'debtor_branch',
        'debtor_institution_ispb',
        'from_ispb',
        'institution_control_number',
        'operation_number',
        'purpose',
        'recipient_document',
        'recipient_name',
        'recipient_type',
        'sender_document',
        'sender_name',
        'sender_type',
        'settlement_date',
        'system_domain',
        'to_ispb',
    }


def test_str0005_business_rules_invalid_sender_document() -> None:
    params = make_valid_str0005_params()
    params['sender_type'] = 'INDIVIDUAL'
    params['sender_document'] = '56369416000136'

    with pytest.raises(ValidationError) as exc:
        STR0005.model_validate(params)
    error_message = str(exc.value)
    assert 'Invalid CPF for sender_type INDIVIDUAL' in error_message


def test_str0005_business_rules_invalid_recipient_document() -> None:
    params = make_valid_str0005_params()
    params['recipient_type'] = 'BUSINESS'
    params['recipient_document'] = '69327934075'

    with pytest.raises(ValidationError) as exc:
        STR0005.model_validate(params)
    error_message = str(exc.value)
    assert 'Invalid CNPJ for recipient_type BUSINESS' in error_message


def test_str0005_business_rules_missing_description_for_other_purpose() -> None:
    params = make_valid_str0005_params()
    params['purpose'] = 'OTHERS'
    del params['description']

    with pytest.raises(ValidationError) as exc:
        STR0005.model_validate(params)
    error_message = str(exc.value)
    assert 'description is required when purpose is OTHERS' in error_message


def test_str0005_business_rules_missing_creditor_branch_for_creditor_account_type_is_not_payment() -> None:
    params = make_valid_str0005_params()
    params['creditor_account_type'] = 'CURRENT'
    del params['creditor_branch']

    with pytest.raises(ValidationError) as exc:
        STR0005.model_validate(params)
    error_message = str(exc.value)
    assert 'creditor_branch is required when creditor_account_type is not PAYMENT' in error_message


def test_str0005_business_rules_missing_creditor_payment_account_number_for_creditor_account_type_is_payment() -> None:
    params = make_valid_str0005_params()
    params['creditor_account_type'] = 'PAYMENT'

    with pytest.raises(ValidationError) as exc:
        STR0005.model_validate(params)
    error_message = str(exc.value)
    assert 'creditor_payment_account_number is required when creditor_account_type is PAYMENT' in error_message


def test_str0005_business_rules_missing_creditor_account_number_for_creditor_account_type_is_not_payment() -> None:
    params = make_valid_str0005_params()
    params['creditor_account_type'] = 'CURRENT'
    del params['creditor_account_number']

    with pytest.raises(ValidationError) as exc:
        STR0005.model_validate(params)
    error_message = str(exc.value)
    assert 'creditor_account_number is required when creditor_account_type is not PAYMENT' in error_message


def test_str0005_to_xml() -> None:
    params = make_valid_str0005_params()
    str0005 = STR0005.model_validate(params)
    xml = str0005.to_xml()

    expected_xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/SPB/STR0005.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>31680151250908000000001</NUOp>
        </BCMSG>
        <SISMSG>
            <STR0005>
                <CodMsg>STR0005</CodMsg>
                <NumCtrlIF>31680151202509090425</NumCtrlIF>
                <ISPBIFDebtd>31680151</ISPBIFDebtd>
                <AgDebtd>0002</AgDebtd>
                <TpPessoaRemet>J</TpPessoaRemet>
                <CNPJ_CPFRemet>56369416000136</CNPJ_CPFRemet>
                <NomRemet>ACME Inc</NomRemet>
                <ISPBIFCredtd>60701190</ISPBIFCredtd>
                <AgCredtd>0001</AgCredtd>
                <CtCredtd>123456</CtCredtd>
                <TpCtCredtd>CC</TpCtCredtd>
                <TpPessoaDestinatario>F</TpPessoaDestinatario>
                <CNPJ_CPFDestinatario>69327934075</CNPJ_CPFDestinatario>
                <NomDestinatario>Joe Doe</NomDestinatario>
                <VlrLanc>100.0</VlrLanc>
                <FinlddCli>10</FinlddCli>
                <Hist>Payment for services</Hist>
                <DtAgendt>2025-09-09</DtAgendt>
                <HrAgendt>15:30:00</HrAgendt>
                <NivelPref>A</NivelPref>
                <DtMovto>2025-09-08</DtMovto>
            </STR0005>
        </SISMSG>
    </DOC>
    """

    assert normalize_xml(expected_xml) == normalize_xml(xml)


def test_str0005e_general_error_to_xml() -> None:
    params = make_valid_str0005e_params(general_error=True)
    str0005e = STR0005E.model_validate(params)
    xml = str0005e.to_xml()

    expected_xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/SPB/STR0005E.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>31680151250908000000001</NUOp>
        </BCMSG>
        <SISMSG>
            <STR0005 CodErro="EGEN0050">
                <CodMsg>STR0005E</CodMsg>
                <NumCtrlIF>31680151202509090425</NumCtrlIF>
                <ISPBIFDebtd>31680151</ISPBIFDebtd>
                <AgDebtd>0002</AgDebtd>
                <TpPessoaRemet>J</TpPessoaRemet>
                <CNPJ_CPFRemet>56369416000136</CNPJ_CPFRemet>
                <NomRemet>ACME Inc</NomRemet>
                <ISPBIFCredtd>60701190</ISPBIFCredtd>
                <AgCredtd>0001</AgCredtd>
                <CtCredtd>123456</CtCredtd>
                <TpCtCredtd>CC</TpCtCredtd>
                <TpPessoaDestinatario>F</TpPessoaDestinatario>
                <CNPJ_CPFDestinatario>69327934075</CNPJ_CPFDestinatario>
                <NomDestinatario>Joe Doe</NomDestinatario>
                <VlrLanc>100.0</VlrLanc>
                <FinlddCli>10</FinlddCli>
                <Hist>Payment for services</Hist>
                <DtAgendt>2025-09-09</DtAgendt>
                <HrAgendt>15:30:00</HrAgendt>
                <NivelPref>A</NivelPref>
                <DtMovto>2025-09-08</DtMovto>
            </STR0005>
        </SISMSG>
    </DOC>
    """

    assert normalize_xml(expected_xml) == normalize_xml(xml)


def test_str0005e_tag_error_to_xml() -> None:
    params = make_valid_str0005e_params()
    str0005e = STR0005E.model_validate(params)
    xml = str0005e.to_xml()

    expected_xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/SPB/STR0005E.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>31680151250908000000001</NUOp>
        </BCMSG>
        <SISMSG>
            <STR0005>
                <CodMsg>STR0005E</CodMsg>
                <NumCtrlIF>31680151202509090425</NumCtrlIF>
                <ISPBIFDebtd CodErro="EGEN0051">31680151</ISPBIFDebtd>
                <AgDebtd>0002</AgDebtd>
                <TpPessoaRemet>J</TpPessoaRemet>
                <CNPJ_CPFRemet>56369416000136</CNPJ_CPFRemet>
                <NomRemet>ACME Inc</NomRemet>
                <ISPBIFCredtd>60701190</ISPBIFCredtd>
                <AgCredtd>0001</AgCredtd>
                <CtCredtd>123456</CtCredtd>
                <TpCtCredtd>CC</TpCtCredtd>
                <TpPessoaDestinatario>F</TpPessoaDestinatario>
                <CNPJ_CPFDestinatario>69327934075</CNPJ_CPFDestinatario>
                <NomDestinatario>Joe Doe</NomDestinatario>
                <VlrLanc>100.0</VlrLanc>
                <FinlddCli>10</FinlddCli>
                <Hist>Payment for services</Hist>
                <DtAgendt>2025-09-09</DtAgendt>
                <HrAgendt>15:30:00</HrAgendt>
                <NivelPref>A</NivelPref>
                <DtMovto>2025-09-08</DtMovto>
            </STR0005>
        </SISMSG>
    </DOC>
    """

    assert normalize_xml(expected_xml) == normalize_xml(xml)


def test_str0005_to_xml_omit_optional_fields() -> None:
    params = make_valid_str0005_params()
    del params['creditor_account_number']
    del params['creditor_account_type']
    del params['creditor_branch']
    del params['description']
    del params['priority']
    del params['scheduled_date']
    del params['scheduled_time']

    str0005 = STR0005.model_validate(params)
    xml = str0005.to_xml()

    expected_xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/SPB/STR0005.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>31680151250908000000001</NUOp>
        </BCMSG>
        <SISMSG>
            <STR0005>
                <CodMsg>STR0005</CodMsg>
                <NumCtrlIF>31680151202509090425</NumCtrlIF>
                <ISPBIFDebtd>31680151</ISPBIFDebtd>
                <AgDebtd>0002</AgDebtd>
                <TpPessoaRemet>J</TpPessoaRemet>
                <CNPJ_CPFRemet>56369416000136</CNPJ_CPFRemet>
                <NomRemet>ACME Inc</NomRemet>
                <ISPBIFCredtd>60701190</ISPBIFCredtd>
                <TpPessoaDestinatario>F</TpPessoaDestinatario>
                <CNPJ_CPFDestinatario>69327934075</CNPJ_CPFDestinatario>
                <NomDestinatario>Joe Doe</NomDestinatario>
                <VlrLanc>100.0</VlrLanc>
                <FinlddCli>10</FinlddCli>
                <DtMovto>2025-09-08</DtMovto>
            </STR0005>
        </SISMSG>
    </DOC>
    """

    assert normalize_xml(expected_xml) == normalize_xml(xml)


def test_str0005_from_xml() -> None:
    xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/SPB/STR0005.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>31680151250908000000001</NUOp>
        </BCMSG>
        <SISMSG>
            <STR0005>
                <CodMsg>STR0005</CodMsg>
                <NumCtrlIF>31680151202509090425</NumCtrlIF>
                <ISPBIFDebtd>31680151</ISPBIFDebtd>
                <AgDebtd>0002</AgDebtd>
                <TpPessoaRemet>J</TpPessoaRemet>
                <CNPJ_CPFRemet>56369416000136</CNPJ_CPFRemet>
                <NomRemet>ACME Inc</NomRemet>
                <ISPBIFCredtd>60701190</ISPBIFCredtd>
                <AgCredtd>0001</AgCredtd>
                <CtCredtd>123456</CtCredtd>
                <TpCtCredtd>CC</TpCtCredtd>
                <TpPessoaDestinatario>F</TpPessoaDestinatario>
                <CNPJ_CPFDestinatario>69327934075</CNPJ_CPFDestinatario>
                <NomDestinatario>Joe Doe</NomDestinatario>
                <VlrLanc>100.0</VlrLanc>
                <FinlddCli>10</FinlddCli>
                <Hist>Payment for services</Hist>
                <DtAgendt>2025-09-09</DtAgendt>
                <HrAgendt>15:30:00</HrAgendt>
                <NivelPref>A</NivelPref>
                <DtMovto>2025-09-08</DtMovto>
            </STR0005>
        </SISMSG>
    </DOC>
    """

    str0005 = STR0005.from_xml(xml)
    assert isinstance(str0005, STR0005)
    assert str0005.amount == Decimal('100.0')
    assert str0005.creditor_account_number == '123456'
    assert str0005.creditor_account_type == AccountType.CURRENT
    assert str0005.creditor_branch == '0001'
    assert str0005.creditor_institution_ispb == '60701190'
    assert str0005.creditor_payment_account_number is None
    assert str0005.debtor_branch == '0002'
    assert str0005.debtor_institution_ispb == '31680151'
    assert str0005.description == 'Payment for services'
    assert str0005.from_ispb == '31680151'
    assert str0005.institution_control_number == '31680151202509090425'
    assert str0005.message_code == 'STR0005'
    assert str0005.operation_number == '31680151250908000000001'
    assert str0005.priority == Priority.HIGHEST
    assert str0005.purpose == CustomerPurpose.CREDIT_IN_ACCOUNT
    assert str0005.recipient_document == '69327934075'
    assert str0005.recipient_name == 'Joe Doe'
    assert str0005.recipient_type == PersonType.INDIVIDUAL
    assert str0005.scheduled_date == date(2025, 9, 9)
    assert str0005.scheduled_time == time(15, 30)
    assert str0005.sender_document == '56369416000136'
    assert str0005.sender_name == 'ACME Inc'
    assert str0005.sender_type == PersonType.BUSINESS
    assert str0005.settlement_date == date(2025, 9, 8)
    assert str0005.system_domain == 'SPB01'
    assert str0005.to_ispb == '00038166'


def test_str0005e_general_error_from_xml() -> None:
    xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/SPB/STR0005E.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>31680151250908000000001</NUOp>
        </BCMSG>
        <SISMSG>
            <STR0005 CodErro="EGEN0050">
                <CodMsg>STR0005E</CodMsg>
                <NumCtrlIF>31680151202509090425</NumCtrlIF>
                <ISPBIFDebtd>31680151</ISPBIFDebtd>
                <AgDebtd>0002</AgDebtd>
                <TpPessoaRemet>J</TpPessoaRemet>
                <CNPJ_CPFRemet>56369416000136</CNPJ_CPFRemet>
                <NomRemet>ACME Inc</NomRemet>
                <ISPBIFCredtd>60701190</ISPBIFCredtd>
                <AgCredtd>0001</AgCredtd>
                <CtCredtd>123456</CtCredtd>
                <TpCtCredtd>CC</TpCtCredtd>
                <TpPessoaDestinatario>F</TpPessoaDestinatario>
                <CNPJ_CPFDestinatario>69327934075</CNPJ_CPFDestinatario>
                <NomDestinatario>Joe Doe</NomDestinatario>
                <VlrLanc>100.0</VlrLanc>
                <FinlddCli>10</FinlddCli>
                <Hist>Payment for services</Hist>
                <DtAgendt>2025-09-09</DtAgendt>
                <HrAgendt>15:30:00</HrAgendt>
                <NivelPref>A</NivelPref>
                <DtMovto>2025-09-08</DtMovto>
            </STR0005>
        </SISMSG>
    </DOC>
    """

    str0005e = STR0005E.from_xml(xml)
    assert isinstance(str0005e, STR0005E)
    assert str0005e.amount == Decimal('100.0')
    assert str0005e.creditor_account_number == '123456'
    assert str0005e.creditor_account_type == AccountType.CURRENT
    assert str0005e.creditor_branch == '0001'
    assert str0005e.creditor_institution_ispb == '60701190'
    assert str0005e.debtor_branch == '0002'
    assert str0005e.debtor_institution_ispb == '31680151'
    assert str0005e.description == 'Payment for services'
    assert str0005e.from_ispb == '31680151'
    assert str0005e.institution_control_number == '31680151202509090425'
    assert str0005e.priority == Priority.HIGHEST
    assert str0005e.purpose == CustomerPurpose.CREDIT_IN_ACCOUNT
    assert str0005e.recipient_document == '69327934075'
    assert str0005e.recipient_name == 'Joe Doe'
    assert str0005e.recipient_type == PersonType.INDIVIDUAL
    assert str0005e.scheduled_date == date(2025, 9, 9)
    assert str0005e.scheduled_time == time(15, 30)
    assert str0005e.sender_document == '56369416000136'
    assert str0005e.sender_name == 'ACME Inc'
    assert str0005e.sender_type == PersonType.BUSINESS
    assert str0005e.settlement_date == date(2025, 9, 8)
    assert str0005e.general_error_code == 'EGEN0050'


def test_str0005e_tag_error_from_xml() -> None:
    xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/SPB/STR0005E.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>31680151250908000000001</NUOp>
        </BCMSG>
        <SISMSG>
            <STR0005>
                <CodMsg>STR0005E</CodMsg>
                <NumCtrlIF>31680151202509090425</NumCtrlIF>
                <ISPBIFDebtd CodErro="EGEN0051">31680151</ISPBIFDebtd>
                <AgDebtd>0002</AgDebtd>
                <TpPessoaRemet>J</TpPessoaRemet>
                <CNPJ_CPFRemet>56369416000136</CNPJ_CPFRemet>
                <NomRemet>ACME Inc</NomRemet>
                <ISPBIFCredtd>60701190</ISPBIFCredtd>
                <AgCredtd>0001</AgCredtd>
                <CtCredtd>123456</CtCredtd>
                <TpCtCredtd>CC</TpCtCredtd>
                <TpPessoaDestinatario>F</TpPessoaDestinatario>
                <CNPJ_CPFDestinatario>69327934075</CNPJ_CPFDestinatario>
                <NomDestinatario>Joe Doe</NomDestinatario>
                <VlrLanc>100.0</VlrLanc>
                <FinlddCli>10</FinlddCli>
                <Hist>Payment for services</Hist>
                <DtAgendt>2025-09-09</DtAgendt>
                <HrAgendt>15:30:00</HrAgendt>
                <NivelPref>A</NivelPref>
                <DtMovto>2025-09-08</DtMovto>
            </STR0005>
        </SISMSG>
    </DOC>
    """

    str0005e = STR0005E.from_xml(xml)
    assert isinstance(str0005e, STR0005E)
    assert str0005e.amount == Decimal('100.0')
    assert str0005e.debtor_institution_ispb == '31680151'
    assert str0005e.debtor_institution_ispb_error_code == 'EGEN0051'
    assert str0005e.general_error_code is None


def test_str0005_from_xml_omit_optional_fields() -> None:
    xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/SPB/STR0005.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>31680151250908000000001</NUOp>
        </BCMSG>
        <SISMSG>
            <STR0005>
                <CodMsg>STR0005</CodMsg>
                <NumCtrlIF>31680151202509090425</NumCtrlIF>
                <ISPBIFDebtd>31680151</ISPBIFDebtd>
                <AgDebtd>0002</AgDebtd>
                <TpPessoaRemet>J</TpPessoaRemet>
                <CNPJ_CPFRemet>56369416000136</CNPJ_CPFRemet>
                <NomRemet>ACME Inc</NomRemet>
                <ISPBIFCredtd>60701190</ISPBIFCredtd>
                <TpPessoaDestinatario>F</TpPessoaDestinatario>
                <CNPJ_CPFDestinatario>69327934075</CNPJ_CPFDestinatario>
                <NomDestinatario>Joe Doe</NomDestinatario>
                <VlrLanc>100.0</VlrLanc>
                <FinlddCli>10</FinlddCli>
                <DtMovto>2025-09-08</DtMovto>
            </STR0005>
        </SISMSG>
    </DOC>
    """

    str0005 = STR0005.from_xml(xml)
    assert isinstance(str0005, STR0005)
    assert str0005.amount == Decimal('100.0')
    assert str0005.creditor_account_number is None
    assert str0005.creditor_account_type is None
    assert str0005.creditor_branch is None
    assert str0005.creditor_institution_ispb == '60701190'
    assert str0005.creditor_payment_account_number is None
    assert str0005.debtor_branch == '0002'
    assert str0005.debtor_institution_ispb == '31680151'
    assert str0005.description is None
    assert str0005.from_ispb == '31680151'
    assert str0005.institution_control_number == '31680151202509090425'
    assert str0005.priority is None
    assert str0005.purpose == CustomerPurpose.CREDIT_IN_ACCOUNT
    assert str0005.recipient_document == '69327934075'
    assert str0005.recipient_name == 'Joe Doe'
    assert str0005.recipient_type == PersonType.INDIVIDUAL
    assert str0005.scheduled_date is None
    assert str0005.scheduled_time is None
    assert str0005.sender_document == '56369416000136'
    assert str0005.sender_name == 'ACME Inc'
    assert str0005.sender_type == PersonType.BUSINESS
    assert str0005.settlement_date == date(2025, 9, 8)
    assert str0005.system_domain == 'SPB01'
    assert str0005.to_ispb == '00038166'


def test_str0005_roundtrip() -> None:
    params = make_valid_str0005_params()
    del params['priority']
    str0005 = STR0005.model_validate(params)
    xml = str0005.to_xml()
    str0005_from_xml = STR0005.from_xml(xml)
    assert str0005 == str0005_from_xml


def test_str0005_from_xml_missing_required_fields() -> None:
    xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/SPB/STR0005.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>31680151250908000000001</NUOp>
        </BCMSG>
        <SISMSG>
            <STR0005>
                <CodMsg>STR0005</CodMsg>
            </STR0005>
        </SISMSG>
    </DOC>
    """

    with pytest.raises(ValidationError) as exc:
        STR0005.from_xml(xml)
    missing_fields = extract_missing_fields(exc.value)
    assert missing_fields == {
        'amount',
        'creditor_institution_ispb',
        'debtor_branch',
        'debtor_institution_ispb',
        'institution_control_number',
        'purpose',
        'recipient_document',
        'recipient_name',
        'recipient_type',
        'sender_document',
        'sender_name',
        'sender_type',
        'settlement_date',
    }


def test_str0005r1_valid_model() -> None:
    params = make_valid_str0005r1_params()
    str0005r1 = STR0005R1.model_validate(params)
    assert isinstance(str0005r1, STR0005R1)
    assert str0005r1.debtor_institution_ispb == '31680151'
    assert str0005r1.from_ispb == '31680151'
    assert str0005r1.institution_control_number == '31680151202509090425'
    assert str0005r1.message_code == 'STR0005R1'
    assert str0005r1.operation_number == '31680151250908000000001'
    assert str0005r1.settlement_date == date(2025, 9, 8)
    assert str0005r1.settlement_timestamp == datetime(2025, 11, 20, 15, 30)
    assert str0005r1.str_control_number == 'STR20250101000000001'
    assert str0005r1.str_settlement_status == StrSettlementStatus.EFFECTIVE
    assert str0005r1.system_domain == 'SPB01'
    assert str0005r1.to_ispb == '00038166'


def test_str0005r1_missing_required_fields() -> None:
    with pytest.raises(ValidationError) as exc:
        STR0005R1.model_validate({})
    missing_fields = extract_missing_fields(exc.value)
    assert missing_fields == {
        'debtor_institution_ispb',
        'from_ispb',
        'institution_control_number',
        'operation_number',
        'settlement_date',
        'settlement_timestamp',
        'str_control_number',
        'str_settlement_status',
        'system_domain',
        'to_ispb',
    }


def test_str0005r1_to_xml() -> None:
    params = make_valid_str0005r1_params()
    str0005r1 = STR0005R1.model_validate(params)
    xml = str0005r1.to_xml()

    expected_xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/SPB/STR0005.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>31680151250908000000001</NUOp>
        </BCMSG>
        <SISMSG>
            <STR0005R1>
                <CodMsg>STR0005R1</CodMsg>
                <NumCtrlIF>31680151202509090425</NumCtrlIF>
                <ISPBIFDebtd>31680151</ISPBIFDebtd>
                <NumCtrlSTR>STR20250101000000001</NumCtrlSTR>
                <SitLancSTR>1</SitLancSTR>
                <DtHrSit>2025-11-20T15:30:00</DtHrSit>
                <DtMovto>2025-09-08</DtMovto>
            </STR0005R1>
        </SISMSG>
    </DOC>
    """

    assert normalize_xml(expected_xml) == normalize_xml(xml)


def test_str0005r1_from_xml() -> None:
    xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/SPB/STR0005.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>31680151250908000000001</NUOp>
        </BCMSG>
        <SISMSG>
            <STR0005R1>
                <CodMsg>STR0005R1</CodMsg>
                <NumCtrlIF>31680151202509090425</NumCtrlIF>
                <ISPBIFDebtd>31680151</ISPBIFDebtd>
                <NumCtrlSTR>STR20250101000000001</NumCtrlSTR>
                <SitLancSTR>1</SitLancSTR>
                <DtHrSit>2025-11-20T15:30:00</DtHrSit>
                <DtMovto>2025-09-08</DtMovto>
            </STR0005R1>
        </SISMSG>
    </DOC>
    """

    str0005r1 = STR0005R1.from_xml(xml)
    assert isinstance(str0005r1, STR0005R1)
    assert str0005r1.debtor_institution_ispb == '31680151'
    assert str0005r1.from_ispb == '31680151'
    assert str0005r1.institution_control_number == '31680151202509090425'
    assert str0005r1.message_code == 'STR0005R1'
    assert str0005r1.operation_number == '31680151250908000000001'
    assert str0005r1.settlement_date == date(2025, 9, 8)
    assert str0005r1.settlement_timestamp == datetime(2025, 11, 20, 15, 30)
    assert str0005r1.str_control_number == 'STR20250101000000001'
    assert str0005r1.str_settlement_status == StrSettlementStatus.EFFECTIVE
    assert str0005r1.system_domain == 'SPB01'
    assert str0005r1.to_ispb == '00038166'


def test_str0005r1_roundtrip() -> None:
    params = make_valid_str0005r1_params()
    str0005r1 = STR0005R1.model_validate(params)
    xml = str0005r1.to_xml()
    str0005r1_from_xml = STR0005R1.from_xml(xml)
    assert str0005r1 == str0005r1_from_xml


def test_str0005r1_from_xml_missing_required_fields() -> None:
    xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/SPB/STR0005.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>31680151250908000000001</NUOp>
        </BCMSG>
        <SISMSG>
            <STR0005R1>
                <CodMsg>STR0005R1</CodMsg>
            </STR0005R1>
        </SISMSG>
    </DOC>
    """

    with pytest.raises(ValidationError) as exc:
        STR0005R1.from_xml(xml)
    missing_fields = extract_missing_fields(exc.value)
    assert missing_fields == {
        'debtor_institution_ispb',
        'institution_control_number',
        'settlement_date',
        'settlement_timestamp',
        'str_control_number',
        'str_settlement_status',
    }


def test_str0005r2_valid_model() -> None:
    params = make_valid_str0005r2_params()
    str0005r2 = STR0005R2.model_validate(params)
    assert isinstance(str0005r2, STR0005R2)
    assert str0005r2.amount == Decimal('100.00')
    assert str0005r2.creditor_account_number == '123456'
    assert str0005r2.creditor_account_type == AccountType.CURRENT
    assert str0005r2.creditor_branch == '0001'
    assert str0005r2.creditor_institution_ispb == '60701190'
    assert str0005r2.creditor_payment_account_number is None
    assert str0005r2.debtor_branch == '0002'
    assert str0005r2.debtor_institution_ispb == '31680151'
    assert str0005r2.description == 'Payment for services'
    assert str0005r2.from_ispb == '31680151'
    assert str0005r2.message_code == 'STR0005R2'
    assert str0005r2.operation_number == '31680151250908000000001'
    assert str0005r2.purpose == CustomerPurpose.CREDIT_IN_ACCOUNT
    assert str0005r2.recipient_document == '69327934075'
    assert str0005r2.recipient_name == 'Joe Doe'
    assert str0005r2.recipient_type == PersonType.INDIVIDUAL
    assert str0005r2.sender_document == '56369416000136'
    assert str0005r2.sender_name == 'ACME Inc'
    assert str0005r2.sender_type == PersonType.BUSINESS
    assert str0005r2.settlement_date == date(2025, 9, 8)
    assert str0005r2.str_control_number == 'STR20250101000000001'
    assert str0005r2.system_domain == 'SPB01'
    assert str0005r2.to_ispb == '00038166'
    assert str0005r2.vendor_timestamp == datetime(2025, 11, 20, 15, 30)


def test_str0005r2_missing_required_fields() -> None:
    with pytest.raises(ValidationError) as exc:
        STR0005R2.model_validate({})
    missing_fields = extract_missing_fields(exc.value)
    assert missing_fields == {
        'amount',
        'creditor_institution_ispb',
        'debtor_branch',
        'debtor_institution_ispb',
        'from_ispb',
        'operation_number',
        'purpose',
        'recipient_document',
        'recipient_name',
        'recipient_type',
        'sender_document',
        'sender_name',
        'sender_type',
        'settlement_date',
        'str_control_number',
        'system_domain',
        'to_ispb',
        'vendor_timestamp',
    }


def test_str0005r2_business_rules_missing_description_for_other_purpose() -> None:
    params = make_valid_str0005r2_params()
    params['purpose'] = 'OTHERS'
    del params['description']

    with pytest.raises(ValidationError) as exc:
        STR0005R2.model_validate(params)
    error_message = str(exc.value)
    assert 'description is required when purpose is OTHERS' in error_message


def test_str0005r2_business_rules_missing_creditor_branch_for_creditor_account_type_is_not_payment() -> None:
    params = make_valid_str0005r2_params()
    params['creditor_account_type'] = 'CURRENT'
    del params['creditor_branch']

    with pytest.raises(ValidationError) as exc:
        STR0005R2.model_validate(params)
    error_message = str(exc.value)
    assert 'creditor_branch is required when creditor_account_type is not PAYMENT' in error_message


def test_str0005r2_business_rules_missing_creditor_payment_account_number_for_creditor_account_type_is_payment() -> (
    None
):
    params = make_valid_str0005r2_params()
    params['creditor_account_type'] = 'PAYMENT'

    with pytest.raises(ValidationError) as exc:
        STR0005R2.model_validate(params)
    error_message = str(exc.value)
    assert 'creditor_payment_account_number is required when creditor_account_type is PAYMENT' in error_message


def test_str0005r2_business_rules_missing_creditor_account_number_for_creditor_account_type_is_not_payment() -> None:
    params = make_valid_str0005r2_params()
    params['creditor_account_type'] = 'CURRENT'
    del params['creditor_account_number']

    with pytest.raises(ValidationError) as exc:
        STR0005R2.model_validate(params)
    error_message = str(exc.value)
    assert 'creditor_account_number is required when creditor_account_type is not PAYMENT' in error_message


def test_str0005r2_to_xml() -> None:
    params = make_valid_str0005r2_params()
    str0005r2 = STR0005R2.model_validate(params)
    xml = str0005r2.to_xml()

    expected_xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/SPB/STR0005.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>31680151250908000000001</NUOp>
        </BCMSG>
        <SISMSG>
            <STR0005R2>
                <CodMsg>STR0005R2</CodMsg>
                <NumCtrlSTR>STR20250101000000001</NumCtrlSTR>
                <DtHrBC>2025-11-20T15:30:00</DtHrBC>
                <ISPBIFDebtd>31680151</ISPBIFDebtd>
                <AgDebtd>0002</AgDebtd>
                <TpPessoaRemet>J</TpPessoaRemet>
                <CNPJ_CPFRemet>56369416000136</CNPJ_CPFRemet>
                <NomRemet>ACME Inc</NomRemet>
                <ISPBIFCredtd>60701190</ISPBIFCredtd>
                <AgCredtd>0001</AgCredtd>
                <CtCredtd>123456</CtCredtd>
                <TpCtCredtd>CC</TpCtCredtd>
                <TpPessoaDestinatario>F</TpPessoaDestinatario>
                <CNPJ_CPFDestinatario>69327934075</CNPJ_CPFDestinatario>
                <NomDestinatario>Joe Doe</NomDestinatario>
                <VlrLanc>100.0</VlrLanc>
                <FinlddCli>10</FinlddCli>
                <Hist>Payment for services</Hist>
                <DtMovto>2025-09-08</DtMovto>
            </STR0005R2>
        </SISMSG>
    </DOC>
    """

    assert normalize_xml(expected_xml) == normalize_xml(xml)


def test_str0005r2_to_xml_omit_optional_fields() -> None:
    params = make_valid_str0005r2_params()
    del params['creditor_account_number']
    del params['creditor_account_type']
    del params['creditor_branch']
    del params['description']

    str0005r2 = STR0005R2.model_validate(params)
    xml = str0005r2.to_xml()

    expected_xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/SPB/STR0005.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>31680151250908000000001</NUOp>
        </BCMSG>
        <SISMSG>
            <STR0005R2>
                <CodMsg>STR0005R2</CodMsg>
                <NumCtrlSTR>STR20250101000000001</NumCtrlSTR>
                <DtHrBC>2025-11-20T15:30:00</DtHrBC>
                <ISPBIFDebtd>31680151</ISPBIFDebtd>
                <AgDebtd>0002</AgDebtd>
                <TpPessoaRemet>J</TpPessoaRemet>
                <CNPJ_CPFRemet>56369416000136</CNPJ_CPFRemet>
                <NomRemet>ACME Inc</NomRemet>
                <ISPBIFCredtd>60701190</ISPBIFCredtd>
                <TpPessoaDestinatario>F</TpPessoaDestinatario>
                <CNPJ_CPFDestinatario>69327934075</CNPJ_CPFDestinatario>
                <NomDestinatario>Joe Doe</NomDestinatario>
                <VlrLanc>100.0</VlrLanc>
                <FinlddCli>10</FinlddCli>
                <DtMovto>2025-09-08</DtMovto>
            </STR0005R2>
        </SISMSG>
    </DOC>
    """

    assert normalize_xml(expected_xml) == normalize_xml(xml)


def test_str0005r2_from_xml() -> None:
    xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/SPB/STR0005.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>31680151250908000000001</NUOp>
        </BCMSG>
        <SISMSG>
            <STR0005R2>
                <CodMsg>STR0005R2</CodMsg>
                <NumCtrlSTR>STR20250101000000001</NumCtrlSTR>
                <DtHrBC>2025-11-20T15:30:00</DtHrBC>
                <ISPBIFDebtd>31680151</ISPBIFDebtd>
                <AgDebtd>0002</AgDebtd>
                <TpPessoaRemet>J</TpPessoaRemet>
                <CNPJ_CPFRemet>56369416000136</CNPJ_CPFRemet>
                <NomRemet>ACME Inc</NomRemet>
                <ISPBIFCredtd>60701190</ISPBIFCredtd>
                <AgCredtd>0001</AgCredtd>
                <CtCredtd>123456</CtCredtd>
                <TpCtCredtd>CC</TpCtCredtd>
                <TpPessoaDestinatario>F</TpPessoaDestinatario>
                <CNPJ_CPFDestinatario>69327934075</CNPJ_CPFDestinatario>
                <NomDestinatario>Joe Doe</NomDestinatario>
                <VlrLanc>100.0</VlrLanc>
                <FinlddCli>10</FinlddCli>
                <Hist>Payment for services</Hist>
                <DtMovto>2025-09-08</DtMovto>
            </STR0005R2>
        </SISMSG>
    </DOC>
    """

    str0005r2 = STR0005R2.from_xml(xml)
    assert isinstance(str0005r2, STR0005R2)
    assert str0005r2.amount == Decimal('100.0')
    assert str0005r2.creditor_account_number == '123456'
    assert str0005r2.creditor_account_type == AccountType.CURRENT
    assert str0005r2.creditor_branch == '0001'
    assert str0005r2.creditor_institution_ispb == '60701190'
    assert str0005r2.creditor_payment_account_number is None
    assert str0005r2.debtor_branch == '0002'
    assert str0005r2.debtor_institution_ispb == '31680151'
    assert str0005r2.description == 'Payment for services'
    assert str0005r2.from_ispb == '31680151'
    assert str0005r2.message_code == 'STR0005R2'
    assert str0005r2.operation_number == '31680151250908000000001'
    assert str0005r2.purpose == CustomerPurpose.CREDIT_IN_ACCOUNT
    assert str0005r2.recipient_document == '69327934075'
    assert str0005r2.recipient_name == 'Joe Doe'
    assert str0005r2.recipient_type == PersonType.INDIVIDUAL
    assert str0005r2.sender_document == '56369416000136'
    assert str0005r2.sender_name == 'ACME Inc'
    assert str0005r2.sender_type == PersonType.BUSINESS
    assert str0005r2.settlement_date == date(2025, 9, 8)
    assert str0005r2.str_control_number == 'STR20250101000000001'
    assert str0005r2.system_domain == 'SPB01'
    assert str0005r2.to_ispb == '00038166'
    assert str0005r2.vendor_timestamp == datetime(2025, 11, 20, 15, 30)


def test_str0005r2_from_xml_omit_optional_fields() -> None:
    xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/SPB/STR0005.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>31680151250908000000001</NUOp>
        </BCMSG>
        <SISMSG>
            <STR0005R2>
                <CodMsg>STR0005R2</CodMsg>
                <NumCtrlSTR>STR20250101000000001</NumCtrlSTR>
                <DtHrBC>2025-11-20T15:30:00</DtHrBC>
                <ISPBIFDebtd>31680151</ISPBIFDebtd>
                <AgDebtd>0002</AgDebtd>
                <TpPessoaRemet>J</TpPessoaRemet>
                <CNPJ_CPFRemet>56369416000136</CNPJ_CPFRemet>
                <NomRemet>ACME Inc</NomRemet>
                <ISPBIFCredtd>60701190</ISPBIFCredtd>
                <TpPessoaDestinatario>F</TpPessoaDestinatario>
                <CNPJ_CPFDestinatario>69327934075</CNPJ_CPFDestinatario>
                <NomDestinatario>Joe Doe</NomDestinatario>
                <VlrLanc>100.0</VlrLanc>
                <FinlddCli>10</FinlddCli>
                <DtMovto>2025-09-08</DtMovto>
            </STR0005R2>
        </SISMSG>
    </DOC>
    """

    str0005r2 = STR0005R2.from_xml(xml)
    assert isinstance(str0005r2, STR0005R2)
    assert str0005r2.amount == Decimal('100.0')
    assert str0005r2.creditor_account_number is None
    assert str0005r2.creditor_account_type is None
    assert str0005r2.creditor_branch is None
    assert str0005r2.creditor_institution_ispb == '60701190'
    assert str0005r2.creditor_payment_account_number is None
    assert str0005r2.debtor_branch == '0002'
    assert str0005r2.debtor_institution_ispb == '31680151'
    assert str0005r2.description is None
    assert str0005r2.from_ispb == '31680151'
    assert str0005r2.purpose == CustomerPurpose.CREDIT_IN_ACCOUNT
    assert str0005r2.recipient_document == '69327934075'
    assert str0005r2.recipient_name == 'Joe Doe'
    assert str0005r2.recipient_type == PersonType.INDIVIDUAL
    assert str0005r2.sender_document == '56369416000136'
    assert str0005r2.sender_name == 'ACME Inc'
    assert str0005r2.sender_type == PersonType.BUSINESS
    assert str0005r2.settlement_date == date(2025, 9, 8)
    assert str0005r2.str_control_number == 'STR20250101000000001'
    assert str0005r2.system_domain == 'SPB01'
    assert str0005r2.to_ispb == '00038166'
    assert str0005r2.vendor_timestamp == datetime(2025, 11, 20, 15, 30)


def test_str0005r2_roundtrip() -> None:
    params = make_valid_str0005r2_params()
    str0005r2 = STR0005R2.model_validate(params)
    xml = str0005r2.to_xml()
    str0005r2_from_xml = STR0005R2.from_xml(xml)
    assert str0005r2 == str0005r2_from_xml


def test_str0005r2_from_xml_missing_required_fields() -> None:
    xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/SPB/STR0005.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>31680151250908000000001</NUOp>
        </BCMSG>
        <SISMSG>
            <STR0005R2>
                <CodMsg>STR0005R2</CodMsg>
            </STR0005R2>
        </SISMSG>
    </DOC>
    """

    with pytest.raises(ValidationError) as exc:
        STR0005R2.from_xml(xml)
    missing_fields = extract_missing_fields(exc.value)
    assert missing_fields == {
        'amount',
        'creditor_institution_ispb',
        'debtor_branch',
        'debtor_institution_ispb',
        'purpose',
        'recipient_document',
        'recipient_name',
        'recipient_type',
        'sender_document',
        'sender_name',
        'sender_type',
        'settlement_date',
        'str_control_number',
        'vendor_timestamp',
    }
