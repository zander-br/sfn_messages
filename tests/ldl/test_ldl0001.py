from datetime import date, datetime
from decimal import Decimal
from typing import Any

import pytest
from pydantic import ValidationError

from sfn_messages.core.types import CreditDebitType, InformationType
from sfn_messages.ldl.ldl0001 import LDL0001, LDL0001E, InformationNetResult, InformationNetResultError
from tests.conftest import extract_missing_fields, normalize_xml

NET_RESULT_SIZE = 2


def make_valid_ldl0001_params() -> dict[str, Any]:
    return {
        'from_ispb': '31680151',
        'to_ispb': '00038166',
        'system_domain': 'SPB01',
        'operation_number': '31680151250908000000001',
        'message_code': 'LDL0001',
        'ldl_control_number': '321',
        'ldl_ispb': '31680153',
        'institution_ispb': '31680151',
        'information_type': 'PRELIMINARY',
        'liquidation_date': '2026-01-22',
        'amount': 120.0,
        'credit_debit_type': 'DEBIT',
        'net_result_group': [
            {
                'cnpj': '68689822000165',
                'participant_identifier': '43075534',
                'amount': 60.0,
            },
            {
                'cnpj': '39548823000191',
                'participant_identifier': '43075534',
                'amount': 60.0,
            },
        ],
        'ldl_timestamp': '2026-01-21T18:01:00',
        'settlement_date': '2026-01-21',
    }


def make_valid_ldl0001e_params(*, general_error: bool = False) -> dict[str, Any]:
    ldl0001e = {
        'from_ispb': '31680151',
        'to_ispb': '00038166',
        'system_domain': 'SPB01',
        'operation_number': '31680151250908000000001',
        'message_code': 'LDL0001E',
        'ldl_control_number': '321',
        'ldl_ispb': '31680153',
        'institution_ispb': '31680151',
        'information_type': 'PRELIMINARY',
        'liquidation_date': '2026-01-22',
        'amount': 120.0,
        'credit_debit_type': 'DEBIT',
        'net_result_group': [
            {
                'cnpj': '68689822000165',
                'participant_identifier': '43075534',
                'amount': 60.0,
            },
            {
                'cnpj': '39548823000191',
                'participant_identifier': '43075534',
                'amount': 60.0,
            },
        ],
        'ldl_timestamp': '2026-01-21T18:01:00',
        'settlement_date': '2026-01-21',
    }

    if general_error:
        ldl0001e['general_error_code'] = 'EGEN0050'
    else:
        ldl0001e['ldl_control_number_error_code'] = 'ELDL0123'

    return ldl0001e


def test_ldl0001_valid_model() -> None:
    params = make_valid_ldl0001_params()
    ldl0001 = LDL0001.model_validate(params)

    assert isinstance(ldl0001, LDL0001)
    assert ldl0001.ldl_control_number == '321'
    assert ldl0001.ldl_ispb == '31680153'
    assert ldl0001.institution_ispb == '31680151'
    assert ldl0001.information_type == InformationType.PRELIMINARY
    assert ldl0001.liquidation_date == date(2026, 1, 22)
    assert ldl0001.amount == Decimal('120.0')
    assert ldl0001.credit_debit_type == CreditDebitType.DEBIT
    assert ldl0001.ldl_timestamp == datetime(2026, 1, 21, 18, 1)
    assert ldl0001.settlement_date == date(2026, 1, 21)

    assert len(ldl0001.net_result_group) == NET_RESULT_SIZE
    result1 = ldl0001.net_result_group[0]
    result2 = ldl0001.net_result_group[1]
    assert isinstance(result1, InformationNetResult)
    assert result1.cnpj == '68689822000165'
    assert result1.participant_identifier == '43075534'
    assert result1.amount == Decimal('60.0')
    assert isinstance(result2, InformationNetResult)
    assert result2.cnpj == '39548823000191'
    assert result2.participant_identifier == '43075534'
    assert result2.amount == Decimal('60.0')


