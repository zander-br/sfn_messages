from datetime import date, datetime
from typing import Any

import pytest
from pydantic import ValidationError

from sfn_messages.core import from_xml, load_message_class, to_xml
from sfn_messages.src.src0001 import SRC0001, SRC0001E, SRC0001R1
from sfn_messages.src.types import ProductPermissionIndicator, ProtectionType
from tests.conftest import extract_missing_fields, normalize_xml

PRODUCT_PERMISSIONS_SIZE = 2


def make_valid_src0001_params() -> dict[str, Any]:
    return {
        'from_ispb': '12345678',
        'to_ispb': '00038166',
        'system_domain': 'MES02',
        'operation_number': '12345678250908000000001',
        'message_code': 'SRC0001',
        'institution_control_number': '00001',
        'responsible_entity_base_cnpj': '12345678',
        'document': '39053344705',
        'protection_type': 'ACCOUNT_OPENING',
        'settlement_date': '2026-08-11',
    }


def make_valid_src0001r1_params() -> dict[str, Any]:
    return {
        'from_ispb': '00038166',
        'to_ispb': '12345678',
        'system_domain': 'MES02',
        'operation_number': '12345678250908000000001',
        'message_code': 'SRC0001R1',
        'institution_control_number': '00001',
        'responsible_entity_base_cnpj': '12345678',
        'src_control_number': 'SRC20260811000000001',
        'product_permissions': [
            {
                'protection_type': 'ACCOUNT_OPENING',
                'product_permission_indicator': 'ALLOWED',
            }
        ],
        'vendor_timestamp': '2026-08-11T12:30:45',
        'settlement_date': '2026-08-11',
    }


def make_valid_src0001e_params(*, general_error: bool = False) -> dict[str, Any]:
    payload = {
        'from_ispb': '00038166',
        'to_ispb': '12345678',
        'system_domain': 'MES02',
        'operation_number': '12345678250908000000001',
        'message_code': 'SRC0001E',
        'institution_control_number': '00001',
        'responsible_entity_base_cnpj': '12345678',
        'document': '39053344705',
        'protection_type': 'ACCOUNT_OPENING',
        'settlement_date': '2026-08-11',
    }
    if general_error:
        payload['general_error_code'] = 'EGEN0050'
    else:
        payload['document_error_code'] = 'EGEN0051'
    return payload


def test_src0001_valid_model() -> None:
    src0001 = SRC0001.model_validate(make_valid_src0001_params())

    assert src0001.message_code == 'SRC0001'
    assert src0001.institution_control_number == '00001'
    assert src0001.responsible_entity_base_cnpj == '12345678'
    assert src0001.document == '39053344705'
    assert src0001.protection_type == ProtectionType.ACCOUNT_OPENING
    assert src0001.settlement_date == date(2026, 8, 11)
    assert src0001.system_domain == 'MES02'


def test_src0001_missing_required_fields() -> None:
    with pytest.raises(ValidationError) as exc:
        SRC0001.model_validate(
            {
                'from_ispb': '12345678',
                'to_ispb': '00038166',
                'system_domain': 'MES02',
                'operation_number': '12345678250908000000001',
            }
        )

    missing = extract_missing_fields(exc.value)
    assert 'institution_control_number' in missing
    assert 'document' in missing
    assert 'protection_type' in missing


