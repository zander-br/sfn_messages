from datetime import UTC, date, datetime
from decimal import Decimal
from typing import Any

import pytest
from pydantic import ValidationError

from sfn_messages.core.types import LdlSettlementStatus
from sfn_messages.ldl.ldl0011 import LDL0011, LDL0011E, LDL0011R1, LDL0011R2
from tests.conftest import extract_missing_fields, normalize_xml


def make_valid_ldl0011_params() -> dict[str, Any]:
    return {
        'from_ispb': '31680151',
        'to_ispb': '00038166',
        'system_domain': 'SPB01',
        'operation_number': '316801512509080000001',
        'message_code': 'LDL0011',
        'institution_control_number': '123',
        'institution_ispb': '31680151',
        'original_ldl_control_number': '321',
        'branch': '001',
        'account_number': '123456',
        'ldl_ispb': '31680153',
        'amount': 199.87,
        'settlement_date': '2025-12-10',
    }


def make_valid_ldl0011r1_params() -> dict[str, Any]:
    return {
        'from_ispb': '31680151',
        'to_ispb': '00038166',
        'system_domain': 'SPB01',
        'operation_number': '316801512509080000001',
        'message_code': 'LDL0011R1',
        'institution_control_number': '123',
        'debtor_institution_ispb': '31680151',
        'str_control_number': 'STR20250101000000001',
        'ldl_settlement_status': 'EFFECTIVE',
        'settlement_timestamp': '2025-12-10T10:02:00+00:00',
        'settlement_date': '2025-12-10',
    }


def make_valid_ldl0011r2_params() -> dict[str, Any]:
    return {
        'from_ispb': '31680151',
        'to_ispb': '00038166',
        'system_domain': 'SPB01',
        'operation_number': '316801512509080000001',
        'message_code': 'LDL0011R2',
        'str_control_number': 'STR20250101000000001',
        'vendor_timestamp': '2025-12-10T10:02:00+00:00',
        'original_ldl_control_number': '321',
        'institution_ispb': '31680151',
        'branch': '001',
        'account_number': '123456',
        'ldl_ispb': '31680153',
        'amount': 199.87,
        'settlement_date': '2025-12-10',
    }


def make_valid_ldl0011e_params(*, general_error: bool = False) -> dict[str, Any]:
    ldl0011e = {
        'from_ispb': '31680151',
        'to_ispb': '00038166',
        'system_domain': 'SPB01',
        'operation_number': '316801512509080000001',
        'message_code': 'LDL0011',
        'institution_control_number': '123',
        'institution_ispb': '31680151',
        'original_ldl_control_number': '321',
        'branch': '001',
        'account_number': '123456',
        'ldl_ispb': '31680153',
        'amount': 199.87,
        'settlement_date': '2025-12-10',
    }

    if general_error:
        ldl0011e['general_error_code'] = 'EGEN0050'
    else:
        ldl0011e['ldl_ispb_error_code'] = 'EGEN0051'

    return ldl0011e


def test_ldl0011_valid_model() -> None:
    params = make_valid_ldl0011_params()
    ldl0011 = LDL0011.model_validate(params)

    assert isinstance(ldl0011, LDL0011)
    assert ldl0011.from_ispb == '31680151'
    assert ldl0011.to_ispb == '00038166'
    assert ldl0011.system_domain == 'SPB01'
    assert ldl0011.operation_number == '316801512509080000001'
    assert ldl0011.message_code == 'LDL0011'
    assert ldl0011.institution_control_number == '123'
    assert ldl0011.institution_ispb == '31680151'
    assert ldl0011.original_ldl_control_number == '321'
    assert ldl0011.branch == '001'
    assert ldl0011.account_number == '123456'
    assert ldl0011.ldl_ispb == '31680153'
    assert ldl0011.amount == Decimal('199.87')
    assert ldl0011.settlement_date == date(2025, 12, 10)


