from datetime import UTC, date, datetime
from decimal import Decimal
from typing import Any

import pytest
from pydantic import ValidationError

from sfn_messages.core.types import StrSettlementStatus
from sfn_messages.ltr.ltr0006 import LTR0006, LTR0006E, LTR0006R1, LTR0006R2
from tests.conftest import extract_missing_fields, normalize_xml


def make_valid_ltr0006_params() -> dict[str, Any]:
    return {
        'from_ispb': '31680151',
        'to_ispb': '00038166',
        'system_domain': 'SPB01',
        'operation_number': '31680151250908000000001',
        'message_code': 'LTR0006',
        'institution_or_ltr_control_number': '123',
        'debtor_institution_or_ltr_ispb': '31680151',
        'creditor_institution_or_ltr_ispb': '31680152',
        'original_ltr_control_number': '321',
        'amount': 123.0,
        'description': 'Test description',
        'settlement_date': '2025-12-04',
    }


def make_valid_ltr0006r1_params() -> dict[str, Any]:
    return {
        'from_ispb': '31680151',
        'to_ispb': '00038166',
        'system_domain': 'SPB01',
        'operation_number': '31680151250908000000001',
        'message_code': 'LTR0006R1',
        'institution_or_ltr_control_number': '123',
        'debtor_institution_or_ltr_ispb': '31680151',
        'str_control_number': 'STR20250101000000001',
        'str_settlement_status': 'EFFECTIVE',
        'settlement_timestamp': '2025-12-04T13:21:00+00:00',
        'settlement_date': '2025-12-04',
    }


def make_valid_ltr0006r2_params() -> dict[str, Any]:
    return {
        'from_ispb': '31680151',
        'to_ispb': '00038166',
        'system_domain': 'SPB01',
        'operation_number': '31680151250908000000001',
        'message_code': 'LTR0006R2',
        'str_control_number': 'STR20250101000000001',
        'debtor_institution_or_ltr_ispb': '31680151',
        'creditor_institution_or_ltr_ispb': '31680152',
        'amount': 123.0,
        'original_str_control_number': 'STR20250101000000001',
        'description': 'Test description',
        'vendor_timestamp': '2025-12-04T13:22:00+00:00',
        'settlement_date': '2025-12-04',
    }


def make_valid_ltr0006e_params(*, general_error: bool = False) -> dict[str, Any]:
    ltr0006e = {
        'from_ispb': '31680151',
        'to_ispb': '00038166',
        'system_domain': 'SPB01',
        'operation_number': '31680151250908000000001',
        'message_code': 'LTR0006',
        'institution_or_ltr_control_number': '123',
        'debtor_institution_or_ltr_ispb': '31680151',
        'creditor_institution_or_ltr_ispb': '31680152',
        'original_ltr_control_number': '321',
        'amount': 123.0,
        'description': 'Test description',
        'settlement_date': '2025-12-04',
    }

    if general_error:
        ltr0006e['general_error_code'] = 'EGEN0050'
    else:
        ltr0006e['original_ltr_control_number_error_code'] = 'EGEN0051'

    return ltr0006e


def test_ltr0006_valid_model() -> None:
    params = make_valid_ltr0006_params()
    ltr0006 = LTR0006.model_validate(params)

    assert isinstance(ltr0006, LTR0006)
    assert ltr0006.from_ispb == '31680151'
    assert ltr0006.to_ispb == '00038166'
    assert ltr0006.system_domain == 'SPB01'
    assert ltr0006.operation_number == '31680151250908000000001'
    assert ltr0006.message_code == 'LTR0006'
    assert ltr0006.institution_or_ltr_control_number == '123'
    assert ltr0006.debtor_institution_or_ltr_ispb == '31680151'
    assert ltr0006.creditor_institution_or_ltr_ispb == '31680152'
    assert ltr0006.original_ltr_control_number == '321'
    assert ltr0006.amount == Decimal('123.0')
    assert ltr0006.description == 'Test description'
    assert ltr0006.settlement_date == date(2025, 12, 4)


