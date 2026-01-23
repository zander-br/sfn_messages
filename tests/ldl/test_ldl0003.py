from datetime import date, datetime
from decimal import Decimal
from typing import Any

import pytest
from pydantic import ValidationError

from sfn_messages.core.types import CreditDebitType, ReconciliationType
from sfn_messages.ldl.ldl0003 import LDL0003, LDL0003E, LDL0003R1, NetResult, NetResultError
from tests.conftest import extract_missing_fields, normalize_xml

NET_RESULT_SIZE = 2


def make_valid_ldl0003_params() -> dict[str, Any]:
    return {
        'from_ispb': '31680151',
        'to_ispb': '00038166',
        'system_domain': 'SPB01',
        'operation_number': '31680151250908000000001',
        'message_code': 'LDL0003',
        'institution_control_number': '123',
        'institution_ispb': '31680151',
        'original_ldl_control_number': '321',
        'ldl_ispb': '31680153',
        'liquidation_date': '2026-01-22',
        'amount': 120.0,
        'credit_debit_type': 'CREDIT',
        'net_result_group': [
            {
                'cnpj': '68689822000165',
                'participant_identifier': '43075534',
                'amount': 60.0,
                'reconciliation_type': 'CONFIRM',
            },
            {
                'cnpj': '39548823000191',
                'participant_identifier': '43075534',
                'amount': 60.0,
                'reconciliation_type': 'CONFIRM',
            },
        ],
        'institution_timestamp': '2026-01-22T16:33:00',
        'settlement_date': '2026-01-22',
    }


def make_valid_ldl0003r1_params() -> dict[str, Any]:
    return {
        'from_ispb': '31680151',
        'to_ispb': '00038166',
        'system_domain': 'SPB01',
        'operation_number': '31680151250908000000001',
        'message_code': 'LDL0003R1',
        'institution_control_number': '123',
        'ldl_ispb': '31680153',
        'ldl_timestamp': '2026-01-22T18:12:00',
        'settlement_date': '2026-01-22',
    }


def make_valid_ldl0003e_params(*, general_error: bool = False) -> dict[str, Any]:
    ldl0003e = {
        'from_ispb': '31680151',
        'to_ispb': '00038166',
        'system_domain': 'SPB01',
        'operation_number': '31680151250908000000001',
        'message_code': 'LDL0003E',
        'institution_control_number': '123',
        'institution_ispb': '31680151',
        'original_ldl_control_number': '321',
        'ldl_ispb': '31680153',
        'liquidation_date': '2026-01-22',
        'amount': 120.0,
        'credit_debit_type': 'CREDIT',
        'net_result_group': [
            {
                'cnpj': '68689822000165',
                'participant_identifier': '43075534',
                'amount': 60.0,
                'reconciliation_type': 'CONFIRM',
            },
            {
                'cnpj': '39548823000191',
                'participant_identifier': '43075534',
                'amount': 60.0,
                'reconciliation_type': 'CONFIRM',
            },
        ],
        'institution_timestamp': '2026-01-22T16:33:00',
        'settlement_date': '2026-01-22',
    }

    if general_error:
        ldl0003e['general_error_code'] = 'EGEN0050'
    else:
        ldl0003e['ldl_ispb_error_code'] = 'ELDL0123'

    return ldl0003e


def test_ldl0003_valid_model() -> None:
    params = make_valid_ldl0003_params()
    ldl0003 = LDL0003.model_validate(params)

    assert isinstance(ldl0003, LDL0003)
    assert ldl0003.message_code == 'LDL0003'
    assert ldl0003.institution_control_number == '123'
    assert ldl0003.institution_ispb == '31680151'
    assert ldl0003.original_ldl_control_number == '321'
    assert ldl0003.ldl_ispb == '31680153'
    assert ldl0003.liquidation_date == date(2026, 1, 22)
    assert ldl0003.amount == Decimal('120.0')
    assert ldl0003.credit_debit_type == CreditDebitType.CREDIT
    assert ldl0003.institution_timestamp == datetime(2026, 1, 22, 16, 33)
    assert ldl0003.settlement_date == date(2026, 1, 22)

    assert len(ldl0003.net_result_group) == NET_RESULT_SIZE
    result1 = ldl0003.net_result_group[0]
    result2 = ldl0003.net_result_group[1]
    assert isinstance(result1, NetResult)
    assert result1.cnpj == '68689822000165'
    assert result1.participant_identifier == '43075534'
    assert result1.amount == Decimal('60.0')
    assert result1.reconciliation_type == ReconciliationType.CONFIRM

    assert isinstance(result2, NetResult)
    assert result2.cnpj == '39548823000191'
    assert result2.participant_identifier == '43075534'
    assert result2.amount == Decimal('60.0')
    assert result2.reconciliation_type == ReconciliationType.CONFIRM


