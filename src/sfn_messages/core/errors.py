class MessageCodeNotFoundError(Exception):
    def __str__(self) -> str:
        return 'Message code not found in XML'


class MessageNotImplementedError(Exception):
    def __init__(self, *, message_code: str) -> None:
        self.message_code = message_code

    def __str__(self) -> str:
        return f'Message {self.message_code} not implemented'
