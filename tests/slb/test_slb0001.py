from datetime import date
from decimal import Decimal
from typing import Any

import pytest
from pydantic import ValidationError

from sfn_messages.core.types import AccountType, PersonType
from sfn_messages.slb.slb0001 import SLB0001, SLB0001E
from sfn_messages.slb.types import SlbPurpose
from tests.conftest import extract_missing_fields, normalize_xml


def make_valid_slb0001_params() -> dict[str, Any]:
    return {
        'from_ispb': '31680151',
        'to_ispb': '00038166',
        'system_domain': 'SPB01',
        'operation_number': '31680151250908000000001',
        'message_code': 'SLB0001',
        'slb_control_number': 'SLB20250101000000001',
        'participant_ispb': '31680153',
        'original_slb_control_number': 'SLB20250101000000002',
        'partner_cnpj': '27063777000151',
        'due_date': '2026-01-29',
        'description': 'Test description',
        'amount': 1390.52,
        'slb_purpose': 'BCB_FX_PURCHASE_SPOT_CREDIT_REAIS_TO_FI',
        'branch': '0001',
        'debtor_account_type': 'CURRENT',
        'account_number': '654321',
        'debtor_type': 'BUSINESS',
        'debtor_document': '43615071000101',
        'settlement_date': '2026-01-28',
    }


def make_valid_slb0001e_params(*, general_error: bool = False) -> dict[str, Any]:
    slb0001e = {
        'from_ispb': '31680151',
        'to_ispb': '00038166',
        'system_domain': 'SPB01',
        'operation_number': '31680151250908000000001',
        'message_code': 'SLB0001E',
        'slb_control_number': 'SLB20250101000000001',
        'participant_ispb': '31680153',
        'original_slb_control_number': 'SLB20250101000000002',
        'partner_cnpj': '27063777000151',
        'due_date': '2026-01-29',
        'description': 'Test description',
        'amount': 1390.52,
        'slb_purpose': 'BCB_FX_PURCHASE_SPOT_CREDIT_REAIS_TO_FI',
        'branch': '0001',
        'debtor_account_type': 'CURRENT',
        'account_number': '654321',
        'debtor_type': 'BUSINESS',
        'debtor_document': '43615071000101',
        'settlement_date': '2026-01-28',
    }

    if general_error:
        slb0001e['general_error_code'] = 'EGEN0050'
    else:
        slb0001e['original_slb_control_number_error_code'] = 'EPCN0100'

    return slb0001e


def test_slb0001_valid_model() -> None:
    params = make_valid_slb0001_params()
    slb0001 = SLB0001.model_validate(params)

    assert isinstance(slb0001, SLB0001)
    assert slb0001.slb_control_number == 'SLB20250101000000001'
    assert slb0001.participant_ispb == '31680153'
    assert slb0001.original_slb_control_number == 'SLB20250101000000002'
    assert slb0001.partner_cnpj == '27063777000151'
    assert slb0001.due_date == date(2026, 1, 29)
    assert slb0001.description == 'Test description'
    assert slb0001.amount == Decimal('1390.52')
    assert slb0001.slb_purpose == SlbPurpose.BCB_FX_PURCHASE_SPOT_CREDIT_REAIS_TO_FI
    assert slb0001.branch == '0001'
    assert slb0001.debtor_account_type == AccountType.CURRENT
    assert slb0001.account_number == '654321'
    assert slb0001.debtor_type == PersonType.BUSINESS
    assert slb0001.debtor_document == '43615071000101'
    assert slb0001.settlement_date == date(2026, 1, 28)


def test_slb0001e_general_error_valid_model() -> None:
    params = make_valid_slb0001e_params(general_error=True)
    slb0001e = SLB0001E.model_validate(params)

    assert isinstance(slb0001e, SLB0001E)
    assert slb0001e.slb_control_number == 'SLB20250101000000001'
    assert slb0001e.participant_ispb == '31680153'
    assert slb0001e.original_slb_control_number == 'SLB20250101000000002'
    assert slb0001e.partner_cnpj == '27063777000151'
    assert slb0001e.due_date == date(2026, 1, 29)
    assert slb0001e.description == 'Test description'
    assert slb0001e.amount == Decimal('1390.52')
    assert slb0001e.slb_purpose == SlbPurpose.BCB_FX_PURCHASE_SPOT_CREDIT_REAIS_TO_FI
    assert slb0001e.branch == '0001'
    assert slb0001e.debtor_account_type == AccountType.CURRENT
    assert slb0001e.account_number == '654321'
    assert slb0001e.debtor_type == PersonType.BUSINESS
    assert slb0001e.debtor_document == '43615071000101'
    assert slb0001e.settlement_date == date(2026, 1, 28)
    assert slb0001e.general_error_code == 'EGEN0050'


