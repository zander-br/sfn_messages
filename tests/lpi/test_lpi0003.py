from datetime import date, datetime
from decimal import Decimal
from typing import Any

import pytest
from pydantic import ValidationError

from sfn_messages.core.types import StrSettlementStatus
from sfn_messages.lpi.lpi0003 import (
    LPI0003,
    LPI0003E,
    LPI0003R1,
    LPI0003R2,
    CreditorClientGroup,
    CreditorClientGroupError,
    CreditorClientR2Group,
)
from sfn_messages.lpi.types import LpiPurpose
from tests.conftest import extract_missing_fields, normalize_xml


def make_valid_lpi0003_params() -> dict[str, Any]:
    return {
        'from_ispb': '31680151',
        'to_ispb': '00038166',
        'system_domain': 'SPB01',
        'operation_number': '31680151250908000000001',
        'message_code': 'LPI0003',
        'pspi_ispb': '31680153',
        'creditor_institution_ispb': '31680151',
        'creditor_client_group': {'branch': '001', 'account_number': '123456', 'cnpj': '39548823000191'},
        'lpi_purpose': 'OWN_MOVEMENT_OR_TO_SETTLER_ACCOUNT_ON_STR',
        'original_str_control_number': 'STR20250101000000001',
        'amount': 321.23,
        'settlement_date': '2026-02-02',
    }


def make_valid_lpi0003r1_params() -> dict[str, Any]:
    return {
        'from_ispb': '31680151',
        'to_ispb': '00038166',
        'system_domain': 'SPB01',
        'operation_number': '31680151250908000000001',
        'message_code': 'LPI0003R1',
        'pspi_control_number': '123',
        'pspi_ispb': '31680151',
        'str_control_number': 'STR20250101000000001',
        'str_settlement_status': 'EFFECTIVE',
        'settlement_timestamp': '2026-02-02T09:38:00',
        'settlement_date': '2026-02-02',
    }


def make_valid_lpi0003r2_params() -> dict[str, Any]:
    return {
        'from_ispb': '31680151',
        'to_ispb': '00038166',
        'system_domain': 'SPB01',
        'operation_number': '31680151250908000000001',
        'message_code': 'LPI0003R2',
        'str_control_number': 'STR20250101000000001',
        'vendor_timestamp': '2026-02-02T09:39:11',
        'pspi_ispb': '31680153',
        'creditor_institution_ispb': '31680151',
        'creditor_client_group': {'branch': '001', 'account_number': '123456', 'cnpj': '39548823000191'},
        'lpi_purpose': 'OWN_MOVEMENT_OR_TO_SETTLER_ACCOUNT_ON_STR',
        'original_str_control_number': 'STR20250101000000001',
        'amount': 321.23,
        'settlement_date': '2026-02-02',
    }


def make_valid_lpi0003e_params(*, general_error: bool = False) -> dict[str, Any]:
    lpi0003e = {
        'from_ispb': '31680151',
        'to_ispb': '00038166',
        'system_domain': 'SPB01',
        'operation_number': '31680151250908000000001',
        'message_code': 'LPI0003E',
        'pspi_ispb': '31680153',
        'creditor_institution_ispb': '31680151',
        'creditor_client_group': {'branch': '001', 'account_number': '123456', 'cnpj': '39548823000191'},
        'lpi_purpose': 'OWN_MOVEMENT_OR_TO_SETTLER_ACCOUNT_ON_STR',
        'original_str_control_number': 'STR20250101000000001',
        'amount': 321.23,
        'settlement_date': '2026-02-02',
    }

    if general_error:
        lpi0003e['general_error_code'] = 'EGEN0050'
    else:
        lpi0003e['pspi_ispb_error_code'] = 'EGEN0051'

    return lpi0003e


