from datetime import date, datetime
from decimal import Decimal
from typing import Any

import pytest
from pydantic import ValidationError

from sfn_messages.core.types import LdlSettlementStatus, ProductCode
from sfn_messages.ldl.ldl0022 import LDL0022, LDL0022E, LDL0022R1, LDL0022R2
from tests.conftest import extract_missing_fields, normalize_xml


def make_valid_ldl0022_params() -> dict[str, Any]:
    return {
        'from_ispb': '31680151',
        'to_ispb': '00038166',
        'system_domain': 'SPB01',
        'operation_number': '31680151250908000000001',
        'message_code': 'LDL0022',
        'institution_control_number': '123',
        'institution_ispb': '31680151',
        'ldl_ispb': '31680153',
        'product_code': 'AMEX_CREDIT_CARD',
        'amount': 177.22,
        'settlement_date': '2025-12-10',
    }


def make_valid_ldl0022r1_params() -> dict[str, Any]:
    return {
        'from_ispb': '31680151',
        'to_ispb': '00038166',
        'system_domain': 'SPB01',
        'operation_number': '31680151250908000000001',
        'message_code': 'LDL0022R1',
        'institution_control_number': '123',
        'institution_ispb': '31680151',
        'str_control_number': 'STR20250101000000001',
        'ldl_settlement_status': 'EFFECTIVE',
        'settlement_timestamp': '2025-12-10T15:30:00',
        'settlement_date': '2025-12-10',
    }


def make_valid_ldl0022r2_params() -> dict[str, Any]:
    return {
        'from_ispb': '31680151',
        'to_ispb': '00038166',
        'system_domain': 'SPB01',
        'operation_number': '31680151250908000000001',
        'message_code': 'LDL0022R2',
        'str_control_number': 'STR20250101000000001',
        'vendor_timestamp': '2025-12-10T15:45:00',
        'institution_ispb': '31680151',
        'ldl_ispb': '31680153',
        'product_code': 'AMEX_CREDIT_CARD',
        'amount': 177.22,
        'settlement_date': '2025-12-10',
    }


def make_valid_ldl0022e_params(*, general_error: bool = False) -> dict[str, Any]:
    ldl0022e = {
        'from_ispb': '31680151',
        'to_ispb': '00038166',
        'system_domain': 'SPB01',
        'operation_number': '31680151250908000000001',
        'message_code': 'LDL0022E',
        'institution_control_number': '123',
        'institution_ispb': '31680151',
        'ldl_ispb': '31680153',
        'product_code': 'AMEX_CREDIT_CARD',
        'amount': 177.22,
        'settlement_date': '2025-12-10',
    }

    if general_error:
        ldl0022e['general_error_code'] = 'EGEN0050'
    else:
        ldl0022e['ldl_ispb_error_code'] = 'ELDL0123'

    return ldl0022e


def test_ldl0022_valid_model() -> None:
    params = make_valid_ldl0022_params()
    ldl0022 = LDL0022.model_validate(params)

    assert isinstance(ldl0022, LDL0022)
    assert ldl0022.from_ispb == '31680151'
    assert ldl0022.to_ispb == '00038166'
    assert ldl0022.system_domain == 'SPB01'
    assert ldl0022.operation_number == '31680151250908000000001'
    assert ldl0022.message_code == 'LDL0022'
    assert ldl0022.institution_control_number == '123'
    assert ldl0022.institution_ispb == '31680151'
    assert ldl0022.ldl_ispb == '31680153'
    assert ldl0022.product_code == ProductCode.AMEX_CREDIT_CARD
    assert ldl0022.amount == Decimal('177.22')
    assert ldl0022.settlement_date == date(2025, 12, 10)


def test_ldl0022r1_valid_model() -> None:
    params = make_valid_ldl0022r1_params()
    ldl0022r1 = LDL0022R1.model_validate(params)

    assert isinstance(ldl0022r1, LDL0022R1)
    assert ldl0022r1.from_ispb == '31680151'
    assert ldl0022r1.to_ispb == '00038166'
    assert ldl0022r1.system_domain == 'SPB01'
    assert ldl0022r1.operation_number == '31680151250908000000001'
    assert ldl0022r1.message_code == 'LDL0022R1'
    assert ldl0022r1.institution_control_number == '123'
    assert ldl0022r1.institution_ispb == '31680151'
    assert ldl0022r1.str_control_number == 'STR20250101000000001'
    assert ldl0022r1.ldl_settlement_status == LdlSettlementStatus.EFFECTIVE
    assert ldl0022r1.settlement_timestamp == datetime(2025, 12, 10, 15, 30)
    assert ldl0022r1.settlement_date == date(2025, 12, 10)


