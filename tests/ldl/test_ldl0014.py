from datetime import date, datetime
from decimal import Decimal
from typing import Any

import pytest
from pydantic import ValidationError

from sfn_messages.core.types import LdlSettlementStatus
from sfn_messages.ldl.ldl0014 import (
    LDL0014,
    LDL0014E,
    LDL0014R1,
    LDL0014R2,
    DepositGroup,
    DepositGroupError,
    DepositGroupR2,
)
from tests.conftest import extract_missing_fields, normalize_xml

DEPOSIT_GROUP_SIZE = 2


def make_valid_ldl0014_params() -> dict[str, Any]:
    return {
        'from_ispb': '31680151',
        'to_ispb': '00038166',
        'system_domain': 'SPB01',
        'operation_number': '31680151250908000000001',
        'message_code': 'LDL0014',
        'institution_control_number': '123',
        'original_ldl_control_number': '321',
        'institution_ispb': '31680151',
        'ldl_ispb': '31680153',
        'amount': 188.0,
        'deposit_group': [
            {
                'cnpj': '50214141000185',
                'participant_identifier': '55386424',
                'amount': 100.0,
                'original_ldl_acceptance_control_number': '312',
                'original_if_request_control_number': '323',
            },
            {
                'cnpj': '53753940000118',
                'participant_identifier': '43075534',
                'amount': 88.0,
                'original_ldl_acceptance_control_number': '132',
                'original_if_request_control_number': '322',
            },
        ],
        'settlement_date': '2025-12-10',
    }


def make_valid_ldl0014r1_params() -> dict[str, Any]:
    return {
        'from_ispb': '31680151',
        'to_ispb': '00038166',
        'system_domain': 'SPB01',
        'operation_number': '31680151250908000000001',
        'message_code': 'LDL0014R1',
        'institution_control_number': '123',
        'institution_ispb': '31680151',
        'str_control_number': 'STR20250101000000001',
        'ldl_settlement_status': 'EFFECTIVE',
        'settlement_timestamp': '2025-12-10T15:30:00',
        'settlement_date': '2025-12-10',
    }


def make_valid_ldl0014r2_params() -> dict[str, Any]:
    return {
        'from_ispb': '31680151',
        'to_ispb': '00038166',
        'system_domain': 'SPB01',
        'operation_number': '31680151250908000000001',
        'message_code': 'LDL0014R2',
        'str_control_number': 'STR20250101000000001',
        'vendor_timestamp': '2025-12-10T15:30:00',
        'original_ldl_control_number': '321',
        'institution_ispb': '31680151',
        'ldl_ispb': '31680153',
        'amount': 188.0,
        'deposit_group': [
            {
                'cnpj': '50214141000185',
                'participant_identifier': '55386424',
                'amount': 100.0,
                'original_ldl_acceptance_control_number': '312',
            },
            {
                'cnpj': '53753940000118',
                'participant_identifier': '43075534',
                'amount': 88.0,
                'original_ldl_acceptance_control_number': '132',
            },
        ],
        'settlement_date': '2025-12-10',
    }


def make_valid_ldl0014e_params(*, general_error: bool = False) -> dict[str, Any]:
    ldl0014e: dict[str, Any] = {
        'from_ispb': '31680151',
        'to_ispb': '00038166',
        'system_domain': 'SPB01',
        'operation_number': '31680151250908000000001',
        'message_code': 'LDL0014E',
        'institution_control_number': '123',
        'original_ldl_control_number': '321',
        'institution_ispb': '31680151',
        'ldl_ispb': '31680153',
        'amount': 188.0,
        'deposit_group': [
            {
                'cnpj': '50214141000185',
                'participant_identifier': '55386424',
                'amount': 100.0,
                'original_ldl_acceptance_control_number': '312',
                'original_if_request_control_number': '323',
            },
            {
                'cnpj': '53753940000118',
                'participant_identifier': '43075534',
                'amount': 88.0,
                'original_ldl_acceptance_control_number': '132',
                'original_if_request_control_number': '322',
            },
        ],
        'settlement_date': '2025-12-10',
    }

    if general_error:
        ldl0014e['general_error_code'] = 'EGEN0050'
    else:
        ldl0014e['ldl_ispb_error_code'] = 'EGEN0051'
        ldl0014e['deposit_group'][1]['participant_identifier_error_code'] = 'ELDL0019'

    return ldl0014e


