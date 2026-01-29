from datetime import date, datetime
from typing import Any

import pytest
from pydantic import ValidationError

from sfn_messages.core.types import GridCode, TimeType
from sfn_messages.str.str0001 import STR0001, STR0001E, STR0001R1, ScheduleGrid
from tests.conftest import extract_missing_fields, normalize_xml


def make_valid_str0001_params() -> dict[str, Any]:
    return {
        'from_ispb': '31680151',
        'to_ispb': '00038166',
        'system_domain': 'SPB01',
        'operation_number': '31680151250908000000001',
        'message_code': 'STR0001',
        'institution_control_number': '31680151202509090425',
        'institution_ispb': '31680151',
        'reference_date': '2026-01-28',
        'hour_type': 'STANDARD',
    }


def make_valid_str0001r1_params() -> dict[str, Any]:
    return {
        'from_ispb': '31680151',
        'to_ispb': '00038166',
        'system_domain': 'SPB01',
        'operation_number': '31680151250908000000001',
        'message_code': 'STR0001R1',
        'institution_control_number': '31680151202509090425',
        'institution_ispb': '31680151',
        'schedule_grid_group': [
            {
                'code': 'PAYMENT_ORDER_SCHEDULING',
                'opening_hour': '2026-01-28T09:30:00',
                'closing_hour': '2026-01-28T18:30:00',
                'hour_type': 'STANDARD',
            }
        ],
        'reference_date': '2026-01-28',
        'vendor_timestamp': '2026-01-28T16:30:21',
    }


def make_valid_str0001e_params(*, general_error: bool = False) -> dict[str, Any]:
    str0001e = {
        'from_ispb': '31680151',
        'to_ispb': '00038166',
        'system_domain': 'SPB01',
        'operation_number': '31680151250908000000001',
        'message_code': 'STR0001E',
        'institution_control_number': '31680151202509090425',
        'institution_ispb': '31680151',
        'reference_date': '2026-01-28',
        'hour_type': 'STANDARD',
    }

    if general_error:
        str0001e['general_error_code'] = 'EGEN0050'
    else:
        str0001e['reference_date_error_code'] = 'EIDT0001'

    return str0001e


def test_str0001_valid_params() -> None:
    params = make_valid_str0001_params()
    str0001 = STR0001.model_validate(params)

    assert isinstance(str0001, STR0001)
    assert str0001.from_ispb == '31680151'
    assert str0001.operation_number == '31680151250908000000001'
    assert str0001.system_domain == 'SPB01'
    assert str0001.to_ispb == '00038166'
    assert str0001.message_code == 'STR0001'
    assert str0001.institution_control_number == '31680151202509090425'
    assert str0001.institution_ispb == '31680151'
    assert str0001.reference_date == date(2026, 1, 28)
    assert str0001.hour_type == TimeType.STANDARD


def test_str0001r1_valid_params() -> None:
    params = make_valid_str0001r1_params()
    str0001r1 = STR0001R1.model_validate(params)

    assert isinstance(str0001r1, STR0001R1)
    assert str0001r1.from_ispb == '31680151'
    assert str0001r1.operation_number == '31680151250908000000001'
    assert str0001r1.system_domain == 'SPB01'
    assert str0001r1.to_ispb == '00038166'
    assert str0001r1.message_code == 'STR0001R1'
    assert str0001r1.institution_control_number == '31680151202509090425'
    assert str0001r1.institution_ispb == '31680151'
    assert str0001r1.reference_date == date(2026, 1, 28)
    assert str0001r1.vendor_timestamp == datetime(2026, 1, 28, 16, 30, 21)

    assert len(str0001r1.schedule_grid_group) == 1
    schedule1 = str0001r1.schedule_grid_group[0]
    assert isinstance(schedule1, ScheduleGrid)
    assert schedule1.code == GridCode.PAYMENT_ORDER_SCHEDULING
    assert schedule1.opening_hour == datetime(2026, 1, 28, 9, 30)
    assert schedule1.closing_hour == datetime(2026, 1, 28, 18, 30)
    assert schedule1.hour_type == TimeType.STANDARD


