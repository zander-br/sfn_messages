from datetime import date, datetime
from decimal import Decimal
from typing import Any

import pytest
from pydantic import ValidationError

from sfn_messages.core.types import CreditDebitType, GridCode, ProductCode
from sfn_messages.ldl.ldl0002 import LDL0002, LDL0002E, LDL0002R1, NetResult, NetResultError
from tests.conftest import extract_missing_fields, normalize_xml

NET_RESULT_SIZE = 2


def make_valid_ldl0002_params() -> dict[str, Any]:
    return {
        'from_ispb': '31680151',
        'to_ispb': '00038166',
        'system_domain': 'SPB01',
        'operation_number': '31680151250908000000001',
        'message_code': 'LDL0002',
        'ldl_control_number': '321',
        'ldl_ispb': '31680153',
        'settlement_cycle_seq_num': '22',
        'product_code': 'AMEX_CREDIT_CARD',
        'liquidation_date': '2026-01-22',
        'code': 'PAYMENT_ORDER_SCHEDULING',
        'net_result_group': [
            {'cnpj': '68689822000165', 'participant_ispb': '43075534', 'amount': 60.0, 'credit_debit_type': 'DEBIT'},
            {'cnpj': '39548823000191', 'participant_ispb': '43075534', 'amount': 60.0, 'credit_debit_type': 'DEBIT'},
        ],
        'ldl_timestamp': '2026-01-22T10:12:00',
        'settlement_date': '2026-01-22',
    }


def make_valid_ldl0002r1_params() -> dict[str, Any]:
    return {
        'from_ispb': '31680151',
        'to_ispb': '00038166',
        'system_domain': 'SPB01',
        'operation_number': '31680151250908000000001',
        'message_code': 'LDL0002R1',
        'ldl_control_number': '123',
        'ldl_ispb': '31680151',
        'vendor_timestamp': '2026-01-22T10:33:00',
        'settlement_date': '2026-01-22',
    }


def make_valid_ldl0002e_params(*, general_error: bool = False) -> dict[str, Any]:
    ldl0002e = {
        'from_ispb': '31680151',
        'to_ispb': '00038166',
        'system_domain': 'SPB01',
        'operation_number': '31680151250908000000001',
        'message_code': 'LDL0002E',
        'ldl_control_number': '321',
        'ldl_ispb': '31680153',
        'settlement_cycle_seq_num': '22',
        'product_code': 'AMEX_CREDIT_CARD',
        'liquidation_date': '2026-01-22',
        'code': 'PAYMENT_ORDER_SCHEDULING',
        'net_result_group': [
            {'participant_ispb': '43075534', 'amount': 60.0, 'cnpj': '68689822000165', 'credit_debit_type': 'DEBIT'},
            {'participant_ispb': '43075534', 'amount': 60.0, 'cnpj': '39548823000191', 'credit_debit_type': 'DEBIT'},
        ],
        'ldl_timestamp': '2026-01-22T10:12:00',
        'settlement_date': '2026-01-22',
    }

    if general_error:
        ldl0002e['general_error_code'] = 'EGEN0050'
    else:
        ldl0002e['ldl_ispb_error_code'] = 'ELDL0123'

    return ldl0002e


def test_ldl0002_valid_model() -> None:
    params = make_valid_ldl0002_params()
    ldl0002 = LDL0002.model_validate(params)

    assert isinstance(ldl0002, LDL0002)
    assert ldl0002.message_code == 'LDL0002'
    assert ldl0002.ldl_control_number == '321'
    assert ldl0002.ldl_ispb == '31680153'
    assert ldl0002.settlement_cycle_seq_num == '22'
    assert ldl0002.product_code == ProductCode.AMEX_CREDIT_CARD
    assert ldl0002.liquidation_date == date(2026, 1, 22)
    assert ldl0002.code == GridCode.PAYMENT_ORDER_SCHEDULING
    assert ldl0002.ldl_timestamp == datetime(2026, 1, 22, 10, 12)
    assert ldl0002.settlement_date == date(2026, 1, 22)

    assert len(ldl0002.net_result_group) == NET_RESULT_SIZE
    result1 = ldl0002.net_result_group[0]
    result2 = ldl0002.net_result_group[1]
    assert isinstance(result1, NetResult)
    assert result1.participant_ispb == '43075534'
    assert result1.amount == Decimal('60.0')
    assert result1.cnpj == '68689822000165'
    assert result1.credit_debit_type == CreditDebitType.DEBIT

    assert isinstance(result2, NetResult)
    assert result2.participant_ispb == '43075534'
    assert result2.amount == Decimal('60.0')
    assert result2.cnpj == '39548823000191'
    assert result2.credit_debit_type == CreditDebitType.DEBIT


