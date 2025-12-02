from datetime import UTC, date, datetime
from typing import Any

import pytest
from pydantic import ValidationError

from sfn_messages.gen.gen0020 import GEN0020, GEN0020R1, Responsible
from tests.conftest import extract_missing_fields, normalize_xml

RESPONSIBLE_SIZE = 2


def make_valid_gen0020_params() -> dict[str, Any]:
    return {
        'from_ispb': '31680151',
        'to_ispb': '00038166',
        'system_domain': 'SPB01',
        'operation_number': '316801512509080000001',
        'message_code': 'GEN0020',
        'participant_institution_control_number': '123',
        'participant_ispb': '31680151',
        'parcitipant_consulted_ispb': '00038166',
        'settlement_date': '2025-11-27',
    }


def make_valid_gen0020r1_params() -> dict[str, Any]:
    return {
        'from_ispb': '31680151',
        'to_ispb': '00038166',
        'system_domain': 'SPB01',
        'operation_number': '316801512509080000001',
        'message_code': 'GEN0020R1',
        'participant_institution_control_number': '123',
        'participant_ispb': '31680151',
        'parcitipant_consulted_ispb': '00038166',
        'responsibles': [
            {
                'cpf': '05046528002',
                'document': '398127955',
                'name': 'John Doe 01',
                'email': 'john.doe.01@test.com',
                'telephone_1': '65994861321',
                'telephone_2': '6537132095',
                'responsible_type': 'SPB_DIRECTOR',
            },
            {
                'cpf': '30288815009',
                'document': '151058246',
                'name': 'John Doe 02',
                'email': 'john.doe.02@test.com',
                'telephone_1': '63987350515',
                'telephone_2': '6325324500',
                'responsible_type': 'MONITOR',
            },
        ],
        'original_description': 'Test description',
        'original_provider_datetime': '2025-11-27T16:02:00+00:00',
        'provider_datetime': '2025-11-27T16:02:00+00:00',
        'settlement_date': '2025-11-27',
    }


def test_gen0020_valid_model() -> None:
    params = make_valid_gen0020_params()
    gen0020 = GEN0020.model_validate(params)

    assert isinstance(gen0020, GEN0020)
    assert gen0020.from_ispb == '31680151'
    assert gen0020.to_ispb == '00038166'
    assert gen0020.system_domain == 'SPB01'
    assert gen0020.operation_number == '316801512509080000001'
    assert gen0020.message_code == 'GEN0020'
    assert gen0020.participant_institution_control_number == '123'
    assert gen0020.participant_ispb == '31680151'
    assert gen0020.parcitipant_consulted_ispb == '00038166'
    assert gen0020.settlement_date == date(2025, 11, 27)


def test_gen0020r1_valid_model() -> None:
    params = make_valid_gen0020r1_params()
    gen0020r1 = GEN0020R1.model_validate(params)

    assert isinstance(gen0020r1, GEN0020R1)
    assert gen0020r1.from_ispb == '31680151'
    assert gen0020r1.to_ispb == '00038166'
    assert gen0020r1.system_domain == 'SPB01'
    assert gen0020r1.operation_number == '316801512509080000001'
    assert gen0020r1.message_code == 'GEN0020R1'
    assert gen0020r1.participant_institution_control_number == '123'
    assert gen0020r1.participant_ispb == '31680151'
    assert gen0020r1.parcitipant_consulted_ispb == '00038166'
    assert gen0020r1.original_description == 'Test description'
    assert gen0020r1.original_provider_datetime == datetime(2025, 11, 27, 16, 2, tzinfo=UTC)
    assert gen0020r1.provider_datetime == datetime(2025, 11, 27, 16, 2, tzinfo=UTC)
    assert gen0020r1.settlement_date == date(2025, 11, 27)

    assert len(gen0020r1.responsibles) == RESPONSIBLE_SIZE
    resp1 = gen0020r1.responsibles[0]
    resp2 = gen0020r1.responsibles[1]
    assert isinstance(resp1, Responsible)
    assert resp1.cpf == '05046528002'
    assert resp1.telephone_1 == '65994861321'
    assert isinstance(resp2, Responsible)
    assert resp2.cpf == '30288815009'
    assert resp2.telephone_1 == '63987350515'


def test_gen0020_missing_required_fields() -> None:
    with pytest.raises(ValidationError) as exc:
        GEN0020.model_validate({})

    missing_fields = extract_missing_fields(exc.value)
    assert missing_fields == {
        'from_ispb',
        'to_ispb',
        'system_domain',
        'operation_number',
        'participant_institution_control_number',
        'participant_ispb',
        'settlement_date',
    }


