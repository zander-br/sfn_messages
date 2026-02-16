from datetime import date, datetime
from decimal import Decimal
from typing import Any

import pytest
from pydantic import ValidationError

from sfn_messages.core.types import CustomerPurpose, PersonType, Priority, StrSettlementStatus
from sfn_messages.str.str0005 import STR0005, STR0005E, STR0005R1, STR0005R2
from tests.conftest import extract_missing_fields


def make_valid_str0005_params() -> dict[str, Any]:
    return {
        'amount': 100.00,
        'creditor_account_number': '123456',
        'creditor_institution_ispb': '60701190',
        'creditor_branch': '0001',
        'creditor_account_type': 'CURRENT',
        'recipient_document': '69327934075',
        'recipient_name': 'Joe Doe',
        'recipient_type': 'INDIVIDUAL',
        'debtor_institution_ispb': '31680151',
        'debtor_branch': '0002',
        'sender_document': '56369416000136',
        'sender_name': 'ACME Inc',
        'sender_type': 'BUSINESS',
        'description': 'Payment for services',
        'institution_control_number': '31680151202509090425',
        'purpose': 'CREDIT_IN_ACCOUNT',
        'scheduled_date': '2025-09-09',
        'scheduled_time': '15:30:00',
        'priority': 'HIGHEST',
        'settlement_date': '2025-09-08',
        'from_ispb': '31680151',
        'to_ispb': '00038166',
        'system_domain': 'SPB01',
        'operation_number': '31680151250908000000001',
    }


def make_valid_str0005r1_params() -> dict[str, Any]:
    return {
        'institution_control_number': '31680151202509090425',
        'debtor_institution_ispb': '31680151',
        'str_control_number': 'STR20250101000000001',
        'str_settlement_status': 'EFFECTIVE',
        'settlement_timestamp': '2025-11-20T15:30:00',
        'settlement_date': '2025-09-08',
        'from_ispb': '31680151',
        'to_ispb': '00038166',
        'system_domain': 'SPB01',
        'operation_number': '31680151250908000000001',
    }


def make_valid_str0005r2_params() -> dict[str, Any]:
    params = make_valid_str0005_params()
    params.pop('scheduled_date')
    params.pop('scheduled_time')
    params.pop('priority')
    params.update(
        {
            'str_control_number': 'STR20250101000000001',
            'vendor_timestamp': '2025-11-20T15:30:00',
        }
    )
    return params


def make_valid_str0005e_params() -> dict[str, Any]:
    params = make_valid_str0005_params()
    params.update(
        {
            'general_error_code': 'EGEN0001',
            'amount_error_code': 'EGEN0042',
            'priority_error_code': 'EGEN0099',
        }
    )
    return params


def test_str0005_valid_model() -> None:
    params = make_valid_str0005_params()
    str0005 = STR0005.model_validate(params)
    assert isinstance(str0005, STR0005)
    assert str0005.amount == Decimal('100.00')
    assert str0005.recipient_type == PersonType.INDIVIDUAL
    assert str0005.sender_type == PersonType.BUSINESS
    assert str0005.purpose == CustomerPurpose.CREDIT_IN_ACCOUNT
    assert str0005.priority == Priority.HIGHEST
    assert str0005.settlement_date == date(2025, 9, 8)


def test_str0005r1_valid_model() -> None:
    params = make_valid_str0005r1_params()
    str0005r1 = STR0005R1.model_validate(params)
    assert isinstance(str0005r1, STR0005R1)
    assert str0005r1.str_control_number == 'STR20250101000000001'
    assert str0005r1.str_settlement_status == StrSettlementStatus.EFFECTIVE


def test_str0005r2_valid_model() -> None:
    params = make_valid_str0005r2_params()
    str0005r2 = STR0005R2.model_validate(params)
    assert isinstance(str0005r2, STR0005R2)
    assert str0005r2.vendor_timestamp == datetime(2025, 11, 20, 15, 30)