def test_ldl0002r1_valid_model() -> None:
    params = make_valid_ldl0002r1_params()
    ldl0002r1 = LDL0002R1.model_validate(params)

    assert isinstance(ldl0002r1, LDL0002R1)
    assert ldl0002r1.from_ispb == '31680151'
    assert ldl0002r1.to_ispb == '00038166'
    assert ldl0002r1.system_domain == 'SPB01'
    assert ldl0002r1.operation_number == '31680151250908000000001'
    assert ldl0002r1.message_code == 'LDL0002R1'
    assert ldl0002r1.ldl_control_number == '123'
    assert ldl0002r1.ldl_ispb == '31680151'
    assert ldl0002r1.vendor_timestamp == datetime(2026, 1, 22, 10, 33)
    assert ldl0002r1.settlement_date == date(2026, 1, 22)


def test_ldl0002e_general_error_valid_model() -> None:
    params = make_valid_ldl0002e_params(general_error=True)
    ldl0002e = LDL0002E.model_validate(params)

    assert isinstance(ldl0002e, LDL0002E)
    assert ldl0002e.message_code == 'LDL0002E'
    assert ldl0002e.ldl_control_number == '321'
    assert ldl0002e.ldl_ispb == '31680153'
    assert ldl0002e.settlement_cycle_seq_num == '22'
    assert ldl0002e.product_code == ProductCode.AMEX_CREDIT_CARD
    assert ldl0002e.liquidation_date == date(2026, 1, 22)
    assert ldl0002e.code == GridCode.PAYMENT_ORDER_SCHEDULING
    assert ldl0002e.ldl_timestamp == datetime(2026, 1, 22, 10, 12)
    assert ldl0002e.settlement_date == date(2026, 1, 22)
    assert ldl0002e.general_error_code == 'EGEN0050'

    assert len(ldl0002e.net_result_group) == NET_RESULT_SIZE
    result1 = ldl0002e.net_result_group[0]
    result2 = ldl0002e.net_result_group[1]
    assert isinstance(result1, NetResultError)
    assert result1.participant_ispb == '43075534'
    assert result1.amount == Decimal('60.0')
    assert result1.cnpj == '68689822000165'
    assert result1.credit_debit_type == CreditDebitType.DEBIT

    assert isinstance(result2, NetResultError)
    assert result2.participant_ispb == '43075534'
    assert result2.amount == Decimal('60.0')
    assert result2.cnpj == '39548823000191'
    assert result2.credit_debit_type == CreditDebitType.DEBIT


