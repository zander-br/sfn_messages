from datetime import date, datetime
from decimal import Decimal
from typing import Any

import pytest
from pydantic import ValidationError

from sfn_messages.core.types import MovementType, PaymentType, ProductCode, StrSettlementStatus
from sfn_messages.ldl.ldl0006 import (
    LDL0006,
    LDL0006E,
    LDL0006R1,
    LDL0006R2,
    CreditRefundGroup,
    CreditRefundGroupError,
    CreditRefundGroupR2,
)
from tests.conftest import extract_missing_fields, normalize_xml

CREDIT_REFUND_SIZE = 2


def make_valid_ldl0006_params() -> dict[str, Any]:
    return {
        'from_ispb': '31680151',
        'to_ispb': '00038166',
        'system_domain': 'SPB01',
        'operation_number': '31680151250908000000001',
        'message_code': 'LDL0006',
        'institution_or_ldl_control_number': '123',
        'debitor_institution_ispb': '31680151',
        'creditor_institution_ispb': '31680153',
        'product_code': 'AMEX_CREDIT_CARD',
        'original_str_control_number': 'STR20250101000000001',
        'amount': 120.0,
        'credit_refund_group': [
            {
                'cnpj': '50214141000185',
                'participant_identifier': '55386424',
                'amount': 100.0,
                'payment_type_ldl': 'DIVIDENDS',
                'movement_type': 'DEPOSIT_OF_ASSET',
                'payment_number': '213',
                'description': 'Refund for overpayment',
            },
            {
                'cnpj': '53753940000118',
                'participant_identifier': '43075534',
                'amount': 20.0,
                'payment_type_ldl': 'DIVIDENDS',
                'movement_type': 'DEPOSIT_OF_ASSET',
                'payment_number': '312',
                'description': 'Refund for overpayment',
            },
        ],
        'settlement_date': '2025-12-09',
    }


def make_valid_ldl0006r1_params() -> dict[str, Any]:
    return {
        'from_ispb': '31680151',
        'to_ispb': '00038166',
        'system_domain': 'SPB01',
        'operation_number': '31680151250908000000001',
        'message_code': 'LDL0006R1',
        'institution_or_ldl_control_number': '123',
        'debitor_institution_ispb': '31680151',
        'str_control_number': 'STR20250101000000001',
        'str_settlement_status': 'EFFECTIVE',
        'settlement_timestamp': '2025-12-09T09:00:00',
        'settlement_date': '2025-12-09',
    }


def make_valid_ldl0006r2_params() -> dict[str, Any]:
    return {
        'from_ispb': '31680151',
        'to_ispb': '00038166',
        'system_domain': 'SPB01',
        'operation_number': '31680151250908000000001',
        'message_code': 'LDL0006R2',
        'str_control_number': 'STR20250101000000001',
        'vendor_timestamp': '2025-12-09T09:00:00',
        'debitor_institution_ispb': '31680151',
        'creditor_institution_ispb': '31680153',
        'product_code': 'AMEX_CREDIT_CARD',
        'amount': 120.0,
        'original_str_control_number': 'STR20250101000000001',
        'credit_refund_group': [
            {
                'cnpj': '50214141000185',
                'participant_identifier': '55386424',
                'amount': 100.0,
                'payment_type_ldl': 'DIVIDENDS',
                'movement_type': 'DEPOSIT_OF_ASSET',
                'payment_number': '213',
                'description': 'Refund for overpayment',
            },
            {
                'cnpj': '53753940000118',
                'participant_identifier': '43075534',
                'amount': 20.0,
                'payment_type_ldl': 'DIVIDENDS',
                'movement_type': 'DEPOSIT_OF_ASSET',
                'payment_number': '312',
                'description': 'Refund for overpayment',
            },
        ],
        'settlement_date': '2025-12-09',
    }


def make_valid_ldl0006e_params(*, general_error: bool = False) -> dict[str, Any]:
    ldl0006e = {
        'from_ispb': '31680151',
        'to_ispb': '00038166',
        'system_domain': 'SPB01',
        'operation_number': '31680151250908000000001',
        'message_code': 'LDL0006E',
        'institution_or_ldl_control_number': '123',
        'debitor_institution_ispb': '31680151',
        'creditor_institution_ispb': '31680153',
        'product_code': 'AMEX_CREDIT_CARD',
        'original_str_control_number': 'STR20250101000000001',
        'amount': 120.0,
        'credit_refund_group': [
            {
                'cnpj': '50214141000185',
                'participant_identifier': '55386424',
                'amount': 100.0,
                'payment_type_ldl': 'DIVIDENDS',
                'movement_type': 'DEPOSIT_OF_ASSET',
                'payment_number': '213',
                'description': 'Refund for overpayment',
            },
            {
                'cnpj': '53753940000118',
                'participant_identifier': '43075534',
                'amount': 20.0,
                'payment_type_ldl': 'DIVIDENDS',
                'movement_type': 'DEPOSIT_OF_ASSET',
                'payment_number': '312',
                'description': 'Refund for overpayment',
            },
        ],
        'settlement_date': '2025-12-09',
    }

    if general_error:
        ldl0006e['general_error_code'] = 'EGEN0050'
    else:
        ldl0006e['creditor_institution_ispb_error_code'] = 'ELDL0123'

    return ldl0006e


