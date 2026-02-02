from datetime import date, datetime
from decimal import Decimal
from typing import Any

import pytest
from pydantic import ValidationError

from sfn_messages.core.types import CreditDebitType, ReturnType
from sfn_messages.str.str0014 import STR0014, STR0014E, STR0014R1, LaunchGroup
from tests.conftest import extract_missing_fields, normalize_xml

LAUNCH_GROUP_SIZE: int = 3


def make_valid_str0014_params() -> dict[str, Any]:
    return {
        'from_ispb': '31680151',
        'to_ispb': '00038166',
        'system_domain': 'SPB01',
        'operation_number': '31680151250908000000001',
        'message_code': 'STR0014',
        'institution_control_number': '123',
        'institution_ispb': '31680151',
        'return_type': 'MESSAGE',
        'start_timestamp': '2026-02-02T09:00:00',
        'finish_timestamp': '2026-02-02T15:00:00',
        'settlement_date': '2026-02-02',
    }


def make_valid_str0014r1_params() -> dict[str, Any]:
    return {
        'from_ispb': '31680151',
        'to_ispb': '00038166',
        'system_domain': 'SPB01',
        'operation_number': '31680151250908000000001',
        'message_code': 'STR0014R1',
        'institution_control_number': '123',
        'institution_ispb': '31680151',
        'start_timestamp': '2026-02-02T09:00:00',
        'initial_amount': 98765.43,
        'launch_group': [
            {
                'original_message_code': 'STR0004',
                'original_if_or_ldl_control_number': '456',
                'counterparty_ispb': '31680152',
                'original_str_control_number': 'STR20250101000000100',
                'settlement_timestamp': '2026-02-02T09:02:44',
                'credit_debit_type': 'CREDIT',
                'amount': 123.5,
            },
            {
                'original_message_code': 'STR0008',
                'original_if_or_ldl_control_number': '321',
                'counterparty_ispb': '31680154',
                'original_str_control_number': 'STR20250101000000102',
                'settlement_timestamp': '2026-02-02T11:02:39',
                'credit_debit_type': 'DEBIT',
                'amount': 9765.5,
            },
            {
                'original_message_code': 'STR0004',
                'original_if_or_ldl_control_number': '789',
                'counterparty_ispb': '31680159',
                'original_str_control_number': 'STR20250101000000154',
                'settlement_timestamp': '2026-02-02T13:22:24',
                'credit_debit_type': 'CREDIT',
                'amount': 555.59,
            },
        ],
        'final_amount': 89679.02,
        'vendor_timestamp': '2026-02-02T16:58:00',
        'settlement_date': '2026-02-02',
        'file_size': 937000,
        'file_identifier': 'TEST_FILENAME_IDENTIFIER',
    }


def make_valid_str0014e_params(*, general_error: bool = False) -> dict[str, Any]:
    str0014e = {
        'from_ispb': '31680151',
        'to_ispb': '00038166',
        'system_domain': 'SPB01',
        'operation_number': '31680151250908000000001',
        'message_code': 'STR0014E',
        'institution_control_number': '123',
        'institution_ispb': '31680151',
        'return_type': 'MESSAGE',
        'start_timestamp': '2026-02-02T09:00:00',
        'finish_timestamp': '2026-02-02T15:00:00',
        'settlement_date': '2026-02-02',
    }

    if general_error:
        str0014e['general_error_code'] = 'EGEN0050'
    else:
        str0014e['institution_ispb_error_code'] = 'EGEN0051'

    return str0014e


def test_str0014_valid_model() -> None:
    params = make_valid_str0014_params()
    str0014 = STR0014.model_validate(params)

    assert isinstance(str0014, STR0014)
    assert str0014.message_code == 'STR0014'
    assert str0014.institution_control_number == '123'
    assert str0014.institution_ispb == '31680151'
    assert str0014.return_type == ReturnType.MESSAGE
    assert str0014.start_timestamp == datetime(2026, 2, 2, 9)
    assert str0014.finish_timestamp == datetime(2026, 2, 2, 15)
    assert str0014.settlement_date == date(2026, 2, 2)


