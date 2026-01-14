from datetime import UTC, date, datetime
from decimal import Decimal
from typing import Any

import pytest
from pydantic import ValidationError

from sfn_messages.core.types import StrSettlementStatus
from sfn_messages.sme.sme0002 import SME0002, SME0002E, SME0002R1, SME0002R2, CreditorGroup, CreditorGroupError
from tests.conftest import extract_missing_fields, normalize_xml

RESPONSIBLE_SIZE = 2


def make_valid_sme0002_params() -> dict[str, Any]:
    return {
        'from_ispb': '31680151',
        'to_ispb': '00038166',
        'system_domain': 'SPB01',
        'operation_number': '316801512509080000001',
        'message_code': 'SME0002',
        'ieme_ispb': '31680153',
        'creditor_account_group': {
            'institution_ispb': '31680151',
            'branch': '001',
            'account_number': '123456',
            'cnpj': '56369416000136',
        },
        'amount': '115.5',
        'settlement_date': '2025-12-03',
    }


def make_valid_sme0002r1_params() -> dict[str, Any]:
    return {
        'from_ispb': '31680151',
        'to_ispb': '00038166',
        'system_domain': 'SPB01',
        'operation_number': '316801512509080000001',
        'message_code': 'SME0002R1',
        'institution_control_number_ieme': '123',
        'ieme_ispb': '31680153',
        'str_control_number': 'STR20250101000000001',
        'str_settlement_status': 'EFFECTIVE',
        'settlement_timestamp': '2025-12-03T10:02:00+00:00',
        'settlement_date': '2025-12-03',
    }


def make_valid_sme0002r2_params() -> dict[str, Any]:
    return {
        'from_ispb': '31680151',
        'to_ispb': '00038166',
        'system_domain': 'SPB01',
        'operation_number': '316801512509080000001',
        'message_code': 'SME0002R2',
        'str_control_number': 'STR20250101000000001',
        'vendor_timestamp': '2025-12-03T10:02:00+00:00',
        'ieme_ispb': '31680153',
        'institution_ispb': '31680151',
        'creditor_branch': '001',
        'creditor_account_number': '123456',
        'creditor_cnpj': '56369416000136',
        'settlement_date': '2025-12-03',
    }


def make_valid_sme0002e_params(*, general_error: bool = False) -> dict[str, Any]:
    sme0002e: dict[str, Any] = {
        'from_ispb': '31680151',
        'to_ispb': '00038166',
        'system_domain': 'SPB01',
        'operation_number': '316801512509080000001',
        'message_code': 'SME0002',
        'ieme_ispb': '31680153',
        'creditor_account_group': {
            'institution_ispb': '31680151',
            'branch': '001',
            'account_number': '123456',
            'cnpj': '56369416000136',
        },
        'amount': '115.5',
        'settlement_date': '2025-12-03',
    }

    if general_error:
        sme0002e['general_error_code'] = 'EGEN0050'
    else:
        sme0002e['ieme_ispb_error_code'] = 'EGEN0051'
        sme0002e['creditor_account_group']['account_number_error_code'] = 'ESME0001'

    return sme0002e


def test_sme0002_valid_model() -> None:
    params = make_valid_sme0002_params()
    sme0002 = SME0002.model_validate(params)

    assert isinstance(sme0002, SME0002)
    assert sme0002.from_ispb == '31680151'
    assert sme0002.to_ispb == '00038166'
    assert sme0002.system_domain == 'SPB01'
    assert sme0002.operation_number == '316801512509080000001'
    assert sme0002.message_code == 'SME0002'
    assert sme0002.ieme_ispb == '31680153'
    assert sme0002.amount == Decimal('115.5')
    assert sme0002.settlement_date == date(2025, 12, 3)

    creditor_group = sme0002.creditor_account_group
    assert isinstance(creditor_group, CreditorGroup)
    assert creditor_group.institution_ispb == '31680151'
    assert creditor_group.branch == '001'
    assert creditor_group.account_number == '123456'
    assert creditor_group.cnpj == '56369416000136'


