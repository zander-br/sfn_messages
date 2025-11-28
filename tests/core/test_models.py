from typing import Annotated
from xml.etree import ElementTree as ET

import pytest
from pydantic import BaseModel

from sfn_messages.core.errors import (
    BaseTagNameNotFoundInClassError,
    DiffBaseTagNameInFieldError,
    InvalidBaseTagNameError,
    InvalidLocalNameInFieldError,
    LocalNameNotSetInFieldError,
    LocalNameSetInFieldError,
)
from sfn_messages.core.models import BaseMessage, BaseSubMessage, XmlPath, XmlSerializerMixin
from sfn_messages.core.types import SystemDomain
from tests.conftest import normalize_xml


class TestXmlPath:
    @pytest.mark.parametrize(
        ('path', 'expected'),
        [
            ('a/b/c/text()', (['a', 'b', 'c'], 'text()')),
            ('x/y/z/@attribute', (['x', 'y', 'z'], '@attribute')),
            ('tag1/tag2/tag3/tag4/tag5', (['tag1', 'tag2', 'tag3', 'tag4', 'tag5'], None)),
        ],
    )
    def test_parts_of_text(self, path: str, expected: tuple[list[str], str | None]) -> None:
        sut = XmlPath(path)
        returned = sut.parts()

        assert returned == expected