def test_str0014r1_valid_model() -> None:
    params = make_valid_str0014r1_params()
    str0014r1 = STR0014R1.model_validate(params)

    assert isinstance(str0014r1, STR0014R1)
    assert str0014r1.message_code == 'STR0014R1'
    assert str0014r1.institution_control_number == '123'
    assert str0014r1.institution_ispb == '31680151'
    assert str0014r1.start_timestamp == datetime(2026, 2, 2, 9)
    assert str0014r1.initial_amount == Decimal('98765.43')
    assert str0014r1.final_amount == Decimal('89679.02')
    assert str0014r1.vendor_timestamp == datetime(2026, 2, 2, 16, 58)
    assert str0014r1.settlement_date == date(2026, 2, 2)
    assert str0014r1.file_size == int('937000')
    assert str0014r1.file_identifier == 'TEST_FILENAME_IDENTIFIER'

    assert len(str0014r1.launch_group) == LAUNCH_GROUP_SIZE
    launch1 = str0014r1.launch_group[0]
    launch2 = str0014r1.launch_group[1]
    launch3 = str0014r1.launch_group[2]

    assert isinstance(launch1, LaunchGroup)
    assert launch1.original_message_code == 'STR0004'
    assert launch1.original_if_or_ldl_control_number == '456'
    assert launch1.counterparty_ispb == '31680152'
    assert launch1.original_str_control_number == 'STR20250101000000100'
    assert launch1.settlement_timestamp == datetime(2026, 2, 2, 9, 2, 44)
    assert launch1.credit_debit_type == CreditDebitType.CREDIT
    assert launch1.amount == Decimal('123.5')

    assert isinstance(launch2, LaunchGroup)
    assert launch2.original_message_code == 'STR0008'
    assert launch2.original_if_or_ldl_control_number == '321'
    assert launch2.counterparty_ispb == '31680154'
    assert launch2.original_str_control_number == 'STR20250101000000102'
    assert launch2.settlement_timestamp == datetime(2026, 2, 2, 11, 2, 39)
    assert launch2.credit_debit_type == CreditDebitType.DEBIT
    assert launch2.amount == Decimal('9765.5')

    assert isinstance(launch3, LaunchGroup)
    assert launch3.original_message_code == 'STR0004'
    assert launch3.original_if_or_ldl_control_number == '789'
    assert launch3.counterparty_ispb == '31680159'
    assert launch3.original_str_control_number == 'STR20250101000000154'
    assert launch3.settlement_timestamp == datetime(2026, 2, 2, 13, 22, 24)
    assert launch3.credit_debit_type == CreditDebitType.CREDIT
    assert launch3.amount == Decimal('555.59')


def test_str0014e_general_error_valid_model() -> None:
    params = make_valid_str0014e_params(general_error=True)
    str0014e = STR0014E.model_validate(params)

    assert isinstance(str0014e, STR0014E)
    assert str0014e.message_code == 'STR0014E'
    assert str0014e.institution_control_number == '123'
    assert str0014e.institution_ispb == '31680151'
    assert str0014e.return_type == 'MESSAGE'
    assert str0014e.start_timestamp == datetime(2026, 2, 2, 9)
    assert str0014e.finish_timestamp == datetime(2026, 2, 2, 15)
    assert str0014e.settlement_date == date(2026, 2, 2)
    assert str0014e.general_error_code == 'EGEN0050'


def test_str0014e_tag_error_valid_model() -> None:
    params = make_valid_str0014e_params()
    str0014e = STR0014E.model_validate(params)

    assert isinstance(str0014e, STR0014E)
    assert str0014e.message_code == 'STR0014E'
    assert str0014e.institution_control_number == '123'
    assert str0014e.institution_ispb == '31680151'
    assert str0014e.return_type == 'MESSAGE'
    assert str0014e.start_timestamp == datetime(2026, 2, 2, 9)
    assert str0014e.finish_timestamp == datetime(2026, 2, 2, 15)
    assert str0014e.settlement_date == date(2026, 2, 2)
    assert str0014e.institution_ispb_error_code == 'EGEN0051'


