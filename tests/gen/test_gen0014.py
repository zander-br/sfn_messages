from datetime import UTC, date, datetime
from typing import Any

import pytest
from pydantic import ValidationError

from sfn_messages.gen.gen0014 import GEN0014, GEN0014E, GEN0014R1
from sfn_messages.gen.types import TransmissionType
from tests.conftest import extract_missing_fields, normalize_xml


def make_valid_gen0014_params() -> dict[str, Any]:
    return {
        'from_ispb': '31680151',
        'to_ispb': '00038166',
        'system_domain': 'SPB01',
        'operation_number': '316801512509080000001',
        'message_code': 'GEN0014',
        'institution_control_number': '123',
        'issuing_ispb': '31680151',
        'recipient_ispb': '31680151',
        'file_name': 'Test file name',
        'selection_criteria': 'Criteria message',
        'transmission_type': 'USERMSG_ATTACHED',
        'settlement_date': '2025-11-27',
    }


def make_valid_gen0014r1_params() -> dict[str, Any]:
    return {
        'from_ispb': '31680151',
        'to_ispb': '00038166',
        'system_domain': 'SPB01',
        'operation_number': '316801512509080000001',
        'message_code': 'GEN0014R1',
        'institution_control_number': '123',
        'institution_request_control_number': '123',
        'institution_ispb': '31680151',
        'institution_datetime': '2025-11-27T10:02:00+00:00',
        'settlement_date': '2025-11-27',
    }


def make_valid_gen0014e_params(*, general_error: bool = False) -> dict[str, Any]:
    gen0014e = {
        'from_ispb': '31680151',
        'to_ispb': '00038166',
        'system_domain': 'SPB01',
        'operation_number': '316801512509080000001',
        'message_code': 'GEN0014',
        'institution_control_number': '123',
        'issuing_ispb': '31680151',
        'recipient_ispb': '31680151',
        'file_name': 'Test file name',
        'selection_criteria': 'Criteria message',
        'transmission_type': 'USERMSG_ATTACHED',
        'settlement_date': '2025-11-27',
    }

    if general_error:
        gen0014e['general_error_code'] = 'EGEN0050'
    else:
        gen0014e['issuing_ispb_error_code'] = 'EGEN0051'

    return gen0014e


def test_gen0014_valid_model() -> None:
    params = make_valid_gen0014_params()
    gen0014 = GEN0014.model_validate(params)

    assert isinstance(gen0014, GEN0014)
    assert gen0014.from_ispb == '31680151'
    assert gen0014.to_ispb == '00038166'
    assert gen0014.message_code == 'GEN0014'
    assert gen0014.institution_control_number == '123'
    assert gen0014.issuing_ispb == '31680151'
    assert gen0014.recipient_ispb == '31680151'
    assert gen0014.file_name == 'Test file name'
    assert gen0014.selection_criteria == 'Criteria message'
    assert gen0014.transmission_type == TransmissionType.USERMSG_ATTACHED
    assert gen0014.settlement_date == date(2025, 11, 27)


def test_gen0014r1_valid_model() -> None:
    params = make_valid_gen0014r1_params()
    gen0014r1 = GEN0014R1.model_validate(params)

    assert isinstance(gen0014r1, GEN0014R1)
    assert gen0014r1.from_ispb == '31680151'
    assert gen0014r1.to_ispb == '00038166'
    assert gen0014r1.message_code == 'GEN0014R1'
    assert gen0014r1.institution_control_number == '123'
    assert gen0014r1.institution_request_control_number == '123'
    assert gen0014r1.institution_ispb == '31680151'
    assert gen0014r1.institution_datetime == datetime(2025, 11, 27, 10, 2, tzinfo=UTC)
    assert gen0014r1.settlement_date == date(2025, 11, 27)


def test_gen0014e_general_error_valid_model() -> None:
    params = make_valid_gen0014e_params(general_error=True)
    gen0014e = GEN0014E.model_validate(params)

    assert isinstance(gen0014e, GEN0014E)
    assert gen0014e.from_ispb == '31680151'
    assert gen0014e.to_ispb == '00038166'
    assert gen0014e.message_code == 'GEN0014'
    assert gen0014e.institution_control_number == '123'
    assert gen0014e.issuing_ispb == '31680151'
    assert gen0014e.recipient_ispb == '31680151'
    assert gen0014e.file_name == 'Test file name'
    assert gen0014e.selection_criteria == 'Criteria message'
    assert gen0014e.transmission_type == TransmissionType.USERMSG_ATTACHED
    assert gen0014e.settlement_date == date(2025, 11, 27)
    assert gen0014e.general_error_code == 'EGEN0050'