def test_gen0020r1_missing_required_fields() -> None:
    with pytest.raises(ValidationError) as exc:
        GEN0020R1.model_validate({})

    missing_fields = extract_missing_fields(exc.value)
    assert missing_fields == {
        'from_ispb',
        'to_ispb',
        'system_domain',
        'operation_number',
        'participant_institution_control_number',
        'participant_ispb',
        'provider_datetime',
        'settlement_date',
    }


def test_gen0020_to_xml() -> None:
    params = make_valid_gen0020_params()
    gen0020 = GEN0020.model_validate(params)

    xml = gen0020.to_xml()

    expected_xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/GEN/GEN0020.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>316801512509080000001</NUOp>
        </BCMSG>
        <SISMSG>
            <GEN0020>
                <CodMsg>GEN0020</CodMsg>
                <NumCtrlPart>123</NumCtrlPart>
                <ISPBPart>31680151</ISPBPart>
                <ISPBPartConsd>00038166</ISPBPartConsd>
                <DtMovto>2025-11-27</DtMovto>
            </GEN0020>
        </SISMSG>
    </DOC>
    """
    assert normalize_xml(expected_xml) == normalize_xml(xml)


def test_gen0020r1_to_xml() -> None:
    params = make_valid_gen0020r1_params()
    gen0020r1 = GEN0020R1.model_validate(params)

    xml = gen0020r1.to_xml()

    expected_xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/GEN/GEN0020.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>316801512509080000001</NUOp>
        </BCMSG>
        <SISMSG>
            <GEN0020R1>
                <CodMsg>GEN0020R1</CodMsg>
                <NumCtrlPart>123</NumCtrlPart>
                <ISPBPart>31680151</ISPBPart>
                <ISPBPartConsd>00038166</ISPBPartConsd>
                <Grupo_GEN0020R1_Respons>
                    <CPFRespons>05046528002</CPFRespons>
                    <NumDocRespons>398127955</NumDocRespons>
                    <NomRespons>John Doe 01</NomRespons>
                    <EndEletrnc>john.doe.01@test.com</EndEletrnc>
                    <NumTelRespons1>65994861321</NumTelRespons1>
                    <NumTelRespons2>6537132095</NumTelRespons2>
                    <TpRespons>D</TpRespons>
                </Grupo_GEN0020R1_Respons>
                <Grupo_GEN0020R1_Respons>
                    <CPFRespons>30288815009</CPFRespons>
                    <NumDocRespons>151058246</NumDocRespons>
                    <NomRespons>John Doe 02</NomRespons>
                    <EndEletrnc>john.doe.02@test.com</EndEletrnc>
                    <NumTelRespons1>63987350515</NumTelRespons1>
                    <NumTelRespons2>6325324500</NumTelRespons2>
                    <TpRespons>M</TpRespons>
                </Grupo_GEN0020R1_Respons>
                <HistOr>Test description</HistOr>
                <DtHrPrestdOr>2025-11-27 16:02:00+00:00</DtHrPrestdOr>
                <DtHrPrestd>2025-11-27 16:02:00+00:00</DtHrPrestd>
                <DtMovto>2025-11-27</DtMovto>
            </GEN0020R1>
        </SISMSG>
    </DOC>
    """
    assert normalize_xml(expected_xml) == normalize_xml(xml)