def test_ldl0014_valid_model() -> None:
    params = make_valid_ldl0014_params()
    ldl0014 = LDL0014.model_validate(params)

    assert isinstance(ldl0014, LDL0014)
    assert ldl0014.from_ispb == '31680151'
    assert ldl0014.to_ispb == '00038166'
    assert ldl0014.system_domain == 'SPB01'
    assert ldl0014.operation_number == '31680151250908000000001'
    assert ldl0014.message_code == 'LDL0014'
    assert ldl0014.institution_control_number == '123'
    assert ldl0014.original_ldl_control_number == '321'
    assert ldl0014.institution_ispb == '31680151'
    assert ldl0014.ldl_ispb == '31680153'
    assert ldl0014.amount == Decimal('188.0')
    assert ldl0014.settlement_date == date(2025, 12, 10)

    assert len(ldl0014.deposit_group) == DEPOSIT_GROUP_SIZE
    deposit1 = ldl0014.deposit_group[0]
    deposit2 = ldl0014.deposit_group[1]
    assert isinstance(deposit1, DepositGroup)
    assert deposit1.cnpj == '50214141000185'
    assert deposit1.participant_identifier == '55386424'
    assert deposit1.amount == Decimal('100.0')
    assert deposit1.original_ldl_acceptance_control_number == '312'
    assert deposit1.original_if_request_control_number == '323'
    assert isinstance(deposit2, DepositGroup)
    assert deposit2.cnpj == '53753940000118'
    assert deposit2.participant_identifier == '43075534'
    assert deposit2.amount == Decimal('88.0')
    assert deposit2.original_ldl_acceptance_control_number == '132'
    assert deposit2.original_if_request_control_number == '322'


def test_ldl0014r1_valid_model() -> None:
    params = make_valid_ldl0014r1_params()
    ldl0014r1 = LDL0014R1.model_validate(params)

    assert isinstance(ldl0014r1, LDL0014R1)
    assert ldl0014r1.from_ispb == '31680151'
    assert ldl0014r1.to_ispb == '00038166'
    assert ldl0014r1.system_domain == 'SPB01'
    assert ldl0014r1.operation_number == '31680151250908000000001'
    assert ldl0014r1.message_code == 'LDL0014R1'
    assert ldl0014r1.institution_control_number == '123'
    assert ldl0014r1.institution_ispb == '31680151'
    assert ldl0014r1.str_control_number == 'STR20250101000000001'
    assert ldl0014r1.ldl_settlement_status == LdlSettlementStatus.EFFECTIVE
    assert ldl0014r1.settlement_timestamp == datetime(2025, 12, 10, 15, 30)
    assert ldl0014r1.settlement_date == date(2025, 12, 10)


def test_ldl0014r2_valid_model() -> None:
    params = make_valid_ldl0014r2_params()
    ldl0014r2 = LDL0014R2.model_validate(params)

    assert isinstance(ldl0014r2, LDL0014R2)
    assert ldl0014r2.from_ispb == '31680151'
    assert ldl0014r2.to_ispb == '00038166'
    assert ldl0014r2.system_domain == 'SPB01'
    assert ldl0014r2.operation_number == '31680151250908000000001'
    assert ldl0014r2.message_code == 'LDL0014R2'
    assert ldl0014r2.str_control_number == 'STR20250101000000001'
    assert ldl0014r2.vendor_timestamp == datetime(2025, 12, 10, 15, 30)
    assert ldl0014r2.original_ldl_control_number == '321'
    assert ldl0014r2.institution_ispb == '31680151'
    assert ldl0014r2.ldl_ispb == '31680153'
    assert ldl0014r2.amount == Decimal('188.0')
    assert ldl0014r2.settlement_date == date(2025, 12, 10)

    assert len(ldl0014r2.deposit_group) == DEPOSIT_GROUP_SIZE
    deposit1 = ldl0014r2.deposit_group[0]
    deposit2 = ldl0014r2.deposit_group[1]
    assert isinstance(deposit1, DepositGroupR2)
    assert deposit1.cnpj == '50214141000185'
    assert deposit1.participant_identifier == '55386424'
    assert deposit1.amount == Decimal('100.0')
    assert deposit1.original_ldl_acceptance_control_number == '312'
    assert isinstance(deposit2, DepositGroupR2)
    assert deposit2.cnpj == '53753940000118'
    assert deposit2.participant_identifier == '43075534'
    assert deposit2.amount == Decimal('88.0')
    assert deposit2.original_ldl_acceptance_control_number == '132'


