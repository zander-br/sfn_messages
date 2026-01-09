from datetime import UTC, date, datetime
from decimal import Decimal
from typing import Any

import pytest
from pydantic import ValidationError

from sfn_messages.core.types import LdlSettlementStatus
from sfn_messages.ldl.ldl0004 import LDL0004, LDL0004E, LDL0004R1, LDL0004R2, NetResult, NetResultError, NetResultR2
from tests.conftest import extract_missing_fields, normalize_xml

NET_RESULT_SIZE = 2


def make_valid_ldl0004_params() -> dict[str, Any]:
    return {
        'from_ispb': '31680151',
        'to_ispb': '00038166',
        'system_domain': 'SPB01',
        'operation_number': '316801512509080000001',
        'message_code': 'LDL0004',
        'institution_control_number': '123',
        'institution_ispb': '31680151',
        'original_ldl_control_number': '321',
        'ldl_ispb': '31680153',
        'amount': 120.0,
        'net_result_group': [
            {
                'cnpj': '68689822000165',
                'participant_identifier': '43075534',
                'amount': 60.0,
            },
            {
                'cnpj': '39548823000191',
                'participant_identifier': '43075534',
                'amount': 60.0,
            },
        ],
        'settlement_date': '2025-12-09',
    }


def make_valid_ldl0004r1_params() -> dict[str, Any]:
    return {
        'from_ispb': '31680151',
        'to_ispb': '00038166',
        'system_domain': 'SPB01',
        'operation_number': '316801512509080000001',
        'message_code': 'LDL0004R1',
        'institution_control_number': '123',
        'institution_ispb': '31680151',
        'str_control_number': 'STR20250101000000001',
        'ldl_settlement_status': 'EFFECTIVE',
        'settlement_timestamp': '2025-12-09T10:00:00+00:00',
        'settlement_date': '2025-12-09',
    }


def make_valid_ldl0004r2_params() -> dict[str, Any]:
    return {
        'from_ispb': '31680151',
        'to_ispb': '00038166',
        'system_domain': 'SPB01',
        'operation_number': '316801512509080000001',
        'message_code': 'LDL0004R2',
        'original_ldl_control_number': '321',
        'institution_ispb': '31680151',
        'str_control_number': 'STR20250101000000001',
        'vendor_timestamp': '2025-12-09T09:00:00+00:00',
        'ldl_ispb': '31680153',
        'amount': 120.0,
        'net_result_group': [
            {
                'cnpj': '68689822000165',
                'participant_identifier': '43075534',
                'amount': 60.0,
            },
            {
                'cnpj': '39548823000191',
                'participant_identifier': '43075534',
                'amount': 60.0,
            },
        ],
        'settlement_date': '2025-12-09',
    }


def make_valid_ldl0004e_params(*, general_error: bool = False) -> dict[str, Any]:
    ldl0004e = {
        'from_ispb': '31680151',
        'to_ispb': '00038166',
        'system_domain': 'SPB01',
        'operation_number': '316801512509080000001',
        'message_code': 'LDL0004',
        'institution_control_number': '123',
        'institution_ispb': '31680151',
        'original_ldl_control_number': '321',
        'ldl_ispb': '31680153',
        'amount': 120.0,
        'net_result_group': [
            {
                'cnpj': '68689822000165',
                'participant_identifier': '43075534',
                'amount': 60.0,
            },
            {
                'cnpj': '39548823000191',
                'participant_identifier': '43075534',
                'amount': 60.0,
            },
        ],
        'settlement_date': '2025-12-09',
    }

    if general_error:
        ldl0004e['general_error_code'] = 'EGEN0050'
    else:
        ldl0004e['institution_ispb_error_code'] = 'ELDL0123'

    return ldl0004e