def test_sme0002r1_valid_model() -> None:
    params = make_valid_sme0002r1_params()
    sme0002r1 = SME0002R1.model_validate(params)

    assert isinstance(sme0002r1, SME0002R1)
    assert sme0002r1.from_ispb == '31680151'
    assert sme0002r1.to_ispb == '00038166'
    assert sme0002r1.system_domain == 'SPB01'
    assert sme0002r1.operation_number == '316801512509080000001'
    assert sme0002r1.message_code == 'SME0002R1'
    assert sme0002r1.institution_control_number_ieme == '123'
    assert sme0002r1.ieme_ispb == '31680153'
    assert sme0002r1.str_control_number == 'STR20250101000000001'
    assert sme0002r1.str_settlement_status == StrSettlementStatus.EFFECTIVE
    assert sme0002r1.settlement_timestamp == datetime(2025, 12, 3, 10, 2, tzinfo=UTC)
    assert sme0002r1.settlement_date == date(2025, 12, 3)


def test_sme0002r2_valid_model() -> None:
    params = make_valid_sme0002r2_params()
    sme0002r2 = SME0002R2.model_validate(params)

    assert isinstance(sme0002r2, SME0002R2)
    assert sme0002r2.from_ispb == '31680151'
    assert sme0002r2.to_ispb == '00038166'
    assert sme0002r2.system_domain == 'SPB01'
    assert sme0002r2.operation_number == '316801512509080000001'
    assert sme0002r2.message_code == 'SME0002R2'
    assert sme0002r2.str_control_number == 'STR20250101000000001'
    assert sme0002r2.vendor_timestamp == datetime(2025, 12, 3, 10, 2, tzinfo=UTC)
    assert sme0002r2.ieme_ispb == '31680153'
    assert sme0002r2.institution_ispb == '31680151'
    assert sme0002r2.creditor_branch == '001'
    assert sme0002r2.creditor_account_number == '123456'
    assert sme0002r2.creditor_cnpj == '56369416000136'
    assert sme0002r2.settlement_date == date(2025, 12, 3)


def test_sme0002e_general_error_valid_model() -> None:
    params = make_valid_sme0002e_params(general_error=True)
    sme0002 = SME0002E.model_validate(params)

    assert isinstance(sme0002, SME0002E)
    assert sme0002.from_ispb == '31680151'
    assert sme0002.to_ispb == '00038166'
    assert sme0002.system_domain == 'SPB01'
    assert sme0002.operation_number == '316801512509080000001'
    assert sme0002.message_code == 'SME0002'
    assert sme0002.ieme_ispb == '31680153'
    assert sme0002.amount == Decimal('115.5')
    assert sme0002.settlement_date == date(2025, 12, 3)
    assert sme0002.general_error_code == 'EGEN0050'

    creditor_group = sme0002.creditor_account_group
    assert isinstance(creditor_group, CreditorGroupError)
    assert creditor_group.institution_ispb == '31680151'
    assert creditor_group.branch == '001'
    assert creditor_group.account_number == '123456'
    assert creditor_group.cnpj == '56369416000136'


def test_sme0002e_tag_error_valid_model() -> None:
    params = make_valid_sme0002e_params()
    sme0002e = SME0002E.model_validate(params)

    assert isinstance(sme0002e, SME0002E)
    assert sme0002e.from_ispb == '31680151'
    assert sme0002e.to_ispb == '00038166'
    assert sme0002e.system_domain == 'SPB01'
    assert sme0002e.operation_number == '316801512509080000001'
    assert sme0002e.message_code == 'SME0002'
    assert sme0002e.ieme_ispb == '31680153'
    assert sme0002e.amount == Decimal('115.5')
    assert sme0002e.settlement_date == date(2025, 12, 3)
    assert sme0002e.ieme_ispb_error_code == 'EGEN0051'

    creditor_group = sme0002e.creditor_account_group
    assert isinstance(creditor_group, CreditorGroupError)
    assert creditor_group.institution_ispb == '31680151'
    assert creditor_group.branch == '001'
    assert creditor_group.account_number == '123456'
    assert creditor_group.cnpj == '56369416000136'
    assert creditor_group.account_number_error_code == 'ESME0001'


def test_sme0002_missing_required_fields() -> None:
    with pytest.raises(ValidationError) as exc:
        SME0002.model_validate({})

    missing_fields = extract_missing_fields(exc.value)
    assert missing_fields == {
        'from_ispb',
        'to_ispb',
        'system_domain',
        'operation_number',
        'ieme_ispb',
        'amount',
        'settlement_date',
    }