def test_str0014_missing_required_fields() -> None:
    with pytest.raises(ValidationError) as exc:
        STR0014.model_validate({})

    missing_fields = extract_missing_fields(exc.value)
    assert missing_fields == {
        'from_ispb',
        'to_ispb',
        'system_domain',
        'operation_number',
        'institution_control_number',
        'institution_ispb',
        'return_type',
        'settlement_date',
    }


def test_str0014r1_missing_required_fields() -> None:
    with pytest.raises(ValidationError) as exc:
        STR0014R1.model_validate({})

    missing_fields = extract_missing_fields(exc.value)
    assert missing_fields == {
        'from_ispb',
        'to_ispb',
        'system_domain',
        'operation_number',
        'institution_control_number',
        'institution_ispb',
        'initial_amount',
        'final_amount',
        'vendor_timestamp',
        'settlement_date',
    }


def test_str0014_to_xml() -> None:
    params = make_valid_str0014_params()
    str0014 = STR0014.model_validate(params)

    xml = str0014.to_xml()

    expected_xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/SPB/STR0014.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>31680151250908000000001</NUOp>
        </BCMSG>
        <SISMSG>
            <STR0014>
                <CodMsg>STR0014</CodMsg>
                <NumCtrlIF_LDL>123</NumCtrlIF_LDL>
                <ISPBIF_LDL>31680151</ISPBIF_LDL>
                <TpRet>M</TpRet>
                <DtHrIni>2026-02-02T09:00:00</DtHrIni>
                <DtHrFim>2026-02-02T15:00:00</DtHrFim>
                <DtMovto>2026-02-02</DtMovto>
            </STR0014>
        </SISMSG>
    </DOC>
    """
    assert normalize_xml(expected_xml) == normalize_xml(xml)


def test_str0014r1_to_xml() -> None:
    params = make_valid_str0014r1_params()
    str0014r1 = STR0014R1.model_validate(params)

    xml = str0014r1.to_xml()

    expected_xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/SPB/STR0014.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>31680151250908000000001</NUOp>
        </BCMSG>
        <SISMSG>
            <STR0014R1>
                <CodMsg>STR0014R1</CodMsg>
                <NumCtrlIF_LDL>123</NumCtrlIF_LDL>
                <ISPBIF_LDL>31680151</ISPBIF_LDL>
                <DtHrIni>2026-02-02T09:00:00</DtHrIni>
                <SldInial>98765.43</SldInial>
                <Grupo_STR0014R1_Lanc>
                    <CodMsgOr>STR0004</CodMsgOr>
                    <NumCtrlIF_LDLOr>456</NumCtrlIF_LDLOr>
                    <ISPBCtrapart>31680152</ISPBCtrapart>
                    <NumCtrlSTROr>STR20250101000000100</NumCtrlSTROr>
                    <DtHrSit>2026-02-02T09:02:44</DtHrSit>
                    <TpDeb_Cred>C</TpDeb_Cred>
                    <VlrLanc>123.5</VlrLanc>
                </Grupo_STR0014R1_Lanc>
                <Grupo_STR0014R1_Lanc>
                    <CodMsgOr>STR0008</CodMsgOr>
                    <NumCtrlIF_LDLOr>321</NumCtrlIF_LDLOr>
                    <ISPBCtrapart>31680154</ISPBCtrapart>
                    <NumCtrlSTROr>STR20250101000000102</NumCtrlSTROr>
                    <DtHrSit>2026-02-02T11:02:39</DtHrSit>
                    <TpDeb_Cred>D</TpDeb_Cred>
                    <VlrLanc>9765.5</VlrLanc>
                </Grupo_STR0014R1_Lanc>
                <Grupo_STR0014R1_Lanc>
                    <CodMsgOr>STR0004</CodMsgOr>
                    <NumCtrlIF_LDLOr>789</NumCtrlIF_LDLOr>
                    <ISPBCtrapart>31680159</ISPBCtrapart>
                    <NumCtrlSTROr>STR20250101000000154</NumCtrlSTROr>
                    <DtHrSit>2026-02-02T13:22:24</DtHrSit>
                    <TpDeb_Cred>C</TpDeb_Cred>
                    <VlrLanc>555.59</VlrLanc>
                </Grupo_STR0014R1_Lanc>
                <SldFinl>89679.02</SldFinl>
                <DtHrBC>2026-02-02T16:58:00</DtHrBC>
                <DtMovto>2026-02-02</DtMovto>
                <TamArq>937000</TamArq>
                <IdentdArq>TEST_FILENAME_IDENTIFIER</IdentdArq>
            </STR0014R1>
        </SISMSG>
    </DOC>
    """
    assert normalize_xml(expected_xml) == normalize_xml(xml)