def test_lpi0003_valid_model() -> None:
    params = make_valid_lpi0003_params()
    lpi0003 = LPI0003.model_validate(params)

    assert isinstance(lpi0003, LPI0003)
    assert lpi0003.message_code == 'LPI0003'
    assert lpi0003.pspi_ispb == '31680153'
    assert lpi0003.creditor_institution_ispb == '31680151'
    assert lpi0003.lpi_purpose == LpiPurpose.OWN_MOVEMENT_OR_TO_SETTLER_ACCOUNT_ON_STR
    assert lpi0003.original_str_control_number == 'STR20250101000000001'
    assert lpi0003.amount == Decimal('321.23')
    assert lpi0003.settlement_date == date(2026, 2, 2)

    creditor_group = lpi0003.creditor_client_group
    assert isinstance(creditor_group, CreditorClientGroup)
    assert creditor_group.branch == '001'
    assert creditor_group.account_number == '123456'
    assert creditor_group.cnpj == '39548823000191'


def test_lpi0003r1_valid_model() -> None:
    params = make_valid_lpi0003r1_params()
    lpi0003r1 = LPI0003R1.model_validate(params)

    assert isinstance(lpi0003r1, LPI0003R1)
    assert lpi0003r1.message_code == 'LPI0003R1'
    assert lpi0003r1.pspi_control_number == '123'
    assert lpi0003r1.pspi_ispb == '31680151'
    assert lpi0003r1.str_control_number == 'STR20250101000000001'
    assert lpi0003r1.str_settlement_status == StrSettlementStatus.EFFECTIVE
    assert lpi0003r1.settlement_timestamp == datetime(2026, 2, 2, 9, 38)
    assert lpi0003r1.settlement_date == date(2026, 2, 2)


def test_lpi0003r2_valid_model() -> None:
    params = make_valid_lpi0003r2_params()
    lpi0003r2 = LPI0003R2.model_validate(params)

    assert isinstance(lpi0003r2, LPI0003R2)
    assert lpi0003r2.message_code == 'LPI0003R2'
    assert lpi0003r2.str_control_number == 'STR20250101000000001'
    assert lpi0003r2.vendor_timestamp == datetime(2026, 2, 2, 9, 39, 11)
    assert lpi0003r2.pspi_ispb == '31680153'
    assert lpi0003r2.creditor_institution_ispb == '31680151'
    assert lpi0003r2.lpi_purpose == LpiPurpose.OWN_MOVEMENT_OR_TO_SETTLER_ACCOUNT_ON_STR
    assert lpi0003r2.original_str_control_number == 'STR20250101000000001'
    assert lpi0003r2.amount == Decimal('321.23')
    assert lpi0003r2.settlement_date == date(2026, 2, 2)

    creditor_group = lpi0003r2.creditor_client_group
    assert isinstance(creditor_group, CreditorClientR2Group)
    assert creditor_group.branch == '001'
    assert creditor_group.account_number == '123456'
    assert creditor_group.cnpj == '39548823000191'


def test_lpi0003e_general_error_valid_model() -> None:
    params = make_valid_lpi0003e_params(general_error=True)
    lpi0003e = LPI0003E.model_validate(params)

    assert isinstance(lpi0003e, LPI0003E)
    assert lpi0003e.message_code == 'LPI0003E'
    assert lpi0003e.pspi_ispb == '31680153'
    assert lpi0003e.creditor_institution_ispb == '31680151'
    assert lpi0003e.lpi_purpose == LpiPurpose.OWN_MOVEMENT_OR_TO_SETTLER_ACCOUNT_ON_STR
    assert lpi0003e.original_str_control_number == 'STR20250101000000001'
    assert lpi0003e.amount == Decimal('321.23')
    assert lpi0003e.settlement_date == date(2026, 2, 2)
    assert lpi0003e.general_error_code == 'EGEN0050'

    creditor_group = lpi0003e.creditor_client_group
    assert isinstance(creditor_group, CreditorClientGroupError)
    assert creditor_group.branch == '001'
    assert creditor_group.account_number == '123456'
    assert creditor_group.cnpj == '39548823000191'


