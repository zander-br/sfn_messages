from datetime import UTC, date, datetime
from typing import Any

import pytest
from pydantic import ValidationError

from sfn_messages.core.types import GridCode, ProductCode, TimeType
from sfn_messages.gen.gen0021 import GEN0021, GEN0021E, ScheduleGrid, ScheduleGridError
from tests.conftest import extract_missing_fields, normalize_xml

HOURS_SIZE = 2


def make_valid_gen0021_params() -> dict[str, Any]:
    return {
        'from_ispb': '31680151',
        'to_ispb': '00038166',
        'system_domain': 'SPB01',
        'operation_number': '316801512509080000001',
        'message_code': 'GEN0021',
        'provider_ispb': '31680151',
        'product_code': 'VISA_INTL_CREDIT_PURCHASE',
        'schedule_grid_group': [
            {
                'code': 'FX_PRIMARY_MARKET',
                'opening_hour': '2025-11-28T08:00:00+00:00',
                'closing_hour': '2025-11-28T18:30:00+00:00',
                'hour_type': 'STANDARD',
            },
            {
                'code': 'CBLC_PUBLIC_FIXED_INCOME_CLEARING',
                'opening_hour': '2025-11-28T08:00:00+00:00',
                'closing_hour': '2025-11-28T21:00:00+00:00',
                'hour_type': 'STANDARD',
            },
        ],
        'reference_date': '2025-11-28',
        'provider_datetime': '2025-11-28T16:01:00+00:00',
        'settlement_date': '2025-11-28',
    }


def make_valid_gen0021e_params(*, general_error: bool = False) -> dict[str, Any]:
    gen0021e: dict[str, Any] = {
        'from_ispb': '31680151',
        'to_ispb': '00038166',
        'system_domain': 'SPB01',
        'operation_number': '316801512509080000001',
        'message_code': 'GEN0021',
        'provider_ispb': '31680151',
        'product_code': 'VISA_INTL_CREDIT_PURCHASE',
        'schedule_grid_group': [
            {
                'code': 'FX_PRIMARY_MARKET',
                'opening_hour': '2025-11-28T08:00:00+00:00',
                'closing_hour': '2025-11-28T18:30:00+00:00',
                'hour_type': 'STANDARD',
            },
            {
                'code': 'CBLC_PUBLIC_FIXED_INCOME_CLEARING',
                'opening_hour': '2025-11-28T08:00:00+00:00',
                'closing_hour': '2025-11-28T21:00:00+00:00',
                'hour_type': 'STANDARD',
            },
        ],
        'reference_date': '2025-11-28',
        'provider_datetime': '2025-11-28T16:01:00+00:00',
        'settlement_date': '2025-11-28',
    }

    if general_error:
        gen0021e['general_error_code'] = 'EGEN0050'
    else:
        gen0021e['provider_ispb_error_code'] = 'EGEN0051'
        gen0021e['schedule_grid_group'][0]['code_error_code'] = 'EGEN0033'

    return gen0021e


def test_gen0021_valid_model() -> None:
    params = make_valid_gen0021_params()
    gen0021 = GEN0021.model_validate(params)

    assert isinstance(gen0021, GEN0021)
    assert gen0021.from_ispb == '31680151'
    assert gen0021.to_ispb == '00038166'
    assert gen0021.system_domain == 'SPB01'
    assert gen0021.operation_number == '316801512509080000001'
    assert gen0021.message_code == 'GEN0021'
    assert gen0021.provider_ispb == '31680151'
    assert gen0021.product_code == ProductCode.VISA_INTL_CREDIT_PURCHASE
    assert gen0021.reference_date == date(2025, 11, 28)
    assert gen0021.provider_datetime == datetime(2025, 11, 28, 16, 1, tzinfo=UTC)
    assert gen0021.settlement_date == date(2025, 11, 28)

    assert len(gen0021.schedule_grid_group) == HOURS_SIZE
    grid1 = gen0021.schedule_grid_group[0]
    grid2 = gen0021.schedule_grid_group[1]
    assert isinstance(grid1, ScheduleGrid)
    assert grid1.code == GridCode.FX_PRIMARY_MARKET
    assert grid1.opening_hour == datetime(2025, 11, 28, 8, 0, tzinfo=UTC)
    assert grid1.closing_hour == datetime(2025, 11, 28, 18, 30, tzinfo=UTC)
    assert grid1.hour_type == TimeType.STANDARD
    assert isinstance(grid2, ScheduleGrid)
    assert grid2.code == GridCode.CBLC_PUBLIC_FIXED_INCOME_CLEARING
    assert grid2.opening_hour == datetime(2025, 11, 28, 8, 0, tzinfo=UTC)
    assert grid2.closing_hour == datetime(2025, 11, 28, 21, 0, tzinfo=UTC)
    assert grid2.hour_type == TimeType.STANDARD