def test_str0014e_general_error_to_xml() -> None:
    params = make_valid_str0014e_params(general_error=True)
    str0014e = STR0014E.model_validate(params)

    xml = str0014e.to_xml()

    expected_xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/SPB/STR0014E.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>31680151250908000000001</NUOp>
        </BCMSG>
        <SISMSG>
            <STR0014 CodErro="EGEN0050">
                <CodMsg>STR0014E</CodMsg>
                <NumCtrlIF_LDL>123</NumCtrlIF_LDL>
                <ISPBIF_LDL>31680151</ISPBIF_LDL>
                <TpRet>M</TpRet>
                <DtHrIni>2026-02-02T09:00:00</DtHrIni>
                <DtHrFim>2026-02-02T15:00:00</DtHrFim>
                <DtMovto>2026-02-02</DtMovto>
            </STR0014>
        </SISMSG>
    </DOC>
    """
    assert normalize_xml(expected_xml) == normalize_xml(xml)


def test_str0014e_tag_error_to_xml() -> None:
    params = make_valid_str0014e_params()
    str0014e = STR0014E.model_validate(params)

    xml = str0014e.to_xml()

    expected_xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/SPB/STR0014E.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>31680151250908000000001</NUOp>
        </BCMSG>
        <SISMSG>
            <STR0014>
                <CodMsg>STR0014E</CodMsg>
                <NumCtrlIF_LDL>123</NumCtrlIF_LDL>
                <ISPBIF_LDL CodErro="EGEN0051">31680151</ISPBIF_LDL>
                <TpRet>M</TpRet>
                <DtHrIni>2026-02-02T09:00:00</DtHrIni>
                <DtHrFim>2026-02-02T15:00:00</DtHrFim>
                <DtMovto>2026-02-02</DtMovto>
            </STR0014>
        </SISMSG>
    </DOC>
    """
    assert normalize_xml(expected_xml) == normalize_xml(xml)


