from typing import Annotated, Literal

from sfn_messages.core.models import BaseMessage, XmlPath
from sfn_messages.core.types import Ispb

from .types import Message

PATH = 'DOC/SISMSG/GEN0001'


class GEN0001(BaseMessage):
    message_code: Annotated[Literal['GEN0001'], XmlPath(f'{PATH}/CodMsg/text()')] = 'GEN0001'
    issuing_ispb: Annotated[Ispb, XmlPath(f'{PATH}/ISPBEmissor/text()')]
    recipient_ispb: Annotated[Ispb, XmlPath(f'{PATH}/ISPBDestinatario/text()')]
    message: Annotated[Message, XmlPath(f'{PATH}/MsgECO/text()')]