def test_gen0021e_general_error_valid_model() -> None:
    params = make_valid_gen0021e_params(general_error=True)
    gen0021e = GEN0021E.model_validate(params)

    assert isinstance(gen0021e, GEN0021E)
    assert gen0021e.from_ispb == '31680151'
    assert gen0021e.to_ispb == '00038166'
    assert gen0021e.system_domain == 'SPB01'
    assert gen0021e.operation_number == '316801512509080000001'
    assert gen0021e.message_code == 'GEN0021'
    assert gen0021e.provider_ispb == '31680151'
    assert gen0021e.product_code == ProductCode.VISA_INTL_CREDIT_PURCHASE
    assert gen0021e.reference_date == date(2025, 11, 28)
    assert gen0021e.provider_datetime == datetime(2025, 11, 28, 16, 1, tzinfo=UTC)
    assert gen0021e.settlement_date == date(2025, 11, 28)
    assert gen0021e.general_error_code == 'EGEN0050'

    assert len(gen0021e.schedule_grid_group) == HOURS_SIZE
    grid1 = gen0021e.schedule_grid_group[0]
    grid2 = gen0021e.schedule_grid_group[1]
    assert isinstance(grid1, ScheduleGridError)
    assert grid1.code == GridCode.FX_PRIMARY_MARKET
    assert grid1.opening_hour == datetime(2025, 11, 28, 8, 0, tzinfo=UTC)
    assert grid1.closing_hour == datetime(2025, 11, 28, 18, 30, tzinfo=UTC)
    assert grid1.hour_type == TimeType.STANDARD
    assert isinstance(grid2, ScheduleGridError)
    assert grid2.code == GridCode.CBLC_PUBLIC_FIXED_INCOME_CLEARING
    assert grid2.opening_hour == datetime(2025, 11, 28, 8, 0, tzinfo=UTC)
    assert grid2.closing_hour == datetime(2025, 11, 28, 21, 0, tzinfo=UTC)
    assert grid2.hour_type == TimeType.STANDARD


def test_gen0021e_tag_error_valid_model() -> None:
    params = make_valid_gen0021e_params()
    gen0021e = GEN0021E.model_validate(params)

    assert isinstance(gen0021e, GEN0021E)
    assert gen0021e.from_ispb == '31680151'
    assert gen0021e.to_ispb == '00038166'
    assert gen0021e.system_domain == 'SPB01'
    assert gen0021e.operation_number == '316801512509080000001'
    assert gen0021e.message_code == 'GEN0021'
    assert gen0021e.provider_ispb == '31680151'
    assert gen0021e.product_code == ProductCode.VISA_INTL_CREDIT_PURCHASE
    assert gen0021e.reference_date == date(2025, 11, 28)
    assert gen0021e.provider_datetime == datetime(2025, 11, 28, 16, 1, tzinfo=UTC)
    assert gen0021e.settlement_date == date(2025, 11, 28)
    assert gen0021e.provider_ispb_error_code == 'EGEN0051'

    assert len(gen0021e.schedule_grid_group) == HOURS_SIZE
    grid1 = gen0021e.schedule_grid_group[0]
    grid2 = gen0021e.schedule_grid_group[1]
    assert isinstance(grid1, ScheduleGridError)
    assert grid1.code == GridCode.FX_PRIMARY_MARKET
    assert grid1.opening_hour == datetime(2025, 11, 28, 8, 0, tzinfo=UTC)
    assert grid1.closing_hour == datetime(2025, 11, 28, 18, 30, tzinfo=UTC)
    assert grid1.hour_type == TimeType.STANDARD
    assert grid1.code_error_code == 'EGEN0033'
    assert isinstance(grid2, ScheduleGridError)
    assert grid2.code == GridCode.CBLC_PUBLIC_FIXED_INCOME_CLEARING
    assert grid2.opening_hour == datetime(2025, 11, 28, 8, 0, tzinfo=UTC)
    assert grid2.closing_hour == datetime(2025, 11, 28, 21, 0, tzinfo=UTC)
    assert grid2.hour_type == TimeType.STANDARD