def test_ldl0004_valid_model() -> None:
    params = make_valid_ldl0004_params()
    ldl0004 = LDL0004.model_validate(params)

    assert isinstance(ldl0004, LDL0004)
    assert ldl0004.from_ispb == '31680151'
    assert ldl0004.to_ispb == '00038166'
    assert ldl0004.system_domain == 'SPB01'
    assert ldl0004.operation_number == '316801512509080000001'
    assert ldl0004.message_code == 'LDL0004'
    assert ldl0004.institution_control_number == '123'
    assert ldl0004.institution_ispb == '31680151'
    assert ldl0004.original_ldl_control_number == '321'
    assert ldl0004.ldl_ispb == '31680153'
    assert ldl0004.amount == Decimal('120.0')
    assert ldl0004.settlement_date == date(2025, 12, 9)

    assert len(ldl0004.net_result_group) == NET_RESULT_SIZE
    result1 = ldl0004.net_result_group[0]
    result2 = ldl0004.net_result_group[1]
    assert isinstance(result1, NetResult)
    assert result1.cnpj == '68689822000165'
    assert result1.participant_identifier == '43075534'
    assert result1.amount == Decimal('60.0')
    assert isinstance(result2, NetResult)
    assert result2.cnpj == '39548823000191'
    assert result2.participant_identifier == '43075534'
    assert result2.amount == Decimal('60.0')


def test_ldl0004r1_valid_model() -> None:
    params = make_valid_ldl0004r1_params()
    ldl0004r1 = LDL0004R1.model_validate(params)

    assert isinstance(ldl0004r1, LDL0004R1)
    assert ldl0004r1.from_ispb == '31680151'
    assert ldl0004r1.to_ispb == '00038166'
    assert ldl0004r1.system_domain == 'SPB01'
    assert ldl0004r1.operation_number == '316801512509080000001'
    assert ldl0004r1.message_code == 'LDL0004R1'
    assert ldl0004r1.institution_control_number == '123'
    assert ldl0004r1.institution_ispb == '31680151'
    assert ldl0004r1.str_control_number == 'STR20250101000000001'
    assert ldl0004r1.ldl_settlement_status == LdlSettlementStatus.EFFECTIVE
    assert ldl0004r1.settlement_date == date(2025, 12, 9)


def test_ldl0004r2_valid_model() -> None:
    params = make_valid_ldl0004r2_params()
    ldl0004r2 = LDL0004R2.model_validate(params)

    assert isinstance(ldl0004r2, LDL0004R2)
    assert ldl0004r2.from_ispb == '31680151'
    assert ldl0004r2.to_ispb == '00038166'
    assert ldl0004r2.system_domain == 'SPB01'
    assert ldl0004r2.operation_number == '316801512509080000001'
    assert ldl0004r2.message_code == 'LDL0004R2'
    assert ldl0004r2.original_ldl_control_number == '321'
    assert ldl0004r2.institution_ispb == '31680151'
    assert ldl0004r2.str_control_number == 'STR20250101000000001'
    assert ldl0004r2.vendor_timestamp == datetime(2025, 12, 9, 9, 0, tzinfo=UTC)
    assert ldl0004r2.ldl_ispb == '31680153'
    assert ldl0004r2.amount == Decimal('120.0')
    assert ldl0004r2.settlement_date == date(2025, 12, 9)

    assert len(ldl0004r2.net_result_group) == NET_RESULT_SIZE
    result1 = ldl0004r2.net_result_group[0]
    result2 = ldl0004r2.net_result_group[1]
    assert isinstance(result1, NetResultR2)
    assert result1.cnpj == '68689822000165'
    assert result1.participant_identifier == '43075534'
    assert result1.amount == Decimal('60.0')
    assert isinstance(result2, NetResultR2)
    assert result2.cnpj == '39548823000191'
    assert result2.participant_identifier == '43075534'
    assert result2.amount == Decimal('60.0')


