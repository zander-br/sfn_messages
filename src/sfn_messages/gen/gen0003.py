from datetime import datetime
from typing import Annotated, ClassVar, Literal

from sfn_messages.core.models import BaseMessage, XmlPath
from sfn_messages.core.types import InstitutionControlNumber, Ispb

from .types import LastOperationNumber

PATH = 'DOC/SISMSG/GEN0003'
PATH_R1 = 'DOC/SISMSG/GEN0003R1'
XML_NAMESPACE = 'http://www.bcb.gov.br/GEN/GEN0003.xsd'


class GEN0003(BaseMessage):
    XML_NAMESPACE: ClassVar[str | None] = XML_NAMESPACE

    message_code: Annotated[Literal['GEN0003'], XmlPath(f'{PATH}/CodMsg/text()')] = 'GEN0003'
    institution_control_number: Annotated[InstitutionControlNumber, XmlPath(f'{PATH}/NumCtrlIF/text()')]
    issuing_ispb: Annotated[Ispb, XmlPath(f'{PATH}/ISPBEmissor/text()')]
    recipient_ispb: Annotated[Ispb, XmlPath(f'{PATH}/ISPBDestinatario/text()')]


class GEN0003R1(BaseMessage):
    XML_NAMESPACE: ClassVar[str | None] = XML_NAMESPACE

    message_code: Annotated[Literal['GEN0003R1'], XmlPath(f'{PATH_R1}/CodMsg/text()')] = 'GEN0003R1'
    institution_control_number: Annotated[InstitutionControlNumber, XmlPath(f'{PATH_R1}/NumCtrlIF/text()')]
    issuing_ispb: Annotated[Ispb, XmlPath(f'{PATH_R1}/ISPBEmissor/text()')]
    recipient_ispb: Annotated[Ispb, XmlPath(f'{PATH_R1}/ISPBDestinatario/text()')]
    last_number_operation: Annotated[LastOperationNumber, XmlPath(f'{PATH_R1}/NumUltOp/text()')]
    last_message_datetime: Annotated[datetime, XmlPath(f'{PATH_R1}/DtHrUltMsg/text()')]
    participant_datetime: Annotated[datetime, XmlPath(f'{PATH_R1}/DtHrPart/text()')]