class TestXmlSerializerMixin:
    def test_to_xml_value(self) -> None:
        expected = """
        <base>
            <header>
                <field1>value1</field1>
                <field2 attribute="value3">value2</field2>
            </header>
            <msg>
                <field4>value4</field4>
                <other field5="value5" />
            </msg>
        </base>
        """

        class Sut(XmlSerializerMixin):
            @classmethod
            def get_base_tag_name(cls) -> str:
                return 'base'

            field1: Annotated[str, XmlPath('base/header/field1/text()')]
            field2: Annotated[str, XmlPath('base/header/field2/text()')]
            field3: Annotated[str, XmlPath('base/header/field2/@attribute')]
            field4: Annotated[str, XmlPath('base/msg/field4/text()')]
            field5: Annotated[str, XmlPath('base/msg/other/@field5')]

        sut = Sut(field1='value1', field2='value2', field3='value3', field4='value4', field5='value5')
        returned = sut.to_xml_value()

        assert normalize_xml(ET.tostring(returned, encoding='unicode')) == normalize_xml(expected)

    def test_to_xml_value_shold_raise_error_for_diff_base(self) -> None:
        class Sut(XmlSerializerMixin):
            @classmethod
            def get_base_tag_name(cls) -> str:
                return 'Base1'

            field1: Annotated[str, XmlPath('Base1/field1/text()')]
            field2: Annotated[str, XmlPath('Base1/field2/text()')]
            field3: Annotated[str, XmlPath('Base2/field2/text()')]
            field4: Annotated[str, XmlPath('Base1/field2/text()')]

        sut = Sut(field1='value1', field2='value2', field3='value3', field4='value4')
        with pytest.raises(DiffBaseTagNameInFieldError) as exc_info:
            sut.to_xml_value()

        assert exc_info.value.cls == Sut
        assert exc_info.value.field_name == 'field3'

    def test_to_xml_value_shold_raise_error_for_field_dont_have_local_name(self) -> None:
        class Sut(XmlSerializerMixin):
            @classmethod
            def get_base_tag_name(cls) -> str:
                return 'Base'

            field1: Annotated[str, XmlPath('Base/field1/text()')]
            field2: Annotated[str, XmlPath('Base/field2')]

        sut = Sut(field1='value1', field2='value2')
        with pytest.raises(LocalNameNotSetInFieldError) as exc_info:
            sut.to_xml_value()

        assert exc_info.value.cls == Sut
        assert exc_info.value.field_name == 'field2'

    def test_to_xml_value_shold_raise_error_for_field_have_invalid_local_name(self) -> None:
        class Sut(XmlSerializerMixin):
            @classmethod
            def get_base_tag_name(cls) -> str:
                return 'Base'

            field1: Annotated[str, XmlPath('Base/field1/text()')]
            field2: Annotated[str, XmlPath('Base/field2/invalid()')]

        sut = Sut(field1='value1', field2='value2')
        with pytest.raises(InvalidLocalNameInFieldError) as exc_info:
            sut.to_xml_value()

        assert exc_info.value.cls == Sut
        assert exc_info.value.field_name == 'field2'

    def test_to_xml_value_shold_raise_error_for_sub_field_have_local_name(self) -> None:
        class SutField(BaseModel):
            def to_xml_value(self) -> ET.Element:
                root = ET.Element('field')
                ET.SubElement(root, 'value1').text = 'value1'
                return root

            @classmethod
            def from_xml_value(cls, xml_value: str | ET.Element) -> SutField:
                raise NotImplementedError

        class Sut(XmlSerializerMixin):
            @classmethod
            def get_base_tag_name(cls) -> str:
                return 'Base'

            field1: Annotated[SutField, XmlPath('Base/field1')]
            field2: Annotated[SutField, XmlPath('Base/field2/text()')]

        sut = Sut(field1=SutField(), field2=SutField())
        with pytest.raises(LocalNameSetInFieldError) as exc_info:
            sut.to_xml_value()

        assert exc_info.value.cls == Sut
        assert exc_info.value.field_name == 'field2'

    def test_from_xml_value(self) -> None:
        xml = """
        <base>
            <header>
                <field1>value1</field1>
                <field2 attribute="value3">value2</field2>
            </header>
            <msg>
                <field4>value4</field4>
                <other field5="value5" />
            </msg>
        </base>
        """

        class Sut(XmlSerializerMixin):
            @classmethod
            def get_base_tag_name(cls) -> str:
                return 'base'

            field1: Annotated[str, XmlPath('base/header/field1/text()')]
            field2: Annotated[str, XmlPath('base/header/field2/text()')]
            field3: Annotated[str, XmlPath('base/header/field2/@attribute')]
            field4: Annotated[str, XmlPath('base/msg/field4/text()')]
            field5: Annotated[str, XmlPath('base/msg/other/@field5')]

        returned = Sut.from_xml_value(ET.fromstring(xml))

        assert returned == Sut(field1='value1', field2='value2', field3='value3', field4='value4', field5='value5')

    def test_from_xml_value_shold_raise_error_for_string(self) -> None:
        class Sut(XmlSerializerMixin):
            @classmethod
            def get_base_tag_name(cls) -> str:
                return 'base'

        with pytest.raises(TypeError):
            Sut.from_xml_value('')

    def test_from_xml_value_shold_raise_error_for_diff_base(self) -> None:
        xml = """
        <base1>
            <header>
                <field1>value1</field1>
                <field2>value2</field2>
            </header>
        </base1>
        """

        class Sut(XmlSerializerMixin):
            @classmethod
            def get_base_tag_name(cls) -> str:
                return 'base'

            field1: Annotated[str, XmlPath('base1/header/field1/text()')]
            field2: Annotated[str, XmlPath('base2/header/field2/text()')]

        with pytest.raises(InvalidBaseTagNameError) as exc_info:
            Sut.from_xml_value(ET.fromstring(xml))

        assert exc_info.value.document_tag == 'base1'
        assert exc_info.value.expected == 'base2'