def test_ldl0004e_valid_model() -> None:
    params = make_valid_ldl0004e_params()
    ldl0004e = LDL0004E.model_validate(params)

    assert isinstance(ldl0004e, LDL0004E)
    assert ldl0004e.from_ispb == '31680151'
    assert ldl0004e.to_ispb == '00038166'
    assert ldl0004e.system_domain == 'SPB01'
    assert ldl0004e.operation_number == '316801512509080000001'
    assert ldl0004e.message_code == 'LDL0004'
    assert ldl0004e.institution_control_number == '123'
    assert ldl0004e.institution_ispb == '31680151'
    assert ldl0004e.original_ldl_control_number == '321'
    assert ldl0004e.ldl_ispb == '31680153'
    assert ldl0004e.amount == Decimal('120.0')
    assert ldl0004e.settlement_date == date(2025, 12, 9)

    assert len(ldl0004e.net_result_group) == NET_RESULT_SIZE
    result1 = ldl0004e.net_result_group[0]
    result2 = ldl0004e.net_result_group[1]
    assert isinstance(result1, NetResultError)
    assert result1.cnpj == '68689822000165'
    assert result1.participant_identifier == '43075534'
    assert result1.amount == Decimal('60.0')
    assert isinstance(result2, NetResultError)
    assert result2.cnpj == '39548823000191'
    assert result2.participant_identifier == '43075534'
    assert result2.amount == Decimal('60.0')

    assert ldl0004e.institution_ispb_error_code == 'ELDL0123'


def test_ldl0004_missing_required_fields() -> None:
    with pytest.raises(ValidationError) as exc:
        LDL0004.model_validate({})

    missing_fields = extract_missing_fields(exc.value)
    assert missing_fields == {
        'from_ispb',
        'to_ispb',
        'system_domain',
        'operation_number',
        'institution_control_number',
        'institution_ispb',
        'original_ldl_control_number',
        'amount',
        'settlement_date',
    }


def test_ldl0004r1_missing_required_fields() -> None:
    with pytest.raises(ValidationError) as exc:
        LDL0004R1.model_validate({})

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


def test_ldl0004r2_missing_required_fields() -> None:
    with pytest.raises(ValidationError) as exc:
        LDL0004R2.model_validate({})

    missing_fields = extract_missing_fields(exc.value)
    assert missing_fields == {
        'from_ispb',
        'to_ispb',
        'system_domain',
        'operation_number',
        'original_ldl_control_number',
        'institution_ispb',
        'str_control_number',
        'vendor_timestamp',
        'ldl_ispb',
        'amount',
        'settlement_date',
    }


def test_ldl0004_to_xml() -> None:
    params = make_valid_ldl0004_params()
    ldl0004 = LDL0004.model_validate(params)

    xml = ldl0004.to_xml()

    expected_xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/LDL/LDL0004.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>316801512509080000001</NUOp>
        </BCMSG>
        <SISMSG>
            <LDL0004>
                <CodMsg>LDL0004</CodMsg>
                <NumCtrlIF>123</NumCtrlIF>
                <ISPBIF>31680151</ISPBIF>
                <NumCtrlLDLOr>321</NumCtrlLDLOr>
                <ISPBLDL>31680153</ISPBLDL>
                <VlrLanc>120.0</VlrLanc>
                <Grupo_LDL0004_ResultLiqd>
                    <CNPJNLiqdant>68689822000165</CNPJNLiqdant>
                    <IdentdPartCamr>43075534</IdentdPartCamr>
                    <VlrResultLiqdNLiqdant>60.0</VlrResultLiqdNLiqdant>
                </Grupo_LDL0004_ResultLiqd>
                <Grupo_LDL0004_ResultLiqd>
                    <CNPJNLiqdant>39548823000191</CNPJNLiqdant>
                    <IdentdPartCamr>43075534</IdentdPartCamr>
                    <VlrResultLiqdNLiqdant>60.0</VlrResultLiqdNLiqdant>
                </Grupo_LDL0004_ResultLiqd>
                <DtMovto>2025-12-09</DtMovto>
            </LDL0004>
        </SISMSG>
    </DOC>
    """
    assert normalize_xml(expected_xml) == normalize_xml(xml)


def test_ldl0004r1_to_xml() -> None:
    params = make_valid_ldl0004r1_params()
    ldl0004r1 = LDL0004R1.model_validate(params)

    xml = ldl0004r1.to_xml()

    expected_xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/LDL/LDL0004.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>316801512509080000001</NUOp>
        </BCMSG>
        <SISMSG>
            <LDL0004R1>
                <CodMsg>LDL0004R1</CodMsg>
                <NumCtrlIF>123</NumCtrlIF>
                <ISPBIF>31680151</ISPBIF>
                <NumCtrlSTR>STR20250101000000001</NumCtrlSTR>
                <SitLancLDL>1</SitLancLDL>
                <DtHrSit>2025-12-09 10:00:00+00:00</DtHrSit>
                <DtMovto>2025-12-09</DtMovto>
            </LDL0004R1>
        </SISMSG>
    </DOC>
    """
    assert normalize_xml(expected_xml) == normalize_xml(xml)