def test_ldl0006_valid_model() -> None:
    params = make_valid_ldl0006_params()
    ldl0006 = LDL0006.model_validate(params)

    assert isinstance(ldl0006, LDL0006)
    assert ldl0006.from_ispb == '31680151'
    assert ldl0006.to_ispb == '00038166'
    assert ldl0006.system_domain == 'SPB01'
    assert ldl0006.operation_number == '31680151250908000000001'
    assert ldl0006.message_code == 'LDL0006'
    assert ldl0006.institution_or_ldl_control_number == '123'
    assert ldl0006.debitor_institution_ispb == '31680151'
    assert ldl0006.creditor_institution_ispb == '31680153'
    assert ldl0006.product_code == ProductCode.AMEX_CREDIT_CARD
    assert ldl0006.original_str_control_number == 'STR20250101000000001'
    assert ldl0006.amount == Decimal('120.0')
    assert ldl0006.settlement_date == date(2025, 12, 9)

    assert len(ldl0006.credit_refund_group) == CREDIT_REFUND_SIZE
    credit1 = ldl0006.credit_refund_group[0]
    credit2 = ldl0006.credit_refund_group[1]
    assert isinstance(credit1, CreditRefundGroup)
    assert credit1.cnpj == '50214141000185'
    assert credit1.participant_identifier == '55386424'
    assert credit1.amount == Decimal('100.0')
    assert credit1.payment_type_ldl == PaymentType.DIVIDENDS
    assert credit1.movement_type == MovementType.DEPOSIT_OF_ASSET
    assert credit1.payment_number == '213'
    assert credit1.description == 'Refund for overpayment'

    assert isinstance(credit2, CreditRefundGroup)
    assert credit2.cnpj == '53753940000118'
    assert credit2.participant_identifier == '43075534'
    assert credit2.amount == Decimal('20.0')
    assert credit2.payment_type_ldl == PaymentType.DIVIDENDS
    assert credit2.movement_type == MovementType.DEPOSIT_OF_ASSET
    assert credit2.payment_number == '312'
    assert credit2.description == 'Refund for overpayment'


def test_ldl0006r1_valid_model() -> None:
    params = make_valid_ldl0006r1_params()
    ldl0006r1 = LDL0006R1.model_validate(params)

    assert isinstance(ldl0006r1, LDL0006R1)
    assert ldl0006r1.from_ispb == '31680151'
    assert ldl0006r1.to_ispb == '00038166'
    assert ldl0006r1.system_domain == 'SPB01'
    assert ldl0006r1.operation_number == '31680151250908000000001'
    assert ldl0006r1.message_code == 'LDL0006R1'
    assert ldl0006r1.institution_or_ldl_control_number == '123'
    assert ldl0006r1.debitor_institution_ispb == '31680151'
    assert ldl0006r1.str_control_number == 'STR20250101000000001'
    assert ldl0006r1.str_settlement_status == StrSettlementStatus.EFFECTIVE
    assert ldl0006r1.settlement_timestamp == datetime(2025, 12, 9, 9, 0)
    assert ldl0006r1.settlement_date == date(2025, 12, 9)


def test_ldl0006r2_valid_model() -> None:
    params = make_valid_ldl0006r2_params()
    ldl0006r2 = LDL0006R2.model_validate(params)

    assert isinstance(ldl0006r2, LDL0006R2)
    assert ldl0006r2.from_ispb == '31680151'
    assert ldl0006r2.to_ispb == '00038166'
    assert ldl0006r2.system_domain == 'SPB01'
    assert ldl0006r2.operation_number == '31680151250908000000001'
    assert ldl0006r2.message_code == 'LDL0006R2'
    assert ldl0006r2.str_control_number == 'STR20250101000000001'
    assert ldl0006r2.vendor_timestamp == datetime(2025, 12, 9, 9, 0)
    assert ldl0006r2.debitor_institution_ispb == '31680151'
    assert ldl0006r2.creditor_institution_ispb == '31680153'
    assert ldl0006r2.product_code == ProductCode.AMEX_CREDIT_CARD
    assert ldl0006r2.amount == Decimal('120.0')
    assert ldl0006r2.original_str_control_number == 'STR20250101000000001'

    assert len(ldl0006r2.credit_refund_group) == CREDIT_REFUND_SIZE
    credit1 = ldl0006r2.credit_refund_group[0]
    credit2 = ldl0006r2.credit_refund_group[1]
    assert isinstance(credit1, CreditRefundGroupR2)
    assert credit1.cnpj == '50214141000185'
    assert credit1.participant_identifier == '55386424'
    assert credit1.amount == Decimal('100.0')
    assert credit1.payment_type_ldl == PaymentType.DIVIDENDS
    assert credit1.movement_type == MovementType.DEPOSIT_OF_ASSET
    assert credit1.payment_number == '213'
    assert credit1.description == 'Refund for overpayment'

    assert isinstance(credit2, CreditRefundGroupR2)
    assert credit2.cnpj == '53753940000118'
    assert credit2.participant_identifier == '43075534'
    assert credit2.amount == Decimal('20.0')
    assert credit2.payment_type_ldl == PaymentType.DIVIDENDS
    assert credit2.movement_type == MovementType.DEPOSIT_OF_ASSET
    assert credit2.payment_number == '312'
    assert credit2.description == 'Refund for overpayment'