def test_ldl0014e_general_error_valid_model() -> None:
    params = make_valid_ldl0014e_params(general_error=True)
    ldl0014e = LDL0014E.model_validate(params)

    assert isinstance(ldl0014e, LDL0014E)
    assert ldl0014e.from_ispb == '31680151'
    assert ldl0014e.to_ispb == '00038166'
    assert ldl0014e.system_domain == 'SPB01'
    assert ldl0014e.operation_number == '31680151250908000000001'
    assert ldl0014e.message_code == 'LDL0014E'
    assert ldl0014e.institution_control_number == '123'
    assert ldl0014e.original_ldl_control_number == '321'
    assert ldl0014e.institution_ispb == '31680151'
    assert ldl0014e.ldl_ispb == '31680153'
    assert ldl0014e.amount == Decimal('188.0')
    assert ldl0014e.settlement_date == date(2025, 12, 10)
    assert ldl0014e.general_error_code == 'EGEN0050'

    assert len(ldl0014e.deposit_group) == DEPOSIT_GROUP_SIZE
    deposit1 = ldl0014e.deposit_group[0]
    deposit2 = ldl0014e.deposit_group[1]
    assert isinstance(deposit1, DepositGroupError)
    assert deposit1.cnpj == '50214141000185'
    assert deposit1.participant_identifier == '55386424'
    assert deposit1.amount == Decimal('100.0')
    assert deposit1.original_ldl_acceptance_control_number == '312'
    assert deposit1.original_if_request_control_number == '323'
    assert isinstance(deposit2, DepositGroupError)
    assert deposit2.cnpj == '53753940000118'
    assert deposit2.participant_identifier == '43075534'
    assert deposit2.amount == Decimal('88.0')
    assert deposit2.original_ldl_acceptance_control_number == '132'
    assert deposit2.original_if_request_control_number == '322'


def test_ldl0014e_tag_error_valid_model() -> None:
    params = make_valid_ldl0014e_params()
    ldl0014e = LDL0014E.model_validate(params)

    assert isinstance(ldl0014e, LDL0014E)
    assert ldl0014e.from_ispb == '31680151'
    assert ldl0014e.to_ispb == '00038166'
    assert ldl0014e.system_domain == 'SPB01'
    assert ldl0014e.operation_number == '31680151250908000000001'
    assert ldl0014e.message_code == 'LDL0014E'
    assert ldl0014e.institution_control_number == '123'
    assert ldl0014e.original_ldl_control_number == '321'
    assert ldl0014e.institution_ispb == '31680151'
    assert ldl0014e.ldl_ispb == '31680153'
    assert ldl0014e.amount == Decimal('188.0')
    assert ldl0014e.settlement_date == date(2025, 12, 10)
    assert ldl0014e.ldl_ispb_error_code == 'EGEN0051'

    assert len(ldl0014e.deposit_group) == DEPOSIT_GROUP_SIZE
    deposit1 = ldl0014e.deposit_group[0]
    deposit2 = ldl0014e.deposit_group[1]
    assert isinstance(deposit1, DepositGroupError)
    assert deposit1.cnpj == '50214141000185'
    assert deposit1.participant_identifier == '55386424'
    assert deposit1.amount == Decimal('100.0')
    assert deposit1.original_ldl_acceptance_control_number == '312'
    assert deposit1.original_if_request_control_number == '323'
    assert isinstance(deposit2, DepositGroupError)
    assert deposit2.cnpj == '53753940000118'
    assert deposit2.participant_identifier == '43075534'
    assert deposit2.amount == Decimal('88.0')
    assert deposit2.original_ldl_acceptance_control_number == '132'
    assert deposit2.original_if_request_control_number == '322'
    assert deposit2.participant_identifier_error_code == 'ELDL0019'


def test_ldl0014_missing_required_fields() -> None:
    with pytest.raises(ValidationError) as exc:
        LDL0014.model_validate({})

    missing_fields = extract_missing_fields(exc.value)
    assert missing_fields == {
        'from_ispb',
        'to_ispb',
        'system_domain',
        'operation_number',
        'institution_control_number',
        'original_ldl_control_number',
        'institution_ispb',
        'ldl_ispb',
        'amount',
        'settlement_date',
    }


def test_ldl0014r1_missing_required_fields() -> None:
    with pytest.raises(ValidationError) as exc:
        LDL0014R1.model_validate({})

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


def test_ldl0014r2_missing_required_fields() -> None:
    with pytest.raises(ValidationError) as exc:
        LDL0014R2.model_validate({})

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
        'ldl_ispb',
        'amount',
        'settlement_date',
    }


