from datetime import date, datetime
from typing import Any

import pytest
from pydantic import ValidationError

from sfn_messages.gen.gen0019 import GEN0019, GEN0019E, GEN0019R1, Responsible, ResponsibleError
from tests.conftest import extract_missing_fields, normalize_xml

RESPONSIBLE_SIZE = 2


def make_valid_gen0019_params() -> dict[str, Any]:
    return {
        'from_ispb': '31680151',
        'to_ispb': '00038166',
        'system_domain': 'SPB01',
        'operation_number': '31680151250908000000001',
        'message_code': 'GEN0019',
        'participant_institution_control_number': '123',
        'participant_ispb': '31680151',
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
        'description': 'GEN0019 Description Test',
        'settlement_date': '2026-02-11',
    }


def make_valid_gen0019r1_params() -> dict[str, Any]:
    return {
        'from_ispb': '31680151',
        'to_ispb': '00038166',
        'system_domain': 'SPB01',
        'operation_number': '31680151250908000000001',
        'message_code': 'GEN0019R1',
        'participant_institution_control_number': '123',
        'participant_ispb': '31680151',
        'provider_datetime': '2026-02-11T18:47:23',
        'settlement_date': '2026-02-11',
    }


def make_valid_gen0019e_params(*, general_error: bool = False) -> dict[str, Any]:
    gen0019e = {
        'from_ispb': '31680151',
        'to_ispb': '00038166',
        'system_domain': 'SPB01',
        'operation_number': '31680151250908000000001',
        'message_code': 'GEN0019E',
        'participant_institution_control_number': '123',
        'participant_ispb': '31680151',
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
        'description': 'GEN0019 Description Test',
        'settlement_date': '2026-02-11',
    }

    if general_error:
        gen0019e['general_error_code'] = 'EGEN0050'
    else:
        gen0019e['participant_ispb_error_code'] = 'EGEN0051'

    return gen0019e


def test_gen0019_valid_model() -> None:
    params = make_valid_gen0019_params()
    gen0019 = GEN0019.model_validate(params)

    assert isinstance(gen0019, GEN0019)
    assert gen0019.from_ispb == '31680151'
    assert gen0019.to_ispb == '00038166'
    assert gen0019.system_domain == 'SPB01'
    assert gen0019.operation_number == '31680151250908000000001'
    assert gen0019.message_code == 'GEN0019'
    assert gen0019.participant_institution_control_number == '123'
    assert gen0019.participant_ispb == '31680151'
    assert gen0019.description == 'GEN0019 Description Test'
    assert gen0019.settlement_date == date(2026, 2, 11)

    assert len(gen0019.responsibles) == RESPONSIBLE_SIZE
    resp1 = gen0019.responsibles[0]
    resp2 = gen0019.responsibles[1]
    assert isinstance(resp1, Responsible)
    assert resp1.cpf == '05046528002'
    assert resp1.telephone_1 == '65994861321'
    assert isinstance(resp2, Responsible)
    assert resp2.cpf == '30288815009'
    assert resp2.telephone_1 == '63987350515'


def test_gen0019r1_valid_model() -> None:
    params = make_valid_gen0019r1_params()
    gen0019r1 = GEN0019R1.model_validate(params)

    assert isinstance(gen0019r1, GEN0019R1)
    assert gen0019r1.from_ispb == '31680151'
    assert gen0019r1.to_ispb == '00038166'
    assert gen0019r1.system_domain == 'SPB01'
    assert gen0019r1.operation_number == '31680151250908000000001'
    assert gen0019r1.message_code == 'GEN0019R1'
    assert gen0019r1.participant_institution_control_number == '123'
    assert gen0019r1.participant_ispb == '31680151'
    assert gen0019r1.provider_datetime == datetime(2026, 2, 11, 18, 47, 23)
    assert gen0019r1.settlement_date == date(2026, 2, 11)