def test_ldl0011r1_valid_model() -> None:
    params = make_valid_ldl0011r1_params()
    ldl0011r1 = LDL0011R1.model_validate(params)

    assert isinstance(ldl0011r1, LDL0011R1)
    assert ldl0011r1.from_ispb == '31680151'
    assert ldl0011r1.to_ispb == '00038166'
    assert ldl0011r1.system_domain == 'SPB01'
    assert ldl0011r1.operation_number == '316801512509080000001'
    assert ldl0011r1.message_code == 'LDL0011R1'
    assert ldl0011r1.institution_control_number == '123'
    assert ldl0011r1.debtor_institution_ispb == '31680151'
    assert ldl0011r1.str_control_number == 'STR20250101000000001'
    assert ldl0011r1.ldl_settlement_status == LdlSettlementStatus.EFFECTIVE
    assert ldl0011r1.settlement_timestamp == datetime(2025, 12, 10, 10, 2, tzinfo=UTC)
    assert ldl0011r1.settlement_date == date(2025, 12, 10)


def test_ldl0011r2_valid_model() -> None:
    params = make_valid_ldl0011r2_params()
    ldl0011r2 = LDL0011R2.model_validate(params)

    assert isinstance(ldl0011r2, LDL0011R2)
    assert ldl0011r2.from_ispb == '31680151'
    assert ldl0011r2.to_ispb == '00038166'
    assert ldl0011r2.system_domain == 'SPB01'
    assert ldl0011r2.operation_number == '316801512509080000001'
    assert ldl0011r2.message_code == 'LDL0011R2'
    assert ldl0011r2.str_control_number == 'STR20250101000000001'
    assert ldl0011r2.vendor_timestamp == datetime(2025, 12, 10, 10, 2, tzinfo=UTC)
    assert ldl0011r2.original_ldl_control_number == '321'
    assert ldl0011r2.institution_ispb == '31680151'
    assert ldl0011r2.branch == '001'
    assert ldl0011r2.account_number == '123456'
    assert ldl0011r2.ldl_ispb == '31680153'
    assert ldl0011r2.amount == Decimal('199.87')
    assert ldl0011r2.settlement_date == date(2025, 12, 10)


def test_ldl0011e_general_error_valid_model() -> None:
    params = make_valid_ldl0011e_params(general_error=True)
    ldl0011e = LDL0011E.model_validate(params)

    assert isinstance(ldl0011e, LDL0011E)
    assert ldl0011e.from_ispb == '31680151'
    assert ldl0011e.to_ispb == '00038166'
    assert ldl0011e.system_domain == 'SPB01'
    assert ldl0011e.operation_number == '316801512509080000001'
    assert ldl0011e.message_code == 'LDL0011'
    assert ldl0011e.institution_control_number == '123'
    assert ldl0011e.institution_ispb == '31680151'
    assert ldl0011e.original_ldl_control_number == '321'
    assert ldl0011e.branch == '001'
    assert ldl0011e.account_number == '123456'
    assert ldl0011e.ldl_ispb == '31680153'
    assert ldl0011e.amount == Decimal('199.87')
    assert ldl0011e.settlement_date == date(2025, 12, 10)
    assert ldl0011e.general_error_code == 'EGEN0050'


def test_ldl0011e_tag_error_valid_model() -> None:
    params = make_valid_ldl0011e_params()
    ldl0011e = LDL0011E.model_validate(params)

    assert isinstance(ldl0011e, LDL0011E)
    assert ldl0011e.from_ispb == '31680151'
    assert ldl0011e.to_ispb == '00038166'
    assert ldl0011e.system_domain == 'SPB01'
    assert ldl0011e.operation_number == '316801512509080000001'
    assert ldl0011e.message_code == 'LDL0011'
    assert ldl0011e.institution_control_number == '123'
    assert ldl0011e.institution_ispb == '31680151'
    assert ldl0011e.original_ldl_control_number == '321'
    assert ldl0011e.branch == '001'
    assert ldl0011e.account_number == '123456'
    assert ldl0011e.ldl_ispb == '31680153'
    assert ldl0011e.amount == Decimal('199.87')
    assert ldl0011e.settlement_date == date(2025, 12, 10)
    assert ldl0011e.ldl_ispb_error_code == 'EGEN0051'


def test_ldl0011_missing_required_fields() -> None:
    with pytest.raises(ValidationError) as exc:
        LDL0011.model_validate({})

    missing_fields = extract_missing_fields(exc.value)
    assert missing_fields == {
        'from_ispb',
        'to_ispb',
        'system_domain',
        'operation_number',
        'institution_control_number',
        'institution_ispb',
        'original_ldl_control_number',
        'branch',
        'account_number',
        'ldl_ispb',
        'amount',
        'settlement_date',
    }