def test_ldl0006e_valid_model() -> None:
    params = make_valid_ldl0006e_params()
    ldl0006e = LDL0006E.model_validate(params)

    assert isinstance(ldl0006e, LDL0006E)
    assert ldl0006e.from_ispb == '31680151'
    assert ldl0006e.to_ispb == '00038166'
    assert ldl0006e.system_domain == 'SPB01'
    assert ldl0006e.operation_number == '31680151250908000000001'
    assert ldl0006e.message_code == 'LDL0006E'
    assert ldl0006e.institution_or_ldl_control_number == '123'
    assert ldl0006e.debitor_institution_ispb == '31680151'
    assert ldl0006e.creditor_institution_ispb == '31680153'
    assert ldl0006e.product_code == ProductCode.AMEX_CREDIT_CARD
    assert ldl0006e.original_str_control_number == 'STR20250101000000001'
    assert ldl0006e.amount == Decimal('120.0')
    assert ldl0006e.settlement_date == date(2025, 12, 9)

    assert len(ldl0006e.credit_refund_group) == CREDIT_REFUND_SIZE
    credit1 = ldl0006e.credit_refund_group[0]
    credit2 = ldl0006e.credit_refund_group[1]
    assert isinstance(credit1, CreditRefundGroupError)
    assert credit1.cnpj == '50214141000185'
    assert credit1.participant_identifier == '55386424'
    assert credit1.amount == Decimal('100.0')
    assert credit1.payment_type_ldl == PaymentType.DIVIDENDS
    assert credit1.movement_type == MovementType.DEPOSIT_OF_ASSET
    assert credit1.payment_number == '213'
    assert credit1.description == 'Refund for overpayment'

    assert isinstance(credit2, CreditRefundGroupError)
    assert credit2.cnpj == '53753940000118'
    assert credit2.participant_identifier == '43075534'
    assert credit2.amount == Decimal('20.0')
    assert credit2.payment_type_ldl == PaymentType.DIVIDENDS
    assert credit2.movement_type == MovementType.DEPOSIT_OF_ASSET
    assert credit2.payment_number == '312'
    assert credit2.description == 'Refund for overpayment'

    assert ldl0006e.creditor_institution_ispb_error_code == 'ELDL0123'


def test_ldl0006_missing_required_fields() -> None:
    with pytest.raises(ValidationError) as exc:
        LDL0006.model_validate({})

    missing_fields = extract_missing_fields(exc.value)
    assert missing_fields == {
        'from_ispb',
        'to_ispb',
        'system_domain',
        'operation_number',
        'institution_or_ldl_control_number',
        'debitor_institution_ispb',
        'creditor_institution_ispb',
        'original_str_control_number',
        'amount',
        'settlement_date',
    }


def test_ldl0006r1_missing_required_fields() -> None:
    with pytest.raises(ValidationError) as exc:
        LDL0006R1.model_validate({})

    missing_fields = extract_missing_fields(exc.value)
    assert missing_fields == {
        'from_ispb',
        'to_ispb',
        'system_domain',
        'operation_number',
        'institution_or_ldl_control_number',
        'debitor_institution_ispb',
        'str_control_number',
        'str_settlement_status',
        'settlement_timestamp',
        'settlement_date',
    }


def test_ldl0006r2_missing_required_fields() -> None:
    with pytest.raises(ValidationError) as exc:
        LDL0006R2.model_validate({})

    missing_fields = extract_missing_fields(exc.value)
    assert missing_fields == {
        'from_ispb',
        'to_ispb',
        'system_domain',
        'operation_number',
        'str_control_number',
        'vendor_timestamp',
        'debitor_institution_ispb',
        'creditor_institution_ispb',
        'amount',
        'original_str_control_number',
        'settlement_date',
    }


def test_ldl0006_to_xml() -> None:
    params = make_valid_ldl0006_params()
    ldl0006 = LDL0006.model_validate(params)

    xml = ldl0006.to_xml()

    expected_xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/SPB/LDL0006.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>31680151250908000000001</NUOp>
        </BCMSG>
        <SISMSG>
            <LDL0006>
                <CodMsg>LDL0006</CodMsg>
                <NumCtrlIF_LDL>123</NumCtrlIF_LDL>
                <ISPBIF_LDLDebtd>31680151</ISPBIF_LDLDebtd>
                <ISPBIF_LDLCredtd>31680153</ISPBIF_LDLCredtd>
                <CodProdt>ACC</CodProdt>
                <NumCtrlSTROr>STR20250101000000001</NumCtrlSTROr>
                <VlrLanc>120.0</VlrLanc>
                <Grupo_LDL0006_DevCred>
                    <CNPJNLiqdant>50214141000185</CNPJNLiqdant>
                    <IdentdPartCamr>55386424</IdentdPartCamr>
                    <VlrNLiqdant>100.0</VlrNLiqdant>
                    <TpPgtoLDL>2</TpPgtoLDL>
                    <TpMovtc>1</TpMovtc>
                    <NumPgtoLDL>213</NumPgtoLDL>
                    <Hist>Refund for overpayment</Hist>
                </Grupo_LDL0006_DevCred>
                <Grupo_LDL0006_DevCred>
                    <CNPJNLiqdant>53753940000118</CNPJNLiqdant>
                    <IdentdPartCamr>43075534</IdentdPartCamr>
                    <VlrNLiqdant>20.0</VlrNLiqdant>
                    <TpPgtoLDL>2</TpPgtoLDL>
                    <TpMovtc>1</TpMovtc>
                    <NumPgtoLDL>312</NumPgtoLDL>
                    <Hist>Refund for overpayment</Hist>
                </Grupo_LDL0006_DevCred>
                <DtMovto>2025-12-09</DtMovto>
            </LDL0006>
        </SISMSG>
    </DOC>
    """
    assert normalize_xml(expected_xml) == normalize_xml(xml)


def test_ldl0006r1_to_xml() -> None:
    params = make_valid_ldl0006r1_params()
    ldl0006r1 = LDL0006R1.model_validate(params)

    xml = ldl0006r1.to_xml()

    expected_xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/SPB/LDL0006.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>31680151250908000000001</NUOp>
        </BCMSG>
        <SISMSG>
            <LDL0006R1>
                <CodMsg>LDL0006R1</CodMsg>
                <NumCtrlIF_LDL>123</NumCtrlIF_LDL>
                <ISPBIF_LDLDebtd>31680151</ISPBIF_LDLDebtd>
                <NumCtrlSTR>STR20250101000000001</NumCtrlSTR>
                <SitLancSTR>1</SitLancSTR>
                <DtHrSit>2025-12-09T09:00:00</DtHrSit>
                <DtMovto>2025-12-09</DtMovto>
            </LDL0006R1>
        </SISMSG>
    </DOC>
    """
    assert normalize_xml(expected_xml) == normalize_xml(xml)