def test_src0001_to_xml() -> None:
    src0001 = SRC0001.model_validate(make_valid_src0001_params())
    xml = src0001.to_xml()

    expected_xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/MES/SRC0001.xsd">
        <BCMSG>
            <IdentdEmissor>12345678</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>MES02</DomSist>
            <NUOp>12345678250908000000001</NUOp>
        </BCMSG>
        <SISMSG>
            <SRC0001>
                <CodMsg>SRC0001</CodMsg>
                <NumCtrlIF>00001</NumCtrlIF>
                <CNPJBaseEntRespons>12345678</CNPJBaseEntRespons>
                <CNPJ_CPF>39053344705</CNPJ_CPF>
                <TpProtc>ACT</TpProtc>
                <DtMovto>2026-08-11</DtMovto>
            </SRC0001>
        </SISMSG>
    </DOC>
    """

    assert normalize_xml(expected_xml) == normalize_xml(xml)


def test_src0001_from_xml() -> None:
    xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/MES/SRC0001.xsd">
        <BCMSG>
            <IdentdEmissor>12345678</IdentdEmissor>
            <IdentdDestinatario>00038166</IdentdDestinatario>
            <DomSist>MES02</DomSist>
            <NUOp>12345678250908000000001</NUOp>
        </BCMSG>
        <SISMSG>
            <SRC0001>
                <CodMsg>SRC0001</CodMsg>
                <NumCtrlIF>00001</NumCtrlIF>
                <CNPJBaseEntRespons>12345678</CNPJBaseEntRespons>
                <CNPJBaseIF>12345678</CNPJBaseIF>
                <CNPJ_CPF>39053344705</CNPJ_CPF>
                <TpProtc>ACT</TpProtc>
                <DtMovto>2026-08-11</DtMovto>
            </SRC0001>
        </SISMSG>
    </DOC>
    """

    src0001 = SRC0001.from_xml(xml)
    assert src0001.document == '39053344705'
    assert src0001.protection_type == ProtectionType.ACCOUNT_OPENING
    assert src0001.institution_base_cnpj == '12345678'


def test_src0001r1_valid_model() -> None:
    src0001r1 = SRC0001R1.model_validate(make_valid_src0001r1_params())

    assert src0001r1.message_code == 'SRC0001R1'
    assert src0001r1.src_control_number == 'SRC20260811000000001'
    assert len(src0001r1.product_permissions) == 1
    assert src0001r1.product_permissions[0].protection_type == ProtectionType.ACCOUNT_OPENING
    assert src0001r1.product_permissions[0].product_permission_indicator == ProductPermissionIndicator.ALLOWED
    assert src0001r1.vendor_timestamp == datetime(2026, 8, 11, 12, 30, 45)


def test_src0001r1_to_xml() -> None:
    src0001r1 = SRC0001R1.model_validate(make_valid_src0001r1_params())
    xml = src0001r1.to_xml()

    expected_xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/MES/SRC0001.xsd">
        <BCMSG>
            <IdentdEmissor>00038166</IdentdEmissor>
            <IdentdDestinatario>12345678</IdentdDestinatario>
            <DomSist>MES02</DomSist>
            <NUOp>12345678250908000000001</NUOp>
        </BCMSG>
        <SISMSG>
            <SRC0001R1>
                <CodMsg>SRC0001R1</CodMsg>
                <NumCtrlIF>00001</NumCtrlIF>
                <CNPJBaseEntRespons>12345678</CNPJBaseEntRespons>
                <NumCtrlSRC>SRC20260811000000001</NumCtrlSRC>
                <Grupo_SRC0001R1_PermsProdt>
                    <TpProtc>ACT</TpProtc>
                    <IndrPermsProdt>S</IndrPermsProdt>
                </Grupo_SRC0001R1_PermsProdt>
                <DtHrBC>2026-08-11T12:30:45</DtHrBC>
                <DtMovto>2026-08-11</DtMovto>
            </SRC0001R1>
        </SISMSG>
    </DOC>
    """

    assert normalize_xml(expected_xml) == normalize_xml(xml)


def test_src0001r1_from_xml() -> None:
    xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/MES/SRC0001.xsd">
        <BCMSG>
            <IdentdEmissor>00038166</IdentdEmissor>
            <IdentdDestinatario>12345678</IdentdDestinatario>
            <DomSist>MES02</DomSist>
            <NUOp>12345678250908000000001</NUOp>
        </BCMSG>
        <SISMSG>
            <SRC0001R1>
                <CodMsg>SRC0001R1</CodMsg>
                <NumCtrlIF>00001</NumCtrlIF>
                <CNPJBaseEntRespons>12345678</CNPJBaseEntRespons>
                <NumCtrlSRC>SRC20260811000000001</NumCtrlSRC>
                <Grupo_SRC0001R1_PermsProdt>
                    <TpProtc>ACT</TpProtc>
                    <IndrPermsProdt>N</IndrPermsProdt>
                </Grupo_SRC0001R1_PermsProdt>
                <Grupo_SRC0001R1_PermsProdt>
                    <TpProtc>ATT</TpProtc>
                    <IndrPermsProdt>S</IndrPermsProdt>
                </Grupo_SRC0001R1_PermsProdt>
                <DtHrBC>2026-08-11T12:30:45</DtHrBC>
                <DtMovto>2026-08-11</DtMovto>
            </SRC0001R1>
        </SISMSG>
    </DOC>
    """

    src0001r1 = SRC0001R1.from_xml(xml)
    assert len(src0001r1.product_permissions) == PRODUCT_PERMISSIONS_SIZE
    assert src0001r1.product_permissions[0].product_permission_indicator == ProductPermissionIndicator.NOT_ALLOWED
    assert src0001r1.product_permissions[1].protection_type == ProtectionType.OWNERSHIP_CHANGE