def test_str0001e_general_error_valid_params() -> None:
    params = make_valid_str0001e_params(general_error=True)
    str0001e = STR0001E.model_validate(params)

    assert isinstance(str0001e, STR0001E)
    assert str0001e.from_ispb == '31680151'
    assert str0001e.operation_number == '31680151250908000000001'
    assert str0001e.system_domain == 'SPB01'
    assert str0001e.to_ispb == '00038166'
    assert str0001e.message_code == 'STR0001E'
    assert str0001e.institution_control_number == '31680151202509090425'
    assert str0001e.institution_ispb == '31680151'
    assert str0001e.reference_date == date(2026, 1, 28)
    assert str0001e.hour_type == TimeType.STANDARD
    assert str0001e.general_error_code == 'EGEN0050'


def test_str0001e_tag_error_valid_params() -> None:
    params = make_valid_str0001e_params()
    str0001e = STR0001E.model_validate(params)

    assert isinstance(str0001e, STR0001E)
    assert str0001e.from_ispb == '31680151'
    assert str0001e.operation_number == '31680151250908000000001'
    assert str0001e.system_domain == 'SPB01'
    assert str0001e.to_ispb == '00038166'
    assert str0001e.message_code == 'STR0001E'
    assert str0001e.institution_control_number == '31680151202509090425'
    assert str0001e.institution_ispb == '31680151'
    assert str0001e.reference_date == date(2026, 1, 28)
    assert str0001e.hour_type == TimeType.STANDARD
    assert str0001e.reference_date_error_code == 'EIDT0001'


def test_str0001_missing_required_fields() -> None:
    with pytest.raises(ValidationError) as exc:
        STR0001.model_validate({})
    missing_fields = extract_missing_fields(exc.value)
    assert missing_fields == {
        'from_ispb',
        'operation_number',
        'system_domain',
        'to_ispb',
        'institution_control_number',
        'institution_ispb',
        'reference_date',
        'hour_type',
    }


def test_str0001r1_missing_required_fields() -> None:
    with pytest.raises(ValidationError) as exc:
        STR0001.model_validate({})
    missing_fields = extract_missing_fields(exc.value)
    assert missing_fields == {
        'from_ispb',
        'operation_number',
        'system_domain',
        'to_ispb',
        'institution_control_number',
        'institution_ispb',
        'reference_date',
        'hour_type',
    }


def test_str0001_to_xml() -> None:
    params = make_valid_str0001_params()
    str0001 = STR0001.model_validate(params)
    xml = str0001.to_xml()

    expected_xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/SPB/STR0001.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>31680151250908000000001</NUOp>
        </BCMSG>
        <SISMSG>
            <STR0001>
                <CodMsg>STR0001</CodMsg>
                <NumCtrlIF>31680151202509090425</NumCtrlIF>
                <ISPBIF>31680151</ISPBIF>
                <DtRef>2026-01-28</DtRef>
                <TpHrio>P</TpHrio>
            </STR0001>
        </SISMSG>
    </DOC>
    """

    assert normalize_xml(expected_xml) == normalize_xml(xml)


def test_str0001r1_to_xml() -> None:
    params = make_valid_str0001r1_params()
    str0001r1 = STR0001R1.model_validate(params)
    xml = str0001r1.to_xml()

    expected_xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/SPB/STR0001.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>31680151250908000000001</NUOp>
        </BCMSG>
        <SISMSG>
            <STR0001R1>
                <CodMsg>STR0001R1</CodMsg>
                <NumCtrlIF>31680151202509090425</NumCtrlIF>
                <ISPBIF>31680151</ISPBIF>
                <Grupo_STR0001R1_GrdHrio>
                    <CodGrd>AGE01</CodGrd>
                    <DtHrAbert>2026-01-28T09:30:00</DtHrAbert>
                    <DtHrFcht>2026-01-28T18:30:00</DtHrFcht>
                    <TpHrio>P</TpHrio>
                </Grupo_STR0001R1_GrdHrio>
                <DtRef>2026-01-28</DtRef>
                <DtHrBC>2026-01-28T16:30:21</DtHrBC>
            </STR0001R1>
        </SISMSG>
    </DOC>
    """

    assert normalize_xml(expected_xml) == normalize_xml(xml)


