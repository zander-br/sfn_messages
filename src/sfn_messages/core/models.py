from abc import ABC, abstractmethod
from contextlib import suppress
from dataclasses import dataclass
from types import GenericAlias
from typing import Annotated, Any, Self, Union
from xml.etree import ElementTree as ET

from defusedxml.ElementTree import fromstring
from pydantic import BaseModel

from .errors import (
    BaseTagNameNotFoundInClassError,
    DiffBaseTagNameInFieldError,
    InvalidBaseTagNameError,
    InvalidLocalNameInFieldError,
    LocalNameNotSetInFieldError,
    LocalNameSetInFieldError,
)
from .types import Ispb, MappableToXmlValue, OperationNumber, SystemDomain


@dataclass(frozen=True)
class XmlPath:
    path: str

    def parts(self) -> tuple[list[str], str | None]:
        p = self.path.split('/')
        if p[-1].endswith('()') or p[-1].startswith('@'):
            return p[:-1], p[-1]
        return p, None


class XmlSerializerMixin(ABC, BaseModel):
    @classmethod
    @abstractmethod
    def get_base_tag_name(cls) -> str:
        raise NotImplementedError

    def to_xml_value(self) -> ET.Element:  # noqa: C901, PLR0912
        fields = (
            (field_name, getattr(self, field_name), metadata)
            for field_name, field_info in self.__class__.model_fields.items()
            for metadata in field_info.metadata
            if isinstance(metadata, XmlPath) and getattr(self, field_name) is not None
        )
        root = ET.Element(self.get_base_tag_name())
        for field_name, field_value, xml_path in fields:
            pointer = root
            [root_name, *path_names], local_name = xml_path.parts()
            if pointer.tag != root_name:
                raise DiffBaseTagNameInFieldError(cls=self.__class__, field_name=field_name)
            for path_name in path_names:
                new_pointer = pointer.find(path_name)
                if new_pointer is None:
                    new_pointer = ET.SubElement(pointer, path_name)
                pointer = new_pointer
            value = self._format_field_value(field_value)
            if isinstance(value, str):
                if local_name is None:
                    raise LocalNameNotSetInFieldError(cls=self.__class__, field_name=field_name)
                if local_name == 'text()':
                    pointer.text = value
                elif local_name.startswith('@'):
                    pointer.attrib[local_name[1:]] = value
                else:
                    raise InvalidLocalNameInFieldError(cls=self.__class__, field_name=field_name)
            elif local_name is None:
                if not isinstance(value, list):
                    value = [value]
                for element in value:
                    pointer.append(element)
            else:
                raise LocalNameSetInFieldError(cls=self.__class__, field_name=field_name)
        return root

    @staticmethod
    def _format_field_value(field_value: object, /) -> str | ET.Element | list[ET.Element]:
        if isinstance(field_value, list):
            return [value.to_xml_value() for value in field_value]
        if isinstance(field_value, MappableToXmlValue):
            return field_value.to_xml_value()
        return str(field_value)

    @classmethod
    def from_xml_value(cls, xml_value: str | ET.Element) -> Self:
        if isinstance(xml_value, str):
            raise TypeError
        fields = (
            (field_name, metadata)
            for field_name, field_info in cls.model_fields.items()
            for metadata in field_info.metadata
            if isinstance(metadata, XmlPath)
        )
        kwargs: dict[str, Any] = {}
        for field_name, xml_path in fields:
            [root_name, *path_names], local_name = xml_path.parts()
            if xml_value.tag != root_name:
                raise InvalidBaseTagNameError(document_tag=xml_value.tag, expected=root_name)
            pointer = xml_value.find('/'.join(path_names)) if path_names else xml_value
            if pointer is not None:
                if local_name is None:
                    kwargs[field_name] = pointer
                elif local_name == 'text()':
                    kwargs[field_name] = pointer.text
                elif local_name.startswith('@'):
                    kwargs[field_name] = pointer.attrib.get(local_name[1:])
        return cls(**{name: cls._parse_field_value(name, value) for name, value in kwargs.items()})

    @classmethod
    def _parse_field_value(cls, field_name: str, xml_value: str | ET.Element, /) -> object:
        classes = list[Any]()
        if klass := cls.__pydantic_fields__[field_name].annotation:
            classes.append(klass)
        while classes:
            klass = classes.pop()
            if isinstance(klass, Union):  # type: ignore[arg-type]
                for k in reversed(klass.__args__):
                    classes.append(k)
            elif isinstance(klass, type) and issubclass(klass, MappableToXmlValue):
                with suppress(ValueError):
                    value = xml_value
                    if issubclass(klass, XmlSerializerMixin):
                        element = xml_value.find(klass.get_base_tag_name())
                        if isinstance(element, ET.Element):
                            value = element
                    return klass.from_xml_value(value)
            elif (
                isinstance(klass, GenericAlias)
                and isinstance(klass.__origin__, type)
                and issubclass(klass.__origin__, list)
                and issubclass(t := klass.__args__[0], XmlSerializerMixin)
            ):
                if isinstance(xml_value, str):
                    raise TypeError
                return [t.from_xml_value(element) for element in xml_value.findall(t.get_base_tag_name())]
        return str(xml_value)


class BaseSubMessage(XmlSerializerMixin, BaseModel):
    @classmethod
    def get_base_tag_name(cls) -> str:
        xml_paths = (
            metadata
            for field_info in cls.model_fields.values()
            for metadata in field_info.metadata
            if isinstance(metadata, XmlPath)
        )
        with suppress(StopIteration):
            xml_path = next(xml_paths)
            return xml_path.parts()[0][0]
        raise BaseTagNameNotFoundInClassError(cls=cls)


class BaseMessage(BaseSubMessage):
    from_ispb: Annotated[Ispb, XmlPath('DOC/BCMSG/IdentdEmissor/text()')]
    to_ispb: Annotated[Ispb, XmlPath('DOC/BCMSG/IdentdDestinatario/text()')]
    system_domain: Annotated[SystemDomain, XmlPath('DOC/BCMSG/DomSist/text()')]
    operation_number: Annotated[OperationNumber, XmlPath('DOC/BCMSG/NUOp/text()')]

    def to_xml(self) -> str:
        xml = self.to_xml_value()
        ET.indent(xml)
        return '<?xml version="1.0"?>\n' + ET.tostring(xml, encoding='unicode')

    @classmethod
    def from_xml(cls, value: str, /) -> Self:
        xml = fromstring(value)
        return cls.from_xml_value(xml)