def test_gen0021_missing_required_fields() -> None:
    with pytest.raises(ValidationError) as exc:
        GEN0021.model_validate({})

    missing_fields = extract_missing_fields(exc.value)
    assert missing_fields == {
        'from_ispb',
        'to_ispb',
        'system_domain',
        'operation_number',
        'provider_ispb',
        'reference_date',
        'provider_datetime',
        'schedule_grid_group',
        'settlement_date',
    }


def test_gen0021_to_xml() -> None:
    params = make_valid_gen0021_params()
    gen0021 = GEN0021.model_validate(params)

    xml = gen0021.to_xml()

    expected_xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/GEN/GEN0021.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>316801512509080000001</NUOp>
        </BCMSG>
        <SISMSG>
            <GEN0021>
                <CodMsg>GEN0021</CodMsg>
                <ISPBPrestd>31680151</ISPBPrestd>
                <CodProdt>VIC</CodProdt>
                <Grupo_GEN0021_GrdHrio>
                    <CodGrd>CAM04</CodGrd>
                    <DtHrAbert>2025-11-28 08:00:00+00:00</DtHrAbert>
                    <DtHrFcht>2025-11-28 18:30:00+00:00</DtHrFcht>
                    <TpHrio>P</TpHrio>
                </Grupo_GEN0021_GrdHrio>
                <Grupo_GEN0021_GrdHrio>
                    <CodGrd>CBL89</CodGrd>
                    <DtHrAbert>2025-11-28 08:00:00+00:00</DtHrAbert>
                    <DtHrFcht>2025-11-28 21:00:00+00:00</DtHrFcht>
                    <TpHrio>P</TpHrio>
                </Grupo_GEN0021_GrdHrio>
                <DtRef>2025-11-28</DtRef>
                <DtHrPrestd>2025-11-28 16:01:00+00:00</DtHrPrestd>
                <DtMovto>2025-11-28</DtMovto>
            </GEN0021>
        </SISMSG>
    </DOC>
    """
    assert normalize_xml(expected_xml) == normalize_xml(xml)


def test_gen0021e_general_error_to_xml() -> None:
    params = make_valid_gen0021e_params(general_error=True)
    gen0021e = GEN0021E.model_validate(params)

    xml = gen0021e.to_xml()

    expected_xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/GEN/GEN0021E.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>316801512509080000001</NUOp>
        </BCMSG>
        <SISMSG>
            <GEN0021E CodErro="EGEN0050">
                <CodMsg>GEN0021</CodMsg>
                <ISPBPrestd>31680151</ISPBPrestd>
                <CodProdt>VIC</CodProdt>
                <Grupo_GEN0021_GrdHrio>
                    <CodGrd>CAM04</CodGrd>
                    <DtHrAbert>2025-11-28 08:00:00+00:00</DtHrAbert>
                    <DtHrFcht>2025-11-28 18:30:00+00:00</DtHrFcht>
                    <TpHrio>P</TpHrio>
                </Grupo_GEN0021_GrdHrio>
                <Grupo_GEN0021_GrdHrio>
                    <CodGrd>CBL89</CodGrd>
                    <DtHrAbert>2025-11-28 08:00:00+00:00</DtHrAbert>
                    <DtHrFcht>2025-11-28 21:00:00+00:00</DtHrFcht>
                    <TpHrio>P</TpHrio>
                </Grupo_GEN0021_GrdHrio>
                <DtRef>2025-11-28</DtRef>
                <DtHrPrestd>2025-11-28 16:01:00+00:00</DtHrPrestd>
                <DtMovto>2025-11-28</DtMovto>
            </GEN0021E>
        </SISMSG>
    </DOC>
    """
    assert normalize_xml(expected_xml) == normalize_xml(xml)