def test_ldl0014_to_xml() -> None:
    params = make_valid_ldl0014_params()
    ldl0014 = LDL0014.model_validate(params)

    xml = ldl0014.to_xml()

    expected_xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/SPB/LDL0014.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>31680151250908000000001</NUOp>
        </BCMSG>
        <SISMSG>
            <LDL0014>
                <CodMsg>LDL0014</CodMsg>
                <NumCtrlIF>123</NumCtrlIF>
                <NumCtrlLDLOr>321</NumCtrlLDLOr>
                <ISPBIF>31680151</ISPBIF>
                <ISPBLDL>31680153</ISPBLDL>
                <VlrLanc>188.0</VlrLanc>
                <Grupo_LDL0014_Dep>
                    <CNPJNLiqdant>50214141000185</CNPJNLiqdant>
                    <IdentdPartCamr>55386424</IdentdPartCamr>
                    <VlrNLiqdant>100.0</VlrNLiqdant>
                    <NumCtrlActeLDLOr>312</NumCtrlActeLDLOr>
                    <NumCtrlReqIFOr>323</NumCtrlReqIFOr>
                </Grupo_LDL0014_Dep>
                <Grupo_LDL0014_Dep>
                    <CNPJNLiqdant>53753940000118</CNPJNLiqdant>
                    <IdentdPartCamr>43075534</IdentdPartCamr>
                    <VlrNLiqdant>88.0</VlrNLiqdant>
                    <NumCtrlActeLDLOr>132</NumCtrlActeLDLOr>
                    <NumCtrlReqIFOr>322</NumCtrlReqIFOr>
                </Grupo_LDL0014_Dep>
                <DtMovto>2025-12-10</DtMovto>
            </LDL0014>
        </SISMSG>
    </DOC>
    """
    assert normalize_xml(expected_xml) == normalize_xml(xml)


def test_ldl0014r1_to_xml() -> None:
    params = make_valid_ldl0014r1_params()
    ldl0014r1 = LDL0014R1.model_validate(params)

    xml = ldl0014r1.to_xml()

    expected_xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/SPB/LDL0014.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>31680151250908000000001</NUOp>
        </BCMSG>
        <SISMSG>
            <LDL0014R1>
                <CodMsg>LDL0014R1</CodMsg>
                <NumCtrlIF>123</NumCtrlIF>
                <ISPBIF>31680151</ISPBIF>
                <NumCtrlSTR>STR20250101000000001</NumCtrlSTR>
                <SitLancLDL>1</SitLancLDL>
                <DtHrSit>2025-12-10T15:30:00</DtHrSit>
                <DtMovto>2025-12-10</DtMovto>
            </LDL0014R1>
        </SISMSG>
    </DOC>
    """
    assert normalize_xml(expected_xml) == normalize_xml(xml)


def test_ldl0014r2_to_xml() -> None:
    params = make_valid_ldl0014r2_params()
    ldl0014r2 = LDL0014R2.model_validate(params)

    xml = ldl0014r2.to_xml()

    expected_xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/SPB/LDL0014.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>31680151250908000000001</NUOp>
        </BCMSG>
        <SISMSG>
            <LDL0014R2>
                <CodMsg>LDL0014R2</CodMsg>
                <NumCtrlSTR>STR20250101000000001</NumCtrlSTR>
                <DtHrBC>2025-12-10T15:30:00</DtHrBC>
                <NumCtrlLDLOr>321</NumCtrlLDLOr>
                <ISPBIF>31680151</ISPBIF>
                <ISPBLDL>31680153</ISPBLDL>
                <VlrLanc>188.0</VlrLanc>
                <Grupo_LDL0014R2_Dep>
                    <CNPJNLiqdant>50214141000185</CNPJNLiqdant>
                    <IdentdPartCamr>55386424</IdentdPartCamr>
                    <VlrNLiqdant>100.0</VlrNLiqdant>
                    <NumCtrlActeLDLOr>312</NumCtrlActeLDLOr>
                </Grupo_LDL0014R2_Dep>
                <Grupo_LDL0014R2_Dep>
                    <CNPJNLiqdant>53753940000118</CNPJNLiqdant>
                    <IdentdPartCamr>43075534</IdentdPartCamr>
                    <VlrNLiqdant>88.0</VlrNLiqdant>
                    <NumCtrlActeLDLOr>132</NumCtrlActeLDLOr>
                </Grupo_LDL0014R2_Dep>
                <DtMovto>2025-12-10</DtMovto>
            </LDL0014R2>
        </SISMSG>
    </DOC>
    """
    assert normalize_xml(expected_xml) == normalize_xml(xml)


def test_ldl0014e_general_error_to_xml() -> None:
    params = make_valid_ldl0014e_params(general_error=True)
    ldl0014e = LDL0014E.model_validate(params)

    xml = ldl0014e.to_xml()

    expected_xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/SPB/LDL0014E.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>31680151250908000000001</NUOp>
        </BCMSG>
        <SISMSG>
            <LDL0014 CodErro="EGEN0050">
                <CodMsg>LDL0014E</CodMsg>
                <NumCtrlIF>123</NumCtrlIF>
                <NumCtrlLDLOr>321</NumCtrlLDLOr>
                <ISPBIF>31680151</ISPBIF>
                <ISPBLDL>31680153</ISPBLDL>
                <VlrLanc>188.0</VlrLanc>
                <Grupo_LDL0014_Dep>
                    <CNPJNLiqdant>50214141000185</CNPJNLiqdant>
                    <IdentdPartCamr>55386424</IdentdPartCamr>
                    <VlrNLiqdant>100.0</VlrNLiqdant>
                    <NumCtrlActeLDLOr>312</NumCtrlActeLDLOr>
                    <NumCtrlReqIFOr>323</NumCtrlReqIFOr>
                </Grupo_LDL0014_Dep>
                <Grupo_LDL0014_Dep>
                    <CNPJNLiqdant>53753940000118</CNPJNLiqdant>
                    <IdentdPartCamr>43075534</IdentdPartCamr>
                    <VlrNLiqdant>88.0</VlrNLiqdant>
                    <NumCtrlActeLDLOr>132</NumCtrlActeLDLOr>
                    <NumCtrlReqIFOr>322</NumCtrlReqIFOr>
                </Grupo_LDL0014_Dep>
                <DtMovto>2025-12-10</DtMovto>
            </LDL0014>
        </SISMSG>
    </DOC>
    """
    assert normalize_xml(expected_xml) == normalize_xml(xml)