def test_src0001r1_product_permissions_defaults_to_empty_list() -> None:
    params = make_valid_src0001r1_params()
    del params['product_permissions']

    src0001r1 = SRC0001R1.model_validate(params)

    assert src0001r1.product_permissions == []


def test_src0001r1_from_xml_without_product_permission_groups() -> None:
    xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/MES/SRC0001.xsd">
        <BCMSG>
            <IdentdEmissor>00038166</IdentdEmissor>
            <IdentdDestinatario>12345678</IdentdDestinatario>
            <DomSist>MES02</DomSist>
            <NUOp>12345678250908000000001</NUOp>
        </BCMSG>
        <SISMSG>
            <SRC0001R1>
                <CodMsg>SRC0001R1</CodMsg>
                <NumCtrlIF>00001</NumCtrlIF>
                <CNPJBaseEntRespons>12345678</CNPJBaseEntRespons>
                <NumCtrlSRC>SRC20260811000000001</NumCtrlSRC>
                <DtHrBC>2026-08-11T12:30:45</DtHrBC>
                <DtMovto>2026-08-11</DtMovto>
            </SRC0001R1>
        </SISMSG>
    </DOC>
    """

    src0001r1 = SRC0001R1.from_xml(xml)
    assert src0001r1.product_permissions == []


def test_src0001e_to_xml() -> None:
    src0001e = SRC0001E.model_validate(make_valid_src0001e_params(general_error=True))
    xml = src0001e.to_xml()

    expected_xml = """<?xml version="1.0"?>
    <DOC xmlns="http://www.bcb.gov.br/MES/SRC0001E.xsd">
        <BCMSG>
            <IdentdEmissor>00038166</IdentdEmissor>
            <IdentdDestinatario>12345678</IdentdDestinatario>
            <DomSist>MES02</DomSist>
            <NUOp>12345678250908000000001</NUOp>
        </BCMSG>
        <SISMSG>
            <SRC0001 CodErro="EGEN0050">
                <CodMsg>SRC0001E</CodMsg>
                <NumCtrlIF>00001</NumCtrlIF>
                <CNPJBaseEntRespons>12345678</CNPJBaseEntRespons>
                <CNPJ_CPF>39053344705</CNPJ_CPF>
                <TpProtc>ACT</TpProtc>
                <DtMovto>2026-08-11</DtMovto>
            </SRC0001>
        </SISMSG>
    </DOC>
    """

    assert normalize_xml(expected_xml) == normalize_xml(xml)


def test_load_message_class_and_to_xml_helpers() -> None:
    assert load_message_class('SRC0001') is SRC0001
    assert load_message_class('SRC0001R1') is SRC0001R1

    xml = to_xml('SRC0001', make_valid_src0001_params())
    parsed = from_xml(xml)
    assert isinstance(parsed, SRC0001)
    assert parsed.document == '39053344705'