def test_gen0021e_tag_error_to_xml() -> None:
    params = make_valid_gen0021e_params()
    gen0021e = GEN0021E.model_validate(params)

    xml = gen0021e.to_xml()

    expected_xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/GEN/GEN0021E.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>316801512509080000001</NUOp>
        </BCMSG>
        <SISMSG>
            <GEN0021E>
                <CodMsg>GEN0021</CodMsg>
                <ISPBPrestd CodErro="EGEN0051">31680151</ISPBPrestd>
                <CodProdt>VIC</CodProdt>
                <Grupo_GEN0021_GrdHrio>
                    <CodGrd CodErro="EGEN0033">CAM04</CodGrd>
                    <DtHrAbert>2025-11-28 08:00:00+00:00</DtHrAbert>
                    <DtHrFcht>2025-11-28 18:30:00+00:00</DtHrFcht>
                    <TpHrio>P</TpHrio>
                </Grupo_GEN0021_GrdHrio>
                <Grupo_GEN0021_GrdHrio>
                    <CodGrd>CBL89</CodGrd>
                    <DtHrAbert>2025-11-28 08:00:00+00:00</DtHrAbert>
                    <DtHrFcht>2025-11-28 21:00:00+00:00</DtHrFcht>
                    <TpHrio>P</TpHrio>
                </Grupo_GEN0021_GrdHrio>
                <DtRef>2025-11-28</DtRef>
                <DtHrPrestd>2025-11-28 16:01:00+00:00</DtHrPrestd>
                <DtMovto>2025-11-28</DtMovto>
            </GEN0021E>
        </SISMSG>
    </DOC>
    """
    assert normalize_xml(expected_xml) == normalize_xml(xml)


def test_gen0021_from_xml() -> None:
    xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/GEN/GEN0021.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>316801512509080000001</NUOp>
        </BCMSG>
        <SISMSG>
            <GEN0021>
                <CodMsg>GEN0021</CodMsg>
                <ISPBPrestd>31680151</ISPBPrestd>
                <CodProdt>VIC</CodProdt>

                <Grupo_GEN0021_GrdHrio>
                    <CodGrd>CAM04</CodGrd>
                    <DtHrAbert>2025-11-28 08:00:00+00:00</DtHrAbert>
                    <DtHrFcht>2025-11-28 18:30:00+00:00</DtHrFcht>
                    <TpHrio>P</TpHrio>
                </Grupo_GEN0021_GrdHrio>
                <Grupo_GEN0021_GrdHrio>
                    <CodGrd>CBL89</CodGrd>
                    <DtHrAbert>2025-11-28 08:00:00+00:00</DtHrAbert>
                    <DtHrFcht>2025-11-28 21:00:00+00:00</DtHrFcht>
                    <TpHrio>P</TpHrio>
                </Grupo_GEN0021_GrdHrio>

                <DtRef>2025-11-28</DtRef>
                <DtHrPrestd>2025-11-28 16:01:00+00:00</DtHrPrestd>
                <DtMovto>2025-11-28</DtMovto>
            </GEN0021>
        </SISMSG>
    </DOC>
    """

    gen0021 = GEN0021.from_xml(xml)

    assert isinstance(gen0021, GEN0021)
    assert gen0021.from_ispb == '31680151'
    assert gen0021.to_ispb == '00038166'
    assert gen0021.system_domain == 'SPB01'
    assert gen0021.operation_number == '316801512509080000001'
    assert gen0021.message_code == 'GEN0021'
    assert gen0021.provider_ispb == '31680151'
    assert gen0021.product_code == ProductCode.VISA_INTL_CREDIT_PURCHASE
    assert gen0021.reference_date == date(2025, 11, 28)
    assert gen0021.provider_datetime == datetime(2025, 11, 28, 16, 1, tzinfo=UTC)
    assert gen0021.settlement_date == date(2025, 11, 28)

    assert len(gen0021.schedule_grid_group) == HOURS_SIZE
    grid1 = gen0021.schedule_grid_group[0]
    grid2 = gen0021.schedule_grid_group[1]
    assert isinstance(grid1, ScheduleGrid)
    assert grid1.code == GridCode.FX_PRIMARY_MARKET
    assert grid1.opening_hour == datetime(2025, 11, 28, 8, 0, tzinfo=UTC)
    assert grid1.closing_hour == datetime(2025, 11, 28, 18, 30, tzinfo=UTC)
    assert grid1.hour_type == TimeType.STANDARD
    assert isinstance(grid2, ScheduleGrid)
    assert grid2.code == GridCode.CBLC_PUBLIC_FIXED_INCOME_CLEARING
    assert grid2.opening_hour == datetime(2025, 11, 28, 8, 0, tzinfo=UTC)
    assert grid2.closing_hour == datetime(2025, 11, 28, 21, 0, tzinfo=UTC)
    assert grid2.hour_type == TimeType.STANDARD