class TestBaseSubMessage:
    def test_get_base_tag_name_shold_return_base_tag_from_first_field(self) -> None:
        class Sut(BaseSubMessage):
            field1: Annotated[str, XmlPath('Base1/a/b/c/text()')]
            field2: Annotated[str, XmlPath('Base2/a/b/c/text()')]

        sut = Sut(field1='value1', field2='value2')
        returned = sut.get_base_tag_name()

        assert returned == 'Base1'

    def test_get_base_tag_name_shold_ignore_non_xml_path(self) -> None:
        class Sut(BaseSubMessage):
            field1: str
            field2: Annotated[str, XmlPath('Base2/a/b/c/text()')]

        sut = Sut(field1='value1', field2='value2')
        returned = sut.get_base_tag_name()

        assert returned == 'Base2'

    def test_get_base_tag_name_shold_raise_error_dont_have_xml_path_field(self) -> None:
        class Sut(BaseSubMessage):
            field1: str
            field2: str

        sut = Sut(field1='value1', field2='value2')
        with pytest.raises(BaseTagNameNotFoundInClassError) as exc_info:
            sut.get_base_tag_name()

        assert exc_info.value.cls == Sut

    def test_to_xml_value(self) -> None:
        expected = """
        <base>
            <field1>value1</field1>
            <field2>value2</field2>
        </base>
        """

        class Sut(BaseSubMessage):
            field1: Annotated[str, XmlPath('base/field1/text()')]
            field2: Annotated[str, XmlPath('base/field2/text()')]

        sut = Sut(field1='value1', field2='value2')
        returned = sut.to_xml_value()

        assert normalize_xml(ET.tostring(returned, encoding='unicode')) == normalize_xml(expected)

    def test_to_xml_value_with_sub_class(self) -> None:
        expected = """
        <base>
            <field1>value1</field1>
            <field2>
                <sub>
                    <field f2="v2">v1</field>
                </sub>
            </field2>
        </base>
        """

        class SubSut(BaseSubMessage):
            f1: Annotated[str, XmlPath('sub/field/text()')]
            f2: Annotated[str, XmlPath('sub/field/@f2')]

        class Sut(BaseSubMessage):
            field1: Annotated[str, XmlPath('base/field1/text()')]
            field2: Annotated[SubSut, XmlPath('base/field2')]

        sut = Sut(field1='value1', field2=SubSut(f1='v1', f2='v2'))
        returned = sut.to_xml_value()

        assert normalize_xml(ET.tostring(returned, encoding='unicode')) == normalize_xml(expected)

    def test_to_xml_value_with_sub_list(self) -> None:
        expected = """
        <base>
            <field1>value1</field1>
            <others>
                <f1>v1</f1>
                <f2>v2</f2>
            </others>
            <others>
                <f1>v3</f1>
                <f2>v4</f2>
            </others>
            <others>
                <f1>v5</f1>
                <f2>v6</f2>
            </others>
        </base>
        """

        class SubSut(BaseSubMessage):
            f1: Annotated[str, XmlPath('others/f1/text()')]
            f2: Annotated[str, XmlPath('others/f2/text()')]

        class Sut(BaseSubMessage):
            field1: Annotated[str, XmlPath('base/field1/text()')]
            field2: Annotated[list[SubSut], XmlPath('base')]

        sut = Sut(
            field1='value1',
            field2=[SubSut(f1='v1', f2='v2'), SubSut(f1='v3', f2='v4'), SubSut(f1='v5', f2='v6')],
        )
        returned = sut.to_xml_value()

        assert normalize_xml(ET.tostring(returned, encoding='unicode')) == normalize_xml(expected)

    def test_from_xml_value(self) -> None:
        xml = """
        <base>
            <field1>value1</field1>
            <field2>value2</field2>
        </base>
        """

        class Sut(BaseSubMessage):
            field1: Annotated[str, XmlPath('base/field1/text()')]
            field2: Annotated[str, XmlPath('base/field2/text()')]

        returned = Sut.from_xml_value(ET.fromstring(xml))

        assert returned == Sut(field1='value1', field2='value2')

    def test_from_xml_value_with_sub_class(self) -> None:
        xml = """
        <base>
            <field1>value1</field1>
            <field2>
                <sub>
                    <field f2="v2">v1</field>
                </sub>
            </field2>
        </base>
        """

        class SubSut(BaseSubMessage):
            f1: Annotated[str, XmlPath('sub/field/text()')]
            f2: Annotated[str, XmlPath('sub/field/@f2')]

        class Sut(BaseSubMessage):
            field1: Annotated[str, XmlPath('base/field1/text()')]
            field2: Annotated[SubSut, XmlPath('base/field2')]

        returned = Sut.from_xml_value(ET.fromstring(xml))

        assert returned == Sut(field1='value1', field2=SubSut(f1='v1', f2='v2'))

    def test_from_xml_value_with_sub_list(self) -> None:
        xml = """
        <base>
            <field1>value1</field1>
            <others>
                <f1>v1</f1>
                <f2>v2</f2>
            </others>
            <others>
                <f1>v3</f1>
                <f2>v4</f2>
            </others>
            <others>
                <f1>v5</f1>
                <f2>v6</f2>
            </others>
        </base>
        """

        class SubSut(BaseSubMessage):
            f1: Annotated[str, XmlPath('others/f1/text()')]
            f2: Annotated[str, XmlPath('others/f2/text()')]

        class Sut(BaseSubMessage):
            field1: Annotated[str, XmlPath('base/field1/text()')]
            field2: Annotated[list[SubSut], XmlPath('base')]

        returned = Sut.from_xml_value(ET.fromstring(xml))

        assert returned == Sut(
            field1='value1',
            field2=[SubSut(f1='v1', f2='v2'), SubSut(f1='v3', f2='v4'), SubSut(f1='v5', f2='v6')],
        )