def test_str0001e_general_error_to_xml() -> None:
    params = make_valid_str0001e_params(general_error=True)
    str0001e = STR0001E.model_validate(params)
    xml = str0001e.to_xml()

    expected_xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/SPB/STR0001E.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>31680151250908000000001</NUOp>
        </BCMSG>
        <SISMSG>
            <STR0001 CodErro="EGEN0050">
                <CodMsg>STR0001E</CodMsg>
                <NumCtrlIF>31680151202509090425</NumCtrlIF>
                <ISPBIF>31680151</ISPBIF>
                <DtRef>2026-01-28</DtRef>
                <TpHrio>P</TpHrio>
            </STR0001>
        </SISMSG>
    </DOC>
    """

    assert normalize_xml(expected_xml) == normalize_xml(xml)


def test_str0001e_tag_error_to_xml() -> None:
    params = make_valid_str0001e_params()
    str0001e = STR0001E.model_validate(params)
    xml = str0001e.to_xml()

    expected_xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/SPB/STR0001E.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>31680151250908000000001</NUOp>
        </BCMSG>
        <SISMSG>
            <STR0001>
                <CodMsg>STR0001E</CodMsg>
                <NumCtrlIF>31680151202509090425</NumCtrlIF>
                <ISPBIF>31680151</ISPBIF>
                <DtRef CodErro="EIDT0001">2026-01-28</DtRef>
                <TpHrio>P</TpHrio>
            </STR0001>
        </SISMSG>
    </DOC>
    """

    assert normalize_xml(expected_xml) == normalize_xml(xml)


def test_str0001_from_xml() -> None:
    xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/SPB/STR0001.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>31680151250908000000001</NUOp>
        </BCMSG>
        <SISMSG>
            <STR0001>
                <CodMsg>STR0001</CodMsg>
                <NumCtrlIF>31680151202509090425</NumCtrlIF>
                <ISPBIF>31680151</ISPBIF>
                <DtRef>2026-01-28</DtRef>
                <TpHrio>P</TpHrio>
            </STR0001>
        </SISMSG>
    </DOC>
    """

    str0001 = STR0001.from_xml(xml)

    assert isinstance(str0001, STR0001)
    assert str0001.from_ispb == '31680151'
    assert str0001.operation_number == '31680151250908000000001'
    assert str0001.system_domain == 'SPB01'
    assert str0001.to_ispb == '00038166'
    assert str0001.message_code == 'STR0001'
    assert str0001.institution_control_number == '31680151202509090425'
    assert str0001.institution_ispb == '31680151'
    assert str0001.reference_date == date(2026, 1, 28)
    assert str0001.hour_type == TimeType.STANDARD


def test_str0001r1_from_xml() -> None:
    xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/SPB/STR0001.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>31680151250908000000001</NUOp>
        </BCMSG>
        <SISMSG>
            <STR0001R1>
                <CodMsg>STR0001R1</CodMsg>
                <NumCtrlIF>31680151202509090425</NumCtrlIF>
                <ISPBIF>31680151</ISPBIF>
                <Grupo_STR0001R1_GrdHrio>
                    <CodGrd>AGE01</CodGrd>
                    <DtHrAbert>2026-01-28T09:30:00</DtHrAbert>
                    <DtHrFcht>2026-01-28T18:30:00</DtHrFcht>
                    <TpHrio>P</TpHrio>
                </Grupo_STR0001R1_GrdHrio>
                <DtRef>2026-01-28</DtRef>
                <DtHrBC>2026-01-28T16:30:21</DtHrBC>
            </STR0001R1>
        </SISMSG>
    </DOC>
    """

    str0001r1 = STR0001R1.from_xml(xml)

    assert isinstance(str0001r1, STR0001R1)
    assert str0001r1.from_ispb == '31680151'
    assert str0001r1.operation_number == '31680151250908000000001'
    assert str0001r1.system_domain == 'SPB01'
    assert str0001r1.to_ispb == '00038166'
    assert str0001r1.message_code == 'STR0001R1'
    assert str0001r1.institution_control_number == '31680151202509090425'
    assert str0001r1.institution_ispb == '31680151'
    assert str0001r1.reference_date == date(2026, 1, 28)
    assert str0001r1.vendor_timestamp == datetime(2026, 1, 28, 16, 30, 21)

    assert len(str0001r1.schedule_grid_group) == 1
    schedule1 = str0001r1.schedule_grid_group[0]
    assert isinstance(schedule1, ScheduleGrid)
    assert schedule1.code == GridCode.PAYMENT_ORDER_SCHEDULING
    assert schedule1.opening_hour == datetime(2026, 1, 28, 9, 30)
    assert schedule1.closing_hour == datetime(2026, 1, 28, 18, 30)
    assert schedule1.hour_type == TimeType.STANDARD