def test_ldl0011r1_missing_required_fields() -> None:
    with pytest.raises(ValidationError) as exc:
        LDL0011R1.model_validate({})

    missing_fields = extract_missing_fields(exc.value)
    assert missing_fields == {
        'from_ispb',
        'to_ispb',
        'system_domain',
        'operation_number',
        'institution_control_number',
        'debtor_institution_ispb',
        'str_control_number',
        'ldl_settlement_status',
        'settlement_timestamp',
        'settlement_date',
    }


def test_ldl0011r2_missing_required_fields() -> None:
    with pytest.raises(ValidationError) as exc:
        LDL0011R2.model_validate({})

    missing_fields = extract_missing_fields(exc.value)
    assert missing_fields == {
        'from_ispb',
        'to_ispb',
        'system_domain',
        'operation_number',
        'str_control_number',
        'vendor_timestamp',
        'original_ldl_control_number',
        'institution_ispb',
        'branch',
        'account_number',
        'ldl_ispb',
        'amount',
        'settlement_date',
    }


def test_ldl0011_to_xml() -> None:
    params = make_valid_ldl0011_params()
    ldl0011 = LDL0011.model_validate(params)

    xml = ldl0011.to_xml()

    expected_xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/LDL/LDL0011.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>316801512509080000001</NUOp>
        </BCMSG>
        <SISMSG>
            <LDL0011>
                <CodMsg>LDL0011</CodMsg>
                <NumCtrlIF>123</NumCtrlIF>
                <ISPBIF>31680151</ISPBIF>
                <NumCtrlLDLOr>321</NumCtrlLDLOr>
                <AgDebtd>001</AgDebtd>
                <CtDebtd>123456</CtDebtd>
                <ISPBLDL>31680153</ISPBLDL>
                <VlrLanc>199.87</VlrLanc>
                <DtMovto>2025-12-10</DtMovto>
            </LDL0011>
        </SISMSG>
    </DOC>
    """
    assert normalize_xml(expected_xml) == normalize_xml(xml)


def test_ldl0011r1_to_xml() -> None:
    params = make_valid_ldl0011r1_params()
    ldl0011r1 = LDL0011R1.model_validate(params)

    xml = ldl0011r1.to_xml()

    expected_xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/LDL/LDL0011.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>316801512509080000001</NUOp>
        </BCMSG>
        <SISMSG>
            <LDL0011R1>
                <CodMsg>LDL0011R1</CodMsg>
                <NumCtrlIF>123</NumCtrlIF>
                <ISPBIFDebtd>31680151</ISPBIFDebtd>
                <NumCtrlSTR>STR20250101000000001</NumCtrlSTR>
                <SitLancLDL>1</SitLancLDL>
                <DtHrSit>2025-12-10 10:02:00+00:00</DtHrSit>
                <DtMovto>2025-12-10</DtMovto>
            </LDL0011R1>
        </SISMSG>
    </DOC>
    """
    assert normalize_xml(expected_xml) == normalize_xml(xml)


