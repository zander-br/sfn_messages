from dataclasses import dataclass
from typing import Annotated, Any, Self
from xml.etree import ElementTree as ET

from defusedxml.ElementTree import fromstring
from pydantic import BaseModel

from .types import Ispb, OperationNumber, SystemDomain


@dataclass(frozen=True, slots=True)
class XmlPath:
    path: str

    def parts(self) -> list[str]:
        return self.path.split('/')


class BaseMessage(BaseModel):
    from_ispb: Annotated[Ispb, XmlPath('DOC/BCMSG/IdentdEmissor/text()')]
    to_ispb: Annotated[Ispb, XmlPath('DOC/BCMSG/IdentdDestinatario/text()')]
    system_domain: Annotated[SystemDomain, XmlPath('DOC/BCMSG/DomSist/text()')]
    operation_number: Annotated[OperationNumber, XmlPath('DOC/BCMSG/NUOp/text()')]

    def to_xml(self) -> str:
        fields = (
            (str(getattr(self, field_name)), metadata)
            for field_name, field_info in self.__class__.model_fields.items()
            for metadata in field_info.metadata
            if isinstance(metadata, XmlPath) and getattr(self, field_name) is not None
        )
        root = ET.Element('DOC')
        for field_value, xml_path in fields:
            pointer = root
            root_name, *path_names, local_name = xml_path.parts()
            if pointer.tag != root_name:
                continue
            for path_name in path_names:
                new_pointer = pointer.find(path_name)
                if new_pointer is None:
                    new_pointer = ET.SubElement(pointer, path_name)
                pointer = new_pointer
            if local_name == 'text()':
                pointer.text = field_value
            elif local_name.startswith('@'):
                pointer.attrib[local_name[1:]] = field_value
        ET.indent(root)
        return '<?xml version="1.0"?>\n' + ET.tostring(root, encoding='unicode')

    @classmethod
    def from_xml(cls, value: str, /) -> Self:
        root = fromstring(value)
        fields = (
            (field_name, metadata)
            for field_name, field_info in cls.model_fields.items()
            for metadata in field_info.metadata
            if isinstance(metadata, XmlPath)
        )
        kwargs: dict[str, Any] = {}
        for field_name, xml_path in fields:
            root_name, *path_names, local_name = xml_path.parts()
            if root.tag != root_name:
                continue
            pointer = root.find('/'.join(path_names))
            if pointer is not None:
                if local_name == 'text()':
                    kwargs[field_name] = pointer.text
                elif local_name.startswith('@'):
                    kwargs[field_name] = pointer.attrib[local_name[1:]]
        return cls(**kwargs)