def test_ldl0006r2_to_xml() -> None:
    params = make_valid_ldl0006r2_params()
    ldl0006r2 = LDL0006R2.model_validate(params)

    xml = ldl0006r2.to_xml()

    expected_xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/SPB/LDL0006.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>31680151250908000000001</NUOp>
        </BCMSG>
        <SISMSG>
            <LDL0006R2>
                <CodMsg>LDL0006R2</CodMsg>
                <NumCtrlSTR>STR20250101000000001</NumCtrlSTR>
                <DtHrBC>2025-12-09T09:00:00</DtHrBC>
                <ISPBIF_LDLDebtd>31680151</ISPBIF_LDLDebtd>
                <ISPBIF_LDLCredtd>31680153</ISPBIF_LDLCredtd>
                <CodProdt>ACC</CodProdt>
                <VlrLanc>120.0</VlrLanc>
                <NumCtrlSTROr>STR20250101000000001</NumCtrlSTROr>
                <Grupo_LDL0006R2_DevCred>
                    <CNPJNLiqdant>50214141000185</CNPJNLiqdant>
                    <IdentdPartCamr>55386424</IdentdPartCamr>
                    <VlrNLiqdant>100.0</VlrNLiqdant>
                    <TpPgtoLDL>2</TpPgtoLDL>
                    <TpMovtc>1</TpMovtc>
                    <NumPgtoLDL>213</NumPgtoLDL>
                    <Hist>Refund for overpayment</Hist>
                </Grupo_LDL0006R2_DevCred>
                <Grupo_LDL0006R2_DevCred>
                    <CNPJNLiqdant>53753940000118</CNPJNLiqdant>
                    <IdentdPartCamr>43075534</IdentdPartCamr>
                    <VlrNLiqdant>20.0</VlrNLiqdant>
                    <TpPgtoLDL>2</TpPgtoLDL>
                    <TpMovtc>1</TpMovtc>
                    <NumPgtoLDL>312</NumPgtoLDL>
                    <Hist>Refund for overpayment</Hist>
                </Grupo_LDL0006R2_DevCred>
                <DtMovto>2025-12-09</DtMovto>
            </LDL0006R2>
        </SISMSG>
    </DOC>
    """
    assert normalize_xml(expected_xml) == normalize_xml(xml)


def test_ldl0006e_general_error_to_xml() -> None:
    params = make_valid_ldl0006e_params(general_error=True)
    ldl0006e = LDL0006E.model_validate(params)

    xml = ldl0006e.to_xml()

    expected_xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/SPB/LDL0006E.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>31680151250908000000001</NUOp>
        </BCMSG>
        <SISMSG>
            <LDL0006 CodErro="EGEN0050">
                <CodMsg>LDL0006E</CodMsg>
                <NumCtrlIF_LDL>123</NumCtrlIF_LDL>
                <ISPBIF_LDLDebtd>31680151</ISPBIF_LDLDebtd>
                <ISPBIF_LDLCredtd>31680153</ISPBIF_LDLCredtd>
                <CodProdt>ACC</CodProdt>
                <NumCtrlSTROr>STR20250101000000001</NumCtrlSTROr>
                <VlrLanc>120.0</VlrLanc>
                <Grupo_LDL0006_DevCred>
                    <CNPJNLiqdant>50214141000185</CNPJNLiqdant>
                    <IdentdPartCamr>55386424</IdentdPartCamr>
                    <VlrNLiqdant>100.0</VlrNLiqdant>
                    <TpPgtoLDL>2</TpPgtoLDL>
                    <TpMovtc>1</TpMovtc>
                    <NumPgtoLDL>213</NumPgtoLDL>
                    <Hist>Refund for overpayment</Hist>
                </Grupo_LDL0006_DevCred>
                <Grupo_LDL0006_DevCred>
                    <CNPJNLiqdant>53753940000118</CNPJNLiqdant>
                    <IdentdPartCamr>43075534</IdentdPartCamr>
                    <VlrNLiqdant>20.0</VlrNLiqdant>
                    <TpPgtoLDL>2</TpPgtoLDL>
                    <TpMovtc>1</TpMovtc>
                    <NumPgtoLDL>312</NumPgtoLDL>
                    <Hist>Refund for overpayment</Hist>
                </Grupo_LDL0006_DevCred>
                <DtMovto>2025-12-09</DtMovto>
            </LDL0006>
        </SISMSG>
    </DOC>
    """
    assert normalize_xml(expected_xml) == normalize_xml(xml)