def test_ldl0002e_tag_error_valid_model() -> None:
    params = make_valid_ldl0002e_params()
    ldl0002e = LDL0002E.model_validate(params)

    assert isinstance(ldl0002e, LDL0002E)
    assert ldl0002e.message_code == 'LDL0002E'
    assert ldl0002e.ldl_control_number == '321'
    assert ldl0002e.ldl_ispb == '31680153'
    assert ldl0002e.settlement_cycle_seq_num == '22'
    assert ldl0002e.product_code == ProductCode.AMEX_CREDIT_CARD
    assert ldl0002e.liquidation_date == date(2026, 1, 22)
    assert ldl0002e.code == GridCode.PAYMENT_ORDER_SCHEDULING
    assert ldl0002e.ldl_timestamp == datetime(2026, 1, 22, 10, 12)
    assert ldl0002e.settlement_date == date(2026, 1, 22)
    assert ldl0002e.ldl_ispb_error_code == 'ELDL0123'

    assert len(ldl0002e.net_result_group) == NET_RESULT_SIZE
    result1 = ldl0002e.net_result_group[0]
    result2 = ldl0002e.net_result_group[1]
    assert isinstance(result1, NetResultError)
    assert result1.participant_ispb == '43075534'
    assert result1.amount == Decimal('60.0')
    assert result1.cnpj == '68689822000165'
    assert result1.credit_debit_type == CreditDebitType.DEBIT

    assert isinstance(result2, NetResultError)
    assert result2.participant_ispb == '43075534'
    assert result2.amount == Decimal('60.0')
    assert result2.cnpj == '39548823000191'
    assert result2.credit_debit_type == CreditDebitType.DEBIT


def test_ldl0002_missing_required_fields() -> None:
    with pytest.raises(ValidationError) as exc:
        LDL0002.model_validate({})

    missing_fields = extract_missing_fields(exc.value)
    assert missing_fields == {
        'from_ispb',
        'to_ispb',
        'system_domain',
        'operation_number',
        'ldl_control_number',
        'ldl_ispb',
        'liquidation_date',
        'ldl_timestamp',
        'settlement_date',
    }


def test_ldl0002r1_missing_required_fields() -> None:
    with pytest.raises(ValidationError) as exc:
        LDL0002R1.model_validate({})

    missing_fields = extract_missing_fields(exc.value)
    assert missing_fields == {
        'from_ispb',
        'to_ispb',
        'system_domain',
        'operation_number',
        'ldl_control_number',
        'ldl_ispb',
        'vendor_timestamp',
        'settlement_date',
    }


def test_ldl0002_to_xml() -> None:
    params = make_valid_ldl0002_params()
    ldl0002 = LDL0002.model_validate(params)

    xml = ldl0002.to_xml()

    expected_xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/SPB/LDL0002.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>31680151250908000000001</NUOp>
        </BCMSG>
        <SISMSG>
            <LDL0002>
                <CodMsg>LDL0002</CodMsg>
                <NumCtrlLDL>321</NumCtrlLDL>
                <ISPBLDL>31680153</ISPBLDL>
                <NumSeqCicloLiquid>22</NumSeqCicloLiquid>
                <CodProdt>ACC</CodProdt>
                <DtLiquid>2026-01-22</DtLiquid>
                <CodGrd>AGE01</CodGrd>
                <Grupo_LDL0002_ResultLiqd>
                    <ISPBPart>43075534</ISPBPart>
                    <VlrLanc>60.0</VlrLanc>
                    <CNPJNLiqdant>68689822000165</CNPJNLiqdant>
                    <TpDeb_Cred>D</TpDeb_Cred>
                </Grupo_LDL0002_ResultLiqd>
                <Grupo_LDL0002_ResultLiqd>
                    <ISPBPart>43075534</ISPBPart>
                    <VlrLanc>60.0</VlrLanc>
                    <CNPJNLiqdant>39548823000191</CNPJNLiqdant>
                    <TpDeb_Cred>D</TpDeb_Cred>
                </Grupo_LDL0002_ResultLiqd>
                <DtHrLDL>2026-01-22T10:12:00</DtHrLDL>
                <DtMovto>2026-01-22</DtMovto>
            </LDL0002>
        </SISMSG>
    </DOC>
    """
    assert normalize_xml(expected_xml) == normalize_xml(xml)


def test_ldl0002r1_to_xml() -> None:
    params = make_valid_ldl0002r1_params()
    ldl0002r1 = LDL0002R1.model_validate(params)

    xml = ldl0002r1.to_xml()

    expected_xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/SPB/LDL0002.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>31680151250908000000001</NUOp>
        </BCMSG>
        <SISMSG>
            <LDL0002R1>
                <CodMsg>LDL0002R1</CodMsg>
                <NumCtrlLDL>123</NumCtrlLDL>
                <ISPBLDL>31680151</ISPBLDL>
                <DtHrBC>2026-01-22T10:33:00</DtHrBC>
                <DtMovto>2026-01-22</DtMovto>
            </LDL0002R1>
        </SISMSG>
    </DOC>
    """
    assert normalize_xml(expected_xml) == normalize_xml(xml)