def test_gen0019e_general_error_valid_model() -> None:
    params = make_valid_gen0019e_params(general_error=True)
    gen0019e = GEN0019E.model_validate(params)

    assert isinstance(gen0019e, GEN0019E)
    assert gen0019e.from_ispb == '31680151'
    assert gen0019e.to_ispb == '00038166'
    assert gen0019e.system_domain == 'SPB01'
    assert gen0019e.operation_number == '31680151250908000000001'
    assert gen0019e.message_code == 'GEN0019E'
    assert gen0019e.participant_institution_control_number == '123'
    assert gen0019e.participant_ispb == '31680151'
    assert gen0019e.description == 'GEN0019 Description Test'
    assert gen0019e.settlement_date == date(2026, 2, 11)
    assert gen0019e.general_error_code == 'EGEN0050'

    assert len(gen0019e.responsibles) == RESPONSIBLE_SIZE
    resp1 = gen0019e.responsibles[0]
    resp2 = gen0019e.responsibles[1]
    assert isinstance(resp1, ResponsibleError)
    assert resp1.cpf == '05046528002'
    assert resp1.telephone_1 == '65994861321'
    assert isinstance(resp2, ResponsibleError)
    assert resp2.cpf == '30288815009'
    assert resp2.telephone_1 == '63987350515'


def test_gen0019e_tag_error_valid_model() -> None:
    params = make_valid_gen0019e_params()
    gen0019e = GEN0019E.model_validate(params)

    assert isinstance(gen0019e, GEN0019E)
    assert gen0019e.from_ispb == '31680151'
    assert gen0019e.to_ispb == '00038166'
    assert gen0019e.system_domain == 'SPB01'
    assert gen0019e.operation_number == '31680151250908000000001'
    assert gen0019e.message_code == 'GEN0019E'
    assert gen0019e.participant_institution_control_number == '123'
    assert gen0019e.participant_ispb == '31680151'
    assert gen0019e.description == 'GEN0019 Description Test'
    assert gen0019e.settlement_date == date(2026, 2, 11)
    assert gen0019e.participant_ispb_error_code == 'EGEN0051'

    assert len(gen0019e.responsibles) == RESPONSIBLE_SIZE
    resp1 = gen0019e.responsibles[0]
    resp2 = gen0019e.responsibles[1]
    assert isinstance(resp1, ResponsibleError)
    assert resp1.cpf == '05046528002'
    assert resp1.telephone_1 == '65994861321'
    assert isinstance(resp2, ResponsibleError)
    assert resp2.cpf == '30288815009'
    assert resp2.telephone_1 == '63987350515'


def test_gen0019_missing_required_fields() -> None:
    with pytest.raises(ValidationError) as exc:
        GEN0019.model_validate({})

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


def test_gen0019r1_missing_required_fields() -> None:
    with pytest.raises(ValidationError) as exc:
        GEN0019R1.model_validate({})

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