def test_str0014_from_xml() -> None:
    xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/SPB/STR0014.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>31680151250908000000001</NUOp>
        </BCMSG>
        <SISMSG>
            <STR0014>
                <CodMsg>STR0014</CodMsg>
                <NumCtrlIF_LDL>123</NumCtrlIF_LDL>
                <ISPBIF_LDL>31680151</ISPBIF_LDL>
                <TpRet>M</TpRet>
                <DtHrIni>2026-02-02T09:00:00</DtHrIni>
                <DtHrFim>2026-02-02T15:00:00</DtHrFim>
                <DtMovto>2026-02-02</DtMovto>
            </STR0014>
        </SISMSG>
    </DOC>
    """

    str0014 = STR0014.from_xml(xml)

    assert isinstance(str0014, STR0014)
    assert str0014.message_code == 'STR0014'
    assert str0014.institution_control_number == '123'
    assert str0014.institution_ispb == '31680151'
    assert str0014.return_type == ReturnType.MESSAGE
    assert str0014.start_timestamp == datetime(2026, 2, 2, 9)
    assert str0014.finish_timestamp == datetime(2026, 2, 2, 15)
    assert str0014.settlement_date == date(2026, 2, 2)


def test_str0014r1_from_xml() -> None:
    xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/SPB/STR0014.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>31680151250908000000001</NUOp>
        </BCMSG>
        <SISMSG>
            <STR0014R1>
                <CodMsg>STR0014R1</CodMsg>
                <NumCtrlIF_LDL>123</NumCtrlIF_LDL>
                <ISPBIF_LDL>31680151</ISPBIF_LDL>
                <DtHrIni>2026-02-02T09:00:00</DtHrIni>
                <SldInial>98765.43</SldInial>
                <Grupo_STR0014R1_Lanc>
                    <CodMsgOr>STR0004</CodMsgOr>
                    <NumCtrlIF_LDLOr>456</NumCtrlIF_LDLOr>
                    <ISPBCtrapart>31680152</ISPBCtrapart>
                    <NumCtrlSTROr>STR20250101000000100</NumCtrlSTROr>
                    <DtHrSit>2026-02-02T09:02:44</DtHrSit>
                    <TpDeb_Cred>C</TpDeb_Cred>
                    <VlrLanc>123.5</VlrLanc>
                </Grupo_STR0014R1_Lanc>
                <Grupo_STR0014R1_Lanc>
                    <CodMsgOr>STR0008</CodMsgOr>
                    <NumCtrlIF_LDLOr>321</NumCtrlIF_LDLOr>
                    <ISPBCtrapart>31680154</ISPBCtrapart>
                    <NumCtrlSTROr>STR20250101000000102</NumCtrlSTROr>
                    <DtHrSit>2026-02-02T11:02:39</DtHrSit>
                    <TpDeb_Cred>D</TpDeb_Cred>
                    <VlrLanc>9765.5</VlrLanc>
                </Grupo_STR0014R1_Lanc>
                <Grupo_STR0014R1_Lanc>
                    <CodMsgOr>STR0004</CodMsgOr>
                    <NumCtrlIF_LDLOr>789</NumCtrlIF_LDLOr>
                    <ISPBCtrapart>31680159</ISPBCtrapart>
                    <NumCtrlSTROr>STR20250101000000154</NumCtrlSTROr>
                    <DtHrSit>2026-02-02T13:22:24</DtHrSit>
                    <TpDeb_Cred>C</TpDeb_Cred>
                    <VlrLanc>555.59</VlrLanc>
                </Grupo_STR0014R1_Lanc>
                <SldFinl>89679.02</SldFinl>
                <DtHrBC>2026-02-02T16:58:00</DtHrBC>
                <DtMovto>2026-02-02</DtMovto>
                <TamArq>937000</TamArq>
                <IdentdArq>TEST_FILENAME_IDENTIFIER</IdentdArq>
            </STR0014R1>
        </SISMSG>
    </DOC>
    """

    str0014r1 = STR0014R1.from_xml(xml)

    assert isinstance(str0014r1, STR0014R1)
    assert str0014r1.message_code == 'STR0014R1'
    assert str0014r1.institution_control_number == '123'
    assert str0014r1.institution_ispb == '31680151'
    assert str0014r1.start_timestamp == datetime(2026, 2, 2, 9)
    assert str0014r1.initial_amount == Decimal('98765.43')
    assert str0014r1.final_amount == Decimal('89679.02')
    assert str0014r1.vendor_timestamp == datetime(2026, 2, 2, 16, 58)
    assert str0014r1.settlement_date == date(2026, 2, 2)
    assert str0014r1.file_size == int('937000')
    assert str0014r1.file_identifier == 'TEST_FILENAME_IDENTIFIER'

    assert len(str0014r1.launch_group) == LAUNCH_GROUP_SIZE
    launch1 = str0014r1.launch_group[0]
    launch2 = str0014r1.launch_group[1]
    launch3 = str0014r1.launch_group[2]

    assert isinstance(launch1, LaunchGroup)
    assert launch1.original_message_code == 'STR0004'
    assert launch1.original_if_or_ldl_control_number == '456'
    assert launch1.counterparty_ispb == '31680152'
    assert launch1.original_str_control_number == 'STR20250101000000100'
    assert launch1.settlement_timestamp == datetime(2026, 2, 2, 9, 2, 44)
    assert launch1.credit_debit_type == CreditDebitType.CREDIT
    assert launch1.amount == Decimal('123.5')

    assert isinstance(launch2, LaunchGroup)
    assert launch2.original_message_code == 'STR0008'
    assert launch2.original_if_or_ldl_control_number == '321'
    assert launch2.counterparty_ispb == '31680154'
    assert launch2.original_str_control_number == 'STR20250101000000102'
    assert launch2.settlement_timestamp == datetime(2026, 2, 2, 11, 2, 39)
    assert launch2.credit_debit_type == CreditDebitType.DEBIT
    assert launch2.amount == Decimal('9765.5')

    assert isinstance(launch3, LaunchGroup)
    assert launch3.original_message_code == 'STR0004'
    assert launch3.original_if_or_ldl_control_number == '789'
    assert launch3.counterparty_ispb == '31680159'
    assert launch3.original_str_control_number == 'STR20250101000000154'
    assert launch3.settlement_timestamp == datetime(2026, 2, 2, 13, 22, 24)
    assert launch3.credit_debit_type == CreditDebitType.CREDIT
    assert launch3.amount == Decimal('555.59')