def test_ldl0002e_general_error_to_xml() -> None:
    params = make_valid_ldl0002e_params(general_error=True)
    ldl0002e = LDL0002E.model_validate(params)

    xml = ldl0002e.to_xml()

    expected_xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/SPB/LDL0002E.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>31680151250908000000001</NUOp>
        </BCMSG>
        <SISMSG>
            <LDL0002 CodErro="EGEN0050">
                <CodMsg>LDL0002E</CodMsg>
                <NumCtrlLDL>321</NumCtrlLDL>
                <ISPBLDL>31680153</ISPBLDL>
                <NumSeqCicloLiquid>22</NumSeqCicloLiquid>
                <CodProdt>ACC</CodProdt>
                <DtLiquid>2026-01-22</DtLiquid>
                <CodGrd>AGE01</CodGrd>
                <Grupo_LDL0002_ResultLiqd>
                    <ISPBPart>43075534</ISPBPart>
                    <VlrLanc>60.0</VlrLanc>
                    <CNPJNLiqdant>68689822000165</CNPJNLiqdant>
                    <TpDeb_Cred>D</TpDeb_Cred>
                </Grupo_LDL0002_ResultLiqd>
                <Grupo_LDL0002_ResultLiqd>
                    <ISPBPart>43075534</ISPBPart>
                    <VlrLanc>60.0</VlrLanc>
                    <CNPJNLiqdant>39548823000191</CNPJNLiqdant>
                    <TpDeb_Cred>D</TpDeb_Cred>
                </Grupo_LDL0002_ResultLiqd>
                <DtHrLDL>2026-01-22T10:12:00</DtHrLDL>
                <DtMovto>2026-01-22</DtMovto>
            </LDL0002>
        </SISMSG>
    </DOC>
    """
    assert normalize_xml(expected_xml) == normalize_xml(xml)


def test_ldl0002e_tag_error_to_xml() -> None:
    params = make_valid_ldl0002e_params()
    ldl0002e = LDL0002E.model_validate(params)

    xml = ldl0002e.to_xml()

    expected_xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/SPB/LDL0002E.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>31680151250908000000001</NUOp>
        </BCMSG>
        <SISMSG>
            <LDL0002>
                <CodMsg>LDL0002E</CodMsg>
                <NumCtrlLDL>321</NumCtrlLDL>
                <ISPBLDL CodErro="ELDL0123">31680153</ISPBLDL>
                <NumSeqCicloLiquid>22</NumSeqCicloLiquid>
                <CodProdt>ACC</CodProdt>
                <DtLiquid>2026-01-22</DtLiquid>
                <CodGrd>AGE01</CodGrd>
                <Grupo_LDL0002_ResultLiqd>
                    <ISPBPart>43075534</ISPBPart>
                    <VlrLanc>60.0</VlrLanc>
                    <CNPJNLiqdant>68689822000165</CNPJNLiqdant>
                    <TpDeb_Cred>D</TpDeb_Cred>
                </Grupo_LDL0002_ResultLiqd>
                <Grupo_LDL0002_ResultLiqd>
                    <ISPBPart>43075534</ISPBPart>
                    <VlrLanc>60.0</VlrLanc>
                    <CNPJNLiqdant>39548823000191</CNPJNLiqdant>
                    <TpDeb_Cred>D</TpDeb_Cred>
                </Grupo_LDL0002_ResultLiqd>
                <DtHrLDL>2026-01-22T10:12:00</DtHrLDL>
                <DtMovto>2026-01-22</DtMovto>
            </LDL0002>
        </SISMSG>
    </DOC>
    """
    assert normalize_xml(expected_xml) == normalize_xml(xml)