def test_ldl0011r2_to_xml() -> None:
    params = make_valid_ldl0011r2_params()
    ldl0011r2 = LDL0011R2.model_validate(params)

    xml = ldl0011r2.to_xml()

    expected_xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/LDL/LDL0011.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>316801512509080000001</NUOp>
        </BCMSG>
        <SISMSG>
            <LDL0011R2>
                <CodMsg>LDL0011R2</CodMsg>
                <NumCtrlSTR>STR20250101000000001</NumCtrlSTR>
                <DtHrBC>2025-12-10 10:02:00+00:00</DtHrBC>
                <NumCtrlLDLOr>321</NumCtrlLDLOr>
                <ISPBIF>31680151</ISPBIF>
                <AgDebtd>001</AgDebtd>
                <CtDebtd>123456</CtDebtd>
                <ISPBLDL>31680153</ISPBLDL>
                <VlrLanc>199.87</VlrLanc>
                <DtMovto>2025-12-10</DtMovto>
            </LDL0011R2>
        </SISMSG>
    </DOC>
    """
    assert normalize_xml(expected_xml) == normalize_xml(xml)


def test_ldl0011e_general_error_to_xml() -> None:
    params = make_valid_ldl0011e_params(general_error=True)
    ldl0011e = LDL0011E.model_validate(params)

    xml = ldl0011e.to_xml()

    expected_xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/LDL/LDL0011E.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>316801512509080000001</NUOp>
        </BCMSG>
        <SISMSG>
            <LDL0011E CodErro="EGEN0050">
                <CodMsg>LDL0011</CodMsg>
                <NumCtrlIF>123</NumCtrlIF>
                <ISPBIF>31680151</ISPBIF>
                <NumCtrlLDLOr>321</NumCtrlLDLOr>
                <AgDebtd>001</AgDebtd>
                <CtDebtd>123456</CtDebtd>
                <ISPBLDL>31680153</ISPBLDL>
                <VlrLanc>199.87</VlrLanc>
                <DtMovto>2025-12-10</DtMovto>
            </LDL0011E>
        </SISMSG>
    </DOC>
    """
    assert normalize_xml(expected_xml) == normalize_xml(xml)


def test_ldl0011e_tag_error_to_xml() -> None:
    params = make_valid_ldl0011e_params()
    ldl0011e = LDL0011E.model_validate(params)

    xml = ldl0011e.to_xml()

    expected_xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/LDL/LDL0011E.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>316801512509080000001</NUOp>
        </BCMSG>
        <SISMSG>
            <LDL0011E>
                <CodMsg>LDL0011</CodMsg>
                <NumCtrlIF>123</NumCtrlIF>
                <ISPBIF>31680151</ISPBIF>
                <NumCtrlLDLOr>321</NumCtrlLDLOr>
                <AgDebtd>001</AgDebtd>
                <CtDebtd>123456</CtDebtd>
                <ISPBLDL CodErro="EGEN0051">31680153</ISPBLDL>
                <VlrLanc>199.87</VlrLanc>
                <DtMovto>2025-12-10</DtMovto>
            </LDL0011E>
        </SISMSG>
    </DOC>
    """
    assert normalize_xml(expected_xml) == normalize_xml(xml)


def test_ldl0011_from_xml() -> None:
    xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/LDL/LDL0011.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>316801512509080000001</NUOp>
        </BCMSG>
        <SISMSG>
            <LDL0011>
                <CodMsg>LDL0011</CodMsg>
                <NumCtrlIF>123</NumCtrlIF>
                <ISPBIF>31680151</ISPBIF>
                <NumCtrlLDLOr>321</NumCtrlLDLOr>
                <AgDebtd>001</AgDebtd>
                <CtDebtd>123456</CtDebtd>
                <ISPBLDL>31680153</ISPBLDL>
                <VlrLanc>199.87</VlrLanc>
                <DtMovto>2025-12-10</DtMovto>
            </LDL0011>
        </SISMSG>
    </DOC>
    """

    ldl0011 = LDL0011.from_xml(xml)

    assert isinstance(ldl0011, LDL0011)
    assert ldl0011.from_ispb == '31680151'
    assert ldl0011.to_ispb == '00038166'
    assert ldl0011.system_domain == 'SPB01'
    assert ldl0011.operation_number == '316801512509080000001'
    assert ldl0011.message_code == 'LDL0011'
    assert ldl0011.institution_control_number == '123'
    assert ldl0011.institution_ispb == '31680151'
    assert ldl0011.original_ldl_control_number == '321'
    assert ldl0011.branch == '001'
    assert ldl0011.account_number == '123456'
    assert ldl0011.ldl_ispb == '31680153'
    assert ldl0011.amount == Decimal('199.87')
    assert ldl0011.settlement_date == date(2025, 12, 10)