def test_gen0014e_tag_error_valid_model() -> None:
    params = make_valid_gen0014e_params()
    gen0014e = GEN0014E.model_validate(params)

    assert isinstance(gen0014e, GEN0014E)
    assert gen0014e.from_ispb == '31680151'
    assert gen0014e.to_ispb == '00038166'
    assert gen0014e.message_code == 'GEN0014'
    assert gen0014e.institution_control_number == '123'
    assert gen0014e.issuing_ispb == '31680151'
    assert gen0014e.recipient_ispb == '31680151'
    assert gen0014e.file_name == 'Test file name'
    assert gen0014e.selection_criteria == 'Criteria message'
    assert gen0014e.transmission_type == TransmissionType.USERMSG_ATTACHED
    assert gen0014e.settlement_date == date(2025, 11, 27)
    assert gen0014e.issuing_ispb_error_code == 'EGEN0051'


def test_gen0014_missing_required_fields() -> None:
    with pytest.raises(ValidationError) as exc:
        GEN0014.model_validate({})

    missing_fields = extract_missing_fields(exc.value)
    assert missing_fields == {
        'from_ispb',
        'to_ispb',
        'system_domain',
        'operation_number',
        'institution_control_number',
        'issuing_ispb',
        'recipient_ispb',
        'file_name',
        'transmission_type',
        'settlement_date',
    }


def test_gen0014r1_missing_required_fields() -> None:
    with pytest.raises(ValidationError) as exc:
        GEN0014R1.model_validate({})

    missing_fields = extract_missing_fields(exc.value)
    assert missing_fields == {
        'from_ispb',
        'to_ispb',
        'system_domain',
        'operation_number',
        'institution_control_number',
        'institution_request_control_number',
        'institution_ispb',
        'institution_datetime',
        'settlement_date',
    }


def test_gen0014_to_xml() -> None:
    params = make_valid_gen0014_params()
    gen0014 = GEN0014.model_validate(params)

    xml = gen0014.to_xml()

    expected_xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/GEN/GEN0014.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>316801512509080000001</NUOp>
        </BCMSG>
        <SISMSG>
            <GEN0014>
                <CodMsg>GEN0014</CodMsg>
                <NumCtrlIF>123</NumCtrlIF>
                <ISPBEmissor>31680151</ISPBEmissor>
                <ISPBDestinatario>31680151</ISPBDestinatario>
                <NomArq>Test file name</NomArq>
                <CritSelec>Criteria message</CritSelec>
                <TpTransm>U</TpTransm>
                <DtMovto>2025-11-27</DtMovto>
            </GEN0014>
        </SISMSG>
    </DOC>
    """
    assert normalize_xml(expected_xml) == normalize_xml(xml)


def test_gen0014r1_to_xml() -> None:
    params = make_valid_gen0014r1_params()
    gen0014r1 = GEN0014R1.model_validate(params)

    xml = gen0014r1.to_xml()

    expected_xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/GEN/GEN0014.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>316801512509080000001</NUOp>
        </BCMSG>
        <SISMSG>
            <GEN0014R1>
                <CodMsg>GEN0014R1</CodMsg>
                <NumCtrlIF>123</NumCtrlIF>
                <NumCtrlReqIF>123</NumCtrlReqIF>
                <ISPBIF>31680151</ISPBIF>
                <DtHrIF>2025-11-27 10:02:00+00:00</DtHrIF>
                <DtMovto>2025-11-27</DtMovto>
            </GEN0014R1>
        </SISMSG>
    </DOC>
    """
    assert normalize_xml(expected_xml) == normalize_xml(xml)