def test_ldl0003r1_valid_model() -> None:
    params = make_valid_ldl0003r1_params()
    ldl0003r1 = LDL0003R1.model_validate(params)

    assert isinstance(ldl0003r1, LDL0003R1)
    assert ldl0003r1.from_ispb == '31680151'
    assert ldl0003r1.to_ispb == '00038166'
    assert ldl0003r1.system_domain == 'SPB01'
    assert ldl0003r1.operation_number == '31680151250908000000001'
    assert ldl0003r1.message_code == 'LDL0003R1'
    assert ldl0003r1.institution_control_number == '123'
    assert ldl0003r1.ldl_ispb == '31680153'
    assert ldl0003r1.ldl_timestamp == datetime(2026, 1, 22, 18, 12)
    assert ldl0003r1.settlement_date == date(2026, 1, 22)


def test_ldl0003e_general_error_valid_model() -> None:
    params = make_valid_ldl0003e_params(general_error=True)
    ldl0003e = LDL0003E.model_validate(params)

    assert isinstance(ldl0003e, LDL0003E)
    assert ldl0003e.message_code == 'LDL0003E'
    assert ldl0003e.institution_control_number == '123'
    assert ldl0003e.institution_ispb == '31680151'
    assert ldl0003e.original_ldl_control_number == '321'
    assert ldl0003e.ldl_ispb == '31680153'
    assert ldl0003e.liquidation_date == date(2026, 1, 22)
    assert ldl0003e.amount == Decimal('120.0')
    assert ldl0003e.credit_debit_type == CreditDebitType.CREDIT
    assert ldl0003e.institution_timestamp == datetime(2026, 1, 22, 16, 33)
    assert ldl0003e.settlement_date == date(2026, 1, 22)
    assert ldl0003e.general_error_code == 'EGEN0050'

    assert len(ldl0003e.net_result_group) == NET_RESULT_SIZE
    result1 = ldl0003e.net_result_group[0]
    result2 = ldl0003e.net_result_group[1]
    assert isinstance(result1, NetResultError)
    assert result1.cnpj == '68689822000165'
    assert result1.participant_identifier == '43075534'
    assert result1.amount == Decimal('60.0')
    assert result1.reconciliation_type == ReconciliationType.CONFIRM

    assert isinstance(result2, NetResultError)
    assert result2.cnpj == '39548823000191'
    assert result2.participant_identifier == '43075534'
    assert result2.amount == Decimal('60.0')
    assert result2.reconciliation_type == ReconciliationType.CONFIRM


def test_ldl0003e_tag_error_valid_model() -> None:
    params = make_valid_ldl0003e_params()
    ldl0003e = LDL0003E.model_validate(params)

    assert isinstance(ldl0003e, LDL0003E)
    assert ldl0003e.message_code == 'LDL0003E'
    assert ldl0003e.institution_control_number == '123'
    assert ldl0003e.institution_ispb == '31680151'
    assert ldl0003e.original_ldl_control_number == '321'
    assert ldl0003e.ldl_ispb == '31680153'
    assert ldl0003e.liquidation_date == date(2026, 1, 22)
    assert ldl0003e.amount == Decimal('120.0')
    assert ldl0003e.credit_debit_type == CreditDebitType.CREDIT
    assert ldl0003e.institution_timestamp == datetime(2026, 1, 22, 16, 33)
    assert ldl0003e.settlement_date == date(2026, 1, 22)
    assert ldl0003e.ldl_ispb_error_code == 'ELDL0123'

    assert len(ldl0003e.net_result_group) == NET_RESULT_SIZE
    result1 = ldl0003e.net_result_group[0]
    result2 = ldl0003e.net_result_group[1]
    assert isinstance(result1, NetResultError)
    assert result1.cnpj == '68689822000165'
    assert result1.participant_identifier == '43075534'
    assert result1.amount == Decimal('60.0')
    assert result1.reconciliation_type == ReconciliationType.CONFIRM

    assert isinstance(result2, NetResultError)
    assert result2.cnpj == '39548823000191'
    assert result2.participant_identifier == '43075534'
    assert result2.amount == Decimal('60.0')
    assert result2.reconciliation_type == ReconciliationType.CONFIRM