def test_ltr0006r1_valid_model() -> None:
    params = make_valid_ltr0006r1_params()
    ltr0006r1 = LTR0006R1.model_validate(params)

    assert isinstance(ltr0006r1, LTR0006R1)
    assert ltr0006r1.from_ispb == '31680151'
    assert ltr0006r1.to_ispb == '00038166'
    assert ltr0006r1.system_domain == 'SPB01'
    assert ltr0006r1.operation_number == '31680151250908000000001'
    assert ltr0006r1.message_code == 'LTR0006R1'
    assert ltr0006r1.institution_or_ltr_control_number == '123'
    assert ltr0006r1.debtor_institution_or_ltr_ispb == '31680151'
    assert ltr0006r1.str_control_number == 'STR20250101000000001'
    assert ltr0006r1.str_settlement_status == StrSettlementStatus.EFFECTIVE
    assert ltr0006r1.settlement_timestamp == datetime(2025, 12, 4, 13, 21, tzinfo=UTC)
    assert ltr0006r1.settlement_date == date(2025, 12, 4)


def test_ltr0006r2_valid_model() -> None:
    params = make_valid_ltr0006r2_params()
    ltr0006r2 = LTR0006R2.model_validate(params)

    assert isinstance(ltr0006r2, LTR0006R2)
    assert ltr0006r2.from_ispb == '31680151'
    assert ltr0006r2.to_ispb == '00038166'
    assert ltr0006r2.system_domain == 'SPB01'
    assert ltr0006r2.operation_number == '31680151250908000000001'
    assert ltr0006r2.message_code == 'LTR0006R2'
    assert ltr0006r2.str_control_number == 'STR20250101000000001'
    assert ltr0006r2.debtor_institution_or_ltr_ispb == '31680151'
    assert ltr0006r2.creditor_institution_or_ltr_ispb == '31680152'
    assert ltr0006r2.amount == Decimal('123.0')
    assert ltr0006r2.original_str_control_number == 'STR20250101000000001'
    assert ltr0006r2.description == 'Test description'
    assert ltr0006r2.vendor_timestamp == datetime(2025, 12, 4, 13, 22, tzinfo=UTC)
    assert ltr0006r2.settlement_date == date(2025, 12, 4)


def test_ltr0006e_general_error_valid_model() -> None:
    params = make_valid_ltr0006e_params(general_error=True)
    ltr0006e = LTR0006E.model_validate(params)

    assert isinstance(ltr0006e, LTR0006E)
    assert ltr0006e.from_ispb == '31680151'
    assert ltr0006e.to_ispb == '00038166'
    assert ltr0006e.system_domain == 'SPB01'
    assert ltr0006e.operation_number == '31680151250908000000001'
    assert ltr0006e.message_code == 'LTR0006'
    assert ltr0006e.institution_or_ltr_control_number == '123'
    assert ltr0006e.debtor_institution_or_ltr_ispb == '31680151'
    assert ltr0006e.creditor_institution_or_ltr_ispb == '31680152'
    assert ltr0006e.original_ltr_control_number == '321'
    assert ltr0006e.amount == Decimal('123.0')
    assert ltr0006e.description == 'Test description'
    assert ltr0006e.settlement_date == date(2025, 12, 4)

    assert ltr0006e.general_error_code == 'EGEN0050'


def test_ltr0006e_tag_error_valid_model() -> None:
    params = make_valid_ltr0006e_params()
    ltr0006e = LTR0006E.model_validate(params)

    assert isinstance(ltr0006e, LTR0006E)
    assert ltr0006e.from_ispb == '31680151'
    assert ltr0006e.to_ispb == '00038166'
    assert ltr0006e.system_domain == 'SPB01'
    assert ltr0006e.operation_number == '31680151250908000000001'
    assert ltr0006e.message_code == 'LTR0006'
    assert ltr0006e.institution_or_ltr_control_number == '123'
    assert ltr0006e.debtor_institution_or_ltr_ispb == '31680151'
    assert ltr0006e.creditor_institution_or_ltr_ispb == '31680152'
    assert ltr0006e.original_ltr_control_number == '321'
    assert ltr0006e.amount == Decimal('123.0')
    assert ltr0006e.description == 'Test description'
    assert ltr0006e.settlement_date == date(2025, 12, 4)

    assert ltr0006e.original_ltr_control_number_error_code == 'EGEN0051'