def test_gen0014e_general_error_to_xml() -> None:
    params = make_valid_gen0014e_params(general_error=True)
    gen0014e = GEN0014E.model_validate(params)

    xml = gen0014e.to_xml()

    expected_xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/GEN/GEN0014E.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>316801512509080000001</NUOp>
        </BCMSG>
        <SISMSG>
            <GEN0014E CodErro="EGEN0050">
                <CodMsg>GEN0014</CodMsg>
                <NumCtrlIF>123</NumCtrlIF>
                <ISPBEmissor>31680151</ISPBEmissor>
                <ISPBDestinatario>31680151</ISPBDestinatario>
                <NomArq>Test file name</NomArq>
                <CritSelec>Criteria message</CritSelec>
                <TpTransm>U</TpTransm>
                <DtMovto>2025-11-27</DtMovto>
            </GEN0014E>
        </SISMSG>
    </DOC>
    """
    assert normalize_xml(expected_xml) == normalize_xml(xml)


def test_gen0014e_tag_error_to_xml() -> None:
    params = make_valid_gen0014e_params()
    gen0014e = GEN0014E.model_validate(params)

    xml = gen0014e.to_xml()

    expected_xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/GEN/GEN0014E.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>316801512509080000001</NUOp>
        </BCMSG>
        <SISMSG>
            <GEN0014E>
                <CodMsg>GEN0014</CodMsg>
                <NumCtrlIF>123</NumCtrlIF>
                <ISPBEmissor CodErro="EGEN0051">31680151</ISPBEmissor>
                <ISPBDestinatario>31680151</ISPBDestinatario>
                <NomArq>Test file name</NomArq>
                <CritSelec>Criteria message</CritSelec>
                <TpTransm>U</TpTransm>
                <DtMovto>2025-11-27</DtMovto>
            </GEN0014E>
        </SISMSG>
    </DOC>
    """
    assert normalize_xml(expected_xml) == normalize_xml(xml)


def test_gen0014_from_xml() -> None:
    xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/GEN/GEN0014.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>316801512509080000001</NUOp>
        </BCMSG>
        <SISMSG>
            <GEN0014>
                <CodMsg>GEN0014</CodMsg>
                <NumCtrlIF>123</NumCtrlIF>
                <ISPBEmissor>31680151</ISPBEmissor>
                <ISPBDestinatario>31680151</ISPBDestinatario>
                <NomArq>Test file name</NomArq>
                <CritSelec>Criteria message</CritSelec>
                <TpTransm>U</TpTransm>
                <DtMovto>2025-11-27</DtMovto>
            </GEN0014>
        </SISMSG>
    </DOC>
    """

    gen0014 = GEN0014.from_xml(xml)

    assert isinstance(gen0014, GEN0014)
    assert gen0014.from_ispb == '31680151'
    assert gen0014.to_ispb == '00038166'
    assert gen0014.message_code == 'GEN0014'
    assert gen0014.institution_control_number == '123'
    assert gen0014.issuing_ispb == '31680151'
    assert gen0014.recipient_ispb == '31680151'
    assert gen0014.file_name == 'Test file name'
    assert gen0014.selection_criteria == 'Criteria message'
    assert gen0014.transmission_type == TransmissionType.USERMSG_ATTACHED
    assert gen0014.settlement_date == date(2025, 11, 27)


def test_gen0014r1_from_xml() -> None:
    xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/GEN/GEN0014.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>316801512509080000001</NUOp>
        </BCMSG>
        <SISMSG>
            <GEN0014R1>
                <CodMsg>GEN0014R1</CodMsg>
                <NumCtrlIF>123</NumCtrlIF>
                <NumCtrlReqIF>123</NumCtrlReqIF>
                <ISPBIF>31680151</ISPBIF>
                <DtHrIF>2025-11-27 10:02:00+00:00</DtHrIF>
                <DtMovto>2025-11-27</DtMovto>
            </GEN0014R1>
        </SISMSG>
    </DOC>
    """

    gen0014r1 = GEN0014R1.from_xml(xml)

    assert isinstance(gen0014r1, GEN0014R1)
    assert gen0014r1.from_ispb == '31680151'
    assert gen0014r1.to_ispb == '00038166'
    assert gen0014r1.message_code == 'GEN0014R1'
    assert gen0014r1.institution_control_number == '123'
    assert gen0014r1.institution_request_control_number == '123'
    assert gen0014r1.institution_ispb == '31680151'
    assert gen0014r1.institution_datetime == datetime(2025, 11, 27, 10, 2, tzinfo=UTC)
    assert gen0014r1.settlement_date == date(2025, 11, 27)


