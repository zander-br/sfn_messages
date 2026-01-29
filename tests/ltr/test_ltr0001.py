from datetime import date
from decimal import Decimal
from typing import Any

import pytest
from pydantic import ValidationError

from sfn_messages.core.types import AssetType
from sfn_messages.ltr.ltr0001 import LTR0001, LTR0001E
from sfn_messages.ltr.types import LtrOperationType
from tests.conftest import extract_missing_fields, normalize_xml


def make_valid_ltr0001_params() -> dict[str, Any]:
    return {
        'from_ispb': '31680151',
        'to_ispb': '00038166',
        'system_domain': 'SPB01',
        'operation_number': '31680151250908000000001',
        'message_code': 'LTR0001',
        'ltr_control_number': '321',
        'ltr_ispb': '31680153',
        'debtor_institution_ispb': '31680151',
        'creditor_institution_ispb': '31680152',
        'cnpj': '27063777000151',
        'participant_identifier': '43075534',
        'debtor_branch': '0002',
        'debtor_account_number': '654321',
        'amount': 123.0,
        'ltr_operation_type': 'NORMAL',
        'ltr_operation_number': '456',
        'sub_asset_type': 'INVESTMENT_PORTFOLIO_ASSETS',
        'asset_description': 'Test asset description',
        'description': 'Test description',
        'settlement_date': '2026-01-28',
    }


def make_valid_ltr0001e_params(*, general_error: bool = False) -> dict[str, Any]:
    ltr0001e = {
        'from_ispb': '31680151',
        'to_ispb': '00038166',
        'system_domain': 'SPB01',
        'operation_number': '31680151250908000000001',
        'message_code': 'LTR0001E',
        'ltr_control_number': '321',
        'ltr_ispb': '31680153',
        'debtor_institution_ispb': '31680151',
        'creditor_institution_ispb': '31680152',
        'cnpj': '27063777000151',
        'participant_identifier': '43075534',
        'debtor_branch': '0002',
        'debtor_account_number': '654321',
        'amount': 123.0,
        'ltr_operation_type': 'NORMAL',
        'ltr_operation_number': '456',
        'sub_asset_type': 'INVESTMENT_PORTFOLIO_ASSETS',
        'asset_description': 'Test asset description',
        'description': 'Test description',
        'settlement_date': '2026-01-28',
    }

    if general_error:
        ltr0001e['general_error_code'] = 'EGEN0050'
    else:
        ltr0001e['ltr_ispb_error_code'] = 'EGEN0051'

    return ltr0001e


def test_ltr0001_valid_model() -> None:
    params = make_valid_ltr0001_params()
    ltr0001 = LTR0001.model_validate(params)

    assert isinstance(ltr0001, LTR0001)
    assert ltr0001.from_ispb == '31680151'
    assert ltr0001.to_ispb == '00038166'
    assert ltr0001.system_domain == 'SPB01'
    assert ltr0001.operation_number == '31680151250908000000001'
    assert ltr0001.message_code == 'LTR0001'
    assert ltr0001.ltr_control_number == '321'
    assert ltr0001.ltr_ispb == '31680153'
    assert ltr0001.debtor_institution_ispb == '31680151'
    assert ltr0001.creditor_institution_ispb == '31680152'
    assert ltr0001.cnpj == '27063777000151'
    assert ltr0001.participant_identifier == '43075534'
    assert ltr0001.debtor_branch == '0002'
    assert ltr0001.debtor_account_number == '654321'
    assert ltr0001.amount == Decimal('123.0')
    assert ltr0001.ltr_operation_type == LtrOperationType.NORMAL
    assert ltr0001.ltr_operation_number == '456'
    assert ltr0001.sub_asset_type == AssetType.INVESTMENT_PORTFOLIO_ASSETS
    assert ltr0001.asset_description == 'Test asset description'
    assert ltr0001.description == 'Test description'
    assert ltr0001.settlement_date == date(2026, 1, 28)


