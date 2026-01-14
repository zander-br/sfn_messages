from datetime import UTC, date, datetime
from decimal import Decimal
from typing import Any

import pytest
from pydantic import ValidationError

from sfn_messages.core.types import CreditDebitType
from sfn_messages.sme.sme0003 import SME0003, SME0003E, SME0003R1, LaunchGroup
from tests.conftest import extract_missing_fields, normalize_xml

LAUNCH_GROUP_SIZE = 2


def make_valid_sme0003_params() -> dict[str, Any]:
    return {
        'from_ispb': '31680151',
        'to_ispb': '00038166',
        'system_domain': 'SPB01',
        'operation_number': '316801512509080000001',
        'message_code': 'SME0003',
        'ieme_control_number': '123',
        'ieme_ispb': '31680153',
        'settlement_date': '2025-12-03',
    }


def make_valid_sme0003r1_params() -> dict[str, Any]:
    return {
        'from_ispb': '31680151',
        'to_ispb': '00038166',
        'system_domain': 'SPB01',
        'operation_number': '316801512509080000001',
        'message_code': 'SME0003R1',
        'ieme_control_number': '123',
        'ieme_ispb': '31680153',
        'initial_amount': 112.73,
        'launch_group': [
            {
                'original_message_code': 'SME0003',
                'ieme_control_number': '123',
                'counterparty_ispb': '31680155',
                'original_str_control_number': 'STR20250101000000001',
                'original_sme_control_number': 'SME20251203011111111',
                'settlement_timestamp': '2025-12-03T12:19:00+00:00',
                'credit_debit_type': 'CREDIT',
                'amount': 50.0,
            },
            {
                'original_message_code': 'SME0003',
                'ieme_control_number': '123',
                'counterparty_ispb': '31680156',
                'original_str_control_number': 'STR20250101000000001',
                'original_sme_control_number': 'SME20251203011111111',
                'settlement_timestamp': '2025-12-03T12:20:00+00:00',
                'credit_debit_type': 'CREDIT',
                'amount': 62.73,
            },
        ],
        'final_amount': 112.73,
        'vendor_timestamp': '2025-12-03T12:22:00+00:00',
        'settlement_date': '2025-12-03',
    }


def make_valid_sme0003e_params(*, general_error: bool = False) -> dict[str, Any]:
    sme0003e = {
        'from_ispb': '31680151',
        'to_ispb': '00038166',
        'system_domain': 'SPB01',
        'operation_number': '316801512509080000001',
        'message_code': 'SME0003',
        'ieme_control_number': '123',
        'ieme_ispb': '31680153',
        'settlement_date': '2025-12-03',
    }

    if general_error:
        sme0003e['general_error_code'] = 'EGEN0050'
    else:
        sme0003e['ieme_ispb_error_code'] = 'EGEN0051'

    return sme0003e


def test_sme0003_valid_model() -> None:
    params = make_valid_sme0003_params()
    sme0003 = SME0003.model_validate(params)

    assert isinstance(sme0003, SME0003)
    assert sme0003.from_ispb == '31680151'
    assert sme0003.to_ispb == '00038166'
    assert sme0003.system_domain == 'SPB01'
    assert sme0003.operation_number == '316801512509080000001'
    assert sme0003.message_code == 'SME0003'
    assert sme0003.ieme_control_number == '123'
    assert sme0003.ieme_ispb == '31680153'
    assert sme0003.settlement_date == date(2025, 12, 3)