def test_ldl0001e_general_error_valid_model() -> None:
    params = make_valid_ldl0001e_params(general_error=True)
    ldl0001e = LDL0001E.model_validate(params)

    assert isinstance(ldl0001e, LDL0001E)
    assert ldl0001e.ldl_control_number == '321'
    assert ldl0001e.ldl_ispb == '31680153'
    assert ldl0001e.institution_ispb == '31680151'
    assert ldl0001e.information_type == InformationType.PRELIMINARY
    assert ldl0001e.liquidation_date == date(2026, 1, 22)
    assert ldl0001e.amount == Decimal('120.0')
    assert ldl0001e.credit_debit_type == CreditDebitType.DEBIT
    assert ldl0001e.ldl_timestamp == datetime(2026, 1, 21, 18, 1)
    assert ldl0001e.settlement_date == date(2026, 1, 21)
    assert ldl0001e.general_error_code == 'EGEN0050'

    assert len(ldl0001e.net_result_group) == NET_RESULT_SIZE
    result1 = ldl0001e.net_result_group[0]
    result2 = ldl0001e.net_result_group[1]
    assert isinstance(result1, InformationNetResultError)
    assert result1.cnpj == '68689822000165'
    assert result1.participant_identifier == '43075534'
    assert result1.amount == Decimal('60.0')

    assert isinstance(result2, InformationNetResultError)
    assert result2.cnpj == '39548823000191'
    assert result2.participant_identifier == '43075534'
    assert result2.amount == Decimal('60.0')


def test_ldl0001e_tag_error_valid_model() -> None:
    params = make_valid_ldl0001e_params()
    ldl0001e = LDL0001E.model_validate(params)

    assert isinstance(ldl0001e, LDL0001E)
    assert ldl0001e.ldl_control_number == '321'
    assert ldl0001e.ldl_ispb == '31680153'
    assert ldl0001e.institution_ispb == '31680151'
    assert ldl0001e.information_type == InformationType.PRELIMINARY
    assert ldl0001e.liquidation_date == date(2026, 1, 22)
    assert ldl0001e.amount == Decimal('120.0')
    assert ldl0001e.credit_debit_type == CreditDebitType.DEBIT
    assert ldl0001e.ldl_timestamp == datetime(2026, 1, 21, 18, 1)
    assert ldl0001e.settlement_date == date(2026, 1, 21)
    assert ldl0001e.ldl_control_number_error_code == 'ELDL0123'

    assert len(ldl0001e.net_result_group) == NET_RESULT_SIZE
    result1 = ldl0001e.net_result_group[0]
    result2 = ldl0001e.net_result_group[1]
    assert isinstance(result1, InformationNetResultError)
    assert result1.cnpj == '68689822000165'
    assert result1.participant_identifier == '43075534'
    assert result1.amount == Decimal('60.0')
    assert isinstance(result2, InformationNetResultError)
    assert result2.cnpj == '39548823000191'
    assert result2.participant_identifier == '43075534'
    assert result2.amount == Decimal('60.0')


def test_ldl0001_missing_required_fields() -> None:
    with pytest.raises(ValidationError) as exc:
        LDL0001.model_validate({})

    missing_fields = extract_missing_fields(exc.value)
    assert missing_fields == {
        'from_ispb',
        'to_ispb',
        'system_domain',
        'operation_number',
        'ldl_control_number',
        'ldl_ispb',
        'institution_ispb',
        'information_type',
        'liquidation_date',
        'amount',
        'credit_debit_type',
        'ldl_timestamp',
        'settlement_date',
    }