def test_slb0001e_tag_error_valid_model() -> None:
    params = make_valid_slb0001e_params()
    slb0001e = SLB0001E.model_validate(params)

    assert isinstance(slb0001e, SLB0001E)
    assert slb0001e.slb_control_number == 'SLB20250101000000001'
    assert slb0001e.participant_ispb == '31680153'
    assert slb0001e.original_slb_control_number == 'SLB20250101000000002'
    assert slb0001e.partner_cnpj == '27063777000151'
    assert slb0001e.due_date == date(2026, 1, 29)
    assert slb0001e.description == 'Test description'
    assert slb0001e.amount == Decimal('1390.52')
    assert slb0001e.slb_purpose == SlbPurpose.BCB_FX_PURCHASE_SPOT_CREDIT_REAIS_TO_FI
    assert slb0001e.branch == '0001'
    assert slb0001e.debtor_account_type == AccountType.CURRENT
    assert slb0001e.account_number == '654321'
    assert slb0001e.debtor_type == PersonType.BUSINESS
    assert slb0001e.debtor_document == '43615071000101'
    assert slb0001e.settlement_date == date(2026, 1, 28)
    assert slb0001e.original_slb_control_number_error_code == 'EPCN0100'


def test_slb0001_missing_required_fields() -> None:
    with pytest.raises(ValidationError) as exc:
        SLB0001.model_validate({})

    missing_fields = extract_missing_fields(exc.value)
    assert missing_fields == {
        'from_ispb',
        'to_ispb',
        'system_domain',
        'operation_number',
        'slb_control_number',
        'participant_ispb',
        'due_date',
        'amount',
        'settlement_date',
    }


def test_slb0001_to_xml() -> None:
    params = make_valid_slb0001_params()
    slb0001 = SLB0001.model_validate(params)

    xml = slb0001.to_xml()

    expected_xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/SPB/SLB0001.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>31680151250908000000001</NUOp>
        </BCMSG>
        <SISMSG>
            <SLB0001>
                <CodMsg>SLB0001</CodMsg>
                <NumCtrlSLB>SLB20250101000000001</NumCtrlSLB>
                <ISPBPart>31680153</ISPBPart>
                <NumCtrlSLBOr>SLB20250101000000002</NumCtrlSLBOr>
                <CNPJConv>27063777000151</CNPJConv>
                <DtVenc>2026-01-29</DtVenc>
                <Hist>Test description</Hist>
                <VlrLanc>1390.52</VlrLanc>
                <FinlddSLB>CAM060164</FinlddSLB>
                <AgDebtd>0001</AgDebtd>
                <TpCtDebtd>CC</TpCtDebtd>
                <CtDebtd>654321</CtDebtd>
                <TpPessoaDebtd>J</TpPessoaDebtd>
                <CNPJ_CPFCliDebtd>43615071000101</CNPJ_CPFCliDebtd>
                <DtMovto>2026-01-28</DtMovto>
            </SLB0001>
        </SISMSG>
    </DOC>
    """
    assert normalize_xml(expected_xml) == normalize_xml(xml)


def test_slb0001e_general_error_to_xml() -> None:
    params = make_valid_slb0001e_params(general_error=True)
    slb0001e = SLB0001E.model_validate(params)

    xml = slb0001e.to_xml()

    expected_xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/SPB/SLB0001E.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>31680151250908000000001</NUOp>
        </BCMSG>
        <SISMSG>
            <SLB0001 CodErro="EGEN0050">
                <CodMsg>SLB0001E</CodMsg>
                <NumCtrlSLB>SLB20250101000000001</NumCtrlSLB>
                <ISPBPart>31680153</ISPBPart>
                <NumCtrlSLBOr>SLB20250101000000002</NumCtrlSLBOr>
                <CNPJConv>27063777000151</CNPJConv>
                <DtVenc>2026-01-29</DtVenc>
                <Hist>Test description</Hist>
                <VlrLanc>1390.52</VlrLanc>
                <FinlddSLB>CAM060164</FinlddSLB>
                <AgDebtd>0001</AgDebtd>
                <TpCtDebtd>CC</TpCtDebtd>
                <CtDebtd>654321</CtDebtd>
                <TpPessoaDebtd>J</TpPessoaDebtd>
                <CNPJ_CPFCliDebtd>43615071000101</CNPJ_CPFCliDebtd>
                <DtMovto>2026-01-28</DtMovto>
            </SLB0001>
        </SISMSG>
    </DOC>
    """
    assert normalize_xml(expected_xml) == normalize_xml(xml)