def test_sme0002r1_missing_required_fields() -> None:
    with pytest.raises(ValidationError) as exc:
        SME0002R1.model_validate({})

    missing_fields = extract_missing_fields(exc.value)
    assert missing_fields == {
        'from_ispb',
        'to_ispb',
        'system_domain',
        'operation_number',
        'institution_control_number_ieme',
        'ieme_ispb',
        'str_control_number',
        'str_settlement_status',
        'settlement_timestamp',
        'settlement_date',
    }


def test_sme0002r2_missing_required_fields() -> None:
    with pytest.raises(ValidationError) as exc:
        SME0002R2.model_validate({})

    missing_fields = extract_missing_fields(exc.value)
    assert missing_fields == {
        'from_ispb',
        'to_ispb',
        'system_domain',
        'operation_number',
        'str_control_number',
        'vendor_timestamp',
        'ieme_ispb',
        'institution_ispb',
        'creditor_branch',
        'creditor_account_number',
        'creditor_cnpj',
        'settlement_date',
    }


def test_sme0002_to_xml() -> None:
    params = make_valid_sme0002_params()
    sme0002 = SME0002.model_validate(params)

    xml = sme0002.to_xml()

    expected_xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/SME/SME0002.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>316801512509080000001</NUOp>
        </BCMSG>
        <SISMSG>
            <SME0002>
                <CodMsg>SME0002</CodMsg>
                <ISPBIEME>31680153</ISPBIEME>
                <Grupo_SME0002_CtCredtd>
                    <ISPBIFCredtd>31680151</ISPBIFCredtd>
                    <AgCredtd>001</AgCredtd>
                    <CtCredtd>123456</CtCredtd>
                    <CNPJCliCredtd>56369416000136</CNPJCliCredtd>
                </Grupo_SME0002_CtCredtd>
                <VlrLanc>115.5</VlrLanc>
                <DtMovto>2025-12-03</DtMovto>
            </SME0002>
        </SISMSG>
    </DOC>
    """
    assert normalize_xml(expected_xml) == normalize_xml(xml)


def test_sme0002r1_to_xml() -> None:
    params = make_valid_sme0002r1_params()
    sme0002r1 = SME0002R1.model_validate(params)

    xml = sme0002r1.to_xml()

    expected_xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/SME/SME0002.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>316801512509080000001</NUOp>
        </BCMSG>
        <SISMSG>
            <SME0002R1>
                <CodMsg>SME0002R1</CodMsg>
                <NumCtrlIEME>123</NumCtrlIEME>
                <ISPBIEME>31680153</ISPBIEME>
                <NumCtrlSTR>STR20250101000000001</NumCtrlSTR>
                <SitLancSTR>1</SitLancSTR>
                <DtHrSit>2025-12-03 10:02:00+00:00</DtHrSit>
                <DtMovto>2025-12-03</DtMovto>
            </SME0002R1>
        </SISMSG>
    </DOC>
    """
    assert normalize_xml(expected_xml) == normalize_xml(xml)


def test_sme0002r2_to_xml() -> None:
    params = make_valid_sme0002r2_params()
    sme0002r2 = SME0002R2.model_validate(params)

    xml = sme0002r2.to_xml()

    expected_xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/SME/SME0002.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>316801512509080000001</NUOp>
        </BCMSG>
        <SISMSG>
            <SME0002R2>
                <CodMsg>SME0002R2</CodMsg>
                <NumCtrlSTR>STR20250101000000001</NumCtrlSTR>
                <DtHrBC>2025-12-03 10:02:00+00:00</DtHrBC>
                <ISPBIEME>31680153</ISPBIEME>
                <ISPBIFCredtd>31680151</ISPBIFCredtd>
                <AgCredtd>001</AgCredtd>
                <CtCredtd>123456</CtCredtd>
                <CNPJCliCredtd>56369416000136</CNPJCliCredtd>
                <DtMovto>2025-12-03</DtMovto>
            </SME0002R2>
        </SISMSG>
    </DOC>
    """
    assert normalize_xml(expected_xml) == normalize_xml(xml)


def test_sme0002e_general_error_to_xml() -> None:
    params = make_valid_sme0002e_params(general_error=True)
    sme0002e = SME0002E.model_validate(params)

    xml = sme0002e.to_xml()

    expected_xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/SME/SME0002E.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>316801512509080000001</NUOp>
        </BCMSG>
        <SISMSG>
            <SME0002E CodErro="EGEN0050">
                <CodMsg>SME0002</CodMsg>
                <ISPBIEME>31680153</ISPBIEME>
                <Grupo_SME0002_CtCredtd>
                    <ISPBIFCredtd>31680151</ISPBIFCredtd>
                    <AgCredtd>001</AgCredtd>
                    <CtCredtd>123456</CtCredtd>
                    <CNPJCliCredtd>56369416000136</CNPJCliCredtd>
                </Grupo_SME0002_CtCredtd>
                <VlrLanc>115.5</VlrLanc>
                <DtMovto>2025-12-03</DtMovto>
            </SME0002E>
        </SISMSG>
    </DOC>
    """
    assert normalize_xml(expected_xml) == normalize_xml(xml)


