from datetime import date
from typing import Annotated, Literal

from sfn_messages.core.models import BaseMessage, XmlPath
from sfn_messages.core.types import InstitutionControlNumber, Ispb

PATH = 'DOC/SISMSG/GEN0020'


class GEN0020(BaseMessage):
    message_code: Annotated[Literal['GEN0020'], XmlPath(f'{PATH}/CodMsg/text()')] = 'GEN0020'
    participant_institution_control_number: Annotated[InstitutionControlNumber, XmlPath(f'{PATH}/NumCtrlPart/text()')]
    participant_ispb: Annotated[Ispb, XmlPath(f'{PATH}/ISPBPart/text()')]
    parcitipant_consulted_ispb: Annotated[Ispb, XmlPath(f'{PATH}/ISPBPartConsd/text()')]
    settlement_date: Annotated[date, XmlPath(f'{PATH}/DtMovto/text()')]