def test_ldl0022r2_valid_model() -> None:
    params = make_valid_ldl0022r2_params()
    ldl0022r2 = LDL0022R2.model_validate(params)

    assert isinstance(ldl0022r2, LDL0022R2)
    assert ldl0022r2.from_ispb == '31680151'
    assert ldl0022r2.to_ispb == '00038166'
    assert ldl0022r2.system_domain == 'SPB01'
    assert ldl0022r2.operation_number == '31680151250908000000001'
    assert ldl0022r2.message_code == 'LDL0022R2'
    assert ldl0022r2.str_control_number == 'STR20250101000000001'
    assert ldl0022r2.vendor_timestamp == datetime(2025, 12, 10, 15, 45)
    assert ldl0022r2.institution_ispb == '31680151'
    assert ldl0022r2.ldl_ispb == '31680153'
    assert ldl0022r2.product_code == ProductCode.AMEX_CREDIT_CARD
    assert ldl0022r2.amount == Decimal('177.22')
    assert ldl0022r2.settlement_date == date(2025, 12, 10)


def test_ldl0022e_valid_model() -> None:
    params = make_valid_ldl0022e_params()
    ldl0022e = LDL0022E.model_validate(params)

    assert isinstance(ldl0022e, LDL0022E)
    assert ldl0022e.from_ispb == '31680151'
    assert ldl0022e.to_ispb == '00038166'
    assert ldl0022e.system_domain == 'SPB01'
    assert ldl0022e.operation_number == '31680151250908000000001'
    assert ldl0022e.message_code == 'LDL0022E'
    assert ldl0022e.institution_control_number == '123'
    assert ldl0022e.institution_ispb == '31680151'
    assert ldl0022e.ldl_ispb == '31680153'
    assert ldl0022e.product_code == ProductCode.AMEX_CREDIT_CARD
    assert ldl0022e.amount == Decimal('177.22')
    assert ldl0022e.settlement_date == date(2025, 12, 10)

    assert ldl0022e.ldl_ispb_error_code == 'ELDL0123'


def test_ldl0022_missing_required_fields() -> None:
    with pytest.raises(ValidationError) as exc:
        LDL0022.model_validate({})

    missing_fields = extract_missing_fields(exc.value)
    assert missing_fields == {
        'from_ispb',
        'to_ispb',
        'system_domain',
        'operation_number',
        'institution_control_number',
        'institution_ispb',
        'ldl_ispb',
        'product_code',
        'amount',
        'settlement_date',
    }


def test_ldl0022r1_missing_required_fields() -> None:
    with pytest.raises(ValidationError) as exc:
        LDL0022R1.model_validate({})

    missing_fields = extract_missing_fields(exc.value)
    assert missing_fields == {
        'from_ispb',
        'to_ispb',
        'system_domain',
        'operation_number',
        'institution_control_number',
        'institution_ispb',
        'str_control_number',
        'ldl_settlement_status',
        'settlement_timestamp',
        'settlement_date',
    }


def test_ldl0022r2_missing_required_fields() -> None:
    with pytest.raises(ValidationError) as exc:
        LDL0022R2.model_validate({})

    missing_fields = extract_missing_fields(exc.value)
    assert missing_fields == {
        'from_ispb',
        'to_ispb',
        'system_domain',
        'operation_number',
        'str_control_number',
        'vendor_timestamp',
        'institution_ispb',
        'ldl_ispb',
        'product_code',
        'amount',
        'settlement_date',
    }