def test_ldl0011r1_from_xml() -> None:
    xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/LDL/LDL0011.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>316801512509080000001</NUOp>
        </BCMSG>
        <SISMSG>
            <LDL0011R1>
                <CodMsg>LDL0011R1</CodMsg>
                <NumCtrlIF>123</NumCtrlIF>
                <ISPBIFDebtd>31680151</ISPBIFDebtd>
                <NumCtrlSTR>STR20250101000000001</NumCtrlSTR>
                <SitLancLDL>1</SitLancLDL>
                <DtHrSit>2025-12-10 10:02:00+00:00</DtHrSit>
                <DtMovto>2025-12-10</DtMovto>
            </LDL0011R1>
        </SISMSG>
    </DOC>
    """

    ldl0011r1 = LDL0011R1.from_xml(xml)

    assert isinstance(ldl0011r1, LDL0011R1)
    assert ldl0011r1.from_ispb == '31680151'
    assert ldl0011r1.to_ispb == '00038166'
    assert ldl0011r1.system_domain == 'SPB01'
    assert ldl0011r1.operation_number == '316801512509080000001'
    assert ldl0011r1.message_code == 'LDL0011R1'
    assert ldl0011r1.institution_control_number == '123'
    assert ldl0011r1.debtor_institution_ispb == '31680151'
    assert ldl0011r1.str_control_number == 'STR20250101000000001'
    assert ldl0011r1.ldl_settlement_status == LdlSettlementStatus.EFFECTIVE
    assert ldl0011r1.settlement_timestamp == datetime(2025, 12, 10, 10, 2, tzinfo=UTC)
    assert ldl0011r1.settlement_date == date(2025, 12, 10)


def test_ldl0011r2_from_xml() -> None:
    xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/LDL/LDL0011.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>316801512509080000001</NUOp>
        </BCMSG>
        <SISMSG>
            <LDL0011R2>
                <CodMsg>LDL0011R2</CodMsg>
                <NumCtrlSTR>STR20250101000000001</NumCtrlSTR>
                <DtHrBC>2025-12-10 10:02:00+00:00</DtHrBC>
                <NumCtrlLDLOr>321</NumCtrlLDLOr>
                <ISPBIF>31680151</ISPBIF>
                <AgDebtd>001</AgDebtd>
                <CtDebtd>123456</CtDebtd>
                <ISPBLDL>31680153</ISPBLDL>
                <VlrLanc>199.87</VlrLanc>
                <DtMovto>2025-12-10</DtMovto>
            </LDL0011R2>
        </SISMSG>
    </DOC>
    """

    ldl0011r2 = LDL0011R2.from_xml(xml)

    assert isinstance(ldl0011r2, LDL0011R2)
    assert ldl0011r2.from_ispb == '31680151'
    assert ldl0011r2.to_ispb == '00038166'
    assert ldl0011r2.system_domain == 'SPB01'
    assert ldl0011r2.operation_number == '316801512509080000001'
    assert ldl0011r2.message_code == 'LDL0011R2'
    assert ldl0011r2.str_control_number == 'STR20250101000000001'
    assert ldl0011r2.vendor_timestamp == datetime(2025, 12, 10, 10, 2, tzinfo=UTC)
    assert ldl0011r2.original_ldl_control_number == '321'
    assert ldl0011r2.institution_ispb == '31680151'
    assert ldl0011r2.branch == '001'
    assert ldl0011r2.account_number == '123456'
    assert ldl0011r2.ldl_ispb == '31680153'
    assert ldl0011r2.amount == Decimal('199.87')
    assert ldl0011r2.settlement_date == date(2025, 12, 10)