def test_ldl0006e_tag_error_to_xml() -> None:
    params = make_valid_ldl0006e_params()
    ldl0006e = LDL0006E.model_validate(params)

    xml = ldl0006e.to_xml()

    expected_xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/SPB/LDL0006E.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>31680151250908000000001</NUOp>
        </BCMSG>
        <SISMSG>
            <LDL0006>
                <CodMsg>LDL0006E</CodMsg>
                <NumCtrlIF_LDL>123</NumCtrlIF_LDL>
                <ISPBIF_LDLDebtd>31680151</ISPBIF_LDLDebtd>
                <ISPBIF_LDLCredtd CodErro="ELDL0123">31680153</ISPBIF_LDLCredtd>
                <CodProdt>ACC</CodProdt>
                <NumCtrlSTROr>STR20250101000000001</NumCtrlSTROr>
                <VlrLanc>120.0</VlrLanc>
                <Grupo_LDL0006_DevCred>
                    <CNPJNLiqdant>50214141000185</CNPJNLiqdant>
                    <IdentdPartCamr>55386424</IdentdPartCamr>
                    <VlrNLiqdant>100.0</VlrNLiqdant>
                    <TpPgtoLDL>2</TpPgtoLDL>
                    <TpMovtc>1</TpMovtc>
                    <NumPgtoLDL>213</NumPgtoLDL>
                    <Hist>Refund for overpayment</Hist>
                </Grupo_LDL0006_DevCred>
                <Grupo_LDL0006_DevCred>
                    <CNPJNLiqdant>53753940000118</CNPJNLiqdant>
                    <IdentdPartCamr>43075534</IdentdPartCamr>
                    <VlrNLiqdant>20.0</VlrNLiqdant>
                    <TpPgtoLDL>2</TpPgtoLDL>
                    <TpMovtc>1</TpMovtc>
                    <NumPgtoLDL>312</NumPgtoLDL>
                    <Hist>Refund for overpayment</Hist>
                </Grupo_LDL0006_DevCred>
                <DtMovto>2025-12-09</DtMovto>
            </LDL0006>
        </SISMSG>
    </DOC>
    """
    assert normalize_xml(expected_xml) == normalize_xml(xml)


def test_ldl0006_from_xml() -> None:
    xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/SPB/LDL0006.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>31680151250908000000001</NUOp>
        </BCMSG>
        <SISMSG>
            <LDL0006>
                <CodMsg>LDL0006</CodMsg>
                <NumCtrlIF_LDL>123</NumCtrlIF_LDL>
                <ISPBIF_LDLDebtd>31680151</ISPBIF_LDLDebtd>
                <ISPBIF_LDLCredtd>31680153</ISPBIF_LDLCredtd>
                <CodProdt>ACC</CodProdt>
                <NumCtrlSTROr>STR20250101000000001</NumCtrlSTROr>
                <VlrLanc>120.0</VlrLanc>
                <Grupo_LDL0006_DevCred>
                    <CNPJNLiqdant>50214141000185</CNPJNLiqdant>
                    <IdentdPartCamr>55386424</IdentdPartCamr>
                    <VlrNLiqdant>100.0</VlrNLiqdant>
                    <TpPgtoLDL>2</TpPgtoLDL>
                    <TpMovtc>1</TpMovtc>
                    <NumPgtoLDL>213</NumPgtoLDL>
                    <Hist>Refund for overpayment</Hist>
                </Grupo_LDL0006_DevCred>
                <Grupo_LDL0006_DevCred>
                    <CNPJNLiqdant>53753940000118</CNPJNLiqdant>
                    <IdentdPartCamr>43075534</IdentdPartCamr>
                    <VlrNLiqdant>20.0</VlrNLiqdant>
                    <TpPgtoLDL>2</TpPgtoLDL>
                    <TpMovtc>1</TpMovtc>
                    <NumPgtoLDL>312</NumPgtoLDL>
                    <Hist>Refund for overpayment</Hist>
                </Grupo_LDL0006_DevCred>
                <DtMovto>2025-12-09</DtMovto>
            </LDL0006>
        </SISMSG>
    </DOC>
    """

    ldl0006 = LDL0006.from_xml(xml)

    assert isinstance(ldl0006, LDL0006)
    assert ldl0006.from_ispb == '31680151'
    assert ldl0006.to_ispb == '00038166'
    assert ldl0006.system_domain == 'SPB01'
    assert ldl0006.operation_number == '31680151250908000000001'
    assert ldl0006.message_code == 'LDL0006'
    assert ldl0006.institution_or_ldl_control_number == '123'
    assert ldl0006.debitor_institution_ispb == '31680151'
    assert ldl0006.creditor_institution_ispb == '31680153'
    assert ldl0006.product_code == ProductCode.AMEX_CREDIT_CARD
    assert ldl0006.original_str_control_number == 'STR20250101000000001'
    assert ldl0006.amount == Decimal('120.0')
    assert ldl0006.settlement_date == date(2025, 12, 9)

    assert len(ldl0006.credit_refund_group) == CREDIT_REFUND_SIZE
    credit1 = ldl0006.credit_refund_group[0]
    credit2 = ldl0006.credit_refund_group[1]
    assert isinstance(credit1, CreditRefundGroup)
    assert credit1.cnpj == '50214141000185'
    assert credit1.participant_identifier == '55386424'
    assert credit1.amount == Decimal('100.0')
    assert credit1.payment_type_ldl == PaymentType.DIVIDENDS
    assert credit1.movement_type == MovementType.DEPOSIT_OF_ASSET
    assert credit1.payment_number == '213'
    assert credit1.description == 'Refund for overpayment'

    assert isinstance(credit2, CreditRefundGroup)
    assert credit2.cnpj == '53753940000118'
    assert credit2.participant_identifier == '43075534'
    assert credit2.amount == Decimal('20.0')
    assert credit2.payment_type_ldl == PaymentType.DIVIDENDS
    assert credit2.movement_type == MovementType.DEPOSIT_OF_ASSET
    assert credit2.payment_number == '312'
    assert credit2.description == 'Refund for overpayment'