def test_ltr0006_missing_required_fields() -> None:
    with pytest.raises(ValidationError) as exc:
        LTR0006.model_validate({})

    missing_fields = extract_missing_fields(exc.value)
    assert missing_fields == {
        'from_ispb',
        'to_ispb',
        'system_domain',
        'operation_number',
        'institution_or_ltr_control_number',
        'debtor_institution_or_ltr_ispb',
        'creditor_institution_or_ltr_ispb',
        'original_ltr_control_number',
        'amount',
        'settlement_date',
    }


def test_ltr0006r1_missing_required_fields() -> None:
    with pytest.raises(ValidationError) as exc:
        LTR0006R1.model_validate({})

    missing_fields = extract_missing_fields(exc.value)
    assert missing_fields == {
        'from_ispb',
        'to_ispb',
        'system_domain',
        'operation_number',
        'institution_or_ltr_control_number',
        'debtor_institution_or_ltr_ispb',
        'str_control_number',
        'str_settlement_status',
        'settlement_timestamp',
        'settlement_date',
    }


def test_ltr0006r2_missing_required_fields() -> None:
    with pytest.raises(ValidationError) as exc:
        LTR0006R2.model_validate({})

    missing_fields = extract_missing_fields(exc.value)
    assert missing_fields == {
        'from_ispb',
        'to_ispb',
        'system_domain',
        'operation_number',
        'str_control_number',
        'debtor_institution_or_ltr_ispb',
        'creditor_institution_or_ltr_ispb',
        'amount',
        'original_str_control_number',
        'vendor_timestamp',
        'settlement_date',
    }


def test_ltr0006_to_xml() -> None:
    params = make_valid_ltr0006_params()
    ltr0006 = LTR0006.model_validate(params)

    xml = ltr0006.to_xml()

    expected_xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/LTR/LTR0006.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>31680151250908000000001</NUOp>
        </BCMSG>
        <SISMSG>
            <LTR0006>
                <CodMsg>LTR0006</CodMsg>
                <NumCtrlIF_LTR>123</NumCtrlIF_LTR>
                <ISPBIF_LTRDebtd>31680151</ISPBIF_LTRDebtd>
                <ISPBIF_LTRCredtd>31680152</ISPBIF_LTRCredtd>
                <NumCtrlLTROr>321</NumCtrlLTROr>
                <VlrLanc>123.0</VlrLanc>
                <Hist>Test description</Hist>
                <DtMovto>2025-12-04</DtMovto>
            </LTR0006>
        </SISMSG>
    </DOC>
    """
    assert normalize_xml(expected_xml) == normalize_xml(xml)


def test_ltr0006r1_to_xml() -> None:
    params = make_valid_ltr0006r1_params()
    ltr0006r1 = LTR0006R1.model_validate(params)

    xml = ltr0006r1.to_xml()

    expected_xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/LTR/LTR0006.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>31680151250908000000001</NUOp>
        </BCMSG>
        <SISMSG>
            <LTR0006R1>
                <CodMsg>LTR0006R1</CodMsg>
                <NumCtrlIF_LTR>123</NumCtrlIF_LTR>
                <ISPBIF_LTRDebtd>31680151</ISPBIF_LTRDebtd>
                <NumCtrlSTR>STR20250101000000001</NumCtrlSTR>
                <SitLancSTR>1</SitLancSTR>
                <DtHrSit>2025-12-04 13:21:00+00:00</DtHrSit>
                <DtMovto>2025-12-04</DtMovto>
            </LTR0006R1>
        </SISMSG>
    </DOC>
    """

    assert normalize_xml(expected_xml) == normalize_xml(xml)