def test_ldl0004r2_to_xml() -> None:
    params = make_valid_ldl0004r2_params()
    ldl0004r2 = LDL0004R2.model_validate(params)

    xml = ldl0004r2.to_xml()

    expected_xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/LDL/LDL0004.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>316801512509080000001</NUOp>
        </BCMSG>
        <SISMSG>
            <LDL0004R2>
                <CodMsg>LDL0004R2</CodMsg>
                <NumCtrlLDLOr>321</NumCtrlLDLOr>
                <ISPBIF>31680151</ISPBIF>
                <NumCtrlSTR>STR20250101000000001</NumCtrlSTR>
                <DtHrBC>2025-12-09 09:00:00+00:00</DtHrBC>
                <ISPBLDL>31680153</ISPBLDL>
                <VlrLanc>120.0</VlrLanc>
                <Grupo_LDL0004R2_ResultLiqd>
                    <CNPJNLiqdant>68689822000165</CNPJNLiqdant>
                    <IdentdPartCamr>43075534</IdentdPartCamr>
                    <VlrResultLiqdNLiqdant>60.0</VlrResultLiqdNLiqdant>
                </Grupo_LDL0004R2_ResultLiqd>
                <Grupo_LDL0004R2_ResultLiqd>
                    <CNPJNLiqdant>39548823000191</CNPJNLiqdant>
                    <IdentdPartCamr>43075534</IdentdPartCamr>
                    <VlrResultLiqdNLiqdant>60.0</VlrResultLiqdNLiqdant>
                </Grupo_LDL0004R2_ResultLiqd>
                <DtMovto>2025-12-09</DtMovto>
            </LDL0004R2>
        </SISMSG>
    </DOC>
    """
    assert normalize_xml(expected_xml) == normalize_xml(xml)


def test_ldl0004e_general_error_to_xml() -> None:
    params = make_valid_ldl0004e_params(general_error=True)
    ldl0004e = LDL0004E.model_validate(params)

    xml = ldl0004e.to_xml()

    expected_xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/LDL/LDL0004E.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>316801512509080000001</NUOp>
        </BCMSG>
        <SISMSG>
            <LDL0004E CodErro="EGEN0050">
                <CodMsg>LDL0004</CodMsg>
                <NumCtrlIF>123</NumCtrlIF>
                <ISPBIF>31680151</ISPBIF>
                <NumCtrlLDLOr>321</NumCtrlLDLOr>
                <ISPBLDL>31680153</ISPBLDL>
                <VlrLanc>120.0</VlrLanc>
                <Grupo_LDL0004_ResultLiqd>
                    <CNPJNLiqdant>68689822000165</CNPJNLiqdant>
                    <IdentdPartCamr>43075534</IdentdPartCamr>
                    <VlrResultLiqdNLiqdant>60.0</VlrResultLiqdNLiqdant>
                </Grupo_LDL0004_ResultLiqd>
                <Grupo_LDL0004_ResultLiqd>
                    <CNPJNLiqdant>39548823000191</CNPJNLiqdant>
                    <IdentdPartCamr>43075534</IdentdPartCamr>
                    <VlrResultLiqdNLiqdant>60.0</VlrResultLiqdNLiqdant>
                </Grupo_LDL0004_ResultLiqd>
                <DtMovto>2025-12-09</DtMovto>
            </LDL0004E>
        </SISMSG>
    </DOC>
    """
    assert normalize_xml(expected_xml) == normalize_xml(xml)