def test_ldl0011e_general_error_from_xml() -> None:
    xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/LDL/LDL0011E.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>316801512509080000001</NUOp>
        </BCMSG>
        <SISMSG>
            <LDL0011E CodErro="EGEN0050">
                <CodMsg>LDL0011</CodMsg>
                <NumCtrlIF>123</NumCtrlIF>
                <ISPBIF>31680151</ISPBIF>
                <NumCtrlLDLOr>321</NumCtrlLDLOr>
                <AgDebtd>001</AgDebtd>
                <CtDebtd>123456</CtDebtd>
                <ISPBLDL>31680153</ISPBLDL>
                <VlrLanc>199.87</VlrLanc>
                <DtMovto>2025-12-10</DtMovto>
            </LDL0011E>
        </SISMSG>
    </DOC>
    """

    ldl0011e = LDL0011E.from_xml(xml)

    assert isinstance(ldl0011e, LDL0011E)
    assert ldl0011e.from_ispb == '31680151'
    assert ldl0011e.to_ispb == '00038166'
    assert ldl0011e.system_domain == 'SPB01'
    assert ldl0011e.operation_number == '316801512509080000001'
    assert ldl0011e.message_code == 'LDL0011'
    assert ldl0011e.institution_control_number == '123'
    assert ldl0011e.institution_ispb == '31680151'
    assert ldl0011e.original_ldl_control_number == '321'
    assert ldl0011e.branch == '001'
    assert ldl0011e.account_number == '123456'
    assert ldl0011e.ldl_ispb == '31680153'
    assert ldl0011e.amount == Decimal('199.87')
    assert ldl0011e.settlement_date == date(2025, 12, 10)
    assert ldl0011e.general_error_code == 'EGEN0050'


def test_ldl0011e_tag_error_from_xml() -> None:
    xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/LDL/LDL0011E.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>316801512509080000001</NUOp>
        </BCMSG>
        <SISMSG>
            <LDL0011E>
                <CodMsg>LDL0011</CodMsg>
                <NumCtrlIF>123</NumCtrlIF>
                <ISPBIF>31680151</ISPBIF>
                <NumCtrlLDLOr>321</NumCtrlLDLOr>
                <AgDebtd>001</AgDebtd>
                <CtDebtd>123456</CtDebtd>
                <ISPBLDL CodErro="EGEN0051">31680153</ISPBLDL>
                <VlrLanc>199.87</VlrLanc>
                <DtMovto>2025-12-10</DtMovto>
            </LDL0011E>
        </SISMSG>
    </DOC>
    """

    ldl0011e = LDL0011E.from_xml(xml)

    assert isinstance(ldl0011e, LDL0011E)
    assert ldl0011e.from_ispb == '31680151'
    assert ldl0011e.to_ispb == '00038166'
    assert ldl0011e.system_domain == 'SPB01'
    assert ldl0011e.operation_number == '316801512509080000001'
    assert ldl0011e.message_code == 'LDL0011'
    assert ldl0011e.institution_control_number == '123'
    assert ldl0011e.institution_ispb == '31680151'
    assert ldl0011e.original_ldl_control_number == '321'
    assert ldl0011e.branch == '001'
    assert ldl0011e.account_number == '123456'
    assert ldl0011e.ldl_ispb == '31680153'
    assert ldl0011e.amount == Decimal('199.87')
    assert ldl0011e.settlement_date == date(2025, 12, 10)
    assert ldl0011e.ldl_ispb_error_code == 'EGEN0051'


def test_ldl0011_roundtrip() -> None:
    params = make_valid_ldl0011_params()

    ldl0011 = LDL0011.model_validate(params)
    xml = ldl0011.to_xml()
    ldl0011_from_xml = LDL0011.from_xml(xml)

    assert ldl0011 == ldl0011_from_xml


def test_ldl0011r1_roundtrip() -> None:
    params = make_valid_ldl0011r1_params()

    ldl0011r1 = LDL0011R1.model_validate(params)
    xml = ldl0011r1.to_xml()
    ldl0011r1_from_xml = LDL0011R1.from_xml(xml)

    assert ldl0011r1 == ldl0011r1_from_xml


def test_ldl0011r2_roundtrip() -> None:
    params = make_valid_ldl0011r2_params()

    ldl0011r2 = LDL0011R2.model_validate(params)
    xml = ldl0011r2.to_xml()
    ldl0011r2_from_xml = LDL0011R2.from_xml(xml)

    assert ldl0011r2 == ldl0011r2_from_xml


def test_ldl0011_from_xml_missing_required_fields() -> None:
    xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/LDL/LDL0011.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>316801512509080000001</NUOp>
        </BCMSG>
        <SISMSG>
            <LDL0011>
                <CodMsg>LDL0011</CodMsg>
            </LDL0011>
        </SISMSG>
    </DOC>
    """

    with pytest.raises(ValidationError) as exc:
        LDL0011.from_xml(xml)

    missing_fields = extract_missing_fields(exc.value)
    assert missing_fields == {
        'institution_control_number',
        'institution_ispb',
        'original_ldl_control_number',
        'branch',
        'account_number',
        'ldl_ispb',
        'amount',
        'settlement_date',
    }