def test_str0005e_valid_model() -> None:
    params = make_valid_str0005e_params()
    str0005e = STR0005E.model_validate(params)
    assert isinstance(str0005e, STR0005E)
    assert str0005e.general_error_code == 'EGEN0001'
    assert str0005e.amount_error_code == 'EGEN0042'
    assert str0005e.priority_error_code == 'EGEN0099'


def test_str0005_missing_required_fields() -> None:
    with pytest.raises(ValidationError) as exc:
        STR0005.model_validate({})
    missing_fields = extract_missing_fields(exc.value)
    assert 'amount' in missing_fields
    assert 'debtor_institution_ispb' in missing_fields


def test_str0005r1_missing_required_fields() -> None:
    with pytest.raises(ValidationError) as exc:
        STR0005R1.model_validate({})
    missing_fields = extract_missing_fields(exc.value)
    assert 'str_control_number' in missing_fields


def test_str0005r2_missing_required_fields() -> None:
    with pytest.raises(ValidationError) as exc:
        STR0005R2.model_validate({})
    missing_fields = extract_missing_fields(exc.value)
    assert 'str_control_number' in missing_fields


def test_str0005_business_rules_invalid_documents() -> None:
    params = make_valid_str0005_params()
    params['sender_type'] = 'INDIVIDUAL'
    params['sender_document'] = '56369416000136'

    with pytest.raises(ValidationError) as exc:
        STR0005.model_validate(params)
    assert 'Invalid CPF for sender_type INDIVIDUAL' in str(exc.value)


def test_str0005_to_xml() -> None:
    params = make_valid_str0005_params()
    str0005 = STR0005.model_validate(params)
    xml = str0005.to_xml()

    assert '<CodMsg>STR0005</CodMsg>' in xml
    assert '<VlrLanc>100.0</VlrLanc>' in xml
    assert '<NivelPref>A</NivelPref>' in xml


def test_str0005e_to_xml() -> None:
    params = make_valid_str0005e_params()
    str0005e = STR0005E.model_validate(params)
    xml = str0005e.to_xml()

    assert 'CodErro="EGEN0001"' in xml
    assert '<VlrLanc CodErro="EGEN0042">100.0</VlrLanc>' in xml
    assert '<NivelPref CodErro="EGEN0099">A</NivelPref>' in xml


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
                <NivelPref>A</NivelPref>
                <DtMovto>2025-09-08</DtMovto>
            </STR0005>
        </SISMSG>
    </DOC>
    """
    str0005 = STR0005.from_xml(xml)
    assert str0005.amount == Decimal('100.0')
    assert str0005.sender_name == 'ACME Inc'
    assert str0005.priority == Priority.HIGHEST


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
    assert str0005r1.str_control_number == 'STR20250101000000001'
    assert str0005r1.str_settlement_status == StrSettlementStatus.EFFECTIVE


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
                <DtMovto>2025-09-08</DtMovto>
            </STR0005R2>
        </SISMSG>
    </DOC>
    """
    str0005r2 = STR0005R2.from_xml(xml)
    assert str0005r2.str_control_number == 'STR20250101000000001'
    assert str0005r2.amount == Decimal('100.0')


def test_str0005e_from_xml() -> None:
    xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/SPB/STR0005.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>31680151250908000000001</NUOp>
        </BCMSG>
        <SISMSG>
            <STR0005 CodErro="EGEN0001">
                <CodMsg>STR0005E</CodMsg>
                <NumCtrlIF>31680151202509090425</NumCtrlIF>
                <VlrLanc CodErro="EGEN0042">100.0</VlrLanc>
                <NivelPref CodErro="EGEN0099">A</NivelPref>
            </STR0005>
        </SISMSG>
    </DOC>
    """
    str0005e = STR0005E.from_xml(xml)
    assert str0005e.general_error_code == 'EGEN0001'
    assert str0005e.amount_error_code == 'EGEN0042'
    assert str0005e.priority_error_code == 'EGEN0099'
    assert str0005e.priority == Priority.HIGHEST