def test_gen0019_to_xml() -> None:
    params = make_valid_gen0019_params()
    gen0019 = GEN0019.model_validate(params)

    xml = gen0019.to_xml()

    expected_xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/GEN/GEN0019.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>31680151250908000000001</NUOp>
        </BCMSG>
        <SISMSG>
            <GEN0019>
                <CodMsg>GEN0019</CodMsg>
                <NumCtrlPart>123</NumCtrlPart>
                <ISPBPart>31680151</ISPBPart>
                <Grupo_GEN0019_Respons>
                    <CPFRespons>05046528002</CPFRespons>
                    <NumDocRespons>398127955</NumDocRespons>
                    <NomRespons>John Doe 01</NomRespons>
                    <EndEletrnc>john.doe.01@test.com</EndEletrnc>
                    <NumTelRespons1>65994861321</NumTelRespons1>
                    <NumTelRespons2>6537132095</NumTelRespons2>
                    <TpRespons>D</TpRespons>
                </Grupo_GEN0019_Respons>
                <Grupo_GEN0019_Respons>
                    <CPFRespons>30288815009</CPFRespons>
                    <NumDocRespons>151058246</NumDocRespons>
                    <NomRespons>John Doe 02</NomRespons>
                    <EndEletrnc>john.doe.02@test.com</EndEletrnc>
                    <NumTelRespons1>63987350515</NumTelRespons1>
                    <NumTelRespons2>6325324500</NumTelRespons2>
                    <TpRespons>M</TpRespons>
                </Grupo_GEN0019_Respons>
                <Hist>GEN0019 Description Test</Hist>
                <DtMovto>2026-02-11</DtMovto>
            </GEN0019>
        </SISMSG>
    </DOC>
    """
    assert normalize_xml(expected_xml) == normalize_xml(xml)


def test_gen0019r1_to_xml() -> None:
    params = make_valid_gen0019r1_params()
    gen0019r1 = GEN0019R1.model_validate(params)

    xml = gen0019r1.to_xml()

    expected_xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/GEN/GEN0019.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>31680151250908000000001</NUOp>
        </BCMSG>
        <SISMSG>
            <GEN0019R1>
                <CodMsg>GEN0019R1</CodMsg>
                <NumCtrlPart>123</NumCtrlPart>
                <ISPBPart>31680151</ISPBPart>
                <DtHrPrestd>2026-02-11T18:47:23</DtHrPrestd>
                <DtMovto>2026-02-11</DtMovto>
            </GEN0019R1>
        </SISMSG>
    </DOC>
    """
    assert normalize_xml(expected_xml) == normalize_xml(xml)


def test_gen0019e_general_error_to_xml() -> None:
    params = make_valid_gen0019e_params(general_error=True)
    gen0019e = GEN0019E.model_validate(params)

    xml = gen0019e.to_xml()

    expected_xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/GEN/GEN0019E.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>31680151250908000000001</NUOp>
        </BCMSG>
        <SISMSG>
            <GEN0019 CodErro="EGEN0050">
                <CodMsg>GEN0019E</CodMsg>
                <NumCtrlPart>123</NumCtrlPart>
                <ISPBPart>31680151</ISPBPart>
                <Grupo_GEN0019_Respons>
                    <CPFRespons>05046528002</CPFRespons>
                    <NumDocRespons>398127955</NumDocRespons>
                    <NomRespons>John Doe 01</NomRespons>
                    <EndEletrnc>john.doe.01@test.com</EndEletrnc>
                    <NumTelRespons1>65994861321</NumTelRespons1>
                    <NumTelRespons2>6537132095</NumTelRespons2>
                    <TpRespons>D</TpRespons>
                </Grupo_GEN0019_Respons>
                <Grupo_GEN0019_Respons>
                    <CPFRespons>30288815009</CPFRespons>
                    <NumDocRespons>151058246</NumDocRespons>
                    <NomRespons>John Doe 02</NomRespons>
                    <EndEletrnc>john.doe.02@test.com</EndEletrnc>
                    <NumTelRespons1>63987350515</NumTelRespons1>
                    <NumTelRespons2>6325324500</NumTelRespons2>
                    <TpRespons>M</TpRespons>
                </Grupo_GEN0019_Respons>
                <Hist>GEN0019 Description Test</Hist>
                <DtMovto>2026-02-11</DtMovto>
            </GEN0019>
        </SISMSG>
    </DOC>
    """
    assert normalize_xml(expected_xml) == normalize_xml(xml)


def test_gen0019e_tag_error_to_xml() -> None:
    params = make_valid_gen0019e_params()
    gen0019e = GEN0019E.model_validate(params)

    xml = gen0019e.to_xml()

    expected_xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/GEN/GEN0019E.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>31680151250908000000001</NUOp>
        </BCMSG>
        <SISMSG>
            <GEN0019>
                <CodMsg>GEN0019E</CodMsg>
                <NumCtrlPart>123</NumCtrlPart>
                <ISPBPart CodErro="EGEN0051">31680151</ISPBPart>
                <Grupo_GEN0019_Respons>
                    <CPFRespons>05046528002</CPFRespons>
                    <NumDocRespons>398127955</NumDocRespons>
                    <NomRespons>John Doe 01</NomRespons>
                    <EndEletrnc>john.doe.01@test.com</EndEletrnc>
                    <NumTelRespons1>65994861321</NumTelRespons1>
                    <NumTelRespons2>6537132095</NumTelRespons2>
                    <TpRespons>D</TpRespons>
                </Grupo_GEN0019_Respons>
                <Grupo_GEN0019_Respons>
                    <CPFRespons>30288815009</CPFRespons>
                    <NumDocRespons>151058246</NumDocRespons>
                    <NomRespons>John Doe 02</NomRespons>
                    <EndEletrnc>john.doe.02@test.com</EndEletrnc>
                    <NumTelRespons1>63987350515</NumTelRespons1>
                    <NumTelRespons2>6325324500</NumTelRespons2>
                    <TpRespons>M</TpRespons>
                </Grupo_GEN0019_Respons>
                <Hist>GEN0019 Description Test</Hist>
                <DtMovto>2026-02-11</DtMovto>
            </GEN0019>
        </SISMSG>
    </DOC>
    """
    assert normalize_xml(expected_xml) == normalize_xml(xml)


