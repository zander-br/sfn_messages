class InvalidMessageCodeError(Exception):
    def __str__(self) -> str:
        return 'Message code not found in XML'


class MessageDefaultVersionError(Exception):
    def __init__(self, *, message_code: str) -> None:
        self.message_code = message_code

    def __str__(self) -> str:
        return f'{self.message_code} does not have a default version'


class MessageNotImplementedError(Exception):
    def __init__(self, *, message_code: str, version: str) -> None:
        self.message_code = message_code
        self.version = version

    def __str__(self) -> str:
        return f'{self.message_code} version {self.version} is not implemented'
