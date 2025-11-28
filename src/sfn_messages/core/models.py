from abc import ABC, abstractmethod
from collections.abc import Iterable, Iterator
from contextlib import suppress
from dataclasses import dataclass
from types import GenericAlias, UnionType
from typing import Annotated, Any, ClassVar, Self, Union, get_args, get_origin
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
    XML_NAMESPACE: ClassVar[str | None] = None

    @classmethod
    def get_xml_namespace(cls) -> str | None:
        return cls.XML_NAMESPACE

    @staticmethod
    def _local_name(tag: str) -> str:
        if tag.startswith('{'):
            return tag.split('}', 1)[1]
        return tag

    @classmethod
    def _qname(cls, tag: str) -> str:
        ns = cls.get_xml_namespace()
        if ns:
            return f'{{{ns}}}{tag}'
        return tag

    @classmethod
    def _iter_xmlpath_fields(cls) -> Iterable[tuple[str, XmlPath]]:
        return (
            (field_name, metadata)
            for field_name, field_info in cls.model_fields.items()
            for metadata in field_info.metadata
            if isinstance(metadata, XmlPath)
        )

    @classmethod
    def _ensure_root_tag(cls, xml_value: ET.Element, expected_root: str) -> None:
        if cls._local_name(xml_value.tag) != expected_root:
            raise InvalidBaseTagNameError(
                document_tag=xml_value.tag,
                expected=expected_root,
            )

    @classmethod
    def _find_child_by_local_name(cls, parent: ET.Element, name: str) -> ET.Element | None:
        for child in parent:
            if cls._local_name(child.tag) == name:
                return child
        return None

    @classmethod
    def _resolve_pointer(cls, xml_value: ET.Element, path_names: list[str]) -> ET.Element | None:
        pointer: ET.Element | None = xml_value
        for path_name in path_names:
            if pointer is None:
                break
            pointer = cls._find_child_by_local_name(pointer, path_name)
        return pointer

    @staticmethod
    def _extract_value_from_pointer(
        pointer: ET.Element,
        local_name: str | None,
    ) -> ET.Element | str | None:
        if local_name is None:
            return pointer
        if local_name == 'text()':
            return pointer.text
        if local_name.startswith('@'):
            return pointer.attrib.get(local_name[1:])
        return None

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

        root = ET.Element(self._qname(self.get_base_tag_name()))

        for field_name, field_value, xml_path in fields:
            pointer = root
            [root_name, *path_names], local_name = xml_path.parts()

            if self._local_name(pointer.tag) != root_name:
                raise DiffBaseTagNameInFieldError(cls=self.__class__, field_name=field_name)

            for path_name in path_names:
                qname = self._qname(path_name)
                new_pointer = pointer.find(qname)
                if new_pointer is None:
                    new_pointer = ET.SubElement(pointer, qname)
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

        kwargs: dict[str, Any] = {}

        for field_name, xml_path in cls._iter_xmlpath_fields():
            [root_name, *path_names], local_name = xml_path.parts()

            cls._ensure_root_tag(xml_value, root_name)

            pointer = cls._resolve_pointer(xml_value, path_names)
            if pointer is None:
                continue

            raw_value = cls._extract_value_from_pointer(pointer, local_name)
            if raw_value is None and local_name not in (None, 'text()'):
                continue

            kwargs[field_name] = raw_value

        parsed_kwargs = {name: cls._parse_field_value(name, value) for name, value in kwargs.items()}
        return cls(**parsed_kwargs)

    @classmethod
    def _iter_annotation_classes(cls, annotation: object | None) -> Iterator[object]:
        if annotation is None:
            return

        origin = get_origin(annotation)
        if origin in (Union, UnionType):
            for arg in get_args(annotation):
                yield from cls._iter_annotation_classes(arg)
            return

        yield annotation

    @classmethod
    def _parse_mappable_class(
        cls,
        klass: object,
        xml_value: str | ET.Element,
    ) -> object | None:
        if not (isinstance(klass, type) and issubclass(klass, MappableToXmlValue)):
            return None

        with suppress(ValueError):
            value: str | ET.Element = xml_value
            if issubclass(klass, XmlSerializerMixin) and isinstance(xml_value, ET.Element):
                base = klass.get_base_tag_name()
                for child in xml_value:
                    if cls._local_name(child.tag) == base:
                        value = child
                        break
            return klass.from_xml_value(value)

        return None

    @classmethod
    def _parse_list_of_submessages(
        cls,
        klass: object,
        xml_value: str | ET.Element,
    ) -> object | None:
        if not isinstance(klass, GenericAlias):
            return None

        origin = klass.__origin__
        if not (isinstance(origin, type) and issubclass(origin, list)):
            return None

        t = klass.__args__[0]
        if not (isinstance(t, type) and issubclass(t, XmlSerializerMixin)):
            return None

        if isinstance(xml_value, str):
            raise TypeError

        elements = [child for child in xml_value if cls._local_name(child.tag) == t.get_base_tag_name()]
        return [t.from_xml_value(element) for element in elements]

    @classmethod
    def _parse_field_value(cls, field_name: str, xml_value: str | ET.Element, /) -> object:
        annotation = cls.__pydantic_fields__[field_name].annotation

        if annotation is None:
            return str(xml_value)

        for klass in cls._iter_annotation_classes(annotation):
            parsed = cls._parse_mappable_class(klass, xml_value)
            if parsed is not None:
                return parsed

            parsed = cls._parse_list_of_submessages(klass, xml_value)
            if parsed is not None:
                return parsed

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

        ns = self.get_xml_namespace()
        if ns:
            ET.register_namespace('', ns)

        ET.indent(xml)
        return '<?xml version="1.0"?>\n' + ET.tostring(xml, encoding='unicode')

    @classmethod
    def from_xml(cls, value: str, /) -> Self:
        xml = fromstring(value)
        return cls.from_xml_value(xml)