def test_gen0019_from_xml() -> None:
    xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/GEN/GEN0019.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>31680151250908000000001</NUOp>
        </BCMSG>
        <SISMSG>
            <GEN0019>
                <CodMsg>GEN0019</CodMsg>
                <NumCtrlPart>123</NumCtrlPart>
                <ISPBPart>31680151</ISPBPart>
                <Grupo_GEN0019_Respons>
                    <CPFRespons>05046528002</CPFRespons>
                    <NumDocRespons>398127955</NumDocRespons>
                    <NomRespons>John Doe 01</NomRespons>
                    <EndEletrnc>john.doe.01@test.com</EndEletrnc>
                    <NumTelRespons1>65994861321</NumTelRespons1>
                    <NumTelRespons2>6537132095</NumTelRespons2>
                    <TpRespons>D</TpRespons>
                </Grupo_GEN0019_Respons>
                <Grupo_GEN0019_Respons>
                    <CPFRespons>30288815009</CPFRespons>
                    <NumDocRespons>151058246</NumDocRespons>
                    <NomRespons>John Doe 02</NomRespons>
                    <EndEletrnc>john.doe.02@test.com</EndEletrnc>
                    <NumTelRespons1>63987350515</NumTelRespons1>
                    <NumTelRespons2>6325324500</NumTelRespons2>
                    <TpRespons>M</TpRespons>
                </Grupo_GEN0019_Respons>
                <Hist>GEN0019 Description Test</Hist>
                <DtMovto>2026-02-11</DtMovto>
            </GEN0019>
        </SISMSG>
    </DOC>
    """

    gen0019 = GEN0019.from_xml(xml)

    assert isinstance(gen0019, GEN0019)
    assert gen0019.from_ispb == '31680151'
    assert gen0019.to_ispb == '00038166'
    assert gen0019.system_domain == 'SPB01'
    assert gen0019.operation_number == '31680151250908000000001'
    assert gen0019.message_code == 'GEN0019'
    assert gen0019.participant_institution_control_number == '123'
    assert gen0019.participant_ispb == '31680151'
    assert gen0019.description == 'GEN0019 Description Test'
    assert gen0019.settlement_date == date(2026, 2, 11)

    assert len(gen0019.responsibles) == RESPONSIBLE_SIZE
    resp1 = gen0019.responsibles[0]
    resp2 = gen0019.responsibles[1]
    assert isinstance(resp1, Responsible)
    assert resp1.cpf == '05046528002'
    assert resp1.telephone_1 == '65994861321'
    assert isinstance(resp2, Responsible)
    assert resp2.cpf == '30288815009'
    assert resp2.telephone_1 == '63987350515'


def test_gen0019r1_from_xml() -> None:
    xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/GEN/GEN0019.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>31680151250908000000001</NUOp>
        </BCMSG>
        <SISMSG>
            <GEN0019R1>
                <CodMsg>GEN0019R1</CodMsg>
                <NumCtrlPart>123</NumCtrlPart>
                <ISPBPart>31680151</ISPBPart>
                <DtHrPrestd>2026-02-11T18:47:23</DtHrPrestd>
                <DtMovto>2026-02-11</DtMovto>
            </GEN0019R1>
        </SISMSG>
    </DOC>
    """

    gen0019r1 = GEN0019R1.from_xml(xml)

    assert isinstance(gen0019r1, GEN0019R1)
    assert gen0019r1.from_ispb == '31680151'
    assert gen0019r1.to_ispb == '00038166'
    assert gen0019r1.system_domain == 'SPB01'
    assert gen0019r1.operation_number == '31680151250908000000001'
    assert gen0019r1.message_code == 'GEN0019R1'
    assert gen0019r1.participant_institution_control_number == '123'
    assert gen0019r1.participant_ispb == '31680151'
    assert gen0019r1.provider_datetime == datetime(2026, 2, 11, 18, 47, 23)
    assert gen0019r1.settlement_date == date(2026, 2, 11)


