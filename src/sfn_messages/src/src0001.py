from datetime import date, datetime
from typing import Annotated, ClassVar, Literal

from pydantic import Field

from sfn_messages.core.models import BaseMessage, BaseSubMessage, XmlPath
from sfn_messages.core.types import Cnpj, Cpf, ErrorCode, InstitutionControlNumber, Ispb

from .types import ProductPermissionIndicator, ProtectionType, SrcControlNumber

PATH = 'DOC/SISMSG/SRC0001'
PATH_R1 = 'DOC/SISMSG/SRC0001R1'
PATH_R1_PERMISSION_GROUP = 'Grupo_SRC0001R1_PermsProdt'
PATH_E = 'DOC/SISMSG/SRC0001'
XML_NAMESPACE = 'http://www.bcb.gov.br/MES/SRC0001.xsd'
XML_NAMESPACE_ERROR = 'http://www.bcb.gov.br/MES/SRC0001E.xsd'


class SRC0001(BaseMessage):
    XML_NAMESPACE: ClassVar[str | None] = XML_NAMESPACE

    message_code: Annotated[Literal['SRC0001'], XmlPath(f'{PATH}/CodMsg/text()')] = 'SRC0001'
    institution_control_number: Annotated[InstitutionControlNumber, XmlPath(f'{PATH}/NumCtrlIF/text()')]
    responsible_entity_base_cnpj: Annotated[Ispb, XmlPath(f'{PATH}/CNPJBaseEntRespons/text()')]
    institution_base_cnpj: Annotated[Ispb | None, XmlPath(f'{PATH}/CNPJBaseIF/text()')] = None
    document: Annotated[Cnpj | Cpf, XmlPath(f'{PATH}/CNPJ_CPF/text()')]
    protection_type: Annotated[ProtectionType, XmlPath(f'{PATH}/TpProtc/text()')]
    settlement_date: Annotated[date, XmlPath(f'{PATH}/DtMovto/text()')]


class ProductPermissionGroup(BaseSubMessage):
    protection_type: Annotated[ProtectionType, XmlPath(f'{PATH_R1_PERMISSION_GROUP}/TpProtc/text()')]
    product_permission_indicator: Annotated[
        ProductPermissionIndicator,
        XmlPath(f'{PATH_R1_PERMISSION_GROUP}/IndrPermsProdt/text()'),
    ]


class SRC0001R1(BaseMessage):
    XML_NAMESPACE: ClassVar[str | None] = XML_NAMESPACE

    message_code: Annotated[Literal['SRC0001R1'], XmlPath(f'{PATH_R1}/CodMsg/text()')] = 'SRC0001R1'
    institution_control_number: Annotated[InstitutionControlNumber, XmlPath(f'{PATH_R1}/NumCtrlIF/text()')]
    responsible_entity_base_cnpj: Annotated[Ispb, XmlPath(f'{PATH_R1}/CNPJBaseEntRespons/text()')]
    src_control_number: Annotated[SrcControlNumber, XmlPath(f'{PATH_R1}/NumCtrlSRC/text()')]
    product_permissions: Annotated[list[ProductPermissionGroup], XmlPath(f'{PATH_R1}')] = Field(default_factory=list)
    vendor_timestamp: Annotated[datetime, XmlPath(f'{PATH_R1}/DtHrBC/text()')]
    settlement_date: Annotated[date, XmlPath(f'{PATH_R1}/DtMovto/text()')]


class SRC0001E(BaseMessage):
    XML_NAMESPACE: ClassVar[str | None] = XML_NAMESPACE_ERROR

    message_code: Annotated[Literal['SRC0001E'], XmlPath(f'{PATH_E}/CodMsg/text()')] = 'SRC0001E'
    institution_control_number: Annotated[InstitutionControlNumber | None, XmlPath(f'{PATH_E}/NumCtrlIF/text()')] = (
        None
    )
    responsible_entity_base_cnpj: Annotated[Ispb | None, XmlPath(f'{PATH_E}/CNPJBaseEntRespons/text()')] = None
    institution_base_cnpj: Annotated[Ispb | None, XmlPath(f'{PATH_E}/CNPJBaseIF/text()')] = None
    document: Annotated[Cnpj | Cpf | None, XmlPath(f'{PATH_E}/CNPJ_CPF/text()')] = None
    protection_type: Annotated[ProtectionType | None, XmlPath(f'{PATH_E}/TpProtc/text()')] = None
    settlement_date: Annotated[date | None, XmlPath(f'{PATH_E}/DtMovto/text()')] = None

    general_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH_E}/@CodErro')] = None
    institution_control_number_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH_E}/NumCtrlIF/@CodErro')] = None
    responsible_entity_base_cnpj_error_code: Annotated[
        ErrorCode | None,
        XmlPath(f'{PATH_E}/CNPJBaseEntRespons/@CodErro'),
    ] = None
    institution_base_cnpj_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH_E}/CNPJBaseIF/@CodErro')] = None
    document_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH_E}/CNPJ_CPF/@CodErro')] = None
    protection_type_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH_E}/TpProtc/@CodErro')] = None
    settlement_date_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH_E}/DtMovto/@CodErro')] = None