def test_ldl0006r1_from_xml() -> None:
    xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/SPB/LDL0006.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>31680151250908000000001</NUOp>
        </BCMSG>
        <SISMSG>
            <LDL0006R1>
                <CodMsg>LDL0006R1</CodMsg>
                <NumCtrlIF_LDL>123</NumCtrlIF_LDL>
                <ISPBIF_LDLDebtd>31680151</ISPBIF_LDLDebtd>
                <NumCtrlSTR>STR20250101000000001</NumCtrlSTR>
                <SitLancSTR>1</SitLancSTR>
                <DtHrSit>2025-12-09T09:00:00</DtHrSit>
                <DtMovto>2025-12-09</DtMovto>
            </LDL0006R1>
        </SISMSG>
    </DOC>
    """

    ldl0006r1 = LDL0006R1.from_xml(xml)

    assert isinstance(ldl0006r1, LDL0006R1)
    assert ldl0006r1.from_ispb == '31680151'
    assert ldl0006r1.to_ispb == '00038166'
    assert ldl0006r1.system_domain == 'SPB01'
    assert ldl0006r1.operation_number == '31680151250908000000001'
    assert ldl0006r1.message_code == 'LDL0006R1'
    assert ldl0006r1.institution_or_ldl_control_number == '123'
    assert ldl0006r1.debitor_institution_ispb == '31680151'
    assert ldl0006r1.str_control_number == 'STR20250101000000001'
    assert ldl0006r1.str_settlement_status == StrSettlementStatus.EFFECTIVE
    assert ldl0006r1.settlement_timestamp == datetime(2025, 12, 9, 9, 0)
    assert ldl0006r1.settlement_date == date(2025, 12, 9)


def test_ldl0006r2_from_xml() -> None:
    xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/SPB/LDL0006.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>31680151250908000000001</NUOp>
        </BCMSG>
        <SISMSG>
            <LDL0006R2>
                <CodMsg>LDL0006R2</CodMsg>
                <NumCtrlSTR>STR20250101000000001</NumCtrlSTR>
                <DtHrBC>2025-12-09T09:00:00</DtHrBC>
                <ISPBIF_LDLDebtd>31680151</ISPBIF_LDLDebtd>
                <ISPBIF_LDLCredtd>31680153</ISPBIF_LDLCredtd>
                <CodProdt>ACC</CodProdt>
                <VlrLanc>120.0</VlrLanc>
                <NumCtrlSTROr>STR20250101000000001</NumCtrlSTROr>
                <Grupo_LDL0006R2_DevCred>
                    <CNPJNLiqdant>50214141000185</CNPJNLiqdant>
                    <IdentdPartCamr>55386424</IdentdPartCamr>
                    <VlrNLiqdant>100.0</VlrNLiqdant>
                    <TpPgtoLDL>2</TpPgtoLDL>
                    <TpMovtc>1</TpMovtc>
                    <NumPgtoLDL>213</NumPgtoLDL>
                    <Hist>Refund for overpayment</Hist>
                </Grupo_LDL0006R2_DevCred>
                <Grupo_LDL0006R2_DevCred>
                    <CNPJNLiqdant>53753940000118</CNPJNLiqdant>
                    <IdentdPartCamr>43075534</IdentdPartCamr>
                    <VlrNLiqdant>20.0</VlrNLiqdant>
                    <TpPgtoLDL>2</TpPgtoLDL>
                    <TpMovtc>1</TpMovtc>
                    <NumPgtoLDL>312</NumPgtoLDL>
                    <Hist>Refund for overpayment</Hist>
                </Grupo_LDL0006R2_DevCred>
                <DtMovto>2025-12-09</DtMovto>
            </LDL0006R2>
        </SISMSG>
    </DOC>
    """

    ldl0006r2 = LDL0006R2.from_xml(xml)

    assert isinstance(ldl0006r2, LDL0006R2)
    assert ldl0006r2.from_ispb == '31680151'
    assert ldl0006r2.to_ispb == '00038166'
    assert ldl0006r2.system_domain == 'SPB01'
    assert ldl0006r2.operation_number == '31680151250908000000001'
    assert ldl0006r2.message_code == 'LDL0006R2'
    assert ldl0006r2.str_control_number == 'STR20250101000000001'
    assert ldl0006r2.vendor_timestamp == datetime(2025, 12, 9, 9, 0)
    assert ldl0006r2.debitor_institution_ispb == '31680151'
    assert ldl0006r2.creditor_institution_ispb == '31680153'
    assert ldl0006r2.product_code == ProductCode.AMEX_CREDIT_CARD
    assert ldl0006r2.amount == Decimal('120.0')
    assert ldl0006r2.original_str_control_number == 'STR20250101000000001'

    assert len(ldl0006r2.credit_refund_group) == CREDIT_REFUND_SIZE
    credit1 = ldl0006r2.credit_refund_group[0]
    credit2 = ldl0006r2.credit_refund_group[1]
    assert isinstance(credit1, CreditRefundGroupR2)
    assert credit1.cnpj == '50214141000185'
    assert credit1.participant_identifier == '55386424'
    assert credit1.amount == Decimal('100.0')
    assert credit1.payment_type_ldl == PaymentType.DIVIDENDS
    assert credit1.movement_type == MovementType.DEPOSIT_OF_ASSET
    assert credit1.payment_number == '213'
    assert credit1.description == 'Refund for overpayment'

    assert isinstance(credit2, CreditRefundGroupR2)
    assert credit2.cnpj == '53753940000118'
    assert credit2.participant_identifier == '43075534'
    assert credit2.amount == Decimal('20.0')
    assert credit2.payment_type_ldl == PaymentType.DIVIDENDS
    assert credit2.movement_type == MovementType.DEPOSIT_OF_ASSET
    assert credit2.payment_number == '312'
    assert credit2.description == 'Refund for overpayment'