def test_gen0020_from_xml() -> None:
    xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/GEN/GEN0020.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>316801512509080000001</NUOp>
        </BCMSG>
        <SISMSG>
            <GEN0020>
                <CodMsg>GEN0020</CodMsg>
                <NumCtrlPart>123</NumCtrlPart>
                <ISPBPart>31680151</ISPBPart>
                <ISPBPartConsd>00038166</ISPBPartConsd>
                <DtMovto>2025-11-27</DtMovto>
            </GEN0020>
        </SISMSG>
    </DOC>
    """

    gen0020 = GEN0020.from_xml(xml)

    assert isinstance(gen0020, GEN0020)
    assert gen0020.from_ispb == '31680151'
    assert gen0020.to_ispb == '00038166'
    assert gen0020.system_domain == 'SPB01'
    assert gen0020.operation_number == '316801512509080000001'
    assert gen0020.message_code == 'GEN0020'
    assert gen0020.participant_institution_control_number == '123'
    assert gen0020.participant_ispb == '31680151'
    assert gen0020.parcitipant_consulted_ispb == '00038166'
    assert gen0020.settlement_date == date(2025, 11, 27)


def test_gen0020r1_from_xml() -> None:
    xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/GEN/GEN0020.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>316801512509080000001</NUOp>
        </BCMSG>
        <SISMSG>
            <GEN0020R1>
                <CodMsg>GEN0020R1</CodMsg>
                <NumCtrlPart>123</NumCtrlPart>
                <ISPBPart>31680151</ISPBPart>
                <ISPBPartConsd>00038166</ISPBPartConsd>
                <Grupo_GEN0020R1_Respons>
                    <CPFRespons>05046528002</CPFRespons>
                    <NumDocRespons>398127955</NumDocRespons>
                    <NomRespons>John Doe 01</NomRespons>
                    <EndEletrnc>john.doe.01@test.com</EndEletrnc>
                    <NumTelRespons1>65994861321</NumTelRespons1>
                    <NumTelRespons2>6537132095</NumTelRespons2>
                    <TpRespons>D</TpRespons>
                </Grupo_GEN0020R1_Respons>
                <Grupo_GEN0020R1_Respons>
                    <CPFRespons>30288815009</CPFRespons>
                    <NumDocRespons>151058246</NumDocRespons>
                    <NomRespons>John Doe 02</NomRespons>
                    <EndEletrnc>john.doe.02@test.com</EndEletrnc>
                    <NumTelRespons1>63987350515</NumTelRespons1>
                    <NumTelRespons2>6325324500</NumTelRespons2>
                    <TpRespons>M</TpRespons>
                </Grupo_GEN0020R1_Respons>
                <HistOr>Test description</HistOr>
                <DtHrPrestdOr>2025-11-27 16:02:00+00:00</DtHrPrestdOr>
                <DtHrPrestd>2025-11-27 16:02:00+00:00</DtHrPrestd>
                <DtMovto>2025-11-27</DtMovto>
            </GEN0020R1>
        </SISMSG>
    </DOC>
    """

    gen0020r1 = GEN0020R1.from_xml(xml)

    assert isinstance(gen0020r1, GEN0020R1)
    assert gen0020r1.from_ispb == '31680151'
    assert gen0020r1.to_ispb == '00038166'
    assert gen0020r1.system_domain == 'SPB01'
    assert gen0020r1.operation_number == '316801512509080000001'
    assert gen0020r1.message_code == 'GEN0020R1'
    assert gen0020r1.participant_institution_control_number == '123'
    assert gen0020r1.participant_ispb == '31680151'
    assert gen0020r1.parcitipant_consulted_ispb == '00038166'
    assert gen0020r1.original_description == 'Test description'
    assert gen0020r1.original_provider_datetime == datetime(2025, 11, 27, 16, 2, tzinfo=UTC)
    assert gen0020r1.provider_datetime == datetime(2025, 11, 27, 16, 2, tzinfo=UTC)
    assert gen0020r1.settlement_date == date(2025, 11, 27)

    assert len(gen0020r1.responsibles) == RESPONSIBLE_SIZE
    resp1 = gen0020r1.responsibles[0]
    resp2 = gen0020r1.responsibles[1]
    assert isinstance(resp1, Responsible)
    assert resp1.cpf == '05046528002'
    assert resp1.telephone_1 == '65994861321'
    assert isinstance(resp2, Responsible)
    assert resp2.cpf == '30288815009'
    assert resp2.telephone_1 == '63987350515'


def test_gen0020_roundtrip() -> None:
    params = make_valid_gen0020_params()

    gen0020 = GEN0020.model_validate(params)
    xml = gen0020.to_xml()
    gen0020_from_xml = GEN0020.from_xml(xml)

    assert gen0020 == gen0020_from_xml


def test_gen0020_from_xml_missing_required_fields() -> None:
    xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/GEN/GEN0020.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>316801512509080000001</NUOp>
        </BCMSG>
        <SISMSG>
            <GEN0020>
                <CodMsg>GEN0020</CodMsg>
            </GEN0020>
        </SISMSG>
    </DOC>
    """

    with pytest.raises(ValidationError) as exc:
        GEN0020.from_xml(xml)

    missing_fields = extract_missing_fields(exc.value)
    assert missing_fields == {
        'participant_institution_control_number',
        'participant_ispb',
        'settlement_date',
    }