def test_ldl0003_missing_required_fields() -> None:
    with pytest.raises(ValidationError) as exc:
        LDL0003.model_validate({})

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
        'liquidation_date',
        'amount',
        'credit_debit_type',
        'institution_timestamp',
        'settlement_date',
    }


def test_ldl0003r1_missing_required_fields() -> None:
    with pytest.raises(ValidationError) as exc:
        LDL0003R1.model_validate({})

    missing_fields = extract_missing_fields(exc.value)
    assert missing_fields == {
        'from_ispb',
        'to_ispb',
        'system_domain',
        'operation_number',
        'institution_control_number',
        'ldl_ispb',
        'ldl_timestamp',
        'settlement_date',
    }


def test_ldl0003_to_xml() -> None:
    params = make_valid_ldl0003_params()
    ldl0003 = LDL0003.model_validate(params)

    xml = ldl0003.to_xml()

    expected_xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/SPB/LDL0003.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>31680151250908000000001</NUOp>
        </BCMSG>
        <SISMSG>
            <LDL0003>
                <CodMsg>LDL0003</CodMsg>
                <NumCtrlIF>123</NumCtrlIF>
                <ISPBIF>31680151</ISPBIF>
                <NumCtrlLDLOr>321</NumCtrlLDLOr>
                <ISPBLDL>31680153</ISPBLDL>
                <DtLiquid>2026-01-22</DtLiquid>
                <VlrLanc>120.0</VlrLanc>
                <TpDeb_Cred>C</TpDeb_Cred>
                <Grupo_LDL0003_ResultLiqd>
                    <CNPJNLiqdant>68689822000165</CNPJNLiqdant>
                    <IdentdPartCamr>43075534</IdentdPartCamr>
                    <VlrResultLiqdNLiqdant>60.0</VlrResultLiqdNLiqdant>
                    <TpConf_Divg>C</TpConf_Divg>
                </Grupo_LDL0003_ResultLiqd>
                <Grupo_LDL0003_ResultLiqd>
                    <CNPJNLiqdant>39548823000191</CNPJNLiqdant>
                    <IdentdPartCamr>43075534</IdentdPartCamr>
                    <VlrResultLiqdNLiqdant>60.0</VlrResultLiqdNLiqdant>
                    <TpConf_Divg>C</TpConf_Divg>
                </Grupo_LDL0003_ResultLiqd>
                <DtHrIF>2026-01-22T16:33:00</DtHrIF>
                <DtMovto>2026-01-22</DtMovto>
            </LDL0003>
        </SISMSG>
    </DOC>
    """
    assert normalize_xml(expected_xml) == normalize_xml(xml)


def test_ldl0003r1_to_xml() -> None:
    params = make_valid_ldl0003r1_params()
    ldl0003r1 = LDL0003R1.model_validate(params)

    xml = ldl0003r1.to_xml()

    expected_xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/SPB/LDL0003.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>31680151250908000000001</NUOp>
        </BCMSG>
        <SISMSG>
            <LDL0003R1>
                <CodMsg>LDL0003R1</CodMsg>
                <NumCtrlIF>123</NumCtrlIF>
                <ISPBLDL>31680153</ISPBLDL>
                <DtHrLDL>2026-01-22T18:12:00</DtHrLDL>
                <DtMovto>2026-01-22</DtMovto>
            </LDL0003R1>
        </SISMSG>
    </DOC>
    """
    assert normalize_xml(expected_xml) == normalize_xml(xml)