def test_ldl0004e_tag_error_to_xml() -> None:
    params = make_valid_ldl0004e_params()
    ldl0004e = LDL0004E.model_validate(params)

    xml = ldl0004e.to_xml()

    expected_xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/LDL/LDL0004E.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>316801512509080000001</NUOp>
        </BCMSG>
        <SISMSG>
            <LDL0004E>
                <CodMsg>LDL0004</CodMsg>
                <NumCtrlIF>123</NumCtrlIF>
                <ISPBIF CodErro="ELDL0123">31680151</ISPBIF>
                <NumCtrlLDLOr>321</NumCtrlLDLOr>
                <ISPBLDL>31680153</ISPBLDL>
                <VlrLanc>120.0</VlrLanc>
                <Grupo_LDL0004_ResultLiqd>
                    <CNPJNLiqdant>68689822000165</CNPJNLiqdant>
                    <IdentdPartCamr>43075534</IdentdPartCamr>
                    <VlrResultLiqdNLiqdant>60.0</VlrResultLiqdNLiqdant>
                </Grupo_LDL0004_ResultLiqd>
                <Grupo_LDL0004_ResultLiqd>
                    <CNPJNLiqdant>39548823000191</CNPJNLiqdant>
                    <IdentdPartCamr>43075534</IdentdPartCamr>
                    <VlrResultLiqdNLiqdant>60.0</VlrResultLiqdNLiqdant>
                </Grupo_LDL0004_ResultLiqd>
                <DtMovto>2025-12-09</DtMovto>
            </LDL0004E>
        </SISMSG>
    </DOC>
    """
    assert normalize_xml(expected_xml) == normalize_xml(xml)


def test_ldl0004_from_xml() -> None:
    xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/LDL/LDL0004.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>316801512509080000001</NUOp>
        </BCMSG>
        <SISMSG>
            <LDL0004>
                <CodMsg>LDL0004</CodMsg>
                <NumCtrlIF>123</NumCtrlIF>
                <ISPBIF>31680151</ISPBIF>
                <NumCtrlLDLOr>321</NumCtrlLDLOr>
                <ISPBLDL>31680153</ISPBLDL>
                <VlrLanc>120.0</VlrLanc>
                <Grupo_LDL0004_ResultLiqd>
                    <CNPJNLiqdant>68689822000165</CNPJNLiqdant>
                    <IdentdPartCamr>43075534</IdentdPartCamr>
                    <VlrResultLiqdNLiqdant>60.0</VlrResultLiqdNLiqdant>
                </Grupo_LDL0004_ResultLiqd>
                <Grupo_LDL0004_ResultLiqd>
                    <CNPJNLiqdant>39548823000191</CNPJNLiqdant>
                    <IdentdPartCamr>43075534</IdentdPartCamr>
                    <VlrResultLiqdNLiqdant>60.0</VlrResultLiqdNLiqdant>
                </Grupo_LDL0004_ResultLiqd>
                <DtMovto>2025-12-09</DtMovto>
            </LDL0004>
        </SISMSG>
    </DOC>
    """

    ldl0004 = LDL0004.from_xml(xml)

    assert isinstance(ldl0004, LDL0004)
    assert ldl0004.from_ispb == '31680151'
    assert ldl0004.to_ispb == '00038166'
    assert ldl0004.system_domain == 'SPB01'
    assert ldl0004.operation_number == '316801512509080000001'
    assert ldl0004.message_code == 'LDL0004'
    assert ldl0004.institution_control_number == '123'
    assert ldl0004.institution_ispb == '31680151'
    assert ldl0004.original_ldl_control_number == '321'
    assert ldl0004.ldl_ispb == '31680153'
    assert ldl0004.amount == Decimal('120.0')
    assert ldl0004.settlement_date == date(2025, 12, 9)

    assert len(ldl0004.net_result_group) == NET_RESULT_SIZE
    result1 = ldl0004.net_result_group[0]
    result2 = ldl0004.net_result_group[1]
    assert isinstance(result1, NetResult)
    assert result1.cnpj == '68689822000165'
    assert result1.participant_identifier == '43075534'
    assert result1.amount == Decimal('60.0')
    assert isinstance(result2, NetResult)
    assert result2.cnpj == '39548823000191'
    assert result2.participant_identifier == '43075534'
    assert result2.amount == Decimal('60.0')