def test_ldl0022_to_xml() -> None:
    params = make_valid_ldl0022_params()
    ldl0022 = LDL0022.model_validate(params)

    xml = ldl0022.to_xml()

    expected_xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/SPB/LDL0022.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>31680151250908000000001</NUOp>
        </BCMSG>
        <SISMSG>
            <LDL0022>
                <CodMsg>LDL0022</CodMsg>
                <NumCtrlIF>123</NumCtrlIF>
                <ISPBIF>31680151</ISPBIF>
                <ISPBLDL>31680153</ISPBLDL>
                <CodProdt>ACC</CodProdt>
                <VlrLanc>177.22</VlrLanc>
                <DtMovto>2025-12-10</DtMovto>
            </LDL0022>
        </SISMSG>
    </DOC>
    """
    assert normalize_xml(expected_xml) == normalize_xml(xml)


def test_ldl0022r1_to_xml() -> None:
    params = make_valid_ldl0022r1_params()
    ldl0022r1 = LDL0022R1.model_validate(params)

    xml = ldl0022r1.to_xml()

    expected_xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/SPB/LDL0022.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>31680151250908000000001</NUOp>
        </BCMSG>
        <SISMSG>
            <LDL0022R1>
                <CodMsg>LDL0022R1</CodMsg>
                <NumCtrlIF>123</NumCtrlIF>
                <ISPBIF>31680151</ISPBIF>
                <NumCtrlSTR>STR20250101000000001</NumCtrlSTR>
                <SitLancLDL>1</SitLancLDL>
                <DtHrSit>2025-12-10T15:30:00</DtHrSit>
                <DtMovto>2025-12-10</DtMovto>
            </LDL0022R1>
        </SISMSG>
    </DOC>
    """
    assert normalize_xml(expected_xml) == normalize_xml(xml)


def test_ldl0022r2_to_xml() -> None:
    params = make_valid_ldl0022r2_params()
    ldl0022r2 = LDL0022R2.model_validate(params)

    xml = ldl0022r2.to_xml()

    expected_xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/SPB/LDL0022.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>31680151250908000000001</NUOp>
        </BCMSG>
        <SISMSG>
            <LDL0022R2>
                <CodMsg>LDL0022R2</CodMsg>
                <NumCtrlSTR>STR20250101000000001</NumCtrlSTR>
                <DtHrBC>2025-12-10T15:45:00</DtHrBC>
                <ISPBIF>31680151</ISPBIF>
                <ISPBLDL>31680153</ISPBLDL>
                <CodProdt>ACC</CodProdt>
                <VlrLanc>177.22</VlrLanc>
                <DtMovto>2025-12-10</DtMovto>
            </LDL0022R2>
        </SISMSG>
    </DOC>
    """
    assert normalize_xml(expected_xml) == normalize_xml(xml)


def test_ldl0022e_general_error_to_xml() -> None:
    params = make_valid_ldl0022e_params(general_error=True)
    ldl0022e = LDL0022E.model_validate(params)

    xml = ldl0022e.to_xml()

    expected_xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/SPB/LDL0022E.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>31680151250908000000001</NUOp>
        </BCMSG>
        <SISMSG>
            <LDL0022 CodErro="EGEN0050">
                <CodMsg>LDL0022E</CodMsg>
                <NumCtrlIF>123</NumCtrlIF>
                <ISPBIF>31680151</ISPBIF>
                <ISPBLDL>31680153</ISPBLDL>
                <CodProdt>ACC</CodProdt>
                <VlrLanc>177.22</VlrLanc>
                <DtMovto>2025-12-10</DtMovto>
            </LDL0022>
        </SISMSG>
    </DOC>
    """
    assert normalize_xml(expected_xml) == normalize_xml(xml)


def test_ldl0022e_tag_error_to_xml() -> None:
    params = make_valid_ldl0022e_params()
    ldl0022e = LDL0022E.model_validate(params)

    xml = ldl0022e.to_xml()

    expected_xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/SPB/LDL0022E.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>31680151250908000000001</NUOp>
        </BCMSG>
        <SISMSG>
            <LDL0022>
                <CodMsg>LDL0022E</CodMsg>
                <NumCtrlIF>123</NumCtrlIF>
                <ISPBIF>31680151</ISPBIF>
                <ISPBLDL CodErro="ELDL0123">31680153</ISPBLDL>
                <CodProdt>ACC</CodProdt>
                <VlrLanc>177.22</VlrLanc>
                <DtMovto>2025-12-10</DtMovto>
            </LDL0022>
        </SISMSG>
    </DOC>
    """
    assert normalize_xml(expected_xml) == normalize_xml(xml)


def test_ldl0022_from_xml() -> None:
    xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/SPB/LDL0022.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>31680151250908000000001</NUOp>
        </BCMSG>
        <SISMSG>
            <LDL0022>
                <CodMsg>LDL0022</CodMsg>
                <NumCtrlIF>123</NumCtrlIF>
                <ISPBIF>31680151</ISPBIF>
                <ISPBLDL>31680153</ISPBLDL>
                <CodProdt>ACC</CodProdt>
                <VlrLanc>177.22</VlrLanc>
                <DtMovto>2025-12-10</DtMovto>
            </LDL0022>
        </SISMSG>
    </DOC>
    """

    ldl0022 = LDL0022.from_xml(xml)

    assert isinstance(ldl0022, LDL0022)
    assert ldl0022.from_ispb == '31680151'
    assert ldl0022.to_ispb == '00038166'
    assert ldl0022.system_domain == 'SPB01'
    assert ldl0022.operation_number == '31680151250908000000001'
    assert ldl0022.message_code == 'LDL0022'
    assert ldl0022.institution_control_number == '123'
    assert ldl0022.institution_ispb == '31680151'
    assert ldl0022.ldl_ispb == '31680153'
    assert ldl0022.product_code == ProductCode.AMEX_CREDIT_CARD
    assert ldl0022.amount == Decimal('177.22')
    assert ldl0022.settlement_date == date(2025, 12, 10)