def test_ldl0001_to_xml() -> None:
    params = make_valid_ldl0001_params()
    ldl0001 = LDL0001.model_validate(params)

    xml = ldl0001.to_xml()

    expected_xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/SPB/LDL0001.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>31680151250908000000001</NUOp>
        </BCMSG>
        <SISMSG>
            <LDL0001>
                <CodMsg>LDL0001</CodMsg>
                <NumCtrlLDL>321</NumCtrlLDL>
                <ISPBLDL>31680153</ISPBLDL>
                <ISPBIF>31680151</ISPBIF>
                <TpInf>P</TpInf>
                <DtLiquid>2026-01-22</DtLiquid>
                <VlrLanc>120.0</VlrLanc>
                <TpDeb_Cred>D</TpDeb_Cred>
                <Grupo_LDL0001_ResultLiqd>
                    <CNPJNLiqdant>68689822000165</CNPJNLiqdant>
                    <IdentdPartCamr>43075534</IdentdPartCamr>
                    <VlrResultLiqdNLiqdant>60.0</VlrResultLiqdNLiqdant>
                </Grupo_LDL0001_ResultLiqd>
                <Grupo_LDL0001_ResultLiqd>
                    <CNPJNLiqdant>39548823000191</CNPJNLiqdant>
                    <IdentdPartCamr>43075534</IdentdPartCamr>
                    <VlrResultLiqdNLiqdant>60.0</VlrResultLiqdNLiqdant>
                </Grupo_LDL0001_ResultLiqd>
                <DtHrLDL>2026-01-21T18:01:00</DtHrLDL>
                <DtMovto>2026-01-21</DtMovto>
            </LDL0001>
        </SISMSG>
    </DOC>
    """
    assert normalize_xml(expected_xml) == normalize_xml(xml)


def test_ldl0001e_general_error_to_xml() -> None:
    params = make_valid_ldl0001e_params(general_error=True)
    ldl0001e = LDL0001E.model_validate(params)

    xml = ldl0001e.to_xml()

    expected_xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/SPB/LDL0001E.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>31680151250908000000001</NUOp>
        </BCMSG>
        <SISMSG>
            <LDL0001 CodErro="EGEN0050">
                <CodMsg>LDL0001E</CodMsg>
                <NumCtrlLDL>321</NumCtrlLDL>
                <ISPBLDL>31680153</ISPBLDL>
                <ISPBIF>31680151</ISPBIF>
                <TpInf>P</TpInf>
                <DtLiquid>2026-01-22</DtLiquid>
                <VlrLanc>120.0</VlrLanc>
                <TpDeb_Cred>D</TpDeb_Cred>
                <Grupo_LDL0001_ResultLiqd>
                    <CNPJNLiqdant>68689822000165</CNPJNLiqdant>
                    <IdentdPartCamr>43075534</IdentdPartCamr>
                    <VlrResultLiqdNLiqdant>60.0</VlrResultLiqdNLiqdant>
                </Grupo_LDL0001_ResultLiqd>
                <Grupo_LDL0001_ResultLiqd>
                    <CNPJNLiqdant>39548823000191</CNPJNLiqdant>
                    <IdentdPartCamr>43075534</IdentdPartCamr>
                    <VlrResultLiqdNLiqdant>60.0</VlrResultLiqdNLiqdant>
                </Grupo_LDL0001_ResultLiqd>
                <DtHrLDL>2026-01-21T18:01:00</DtHrLDL>
                <DtMovto>2026-01-21</DtMovto>
            </LDL0001>
        </SISMSG>
    </DOC>
    """
    assert normalize_xml(expected_xml) == normalize_xml(xml)


def test_ldl0001e_tag_error_to_xml() -> None:
    params = make_valid_ldl0001e_params()
    ldl0001e = LDL0001E.model_validate(params)

    xml = ldl0001e.to_xml()

    expected_xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/SPB/LDL0001E.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>31680151250908000000001</NUOp>
        </BCMSG>
        <SISMSG>
            <LDL0001>
                <CodMsg>LDL0001E</CodMsg>
                <NumCtrlLDL CodErro="ELDL0123">321</NumCtrlLDL>
                <ISPBLDL>31680153</ISPBLDL>
                <ISPBIF>31680151</ISPBIF>
                <TpInf>P</TpInf>
                <DtLiquid>2026-01-22</DtLiquid>
                <VlrLanc>120.0</VlrLanc>
                <TpDeb_Cred>D</TpDeb_Cred>
                <Grupo_LDL0001_ResultLiqd>
                    <CNPJNLiqdant>68689822000165</CNPJNLiqdant>
                    <IdentdPartCamr>43075534</IdentdPartCamr>
                    <VlrResultLiqdNLiqdant>60.0</VlrResultLiqdNLiqdant>
                </Grupo_LDL0001_ResultLiqd>
                <Grupo_LDL0001_ResultLiqd>
                    <CNPJNLiqdant>39548823000191</CNPJNLiqdant>
                    <IdentdPartCamr>43075534</IdentdPartCamr>
                    <VlrResultLiqdNLiqdant>60.0</VlrResultLiqdNLiqdant>
                </Grupo_LDL0001_ResultLiqd>
                <DtHrLDL>2026-01-21T18:01:00</DtHrLDL>
                <DtMovto>2026-01-21</DtMovto>
            </LDL0001>
        </SISMSG>
    </DOC>
    """
    assert normalize_xml(expected_xml) == normalize_xml(xml)


def test_ldl0001_from_xml() -> None:
    xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/SPB/LDL0001.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>31680151250908000000001</NUOp>
        </BCMSG>
        <SISMSG>
            <LDL0001>
                <CodMsg>LDL0001</CodMsg>
                <NumCtrlLDL>321</NumCtrlLDL>
                <ISPBLDL>31680153</ISPBLDL>
                <ISPBIF>31680151</ISPBIF>
                <TpInf>P</TpInf>
                <DtLiquid>2026-01-22</DtLiquid>
                <VlrLanc>120.0</VlrLanc>
                <TpDeb_Cred>D</TpDeb_Cred>
                <Grupo_LDL0001_ResultLiqd>
                    <CNPJNLiqdant>68689822000165</CNPJNLiqdant>
                    <IdentdPartCamr>43075534</IdentdPartCamr>
                    <VlrResultLiqdNLiqdant>60.0</VlrResultLiqdNLiqdant>
                </Grupo_LDL0001_ResultLiqd>
                <Grupo_LDL0001_ResultLiqd>
                    <CNPJNLiqdant>39548823000191</CNPJNLiqdant>
                    <IdentdPartCamr>43075534</IdentdPartCamr>
                    <VlrResultLiqdNLiqdant>60.0</VlrResultLiqdNLiqdant>
                </Grupo_LDL0001_ResultLiqd>
                <DtHrLDL>2026-01-21T18:01:00</DtHrLDL>
                <DtMovto>2026-01-21</DtMovto>
            </LDL0001>
        </SISMSG>
    </DOC>
    """

    ldl0001 = LDL0001.from_xml(xml)

    assert isinstance(ldl0001, LDL0001)
    assert ldl0001.ldl_control_number == '321'
    assert ldl0001.ldl_ispb == '31680153'
    assert ldl0001.institution_ispb == '31680151'
    assert ldl0001.information_type == InformationType.PRELIMINARY
    assert ldl0001.liquidation_date == date(2026, 1, 22)
    assert ldl0001.amount == Decimal('120.0')
    assert ldl0001.credit_debit_type == CreditDebitType.DEBIT
    assert ldl0001.ldl_timestamp == datetime(2026, 1, 21, 18, 1)
    assert ldl0001.settlement_date == date(2026, 1, 21)

    assert len(ldl0001.net_result_group) == NET_RESULT_SIZE
    result1 = ldl0001.net_result_group[0]
    result2 = ldl0001.net_result_group[1]
    assert isinstance(result1, InformationNetResult)
    assert result1.cnpj == '68689822000165'
    assert result1.participant_identifier == '43075534'
    assert result1.amount == Decimal('60.0')
    assert isinstance(result2, InformationNetResult)
    assert result2.cnpj == '39548823000191'
    assert result2.participant_identifier == '43075534'
    assert result2.amount == Decimal('60.0')