def test_lpi0003e_tag_error_valid_model() -> None:
    params = make_valid_lpi0003e_params()
    lpi0003e = LPI0003E.model_validate(params)

    assert isinstance(lpi0003e, LPI0003E)
    assert lpi0003e.message_code == 'LPI0003E'
    assert lpi0003e.pspi_ispb == '31680153'
    assert lpi0003e.creditor_institution_ispb == '31680151'
    assert lpi0003e.lpi_purpose == LpiPurpose.OWN_MOVEMENT_OR_TO_SETTLER_ACCOUNT_ON_STR
    assert lpi0003e.original_str_control_number == 'STR20250101000000001'
    assert lpi0003e.amount == Decimal('321.23')
    assert lpi0003e.settlement_date == date(2026, 2, 2)
    assert lpi0003e.pspi_ispb_error_code == 'EGEN0051'

    creditor_group = lpi0003e.creditor_client_group
    assert isinstance(creditor_group, CreditorClientGroupError)
    assert creditor_group.branch == '001'
    assert creditor_group.account_number == '123456'
    assert creditor_group.cnpj == '39548823000191'


def test_lpi0003_missing_required_fields() -> None:
    with pytest.raises(ValidationError) as exc:
        LPI0003.model_validate({})

    missing_fields = extract_missing_fields(exc.value)
    assert missing_fields == {
        'from_ispb',
        'to_ispb',
        'system_domain',
        'operation_number',
        'pspi_ispb',
        'creditor_institution_ispb',
        'lpi_purpose',
        'amount',
        'settlement_date',
    }


def test_lpi0003r1_missing_required_fields() -> None:
    with pytest.raises(ValidationError) as exc:
        LPI0003R1.model_validate({})

    missing_fields = extract_missing_fields(exc.value)
    assert missing_fields == {
        'from_ispb',
        'to_ispb',
        'system_domain',
        'operation_number',
        'pspi_control_number',
        'pspi_ispb',
        'str_control_number',
        'str_settlement_status',
        'settlement_timestamp',
        'settlement_date',
    }


def test_lpi0003r2_missing_required_fields() -> None:
    with pytest.raises(ValidationError) as exc:
        LPI0003R2.model_validate({})

    missing_fields = extract_missing_fields(exc.value)
    assert missing_fields == {
        'from_ispb',
        'to_ispb',
        'system_domain',
        'operation_number',
        'str_control_number',
        'vendor_timestamp',
        'pspi_ispb',
        'creditor_institution_ispb',
        'lpi_purpose',
        'amount',
        'settlement_date',
    }


def test_lpi0003_to_xml() -> None:
    params = make_valid_lpi0003_params()
    lpi0003 = LPI0003.model_validate(params)

    xml = lpi0003.to_xml()

    expected_xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/SPB/LPI0003.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>31680151250908000000001</NUOp>
        </BCMSG>
        <SISMSG>
            <LPI0003>
                <CodMsg>LPI0003</CodMsg>
                <ISPBPSPI>31680153</ISPBPSPI>
                <ISPBIFCredtd>31680151</ISPBIFCredtd>
                <Grupo_LPI0003_CliCredtd>
                    <AgCredtd>001</AgCredtd>
                    <CtCredtd>123456</CtCredtd>
                    <CNPJCliCredtd>39548823000191</CNPJCliCredtd>
                </Grupo_LPI0003_CliCredtd>
                <FinlddLPI>1</FinlddLPI>
                <NumCtrlSTROr>STR20250101000000001</NumCtrlSTROr>
                <VlrLanc>321.23</VlrLanc>
                <DtMovto>2026-02-02</DtMovto>
            </LPI0003>
        </SISMSG>
    </DOC>
    """
    assert normalize_xml(expected_xml) == normalize_xml(xml)


def test_lpi0003r1_to_xml() -> None:
    params = make_valid_lpi0003r1_params()
    lpi0003r1 = LPI0003R1.model_validate(params)

    xml = lpi0003r1.to_xml()

    expected_xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/SPB/LPI0003.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>31680151250908000000001</NUOp>
        </BCMSG>
        <SISMSG>
            <LPI0003R1>
                <CodMsg>LPI0003R1</CodMsg>
                <NumCtrlPSPI>123</NumCtrlPSPI>
                <ISPBPSPI>31680151</ISPBPSPI>
                <NumCtrlSTR>STR20250101000000001</NumCtrlSTR>
                <SitLancSTR>1</SitLancSTR>
                <DtHrSit>2026-02-02T09:38:00</DtHrSit>
                <DtMovto>2026-02-02</DtMovto>
            </LPI0003R1>
        </SISMSG>
    </DOC>
    """
    assert normalize_xml(expected_xml) == normalize_xml(xml)