def test_ltr0001e_general_error_valid_model() -> None:
    params = make_valid_ltr0001e_params(general_error=True)
    ltr0001e = LTR0001E.model_validate(params)

    assert isinstance(ltr0001e, LTR0001E)
    assert ltr0001e.from_ispb == '31680151'
    assert ltr0001e.to_ispb == '00038166'
    assert ltr0001e.system_domain == 'SPB01'
    assert ltr0001e.operation_number == '31680151250908000000001'
    assert ltr0001e.message_code == 'LTR0001E'
    assert ltr0001e.ltr_control_number == '321'
    assert ltr0001e.ltr_ispb == '31680153'
    assert ltr0001e.debtor_institution_ispb == '31680151'
    assert ltr0001e.creditor_institution_ispb == '31680152'
    assert ltr0001e.cnpj == '27063777000151'
    assert ltr0001e.participant_identifier == '43075534'
    assert ltr0001e.debtor_branch == '0002'
    assert ltr0001e.debtor_account_number == '654321'
    assert ltr0001e.amount == Decimal('123.0')
    assert ltr0001e.ltr_operation_type == LtrOperationType.NORMAL
    assert ltr0001e.ltr_operation_number == '456'
    assert ltr0001e.sub_asset_type == AssetType.INVESTMENT_PORTFOLIO_ASSETS
    assert ltr0001e.asset_description == 'Test asset description'
    assert ltr0001e.description == 'Test description'
    assert ltr0001e.settlement_date == date(2026, 1, 28)
    assert ltr0001e.general_error_code == 'EGEN0050'


def test_ltr0001e_tag_error_valid_model() -> None:
    params = make_valid_ltr0001e_params()
    ltr0001e = LTR0001E.model_validate(params)

    assert isinstance(ltr0001e, LTR0001E)
    assert ltr0001e.from_ispb == '31680151'
    assert ltr0001e.to_ispb == '00038166'
    assert ltr0001e.system_domain == 'SPB01'
    assert ltr0001e.operation_number == '31680151250908000000001'
    assert ltr0001e.message_code == 'LTR0001E'
    assert ltr0001e.ltr_control_number == '321'
    assert ltr0001e.ltr_ispb == '31680153'
    assert ltr0001e.debtor_institution_ispb == '31680151'
    assert ltr0001e.creditor_institution_ispb == '31680152'
    assert ltr0001e.cnpj == '27063777000151'
    assert ltr0001e.participant_identifier == '43075534'
    assert ltr0001e.debtor_branch == '0002'
    assert ltr0001e.debtor_account_number == '654321'
    assert ltr0001e.amount == Decimal('123.0')
    assert ltr0001e.ltr_operation_type == LtrOperationType.NORMAL
    assert ltr0001e.ltr_operation_number == '456'
    assert ltr0001e.sub_asset_type == AssetType.INVESTMENT_PORTFOLIO_ASSETS
    assert ltr0001e.asset_description == 'Test asset description'
    assert ltr0001e.description == 'Test description'
    assert ltr0001e.settlement_date == date(2026, 1, 28)
    assert ltr0001e.ltr_ispb_error_code == 'EGEN0051'


def test_ltr0001_missing_required_fields() -> None:
    with pytest.raises(ValidationError) as exc:
        LTR0001.model_validate({})

    missing_fields = extract_missing_fields(exc.value)
    assert missing_fields == {
        'from_ispb',
        'to_ispb',
        'system_domain',
        'operation_number',
        'ltr_control_number',
        'ltr_ispb',
        'debtor_institution_ispb',
        'creditor_institution_ispb',
        'cnpj',
        'amount',
        'ltr_operation_type',
        'ltr_operation_number',
        'sub_asset_type',
        'settlement_date',
    }


