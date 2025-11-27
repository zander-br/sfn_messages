from datetime import date, datetime
from typing import Annotated, Literal

from sfn_messages.core.models import BaseMessage, XmlPath
from sfn_messages.core.types import Amount, InstitutionControlNumber, Ispb

PATH = 'DOC/SISMSG/STR0013'
PATH_R1 = 'DOC/SISMSG/STR0013R1'


class STR013(BaseMessage):
    message_code: Annotated[Literal['STR0013'], XmlPath(f'{PATH}/CodMsg/text()')] = 'STR0013'
    institution_control_number: Annotated[InstitutionControlNumber, XmlPath(f'{PATH}/NumCtrlIF_LDL/text()')]
    institution_ispb: Annotated[Ispb, XmlPath(f'{PATH}/ISPBIF_LDL/text()')]
    settlement_date: Annotated[date, XmlPath(f'{PATH}/DtMovto/text()')]


class STR013R1(BaseMessage):
    message_code: Annotated[Literal['STR0013R1'], XmlPath(f'{PATH_R1}/CodMsg/text()')] = 'STR0013R1'
    institution_control_number: Annotated[InstitutionControlNumber, XmlPath(f'{PATH_R1}/NumCtrlIF_LDL/text()')]
    institution_ispb: Annotated[Ispb, XmlPath(f'{PATH_R1}/ISPBIF_LDL/text()')]
    balance: Annotated[Amount, XmlPath(f'{PATH_R1}/SldRB_CL/text()')]
    vendor_timestamp: Annotated[datetime, XmlPath(f'{PATH_R1}/DtHrBC/text()')]
    settlement_date: Annotated[date, XmlPath(f'{PATH_R1}/DtMovto/text()')]