def test_ldl0004_from_xml() -> None:
    xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/SPB/LDL0002.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>31680151250908000000001</NUOp>
        </BCMSG>
        <SISMSG>
            <LDL0002>
                <CodMsg>LDL0002</CodMsg>
                <NumCtrlLDL>321</NumCtrlLDL>
                <ISPBLDL>31680153</ISPBLDL>
                <NumSeqCicloLiquid>22</NumSeqCicloLiquid>
                <CodProdt>ACC</CodProdt>
                <DtLiquid>2026-01-22</DtLiquid>
                <CodGrd>AGE01</CodGrd>
                <Grupo_LDL0002_ResultLiqd>
                    <ISPBPart>43075534</ISPBPart>
                    <VlrLanc>60.0</VlrLanc>
                    <CNPJNLiqdant>68689822000165</CNPJNLiqdant>
                    <TpDeb_Cred>D</TpDeb_Cred>
                </Grupo_LDL0002_ResultLiqd>
                <Grupo_LDL0002_ResultLiqd>
                    <ISPBPart>43075534</ISPBPart>
                    <VlrLanc>60.0</VlrLanc>
                    <CNPJNLiqdant>39548823000191</CNPJNLiqdant>
                    <TpDeb_Cred>D</TpDeb_Cred>
                </Grupo_LDL0002_ResultLiqd>
                <DtHrLDL>2026-01-22T10:12:00</DtHrLDL>
                <DtMovto>2026-01-22</DtMovto>
            </LDL0002>
        </SISMSG>
    </DOC>
    """

    ldl0002 = LDL0002.from_xml(xml)

    assert isinstance(ldl0002, LDL0002)
    assert ldl0002.message_code == 'LDL0002'
    assert ldl0002.ldl_control_number == '321'
    assert ldl0002.ldl_ispb == '31680153'
    assert ldl0002.settlement_cycle_seq_num == '22'
    assert ldl0002.product_code == 'AMEX_CREDIT_CARD'
    assert ldl0002.liquidation_date == date(2026, 1, 22)
    assert ldl0002.code == 'PAYMENT_ORDER_SCHEDULING'
    assert ldl0002.ldl_timestamp == datetime(2026, 1, 22, 10, 12)
    assert ldl0002.settlement_date == date(2026, 1, 22)

    assert len(ldl0002.net_result_group) == NET_RESULT_SIZE
    result1 = ldl0002.net_result_group[0]
    result2 = ldl0002.net_result_group[1]
    assert isinstance(result1, NetResult)
    assert result1.participant_ispb == '43075534'
    assert result1.amount == Decimal('60.0')
    assert result1.cnpj == '68689822000165'
    assert result1.credit_debit_type == 'DEBIT'

    assert isinstance(result2, NetResult)
    assert result2.participant_ispb == '43075534'
    assert result2.amount == Decimal('60.0')
    assert result2.cnpj == '39548823000191'
    assert result2.credit_debit_type == CreditDebitType.DEBIT


def test_ldl0002r1_from_xml() -> None:
    xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/SPB/LDL0002.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>31680151250908000000001</NUOp>
        </BCMSG>
        <SISMSG>
            <LDL0002R1>
                <CodMsg>LDL0002R1</CodMsg>
                <NumCtrlLDL>123</NumCtrlLDL>
                <ISPBLDL>31680151</ISPBLDL>
                <DtHrBC>2026-01-22T10:33:00</DtHrBC>
                <DtMovto>2026-01-22</DtMovto>
            </LDL0002R1>
        </SISMSG>
    </DOC>
    """

    ldl0002r1 = LDL0002R1.from_xml(xml)

    assert isinstance(ldl0002r1, LDL0002R1)
    assert ldl0002r1.from_ispb == '31680151'
    assert ldl0002r1.to_ispb == '00038166'
    assert ldl0002r1.system_domain == 'SPB01'
    assert ldl0002r1.operation_number == '31680151250908000000001'
    assert ldl0002r1.message_code == 'LDL0002R1'
    assert ldl0002r1.ldl_control_number == '123'
    assert ldl0002r1.ldl_ispb == '31680151'
    assert ldl0002r1.vendor_timestamp == datetime(2026, 1, 22, 10, 33)
    assert ldl0002r1.settlement_date == date(2026, 1, 22)