def test_ldl0022r1_from_xml() -> None:
    xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/SPB/LDL0022.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>31680151250908000000001</NUOp>
        </BCMSG>
        <SISMSG>
            <LDL0022R1>
                <CodMsg>LDL0022R1</CodMsg>
                <NumCtrlIF>123</NumCtrlIF>
                <ISPBIF>31680151</ISPBIF>
                <NumCtrlSTR>STR20250101000000001</NumCtrlSTR>
                <SitLancLDL>1</SitLancLDL>
                <DtHrSit>2025-12-10T15:30:00</DtHrSit>
                <DtMovto>2025-12-10</DtMovto>
            </LDL0022R1>
        </SISMSG>
    </DOC>
    """

    ldl0022r1 = LDL0022R1.from_xml(xml)

    assert isinstance(ldl0022r1, LDL0022R1)
    assert ldl0022r1.from_ispb == '31680151'
    assert ldl0022r1.to_ispb == '00038166'
    assert ldl0022r1.system_domain == 'SPB01'
    assert ldl0022r1.operation_number == '31680151250908000000001'
    assert ldl0022r1.message_code == 'LDL0022R1'
    assert ldl0022r1.institution_control_number == '123'
    assert ldl0022r1.institution_ispb == '31680151'
    assert ldl0022r1.str_control_number == 'STR20250101000000001'
    assert ldl0022r1.ldl_settlement_status == LdlSettlementStatus.EFFECTIVE
    assert ldl0022r1.settlement_timestamp == datetime(2025, 12, 10, 15, 30)
    assert ldl0022r1.settlement_date == date(2025, 12, 10)


def test_ldl0022r2_from_xml() -> None:
    xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/SPB/LDL0022.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>31680151250908000000001</NUOp>
        </BCMSG>
        <SISMSG>
            <LDL0022R2>
                <CodMsg>LDL0022R2</CodMsg>
                <NumCtrlSTR>STR20250101000000001</NumCtrlSTR>
                <DtHrBC>2025-12-10T15:45:00</DtHrBC>
                <ISPBIF>31680151</ISPBIF>
                <ISPBLDL>31680153</ISPBLDL>
                <CodProdt>ACC</CodProdt>
                <VlrLanc>177.22</VlrLanc>
                <DtMovto>2025-12-10</DtMovto>
            </LDL0022R2>
        </SISMSG>
    </DOC>
    """

    ldl0022r2 = LDL0022R2.from_xml(xml)

    assert isinstance(ldl0022r2, LDL0022R2)
    assert ldl0022r2.from_ispb == '31680151'
    assert ldl0022r2.to_ispb == '00038166'
    assert ldl0022r2.system_domain == 'SPB01'
    assert ldl0022r2.operation_number == '31680151250908000000001'
    assert ldl0022r2.message_code == 'LDL0022R2'
    assert ldl0022r2.str_control_number == 'STR20250101000000001'
    assert ldl0022r2.vendor_timestamp == datetime(2025, 12, 10, 15, 45)
    assert ldl0022r2.institution_ispb == '31680151'
    assert ldl0022r2.ldl_ispb == '31680153'
    assert ldl0022r2.product_code == ProductCode.AMEX_CREDIT_CARD
    assert ldl0022r2.amount == Decimal('177.22')
    assert ldl0022r2.settlement_date == date(2025, 12, 10)


