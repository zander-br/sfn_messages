from datetime import date, datetime
from decimal import Decimal
from typing import Annotated, ClassVar, Literal

from pydantic import Field

from sfn_messages.core.models import BaseMessage, BaseSubMessage, XmlPath
from sfn_messages.core.types import (
    Cnpj,
    InstitutionControlNumber,
    Ispb,
    LdlControlNumber,
    LdlSettlementStatus,
    ParticipantIdentifier,
    StrControlNumber,
)

PATH = 'DOC/SISMSG/LDL0004'
PATH_GROUP = 'Grupo_LDL0004_ResultLiqd'
PATH_R1 = 'DOC/SISMSG/LDL0004R1'
PATH_R2 = 'DOC/SISMSG/LDL0004R2'
PATH_R2_GROUP = 'Grupo_LDL0004R2_ResultLiqd'
XML_NAMESPACE = 'http://www.bcb.gov.br/LDL/LDL0004.xsd'


class NetResult(BaseSubMessage):
    cnpj: Annotated[Cnpj, XmlPath(f'{PATH_GROUP}/CNPJNLiqdant/text()')]
    participant_identifier: Annotated[ParticipantIdentifier | None, XmlPath(f'{PATH_GROUP}/IdentdPartCamr/text()')] = (
        None
    )
    amount: Annotated[Decimal, XmlPath(f'{PATH_GROUP}/VlrResultLiqdNLiqdant/text()')]


class LDL0004(BaseMessage):
    XML_NAMESPACE: ClassVar[str | None] = XML_NAMESPACE

    message_code: Annotated[Literal['LDL0004'], XmlPath(f'{PATH}/CodMsg/text()')] = 'LDL0004'
    institution_control_number: Annotated[InstitutionControlNumber, XmlPath(f'{PATH}/NumCtrlIF/text()')]
    institution_ispb: Annotated[Ispb, XmlPath(f'{PATH}/ISPBIF/text()')]
    original_ldl_control_number: Annotated[LdlControlNumber, XmlPath(f'{PATH}/NumCtrlLDLOr/text()')]
    ldl_ispb: Annotated[Ispb | None, XmlPath(f'{PATH}/ISPBLDL/text()')] = None
    amount: Annotated[Decimal, XmlPath(f'{PATH}/VlrLanc/text()')]
    net_result_group: Annotated[list[NetResult], XmlPath(f'{PATH}')] = Field(default_factory=list)
    settlement_date: Annotated[date, XmlPath(f'{PATH}/DtMovto/text()')]


class LDL0004R1(BaseMessage):
    XML_NAMESPACE: ClassVar[str | None] = XML_NAMESPACE

    message_code: Annotated[Literal['LDL0004R1'], XmlPath(f'{PATH_R1}/CodMsg/text()')] = 'LDL0004R1'
    institution_control_number: Annotated[InstitutionControlNumber, XmlPath(f'{PATH_R1}/NumCtrlIF/text()')]
    institution_ispb: Annotated[Ispb, XmlPath(f'{PATH_R1}/ISPBIF/text()')]
    str_control_number: Annotated[InstitutionControlNumber, XmlPath(f'{PATH_R1}/NumCtrlSTR/text()')]
    ldl_settlement_status: Annotated[LdlSettlementStatus, XmlPath(f'{PATH_R1}/SitLancLDL/text()')]
    settlement_timestamp: Annotated[datetime, XmlPath(f'{PATH_R1}/DtHrSit/text()')]
    settlement_date: Annotated[date, XmlPath(f'{PATH_R1}/DtMovto/text()')]


class NetResultR2(BaseSubMessage):
    cnpj: Annotated[Cnpj, XmlPath(f'{PATH_R2_GROUP}/CNPJNLiqdant/text()')]
    participant_identifier: Annotated[
        ParticipantIdentifier | None, XmlPath(f'{PATH_R2_GROUP}/IdentdPartCamr/text()')
    ] = None
    amount: Annotated[Decimal, XmlPath(f'{PATH_R2_GROUP}/VlrResultLiqdNLiqdant/text()')]


class LDL0004R2(BaseMessage):
    XML_NAMESPACE: ClassVar[str | None] = XML_NAMESPACE

    message_code: Annotated[Literal['LDL0004R2'], XmlPath(f'{PATH_R2}/CodMsg/text()')] = 'LDL0004R2'
    original_ldl_control_number: Annotated[LdlControlNumber, XmlPath(f'{PATH_R2}/NumCtrlLDLOr/text()')]
    institution_ispb: Annotated[Ispb, XmlPath(f'{PATH_R2}/ISPBIF/text()')]
    str_control_number: Annotated[StrControlNumber, XmlPath(f'{PATH_R2}/NumCtrlSTR/text()')]
    vendor_timestamp: Annotated[datetime, XmlPath(f'{PATH_R2}/DtHrBC/text()')]
    ldl_ispb: Annotated[Ispb, XmlPath(f'{PATH_R2}/ISPBLDL/text()')]
    amount: Annotated[Decimal, XmlPath(f'{PATH_R2}/VlrLanc/text()')]
    net_result_group: Annotated[list[NetResultR2], XmlPath(f'{PATH_R2}')] = Field(default_factory=list)
    settlement_date: Annotated[date, XmlPath(f'{PATH_R2}/DtMovto/text()')]