def test_lpi0003r2_to_xml() -> None:
    params = make_valid_lpi0003r2_params()
    lpi0003r2 = LPI0003R2.model_validate(params)

    xml = lpi0003r2.to_xml()

    expected_xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/SPB/LPI0003.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>31680151250908000000001</NUOp>
        </BCMSG>
        <SISMSG>
            <LPI0003R2>
                <CodMsg>LPI0003R2</CodMsg>
                <NumCtrlSTR>STR20250101000000001</NumCtrlSTR>
                <DtHrBC>2026-02-02T09:39:11</DtHrBC>
                <ISPBPSPI>31680153</ISPBPSPI>
                <ISPBIFCredtd>31680151</ISPBIFCredtd>
                <Grupo_LPI0003R2_CliCredtd>
                    <AgCredtd>001</AgCredtd>
                    <CtCredtd>123456</CtCredtd>
                    <CNPJCliCredtd>39548823000191</CNPJCliCredtd>
                </Grupo_LPI0003R2_CliCredtd>
                <FinlddLPI>1</FinlddLPI>
                <NumCtrlSTROr>STR20250101000000001</NumCtrlSTROr>
                <VlrLanc>321.23</VlrLanc>
                <DtMovto>2026-02-02</DtMovto>
            </LPI0003R2>
        </SISMSG>
    </DOC>
    """
    assert normalize_xml(expected_xml) == normalize_xml(xml)


def test_lpi0003e_general_error_to_xml() -> None:
    params = make_valid_lpi0003e_params(general_error=True)
    lpi0003e = LPI0003E.model_validate(params)

    xml = lpi0003e.to_xml()

    expected_xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/SPB/LPI0003E.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>31680151250908000000001</NUOp>
        </BCMSG>
        <SISMSG>
            <LPI0003 CodErro="EGEN0050">
                <CodMsg>LPI0003E</CodMsg>
                <ISPBPSPI>31680153</ISPBPSPI>
                <ISPBIFCredtd>31680151</ISPBIFCredtd>
                <Grupo_LPI0003_CliCredtd>
                    <AgCredtd>001</AgCredtd>
                    <CtCredtd>123456</CtCredtd>
                    <CNPJCliCredtd>39548823000191</CNPJCliCredtd>
                </Grupo_LPI0003_CliCredtd>
                <FinlddLPI>1</FinlddLPI>
                <NumCtrlSTROr>STR20250101000000001</NumCtrlSTROr>
                <VlrLanc>321.23</VlrLanc>
                <DtMovto>2026-02-02</DtMovto>
            </LPI0003>
        </SISMSG>
    </DOC>
    """
    assert normalize_xml(expected_xml) == normalize_xml(xml)