def test_gen0021e_general_error_from_xml() -> None:
    xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/GEN/GEN0021E.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>316801512509080000001</NUOp>
        </BCMSG>
        <SISMSG>
            <GEN0021E CodErro="EGEN0050">
                <CodMsg>GEN0021</CodMsg>
                <ISPBPrestd>31680151</ISPBPrestd>
                <CodProdt>VIC</CodProdt>
                <Grupo_GEN0021_GrdHrio>
                    <CodGrd>CAM04</CodGrd>
                    <DtHrAbert>2025-11-28 08:00:00+00:00</DtHrAbert>
                    <DtHrFcht>2025-11-28 18:30:00+00:00</DtHrFcht>
                    <TpHrio>P</TpHrio>
                </Grupo_GEN0021_GrdHrio>
                <Grupo_GEN0021_GrdHrio>
                    <CodGrd>CBL89</CodGrd>
                    <DtHrAbert>2025-11-28 08:00:00+00:00</DtHrAbert>
                    <DtHrFcht>2025-11-28 21:00:00+00:00</DtHrFcht>
                    <TpHrio>P</TpHrio>
                </Grupo_GEN0021_GrdHrio>
                <DtRef>2025-11-28</DtRef>
                <DtHrPrestd>2025-11-28 16:01:00+00:00</DtHrPrestd>
                <DtMovto>2025-11-28</DtMovto>
            </GEN0021E>
        </SISMSG>
    </DOC>
    """

    gen0021e = GEN0021E.from_xml(xml)

    assert isinstance(gen0021e, GEN0021E)
    assert gen0021e.from_ispb == '31680151'
    assert gen0021e.to_ispb == '00038166'
    assert gen0021e.system_domain == 'SPB01'
    assert gen0021e.operation_number == '316801512509080000001'
    assert gen0021e.message_code == 'GEN0021'
    assert gen0021e.provider_ispb == '31680151'
    assert gen0021e.product_code == ProductCode.VISA_INTL_CREDIT_PURCHASE
    assert gen0021e.reference_date == date(2025, 11, 28)
    assert gen0021e.provider_datetime == datetime(2025, 11, 28, 16, 1, tzinfo=UTC)
    assert gen0021e.settlement_date == date(2025, 11, 28)
    assert gen0021e.general_error_code == 'EGEN0050'

    assert len(gen0021e.schedule_grid_group) == HOURS_SIZE
    grid1 = gen0021e.schedule_grid_group[0]
    grid2 = gen0021e.schedule_grid_group[1]
    assert isinstance(grid1, ScheduleGridError)
    assert grid1.code == GridCode.FX_PRIMARY_MARKET
    assert grid1.opening_hour == datetime(2025, 11, 28, 8, 0, tzinfo=UTC)
    assert grid1.closing_hour == datetime(2025, 11, 28, 18, 30, tzinfo=UTC)
    assert grid1.hour_type == TimeType.STANDARD
    assert isinstance(grid2, ScheduleGridError)
    assert grid2.code == GridCode.CBLC_PUBLIC_FIXED_INCOME_CLEARING
    assert grid2.opening_hour == datetime(2025, 11, 28, 8, 0, tzinfo=UTC)
    assert grid2.closing_hour == datetime(2025, 11, 28, 21, 0, tzinfo=UTC)
    assert grid2.hour_type == TimeType.STANDARD


def test_gen0021e_tag_error_from_xml() -> None:
    xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/GEN/GEN0021E.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>316801512509080000001</NUOp>
        </BCMSG>
        <SISMSG>
            <GEN0021E>
                <CodMsg>GEN0021</CodMsg>
                <ISPBPrestd CodErro="EGEN0051">31680151</ISPBPrestd>
                <CodProdt>VIC</CodProdt>
                <Grupo_GEN0021_GrdHrio>
                    <CodGrd CodErro="EGEN0033">CAM04</CodGrd>
                    <DtHrAbert>2025-11-28 08:00:00+00:00</DtHrAbert>
                    <DtHrFcht>2025-11-28 18:30:00+00:00</DtHrFcht>
                    <TpHrio>P</TpHrio>
                </Grupo_GEN0021_GrdHrio>
                <Grupo_GEN0021_GrdHrio>
                    <CodGrd>CBL89</CodGrd>
                    <DtHrAbert>2025-11-28 08:00:00+00:00</DtHrAbert>
                    <DtHrFcht>2025-11-28 21:00:00+00:00</DtHrFcht>
                    <TpHrio>P</TpHrio>
                </Grupo_GEN0021_GrdHrio>
                <DtRef>2025-11-28</DtRef>
                <DtHrPrestd>2025-11-28 16:01:00+00:00</DtHrPrestd>
                <DtMovto>2025-11-28</DtMovto>
            </GEN0021E>
        </SISMSG>
    </DOC>
    """

    gen0021e = GEN0021E.from_xml(xml)

    assert isinstance(gen0021e, GEN0021E)
    assert gen0021e.from_ispb == '31680151'
    assert gen0021e.to_ispb == '00038166'
    assert gen0021e.system_domain == 'SPB01'
    assert gen0021e.operation_number == '316801512509080000001'
    assert gen0021e.message_code == 'GEN0021'
    assert gen0021e.provider_ispb == '31680151'
    assert gen0021e.product_code == ProductCode.VISA_INTL_CREDIT_PURCHASE
    assert gen0021e.reference_date == date(2025, 11, 28)
    assert gen0021e.provider_datetime == datetime(2025, 11, 28, 16, 1, tzinfo=UTC)
    assert gen0021e.settlement_date == date(2025, 11, 28)
    assert gen0021e.provider_ispb_error_code == 'EGEN0051'

    assert len(gen0021e.schedule_grid_group) == HOURS_SIZE
    grid1 = gen0021e.schedule_grid_group[0]
    grid2 = gen0021e.schedule_grid_group[1]
    assert isinstance(grid1, ScheduleGridError)
    assert grid1.code == GridCode.FX_PRIMARY_MARKET
    assert grid1.opening_hour == datetime(2025, 11, 28, 8, 0, tzinfo=UTC)
    assert grid1.closing_hour == datetime(2025, 11, 28, 18, 30, tzinfo=UTC)
    assert grid1.hour_type == TimeType.STANDARD
    assert grid1.code_error_code == 'EGEN0033'
    assert isinstance(grid2, ScheduleGridError)
    assert grid2.code == GridCode.CBLC_PUBLIC_FIXED_INCOME_CLEARING
    assert grid2.opening_hour == datetime(2025, 11, 28, 8, 0, tzinfo=UTC)
    assert grid2.closing_hour == datetime(2025, 11, 28, 21, 0, tzinfo=UTC)
    assert grid2.hour_type == TimeType.STANDARD


def test_gen0021_from_xml_missing_required_fields() -> None:
    xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/GEN/GEN0021.xsd">
        <BCMSG>
            <IdentdEmissor>31680151</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>SPB01</DomSist>
            <NUOp>316801512509080000001</NUOp>
        </BCMSG>
        <SISMSG>
            <GEN0021>
                <CodMsg>GEN0021</CodMsg>
            </GEN0021>
        </SISMSG>
    </DOC>
    """

    with pytest.raises(ValidationError) as exc:
        GEN0021.from_xml(xml)

    missing_fields = extract_missing_fields(exc.value)
    assert missing_fields == {
        'provider_ispb',
        'reference_date',
        'provider_datetime',
        'settlement_date',
    }