def test_ldl0004r1_from_xml() -> None:
    xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/LDL/LDL0004.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>316801512509080000001</NUOp>
        </BCMSG>
        <SISMSG>
            <LDL0004R1>
                <CodMsg>LDL0004R1</CodMsg>
                <NumCtrlIF>123</NumCtrlIF>
                <ISPBIF>31680151</ISPBIF>
                <NumCtrlSTR>STR20250101000000001</NumCtrlSTR>
                <SitLancLDL>1</SitLancLDL>
                <DtHrSit>2025-12-09 10:00:00+00:00</DtHrSit>
                <DtMovto>2025-12-09</DtMovto>
            </LDL0004R1>
        </SISMSG>
    </DOC>
    """

    ldl0004r1 = LDL0004R1.from_xml(xml)

    assert isinstance(ldl0004r1, LDL0004R1)
    assert ldl0004r1.from_ispb == '31680151'
    assert ldl0004r1.to_ispb == '00038166'
    assert ldl0004r1.system_domain == 'SPB01'
    assert ldl0004r1.operation_number == '316801512509080000001'
    assert ldl0004r1.message_code == 'LDL0004R1'
    assert ldl0004r1.institution_control_number == '123'
    assert ldl0004r1.institution_ispb == '31680151'
    assert ldl0004r1.str_control_number == 'STR20250101000000001'
    assert ldl0004r1.ldl_settlement_status == LdlSettlementStatus.EFFECTIVE
    assert ldl0004r1.settlement_date == date(2025, 12, 9)


def test_ldl0004r2_from_xml() -> None:
    xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/LDL/LDL0004.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>316801512509080000001</NUOp>
        </BCMSG>
        <SISMSG>
            <LDL0004R2>
                <CodMsg>LDL0004R2</CodMsg>
                <NumCtrlLDLOr>321</NumCtrlLDLOr>
                <ISPBIF>31680151</ISPBIF>
                <NumCtrlSTR>STR20250101000000001</NumCtrlSTR>
                <DtHrBC>2025-12-09 09:00:00+00:00</DtHrBC>
                <ISPBLDL>31680153</ISPBLDL>
                <VlrLanc>120.0</VlrLanc>
                <Grupo_LDL0004R2_ResultLiqd>
                    <CNPJNLiqdant>68689822000165</CNPJNLiqdant>
                    <IdentdPartCamr>43075534</IdentdPartCamr>
                    <VlrResultLiqdNLiqdant>60.0</VlrResultLiqdNLiqdant>
                </Grupo_LDL0004R2_ResultLiqd>
                <Grupo_LDL0004R2_ResultLiqd>
                    <CNPJNLiqdant>39548823000191</CNPJNLiqdant>
                    <IdentdPartCamr>43075534</IdentdPartCamr>
                    <VlrResultLiqdNLiqdant>60.0</VlrResultLiqdNLiqdant>
                </Grupo_LDL0004R2_ResultLiqd>
                <DtMovto>2025-12-09</DtMovto>
            </LDL0004R2>
        </SISMSG>
    </DOC>
    """

    ldl0004r2 = LDL0004R2.from_xml(xml)

    assert isinstance(ldl0004r2, LDL0004R2)
    assert ldl0004r2.from_ispb == '31680151'
    assert ldl0004r2.to_ispb == '00038166'
    assert ldl0004r2.system_domain == 'SPB01'
    assert ldl0004r2.operation_number == '316801512509080000001'
    assert ldl0004r2.message_code == 'LDL0004R2'
    assert ldl0004r2.original_ldl_control_number == '321'
    assert ldl0004r2.institution_ispb == '31680151'
    assert ldl0004r2.str_control_number == 'STR20250101000000001'
    assert ldl0004r2.vendor_timestamp == datetime(2025, 12, 9, 9, 0, tzinfo=UTC)
    assert ldl0004r2.ldl_ispb == '31680153'
    assert ldl0004r2.amount == Decimal('120.0')
    assert ldl0004r2.settlement_date == date(2025, 12, 9)

    assert len(ldl0004r2.net_result_group) == NET_RESULT_SIZE
    result1 = ldl0004r2.net_result_group[0]
    result2 = ldl0004r2.net_result_group[1]
    assert isinstance(result1, NetResultR2)
    assert result1.cnpj == '68689822000165'
    assert result1.participant_identifier == '43075534'
    assert result1.amount == Decimal('60.0')
    assert isinstance(result2, NetResultR2)
    assert result2.cnpj == '39548823000191'
    assert result2.participant_identifier == '43075534'
    assert result2.amount == Decimal('60.0')


