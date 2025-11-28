from datetime import UTC, date, datetime
from typing import Any

import pytest
from pydantic import ValidationError

from sfn_messages.core.types import GridCode, ProductCode, TimeType
from sfn_messages.gen.gen0021 import GEN0021, GEN0021SCHEDULEGRIDGROUP
from tests.conftest import extract_missing_fields, normalize_xml

GRID_HOURS_SIZE = 2


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
                'grid_code': 'FX_PRIMARY_MARKET',
                'grid_opening_hour': '2025-11-28T08:00:00+00:00',
                'grid_closing_hour': '2025-11-28T18:30:00+00:00',
                'grid_hour_type': 'STANDARD',
            },
            {
                'grid_code': 'CBLC_PUBLIC_FIXED_INCOME_CLEARING',
                'grid_opening_hour': '2025-11-28T08:00:00+00:00',
                'grid_closing_hour': '2025-11-28T21:00:00+00:00',
                'grid_hour_type': 'STANDARD',
            },
        ],
        'reference_date': '2025-11-28',
        'provider_datetime': '2025-11-28T16:01:00+00:00',
        'settlement_date': '2025-11-28',
    }


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

    assert len(gen0021.schedule_grid_group) == GRID_HOURS_SIZE
    grid1 = gen0021.schedule_grid_group[0]
    grid2 = gen0021.schedule_grid_group[1]
    assert isinstance(grid1, GEN0021SCHEDULEGRIDGROUP)
    assert grid1.grid_code == GridCode.FX_PRIMARY_MARKET
    assert grid1.grid_opening_hour == datetime(2025, 11, 28, 8, 0, tzinfo=UTC)
    assert grid1.grid_closing_hour == datetime(2025, 11, 28, 18, 30, tzinfo=UTC)
    assert grid1.grid_hour_type == TimeType.STANDARD
    assert isinstance(grid2, GEN0021SCHEDULEGRIDGROUP)
    assert grid2.grid_code == GridCode.CBLC_PUBLIC_FIXED_INCOME_CLEARING
    assert grid2.grid_opening_hour == datetime(2025, 11, 28, 8, 0, tzinfo=UTC)
    assert grid2.grid_closing_hour == datetime(2025, 11, 28, 21, 0, tzinfo=UTC)
    assert grid2.grid_hour_type == TimeType.STANDARD


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

    assert len(gen0021.schedule_grid_group) == GRID_HOURS_SIZE
    grid1 = gen0021.schedule_grid_group[0]
    grid2 = gen0021.schedule_grid_group[1]
    assert isinstance(grid1, GEN0021SCHEDULEGRIDGROUP)
    assert grid1.grid_code == GridCode.FX_PRIMARY_MARKET
    assert grid1.grid_opening_hour == datetime(2025, 11, 28, 8, 0, tzinfo=UTC)
    assert grid1.grid_closing_hour == datetime(2025, 11, 28, 18, 30, tzinfo=UTC)
    assert grid1.grid_hour_type == TimeType.STANDARD
    assert isinstance(grid2, GEN0021SCHEDULEGRIDGROUP)
    assert grid2.grid_code == GridCode.CBLC_PUBLIC_FIXED_INCOME_CLEARING
    assert grid2.grid_opening_hour == datetime(2025, 11, 28, 8, 0, tzinfo=UTC)
    assert grid2.grid_closing_hour == datetime(2025, 11, 28, 21, 0, tzinfo=UTC)
    assert grid2.grid_hour_type == TimeType.STANDARD


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