def test_str0014e_general_error_from_xml() -> None:
    xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/SPB/STR0014E.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>31680151250908000000001</NUOp>
        </BCMSG>
        <SISMSG>
            <STR0014 CodErro="EGEN0050">
                <CodMsg>STR0014E</CodMsg>
                <NumCtrlIF_LDL>123</NumCtrlIF_LDL>
                <ISPBIF_LDL>31680151</ISPBIF_LDL>
                <TpRet>M</TpRet>
                <DtHrIni>2026-02-02T09:00:00</DtHrIni>
                <DtHrFim>2026-02-02T15:00:00</DtHrFim>
                <DtMovto>2026-02-02</DtMovto>
            </STR0014>
        </SISMSG>
    </DOC>
    """

    str0014e = STR0014E.from_xml(xml)

    assert isinstance(str0014e, STR0014E)
    assert str0014e.message_code == 'STR0014E'
    assert str0014e.institution_control_number == '123'
    assert str0014e.institution_ispb == '31680151'
    assert str0014e.return_type == 'MESSAGE'
    assert str0014e.start_timestamp == datetime(2026, 2, 2, 9)
    assert str0014e.finish_timestamp == datetime(2026, 2, 2, 15)
    assert str0014e.settlement_date == date(2026, 2, 2)
    assert str0014e.general_error_code == 'EGEN0050'


def test_str0014e_tag_error_from_xml() -> None:
    xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/SPB/STR0014E.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>31680151250908000000001</NUOp>
        </BCMSG>
        <SISMSG>
            <STR0014>
                <CodMsg>STR0014E</CodMsg>
                <NumCtrlIF_LDL>123</NumCtrlIF_LDL>
                <ISPBIF_LDL CodErro="EGEN0051">31680151</ISPBIF_LDL>
                <TpRet>M</TpRet>
                <DtHrIni>2026-02-02T09:00:00</DtHrIni>
                <DtHrFim>2026-02-02T15:00:00</DtHrFim>
                <DtMovto>2026-02-02</DtMovto>
            </STR0014>
        </SISMSG>
    </DOC>
    """

    str0014e = STR0014E.from_xml(xml)

    assert isinstance(str0014e, STR0014E)
    assert str0014e.message_code == 'STR0014E'
    assert str0014e.institution_control_number == '123'
    assert str0014e.institution_ispb == '31680151'
    assert str0014e.return_type == 'MESSAGE'
    assert str0014e.start_timestamp == datetime(2026, 2, 2, 9)
    assert str0014e.finish_timestamp == datetime(2026, 2, 2, 15)
    assert str0014e.settlement_date == date(2026, 2, 2)
    assert str0014e.institution_ispb_error_code == 'EGEN0051'


def test_str0014_roundtrip() -> None:
    params = make_valid_str0014_params()

    str0014 = STR0014.model_validate(params)
    xml = str0014.to_xml()
    str0014_from_xml = STR0014.from_xml(xml)

    assert str0014 == str0014_from_xml


def test_str0014r1_roundtrip() -> None:
    params = make_valid_str0014r1_params()

    str0014r1 = STR0014R1.model_validate(params)
    xml = str0014r1.to_xml()
    str0014r1_from_xml = STR0014R1.from_xml(xml)

    assert str0014r1 == str0014r1_from_xml
