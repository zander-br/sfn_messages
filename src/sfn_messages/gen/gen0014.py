from datetime import date, datetime
from typing import Annotated, Literal

from sfn_messages.core.models import BaseMessage, XmlPath
from sfn_messages.core.types import InstitutionControlNumber, Ispb, Name

from .types import SelectionCriteria, TransmissionType

PATH = 'DOC/SISMSG/GEN0014'
PATH_R1 = 'DOC/SISMSG/GEN0014R1'


class GEN0014(BaseMessage):
    message_code: Annotated[Literal['GEN0014'], XmlPath(f'{PATH}/CodMsg/text()')] = 'GEN0014'
    institution_control_number: Annotated[InstitutionControlNumber, XmlPath(f'{PATH}/NumCtrlIF/text()')]
    issuing_ispb: Annotated[Ispb, XmlPath(f'{PATH}/ISPBEmissor/text()')]
    recipient_ispb: Annotated[Ispb, XmlPath(f'{PATH}/ISPBDestinatario/text()')]
    file_name: Annotated[Name, XmlPath(f'{PATH}/NomArq/text()')]
    selection_criteria: Annotated[SelectionCriteria, XmlPath(f'{PATH}/CritSelec/text()')]
    transmission_type: Annotated[TransmissionType, XmlPath(f'{PATH}/TpTransm/text()')]
    settlement_date: Annotated[date, XmlPath(f'{PATH}/DtMovto/text()')]


class GEN0014R1(BaseMessage):
    message_code: Annotated[Literal['GEN0014R1'], XmlPath(f'{PATH_R1}/CodMsg/text()')] = 'GEN0014R1'
    institution_control_number: Annotated[InstitutionControlNumber, XmlPath(f'{PATH_R1}/NumCtrlIF/text()')]
    institution_request_control_number: Annotated[InstitutionControlNumber, XmlPath(f'{PATH_R1}/NumCtrlReqIF/text()')]
    institution_ispb: Annotated[Ispb, XmlPath(f'{PATH_R1}/ISPBIF/text()')]
    institution_datetime: Annotated[datetime, XmlPath(f'{PATH_R1}/DtHrIF/text()')]
    settlement_date: Annotated[date, XmlPath(f'{PATH_R1}/DtMovto/text()')]