def test_ldl0003e_general_error_to_xml() -> None:
    params = make_valid_ldl0003e_params(general_error=True)
    ldl0003e = LDL0003E.model_validate(params)

    xml = ldl0003e.to_xml()

    expected_xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/SPB/LDL0003E.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>31680151250908000000001</NUOp>
        </BCMSG>
        <SISMSG>
            <LDL0003 CodErro="EGEN0050">
                <CodMsg>LDL0003E</CodMsg>
                <NumCtrlIF>123</NumCtrlIF>
                <ISPBIF>31680151</ISPBIF>
                <NumCtrlLDLOr>321</NumCtrlLDLOr>
                <ISPBLDL>31680153</ISPBLDL>
                <DtLiquid>2026-01-22</DtLiquid>
                <VlrLanc>120.0</VlrLanc>
                <TpDeb_Cred>C</TpDeb_Cred>
                <Grupo_LDL0003_ResultLiqd>
                    <CNPJNLiqdant>68689822000165</CNPJNLiqdant>
                    <IdentdPartCamr>43075534</IdentdPartCamr>
                    <VlrResultLiqdNLiqdant>60.0</VlrResultLiqdNLiqdant>
                    <TpConf_Divg>C</TpConf_Divg>
                </Grupo_LDL0003_ResultLiqd>
                <Grupo_LDL0003_ResultLiqd>
                    <CNPJNLiqdant>39548823000191</CNPJNLiqdant>
                    <IdentdPartCamr>43075534</IdentdPartCamr>
                    <VlrResultLiqdNLiqdant>60.0</VlrResultLiqdNLiqdant>
                    <TpConf_Divg>C</TpConf_Divg>
                </Grupo_LDL0003_ResultLiqd>
                <DtHrIF>2026-01-22T16:33:00</DtHrIF>
                <DtMovto>2026-01-22</DtMovto>
            </LDL0003>
        </SISMSG>
    </DOC>
    """
    assert normalize_xml(expected_xml) == normalize_xml(xml)


def test_ldl0003e_tag_error_to_xml() -> None:
    params = make_valid_ldl0003e_params()
    ldl0003e = LDL0003E.model_validate(params)

    xml = ldl0003e.to_xml()

    expected_xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/SPB/LDL0003E.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>31680151250908000000001</NUOp>
        </BCMSG>
        <SISMSG>
            <LDL0003>
                <CodMsg>LDL0003E</CodMsg>
                <NumCtrlIF>123</NumCtrlIF>
                <ISPBIF>31680151</ISPBIF>
                <NumCtrlLDLOr>321</NumCtrlLDLOr>
                <ISPBLDL CodErro="ELDL0123">31680153</ISPBLDL>
                <DtLiquid>2026-01-22</DtLiquid>
                <VlrLanc>120.0</VlrLanc>
                <TpDeb_Cred>C</TpDeb_Cred>
                <Grupo_LDL0003_ResultLiqd>
                    <CNPJNLiqdant>68689822000165</CNPJNLiqdant>
                    <IdentdPartCamr>43075534</IdentdPartCamr>
                    <VlrResultLiqdNLiqdant>60.0</VlrResultLiqdNLiqdant>
                    <TpConf_Divg>C</TpConf_Divg>
                </Grupo_LDL0003_ResultLiqd>
                <Grupo_LDL0003_ResultLiqd>
                    <CNPJNLiqdant>39548823000191</CNPJNLiqdant>
                    <IdentdPartCamr>43075534</IdentdPartCamr>
                    <VlrResultLiqdNLiqdant>60.0</VlrResultLiqdNLiqdant>
                    <TpConf_Divg>C</TpConf_Divg>
                </Grupo_LDL0003_ResultLiqd>
                <DtHrIF>2026-01-22T16:33:00</DtHrIF>
                <DtMovto>2026-01-22</DtMovto>
            </LDL0003>
        </SISMSG>
    </DOC>
    """
    assert normalize_xml(expected_xml) == normalize_xml(xml)