def test_ldl0004e_general_error_from_xml() -> None:
    xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/LDL/LDL0004E.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>316801512509080000001</NUOp>
        </BCMSG>
        <SISMSG>
            <LDL0004E CodErro="EGEN0050">
                <CodMsg>LDL0004</CodMsg>
                <NumCtrlIF>123</NumCtrlIF>
                <ISPBIF>31680151</ISPBIF>
                <NumCtrlLDLOr>321</NumCtrlLDLOr>
                <ISPBLDL>31680153</ISPBLDL>
                <VlrLanc>120.0</VlrLanc>
                <Grupo_LDL0004_ResultLiqd>
                    <CNPJNLiqdant>68689822000165</CNPJNLiqdant>
                    <IdentdPartCamr>43075534</IdentdPartCamr>
                    <VlrResultLiqdNLiqdant>60.0</VlrResultLiqdNLiqdant>
                </Grupo_LDL0004_ResultLiqd>
                <Grupo_LDL0004_ResultLiqd>
                    <CNPJNLiqdant>39548823000191</CNPJNLiqdant>
                    <IdentdPartCamr>43075534</IdentdPartCamr>
                    <VlrResultLiqdNLiqdant>60.0</VlrResultLiqdNLiqdant>
                </Grupo_LDL0004_ResultLiqd>
                <DtMovto>2025-12-09</DtMovto>
            </LDL0004E>
        </SISMSG>
    </DOC>
    """

    ldl0004e = LDL0004E.from_xml(xml)

    assert isinstance(ldl0004e, LDL0004E)
    assert ldl0004e.from_ispb == '31680151'
    assert ldl0004e.to_ispb == '00038166'
    assert ldl0004e.system_domain == 'SPB01'
    assert ldl0004e.operation_number == '316801512509080000001'
    assert ldl0004e.message_code == 'LDL0004'
    assert ldl0004e.institution_control_number == '123'
    assert ldl0004e.institution_ispb == '31680151'
    assert ldl0004e.original_ldl_control_number == '321'
    assert ldl0004e.ldl_ispb == '31680153'
    assert ldl0004e.amount == Decimal('120.0')
    assert ldl0004e.settlement_date == date(2025, 12, 9)

    assert len(ldl0004e.net_result_group) == NET_RESULT_SIZE
    result1 = ldl0004e.net_result_group[0]
    result2 = ldl0004e.net_result_group[1]
    assert isinstance(result1, NetResultError)
    assert result1.cnpj == '68689822000165'
    assert result1.participant_identifier == '43075534'
    assert result1.amount == Decimal('60.0')
    assert isinstance(result2, NetResultError)
    assert result2.cnpj == '39548823000191'
    assert result2.participant_identifier == '43075534'
    assert result2.amount == Decimal('60.0')

    assert ldl0004e.general_error_code == 'EGEN0050'


def test_ldl0004e_tag_error_from_xml() -> None:
    xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/LDL/LDL0004E.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>316801512509080000001</NUOp>
        </BCMSG>
        <SISMSG>
            <LDL0004E>
                <CodMsg>LDL0004</CodMsg>
                <NumCtrlIF>123</NumCtrlIF>
                <ISPBIF CodErro="ELDL0123">31680151</ISPBIF>
                <NumCtrlLDLOr>321</NumCtrlLDLOr>
                <ISPBLDL>31680153</ISPBLDL>
                <VlrLanc>120.0</VlrLanc>
                <Grupo_LDL0004_ResultLiqd>
                    <CNPJNLiqdant>68689822000165</CNPJNLiqdant>
                    <IdentdPartCamr>43075534</IdentdPartCamr>
                    <VlrResultLiqdNLiqdant>60.0</VlrResultLiqdNLiqdant>
                </Grupo_LDL0004_ResultLiqd>
                <Grupo_LDL0004_ResultLiqd>
                    <CNPJNLiqdant>39548823000191</CNPJNLiqdant>
                    <IdentdPartCamr>43075534</IdentdPartCamr>
                    <VlrResultLiqdNLiqdant>60.0</VlrResultLiqdNLiqdant>
                </Grupo_LDL0004_ResultLiqd>
                <DtMovto>2025-12-09</DtMovto>
            </LDL0004E>
        </SISMSG>
    </DOC>
    """

    ldl0004e = LDL0004E.from_xml(xml)

    assert isinstance(ldl0004e, LDL0004E)
    assert ldl0004e.from_ispb == '31680151'
    assert ldl0004e.to_ispb == '00038166'
    assert ldl0004e.system_domain == 'SPB01'
    assert ldl0004e.operation_number == '316801512509080000001'
    assert ldl0004e.message_code == 'LDL0004'
    assert ldl0004e.institution_control_number == '123'
    assert ldl0004e.institution_ispb == '31680151'
    assert ldl0004e.original_ldl_control_number == '321'
    assert ldl0004e.ldl_ispb == '31680153'
    assert ldl0004e.amount == Decimal('120.0')
    assert ldl0004e.settlement_date == date(2025, 12, 9)

    assert len(ldl0004e.net_result_group) == NET_RESULT_SIZE
    result1 = ldl0004e.net_result_group[0]
    result2 = ldl0004e.net_result_group[1]
    assert isinstance(result1, NetResultError)
    assert result1.cnpj == '68689822000165'
    assert result1.participant_identifier == '43075534'
    assert result1.amount == Decimal('60.0')
    assert isinstance(result2, NetResultError)
    assert result2.cnpj == '39548823000191'
    assert result2.participant_identifier == '43075534'
    assert result2.amount == Decimal('60.0')

    assert ldl0004e.institution_ispb_error_code == 'ELDL0123'