def test_lpi0003e_tag_error_to_xml() -> None:
    params = make_valid_lpi0003e_params()
    lpi0003e = LPI0003E.model_validate(params)

    xml = lpi0003e.to_xml()

    expected_xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/SPB/LPI0003E.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>31680151250908000000001</NUOp>
        </BCMSG>
        <SISMSG>
            <LPI0003>
                <CodMsg>LPI0003E</CodMsg>
                <ISPBPSPI CodErro="EGEN0051">31680153</ISPBPSPI>
                <ISPBIFCredtd>31680151</ISPBIFCredtd>
                <Grupo_LPI0003_CliCredtd>
                    <AgCredtd>001</AgCredtd>
                    <CtCredtd>123456</CtCredtd>
                    <CNPJCliCredtd>39548823000191</CNPJCliCredtd>
                </Grupo_LPI0003_CliCredtd>
                <FinlddLPI>1</FinlddLPI>
                <NumCtrlSTROr>STR20250101000000001</NumCtrlSTROr>
                <VlrLanc>321.23</VlrLanc>
                <DtMovto>2026-02-02</DtMovto>
            </LPI0003>
        </SISMSG>
    </DOC>
    """
    assert normalize_xml(expected_xml) == normalize_xml(xml)


def test_lpi0003_from_xml() -> None:
    xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/SPB/LPI0003.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>31680151250908000000001</NUOp>
        </BCMSG>
        <SISMSG>
            <LPI0003>
                <CodMsg>LPI0003</CodMsg>
                <ISPBPSPI>31680153</ISPBPSPI>
                <ISPBIFCredtd>31680151</ISPBIFCredtd>
                <Grupo_LPI0003_CliCredtd>
                    <AgCredtd>001</AgCredtd>
                    <CtCredtd>123456</CtCredtd>
                    <CNPJCliCredtd>39548823000191</CNPJCliCredtd>
                </Grupo_LPI0003_CliCredtd>
                <FinlddLPI>1</FinlddLPI>
                <NumCtrlSTROr>STR20250101000000001</NumCtrlSTROr>
                <VlrLanc>321.23</VlrLanc>
                <DtMovto>2026-02-02</DtMovto>
            </LPI0003>
        </SISMSG>
    </DOC>
    """

    lpi0003 = LPI0003.from_xml(xml)

    assert isinstance(lpi0003, LPI0003)
    assert lpi0003.message_code == 'LPI0003'
    assert lpi0003.pspi_ispb == '31680153'
    assert lpi0003.creditor_institution_ispb == '31680151'
    assert lpi0003.lpi_purpose == LpiPurpose.OWN_MOVEMENT_OR_TO_SETTLER_ACCOUNT_ON_STR
    assert lpi0003.original_str_control_number == 'STR20250101000000001'
    assert lpi0003.amount == Decimal('321.23')
    assert lpi0003.settlement_date == date(2026, 2, 2)

    creditor_group = lpi0003.creditor_client_group
    assert isinstance(creditor_group, CreditorClientGroup)
    assert creditor_group.branch == '001'
    assert creditor_group.account_number == '123456'
    assert creditor_group.cnpj == '39548823000191'