def test_ldl0022e_general_error_from_xml() -> None:
    xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/SPB/LDL0022E.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>31680151250908000000001</NUOp>
        </BCMSG>
        <SISMSG>
            <LDL0022 CodErro="EGEN0050">
                <CodMsg>LDL0022E</CodMsg>
                <NumCtrlIF>123</NumCtrlIF>
                <ISPBIF>31680151</ISPBIF>
                <ISPBLDL>31680153</ISPBLDL>
                <CodProdt>ACC</CodProdt>
                <VlrLanc>177.22</VlrLanc>
                <DtMovto>2025-12-10</DtMovto>
            </LDL0022>
        </SISMSG>
    </DOC>
    """

    ldl0022e = LDL0022E.from_xml(xml)

    assert isinstance(ldl0022e, LDL0022E)
    assert ldl0022e.from_ispb == '31680151'
    assert ldl0022e.to_ispb == '00038166'
    assert ldl0022e.system_domain == 'SPB01'
    assert ldl0022e.operation_number == '31680151250908000000001'
    assert ldl0022e.message_code == 'LDL0022E'
    assert ldl0022e.institution_control_number == '123'
    assert ldl0022e.institution_ispb == '31680151'
    assert ldl0022e.ldl_ispb == '31680153'
    assert ldl0022e.product_code == ProductCode.AMEX_CREDIT_CARD
    assert ldl0022e.amount == Decimal('177.22')
    assert ldl0022e.settlement_date == date(2025, 12, 10)

    assert ldl0022e.general_error_code == 'EGEN0050'


def test_ldl0022e_tag_error_from_xml() -> None:
    xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/SPB/LDL0022E.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>31680151250908000000001</NUOp>
        </BCMSG>
        <SISMSG>
            <LDL0022>
                <CodMsg>LDL0022E</CodMsg>
                <NumCtrlIF>123</NumCtrlIF>
                <ISPBIF>31680151</ISPBIF>
                <ISPBLDL CodErro="ELDL0123">31680153</ISPBLDL>
                <CodProdt>ACC</CodProdt>
                <VlrLanc>177.22</VlrLanc>
                <DtMovto>2025-12-10</DtMovto>
            </LDL0022>
        </SISMSG>
    </DOC>
    """

    ldl0022e = LDL0022E.from_xml(xml)

    assert isinstance(ldl0022e, LDL0022E)
    assert ldl0022e.from_ispb == '31680151'
    assert ldl0022e.to_ispb == '00038166'
    assert ldl0022e.system_domain == 'SPB01'
    assert ldl0022e.operation_number == '31680151250908000000001'
    assert ldl0022e.message_code == 'LDL0022E'
    assert ldl0022e.institution_control_number == '123'
    assert ldl0022e.institution_ispb == '31680151'
    assert ldl0022e.ldl_ispb == '31680153'
    assert ldl0022e.product_code == ProductCode.AMEX_CREDIT_CARD
    assert ldl0022e.amount == Decimal('177.22')
    assert ldl0022e.settlement_date == date(2025, 12, 10)

    assert ldl0022e.ldl_ispb_error_code == 'ELDL0123'


def test_ldl0022_roundtrip() -> None:
    params = make_valid_ldl0022_params()

    ldl0022 = LDL0022.model_validate(params)
    xml = ldl0022.to_xml()
    ldl0022_from_xml = LDL0022.from_xml(xml)

    assert ldl0022 == ldl0022_from_xml


def test_ldl0022r1_roundtrip() -> None:
    params = make_valid_ldl0022r1_params()

    ldl0022r1 = LDL0022R1.model_validate(params)
    xml = ldl0022r1.to_xml()
    ldl0022r1_from_xml = LDL0022R1.from_xml(xml)

    assert ldl0022r1 == ldl0022r1_from_xml


def test_ldl0022r2_roundtrip() -> None:
    params = make_valid_ldl0022r2_params()

    ldl0022r2 = LDL0022R2.model_validate(params)
    xml = ldl0022r2.to_xml()
    ldl0022r2_from_xml = LDL0022R2.from_xml(xml)

    assert ldl0022r2 == ldl0022r2_from_xml


def test_ldl0022_from_xml_missing_required_fields() -> None:
    xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/SPB/LDL0022.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>31680151250908000000001</NUOp>
        </BCMSG>
        <SISMSG>
            <LDL0022>
                <CodMsg>LDL0022</CodMsg>
            </LDL0022>
        </SISMSG>
    </DOC>
    """

    with pytest.raises(ValidationError) as exc:
        LDL0022.from_xml(xml)

    missing_fields = extract_missing_fields(exc.value)
    assert missing_fields == {
        'institution_control_number',
        'institution_ispb',
        'ldl_ispb',
        'product_code',
        'amount',
        'settlement_date',
    }