def test_ldl0004e_general_error_from_xml() -> None:
    xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/SPB/LDL0002E.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>31680151250908000000001</NUOp>
        </BCMSG>
        <SISMSG>
            <LDL0002 CodErro="EGEN0050">
                <CodMsg>LDL0002E</CodMsg>
                <NumCtrlLDL>321</NumCtrlLDL>
                <ISPBLDL>31680153</ISPBLDL>
                <NumSeqCicloLiquid>22</NumSeqCicloLiquid>
                <CodProdt>ACC</CodProdt>
                <DtLiquid>2026-01-22</DtLiquid>
                <CodGrd>AGE01</CodGrd>
                <Grupo_LDL0002_ResultLiqd>
                    <ISPBPart>43075534</ISPBPart>
                    <VlrLanc>60.0</VlrLanc>
                    <CNPJNLiqdant>68689822000165</CNPJNLiqdant>
                    <TpDeb_Cred>D</TpDeb_Cred>
                </Grupo_LDL0002_ResultLiqd>
                <Grupo_LDL0002_ResultLiqd>
                    <ISPBPart>43075534</ISPBPart>
                    <VlrLanc>60.0</VlrLanc>
                    <CNPJNLiqdant>39548823000191</CNPJNLiqdant>
                    <TpDeb_Cred>D</TpDeb_Cred>
                </Grupo_LDL0002_ResultLiqd>
                <DtHrLDL>2026-01-22T10:12:00</DtHrLDL>
                <DtMovto>2026-01-22</DtMovto>
            </LDL0002>
        </SISMSG>
    </DOC>
    """

    ldl0002e = LDL0002E.from_xml(xml)

    assert isinstance(ldl0002e, LDL0002E)
    assert ldl0002e.message_code == 'LDL0002E'
    assert ldl0002e.ldl_control_number == '321'
    assert ldl0002e.ldl_ispb == '31680153'
    assert ldl0002e.settlement_cycle_seq_num == '22'
    assert ldl0002e.product_code == 'AMEX_CREDIT_CARD'
    assert ldl0002e.liquidation_date == date(2026, 1, 22)
    assert ldl0002e.code == 'PAYMENT_ORDER_SCHEDULING'
    assert ldl0002e.ldl_timestamp == datetime(2026, 1, 22, 10, 12)
    assert ldl0002e.settlement_date == date(2026, 1, 22)
    assert ldl0002e.general_error_code == 'EGEN0050'

    assert len(ldl0002e.net_result_group) == NET_RESULT_SIZE
    result1 = ldl0002e.net_result_group[0]
    result2 = ldl0002e.net_result_group[1]
    assert isinstance(result1, NetResultError)
    assert result1.participant_ispb == '43075534'
    assert result1.amount == Decimal('60.0')
    assert result1.cnpj == '68689822000165'
    assert result1.credit_debit_type == CreditDebitType.DEBIT

    assert isinstance(result2, NetResultError)
    assert result2.participant_ispb == '43075534'
    assert result2.amount == Decimal('60.0')
    assert result2.cnpj == '39548823000191'
    assert result2.credit_debit_type == CreditDebitType.DEBIT


def test_ldl0004e_tag_error_from_xml() -> None:
    xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/SPB/LDL0002E.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>31680151250908000000001</NUOp>
        </BCMSG>
        <SISMSG>
            <LDL0002>
                <CodMsg>LDL0002E</CodMsg>
                <NumCtrlLDL>321</NumCtrlLDL>
                <ISPBLDL CodErro="ELDL0123">31680153</ISPBLDL>
                <NumSeqCicloLiquid>22</NumSeqCicloLiquid>
                <CodProdt>ACC</CodProdt>
                <DtLiquid>2026-01-22</DtLiquid>
                <CodGrd>AGE01</CodGrd>
                <Grupo_LDL0002_ResultLiqd>
                    <ISPBPart>43075534</ISPBPart>
                    <VlrLanc>60.0</VlrLanc>
                    <CNPJNLiqdant>68689822000165</CNPJNLiqdant>
                    <TpDeb_Cred>D</TpDeb_Cred>
                </Grupo_LDL0002_ResultLiqd>
                <Grupo_LDL0002_ResultLiqd>
                    <ISPBPart>43075534</ISPBPart>
                    <VlrLanc>60.0</VlrLanc>
                    <CNPJNLiqdant>39548823000191</CNPJNLiqdant>
                    <TpDeb_Cred>D</TpDeb_Cred>
                </Grupo_LDL0002_ResultLiqd>
                <DtHrLDL>2026-01-22T10:12:00</DtHrLDL>
                <DtMovto>2026-01-22</DtMovto>
            </LDL0002>
        </SISMSG>
    </DOC>
    """

    ldl0002e = LDL0002E.from_xml(xml)

    assert isinstance(ldl0002e, LDL0002E)
    assert ldl0002e.message_code == 'LDL0002E'
    assert ldl0002e.ldl_control_number == '321'
    assert ldl0002e.ldl_ispb == '31680153'
    assert ldl0002e.settlement_cycle_seq_num == '22'
    assert ldl0002e.product_code == 'AMEX_CREDIT_CARD'
    assert ldl0002e.liquidation_date == date(2026, 1, 22)
    assert ldl0002e.code == 'PAYMENT_ORDER_SCHEDULING'
    assert ldl0002e.ldl_timestamp == datetime(2026, 1, 22, 10, 12)
    assert ldl0002e.settlement_date == date(2026, 1, 22)
    assert ldl0002e.ldl_ispb_error_code == 'ELDL0123'

    assert len(ldl0002e.net_result_group) == NET_RESULT_SIZE
    result1 = ldl0002e.net_result_group[0]
    result2 = ldl0002e.net_result_group[1]
    assert isinstance(result1, NetResultError)
    assert result1.participant_ispb == '43075534'
    assert result1.amount == Decimal('60.0')
    assert result1.cnpj == '68689822000165'
    assert result1.credit_debit_type == CreditDebitType.DEBIT

    assert isinstance(result2, NetResultError)
    assert result2.participant_ispb == '43075534'
    assert result2.amount == Decimal('60.0')
    assert result2.cnpj == '39548823000191'
    assert result2.credit_debit_type == CreditDebitType.DEBIT


