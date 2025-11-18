from abc import ABC, abstractmethod
from typing import Self
from xml.etree.ElementTree import Element, SubElement

from pydantic import BaseModel, ConfigDict

from sfn_messages.core.enums import SystemDomain
from sfn_messages.core.xml_utils import pretty_xml


class BaseMessage(BaseModel, ABC):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    from_ispb: str
    to_ispb: str
    system_domain: SystemDomain
    operation_number: str

    def to_xml(self) -> str:
        root = Element('DOC')
        self._build_control_segment(root)
        self._build_system_segment(root)
        return pretty_xml(root)

    @classmethod
    @abstractmethod
    def from_xml(cls, xml: str) -> Self: ...

    def _build_control_segment(self, root: Element):
        control = SubElement(root, 'BCMSG')
        SubElement(control, 'IdentdEmissor').text = self.from_ispb
        SubElement(control, 'IdentdDestinatario').text = self.to_ispb
        SubElement(control, 'DomSist').text = self.system_domain.value
        SubElement(control, 'NUOp').text = self.operation_number

    @abstractmethod
    def _build_system_segment(self, root: Element) -> None: ...

    @classmethod
    def _extract_control_segment(cls, tree: Element) -> dict[str, str | None]:
        return {
            'from_ispb': tree.findtext('.//IdentdEmissor'),
            'to_ispb': tree.findtext('.//IdentdDestinatario'),
            'system_domain': tree.findtext('.//DomSist'),
            'operation_number': tree.findtext('.//NUOp'),
        }