def test_ldl0006e_general_error_from_xml() -> None:
    xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/SPB/LDL0006E.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>31680151250908000000001</NUOp>
        </BCMSG>
        <SISMSG>
            <LDL0006 CodErro="EGEN0050">
                <CodMsg>LDL0006E</CodMsg>
                <NumCtrlIF_LDL>123</NumCtrlIF_LDL>
                <ISPBIF_LDLDebtd>31680151</ISPBIF_LDLDebtd>
                <ISPBIF_LDLCredtd>31680153</ISPBIF_LDLCredtd>
                <CodProdt>ACC</CodProdt>
                <NumCtrlSTROr>STR20250101000000001</NumCtrlSTROr>
                <VlrLanc>120.0</VlrLanc>
                <Grupo_LDL0006_DevCred>
                    <CNPJNLiqdant>50214141000185</CNPJNLiqdant>
                    <IdentdPartCamr>55386424</IdentdPartCamr>
                    <VlrNLiqdant>100.0</VlrNLiqdant>
                    <TpPgtoLDL>2</TpPgtoLDL>
                    <TpMovtc>1</TpMovtc>
                    <NumPgtoLDL>213</NumPgtoLDL>
                    <Hist>Refund for overpayment</Hist>
                </Grupo_LDL0006_DevCred>
                <Grupo_LDL0006_DevCred>
                    <CNPJNLiqdant>53753940000118</CNPJNLiqdant>
                    <IdentdPartCamr>43075534</IdentdPartCamr>
                    <VlrNLiqdant>20.0</VlrNLiqdant>
                    <TpPgtoLDL>2</TpPgtoLDL>
                    <TpMovtc>1</TpMovtc>
                    <NumPgtoLDL>312</NumPgtoLDL>
                    <Hist>Refund for overpayment</Hist>
                </Grupo_LDL0006_DevCred>
                <DtMovto>2025-12-09</DtMovto>
            </LDL0006>
        </SISMSG>
    </DOC>
    """

    ldl0006e = LDL0006E.from_xml(xml)

    assert isinstance(ldl0006e, LDL0006E)
    assert ldl0006e.from_ispb == '31680151'
    assert ldl0006e.to_ispb == '00038166'
    assert ldl0006e.system_domain == 'SPB01'
    assert ldl0006e.operation_number == '31680151250908000000001'
    assert ldl0006e.message_code == 'LDL0006E'
    assert ldl0006e.institution_or_ldl_control_number == '123'
    assert ldl0006e.debitor_institution_ispb == '31680151'
    assert ldl0006e.creditor_institution_ispb == '31680153'
    assert ldl0006e.product_code == ProductCode.AMEX_CREDIT_CARD
    assert ldl0006e.original_str_control_number == 'STR20250101000000001'
    assert ldl0006e.amount == Decimal('120.0')
    assert ldl0006e.settlement_date == date(2025, 12, 9)

    assert len(ldl0006e.credit_refund_group) == CREDIT_REFUND_SIZE
    credit1 = ldl0006e.credit_refund_group[0]
    credit2 = ldl0006e.credit_refund_group[1]
    assert isinstance(credit1, CreditRefundGroupError)
    assert credit1.cnpj == '50214141000185'
    assert credit1.participant_identifier == '55386424'
    assert credit1.amount == Decimal('100.0')
    assert credit1.payment_type_ldl == PaymentType.DIVIDENDS
    assert credit1.movement_type == MovementType.DEPOSIT_OF_ASSET
    assert credit1.payment_number == '213'
    assert credit1.description == 'Refund for overpayment'

    assert isinstance(credit2, CreditRefundGroupError)
    assert credit2.cnpj == '53753940000118'
    assert credit2.participant_identifier == '43075534'
    assert credit2.amount == Decimal('20.0')
    assert credit2.payment_type_ldl == PaymentType.DIVIDENDS
    assert credit2.movement_type == MovementType.DEPOSIT_OF_ASSET
    assert credit2.payment_number == '312'
    assert credit2.description == 'Refund for overpayment'

    assert ldl0006e.general_error_code == 'EGEN0050'


def test_ldl0006e_tag_error_from_xml() -> None:
    xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/SPB/LDL0006E.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>31680151250908000000001</NUOp>
        </BCMSG>
        <SISMSG>
            <LDL0006>
                <CodMsg>LDL0006E</CodMsg>
                <NumCtrlIF_LDL>123</NumCtrlIF_LDL>
                <ISPBIF_LDLDebtd>31680151</ISPBIF_LDLDebtd>
                <ISPBIF_LDLCredtd CodErro="ELDL0123">31680153</ISPBIF_LDLCredtd>
                <CodProdt>ACC</CodProdt>
                <NumCtrlSTROr>STR20250101000000001</NumCtrlSTROr>
                <VlrLanc>120.0</VlrLanc>
                <Grupo_LDL0006_DevCred>
                    <CNPJNLiqdant>50214141000185</CNPJNLiqdant>
                    <IdentdPartCamr>55386424</IdentdPartCamr>
                    <VlrNLiqdant>100.0</VlrNLiqdant>
                    <TpPgtoLDL>2</TpPgtoLDL>
                    <TpMovtc>1</TpMovtc>
                    <NumPgtoLDL>213</NumPgtoLDL>
                    <Hist>Refund for overpayment</Hist>
                </Grupo_LDL0006_DevCred>
                <Grupo_LDL0006_DevCred>
                    <CNPJNLiqdant>53753940000118</CNPJNLiqdant>
                    <IdentdPartCamr>43075534</IdentdPartCamr>
                    <VlrNLiqdant>20.0</VlrNLiqdant>
                    <TpPgtoLDL>2</TpPgtoLDL>
                    <TpMovtc>1</TpMovtc>
                    <NumPgtoLDL>312</NumPgtoLDL>
                    <Hist>Refund for overpayment</Hist>
                </Grupo_LDL0006_DevCred>
                <DtMovto>2025-12-09</DtMovto>
            </LDL0006>
        </SISMSG>
    </DOC>
    """

    ldl0006e = LDL0006E.from_xml(xml)

    assert isinstance(ldl0006e, LDL0006E)
    assert ldl0006e.from_ispb == '31680151'
    assert ldl0006e.to_ispb == '00038166'
    assert ldl0006e.system_domain == 'SPB01'
    assert ldl0006e.operation_number == '31680151250908000000001'
    assert ldl0006e.message_code == 'LDL0006E'
    assert ldl0006e.institution_or_ldl_control_number == '123'
    assert ldl0006e.debitor_institution_ispb == '31680151'
    assert ldl0006e.creditor_institution_ispb == '31680153'
    assert ldl0006e.product_code == ProductCode.AMEX_CREDIT_CARD
    assert ldl0006e.original_str_control_number == 'STR20250101000000001'
    assert ldl0006e.amount == Decimal('120.0')
    assert ldl0006e.settlement_date == date(2025, 12, 9)

    assert len(ldl0006e.credit_refund_group) == CREDIT_REFUND_SIZE
    credit1 = ldl0006e.credit_refund_group[0]
    credit2 = ldl0006e.credit_refund_group[1]
    assert isinstance(credit1, CreditRefundGroupError)
    assert credit1.cnpj == '50214141000185'
    assert credit1.participant_identifier == '55386424'
    assert credit1.amount == Decimal('100.0')
    assert credit1.payment_type_ldl == PaymentType.DIVIDENDS
    assert credit1.movement_type == MovementType.DEPOSIT_OF_ASSET
    assert credit1.payment_number == '213'
    assert credit1.description == 'Refund for overpayment'

    assert isinstance(credit2, CreditRefundGroupError)
    assert credit2.cnpj == '53753940000118'
    assert credit2.participant_identifier == '43075534'
    assert credit2.amount == Decimal('20.0')
    assert credit2.payment_type_ldl == PaymentType.DIVIDENDS
    assert credit2.movement_type == MovementType.DEPOSIT_OF_ASSET
    assert credit2.payment_number == '312'
    assert credit2.description == 'Refund for overpayment'

    assert ldl0006e.creditor_institution_ispb_error_code == 'ELDL0123'