def test_ltr0001_to_xml() -> None:
    params = make_valid_ltr0001_params()
    ltr0001 = LTR0001.model_validate(params)

    xml = ltr0001.to_xml()

    expected_xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/SPB/LTR0001.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>31680151250908000000001</NUOp>
        </BCMSG>
        <SISMSG>
            <LTR0001>
                <CodMsg>LTR0001</CodMsg>
                <NumCtrlLTR>321</NumCtrlLTR>
                <ISPBLTR>31680153</ISPBLTR>
                <ISPBIFDebtd>31680151</ISPBIFDebtd>
                <ISPBIFCredtd>31680152</ISPBIFCredtd>
                <CNPJNLiqdant>27063777000151</CNPJNLiqdant>
                <IdentdPartCamr>43075534</IdentdPartCamr>
                <AgDebtd>0002</AgDebtd>
                <CtDebtd>654321</CtDebtd>
                <VlrLanc>123.0</VlrLanc>
                <TpOpLTR>0</TpOpLTR>
                <NumOpLTR>456</NumOpLTR>
                <SubTpAtv>ACI</SubTpAtv>
                <DescAtv>Test asset description</DescAtv>
                <Hist>Test description</Hist>
                <DtMovto>2026-01-28</DtMovto>
            </LTR0001>
        </SISMSG>
    </DOC>
    """
    assert normalize_xml(expected_xml) == normalize_xml(xml)


def test_ltr0001e_general_error_to_xml() -> None:
    params = make_valid_ltr0001e_params(general_error=True)
    ltr0001e = LTR0001E.model_validate(params)

    xml = ltr0001e.to_xml()

    expected_xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/SPB/LTR0001E.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>31680151250908000000001</NUOp>
        </BCMSG>
        <SISMSG>
            <LTR0001 CodErro="EGEN0050">
                <CodMsg>LTR0001E</CodMsg>
                <NumCtrlLTR>321</NumCtrlLTR>
                <ISPBLTR>31680153</ISPBLTR>
                <ISPBIFDebtd>31680151</ISPBIFDebtd>
                <ISPBIFCredtd>31680152</ISPBIFCredtd>
                <CNPJNLiqdant>27063777000151</CNPJNLiqdant>
                <IdentdPartCamr>43075534</IdentdPartCamr>
                <AgDebtd>0002</AgDebtd>
                <CtDebtd>654321</CtDebtd>
                <VlrLanc>123.0</VlrLanc>
                <TpOpLTR>0</TpOpLTR>
                <NumOpLTR>456</NumOpLTR>
                <SubTpAtv>ACI</SubTpAtv>
                <DescAtv>Test asset description</DescAtv>
                <Hist>Test description</Hist>
                <DtMovto>2026-01-28</DtMovto>
            </LTR0001>
        </SISMSG>
    </DOC>
    """
    assert normalize_xml(expected_xml) == normalize_xml(xml)