def test_ldl0003_from_xml() -> None:
    xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/SPB/LDL0003.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>31680151250908000000001</NUOp>
        </BCMSG>
        <SISMSG>
            <LDL0003>
                <CodMsg>LDL0003</CodMsg>
                <NumCtrlIF>123</NumCtrlIF>
                <ISPBIF>31680151</ISPBIF>
                <NumCtrlLDLOr>321</NumCtrlLDLOr>
                <ISPBLDL>31680153</ISPBLDL>
                <DtLiquid>2026-01-22</DtLiquid>
                <VlrLanc>120.0</VlrLanc>
                <TpDeb_Cred>C</TpDeb_Cred>
                <Grupo_LDL0003_ResultLiqd>
                    <CNPJNLiqdant>68689822000165</CNPJNLiqdant>
                    <IdentdPartCamr>43075534</IdentdPartCamr>
                    <VlrResultLiqdNLiqdant>60.0</VlrResultLiqdNLiqdant>
                    <TpConf_Divg>C</TpConf_Divg>
                </Grupo_LDL0003_ResultLiqd>
                <Grupo_LDL0003_ResultLiqd>
                    <CNPJNLiqdant>39548823000191</CNPJNLiqdant>
                    <IdentdPartCamr>43075534</IdentdPartCamr>
                    <VlrResultLiqdNLiqdant>60.0</VlrResultLiqdNLiqdant>
                    <TpConf_Divg>C</TpConf_Divg>
                </Grupo_LDL0003_ResultLiqd>
                <DtHrIF>2026-01-22T16:33:00</DtHrIF>
                <DtMovto>2026-01-22</DtMovto>
            </LDL0003>
        </SISMSG>
    </DOC>
    """

    ldl0003 = LDL0003.from_xml(xml)

    assert isinstance(ldl0003, LDL0003)
    assert ldl0003.message_code == 'LDL0003'
    assert ldl0003.institution_control_number == '123'
    assert ldl0003.institution_ispb == '31680151'
    assert ldl0003.original_ldl_control_number == '321'
    assert ldl0003.ldl_ispb == '31680153'
    assert ldl0003.liquidation_date == date(2026, 1, 22)
    assert ldl0003.amount == Decimal('120.0')
    assert ldl0003.credit_debit_type == CreditDebitType.CREDIT
    assert ldl0003.institution_timestamp == datetime(2026, 1, 22, 16, 33)
    assert ldl0003.settlement_date == date(2026, 1, 22)

    assert len(ldl0003.net_result_group) == NET_RESULT_SIZE
    result1 = ldl0003.net_result_group[0]
    result2 = ldl0003.net_result_group[1]
    assert isinstance(result1, NetResult)
    assert result1.cnpj == '68689822000165'
    assert result1.participant_identifier == '43075534'
    assert result1.amount == Decimal('60.0')
    assert result1.reconciliation_type == ReconciliationType.CONFIRM

    assert isinstance(result2, NetResult)
    assert result2.cnpj == '39548823000191'
    assert result2.participant_identifier == '43075534'
    assert result2.amount == Decimal('60.0')
    assert result2.reconciliation_type == ReconciliationType.CONFIRM


def test_ldl0003r1_from_xml() -> None:
    xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/SPB/LDL0003.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>31680151250908000000001</NUOp>
        </BCMSG>
        <SISMSG>
            <LDL0003R1>
                <CodMsg>LDL0003R1</CodMsg>
                <NumCtrlIF>123</NumCtrlIF>
                <ISPBLDL>31680151</ISPBLDL>
                <DtHrLDL>2026-01-22T10:33:00</DtHrLDL>
                <DtMovto>2026-01-22</DtMovto>
            </LDL0003R1>
        </SISMSG>
    </DOC>
    """

    ldl0003r1 = LDL0003R1.from_xml(xml)

    assert isinstance(ldl0003r1, LDL0003R1)
    assert ldl0003r1.from_ispb == '31680151'
    assert ldl0003r1.to_ispb == '00038166'
    assert ldl0003r1.system_domain == 'SPB01'
    assert ldl0003r1.operation_number == '31680151250908000000001'
    assert ldl0003r1.message_code == 'LDL0003R1'
    assert ldl0003r1.institution_control_number == '123'
    assert ldl0003r1.ldl_ispb == '31680151'
    assert ldl0003r1.ldl_timestamp == datetime(2026, 1, 22, 10, 33)
    assert ldl0003r1.settlement_date == date(2026, 1, 22)


