from datetime import date, datetime
from typing import Any, ClassVar
from xml.etree.ElementTree import Element, SubElement, fromstring

from pydantic import Field, model_validator

from sfn_messages.core.registry import register

from .model import GEN0006


class GEN0006_V511(GEN0006):
    VERSION: ClassVar[str] = '5.11'

    from_ispb: str = Field(..., pattern=r'^[0-9A-Z]{8}$')
    to_ispb: str = Field(..., pattern=r'^[0-9A-Z]{8}$')
    internal_ispb: str = Field(..., pattern=r'^[0-9A-Z]{8}$')
    operation_number: str = Field(..., pattern=r'^[0-9A-Z]{8}[0-9]{13}$')
    internal_control_number: str = Field(..., min_length=1, max_length=20)
    settlement_date: date
    certificate_serial_number: str | None = Field(default=None, min_length=32, max_length=32)
    description: str | None = Field(default=None, max_length=200)
    provider_timestamp: datetime | None = Field(default=None)

    @model_validator(mode='after')
    def validate_required_by_message_code(self) -> GEN0006_V511:
        code = self.message_code.value
        errors: list[str] = []

        if code == 'GEN0006':
            if self.certificate_issue is None:
                errors.append('certificate_issue is required')
            if self.certificate_serial_number is None:
                errors.append('certificate_serial_number is required')

        elif code == 'GEN0006R1':
            if self.provider_timestamp is None:
                errors.append('provider_timestamp is required')

        if errors:
            raise ValueError('; '.join(errors))

        return self

    def _build_system_segment(self, root: Element) -> None:
        system_segment = SubElement(root, 'SISMSG')
        message_element = SubElement(system_segment, 'GEN0006')
        SubElement(message_element, 'CodMsg').text = self.message_code.value
        SubElement(message_element, 'NumCtrlIF').text = self.internal_control_number
        SubElement(message_element, 'ISPBIF').text = self.internal_ispb
        if self.certificate_issue is not None:
            SubElement(message_element, 'CodCertifrAtv').text = str(self.certificate_issue.value)
        if self.certificate_serial_number is not None:
            SubElement(message_element, 'CertifAtv').text = self.certificate_serial_number
        if self.description:
            SubElement(message_element, 'Hist').text = self.description
        SubElement(message_element, 'DtMovto').text = self.settlement_date.strftime('%Y-%m-%d')

    @classmethod
    def from_xml(cls, xml: str) -> GEN0006_V511:
        tree = fromstring(xml)
        control_params = cls._extract_control_segment(tree)
        params: dict[str, Any] = {
            **control_params,
            'message_code': tree.findtext('.//CodMsg'),
            'internal_control_number': tree.findtext('.//NumCtrlIF'),
            'internal_ispb': tree.findtext('.//ISPBIF'),
            'version': cls.VERSION,
            'certificate_issue': tree.findtext('.//CodCertifrAtv'),
            'certificate_serial_number': tree.findtext('.//CertifAtv'),
            'settlement_date': tree.findtext('.//DtMovto'),
            'provider_timestamp': tree.findtext('.//DtHrBC') or None,
            'description': tree.findtext('.//Hist') or None,
        }
        return cls.model_validate(params)


register('GEN0006', GEN0006_V511.VERSION, GEN0006_V511)
