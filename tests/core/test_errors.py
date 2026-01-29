import pytest

from sfn_messages.core.errors import (
    BaseTagNameNotFoundInClassError,
    DiffBaseTagNameInFieldError,
    InvalidBaseTagNameError,
    InvalidLocalNameInFieldError,
    LocalNameNotSetInFieldError,
    LocalNameSetInFieldError,
    MessageCodeNotFoundError,
    MessageNotImplementedError,
)


def test_message_code_not_found_error_str() -> None:
    exc = MessageCodeNotFoundError()
    assert str(exc) == 'Message code not found in XML'


@pytest.mark.parametrize(
    ('message_code', 'expected_message'),
    [
        ('ABC', 'Message ABC not implemented'),
        ('SME0001', 'Message SME0001 not implemented'),
    ],
)
def test_message_not_implemented_error_str(
    message_code: str,
    expected_message: str,
) -> None:
    exc = MessageNotImplementedError(message_code=message_code)
    assert exc.message_code == message_code
    assert str(exc) == expected_message


@pytest.mark.parametrize(
    'cls',
    [
        dict,
        list,
        Exception,
    ],
)
def test_base_tag_name_not_found_in_class_error_str(cls: type) -> None:
    exc = BaseTagNameNotFoundInClassError(cls=cls)
    assert exc.cls is cls
    assert str(exc) == f'Not found XmlPath annotation in fields of {cls}'


@pytest.mark.parametrize(
    ('document_tag', 'expected'),
    [
        ('Root', 'ExpectedRoot'),
        ('Message', 'Envelope'),
    ],
)
def test_invalid_base_tag_name_error_str(
    document_tag: str,
    expected: str,
) -> None:
    exc = InvalidBaseTagNameError(
        document_tag=document_tag,
        expected=expected,
    )
    assert exc.document_tag == document_tag
    assert exc.expected == expected
    assert str(exc) == f'Invalid base tag name in document ({document_tag}) expected {expected}'


@pytest.mark.parametrize(
    ('cls', 'field_name'),
    [
        (dict, 'field_a'),
        (list, 'field_b'),
    ],
)
def test_diff_base_tag_name_in_field_error_str(
    cls: type,
    field_name: str,
) -> None:
    exc = DiffBaseTagNameInFieldError(
        cls=cls,
        field_name=field_name,
    )
    assert exc.cls is cls
    assert exc.field_name == field_name
    assert str(exc) == f'Diff base tag name in {field_name} of {cls}'


@pytest.mark.parametrize(
    ('cls', 'field_name'),
    [
        (dict, 'value'),
        (list, 'amount'),
    ],
)
def test_local_name_not_set_in_field_error_str(
    cls: type,
    field_name: str,
) -> None:
    exc = LocalNameNotSetInFieldError(
        cls=cls,
        field_name=field_name,
    )
    assert exc.cls is cls
    assert exc.field_name == field_name
    assert str(exc) == f'Local name not set for value {field_name} of {cls}'


@pytest.mark.parametrize(
    ('cls', 'field_name'),
    [
        (dict, 'sub_message'),
        (list, 'child'),
    ],
)
def test_local_name_set_in_field_error_str(
    cls: type,
    field_name: str,
) -> None:
    exc = LocalNameSetInFieldError(
        cls=cls,
        field_name=field_name,
    )
    assert exc.cls is cls
    assert exc.field_name == field_name
    assert str(exc) == f'Local name set for sub message {field_name} of {cls}'


@pytest.mark.parametrize(
    ('cls', 'field_name'),
    [
        (dict, 'invalid'),
        (list, 'wrong'),
    ],
)
def test_invalid_local_name_in_field_error_str(
    cls: type,
    field_name: str,
) -> None:
    exc = InvalidLocalNameInFieldError(
        cls=cls,
        field_name=field_name,
    )
    assert exc.cls is cls
    assert exc.field_name == field_name
    assert str(exc) == f'Invalid local name in {field_name} of {cls}'