def test_ldl0002_roundtrip() -> None:
    params = make_valid_ldl0002_params()

    ldl0002 = LDL0002.model_validate(params)
    xml = ldl0002.to_xml()
    ldl0002_from_xml = LDL0002.from_xml(xml)

    assert ldl0002 == ldl0002_from_xml


def test_ldl0002r1_roundtrip() -> None:
    params = make_valid_ldl0002r1_params()

    ldl0002r1 = LDL0002R1.model_validate(params)
    xml = ldl0002r1.to_xml()
    ldl0002r1_from_xml = LDL0002R1.from_xml(xml)

    assert ldl0002r1 == ldl0002r1_from_xml


def test_ldl0002_from_xml_missing_required_fields() -> None:
    xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/SPB/LDL0002.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>31680151250908000000001</NUOp>
        </BCMSG>
        <SISMSG>
            <LDL0002>
                <CodMsg>LDL0002</CodMsg>
            </LDL0002>
        </SISMSG>
    </DOC>
    """

    with pytest.raises(ValidationError) as exc:
        LDL0002.from_xml(xml)

    missing_fields = extract_missing_fields(exc.value)
    assert missing_fields == {
        'ldl_control_number',
        'ldl_ispb',
        'liquidation_date',
        'ldl_timestamp',
        'settlement_date',
    }