def test_ldl0001e_general_error_from_xml() -> None:
    xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/SPB/LDL0001E.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>31680151250908000000001</NUOp>
        </BCMSG>
        <SISMSG>
            <LDL0001 CodErro="EGEN0050">
                <CodMsg>LDL0001E</CodMsg>
                <NumCtrlLDL>321</NumCtrlLDL>
                <ISPBLDL>31680153</ISPBLDL>
                <ISPBIF>31680151</ISPBIF>
                <TpInf>P</TpInf>
                <DtLiquid>2026-01-22</DtLiquid>
                <VlrLanc>120.0</VlrLanc>
                <TpDeb_Cred>D</TpDeb_Cred>
                <Grupo_LDL0001_ResultLiqd>
                    <CNPJNLiqdant>68689822000165</CNPJNLiqdant>
                    <IdentdPartCamr>43075534</IdentdPartCamr>
                    <VlrResultLiqdNLiqdant>60.0</VlrResultLiqdNLiqdant>
                </Grupo_LDL0001_ResultLiqd>
                <Grupo_LDL0001_ResultLiqd>
                    <CNPJNLiqdant>39548823000191</CNPJNLiqdant>
                    <IdentdPartCamr>43075534</IdentdPartCamr>
                    <VlrResultLiqdNLiqdant>60.0</VlrResultLiqdNLiqdant>
                </Grupo_LDL0001_ResultLiqd>
                <DtHrLDL>2026-01-21T18:01:00</DtHrLDL>
                <DtMovto>2026-01-21</DtMovto>
            </LDL0001>
        </SISMSG>
    </DOC>
    """

    ldl0001e = LDL0001E.from_xml(xml)

    assert isinstance(ldl0001e, LDL0001E)
    assert ldl0001e.ldl_control_number == '321'
    assert ldl0001e.ldl_ispb == '31680153'
    assert ldl0001e.institution_ispb == '31680151'
    assert ldl0001e.information_type == InformationType.PRELIMINARY
    assert ldl0001e.liquidation_date == date(2026, 1, 22)
    assert ldl0001e.amount == Decimal('120.0')
    assert ldl0001e.credit_debit_type == CreditDebitType.DEBIT
    assert ldl0001e.ldl_timestamp == datetime(2026, 1, 21, 18, 1)
    assert ldl0001e.settlement_date == date(2026, 1, 21)
    assert ldl0001e.general_error_code == 'EGEN0050'

    assert len(ldl0001e.net_result_group) == NET_RESULT_SIZE
    result1 = ldl0001e.net_result_group[0]
    result2 = ldl0001e.net_result_group[1]
    assert isinstance(result1, InformationNetResultError)
    assert result1.cnpj == '68689822000165'
    assert result1.participant_identifier == '43075534'
    assert result1.amount == Decimal('60.0')
    assert isinstance(result2, InformationNetResultError)
    assert result2.cnpj == '39548823000191'
    assert result2.participant_identifier == '43075534'
    assert result2.amount == Decimal('60.0')


def test_ldl0001e_tag_error_from_xml() -> None:
    xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/SPB/LDL0001E.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>31680151250908000000001</NUOp>
        </BCMSG>
        <SISMSG>
            <LDL0001>
                <CodMsg>LDL0001E</CodMsg>
                <NumCtrlLDL CodErro="ELDL0123">321</NumCtrlLDL>
                <ISPBLDL>31680153</ISPBLDL>
                <ISPBIF>31680151</ISPBIF>
                <TpInf>P</TpInf>
                <DtLiquid>2026-01-22</DtLiquid>
                <VlrLanc>120.0</VlrLanc>
                <TpDeb_Cred>D</TpDeb_Cred>
                <Grupo_LDL0001_ResultLiqd>
                    <CNPJNLiqdant>68689822000165</CNPJNLiqdant>
                    <IdentdPartCamr>43075534</IdentdPartCamr>
                    <VlrResultLiqdNLiqdant>60.0</VlrResultLiqdNLiqdant>
                </Grupo_LDL0001_ResultLiqd>
                <Grupo_LDL0001_ResultLiqd>
                    <CNPJNLiqdant>39548823000191</CNPJNLiqdant>
                    <IdentdPartCamr>43075534</IdentdPartCamr>
                    <VlrResultLiqdNLiqdant>60.0</VlrResultLiqdNLiqdant>
                </Grupo_LDL0001_ResultLiqd>
                <DtHrLDL>2026-01-21T18:01:00</DtHrLDL>
                <DtMovto>2026-01-21</DtMovto>
            </LDL0001>
        </SISMSG>
    </DOC>
    """

    ldl0001e = LDL0001E.from_xml(xml)

    assert isinstance(ldl0001e, LDL0001E)
    assert ldl0001e.ldl_control_number == '321'
    assert ldl0001e.ldl_ispb == '31680153'
    assert ldl0001e.institution_ispb == '31680151'
    assert ldl0001e.information_type == InformationType.PRELIMINARY
    assert ldl0001e.liquidation_date == date(2026, 1, 22)
    assert ldl0001e.amount == Decimal('120.0')
    assert ldl0001e.credit_debit_type == CreditDebitType.DEBIT
    assert ldl0001e.ldl_timestamp == datetime(2026, 1, 21, 18, 1)
    assert ldl0001e.settlement_date == date(2026, 1, 21)
    assert ldl0001e.ldl_control_number_error_code == 'ELDL0123'

    assert len(ldl0001e.net_result_group) == NET_RESULT_SIZE
    result1 = ldl0001e.net_result_group[0]
    result2 = ldl0001e.net_result_group[1]
    assert isinstance(result1, InformationNetResultError)
    assert result1.cnpj == '68689822000165'
    assert result1.participant_identifier == '43075534'
    assert result1.amount == Decimal('60.0')
    assert isinstance(result2, InformationNetResultError)
    assert result2.cnpj == '39548823000191'
    assert result2.participant_identifier == '43075534'
    assert result2.amount == Decimal('60.0')


def test_ldl0001_roundtrip() -> None:
    params = make_valid_ldl0001_params()

    ldl0001 = LDL0001.model_validate(params)
    xml = ldl0001.to_xml()
    ldl0001_from_xml = LDL0001.from_xml(xml)

    assert ldl0001 == ldl0001_from_xml


def test_ldl0001_from_xml_missing_required_fields() -> None:
    xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/SPB/LDL0001.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>31680151250908000000001</NUOp>
        </BCMSG>
        <SISMSG>
            <LDL0001>
                <CodMsg>LDL0001</CodMsg>
            </LDL0001>
        </SISMSG>
    </DOC>
    """

    with pytest.raises(ValidationError) as exc:
        LDL0001.from_xml(xml)

    missing_fields = extract_missing_fields(exc.value)
    assert missing_fields == {
        'ldl_control_number',
        'ldl_ispb',
        'institution_ispb',
        'information_type',
        'liquidation_date',
        'amount',
        'credit_debit_type',
        'ldl_timestamp',
        'settlement_date',
    }