def test_ldl0014e_tag_error_to_xml() -> None:
    params = make_valid_ldl0014e_params()
    ldl0014e = LDL0014E.model_validate(params)

    xml = ldl0014e.to_xml()

    expected_xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/SPB/LDL0014E.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>31680151250908000000001</NUOp>
        </BCMSG>
        <SISMSG>
            <LDL0014>
                <CodMsg>LDL0014E</CodMsg>
                <NumCtrlIF>123</NumCtrlIF>
                <NumCtrlLDLOr>321</NumCtrlLDLOr>
                <ISPBIF>31680151</ISPBIF>
                <ISPBLDL CodErro="EGEN0051">31680153</ISPBLDL>
                <VlrLanc>188.0</VlrLanc>
                <Grupo_LDL0014_Dep>
                    <CNPJNLiqdant>50214141000185</CNPJNLiqdant>
                    <IdentdPartCamr>55386424</IdentdPartCamr>
                    <VlrNLiqdant>100.0</VlrNLiqdant>
                    <NumCtrlActeLDLOr>312</NumCtrlActeLDLOr>
                    <NumCtrlReqIFOr>323</NumCtrlReqIFOr>
                </Grupo_LDL0014_Dep>
                <Grupo_LDL0014_Dep>
                    <CNPJNLiqdant>53753940000118</CNPJNLiqdant>
                    <IdentdPartCamr CodErro="ELDL0019">43075534</IdentdPartCamr>
                    <VlrNLiqdant>88.0</VlrNLiqdant>
                    <NumCtrlActeLDLOr>132</NumCtrlActeLDLOr>
                    <NumCtrlReqIFOr>322</NumCtrlReqIFOr>
                </Grupo_LDL0014_Dep>
                <DtMovto>2025-12-10</DtMovto>
            </LDL0014>
        </SISMSG>
    </DOC>
    """
    assert normalize_xml(expected_xml) == normalize_xml(xml)


def test_ldl0014_from_xml() -> None:
    xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/SPB/LDL0014.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>31680151250908000000001</NUOp>
        </BCMSG>
        <SISMSG>
            <LDL0014>
                <CodMsg>LDL0014</CodMsg>
                <NumCtrlIF>123</NumCtrlIF>
                <NumCtrlLDLOr>321</NumCtrlLDLOr>
                <ISPBIF>31680151</ISPBIF>
                <ISPBLDL>31680153</ISPBLDL>
                <VlrLanc>188.0</VlrLanc>
                <Grupo_LDL0014_Dep>
                    <CNPJNLiqdant>50214141000185</CNPJNLiqdant>
                    <IdentdPartCamr>55386424</IdentdPartCamr>
                    <VlrNLiqdant>100.0</VlrNLiqdant>
                    <NumCtrlActeLDLOr>312</NumCtrlActeLDLOr>
                    <NumCtrlReqIFOr>323</NumCtrlReqIFOr>
                </Grupo_LDL0014_Dep>
                <Grupo_LDL0014_Dep>
                    <CNPJNLiqdant>53753940000118</CNPJNLiqdant>
                    <IdentdPartCamr>43075534</IdentdPartCamr>
                    <VlrNLiqdant>88.0</VlrNLiqdant>
                    <NumCtrlActeLDLOr>132</NumCtrlActeLDLOr>
                    <NumCtrlReqIFOr>322</NumCtrlReqIFOr>
                </Grupo_LDL0014_Dep>
                <DtMovto>2025-12-10</DtMovto>
            </LDL0014>
        </SISMSG>
    </DOC>
    """

    ldl0014 = LDL0014.from_xml(xml)

    assert isinstance(ldl0014, LDL0014)
    assert ldl0014.from_ispb == '31680151'
    assert ldl0014.to_ispb == '00038166'
    assert ldl0014.system_domain == 'SPB01'
    assert ldl0014.operation_number == '31680151250908000000001'
    assert ldl0014.message_code == 'LDL0014'
    assert ldl0014.institution_control_number == '123'
    assert ldl0014.original_ldl_control_number == '321'
    assert ldl0014.institution_ispb == '31680151'
    assert ldl0014.ldl_ispb == '31680153'
    assert ldl0014.amount == Decimal('188.0')
    assert ldl0014.settlement_date == date(2025, 12, 10)

    assert len(ldl0014.deposit_group) == DEPOSIT_GROUP_SIZE
    deposit1 = ldl0014.deposit_group[0]
    deposit2 = ldl0014.deposit_group[1]
    assert isinstance(deposit1, DepositGroup)
    assert deposit1.cnpj == '50214141000185'
    assert deposit1.participant_identifier == '55386424'
    assert deposit1.amount == Decimal('100.0')
    assert deposit1.original_ldl_acceptance_control_number == '312'
    assert deposit1.original_if_request_control_number == '323'
    assert isinstance(deposit2, DepositGroup)
    assert deposit2.cnpj == '53753940000118'
    assert deposit2.participant_identifier == '43075534'
    assert deposit2.amount == Decimal('88.0')
    assert deposit2.original_ldl_acceptance_control_number == '132'
    assert deposit2.original_if_request_control_number == '322'


