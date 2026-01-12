from datetime import datetime
from typing import Annotated, ClassVar, Literal

from sfn_messages.core.models import BaseMessage, XmlPath
from sfn_messages.core.types import (
    Description,
    ErrorCode,
    Ispb,
    OperationNumber,
    StaProtocolNumber,
)

from .types import MqMessageNumber

PATH = 'DOC/SISMSG/GEN0004'
XML_NAMESPACE = 'http://www.bcb.gov.br/GEN/GEN0004.xsd'


class GEN0004(BaseMessage):
    XML_NAMESPACE: ClassVar[str | None] = XML_NAMESPACE

    message_code: Annotated[Literal['GEN0004'], XmlPath(f'{PATH}/CodMsg/text()')] = 'GEN0004'
    generic_error: Annotated[ErrorCode, XmlPath(f'{PATH}/ErroGEN/text()')]
    issuing_ispb: Annotated[Ispb, XmlPath(f'{PATH}/ISPBEmissor/text()')]
    recipient_ispb: Annotated[Ispb, XmlPath(f'{PATH}/ISPBDestinatario/text()')]
    mq_number: Annotated[MqMessageNumber | None, XmlPath(f'{PATH}/NumMQ/text()')] = None
    unique_operation_number: Annotated[OperationNumber | None, XmlPath(f'{PATH}/NUOpOr/text()')] = None
    original_protocol_sta_number: Annotated[StaProtocolNumber | None, XmlPath(f'{PATH}/NumProtSTAOr/text()')] = None
    description: Annotated[Description | None, XmlPath(f'{PATH}/Hist/text()')] = None
    participant_datetime: Annotated[datetime, XmlPath(f'{PATH}/DtHrPart/text()')]