def test_ldl0006_roundtrip() -> None:
    params = make_valid_ldl0006_params()

    ldl0006 = LDL0006.model_validate(params)
    xml = ldl0006.to_xml()
    ldl0006_from_xml = LDL0006.from_xml(xml)

    assert ldl0006 == ldl0006_from_xml


def test_ldl0006r1_roundtrip() -> None:
    params = make_valid_ldl0006r1_params()

    ldl0006r1 = LDL0006R1.model_validate(params)
    xml = ldl0006r1.to_xml()
    ldl0006r1_from_xml = LDL0006R1.from_xml(xml)

    assert ldl0006r1 == ldl0006r1_from_xml


def test_ldl0006r2_roundtrip() -> None:
    params = make_valid_ldl0006r2_params()

    ldl0006r2 = LDL0006R2.model_validate(params)
    xml = ldl0006r2.to_xml()
    ldl0006r2_from_xml = LDL0006R2.from_xml(xml)

    assert ldl0006r2 == ldl0006r2_from_xml


def test_ldl0006_from_xml_missing_required_fields() -> None:
    xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/SPB/LDL0006.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>31680151250908000000001</NUOp>
        </BCMSG>
        <SISMSG>
            <SME0001>
                <CodMsg>SME0001</CodMsg>
            </SME0001>
        </SISMSG>
    </DOC>
    """

    with pytest.raises(ValidationError) as exc:
        LDL0006.from_xml(xml)

    missing_fields = extract_missing_fields(exc.value)
    assert missing_fields == {
        'institution_or_ldl_control_number',
        'debitor_institution_ispb',
        'creditor_institution_ispb',
        'original_str_control_number',
        'amount',
        'settlement_date',
    }