def test_sme0002e_tag_error_to_xml() -> None:
    params = make_valid_sme0002e_params()
    sme0002e = SME0002E.model_validate(params)

    xml = sme0002e.to_xml()

    expected_xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/SME/SME0002E.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>316801512509080000001</NUOp>
        </BCMSG>
        <SISMSG>
            <SME0002E>
                <CodMsg>SME0002</CodMsg>
                <ISPBIEME CodErro="EGEN0051">31680153</ISPBIEME>
                <Grupo_SME0002_CtCredtd>
                    <ISPBIFCredtd>31680151</ISPBIFCredtd>
                    <AgCredtd>001</AgCredtd>
                    <CtCredtd CodErro="ESME0001">123456</CtCredtd>
                    <CNPJCliCredtd>56369416000136</CNPJCliCredtd>
                </Grupo_SME0002_CtCredtd>
                <VlrLanc>115.5</VlrLanc>
                <DtMovto>2025-12-03</DtMovto>
            </SME0002E>
        </SISMSG>
    </DOC>
    """
    assert normalize_xml(expected_xml) == normalize_xml(xml)


def test_sme0002_from_xml() -> None:
    xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/SME/SME0002.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>316801512509080000001</NUOp>
        </BCMSG>
        <SISMSG>
            <SME0002>
                <CodMsg>SME0002</CodMsg>
                <ISPBIEME>31680153</ISPBIEME>
                <Grupo_SME0002_CtCredtd>
                    <ISPBIFCredtd>31680151</ISPBIFCredtd>
                    <AgCredtd>001</AgCredtd>
                    <CtCredtd>123456</CtCredtd>
                    <CNPJCliCredtd>56369416000136</CNPJCliCredtd>
                </Grupo_SME0002_CtCredtd>
                <VlrLanc>115.5</VlrLanc>
                <DtMovto>2025-12-03</DtMovto>
            </SME0002>
        </SISMSG>
    </DOC>
    """

    sme0002 = SME0002.from_xml(xml)

    assert isinstance(sme0002, SME0002)
    assert sme0002.from_ispb == '31680151'
    assert sme0002.to_ispb == '00038166'
    assert sme0002.system_domain == 'SPB01'
    assert sme0002.operation_number == '316801512509080000001'
    assert sme0002.message_code == 'SME0002'
    assert sme0002.ieme_ispb == '31680153'
    assert sme0002.amount == Decimal('115.5')
    assert sme0002.settlement_date == date(2025, 12, 3)

    creditor_group = sme0002.creditor_account_group
    assert isinstance(creditor_group, CreditorGroup)
    assert creditor_group.institution_ispb == '31680151'
    assert creditor_group.branch == '001'
    assert creditor_group.account_number == '123456'
    assert creditor_group.cnpj == '56369416000136'


