from __future__ import annotations

from datetime import date, datetime
from typing import Any, Dict

import pytest

from sfn_messages.gen.gen0006.v511 import GEN0006_V511
from sfn_messages.gen.gen0006.enums import CertificateIssue


def make_valid_params() -> Dict[str, Any]:
    return {
        'from_ispb': '31680151',
        'to_ispb': '00038166',
        'system_domain': 'SPB01',
        'operation_number': '316801512509080000001',
        'message_code': 'GEN0006',
        'internal_control_number': '123',
        'internal_ispb': '31680151',
        'version': GEN0006_V511.VERSION,
        'certificate_issue': 'SERPRO',
        'certificate_serial_number': 'A' * 32,
        'settlement_date': date(2025, 11, 8),
        'description': 'Teste GEN0006',
    }


def test_gen0006_v511_valid_model():
    params = make_valid_params()

    msg = GEN0006_V511.model_validate(params)

    assert isinstance(msg, GEN0006_V511)
    assert msg.from_ispb == '31680151'
    assert msg.to_ispb == '00038166'
    assert msg.internal_ispb == '31680151'
    assert msg.certificate_issue == CertificateIssue.SERPRO
    assert msg.certificate_serial_number == 'A' * 32
    assert msg.settlement_date == date(2025, 11, 8)


def test_gen0006_v511_missing_certificate_fields():
    params = make_valid_params()
    params['certificate_issue'] = None
    params['certificate_serial_number'] = None

    with pytest.raises(Exception) as exc:
        GEN0006_V511.model_validate(params)

    msg = str(exc.value)
    assert 'certificate_issue is required' in msg
    assert 'certificate_serial_number is required' in msg


def test_gen0006_v511_missing_timestamp_for_r1():
    params = make_valid_params()
    params['message_code'] = 'GEN0006R1'
    params['certificate_issue'] = None
    params['certificate_serial_number'] = None
    params['provider_timestamp'] = None

    with pytest.raises(Exception) as exc:
        GEN0006_V511.model_validate(params)

    assert 'provider_timestamp is required' in str(exc.value)


def test_gen0006_v511_valid_r1():
    params = make_valid_params()
    params['message_code'] = 'GEN0006R1'
    params['certificate_issue'] = None
    params['certificate_serial_number'] = None
    params['provider_timestamp'] = datetime(2025, 11, 8, 10, 30)

    msg = GEN0006_V511.model_validate(params)

    assert msg.message_code.value == 'GEN0006R1'
    assert msg.provider_timestamp is not None


def test_gen0006_v511_to_xml():
    params = make_valid_params()
    msg = GEN0006_V511.model_validate(params)

    xml = msg.to_xml()

    assert '<DOC>' in xml
    assert '<BCMSG>' in xml
    assert '<SISMSG>' in xml
    assert '<GEN0006>' in xml

    assert '<CodMsg>GEN0006</CodMsg>' in xml
    assert '<NumCtrlIF>123</NumCtrlIF>' in xml
    assert '<ISPBIF>31680151</ISPBIF>' in xml
    assert '<DtMovto>2025-11-08</DtMovto>' in xml


def test_gen0006_v511_from_xml():
    xml = """
    <DOC>
      <BCMSG>
        <IdentdEmissor>31680151</IdentdEmissor>
        <IdentdDestinatario>00038166</IdentdDestinatario>
        <DomSist>SPB01</DomSist>
        <NUOp>316801512509080000001</NUOp>
      </BCMSG>
      <SISMSG>
        <GEN0006>
          <CodMsg>GEN0006</CodMsg>
          <NumCtrlIF>123</NumCtrlIF>
          <ISPBIF>31680151</ISPBIF>
          <CodCertifrAtv>1</CodCertifrAtv>
          <CertifAtv>AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA</CertifAtv>
          <Hist>Teste GEN0006</Hist>
          <DtMovto>2025-11-08</DtMovto>
        </GEN0006>
      </SISMSG>
    </DOC>
    """

    msg = GEN0006_V511.from_xml(xml)

    assert isinstance(msg, GEN0006_V511)
    assert msg.from_ispb == '31680151'
    assert msg.to_ispb == '00038166'
    assert msg.internal_ispb == '31680151'
    assert msg.internal_control_number == '123'
    assert msg.certificate_serial_number is not None
    assert msg.description == 'Teste GEN0006'
    assert msg.settlement_date == date(2025, 11, 8)


def test_gen0006_v511_roundtrip():
    params = make_valid_params()
    msg1 = GEN0006_V511.model_validate(params)

    xml = msg1.to_xml()

    msg2 = GEN0006_V511.from_xml(xml)

    assert msg2.from_ispb == msg1.from_ispb
    assert msg2.to_ispb == msg1.to_ispb
    assert msg2.internal_ispb == msg1.internal_ispb
    assert msg2.internal_control_number == msg1.internal_control_number
    assert msg2.settlement_date == msg1.settlement_date