def test_sme0003r1_valid_model() -> None:
    params = make_valid_sme0003r1_params()
    sme0003r1 = SME0003R1.model_validate(params)

    assert isinstance(sme0003r1, SME0003R1)
    assert sme0003r1.from_ispb == '31680151'
    assert sme0003r1.to_ispb == '00038166'
    assert sme0003r1.system_domain == 'SPB01'
    assert sme0003r1.operation_number == '316801512509080000001'
    assert sme0003r1.message_code == 'SME0003R1'
    assert sme0003r1.ieme_control_number == '123'
    assert sme0003r1.ieme_ispb == '31680153'
    assert sme0003r1.initial_amount == Decimal('112.73')
    assert sme0003r1.final_amount == Decimal('112.73')
    assert sme0003r1.vendor_timestamp == datetime(2025, 12, 3, 12, 22, tzinfo=UTC)
    assert sme0003r1.settlement_date == date(2025, 12, 3)

    assert len(sme0003r1.launch_group) == LAUNCH_GROUP_SIZE
    launch1 = sme0003r1.launch_group[0]
    launch2 = sme0003r1.launch_group[1]

    assert isinstance(launch1, LaunchGroup)
    assert launch1.original_message_code == 'SME0003'
    assert launch1.ieme_control_number == '123'
    assert launch1.counterparty_ispb == '31680155'
    assert launch1.original_str_control_number == 'STR20250101000000001'
    assert launch1.original_sme_control_number == 'SME20251203011111111'
    assert launch1.settlement_timestamp == datetime(2025, 12, 3, 12, 19, tzinfo=UTC)
    assert launch1.credit_debit_type == CreditDebitType.CREDIT
    assert launch1.amount == Decimal('50.0')

    assert isinstance(launch2, LaunchGroup)
    assert launch2.original_message_code == 'SME0003'
    assert launch2.ieme_control_number == '123'
    assert launch2.counterparty_ispb == '31680156'
    assert launch2.original_str_control_number == 'STR20250101000000001'
    assert launch2.original_sme_control_number == 'SME20251203011111111'
    assert launch2.settlement_timestamp == datetime(2025, 12, 3, 12, 20, tzinfo=UTC)
    assert launch2.credit_debit_type == CreditDebitType.CREDIT
    assert launch2.amount == Decimal('62.73')


def test_sme0003e_general_error_valid_model() -> None:
    params = make_valid_sme0003e_params(general_error=True)
    sme0003e = SME0003E.model_validate(params)

    assert isinstance(sme0003e, SME0003E)
    assert sme0003e.from_ispb == '31680151'
    assert sme0003e.to_ispb == '00038166'
    assert sme0003e.system_domain == 'SPB01'
    assert sme0003e.operation_number == '316801512509080000001'
    assert sme0003e.message_code == 'SME0003'
    assert sme0003e.ieme_control_number == '123'
    assert sme0003e.ieme_ispb == '31680153'
    assert sme0003e.settlement_date == date(2025, 12, 3)
    assert sme0003e.general_error_code == 'EGEN0050'


def test_sme0003e_tag_error_valid_model() -> None:
    params = make_valid_sme0003e_params()
    sme0003e = SME0003E.model_validate(params)

    assert isinstance(sme0003e, SME0003E)
    assert sme0003e.from_ispb == '31680151'
    assert sme0003e.to_ispb == '00038166'
    assert sme0003e.system_domain == 'SPB01'
    assert sme0003e.operation_number == '316801512509080000001'
    assert sme0003e.message_code == 'SME0003'
    assert sme0003e.ieme_control_number == '123'
    assert sme0003e.ieme_ispb == '31680153'
    assert sme0003e.settlement_date == date(2025, 12, 3)
    assert sme0003e.ieme_ispb_error_code == 'EGEN0051'


def test_sme0003_missing_required_fields() -> None:
    with pytest.raises(ValidationError) as exc:
        SME0003.model_validate({})

    missing_fields = extract_missing_fields(exc.value)
    assert missing_fields == {
        'from_ispb',
        'to_ispb',
        'system_domain',
        'operation_number',
        'ieme_control_number',
        'ieme_ispb',
        'settlement_date',
    }


def test_sme0003r1_missing_required_fields() -> None:
    with pytest.raises(ValidationError) as exc:
        SME0003R1.model_validate({})

    missing_fields = extract_missing_fields(exc.value)
    assert missing_fields == {
        'from_ispb',
        'to_ispb',
        'system_domain',
        'operation_number',
        'ieme_control_number',
        'ieme_ispb',
        'initial_amount',
        'final_amount',
        'vendor_timestamp',
        'settlement_date',
    }