def test_str0001e_general_error_from_xml() -> None:
    xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/SPB/STR0001E.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>31680151250908000000001</NUOp>
        </BCMSG>
        <SISMSG>
            <STR0001 CodErro="EGEN0050">
                <CodMsg>STR0001E</CodMsg>
                <NumCtrlIF>31680151202509090425</NumCtrlIF>
                <ISPBIF>31680151</ISPBIF>
                <DtRef>2026-01-28</DtRef>
                <TpHrio>P</TpHrio>
            </STR0001>
        </SISMSG>
    </DOC>
    """

    str0001e = STR0001E.from_xml(xml)

    assert isinstance(str0001e, STR0001E)
    assert str0001e.from_ispb == '31680151'
    assert str0001e.operation_number == '31680151250908000000001'
    assert str0001e.system_domain == 'SPB01'
    assert str0001e.to_ispb == '00038166'
    assert str0001e.message_code == 'STR0001E'
    assert str0001e.institution_control_number == '31680151202509090425'
    assert str0001e.institution_ispb == '31680151'
    assert str0001e.reference_date == date(2026, 1, 28)
    assert str0001e.hour_type == TimeType.STANDARD
    assert str0001e.general_error_code == 'EGEN0050'


def test_str0001e_tag_error_from_xml() -> None:
    xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/SPB/STR0001E.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>31680151250908000000001</NUOp>
        </BCMSG>
        <SISMSG>
            <STR0001>
                <CodMsg>STR0001E</CodMsg>
                <NumCtrlIF>31680151202509090425</NumCtrlIF>
                <ISPBIF>31680151</ISPBIF>
                <DtRef CodErro="EIDT0001">2026-01-28</DtRef>
                <TpHrio>P</TpHrio>
            </STR0001>
        </SISMSG>
    </DOC>
    """

    str0001e = STR0001E.from_xml(xml)

    assert isinstance(str0001e, STR0001E)
    assert str0001e.from_ispb == '31680151'
    assert str0001e.operation_number == '31680151250908000000001'
    assert str0001e.system_domain == 'SPB01'
    assert str0001e.to_ispb == '00038166'
    assert str0001e.message_code == 'STR0001E'
    assert str0001e.institution_control_number == '31680151202509090425'
    assert str0001e.institution_ispb == '31680151'
    assert str0001e.reference_date == date(2026, 1, 28)
    assert str0001e.hour_type == TimeType.STANDARD
    assert str0001e.reference_date_error_code == 'EIDT0001'


def test_str0001_roundtrip() -> None:
    params = make_valid_str0001_params()
    str0001 = STR0001.model_validate(params)
    xml = str0001.to_xml()
    str0001_from_xml = STR0001.from_xml(xml)
    assert str0001 == str0001_from_xml


def test_str0001r1_roundtrip() -> None:
    params = make_valid_str0001r1_params()
    str0001r1 = STR0001R1.model_validate(params)
    xml = str0001r1.to_xml()
    str0001r1_from_xml = STR0001R1.from_xml(xml)
    assert str0001r1 == str0001r1_from_xml


def test_str0001_from_xml_missing_required_fields() -> None:
    xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/SPB/STR0001.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>31680151250908000000001</NUOp>
        </BCMSG>
        <SISMSG>
            <STR0001>
                <CodMsg>STR0001</CodMsg>
            </STR0001>
        </SISMSG>
    </DOC>
    """

    with pytest.raises(ValidationError) as exc:
        STR0001.from_xml(xml)

    missing_fields = extract_missing_fields(exc.value)
    assert missing_fields == {
        'institution_control_number',
        'institution_ispb',
        'reference_date',
        'hour_type',
    }


def test_str0001r1_from_xml_missing_required_fields() -> None:
    xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/SPB/STR0001.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>31680151250908000000001</NUOp>
        </BCMSG>
        <SISMSG>
            <STR0001R1>
                <CodMsg>STR0001R1</CodMsg>
            </STR0001R1>
        </SISMSG>
    </DOC>
    """

    with pytest.raises(ValidationError) as exc:
        STR0001R1.from_xml(xml)

    missing_fields = extract_missing_fields(exc.value)
    assert missing_fields == {
        'institution_control_number',
        'institution_ispb',
        'reference_date',
        'vendor_timestamp',
    }
