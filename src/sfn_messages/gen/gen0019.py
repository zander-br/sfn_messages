from datetime import date, datetime
from typing import Annotated, ClassVar, Literal

from pydantic import Field

from sfn_messages.core.models import BaseMessage, BaseSubMessage, XmlPath
from sfn_messages.core.types import Cpf, Description, Email, ErrorCode, InstitutionControlNumber, Ispb, Name, Telephone

from .types import IndividualIdentificationNumber, ResponsibleType

PATH = 'DOC/SISMSG/GEN0019'
PATH_GROUP = 'Grupo_GEN0019_Respons'
PATH_R1 = 'DOC/SISMSG/GEN0019R1'
PATH_E = 'DOC/SISMSG/GEN0019'
XML_NAMESPACE = 'http://www.bcb.gov.br/GEN/GEN0019.xsd'
XML_NAMESPACE_ERROR = 'http://www.bcb.gov.br/GEN/GEN0019E.xsd'


class ResponsibleTypeField(BaseSubMessage):
    responsible_type_field: Annotated[ResponsibleType, XmlPath('TpRespons/text()')]


class Responsible(BaseSubMessage):
    cpf: Annotated[Cpf | None, XmlPath(f'{PATH_GROUP}/CPFRespons/text()')]
    document: Annotated[IndividualIdentificationNumber | None, XmlPath(f'{PATH_GROUP}/NumDocRespons/text()')]
    name: Annotated[Name | None, XmlPath(f'{PATH_GROUP}/NomRespons/text()')]
    email: Annotated[Email | None, XmlPath(f'{PATH_GROUP}/EndEletrnc/text()')]
    telephone_1: Annotated[Telephone, XmlPath(f'{PATH_GROUP}/NumTelRespons1/text()')]
    telephone_2: Annotated[Telephone | None, XmlPath(f'{PATH_GROUP}/NumTelRespons2/text()')]
    telephone_3: Annotated[Telephone | None, XmlPath(f'{PATH_GROUP}/NumTelRespons3/text()')] = None
    responsible_type: Annotated[list[ResponsibleTypeField] | None, XmlPath(f'{PATH_GROUP}')] = Field(
        default_factory=list
    )


class GEN0019(BaseMessage):
    XML_NAMESPACE: ClassVar[str | None] = XML_NAMESPACE

    message_code: Annotated[Literal['GEN0019'], XmlPath(f'{PATH}/CodMsg/text()')] = 'GEN0019'
    participant_institution_control_number: Annotated[InstitutionControlNumber, XmlPath(f'{PATH}/NumCtrlPart/text()')]
    participant_ispb: Annotated[Ispb, XmlPath(f'{PATH}/ISPBPart/text()')]
    responsibles: Annotated[list[Responsible], XmlPath(f'{PATH}')] = Field(default_factory=list)
    description: Annotated[Description | None, XmlPath(f'{PATH}/Hist/text()')] = None
    settlement_date: Annotated[date, XmlPath(f'{PATH}/DtMovto/text()')]


class GEN0019R1(BaseMessage):
    XML_NAMESPACE: ClassVar[str | None] = XML_NAMESPACE

    message_code: Annotated[Literal['GEN0019R1'], XmlPath(f'{PATH_R1}/CodMsg/text()')] = 'GEN0019R1'
    participant_institution_control_number: Annotated[
        InstitutionControlNumber, XmlPath(f'{PATH_R1}/NumCtrlPart/text()')
    ]
    participant_ispb: Annotated[Ispb, XmlPath(f'{PATH_R1}/ISPBPart/text()')]
    provider_datetime: Annotated[datetime, XmlPath(f'{PATH_R1}/DtHrPrestd/text()')]
    settlement_date: Annotated[date, XmlPath(f'{PATH_R1}/DtMovto/text()')]


class ResponsibleTypeFieldError(BaseSubMessage):
    responsible_type_field: Annotated[ResponsibleType, XmlPath('TpRespons/text()')]


class ResponsibleError(BaseSubMessage):
    cpf: Annotated[Cpf | None, XmlPath(f'{PATH_GROUP}/CPFRespons/text()')] = None
    document: Annotated[IndividualIdentificationNumber | None, XmlPath(f'{PATH_GROUP}/NumDocRespons/text()')] = None
    name: Annotated[Name | None, XmlPath(f'{PATH_GROUP}/NomRespons/text()')] = None
    email: Annotated[Email | None, XmlPath(f'{PATH_GROUP}/EndEletrnc/text()')] = None
    telephone_1: Annotated[Telephone | None, XmlPath(f'{PATH_GROUP}/NumTelRespons1/text()')] = None
    telephone_2: Annotated[Telephone | None, XmlPath(f'{PATH_GROUP}/NumTelRespons2/text()')] = None
    telephone_3: Annotated[Telephone | None, XmlPath(f'{PATH_GROUP}/NumTelRespons3/text()')] = None
    responsible_type: Annotated[list[ResponsibleTypeFieldError] | None, XmlPath(f'{PATH_GROUP}')] = Field(
        default_factory=list
    )

    cpf_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH_GROUP}/CPFRespons/@CodErro')] = None
    document_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH_GROUP}/NumDocRespons/@CodErro')] = None
    name_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH_GROUP}/NomRespons/@CodErro')] = None
    email_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH_GROUP}/EndEletrnc/@CodErro')] = None
    telephone_1_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH_GROUP}/NumTelRespons1/@CodErro')] = None
    telephone_2_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH_GROUP}/NumTelRespons2/@CodErro')] = None
    telephone_3_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH_GROUP}/NumTelRespons3/@CodErro')] = None
    responsible_type_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH_GROUP}/TpRespons/@CodErro')] = None


class GEN0019E(BaseMessage):
    XML_NAMESPACE: ClassVar[str | None] = XML_NAMESPACE_ERROR

    message_code: Annotated[Literal['GEN0019E'], XmlPath(f'{PATH_E}/CodMsg/text()')] = 'GEN0019E'
    participant_institution_control_number: Annotated[
        InstitutionControlNumber | None, XmlPath(f'{PATH_E}/NumCtrlPart/text()')
    ] = None
    participant_ispb: Annotated[Ispb | None, XmlPath(f'{PATH_E}/ISPBPart/text()')] = None
    responsibles: Annotated[list[ResponsibleError], XmlPath(f'{PATH_E}')] = Field(default_factory=list)
    description: Annotated[Description | None, XmlPath(f'{PATH_E}/Hist/text()')] = None
    settlement_date: Annotated[date | None, XmlPath(f'{PATH_E}/DtMovto/text()')] = None

    general_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH_E}/@CodErro')] = None
    participant_institution_control_number_error_code: Annotated[
        ErrorCode | None, XmlPath(f'{PATH_E}/NumCtrlPart/@CodErro')
    ] = None
    participant_ispb_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH_E}/ISPBPart/@CodErro')] = None
    description_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH_E}/Hist/@CodErro')] = None
    settlement_date_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH_E}/DtMovto/@CodErro')] = None