def test_ltr0003r1_from_xml() -> None:
    xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/SPB/LPI0003.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>31680151250908000000001</NUOp>
        </BCMSG>
        <SISMSG>
            <LPI0003R1>
                <CodMsg>LPI0003R1</CodMsg>
                <NumCtrlPSPI>123</NumCtrlPSPI>
                <ISPBPSPI>31680151</ISPBPSPI>
                <NumCtrlSTR>STR20250101000000001</NumCtrlSTR>
                <SitLancSTR>1</SitLancSTR>
                <DtHrSit>2026-02-02T09:38:00</DtHrSit>
                <DtMovto>2026-02-02</DtMovto>
            </LPI0003R1>
        </SISMSG>
    </DOC>
    """

    lpi0003r1 = LPI0003R1.from_xml(xml)

    assert isinstance(lpi0003r1, LPI0003R1)
    assert lpi0003r1.message_code == 'LPI0003R1'
    assert lpi0003r1.pspi_control_number == '123'
    assert lpi0003r1.pspi_ispb == '31680151'
    assert lpi0003r1.str_control_number == 'STR20250101000000001'
    assert lpi0003r1.str_settlement_status == StrSettlementStatus.EFFECTIVE
    assert lpi0003r1.settlement_timestamp == datetime(2026, 2, 2, 9, 38)
    assert lpi0003r1.settlement_date == date(2026, 2, 2)


def test_ltr0003r2_from_xml() -> None:
    xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/SPB/LPI0003.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>31680151250908000000001</NUOp>
        </BCMSG>
        <SISMSG>
            <LPI0003R2>
                <CodMsg>LPI0003R2</CodMsg>
                <NumCtrlSTR>STR20250101000000001</NumCtrlSTR>
                <DtHrBC>2026-02-02T09:39:11</DtHrBC>
                <ISPBPSPI>31680153</ISPBPSPI>
                <ISPBIFCredtd>31680151</ISPBIFCredtd>
                <Grupo_LPI0003R2_CliCredtd>
                    <AgCredtd>001</AgCredtd>
                    <CtCredtd>123456</CtCredtd>
                    <CNPJCliCredtd>39548823000191</CNPJCliCredtd>
                </Grupo_LPI0003R2_CliCredtd>
                <FinlddLPI>1</FinlddLPI>
                <NumCtrlSTROr>STR20250101000000001</NumCtrlSTROr>
                <VlrLanc>321.23</VlrLanc>
                <DtMovto>2026-02-02</DtMovto>
            </LPI0003R2>
        </SISMSG>
    </DOC>
    """

    lpi0003r2 = LPI0003R2.from_xml(xml)

    assert isinstance(lpi0003r2, LPI0003R2)
    assert lpi0003r2.message_code == 'LPI0003R2'
    assert lpi0003r2.str_control_number == 'STR20250101000000001'
    assert lpi0003r2.vendor_timestamp == datetime(2026, 2, 2, 9, 39, 11)
    assert lpi0003r2.pspi_ispb == '31680153'
    assert lpi0003r2.creditor_institution_ispb == '31680151'
    assert lpi0003r2.lpi_purpose == LpiPurpose.OWN_MOVEMENT_OR_TO_SETTLER_ACCOUNT_ON_STR
    assert lpi0003r2.original_str_control_number == 'STR20250101000000001'
    assert lpi0003r2.amount == Decimal('321.23')
    assert lpi0003r2.settlement_date == date(2026, 2, 2)

    creditor_group = lpi0003r2.creditor_client_group
    assert isinstance(creditor_group, CreditorClientR2Group)
    assert creditor_group.branch == '001'
    assert creditor_group.account_number == '123456'
    assert creditor_group.cnpj == '39548823000191'


