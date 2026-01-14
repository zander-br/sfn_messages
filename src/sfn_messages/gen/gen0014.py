from datetime import date, datetime
from typing import Annotated, ClassVar, Literal

from sfn_messages.core.models import BaseMessage, XmlPath
from sfn_messages.core.types import ErrorCode, InstitutionControlNumber, Ispb, Name

from .types import SelectionCriteria, TransmissionType

PATH = 'DOC/SISMSG/GEN0014'
PATH_R1 = 'DOC/SISMSG/GEN0014R1'
PATH_E = 'DOC/SISMSG/GEN0014E'
XML_NAMESPACE = 'http://www.bcb.gov.br/GEN/GEN0014.xsd'
XML_NAMESPACE_ERROR = 'http://www.bcb.gov.br/GEN/GEN0014E.xsd'


class GEN0014(BaseMessage):
    XML_NAMESPACE: ClassVar[str | None] = XML_NAMESPACE

    message_code: Annotated[Literal['GEN0014'], XmlPath(f'{PATH}/CodMsg/text()')] = 'GEN0014'
    institution_control_number: Annotated[InstitutionControlNumber, XmlPath(f'{PATH}/NumCtrlIF/text()')]
    issuing_ispb: Annotated[Ispb, XmlPath(f'{PATH}/ISPBEmissor/text()')]
    recipient_ispb: Annotated[Ispb, XmlPath(f'{PATH}/ISPBDestinatario/text()')]
    file_name: Annotated[Name, XmlPath(f'{PATH}/NomArq/text()')]
    selection_criteria: Annotated[SelectionCriteria | None, XmlPath(f'{PATH}/CritSelec/text()')] = None
    transmission_type: Annotated[TransmissionType, XmlPath(f'{PATH}/TpTransm/text()')]
    settlement_date: Annotated[date, XmlPath(f'{PATH}/DtMovto/text()')]


class GEN0014R1(BaseMessage):
    XML_NAMESPACE: ClassVar[str | None] = XML_NAMESPACE

    message_code: Annotated[Literal['GEN0014R1'], XmlPath(f'{PATH_R1}/CodMsg/text()')] = 'GEN0014R1'
    institution_control_number: Annotated[InstitutionControlNumber, XmlPath(f'{PATH_R1}/NumCtrlIF/text()')]
    institution_request_control_number: Annotated[InstitutionControlNumber, XmlPath(f'{PATH_R1}/NumCtrlReqIF/text()')]
    institution_ispb: Annotated[Ispb, XmlPath(f'{PATH_R1}/ISPBIF/text()')]
    institution_datetime: Annotated[datetime, XmlPath(f'{PATH_R1}/DtHrIF/text()')]
    settlement_date: Annotated[date, XmlPath(f'{PATH_R1}/DtMovto/text()')]


class GEN0014E(BaseMessage):
    XML_NAMESPACE: ClassVar[str | None] = XML_NAMESPACE_ERROR

    message_code: Annotated[Literal['GEN0014'], XmlPath(f'{PATH_E}/CodMsg/text()')] = 'GEN0014'
    institution_control_number: Annotated[InstitutionControlNumber, XmlPath(f'{PATH_E}/NumCtrlIF/text()')]
    issuing_ispb: Annotated[Ispb, XmlPath(f'{PATH_E}/ISPBEmissor/text()')]
    recipient_ispb: Annotated[Ispb, XmlPath(f'{PATH_E}/ISPBDestinatario/text()')]
    file_name: Annotated[Name, XmlPath(f'{PATH_E}/NomArq/text()')]
    selection_criteria: Annotated[SelectionCriteria | None, XmlPath(f'{PATH_E}/CritSelec/text()')] = None
    transmission_type: Annotated[TransmissionType, XmlPath(f'{PATH_E}/TpTransm/text()')]
    settlement_date: Annotated[date, XmlPath(f'{PATH_E}/DtMovto/text()')]

    general_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH_E}/@CodErro')] = None
    institution_control_number_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH_E}/NumCtrlIF/@CodErro')] = None
    issuing_ispb_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH_E}/ISPBEmissor/@CodErro')] = None
    recipient_ispb_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH_E}/ISPBDestinatario/@CodErro')] = None
    file_name_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH_E}/NomArq/@CodErro')] = None
    selection_criteria_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH_E}/CritSelec/@CodErro')] = None
    transmission_type_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH_E}/TpTransm/@CodErro')] = None
    settlement_date_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH_E}/DtMovto/@CodErro')] = None