def test_slb0001e_tag_error_to_xml() -> None:
    params = make_valid_slb0001e_params()
    slb0001e = SLB0001E.model_validate(params)

    xml = slb0001e.to_xml()

    expected_xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/SPB/SLB0001E.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>31680151250908000000001</NUOp>
        </BCMSG>
        <SISMSG>
            <SLB0001>
                <CodMsg>SLB0001E</CodMsg>
                <NumCtrlSLB>SLB20250101000000001</NumCtrlSLB>
                <ISPBPart>31680153</ISPBPart>
                <NumCtrlSLBOr CodErro="EPCN0100">SLB20250101000000002</NumCtrlSLBOr>
                <CNPJConv>27063777000151</CNPJConv>
                <DtVenc>2026-01-29</DtVenc>
                <Hist>Test description</Hist>
                <VlrLanc>1390.52</VlrLanc>
                <FinlddSLB>CAM060164</FinlddSLB>
                <AgDebtd>0001</AgDebtd>
                <TpCtDebtd>CC</TpCtDebtd>
                <CtDebtd>654321</CtDebtd>
                <TpPessoaDebtd>J</TpPessoaDebtd>
                <CNPJ_CPFCliDebtd>43615071000101</CNPJ_CPFCliDebtd>
                <DtMovto>2026-01-28</DtMovto>
            </SLB0001>
        </SISMSG>
    </DOC>
    """
    assert normalize_xml(expected_xml) == normalize_xml(xml)


def test_slb0001_from_xml() -> None:
    xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/SPB/SLB0001.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>31680151250908000000001</NUOp>
        </BCMSG>
        <SISMSG>
            <SLB0001>
                <CodMsg>SLB0001</CodMsg>
                <NumCtrlSLB>SLB20250101000000001</NumCtrlSLB>
                <ISPBPart>31680153</ISPBPart>
                <NumCtrlSLBOr>SLB20250101000000002</NumCtrlSLBOr>
                <CNPJConv>27063777000151</CNPJConv>
                <DtVenc>2026-01-29</DtVenc>
                <Hist>Test description</Hist>
                <VlrLanc>1390.52</VlrLanc>
                <FinlddSLB>CAM060164</FinlddSLB>
                <AgDebtd>0001</AgDebtd>
                <TpCtDebtd>CC</TpCtDebtd>
                <CtDebtd>654321</CtDebtd>
                <TpPessoaDebtd>J</TpPessoaDebtd>
                <CNPJ_CPFCliDebtd>43615071000101</CNPJ_CPFCliDebtd>
                <DtMovto>2026-01-28</DtMovto>
            </SLB0001>
        </SISMSG>
    </DOC>
    """

    slb0001 = SLB0001.from_xml(xml)

    assert isinstance(slb0001, SLB0001)
    assert slb0001.slb_control_number == 'SLB20250101000000001'
    assert slb0001.participant_ispb == '31680153'
    assert slb0001.original_slb_control_number == 'SLB20250101000000002'
    assert slb0001.partner_cnpj == '27063777000151'
    assert slb0001.due_date == date(2026, 1, 29)
    assert slb0001.description == 'Test description'
    assert slb0001.amount == Decimal('1390.52')
    assert slb0001.slb_purpose == SlbPurpose.BCB_FX_PURCHASE_SPOT_CREDIT_REAIS_TO_FI
    assert slb0001.branch == '0001'
    assert slb0001.debtor_account_type == AccountType.CURRENT
    assert slb0001.account_number == '654321'
    assert slb0001.debtor_type == PersonType.BUSINESS
    assert slb0001.debtor_document == '43615071000101'
    assert slb0001.settlement_date == date(2026, 1, 28)