def test_ldl0014r1_from_xml() -> None:
    xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/SPB/LDL0014.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>31680151250908000000001</NUOp>
        </BCMSG>
        <SISMSG>
            <LDL0014R1>
                <CodMsg>LDL0014R1</CodMsg>
                <NumCtrlIF>123</NumCtrlIF>
                <ISPBIF>31680151</ISPBIF>
                <NumCtrlSTR>STR20250101000000001</NumCtrlSTR>
                <SitLancLDL>1</SitLancLDL>
                <DtHrSit>2025-12-10T15:30:00</DtHrSit>
                <DtMovto>2025-12-10</DtMovto>
            </LDL0014R1>
        </SISMSG>
    </DOC>
    """

    ldl0014r1 = LDL0014R1.from_xml(xml)

    assert isinstance(ldl0014r1, LDL0014R1)
    assert ldl0014r1.from_ispb == '31680151'
    assert ldl0014r1.to_ispb == '00038166'
    assert ldl0014r1.system_domain == 'SPB01'
    assert ldl0014r1.operation_number == '31680151250908000000001'
    assert ldl0014r1.message_code == 'LDL0014R1'
    assert ldl0014r1.institution_control_number == '123'
    assert ldl0014r1.institution_ispb == '31680151'
    assert ldl0014r1.str_control_number == 'STR20250101000000001'
    assert ldl0014r1.ldl_settlement_status == LdlSettlementStatus.EFFECTIVE
    assert ldl0014r1.settlement_timestamp == datetime(2025, 12, 10, 15, 30)
    assert ldl0014r1.settlement_date == date(2025, 12, 10)


def test_ldl0014r2_from_xml() -> None:
    xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/SPB/LDL0014.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>31680151250908000000001</NUOp>
        </BCMSG>
        <SISMSG>
            <LDL0014R2>
                <CodMsg>LDL0014R2</CodMsg>
                <NumCtrlSTR>STR20250101000000001</NumCtrlSTR>
                <DtHrBC>2025-12-10T15:30:00</DtHrBC>
                <NumCtrlLDLOr>321</NumCtrlLDLOr>
                <ISPBIF>31680151</ISPBIF>
                <ISPBLDL>31680153</ISPBLDL>
                <VlrLanc>188.0</VlrLanc>
                <Grupo_LDL0014R2_Dep>
                    <CNPJNLiqdant>50214141000185</CNPJNLiqdant>
                    <IdentdPartCamr>55386424</IdentdPartCamr>
                    <VlrNLiqdant>100.0</VlrNLiqdant>
                    <NumCtrlActeLDLOr>312</NumCtrlActeLDLOr>
                </Grupo_LDL0014R2_Dep>
                <Grupo_LDL0014R2_Dep>
                    <CNPJNLiqdant>53753940000118</CNPJNLiqdant>
                    <IdentdPartCamr>43075534</IdentdPartCamr>
                    <VlrNLiqdant>88.0</VlrNLiqdant>
                    <NumCtrlActeLDLOr>132</NumCtrlActeLDLOr>
                </Grupo_LDL0014R2_Dep>
                <DtMovto>2025-12-10</DtMovto>
            </LDL0014R2>
        </SISMSG>
    </DOC>
    """

    ldl0014r2 = LDL0014R2.from_xml(xml)

    assert isinstance(ldl0014r2, LDL0014R2)
    assert ldl0014r2.from_ispb == '31680151'
    assert ldl0014r2.to_ispb == '00038166'
    assert ldl0014r2.system_domain == 'SPB01'
    assert ldl0014r2.operation_number == '31680151250908000000001'
    assert ldl0014r2.message_code == 'LDL0014R2'
    assert ldl0014r2.str_control_number == 'STR20250101000000001'
    assert ldl0014r2.vendor_timestamp == datetime(2025, 12, 10, 15, 30)
    assert ldl0014r2.original_ldl_control_number == '321'
    assert ldl0014r2.institution_ispb == '31680151'
    assert ldl0014r2.ldl_ispb == '31680153'
    assert ldl0014r2.amount == Decimal('188.0')
    assert ldl0014r2.settlement_date == date(2025, 12, 10)

    assert len(ldl0014r2.deposit_group) == DEPOSIT_GROUP_SIZE
    deposit1 = ldl0014r2.deposit_group[0]
    deposit2 = ldl0014r2.deposit_group[1]
    assert isinstance(deposit1, DepositGroupR2)
    assert deposit1.cnpj == '50214141000185'
    assert deposit1.participant_identifier == '55386424'
    assert deposit1.amount == Decimal('100.0')
    assert deposit1.original_ldl_acceptance_control_number == '312'
    assert isinstance(deposit2, DepositGroupR2)
    assert deposit2.cnpj == '53753940000118'
    assert deposit2.participant_identifier == '43075534'
    assert deposit2.amount == Decimal('88.0')
    assert deposit2.original_ldl_acceptance_control_number == '132'


