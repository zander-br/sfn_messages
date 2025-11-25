from typing import Annotated, Literal

from sfn_messages.core.models import BaseMessage, XmlPath
from sfn_messages.core.types import Ispb

from .types import Message

PATH = 'DOC/SISMSG/GEN0001'
PATH_R1 = 'DOC/SISMSG/GEN0001R1'


class GEN0001(BaseMessage):
    message_code: Annotated[Literal['GEN0001'], XmlPath(f'{PATH}/CodMsg/text()')] = 'GEN0001'
    issuing_ispb: Annotated[Ispb, XmlPath(f'{PATH}/ISPBEmissor/text()')]
    recipient_ispb: Annotated[Ispb, XmlPath(f'{PATH}/ISPBDestinatario/text()')]
    message: Annotated[Message, XmlPath(f'{PATH}/MsgECO/text()')]


class GEN0001R1(BaseMessage):
    message_code: Annotated[Literal['GEN0001R1'], XmlPath(f'{PATH_R1}/CodMsg/text()')] = 'GEN0001R1'
    issuing_ispb: Annotated[Ispb, XmlPath(f'{PATH_R1}/ISPBEmissor/text()')]
    recipient_ispb: Annotated[Ispb, XmlPath(f'{PATH_R1}/ISPBDestinatario/text()')]
    message: Annotated[Message, XmlPath(f'{PATH_R1}/MsgECO/text()')]
