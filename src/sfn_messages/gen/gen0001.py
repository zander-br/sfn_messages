from typing import Annotated, ClassVar, Literal

from sfn_messages.core.models import BaseMessage, XmlPath
from sfn_messages.core.types import ErrorCode, Ispb

from .types import Message

PATH = 'DOC/SISMSG/GEN0001'
PATH_R1 = 'DOC/SISMSG/GEN0001R1'
PATH_E = 'DOC/SISMSG/GEN0001'
XML_NAMESPACE = 'http://www.bcb.gov.br/GEN/GEN0001.xsd'
XML_NAMESPACE_ERROR = 'http://www.bcb.gov.br/GEN/GEN0001E.xsd'


class GEN0001(BaseMessage):
    XML_NAMESPACE: ClassVar[str | None] = XML_NAMESPACE

    message_code: Annotated[Literal['GEN0001'], XmlPath(f'{PATH}/CodMsg/text()')] = 'GEN0001'
    issuing_ispb: Annotated[Ispb, XmlPath(f'{PATH}/ISPBEmissor/text()')]
    recipient_ispb: Annotated[Ispb, XmlPath(f'{PATH}/ISPBDestinatario/text()')]
    message: Annotated[Message, XmlPath(f'{PATH}/MsgECO/text()')]


class GEN0001R1(BaseMessage):
    XML_NAMESPACE: ClassVar[str | None] = XML_NAMESPACE

    message_code: Annotated[Literal['GEN0001R1'], XmlPath(f'{PATH_R1}/CodMsg/text()')] = 'GEN0001R1'
    issuing_ispb: Annotated[Ispb, XmlPath(f'{PATH_R1}/ISPBEmissor/text()')]
    recipient_ispb: Annotated[Ispb, XmlPath(f'{PATH_R1}/ISPBDestinatario/text()')]
    message: Annotated[Message, XmlPath(f'{PATH_R1}/MsgECO/text()')]


class GEN0001E(BaseMessage):
    XML_NAMESPACE: ClassVar[str | None] = XML_NAMESPACE_ERROR

    message_code: Annotated[Literal['GEN0001E'], XmlPath(f'{PATH_E}/CodMsg/text()')] = 'GEN0001E'
    issuing_ispb: Annotated[Ispb | None, XmlPath(f'{PATH_E}/ISPBEmissor/text()')] = None
    recipient_ispb: Annotated[Ispb | None, XmlPath(f'{PATH_E}/ISPBDestinatario/text()')] = None
    message: Annotated[Message | None, XmlPath(f'{PATH_E}/MsgECO/text()')] = None

    general_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH_E}/@CodErro')] = None
    issuing_ispb_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH_E}/ISPBEmissor/@CodErro')] = None
    recipient_ispb_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH_E}/ISPBDestinatario/@CodErro')] = None
    message_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH_E}/MsgECO/@CodErro')] = None
