from datetime import date
from typing import Annotated, Literal

from sfn_messages.core.models import BaseMessage, XmlPath
from sfn_messages.core.types import InstitutionControlNumber, Ispb

PATH = 'DOC/SISMSG/STR0013'


class STR013(BaseMessage):
    message_code: Annotated[Literal['STR0013'], XmlPath(f'{PATH}/CodMsg/text()')] = 'STR0013'
    institution_control_number: Annotated[InstitutionControlNumber, XmlPath(f'{PATH}/NumCtrlIF_LDL/text()')]
    institution_ispb: Annotated[Ispb, XmlPath(f'{PATH}/ISPBIF_LDL/text()')]
    settlement_date: Annotated[date, XmlPath(f'{PATH}/DtMovto/text()')]