def test_sme0002r1_from_xml() -> None:
    xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/SME/SME0002.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>316801512509080000001</NUOp>
        </BCMSG>
        <SISMSG>
            <SME0002R1>
                <CodMsg>SME0002R1</CodMsg>
                <NumCtrlIEME>123</NumCtrlIEME>
                <ISPBIEME>31680153</ISPBIEME>
                <NumCtrlSTR>STR20250101000000001</NumCtrlSTR>
                <SitLancSTR>1</SitLancSTR>
                <DtHrSit>2025-12-03 10:02:00+00:00</DtHrSit>
                <DtMovto>2025-12-03</DtMovto>
            </SME0002R1>
        </SISMSG>
    </DOC>
    """

    sme0002r1 = SME0002R1.from_xml(xml)

    assert isinstance(sme0002r1, SME0002R1)
    assert sme0002r1.from_ispb == '31680151'
    assert sme0002r1.to_ispb == '00038166'
    assert sme0002r1.system_domain == 'SPB01'
    assert sme0002r1.operation_number == '316801512509080000001'
    assert sme0002r1.message_code == 'SME0002R1'
    assert sme0002r1.institution_control_number_ieme == '123'
    assert sme0002r1.ieme_ispb == '31680153'
    assert sme0002r1.str_control_number == 'STR20250101000000001'
    assert sme0002r1.str_settlement_status == StrSettlementStatus.EFFECTIVE
    assert sme0002r1.settlement_timestamp == datetime(2025, 12, 3, 10, 2, tzinfo=UTC)
    assert sme0002r1.settlement_date == date(2025, 12, 3)


def test_sme0002r2_from_xml() -> None:
    xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/SME/SME0002.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>316801512509080000001</NUOp>
        </BCMSG>
        <SISMSG>
            <SME0002R2>
                <CodMsg>SME0002R2</CodMsg>
                <NumCtrlSTR>STR20250101000000001</NumCtrlSTR>
                <DtHrBC>2025-12-03 10:02:00+00:00</DtHrBC>
                <ISPBIEME>31680153</ISPBIEME>
                <ISPBIFCredtd>31680151</ISPBIFCredtd>
                <AgCredtd>001</AgCredtd>
                <CtCredtd>123456</CtCredtd>
                <CNPJCliCredtd>56369416000136</CNPJCliCredtd>
                <DtMovto>2025-12-03</DtMovto>
            </SME0002R2>
        </SISMSG>
    </DOC>
    """

    sme0002r2 = SME0002R2.from_xml(xml)

    assert isinstance(sme0002r2, SME0002R2)
    assert sme0002r2.from_ispb == '31680151'
    assert sme0002r2.to_ispb == '00038166'
    assert sme0002r2.system_domain == 'SPB01'
    assert sme0002r2.operation_number == '316801512509080000001'
    assert sme0002r2.message_code == 'SME0002R2'
    assert sme0002r2.str_control_number == 'STR20250101000000001'
    assert sme0002r2.vendor_timestamp == datetime(2025, 12, 3, 10, 2, tzinfo=UTC)
    assert sme0002r2.ieme_ispb == '31680153'
    assert sme0002r2.institution_ispb == '31680151'
    assert sme0002r2.creditor_branch == '001'
    assert sme0002r2.creditor_account_number == '123456'
    assert sme0002r2.creditor_cnpj == '56369416000136'
    assert sme0002r2.settlement_date == date(2025, 12, 3)