def test_ltr0006r2_to_xml() -> None:
    params = make_valid_ltr0006r2_params()
    ltr0006r2 = LTR0006R2.model_validate(params)

    xml = ltr0006r2.to_xml()

    expected_xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/LTR/LTR0006.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>31680151250908000000001</NUOp>
        </BCMSG>
        <SISMSG>
            <LTR0006R2>
                <CodMsg>LTR0006R2</CodMsg>
                <NumCtrlSTR>STR20250101000000001</NumCtrlSTR>
                <ISPBIF_LTRDebtd>31680151</ISPBIF_LTRDebtd>
                <ISPBIF_LTRCredtd>31680152</ISPBIF_LTRCredtd>
                <VlrLanc>123.0</VlrLanc>
                <NumCtrlSTROr>STR20250101000000001</NumCtrlSTROr>
                <Hist>Test description</Hist>
                <DtHrBC>2025-12-04 13:22:00+00:00</DtHrBC>
                <DtMovto>2025-12-04</DtMovto>
            </LTR0006R2>
        </SISMSG>
    </DOC>
    """
    assert normalize_xml(expected_xml) == normalize_xml(xml)


def test_ltr0006e_general_error_to_xml() -> None:
    params = make_valid_ltr0006e_params(general_error=True)
    ltr0006e = LTR0006E.model_validate(params)

    xml = ltr0006e.to_xml()

    expected_xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/LTR/LTR0006E.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>31680151250908000000001</NUOp>
        </BCMSG>
        <SISMSG>
            <LTR0006E CodErro="EGEN0050">
                <CodMsg>LTR0006</CodMsg>
                <NumCtrlIF_LTR>123</NumCtrlIF_LTR>
                <ISPBIF_LTRDebtd>31680151</ISPBIF_LTRDebtd>
                <ISPBIF_LTRCredtd>31680152</ISPBIF_LTRCredtd>
                <NumCtrlLTROr>321</NumCtrlLTROr>
                <VlrLanc>123.0</VlrLanc>
                <Hist>Test description</Hist>
                <DtMovto>2025-12-04</DtMovto>
            </LTR0006E>
        </SISMSG>
    </DOC>
    """
    assert normalize_xml(expected_xml) == normalize_xml(xml)


def test_ltr0006e_tag_error_to_xml() -> None:
    params = make_valid_ltr0006e_params()
    ltr0006e = LTR0006E.model_validate(params)

    xml = ltr0006e.to_xml()

    expected_xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/LTR/LTR0006E.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>31680151250908000000001</NUOp>
        </BCMSG>
        <SISMSG>
            <LTR0006E>
                <CodMsg>LTR0006</CodMsg>
                <NumCtrlIF_LTR>123</NumCtrlIF_LTR>
                <ISPBIF_LTRDebtd>31680151</ISPBIF_LTRDebtd>
                <ISPBIF_LTRCredtd>31680152</ISPBIF_LTRCredtd>
                <NumCtrlLTROr CodErro="EGEN0051">321</NumCtrlLTROr>
                <VlrLanc>123.0</VlrLanc>
                <Hist>Test description</Hist>
                <DtMovto>2025-12-04</DtMovto>
            </LTR0006E>
        </SISMSG>
    </DOC>
    """
    assert normalize_xml(expected_xml) == normalize_xml(xml)


def test_ltr0006_from_xml() -> None:
    xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/LTR/LTR0006.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>31680151250908000000001</NUOp>
        </BCMSG>
        <SISMSG>
            <LTR0006>
                <CodMsg>LTR0006</CodMsg>
                <NumCtrlIF_LTR>123</NumCtrlIF_LTR>
                <ISPBIF_LTRDebtd>31680151</ISPBIF_LTRDebtd>
                <ISPBIF_LTRCredtd>31680152</ISPBIF_LTRCredtd>
                <NumCtrlLTROr>321</NumCtrlLTROr>
                <VlrLanc>123.0</VlrLanc>
                <Hist>Test description</Hist>
                <DtMovto>2025-12-04</DtMovto>
            </LTR0006>
        </SISMSG>
    </DOC>
    """

    ltr0006 = LTR0006.from_xml(xml)

    assert isinstance(ltr0006, LTR0006)
    assert ltr0006.from_ispb == '31680151'
    assert ltr0006.to_ispb == '00038166'
    assert ltr0006.system_domain == 'SPB01'
    assert ltr0006.operation_number == '31680151250908000000001'
    assert ltr0006.message_code == 'LTR0006'
    assert ltr0006.institution_or_ltr_control_number == '123'
    assert ltr0006.debtor_institution_or_ltr_ispb == '31680151'
    assert ltr0006.creditor_institution_or_ltr_ispb == '31680152'
    assert ltr0006.original_ltr_control_number == '321'
    assert ltr0006.amount == Decimal('123.0')
    assert ltr0006.description == 'Test description'
    assert ltr0006.settlement_date == date(2025, 12, 4)