def test_slb0001e_general_error_from_xml() -> None:
    xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/SPB/SLB0001E.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>31680151250908000000001</NUOp>
        </BCMSG>
        <SISMSG>
            <SLB0001 CodErro="EGEN0050">
                <CodMsg>SLB0001E</CodMsg>
                <NumCtrlSLB>SLB20250101000000001</NumCtrlSLB>
                <ISPBPart>31680153</ISPBPart>
                <NumCtrlSLBOr>SLB20250101000000002</NumCtrlSLBOr>
                <CNPJConv>27063777000151</CNPJConv>
                <DtVenc>2026-01-29</DtVenc>
                <Hist>Test description</Hist>
                <VlrLanc>1390.52</VlrLanc>
                <FinlddSLB>CAM060164</FinlddSLB>
                <AgDebtd>0001</AgDebtd>
                <TpCtDebtd>CC</TpCtDebtd>
                <CtDebtd>654321</CtDebtd>
                <TpPessoaDebtd>J</TpPessoaDebtd>
                <CNPJ_CPFCliDebtd>43615071000101</CNPJ_CPFCliDebtd>
                <DtMovto>2026-01-28</DtMovto>
            </SLB0001>
        </SISMSG>
    </DOC>
    """

    slb0001e = SLB0001E.from_xml(xml)

    assert isinstance(slb0001e, SLB0001E)
    assert slb0001e.slb_control_number == 'SLB20250101000000001'
    assert slb0001e.participant_ispb == '31680153'
    assert slb0001e.original_slb_control_number == 'SLB20250101000000002'
    assert slb0001e.partner_cnpj == '27063777000151'
    assert slb0001e.due_date == date(2026, 1, 29)
    assert slb0001e.description == 'Test description'
    assert slb0001e.amount == Decimal('1390.52')
    assert slb0001e.slb_purpose == SlbPurpose.BCB_FX_PURCHASE_SPOT_CREDIT_REAIS_TO_FI
    assert slb0001e.branch == '0001'
    assert slb0001e.debtor_account_type == AccountType.CURRENT
    assert slb0001e.account_number == '654321'
    assert slb0001e.debtor_type == PersonType.BUSINESS
    assert slb0001e.debtor_document == '43615071000101'
    assert slb0001e.settlement_date == date(2026, 1, 28)
    assert slb0001e.general_error_code == 'EGEN0050'


def test_slb0001e_tag_error_from_xml() -> None:
    xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/SPB/SLB0001E.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>31680151250908000000001</NUOp>
        </BCMSG>
        <SISMSG>
            <SLB0001>
                <CodMsg>SLB0001E</CodMsg>
                <NumCtrlSLB>SLB20250101000000001</NumCtrlSLB>
                <ISPBPart>31680153</ISPBPart>
                <NumCtrlSLBOr CodErro="EPCN0100">SLB20250101000000002</NumCtrlSLBOr>
                <CNPJConv>27063777000151</CNPJConv>
                <DtVenc>2026-01-29</DtVenc>
                <Hist>Test description</Hist>
                <VlrLanc>1390.52</VlrLanc>
                <FinlddSLB>CAM060164</FinlddSLB>
                <AgDebtd>0001</AgDebtd>
                <TpCtDebtd>CC</TpCtDebtd>
                <CtDebtd>654321</CtDebtd>
                <TpPessoaDebtd>J</TpPessoaDebtd>
                <CNPJ_CPFCliDebtd>43615071000101</CNPJ_CPFCliDebtd>
                <DtMovto>2026-01-28</DtMovto>
            </SLB0001>
        </SISMSG>
    </DOC>
    """
    slb0001e = SLB0001E.from_xml(xml)

    assert isinstance(slb0001e, SLB0001E)
    assert slb0001e.slb_control_number == 'SLB20250101000000001'
    assert slb0001e.participant_ispb == '31680153'
    assert slb0001e.original_slb_control_number == 'SLB20250101000000002'
    assert slb0001e.partner_cnpj == '27063777000151'
    assert slb0001e.due_date == date(2026, 1, 29)
    assert slb0001e.description == 'Test description'
    assert slb0001e.amount == Decimal('1390.52')
    assert slb0001e.slb_purpose == SlbPurpose.BCB_FX_PURCHASE_SPOT_CREDIT_REAIS_TO_FI
    assert slb0001e.branch == '0001'
    assert slb0001e.debtor_account_type == AccountType.CURRENT
    assert slb0001e.account_number == '654321'
    assert slb0001e.debtor_type == PersonType.BUSINESS
    assert slb0001e.debtor_document == '43615071000101'
    assert slb0001e.settlement_date == date(2026, 1, 28)
    assert slb0001e.original_slb_control_number_error_code == 'EPCN0100'


def test_slb0001_roundtrip() -> None:
    params = make_valid_slb0001_params()

    slb0001 = SLB0001.model_validate(params)
    xml = slb0001.to_xml()
    slb0001_from_xml = SLB0001.from_xml(xml)

    assert slb0001 == slb0001_from_xml


def test_slb0001_from_xml_missing_required_fields() -> None:
    xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/SPB/SLB0001.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>31680151250908000000001</NUOp>
        </BCMSG>
        <SISMSG>
            <SLB0001>
                <CodMsg>SLB0001</CodMsg>
                <NivelPref>B</NivelPref>
            </SLB0001>
        </SISMSG>
    </DOC>
    """

    with pytest.raises(ValidationError) as exc:
        SLB0001.from_xml(xml)

    missing_fields = extract_missing_fields(exc.value)
    assert missing_fields == {
        'slb_control_number',
        'participant_ispb',
        'due_date',
        'amount',
        'settlement_date',
    }