def test_sme0002e_general_error_from_xml() -> None:
    xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/SME/SME0002E.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>316801512509080000001</NUOp>
        </BCMSG>
        <SISMSG>
            <SME0002E CodErro="EGEN0050">
                <CodMsg>SME0002</CodMsg>
                <ISPBIEME>31680153</ISPBIEME>
                <Grupo_SME0002_CtCredtd>
                    <ISPBIFCredtd>31680151</ISPBIFCredtd>
                    <AgCredtd>001</AgCredtd>
                    <CtCredtd>123456</CtCredtd>
                    <CNPJCliCredtd>56369416000136</CNPJCliCredtd>
                </Grupo_SME0002_CtCredtd>
                <VlrLanc>115.5</VlrLanc>
                <DtMovto>2025-12-03</DtMovto>
            </SME0002E>
        </SISMSG>
    </DOC>
    """

    sme0002e = SME0002E.from_xml(xml)

    assert isinstance(sme0002e, SME0002E)
    assert sme0002e.from_ispb == '31680151'
    assert sme0002e.to_ispb == '00038166'
    assert sme0002e.system_domain == 'SPB01'
    assert sme0002e.operation_number == '316801512509080000001'
    assert sme0002e.message_code == 'SME0002'
    assert sme0002e.ieme_ispb == '31680153'
    assert sme0002e.amount == Decimal('115.5')
    assert sme0002e.settlement_date == date(2025, 12, 3)
    assert sme0002e.general_error_code == 'EGEN0050'

    creditor_group = sme0002e.creditor_account_group
    assert isinstance(creditor_group, CreditorGroupError)
    assert creditor_group.institution_ispb == '31680151'
    assert creditor_group.branch == '001'
    assert creditor_group.account_number == '123456'
    assert creditor_group.cnpj == '56369416000136'


def test_sme0002e_tag_error_from_xml() -> None:
    xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/SME/SME0002E.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>316801512509080000001</NUOp>
        </BCMSG>
        <SISMSG>
            <SME0002E>
                <CodMsg>SME0002</CodMsg>
                <ISPBIEME CodErro="EGEN0051">31680153</ISPBIEME>
                <Grupo_SME0002_CtCredtd>
                    <ISPBIFCredtd>31680151</ISPBIFCredtd>
                    <AgCredtd>001</AgCredtd>
                    <CtCredtd CodErro="ESME0001">123456</CtCredtd>
                    <CNPJCliCredtd>56369416000136</CNPJCliCredtd>
                </Grupo_SME0002_CtCredtd>
                <VlrLanc>115.5</VlrLanc>
                <DtMovto>2025-12-03</DtMovto>
            </SME0002E>
        </SISMSG>
    </DOC>
    """

    sme0002e = SME0002E.from_xml(xml)

    assert isinstance(sme0002e, SME0002E)
    assert sme0002e.from_ispb == '31680151'
    assert sme0002e.to_ispb == '00038166'
    assert sme0002e.system_domain == 'SPB01'
    assert sme0002e.operation_number == '316801512509080000001'
    assert sme0002e.message_code == 'SME0002'
    assert sme0002e.ieme_ispb == '31680153'
    assert sme0002e.amount == Decimal('115.5')
    assert sme0002e.settlement_date == date(2025, 12, 3)
    assert sme0002e.ieme_ispb_error_code == 'EGEN0051'

    creditor_group = sme0002e.creditor_account_group
    assert isinstance(creditor_group, CreditorGroupError)
    assert creditor_group.institution_ispb == '31680151'
    assert creditor_group.branch == '001'
    assert creditor_group.account_number == '123456'
    assert creditor_group.cnpj == '56369416000136'
    assert creditor_group.account_number_error_code == 'ESME0001'


def test_sme0002_roundtrip() -> None:
    params = make_valid_sme0002_params()

    sme0002 = SME0002.model_validate(params)
    xml = sme0002.to_xml()
    sme0002_from_xml = SME0002.from_xml(xml)

    assert sme0002 == sme0002_from_xml


def test_sme0002r1_roundtrip() -> None:
    params = make_valid_sme0002r1_params()

    sme0002r1 = SME0002R1.model_validate(params)
    xml = sme0002r1.to_xml()
    sme0002r1_from_xml = SME0002R1.from_xml(xml)

    assert sme0002r1 == sme0002r1_from_xml


def test_sme0002r2_roundtrip() -> None:
    params = make_valid_sme0002r2_params()

    sme0002r2 = SME0002R2.model_validate(params)
    xml = sme0002r2.to_xml()
    sme0002r2_from_xml = SME0002R2.from_xml(xml)

    assert sme0002r2 == sme0002r2_from_xml


def test_sme0002_from_xml_missing_required_fields() -> None:
    xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/SME/SME0002.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>316801512509080000001</NUOp>
        </BCMSG>
        <SISMSG>
            <SME0002>
                <CodMsg>SME0002</CodMsg>
                <Grupo_SME0002_CtCredtd>
                    <ISPBIFCredtd>31680151</ISPBIFCredtd>
                    <AgCredtd>001</AgCredtd>
                    <CtCredtd>123456</CtCredtd>
                    <CNPJCliCredtd>56369416000136</CNPJCliCredtd>
                </Grupo_SME0002_CtCredtd>
            </SME0002>
        </SISMSG>
    </DOC>
    """

    with pytest.raises(ValidationError) as exc:
        SME0002.from_xml(xml)

    missing_fields = extract_missing_fields(exc.value)
    assert missing_fields == {
        'ieme_ispb',
        'amount',
        'settlement_date',
    }
