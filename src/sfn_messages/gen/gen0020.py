from datetime import date, datetime
from typing import Annotated, ClassVar, Literal

from pydantic import Field

from sfn_messages.core.models import BaseMessage, BaseSubMessage, XmlPath
from sfn_messages.core.types import Cpf, Description, Email, ErrorCode, InstitutionControlNumber, Ispb, Name, Telephone

from .types import IndividualIdentificationNumber, ResponsibleType

PATH = 'DOC/SISMSG/GEN0020'
PATH_R1 = 'DOC/SISMSG/GEN0020R1'
PATH_R1_GROUP = 'Grupo_GEN0020R1_Respons'
PATH_E = 'DOC/SISMSG/GEN0020E'
XML_NAMESPACE = 'http://www.bcb.gov.br/GEN/GEN0020.xsd'
XML_NAMESPACE_ERROR = 'http://www.bcb.gov.br/GEN/GEN0020E.xsd'


class GEN0020(BaseMessage):
    XML_NAMESPACE: ClassVar[str | None] = XML_NAMESPACE

    message_code: Annotated[Literal['GEN0020'], XmlPath(f'{PATH}/CodMsg/text()')] = 'GEN0020'
    participant_institution_control_number: Annotated[InstitutionControlNumber, XmlPath(f'{PATH}/NumCtrlPart/text()')]
    participant_ispb: Annotated[Ispb, XmlPath(f'{PATH}/ISPBPart/text()')]
    parcitipant_consulted_ispb: Annotated[Ispb | None, XmlPath(f'{PATH}/ISPBPartConsd/text()')] = None
    settlement_date: Annotated[date, XmlPath(f'{PATH}/DtMovto/text()')]


class Responsible(BaseSubMessage):
    cpf: Annotated[Cpf | None, XmlPath(f'{PATH_R1_GROUP}/CPFRespons/text()')] = None
    document: Annotated[IndividualIdentificationNumber | None, XmlPath(f'{PATH_R1_GROUP}/NumDocRespons/text()')] = None
    name: Annotated[Name | None, XmlPath(f'{PATH_R1_GROUP}/NomRespons/text()')] = None
    email: Annotated[Email | None, XmlPath(f'{PATH_R1_GROUP}/EndEletrnc/text()')] = None
    telephone_1: Annotated[Telephone, XmlPath(f'{PATH_R1_GROUP}/NumTelRespons1/text()')]
    telephone_2: Annotated[Telephone | None, XmlPath(f'{PATH_R1_GROUP}/NumTelRespons2/text()')] = None
    telephone_3: Annotated[Telephone | None, XmlPath(f'{PATH_R1_GROUP}/NumTelRespons3/text()')] = None
    responsible_type: Annotated[ResponsibleType | None, XmlPath(f'{PATH_R1_GROUP}/TpRespons/text()')] = None


class GEN0020R1(BaseMessage):
    XML_NAMESPACE: ClassVar[str | None] = XML_NAMESPACE

    message_code: Annotated[Literal['GEN0020R1'], XmlPath(f'{PATH_R1}/CodMsg/text()')] = 'GEN0020R1'
    participant_institution_control_number: Annotated[
        InstitutionControlNumber, XmlPath(f'{PATH_R1}/NumCtrlPart/text()')
    ]
    participant_ispb: Annotated[Ispb, XmlPath(f'{PATH_R1}/ISPBPart/text()')]
    parcitipant_consulted_ispb: Annotated[Ispb | None, XmlPath(f'{PATH_R1}/ISPBPartConsd/text()')] = None
    responsibles: Annotated[list[Responsible], XmlPath(f'{PATH_R1}')] = Field(default_factory=list)
    original_description: Annotated[Description | None, XmlPath(f'{PATH_R1}/HistOr/text()')] = None
    original_provider_datetime: Annotated[datetime | None, XmlPath(f'{PATH_R1}/DtHrPrestdOr/text()')] = None
    provider_datetime: Annotated[datetime, XmlPath(f'{PATH_R1}/DtHrPrestd/text()')]
    settlement_date: Annotated[date, XmlPath(f'{PATH_R1}/DtMovto/text()')]


class GEN0020E(BaseMessage):
    XML_NAMESPACE: ClassVar[str | None] = XML_NAMESPACE_ERROR

    message_code: Annotated[Literal['GEN0020'], XmlPath(f'{PATH_E}/CodMsg/text()')] = 'GEN0020'
    participant_institution_control_number: Annotated[
        InstitutionControlNumber, XmlPath(f'{PATH_E}/NumCtrlPart/text()')
    ]
    participant_ispb: Annotated[Ispb, XmlPath(f'{PATH_E}/ISPBPart/text()')]
    parcitipant_consulted_ispb: Annotated[Ispb | None, XmlPath(f'{PATH_E}/ISPBPartConsd/text()')] = None
    settlement_date: Annotated[date, XmlPath(f'{PATH_E}/DtMovto/text()')]

    general_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH_E}/@CodErro')] = None
    participant_institution_control_number_error_code: Annotated[
        ErrorCode | None, XmlPath(f'{PATH_E}/NumCtrlPart/@CodErro')
    ] = None
    participant_ispb_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH_E}/ISPBPart/@CodErro')] = None
    parcitipant_consulted_ispb_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH_E}/ISPBPartConsd/@CodErro')] = (
        None
    )
    settlement_date_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH_E}/DtMovto/@CodErro')] = None