def test_sme0003_to_xml() -> None:
    params = make_valid_sme0003_params()
    sme0003 = SME0003.model_validate(params)

    xml = sme0003.to_xml()

    expected_xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/SME/SME0003.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>316801512509080000001</NUOp>
        </BCMSG>
        <SISMSG>
            <SME0003>
                <CodMsg>SME0003</CodMsg>
                <NumCtrlIEME>123</NumCtrlIEME>
                <ISPBIEME>31680153</ISPBIEME>
                <DtMovto>2025-12-03</DtMovto>
            </SME0003>
        </SISMSG>
    </DOC>
    """
    assert normalize_xml(expected_xml) == normalize_xml(xml)


def test_sme0003r1_to_xml() -> None:
    params = make_valid_sme0003r1_params()
    sme0003r1 = SME0003R1.model_validate(params)

    xml = sme0003r1.to_xml()

    expected_xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/SME/SME0003.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>316801512509080000001</NUOp>
        </BCMSG>
        <SISMSG>
            <SME0003R1>
                <CodMsg>SME0003R1</CodMsg>
                <NumCtrlIEME>123</NumCtrlIEME>
                <ISPBIEME>31680153</ISPBIEME>
                <SldInial>112.73</SldInial>
                <Grupo_SME0003R1_Lanc>
                    <CodMsgOr>SME0003</CodMsgOr>
                    <NumCtrlIEMEOr>123</NumCtrlIEMEOr>
                    <ISPBCtrapart>31680155</ISPBCtrapart>
                    <NumCtrlSTROr>STR20250101000000001</NumCtrlSTROr>
                    <NumCtrlSMEOr>SME20251203011111111</NumCtrlSMEOr>
                    <DtHrSit>2025-12-03 12:19:00+00:00</DtHrSit>
                    <TpDeb_Cred>C</TpDeb_Cred>
                    <VlrLanc>50.0</VlrLanc>
                </Grupo_SME0003R1_Lanc>
                <Grupo_SME0003R1_Lanc>
                    <CodMsgOr>SME0003</CodMsgOr>
                    <NumCtrlIEMEOr>123</NumCtrlIEMEOr>
                    <ISPBCtrapart>31680156</ISPBCtrapart>
                    <NumCtrlSTROr>STR20250101000000001</NumCtrlSTROr>
                    <NumCtrlSMEOr>SME20251203011111111</NumCtrlSMEOr>
                    <DtHrSit>2025-12-03 12:20:00+00:00</DtHrSit>
                    <TpDeb_Cred>C</TpDeb_Cred>
                    <VlrLanc>62.73</VlrLanc>
                </Grupo_SME0003R1_Lanc>
                <SldFinl>112.73</SldFinl>
                <DtHrBC>2025-12-03 12:22:00+00:00</DtHrBC>
                <DtMovto>2025-12-03</DtMovto>
            </SME0003R1>
        </SISMSG>
    </DOC>
    """
    assert normalize_xml(expected_xml) == normalize_xml(xml)


def test_sme0003e_general_error_to_xml() -> None:
    params = make_valid_sme0003e_params(general_error=True)
    sme0003e = SME0003E.model_validate(params)

    xml = sme0003e.to_xml()

    expected_xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/SME/SME0003E.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>316801512509080000001</NUOp>
        </BCMSG>
        <SISMSG>
            <SME0003E CodErro="EGEN0050">
                <CodMsg>SME0003</CodMsg>
                <NumCtrlIEME>123</NumCtrlIEME>
                <ISPBIEME>31680153</ISPBIEME>
                <DtMovto>2025-12-03</DtMovto>
            </SME0003E>
        </SISMSG>
    </DOC>
    """
    assert normalize_xml(expected_xml) == normalize_xml(xml)


def test_sme0003e_tag_error_to_xml() -> None:
    params = make_valid_sme0003e_params()
    sme0003e = SME0003E.model_validate(params)

    xml = sme0003e.to_xml()

    expected_xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/SME/SME0003E.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>316801512509080000001</NUOp>
        </BCMSG>
        <SISMSG>
            <SME0003E>
                <CodMsg>SME0003</CodMsg>
                <NumCtrlIEME>123</NumCtrlIEME>
                <ISPBIEME CodErro="EGEN0051">31680153</ISPBIEME>
                <DtMovto>2025-12-03</DtMovto>
            </SME0003E>
        </SISMSG>
    </DOC>
    """
    assert normalize_xml(expected_xml) == normalize_xml(xml)