def test_ldl0004_roundtrip() -> None:
    params = make_valid_ldl0004_params()

    ldl0004 = LDL0004.model_validate(params)
    xml = ldl0004.to_xml()
    ldl0004_from_xml = LDL0004.from_xml(xml)

    assert ldl0004 == ldl0004_from_xml


def test_ldl0004r1_roundtrip() -> None:
    params = make_valid_ldl0004r1_params()

    ldl0004r1 = LDL0004R1.model_validate(params)
    xml = ldl0004r1.to_xml()
    ldl0004r1_from_xml = LDL0004R1.from_xml(xml)

    assert ldl0004r1 == ldl0004r1_from_xml


def test_ldl0004r2_roundtrip() -> None:
    params = make_valid_ldl0004r2_params()

    ldl0004r2 = LDL0004R2.model_validate(params)
    xml = ldl0004r2.to_xml()
    ldl0004r2_from_xml = LDL0004R2.from_xml(xml)

    assert ldl0004r2 == ldl0004r2_from_xml


def test_ldl0004_from_xml_missing_required_fields() -> None:
    xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/SME/SME0001.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>316801512509080000001</NUOp>
        </BCMSG>
        <SISMSG>
            <LDL0004>
                <CodMsg>LDL0004</CodMsg>
            </LDL0004>
        </SISMSG>
    </DOC>
    """

    with pytest.raises(ValidationError) as exc:
        LDL0004.from_xml(xml)

    missing_fields = extract_missing_fields(exc.value)
    assert missing_fields == {
        'institution_control_number',
        'institution_ispb',
        'original_ldl_control_number',
        'amount',
        'settlement_date',
    }