def test_ldl0003e_general_error_from_xml() -> None:
    xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/SPB/LDL0003E.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>31680151250908000000001</NUOp>
        </BCMSG>
        <SISMSG>
            <LDL0003 CodErro="EGEN0050">
                <CodMsg>LDL0003E</CodMsg>
                <NumCtrlIF>123</NumCtrlIF>
                <ISPBIF>31680151</ISPBIF>
                <NumCtrlLDLOr>321</NumCtrlLDLOr>
                <ISPBLDL>31680153</ISPBLDL>
                <DtLiquid>2026-01-22</DtLiquid>
                <VlrLanc>120.0</VlrLanc>
                <TpDeb_Cred>C</TpDeb_Cred>
                <Grupo_LDL0003_ResultLiqd>
                    <CNPJNLiqdant>68689822000165</CNPJNLiqdant>
                    <IdentdPartCamr>43075534</IdentdPartCamr>
                    <VlrResultLiqdNLiqdant>60.0</VlrResultLiqdNLiqdant>
                    <TpConf_Divg>C</TpConf_Divg>
                </Grupo_LDL0003_ResultLiqd>
                <Grupo_LDL0003_ResultLiqd>
                    <CNPJNLiqdant>39548823000191</CNPJNLiqdant>
                    <IdentdPartCamr>43075534</IdentdPartCamr>
                    <VlrResultLiqdNLiqdant>60.0</VlrResultLiqdNLiqdant>
                    <TpConf_Divg>C</TpConf_Divg>
                </Grupo_LDL0003_ResultLiqd>
                <DtHrIF>2026-01-22T16:33:00</DtHrIF>
                <DtMovto>2026-01-22</DtMovto>
            </LDL0003>
        </SISMSG>
    </DOC>
    """

    ldl0003e = LDL0003E.from_xml(xml)

    assert isinstance(ldl0003e, LDL0003E)
    assert ldl0003e.message_code == 'LDL0003E'
    assert ldl0003e.institution_control_number == '123'
    assert ldl0003e.institution_ispb == '31680151'
    assert ldl0003e.original_ldl_control_number == '321'
    assert ldl0003e.ldl_ispb == '31680153'
    assert ldl0003e.liquidation_date == date(2026, 1, 22)
    assert ldl0003e.amount == Decimal('120.0')
    assert ldl0003e.credit_debit_type == CreditDebitType.CREDIT
    assert ldl0003e.institution_timestamp == datetime(2026, 1, 22, 16, 33)
    assert ldl0003e.settlement_date == date(2026, 1, 22)
    assert ldl0003e.general_error_code == 'EGEN0050'

    assert len(ldl0003e.net_result_group) == NET_RESULT_SIZE
    result1 = ldl0003e.net_result_group[0]
    result2 = ldl0003e.net_result_group[1]
    assert isinstance(result1, NetResultError)
    assert result1.cnpj == '68689822000165'
    assert result1.participant_identifier == '43075534'
    assert result1.amount == Decimal('60.0')
    assert result1.reconciliation_type == ReconciliationType.CONFIRM

    assert isinstance(result2, NetResultError)
    assert result2.cnpj == '39548823000191'
    assert result2.participant_identifier == '43075534'
    assert result2.amount == Decimal('60.0')
    assert result2.reconciliation_type == ReconciliationType.CONFIRM


def test_ldl0003e_tag_error_from_xml() -> None:
    xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/SPB/LDL0003E.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>31680151250908000000001</NUOp>
        </BCMSG>
        <SISMSG>
            <LDL0003>
                <CodMsg>LDL0003E</CodMsg>
                <NumCtrlIF>123</NumCtrlIF>
                <ISPBIF>31680151</ISPBIF>
                <NumCtrlLDLOr>321</NumCtrlLDLOr>
                <ISPBLDL CodErro="ELDL0123">31680153</ISPBLDL>
                <DtLiquid>2026-01-22</DtLiquid>
                <VlrLanc>120.0</VlrLanc>
                <TpDeb_Cred>C</TpDeb_Cred>
                <Grupo_LDL0003_ResultLiqd>
                    <CNPJNLiqdant>68689822000165</CNPJNLiqdant>
                    <IdentdPartCamr>43075534</IdentdPartCamr>
                    <VlrResultLiqdNLiqdant>60.0</VlrResultLiqdNLiqdant>
                    <TpConf_Divg>C</TpConf_Divg>
                </Grupo_LDL0003_ResultLiqd>
                <Grupo_LDL0003_ResultLiqd>
                    <CNPJNLiqdant>39548823000191</CNPJNLiqdant>
                    <IdentdPartCamr>43075534</IdentdPartCamr>
                    <VlrResultLiqdNLiqdant>60.0</VlrResultLiqdNLiqdant>
                    <TpConf_Divg>C</TpConf_Divg>
                </Grupo_LDL0003_ResultLiqd>
                <DtHrIF>2026-01-22T16:33:00</DtHrIF>
                <DtMovto>2026-01-22</DtMovto>
            </LDL0003>
        </SISMSG>
    </DOC>
    """

    ldl0003e = LDL0003E.from_xml(xml)

    assert isinstance(ldl0003e, LDL0003E)
    assert ldl0003e.message_code == 'LDL0003E'
    assert ldl0003e.institution_control_number == '123'
    assert ldl0003e.institution_ispb == '31680151'
    assert ldl0003e.original_ldl_control_number == '321'
    assert ldl0003e.ldl_ispb == '31680153'
    assert ldl0003e.liquidation_date == date(2026, 1, 22)
    assert ldl0003e.amount == Decimal('120.0')
    assert ldl0003e.credit_debit_type == CreditDebitType.CREDIT
    assert ldl0003e.institution_timestamp == datetime(2026, 1, 22, 16, 33)
    assert ldl0003e.settlement_date == date(2026, 1, 22)
    assert ldl0003e.ldl_ispb_error_code == 'ELDL0123'

    assert len(ldl0003e.net_result_group) == NET_RESULT_SIZE
    result1 = ldl0003e.net_result_group[0]
    result2 = ldl0003e.net_result_group[1]
    assert isinstance(result1, NetResultError)
    assert result1.cnpj == '68689822000165'
    assert result1.participant_identifier == '43075534'
    assert result1.amount == Decimal('60.0')
    assert result1.reconciliation_type == ReconciliationType.CONFIRM

    assert isinstance(result2, NetResultError)
    assert result2.cnpj == '39548823000191'
    assert result2.participant_identifier == '43075534'
    assert result2.amount == Decimal('60.0')
    assert result2.reconciliation_type == ReconciliationType.CONFIRM