def test_ldl0014e_general_error_from_xml() -> None:
    xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/SPB/LDL0014E.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>31680151250908000000001</NUOp>
        </BCMSG>
        <SISMSG>
            <LDL0014 CodErro="EGEN0050">
                <CodMsg>LDL0014E</CodMsg>
                <NumCtrlIF>123</NumCtrlIF>
                <NumCtrlLDLOr>321</NumCtrlLDLOr>
                <ISPBIF>31680151</ISPBIF>
                <ISPBLDL>31680153</ISPBLDL>
                <VlrLanc>188.0</VlrLanc>
                <Grupo_LDL0014_Dep>
                    <CNPJNLiqdant>50214141000185</CNPJNLiqdant>
                    <IdentdPartCamr>55386424</IdentdPartCamr>
                    <VlrNLiqdant>100.0</VlrNLiqdant>
                    <NumCtrlActeLDLOr>312</NumCtrlActeLDLOr>
                    <NumCtrlReqIFOr>323</NumCtrlReqIFOr>
                </Grupo_LDL0014_Dep>
                <Grupo_LDL0014_Dep>
                    <CNPJNLiqdant>53753940000118</CNPJNLiqdant>
                    <IdentdPartCamr>43075534</IdentdPartCamr>
                    <VlrNLiqdant>88.0</VlrNLiqdant>
                    <NumCtrlActeLDLOr>132</NumCtrlActeLDLOr>
                    <NumCtrlReqIFOr>322</NumCtrlReqIFOr>
                </Grupo_LDL0014_Dep>
                <DtMovto>2025-12-10</DtMovto>
            </LDL0014>
        </SISMSG>
    </DOC>
    """

    ldl0014e = LDL0014E.from_xml(xml)

    assert isinstance(ldl0014e, LDL0014E)
    assert ldl0014e.from_ispb == '31680151'
    assert ldl0014e.to_ispb == '00038166'
    assert ldl0014e.system_domain == 'SPB01'
    assert ldl0014e.operation_number == '31680151250908000000001'
    assert ldl0014e.message_code == 'LDL0014E'
    assert ldl0014e.institution_control_number == '123'
    assert ldl0014e.original_ldl_control_number == '321'
    assert ldl0014e.institution_ispb == '31680151'
    assert ldl0014e.ldl_ispb == '31680153'
    assert ldl0014e.amount == Decimal('188.0')
    assert ldl0014e.settlement_date == date(2025, 12, 10)
    assert ldl0014e.general_error_code == 'EGEN0050'

    assert len(ldl0014e.deposit_group) == DEPOSIT_GROUP_SIZE
    deposit1 = ldl0014e.deposit_group[0]
    deposit2 = ldl0014e.deposit_group[1]
    assert isinstance(deposit1, DepositGroupError)
    assert deposit1.cnpj == '50214141000185'
    assert deposit1.participant_identifier == '55386424'
    assert deposit1.amount == Decimal('100.0')
    assert deposit1.original_ldl_acceptance_control_number == '312'
    assert deposit1.original_if_request_control_number == '323'
    assert isinstance(deposit2, DepositGroupError)
    assert deposit2.cnpj == '53753940000118'
    assert deposit2.participant_identifier == '43075534'
    assert deposit2.amount == Decimal('88.0')
    assert deposit2.original_ldl_acceptance_control_number == '132'
    assert deposit2.original_if_request_control_number == '322'


def test_ldl0014e_tag_error_from_xml() -> None:
    xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/SPB/LDL0014E.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>31680151250908000000001</NUOp>
        </BCMSG>
        <SISMSG>
            <LDL0014>
                <CodMsg>LDL0014E</CodMsg>
                <NumCtrlIF>123</NumCtrlIF>
                <NumCtrlLDLOr>321</NumCtrlLDLOr>
                <ISPBIF>31680151</ISPBIF>
                <ISPBLDL CodErro="EGEN0051">31680153</ISPBLDL>
                <VlrLanc>188.0</VlrLanc>
                <Grupo_LDL0014_Dep>
                    <CNPJNLiqdant>50214141000185</CNPJNLiqdant>
                    <IdentdPartCamr>55386424</IdentdPartCamr>
                    <VlrNLiqdant>100.0</VlrNLiqdant>
                    <NumCtrlActeLDLOr>312</NumCtrlActeLDLOr>
                    <NumCtrlReqIFOr>323</NumCtrlReqIFOr>
                </Grupo_LDL0014_Dep>
                <Grupo_LDL0014_Dep>
                    <CNPJNLiqdant>53753940000118</CNPJNLiqdant>
                    <IdentdPartCamr CodErro="ELDL0019">43075534</IdentdPartCamr>
                    <VlrNLiqdant>88.0</VlrNLiqdant>
                    <NumCtrlActeLDLOr>132</NumCtrlActeLDLOr>
                    <NumCtrlReqIFOr>322</NumCtrlReqIFOr>
                </Grupo_LDL0014_Dep>
                <DtMovto>2025-12-10</DtMovto>
            </LDL0014>
        </SISMSG>
    </DOC>
    """

    ldl0014e = LDL0014E.from_xml(xml)

    assert isinstance(ldl0014e, LDL0014E)
    assert ldl0014e.from_ispb == '31680151'
    assert ldl0014e.to_ispb == '00038166'
    assert ldl0014e.system_domain == 'SPB01'
    assert ldl0014e.operation_number == '31680151250908000000001'
    assert ldl0014e.message_code == 'LDL0014E'
    assert ldl0014e.institution_control_number == '123'
    assert ldl0014e.original_ldl_control_number == '321'
    assert ldl0014e.institution_ispb == '31680151'
    assert ldl0014e.ldl_ispb == '31680153'
    assert ldl0014e.amount == Decimal('188.0')
    assert ldl0014e.settlement_date == date(2025, 12, 10)
    assert ldl0014e.ldl_ispb_error_code == 'EGEN0051'

    assert len(ldl0014e.deposit_group) == DEPOSIT_GROUP_SIZE
    deposit1 = ldl0014e.deposit_group[0]
    deposit2 = ldl0014e.deposit_group[1]
    assert isinstance(deposit1, DepositGroupError)
    assert deposit1.cnpj == '50214141000185'
    assert deposit1.participant_identifier == '55386424'
    assert deposit1.amount == Decimal('100.0')
    assert deposit1.original_ldl_acceptance_control_number == '312'
    assert deposit1.original_if_request_control_number == '323'
    assert isinstance(deposit2, DepositGroupError)
    assert deposit2.cnpj == '53753940000118'
    assert deposit2.participant_identifier == '43075534'
    assert deposit2.amount == Decimal('88.0')
    assert deposit2.original_ldl_acceptance_control_number == '132'
    assert deposit2.original_if_request_control_number == '322'
    assert deposit2.participant_identifier_error_code == 'ELDL0019'