class TestBaseMessage:
    def test_to_xml(self) -> None:
        expected = """
        <DOC>
            <BCMSG>
                <IdentdEmissor>12345ABC</IdentdEmissor>
                <IdentdDestinatario>67890XYZ</IdentdDestinatario>
                <DomSist>MES01</DomSist>
                <NUOp>123456781234567890123</NUOp>
            </BCMSG>
            <SISMSG>
                <Test>
                    <field1>value1</field1>
                    <field2>
                        <sub>
                            <field f2="v2">v1</field>
                        </sub>
                    </field2>
                </Test>
            </SISMSG>
        </DOC>
        """

        class SubSut(BaseSubMessage):
            f1: Annotated[str, XmlPath('sub/field/text()')]
            f2: Annotated[str, XmlPath('sub/field/@f2')]

        class Sut(BaseMessage):
            field1: Annotated[str, XmlPath('DOC/SISMSG/Test/field1/text()')]
            field2: Annotated[SubSut, XmlPath('DOC/SISMSG/Test/field2')]

        sut = Sut(
            from_ispb='12345abc',
            to_ispb='67890xyz',
            system_domain=SystemDomain.MES01,
            operation_number='123456781234567890123',
            field1='value1',
            field2=SubSut(f1='v1', f2='v2'),
        )
        returned = sut.to_xml()

        assert normalize_xml(returned) == normalize_xml(expected)

    def test_from_xml(self) -> None:
        xml = """
        <DOC>
            <BCMSG>
                <IdentdEmissor>12345ABC</IdentdEmissor>
                <IdentdDestinatario>67890XYZ</IdentdDestinatario>
                <DomSist>MES01</DomSist>
                <NUOp>123456781234567890123</NUOp>
            </BCMSG>
            <SISMSG>
                <Test>
                    <field1>value1</field1>
                    <field2>
                        <sub>
                            <field f2="v2">v1</field>
                        </sub>
                    </field2>
                </Test>
            </SISMSG>
        </DOC>
        """

        class SubSut(BaseSubMessage):
            f1: Annotated[str, XmlPath('sub/field/text()')]
            f2: Annotated[str, XmlPath('sub/field/@f2')]

        class Sut(BaseMessage):
            field1: Annotated[str, XmlPath('DOC/SISMSG/Test/field1/text()')]
            field2: Annotated[SubSut, XmlPath('DOC/SISMSG/Test/field2')]

        returned = Sut.from_xml(xml)

        assert returned == Sut(
            from_ispb='12345abc',
            to_ispb='67890xyz',
            system_domain=SystemDomain.MES01,
            operation_number='123456781234567890123',
            field1='value1',
            field2=SubSut(f1='v1', f2='v2'),
        )