def test_ltr0003e_general_error_from_xml() -> None:
    xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/SPB/LPI0003E.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>31680151250908000000001</NUOp>
        </BCMSG>
        <SISMSG>
            <LPI0003 CodErro="EGEN0050">
                <CodMsg>LPI0003E</CodMsg>
                <ISPBPSPI>31680153</ISPBPSPI>
                <ISPBIFCredtd>31680151</ISPBIFCredtd>
                <Grupo_LPI0003_CliCredtd>
                    <AgCredtd>001</AgCredtd>
                    <CtCredtd>123456</CtCredtd>
                    <CNPJCliCredtd>39548823000191</CNPJCliCredtd>
                </Grupo_LPI0003_CliCredtd>
                <FinlddLPI>1</FinlddLPI>
                <NumCtrlSTROr>STR20250101000000001</NumCtrlSTROr>
                <VlrLanc>321.23</VlrLanc>
                <DtMovto>2026-02-02</DtMovto>
            </LPI0003>
        </SISMSG>
    </DOC>
    """

    lpi0003e = LPI0003E.from_xml(xml)

    assert isinstance(lpi0003e, LPI0003E)
    assert lpi0003e.message_code == 'LPI0003E'
    assert lpi0003e.pspi_ispb == '31680153'
    assert lpi0003e.creditor_institution_ispb == '31680151'
    assert lpi0003e.lpi_purpose == LpiPurpose.OWN_MOVEMENT_OR_TO_SETTLER_ACCOUNT_ON_STR
    assert lpi0003e.original_str_control_number == 'STR20250101000000001'
    assert lpi0003e.amount == Decimal('321.23')
    assert lpi0003e.settlement_date == date(2026, 2, 2)
    assert lpi0003e.general_error_code == 'EGEN0050'

    creditor_group = lpi0003e.creditor_client_group
    assert isinstance(creditor_group, CreditorClientGroupError)
    assert creditor_group.branch == '001'
    assert creditor_group.account_number == '123456'
    assert creditor_group.cnpj == '39548823000191'


def test_ltr0003e_tag_error_from_xml() -> None:
    xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/SPB/LPI0003E.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>31680151250908000000001</NUOp>
        </BCMSG>
        <SISMSG>
            <LPI0003>
                <CodMsg>LPI0003E</CodMsg>
                <ISPBPSPI CodErro="EGEN0051">31680153</ISPBPSPI>
                <ISPBIFCredtd>31680151</ISPBIFCredtd>
                <Grupo_LPI0003_CliCredtd>
                    <AgCredtd>001</AgCredtd>
                    <CtCredtd>123456</CtCredtd>
                    <CNPJCliCredtd>39548823000191</CNPJCliCredtd>
                </Grupo_LPI0003_CliCredtd>
                <FinlddLPI>1</FinlddLPI>
                <NumCtrlSTROr>STR20250101000000001</NumCtrlSTROr>
                <VlrLanc>321.23</VlrLanc>
                <DtMovto>2026-02-02</DtMovto>
            </LPI0003>
        </SISMSG>
    </DOC>
    """

    lpi0003e = LPI0003E.from_xml(xml)

    assert isinstance(lpi0003e, LPI0003E)
    assert lpi0003e.message_code == 'LPI0003E'
    assert lpi0003e.pspi_ispb == '31680153'
    assert lpi0003e.creditor_institution_ispb == '31680151'
    assert lpi0003e.lpi_purpose == LpiPurpose.OWN_MOVEMENT_OR_TO_SETTLER_ACCOUNT_ON_STR
    assert lpi0003e.original_str_control_number == 'STR20250101000000001'
    assert lpi0003e.amount == Decimal('321.23')
    assert lpi0003e.settlement_date == date(2026, 2, 2)
    assert lpi0003e.pspi_ispb_error_code == 'EGEN0051'

    creditor_group = lpi0003e.creditor_client_group
    assert isinstance(creditor_group, CreditorClientGroupError)
    assert creditor_group.branch == '001'
    assert creditor_group.account_number == '123456'
    assert creditor_group.cnpj == '39548823000191'


def test_lpi0003_roundtrip() -> None:
    params = make_valid_lpi0003_params()

    lpi0003 = LPI0003.model_validate(params)
    xml = lpi0003.to_xml()
    lpi0003_from_xml = LPI0003.from_xml(xml)

    assert lpi0003 == lpi0003_from_xml


def test_lpi0003r1_roundtrip() -> None:
    params = make_valid_lpi0003r1_params()

    lpi0003r1 = LPI0003R1.model_validate(params)
    xml = lpi0003r1.to_xml()
    lpi0003r1_from_xml = LPI0003R1.from_xml(xml)

    assert lpi0003r1 == lpi0003r1_from_xml


def test_lpi0003r2_roundtrip() -> None:
    params = make_valid_lpi0003r2_params()

    lpi0003r2 = LPI0003R2.model_validate(params)
    xml = lpi0003r2.to_xml()
    lpi0003r2_from_xml = LPI0003R2.from_xml(xml)

    assert lpi0003r2 == lpi0003r2_from_xml
