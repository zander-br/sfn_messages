from datetime import date, datetime
from typing import Annotated, Literal

from sfn_messages.core.models import BaseMessage, XmlPath
from sfn_messages.core.types import FileIdentifier, InstitutionControlNumber, Ispb, OperationNumber

from .types import TransmissionType

PATH = 'DOC/SISMSG/GEN0012'
PATH_R1 = 'DOC/SISMSG/GEN0012R1'


class GEN0012(BaseMessage):
    message_code: Annotated[Literal['GEN0012'], XmlPath(f'{PATH}/CodMsg/text()')] = 'GEN0012'
    institution_control_number: Annotated[InstitutionControlNumber, XmlPath(f'{PATH}/NumCtrlIF/text()')]
    institution_ispb: Annotated[Ispb, XmlPath(f'{PATH}/ISPBIF/text()')]
    recipient_ispb: Annotated[Ispb, XmlPath(f'{PATH}/ISPBDestinatario/text()')]
    transmission_type: Annotated[TransmissionType, XmlPath(f'{PATH}/TpTransm/text()')]
    institution_origin_control_number: Annotated[InstitutionControlNumber, XmlPath(f'{PATH}/NumCtrlSistOr/text()')]
    original_operation_number: Annotated[OperationNumber, XmlPath(f'{PATH}/NUOpOr/text()')]
    settlement_date: Annotated[date, XmlPath(f'{PATH}/DtMovto/text()')]


class GEN0012R1(BaseMessage):
    message_code: Annotated[Literal['GEN0012R1'], XmlPath(f'{PATH_R1}/CodMsg/text()')] = 'GEN0012R1'
    institution_control_number: Annotated[InstitutionControlNumber, XmlPath(f'{PATH_R1}/NumCtrlIF/text()')]
    institution_ispb: Annotated[Ispb, XmlPath(f'{PATH_R1}/ISPBIF/text()')]
    file_identifier: Annotated[FileIdentifier, XmlPath(f'{PATH_R1}/IdentdArq/text()')]
    participant_datetime: Annotated[datetime, XmlPath(f'{PATH_R1}/DtHrPart/text()')]
    settlement_date: Annotated[date, XmlPath(f'{PATH_R1}/DtMovto/text()')]