def test_ltr0001e_tag_error_to_xml() -> None:
    params = make_valid_ltr0001e_params()
    ltr0001e = LTR0001E.model_validate(params)

    xml = ltr0001e.to_xml()

    expected_xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/SPB/LTR0001E.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>31680151250908000000001</NUOp>
        </BCMSG>
        <SISMSG>
            <LTR0001>
                <CodMsg>LTR0001E</CodMsg>
                <NumCtrlLTR>321</NumCtrlLTR>
                <ISPBLTR CodErro="EGEN0051">31680153</ISPBLTR>
                <ISPBIFDebtd>31680151</ISPBIFDebtd>
                <ISPBIFCredtd>31680152</ISPBIFCredtd>
                <CNPJNLiqdant>27063777000151</CNPJNLiqdant>
                <IdentdPartCamr>43075534</IdentdPartCamr>
                <AgDebtd>0002</AgDebtd>
                <CtDebtd>654321</CtDebtd>
                <VlrLanc>123.0</VlrLanc>
                <TpOpLTR>0</TpOpLTR>
                <NumOpLTR>456</NumOpLTR>
                <SubTpAtv>ACI</SubTpAtv>
                <DescAtv>Test asset description</DescAtv>
                <Hist>Test description</Hist>
                <DtMovto>2026-01-28</DtMovto>
            </LTR0001>
        </SISMSG>
    </DOC>
    """
    assert normalize_xml(expected_xml) == normalize_xml(xml)


def test_ltr0001_from_xml() -> None:
    xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/SPB/LTR0001.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>31680151250908000000001</NUOp>
        </BCMSG>
        <SISMSG>
            <LTR0001>
                <CodMsg>LTR0001</CodMsg>
                <NumCtrlLTR>321</NumCtrlLTR>
                <ISPBLTR>31680153</ISPBLTR>
                <ISPBIFDebtd>31680151</ISPBIFDebtd>
                <ISPBIFCredtd>31680152</ISPBIFCredtd>
                <CNPJNLiqdant>27063777000151</CNPJNLiqdant>
                <IdentdPartCamr>43075534</IdentdPartCamr>
                <AgDebtd>0002</AgDebtd>
                <CtDebtd>654321</CtDebtd>
                <VlrLanc>123.0</VlrLanc>
                <TpOpLTR>0</TpOpLTR>
                <NumOpLTR>456</NumOpLTR>
                <SubTpAtv>ACI</SubTpAtv>
                <DescAtv>Test asset description</DescAtv>
                <Hist>Test description</Hist>
                <DtMovto>2026-01-28</DtMovto>
            </LTR0001>
        </SISMSG>
    </DOC>
    """

    ltr0001 = LTR0001.from_xml(xml)

    assert isinstance(ltr0001, LTR0001)
    assert ltr0001.from_ispb == '31680151'
    assert ltr0001.to_ispb == '00038166'
    assert ltr0001.system_domain == 'SPB01'
    assert ltr0001.operation_number == '31680151250908000000001'
    assert ltr0001.message_code == 'LTR0001'
    assert ltr0001.ltr_control_number == '321'
    assert ltr0001.ltr_ispb == '31680153'
    assert ltr0001.debtor_institution_ispb == '31680151'
    assert ltr0001.creditor_institution_ispb == '31680152'
    assert ltr0001.cnpj == '27063777000151'
    assert ltr0001.participant_identifier == '43075534'
    assert ltr0001.debtor_branch == '0002'
    assert ltr0001.debtor_account_number == '654321'
    assert ltr0001.amount == Decimal('123.0')
    assert ltr0001.ltr_operation_type == LtrOperationType.NORMAL
    assert ltr0001.ltr_operation_number == '456'
    assert ltr0001.sub_asset_type == AssetType.INVESTMENT_PORTFOLIO_ASSETS
    assert ltr0001.asset_description == 'Test asset description'
    assert ltr0001.description == 'Test description'
    assert ltr0001.settlement_date == date(2026, 1, 28)