def test_gen0014e_general_error_from_xml() -> None:
    xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/GEN/GEN0014E.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>316801512509080000001</NUOp>
        </BCMSG>
        <SISMSG>
            <GEN0014E CodErro="EGEN0050">
                <CodMsg>GEN0014</CodMsg>
                <NumCtrlIF>123</NumCtrlIF>
                <ISPBEmissor>31680151</ISPBEmissor>
                <ISPBDestinatario>31680151</ISPBDestinatario>
                <NomArq>Test file name</NomArq>
                <CritSelec>Criteria message</CritSelec>
                <TpTransm>U</TpTransm>
                <DtMovto>2025-11-27</DtMovto>
            </GEN0014E>
        </SISMSG>
    </DOC>
    """

    gen0014e = GEN0014E.from_xml(xml)

    assert isinstance(gen0014e, GEN0014E)
    assert gen0014e.from_ispb == '31680151'
    assert gen0014e.to_ispb == '00038166'
    assert gen0014e.message_code == 'GEN0014'
    assert gen0014e.institution_control_number == '123'
    assert gen0014e.issuing_ispb == '31680151'
    assert gen0014e.recipient_ispb == '31680151'
    assert gen0014e.file_name == 'Test file name'
    assert gen0014e.selection_criteria == 'Criteria message'
    assert gen0014e.transmission_type == TransmissionType.USERMSG_ATTACHED
    assert gen0014e.settlement_date == date(2025, 11, 27)
    assert gen0014e.general_error_code == 'EGEN0050'


def test_gen0014e_tag_error_from_xml() -> None:
    xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/GEN/GEN0014E.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>316801512509080000001</NUOp>
        </BCMSG>
        <SISMSG>
            <GEN0014E>
                <CodMsg>GEN0014</CodMsg>
                <NumCtrlIF>123</NumCtrlIF>
                <ISPBEmissor CodErro="EGEN0051">31680151</ISPBEmissor>
                <ISPBDestinatario>31680151</ISPBDestinatario>
                <NomArq>Test file name</NomArq>
                <CritSelec>Criteria message</CritSelec>
                <TpTransm>U</TpTransm>
                <DtMovto>2025-11-27</DtMovto>
            </GEN0014E>
        </SISMSG>
    </DOC>
    """

    gen0014e = GEN0014E.from_xml(xml)

    assert isinstance(gen0014e, GEN0014E)
    assert gen0014e.from_ispb == '31680151'
    assert gen0014e.to_ispb == '00038166'
    assert gen0014e.message_code == 'GEN0014'
    assert gen0014e.institution_control_number == '123'
    assert gen0014e.issuing_ispb == '31680151'
    assert gen0014e.recipient_ispb == '31680151'
    assert gen0014e.file_name == 'Test file name'
    assert gen0014e.selection_criteria == 'Criteria message'
    assert gen0014e.transmission_type == TransmissionType.USERMSG_ATTACHED
    assert gen0014e.settlement_date == date(2025, 11, 27)
    assert gen0014e.issuing_ispb_error_code == 'EGEN0051'


def test_gen0014_roundtrip() -> None:
    params = make_valid_gen0014_params()

    gen0014 = GEN0014.model_validate(params)
    xml = gen0014.to_xml()
    gen0014_from_xml = GEN0014.from_xml(xml)

    assert gen0014 == gen0014_from_xml


def test_gen0014r1_roundtrip() -> None:
    params = make_valid_gen0014r1_params()

    gen0014r1 = GEN0014R1.model_validate(params)
    xml = gen0014r1.to_xml()
    gen0014r1_from_xml = GEN0014R1.from_xml(xml)

    assert gen0014r1 == gen0014r1_from_xml


def test_gen0014_from_xml_missing_required_fields() -> None:
    xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/GEN/GEN0014.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>316801512509080000001</NUOp>
        </BCMSG>
        <SISMSG>
            <GEN0014>
                <CodMsg>GEN0014</CodMsg>
            </GEN0014>
        </SISMSG>
    </DOC>
    """

    with pytest.raises(ValidationError) as exc:
        GEN0014.from_xml(xml)

    missing_fields = extract_missing_fields(exc.value)
    assert missing_fields == {
        'institution_control_number',
        'issuing_ispb',
        'recipient_ispb',
        'file_name',
        'transmission_type',
        'settlement_date',
    }


def test_gen0014r1_from_xml_missing_required_fields() -> None:
    xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/GEN/GEN0014.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>316801512509080000001</NUOp>
        </BCMSG>
        <SISMSG>
            <GEN0014R1>
                <CodMsg>GEN0014R1</CodMsg>
            </GEN0014R1>
        </SISMSG>
    </DOC>
    """

    with pytest.raises(ValidationError) as exc:
        GEN0014R1.from_xml(xml)

    missing_fields = extract_missing_fields(exc.value)
    assert missing_fields == {
        'institution_control_number',
        'institution_request_control_number',
        'institution_ispb',
        'institution_datetime',
        'settlement_date',
    }