def test_ltr0006r1_from_xml() -> None:
    xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/LTR/LTR0006.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>31680151250908000000001</NUOp>
        </BCMSG>
        <SISMSG>
            <LTR0006R1>
                <CodMsg>LTR0006R1</CodMsg>
                <NumCtrlIF_LTR>123</NumCtrlIF_LTR>
                <ISPBIF_LTRDebtd>31680151</ISPBIF_LTRDebtd>
                <NumCtrlSTR>STR20250101000000001</NumCtrlSTR>
                <SitLancSTR>1</SitLancSTR>
                <DtHrSit>2025-12-04 13:21:00+00:00</DtHrSit>
                <DtMovto>2025-12-04</DtMovto>
            </LTR0006R1>
        </SISMSG>
    </DOC>
    """

    ltr0006r1 = LTR0006R1.from_xml(xml)

    assert isinstance(ltr0006r1, LTR0006R1)
    assert ltr0006r1.from_ispb == '31680151'
    assert ltr0006r1.to_ispb == '00038166'
    assert ltr0006r1.system_domain == 'SPB01'
    assert ltr0006r1.operation_number == '31680151250908000000001'
    assert ltr0006r1.message_code == 'LTR0006R1'
    assert ltr0006r1.institution_or_ltr_control_number == '123'
    assert ltr0006r1.debtor_institution_or_ltr_ispb == '31680151'
    assert ltr0006r1.str_control_number == 'STR20250101000000001'
    assert ltr0006r1.str_settlement_status == StrSettlementStatus.EFFECTIVE
    assert ltr0006r1.settlement_timestamp == datetime(2025, 12, 4, 13, 21, tzinfo=UTC)
    assert ltr0006r1.settlement_date == date(2025, 12, 4)


def test_ltr0006r2_from_xml() -> None:
    xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/LTR/LTR0006.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>31680151250908000000001</NUOp>
        </BCMSG>
        <SISMSG>
            <LTR0006R2>
                <CodMsg>LTR0006R2</CodMsg>
                <NumCtrlSTR>STR20250101000000001</NumCtrlSTR>
                <ISPBIF_LTRDebtd>31680151</ISPBIF_LTRDebtd>
                <ISPBIF_LTRCredtd>31680152</ISPBIF_LTRCredtd>
                <VlrLanc>123.0</VlrLanc>
                <NumCtrlSTROr>STR20250101000000001</NumCtrlSTROr>
                <Hist>Test description</Hist>
                <DtHrBC>2025-12-04 13:22:00+00:00</DtHrBC>
                <DtMovto>2025-12-04</DtMovto>
            </LTR0006R2>
        </SISMSG>
    </DOC>
    """

    ltr0006r2 = LTR0006R2.from_xml(xml)

    assert isinstance(ltr0006r2, LTR0006R2)
    assert ltr0006r2.from_ispb == '31680151'
    assert ltr0006r2.to_ispb == '00038166'
    assert ltr0006r2.system_domain == 'SPB01'
    assert ltr0006r2.operation_number == '31680151250908000000001'
    assert ltr0006r2.message_code == 'LTR0006R2'
    assert ltr0006r2.str_control_number == 'STR20250101000000001'
    assert ltr0006r2.debtor_institution_or_ltr_ispb == '31680151'
    assert ltr0006r2.creditor_institution_or_ltr_ispb == '31680152'
    assert ltr0006r2.amount == Decimal('123.0')
    assert ltr0006r2.original_str_control_number == 'STR20250101000000001'
    assert ltr0006r2.description == 'Test description'
    assert ltr0006r2.vendor_timestamp == datetime(2025, 12, 4, 13, 22, tzinfo=UTC)
    assert ltr0006r2.settlement_date == date(2025, 12, 4)