def test_ltr0001e_general_error_from_xml() -> None:
    xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/SPB/LTR0001E.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>31680151250908000000001</NUOp>
        </BCMSG>
        <SISMSG>
            <LTR0001 CodErro="EGEN0050">
                <CodMsg>LTR0001E</CodMsg>
                <NumCtrlLTR>321</NumCtrlLTR>
                <ISPBLTR>31680153</ISPBLTR>
                <ISPBIFDebtd>31680151</ISPBIFDebtd>
                <ISPBIFCredtd>31680152</ISPBIFCredtd>
                <CNPJNLiqdant>27063777000151</CNPJNLiqdant>
                <IdentdPartCamr>43075534</IdentdPartCamr>
                <AgDebtd>0002</AgDebtd>
                <CtDebtd>654321</CtDebtd>
                <VlrLanc>123.0</VlrLanc>
                <TpOpLTR>0</TpOpLTR>
                <NumOpLTR>456</NumOpLTR>
                <SubTpAtv>ACI</SubTpAtv>
                <DescAtv>Test asset description</DescAtv>
                <Hist>Test description</Hist>
                <DtMovto>2026-01-28</DtMovto>
            </LTR0001>
        </SISMSG>
    </DOC>
    """

    ltr0001e = LTR0001E.from_xml(xml)

    assert isinstance(ltr0001e, LTR0001E)
    assert ltr0001e.from_ispb == '31680151'
    assert ltr0001e.to_ispb == '00038166'
    assert ltr0001e.system_domain == 'SPB01'
    assert ltr0001e.operation_number == '31680151250908000000001'
    assert ltr0001e.message_code == 'LTR0001E'
    assert ltr0001e.ltr_control_number == '321'
    assert ltr0001e.ltr_ispb == '31680153'
    assert ltr0001e.debtor_institution_ispb == '31680151'
    assert ltr0001e.creditor_institution_ispb == '31680152'
    assert ltr0001e.cnpj == '27063777000151'
    assert ltr0001e.participant_identifier == '43075534'
    assert ltr0001e.debtor_branch == '0002'
    assert ltr0001e.debtor_account_number == '654321'
    assert ltr0001e.amount == Decimal('123.0')
    assert ltr0001e.ltr_operation_type == LtrOperationType.NORMAL
    assert ltr0001e.ltr_operation_number == '456'
    assert ltr0001e.sub_asset_type == AssetType.INVESTMENT_PORTFOLIO_ASSETS
    assert ltr0001e.asset_description == 'Test asset description'
    assert ltr0001e.description == 'Test description'
    assert ltr0001e.settlement_date == date(2026, 1, 28)
    assert ltr0001e.general_error_code == 'EGEN0050'


def test_ltr0001e_tag_error_from_xml() -> None:
    xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/SPB/LTR0001E.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>31680151250908000000001</NUOp>
        </BCMSG>
        <SISMSG>
            <LTR0001>
                <CodMsg>LTR0001E</CodMsg>
                <NumCtrlLTR>321</NumCtrlLTR>
                <ISPBLTR CodErro="EGEN0051">31680153</ISPBLTR>
                <ISPBIFDebtd>31680151</ISPBIFDebtd>
                <ISPBIFCredtd>31680152</ISPBIFCredtd>
                <CNPJNLiqdant>27063777000151</CNPJNLiqdant>
                <IdentdPartCamr>43075534</IdentdPartCamr>
                <AgDebtd>0002</AgDebtd>
                <CtDebtd>654321</CtDebtd>
                <VlrLanc>123.0</VlrLanc>
                <TpOpLTR>0</TpOpLTR>
                <NumOpLTR>456</NumOpLTR>
                <SubTpAtv>ACI</SubTpAtv>
                <DescAtv>Test asset description</DescAtv>
                <Hist>Test description</Hist>
                <DtMovto>2026-01-28</DtMovto>
            </LTR0001>
        </SISMSG>
    </DOC>
    """

    ltr0001e = LTR0001E.from_xml(xml)

    assert isinstance(ltr0001e, LTR0001E)
    assert ltr0001e.from_ispb == '31680151'
    assert ltr0001e.to_ispb == '00038166'
    assert ltr0001e.system_domain == 'SPB01'
    assert ltr0001e.operation_number == '31680151250908000000001'
    assert ltr0001e.message_code == 'LTR0001E'
    assert ltr0001e.ltr_control_number == '321'
    assert ltr0001e.ltr_ispb == '31680153'
    assert ltr0001e.debtor_institution_ispb == '31680151'
    assert ltr0001e.creditor_institution_ispb == '31680152'
    assert ltr0001e.cnpj == '27063777000151'
    assert ltr0001e.participant_identifier == '43075534'
    assert ltr0001e.debtor_branch == '0002'
    assert ltr0001e.debtor_account_number == '654321'
    assert ltr0001e.amount == Decimal('123.0')
    assert ltr0001e.ltr_operation_type == LtrOperationType.NORMAL
    assert ltr0001e.ltr_operation_number == '456'
    assert ltr0001e.sub_asset_type == AssetType.INVESTMENT_PORTFOLIO_ASSETS
    assert ltr0001e.asset_description == 'Test asset description'
    assert ltr0001e.description == 'Test description'
    assert ltr0001e.settlement_date == date(2026, 1, 28)
    assert ltr0001e.ltr_ispb_error_code == 'EGEN0051'


def test_ltr0001_roundtrip() -> None:
    params = make_valid_ltr0001_params()

    ltr0001 = LTR0001.model_validate(params)
    xml = ltr0001.to_xml()
    ltr0001_from_xml = LTR0001.from_xml(xml)

    assert ltr0001 == ltr0001_from_xml