def test_ldl0003_roundtrip() -> None:
    params = make_valid_ldl0003_params()

    ldl0003 = LDL0003.model_validate(params)
    xml = ldl0003.to_xml()
    ldl0003_from_xml = LDL0003.from_xml(xml)

    assert ldl0003 == ldl0003_from_xml


def test_ldl0003r1_roundtrip() -> None:
    params = make_valid_ldl0003r1_params()

    ldl0003r1 = LDL0003R1.model_validate(params)
    xml = ldl0003r1.to_xml()
    ldl0003r1_from_xml = LDL0003R1.from_xml(xml)

    assert ldl0003r1 == ldl0003r1_from_xml


def test_ldl0003_from_xml_missing_required_fields() -> None:
    xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/SPB/LDL0003.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>31680151250908000000001</NUOp>
        </BCMSG>
        <SISMSG>
            <LDL0003>
                <CodMsg>LDL0003</CodMsg>
            </LDL0003>
        </SISMSG>
    </DOC>
    """

    with pytest.raises(ValidationError) as exc:
        LDL0003.from_xml(xml)

    missing_fields = extract_missing_fields(exc.value)
    assert missing_fields == {
        'institution_control_number',
        'institution_ispb',
        'original_ldl_control_number',
        'ldl_ispb',
        'liquidation_date',
        'amount',
        'credit_debit_type',
        'institution_timestamp',
        'settlement_date',
    }