def test_ltr0006e_general_error_from_xml() -> None:
    xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/LTR/LTR0006E.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>31680151250908000000001</NUOp>
        </BCMSG>
        <SISMSG>
            <LTR0006E CodErro="EGEN0050">
                <CodMsg>LTR0006</CodMsg>
                <NumCtrlIF_LTR>123</NumCtrlIF_LTR>
                <ISPBIF_LTRDebtd>31680151</ISPBIF_LTRDebtd>
                <ISPBIF_LTRCredtd>31680152</ISPBIF_LTRCredtd>
                <NumCtrlLTROr>321</NumCtrlLTROr>
                <VlrLanc>123.0</VlrLanc>
                <Hist>Test description</Hist>
                <DtMovto>2025-12-04</DtMovto>
            </LTR0006E>
        </SISMSG>
    </DOC>
    """

    ltr0006e = LTR0006E.from_xml(xml)

    assert isinstance(ltr0006e, LTR0006E)
    assert ltr0006e.from_ispb == '31680151'
    assert ltr0006e.to_ispb == '00038166'
    assert ltr0006e.system_domain == 'SPB01'
    assert ltr0006e.operation_number == '31680151250908000000001'
    assert ltr0006e.message_code == 'LTR0006'
    assert ltr0006e.institution_or_ltr_control_number == '123'
    assert ltr0006e.debtor_institution_or_ltr_ispb == '31680151'
    assert ltr0006e.creditor_institution_or_ltr_ispb == '31680152'
    assert ltr0006e.original_ltr_control_number == '321'
    assert ltr0006e.amount == Decimal('123.0')
    assert ltr0006e.description == 'Test description'
    assert ltr0006e.settlement_date == date(2025, 12, 4)

    assert ltr0006e.general_error_code == 'EGEN0050'


def test_ltr0006e_tag_error_from_xml() -> None:
    xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/LTR/LTR0006E.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>31680151250908000000001</NUOp>
        </BCMSG>
        <SISMSG>
            <LTR0006E>
                <CodMsg>LTR0006</CodMsg>
                <NumCtrlIF_LTR>123</NumCtrlIF_LTR>
                <ISPBIF_LTRDebtd>31680151</ISPBIF_LTRDebtd>
                <ISPBIF_LTRCredtd>31680152</ISPBIF_LTRCredtd>
                <NumCtrlLTROr CodErro="EGEN0051">321</NumCtrlLTROr>
                <VlrLanc>123.0</VlrLanc>
                <Hist>Test description</Hist>
                <DtMovto>2025-12-04</DtMovto>
            </LTR0006E>
        </SISMSG>
    </DOC>
    """

    ltr0006e = LTR0006E.from_xml(xml)

    assert isinstance(ltr0006e, LTR0006E)
    assert ltr0006e.from_ispb == '31680151'
    assert ltr0006e.to_ispb == '00038166'
    assert ltr0006e.system_domain == 'SPB01'
    assert ltr0006e.operation_number == '31680151250908000000001'
    assert ltr0006e.message_code == 'LTR0006'
    assert ltr0006e.institution_or_ltr_control_number == '123'
    assert ltr0006e.debtor_institution_or_ltr_ispb == '31680151'
    assert ltr0006e.creditor_institution_or_ltr_ispb == '31680152'
    assert ltr0006e.original_ltr_control_number == '321'
    assert ltr0006e.amount == Decimal('123.0')
    assert ltr0006e.description == 'Test description'
    assert ltr0006e.settlement_date == date(2025, 12, 4)

    assert ltr0006e.original_ltr_control_number_error_code == 'EGEN0051'


def test_ltr0006_roundtrip() -> None:
    params = make_valid_ltr0006_params()

    ltr0006 = LTR0006.model_validate(params)
    xml = ltr0006.to_xml()
    ltr0006_from_xml = LTR0006.from_xml(xml)

    assert ltr0006 == ltr0006_from_xml


def test_ltr0006r1_roundtrip() -> None:
    params = make_valid_ltr0006r1_params()

    ltr0006r1 = LTR0006R1.model_validate(params)
    xml = ltr0006r1.to_xml()
    ltr0006r1_from_xml = LTR0006R1.from_xml(xml)

    assert ltr0006r1 == ltr0006r1_from_xml


def test_ltr0006r2_roundtrip() -> None:
    params = make_valid_ltr0006r2_params()

    ltr0006r2 = LTR0006R2.model_validate(params)
    xml = ltr0006r2.to_xml()
    ltr0006r2_from_xml = LTR0006R2.from_xml(xml)

    assert ltr0006r2 == ltr0006r2_from_xml