def test_sme0003_from_xml() -> None:
    xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/SME/SME0003.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>316801512509080000001</NUOp>
        </BCMSG>
        <SISMSG>
            <SME0003>
                <CodMsg>SME0003</CodMsg>
                <NumCtrlIEME>123</NumCtrlIEME>
                <ISPBIEME>31680153</ISPBIEME>
                <DtMovto>2025-12-03</DtMovto>
            </SME0003>
        </SISMSG>
    </DOC>
    """

    sme0003 = SME0003.from_xml(xml)

    assert isinstance(sme0003, SME0003)
    assert sme0003.from_ispb == '31680151'
    assert sme0003.to_ispb == '00038166'
    assert sme0003.system_domain == 'SPB01'
    assert sme0003.operation_number == '316801512509080000001'
    assert sme0003.message_code == 'SME0003'
    assert sme0003.ieme_control_number == '123'
    assert sme0003.ieme_ispb == '31680153'
    assert sme0003.settlement_date == date(2025, 12, 3)


def test_sme0003r1_from_xml() -> None:
    xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/SME/SME0003.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>316801512509080000001</NUOp>
        </BCMSG>
        <SISMSG>
            <SME0003R1>
                <CodMsg>SME0003R1</CodMsg>
                <NumCtrlIEME>123</NumCtrlIEME>
                <ISPBIEME>31680153</ISPBIEME>
                <SldInial>112.73</SldInial>
                <Grupo_SME0003R1_Lanc>
                    <CodMsgOr>SME0003</CodMsgOr>
                    <NumCtrlIEMEOr>123</NumCtrlIEMEOr>
                    <ISPBCtrapart>31680155</ISPBCtrapart>
                    <NumCtrlSTROr>STR20250101000000001</NumCtrlSTROr>
                    <NumCtrlSMEOr>SME20251203011111111</NumCtrlSMEOr>
                    <DtHrSit>2025-12-03 12:19:00+00:00</DtHrSit>
                    <TpDeb_Cred>C</TpDeb_Cred>
                    <VlrLanc>50.0</VlrLanc>
                </Grupo_SME0003R1_Lanc>
                <Grupo_SME0003R1_Lanc>
                    <CodMsgOr>SME0003</CodMsgOr>
                    <NumCtrlIEMEOr>123</NumCtrlIEMEOr>
                    <ISPBCtrapart>31680156</ISPBCtrapart>
                    <NumCtrlSTROr>STR20250101000000001</NumCtrlSTROr>
                    <NumCtrlSMEOr>SME20251203011111111</NumCtrlSMEOr>
                    <DtHrSit>2025-12-03 12:20:00+00:00</DtHrSit>
                    <TpDeb_Cred>C</TpDeb_Cred>
                    <VlrLanc>62.73</VlrLanc>
                </Grupo_SME0003R1_Lanc>
                <SldFinl>112.73</SldFinl>
                <DtHrBC>2025-12-03 12:22:00+00:00</DtHrBC>
                <DtMovto>2025-12-03</DtMovto>
            </SME0003R1>
        </SISMSG>
    </DOC>
    """

    sme0003r1 = SME0003R1.from_xml(xml)

    assert isinstance(sme0003r1, SME0003R1)
    assert sme0003r1.from_ispb == '31680151'
    assert sme0003r1.to_ispb == '00038166'
    assert sme0003r1.system_domain == 'SPB01'
    assert sme0003r1.operation_number == '316801512509080000001'
    assert sme0003r1.message_code == 'SME0003R1'
    assert sme0003r1.ieme_control_number == '123'
    assert sme0003r1.ieme_ispb == '31680153'
    assert sme0003r1.initial_amount == Decimal('112.73')
    assert sme0003r1.final_amount == Decimal('112.73')
    assert sme0003r1.vendor_timestamp == datetime(2025, 12, 3, 12, 22, tzinfo=UTC)
    assert sme0003r1.settlement_date == date(2025, 12, 3)

    assert len(sme0003r1.launch_group) == LAUNCH_GROUP_SIZE
    launch1 = sme0003r1.launch_group[0]
    launch2 = sme0003r1.launch_group[1]

    assert isinstance(launch1, LaunchGroup)
    assert launch1.original_message_code == 'SME0003'
    assert launch1.ieme_control_number == '123'
    assert launch1.counterparty_ispb == '31680155'
    assert launch1.original_str_control_number == 'STR20250101000000001'
    assert launch1.original_sme_control_number == 'SME20251203011111111'
    assert launch1.settlement_timestamp == datetime(2025, 12, 3, 12, 19, tzinfo=UTC)
    assert launch1.credit_debit_type == CreditDebitType.CREDIT
    assert launch1.amount == Decimal('50.0')

    assert isinstance(launch2, LaunchGroup)
    assert launch2.original_message_code == 'SME0003'
    assert launch2.ieme_control_number == '123'
    assert launch2.counterparty_ispb == '31680156'
    assert launch2.original_str_control_number == 'STR20250101000000001'
    assert launch2.original_sme_control_number == 'SME20251203011111111'
    assert launch2.settlement_timestamp == datetime(2025, 12, 3, 12, 20, tzinfo=UTC)
    assert launch2.credit_debit_type == CreditDebitType.CREDIT
    assert launch2.amount == Decimal('62.73')


