class MessageCodeNotFoundError(Exception):
    def __str__(self) -> str:
        return 'Message code not found in XML'


class MessageNotImplementedError(Exception):
    def __init__(self, *, message_code: str) -> None:
        self.message_code = message_code

    def __str__(self) -> str:
        return f'Message {self.message_code} not implemented'


class BaseTagNameNotFoundInClassError(Exception):
    def __init__(self, *, cls: type) -> None:
        self.cls = cls

    def __str__(self) -> str:
        return f'Not found XmlPath annotation in fields of {self.cls}'


class InvalidBaseTagNameError(Exception):
    def __init__(self, *, document_tag: str, expected: str) -> None:
        self.document_tag = document_tag
        self.expected = expected

    def __str__(self) -> str:
        return f'Invalid base tag name in document ({self.document_tag}) expected {self.expected}'


class DiffBaseTagNameInFieldError(Exception):
    def __init__(self, *, cls: type, field_name: str) -> None:
        self.cls = cls
        self.field_name = field_name

    def __str__(self) -> str:
        return f'Diff base tag name in {self.field_name} of {self.cls}'


class LocalNameNotSetInFieldError(Exception):
    def __init__(self, *, cls: type, field_name: str) -> None:
        self.cls = cls
        self.field_name = field_name

    def __str__(self) -> str:
        return f'Local name not set for value {self.field_name} of {self.cls}'


class LocalNameSetInFieldError(Exception):
    def __init__(self, *, cls: type, field_name: str) -> None:
        self.cls = cls
        self.field_name = field_name

    def __str__(self) -> str:
        return f'Local name set for sub message {self.field_name} of {self.cls}'


class InvalidLocalNameInFieldError(Exception):
    def __init__(self, *, cls: type, field_name: str) -> None:
        self.cls = cls
        self.field_name = field_name

    def __str__(self) -> str:
        return f'Invalid local name in {self.field_name} of {self.cls}'