def test_ldl0014_roundtrip() -> None:
    params = make_valid_ldl0014_params()

    ldl0014 = LDL0014.model_validate(params)
    xml = ldl0014.to_xml()
    ldl0014_from_xml = LDL0014.from_xml(xml)

    assert ldl0014 == ldl0014_from_xml


def test_ldl0014r1_roundtrip() -> None:
    params = make_valid_ldl0014r1_params()

    ldl0014r1 = LDL0014R1.model_validate(params)
    xml = ldl0014r1.to_xml()
    ldl0014r1_from_xml = LDL0014R1.from_xml(xml)

    assert ldl0014r1 == ldl0014r1_from_xml


def test_ldl0014r2_roundtrip() -> None:
    params = make_valid_ldl0014r2_params()

    ldl0014r2 = LDL0014R2.model_validate(params)
    xml = ldl0014r2.to_xml()
    ldl0014r2_from_xml = LDL0014R2.from_xml(xml)

    assert ldl0014r2 == ldl0014r2_from_xml


def test_ldl0014_from_xml_missing_required_fields() -> None:
    xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/SPB/LDL0014.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>31680151250908000000001</NUOp>
        </BCMSG>
        <SISMSG>
            <LDL0014>
                <CodMsg>LDL0014</CodMsg>
            </LDL0014>
        </SISMSG>
    </DOC>
    """

    with pytest.raises(ValidationError) as exc:
        LDL0014.from_xml(xml)

    missing_fields = extract_missing_fields(exc.value)
    assert missing_fields == {
        'institution_control_number',
        'original_ldl_control_number',
        'institution_ispb',
        'ldl_ispb',
        'amount',
        'settlement_date',
    }