def test_sme0003e_general_error_from_xml() -> None:
    xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/SME/SME0003E.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>316801512509080000001</NUOp>
        </BCMSG>
        <SISMSG>
            <SME0003E CodErro="EGEN0050">
                <CodMsg>SME0003</CodMsg>
                <NumCtrlIEME>123</NumCtrlIEME>
                <ISPBIEME>31680153</ISPBIEME>
                <DtMovto>2025-12-03</DtMovto>
            </SME0003E>
        </SISMSG>
    </DOC>
    """

    sme0003e = SME0003E.from_xml(xml)

    assert isinstance(sme0003e, SME0003E)
    assert sme0003e.from_ispb == '31680151'
    assert sme0003e.to_ispb == '00038166'
    assert sme0003e.system_domain == 'SPB01'
    assert sme0003e.operation_number == '316801512509080000001'
    assert sme0003e.message_code == 'SME0003'
    assert sme0003e.ieme_control_number == '123'
    assert sme0003e.ieme_ispb == '31680153'
    assert sme0003e.settlement_date == date(2025, 12, 3)
    assert sme0003e.general_error_code == 'EGEN0050'


def test_sme0003e_tag_error_from_xml() -> None:
    xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/SME/SME0003E.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>316801512509080000001</NUOp>
        </BCMSG>
        <SISMSG>
            <SME0003E>
                <CodMsg>SME0003</CodMsg>
                <NumCtrlIEME>123</NumCtrlIEME>
                <ISPBIEME CodErro="EGEN0051">31680153</ISPBIEME>
                <DtMovto>2025-12-03</DtMovto>
            </SME0003E>
        </SISMSG>
    </DOC>
    """

    sme0003e = SME0003E.from_xml(xml)

    assert isinstance(sme0003e, SME0003E)
    assert sme0003e.from_ispb == '31680151'
    assert sme0003e.to_ispb == '00038166'
    assert sme0003e.system_domain == 'SPB01'
    assert sme0003e.operation_number == '316801512509080000001'
    assert sme0003e.message_code == 'SME0003'
    assert sme0003e.ieme_control_number == '123'
    assert sme0003e.ieme_ispb == '31680153'
    assert sme0003e.settlement_date == date(2025, 12, 3)
    assert sme0003e.ieme_ispb_error_code == 'EGEN0051'


def test_sme0003_roundtrip() -> None:
    params = make_valid_sme0003_params()

    sme0003 = SME0003.model_validate(params)
    xml = sme0003.to_xml()
    sme0003_from_xml = SME0003.from_xml(xml)

    assert sme0003 == sme0003_from_xml


def test_sme0003_from_xml_missing_required_fields() -> None:
    xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/SME/SME0003.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>316801512509080000001</NUOp>
        </BCMSG>
        <SISMSG>
            <SME0003>
                <CodMsg>SME0003</CodMsg>
            </SME0003>
        </SISMSG>
    </DOC>
    """

    with pytest.raises(ValidationError) as exc:
        SME0003.from_xml(xml)

    missing_fields = extract_missing_fields(exc.value)
    assert missing_fields == {'ieme_control_number', 'ieme_ispb', 'settlement_date'}