def test_gen0019e_general_error_from_xml() -> None:
    xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/GEN/GEN0019E.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>31680151250908000000001</NUOp>
        </BCMSG>
        <SISMSG>
            <GEN0019 CodErro="EGEN0050">
                <CodMsg>GEN0019E</CodMsg>
                <NumCtrlPart>123</NumCtrlPart>
                <ISPBPart>31680151</ISPBPart>
                <Grupo_GEN0019_Respons>
                    <CPFRespons>05046528002</CPFRespons>
                    <NumDocRespons>398127955</NumDocRespons>
                    <NomRespons>John Doe 01</NomRespons>
                    <EndEletrnc>john.doe.01@test.com</EndEletrnc>
                    <NumTelRespons1>65994861321</NumTelRespons1>
                    <NumTelRespons2>6537132095</NumTelRespons2>
                    <TpRespons>D</TpRespons>
                </Grupo_GEN0019_Respons>
                <Grupo_GEN0019_Respons>
                    <CPFRespons>30288815009</CPFRespons>
                    <NumDocRespons>151058246</NumDocRespons>
                    <NomRespons>John Doe 02</NomRespons>
                    <EndEletrnc>john.doe.02@test.com</EndEletrnc>
                    <NumTelRespons1>63987350515</NumTelRespons1>
                    <NumTelRespons2>6325324500</NumTelRespons2>
                    <TpRespons>M</TpRespons>
                </Grupo_GEN0019_Respons>
                <Hist>GEN0019 Description Test</Hist>
                <DtMovto>2026-02-11</DtMovto>
            </GEN0019>
        </SISMSG>
    </DOC>
    """

    gen0019e = GEN0019E.from_xml(xml)

    assert isinstance(gen0019e, GEN0019E)
    assert gen0019e.from_ispb == '31680151'
    assert gen0019e.to_ispb == '00038166'
    assert gen0019e.system_domain == 'SPB01'
    assert gen0019e.operation_number == '31680151250908000000001'
    assert gen0019e.message_code == 'GEN0019E'
    assert gen0019e.participant_institution_control_number == '123'
    assert gen0019e.participant_ispb == '31680151'
    assert gen0019e.description == 'GEN0019 Description Test'
    assert gen0019e.settlement_date == date(2026, 2, 11)
    assert gen0019e.general_error_code == 'EGEN0050'

    assert len(gen0019e.responsibles) == RESPONSIBLE_SIZE
    resp1 = gen0019e.responsibles[0]
    resp2 = gen0019e.responsibles[1]
    assert isinstance(resp1, ResponsibleError)
    assert resp1.cpf == '05046528002'
    assert resp1.telephone_1 == '65994861321'
    assert isinstance(resp2, ResponsibleError)
    assert resp2.cpf == '30288815009'
    assert resp2.telephone_1 == '63987350515'


def test_gen0019e_tag_error_from_xml() -> None:
    xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/GEN/GEN0019E.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>31680151250908000000001</NUOp>
        </BCMSG>
        <SISMSG>
            <GEN0019>
                <CodMsg>GEN0019E</CodMsg>
                <NumCtrlPart>123</NumCtrlPart>
                <ISPBPart CodErro="EGEN0051">31680151</ISPBPart>
                <Grupo_GEN0019_Respons>
                    <CPFRespons>05046528002</CPFRespons>
                    <NumDocRespons>398127955</NumDocRespons>
                    <NomRespons>John Doe 01</NomRespons>
                    <EndEletrnc>john.doe.01@test.com</EndEletrnc>
                    <NumTelRespons1>65994861321</NumTelRespons1>
                    <NumTelRespons2>6537132095</NumTelRespons2>
                    <TpRespons>D</TpRespons>
                </Grupo_GEN0019_Respons>
                <Grupo_GEN0019_Respons>
                    <CPFRespons>30288815009</CPFRespons>
                    <NumDocRespons>151058246</NumDocRespons>
                    <NomRespons>John Doe 02</NomRespons>
                    <EndEletrnc>john.doe.02@test.com</EndEletrnc>
                    <NumTelRespons1>63987350515</NumTelRespons1>
                    <NumTelRespons2>6325324500</NumTelRespons2>
                    <TpRespons>M</TpRespons>
                </Grupo_GEN0019_Respons>
                <Hist>GEN0019 Description Test</Hist>
                <DtMovto>2026-02-11</DtMovto>
            </GEN0019>
        </SISMSG>
    </DOC>
    """

    gen0019e = GEN0019E.from_xml(xml)

    assert isinstance(gen0019e, GEN0019E)
    assert gen0019e.from_ispb == '31680151'
    assert gen0019e.to_ispb == '00038166'
    assert gen0019e.system_domain == 'SPB01'
    assert gen0019e.operation_number == '31680151250908000000001'
    assert gen0019e.message_code == 'GEN0019E'
    assert gen0019e.participant_institution_control_number == '123'
    assert gen0019e.participant_ispb == '31680151'
    assert gen0019e.description == 'GEN0019 Description Test'
    assert gen0019e.settlement_date == date(2026, 2, 11)
    assert gen0019e.participant_ispb_error_code == 'EGEN0051'

    assert len(gen0019e.responsibles) == RESPONSIBLE_SIZE
    resp1 = gen0019e.responsibles[0]
    resp2 = gen0019e.responsibles[1]
    assert isinstance(resp1, ResponsibleError)
    assert resp1.cpf == '05046528002'
    assert resp1.telephone_1 == '65994861321'
    assert isinstance(resp2, ResponsibleError)
    assert resp2.cpf == '30288815009'
    assert resp2.telephone_1 == '63987350515'


def test_gen0019_roundtrip() -> None:
    params = make_valid_gen0019_params()

    gen0019 = GEN0019.model_validate(params)
    xml = gen0019.to_xml()
    gen0019_from_xml = GEN0019.from_xml(xml)

    assert gen0019 == gen0019_from_xml


def test_gen0019r1_roundtrip() -> None:
    params = make_valid_gen0019r1_params()

    gen0019r1 = GEN0019R1.model_validate(params)
    xml = gen0019r1.to_xml()
    gen0019r1_from_xml = GEN0019R1.from_xml(xml)

    assert gen0019r1 == gen0019r1_from_xml


def test_gen0019_from_xml_missing_required_fields() -> None:
    xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/GEN/GEN0019.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>31680151250908000000001</NUOp>
        </BCMSG>
        <SISMSG>
            <GEN0019>
                <CodMsg>GEN0019</CodMsg>
            </GEN0019>
        </SISMSG>
    </DOC>
    """

    with pytest.raises(ValidationError) as exc:
        GEN0019.from_xml(xml)

    missing_fields = extract_missing_fields(exc.value)
    assert missing_fields == {
        'participant_institution_control_number',
        'participant_ispb',
        'settlement_date',
    }
