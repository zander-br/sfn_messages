from typing import Annotated, Literal

from sfn_messages.core.models import BaseMessage, XmlPath
from sfn_messages.core.types import InstitutionControlNumber, Ispb

PATH = 'DOC/SISMSG/GEN0003'


class GEN0003(BaseMessage):
    message_code: Annotated[Literal['GEN0003'], XmlPath(f'{PATH}/CodMsg/text()')] = 'GEN0003'
    institution_control_number: Annotated[InstitutionControlNumber, XmlPath(f'{PATH}/NumCtrlIF/text()')]
    issuing_ispb: Annotated[Ispb, XmlPath(f'{PATH}/ISPBEmissor/text()')]
    recipient_ispb: Annotated[Ispb, XmlPath(f'{PATH}/ISPBDestinatario/text()')]
