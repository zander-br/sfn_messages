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
    PaymentNumber,
    PaymentType,
    StrControlNumber,
)

PATH = 'DOC/SISMSG/LDL0008'
PATH_GROUP = 'Grupo_LDL0008_EvtEms'
PATH_R1 = 'DOC/SISMSG/LDL0008R1'
PATH_R2 = 'DOC/SISMSG/LDL0008R2'
PATH_GROUP_R2 = 'Grupo_LDL0008R2_EvtEms'
XML_NAMESPACE = 'http://www.bcb.gov.br/LDL/LDL0008.xsd'


class EmissionEventGroup(BaseSubMessage):
    cnpj: Annotated[Cnpj, XmlPath(f'{PATH_GROUP}/CNPJNLiqdant/text()')]
    amount: Annotated[Decimal, XmlPath(f'{PATH_GROUP}/VlrNLiqdant/text()')]
    payment_type_ldl: Annotated[PaymentType | None, XmlPath(f'{PATH_GROUP}/TpPgtoLDL/text()')] = None
    payment_number: Annotated[PaymentNumber | None, XmlPath(f'{PATH_GROUP}/NumPgtoLDL/text()')] = None
    participant_identifier: Annotated[ParticipantIdentifier | None, XmlPath(f'{PATH_GROUP}/IdentdPartCamr/text()')] = (
        None
    )


class LDL0008(BaseMessage):
    XML_NAMESPACE: ClassVar[str | None] = XML_NAMESPACE

    message_code: Annotated[Literal['LDL0008'], XmlPath(f'{PATH}/CodMsg/text()')] = 'LDL0008'
    institution_control_number: Annotated[InstitutionControlNumber, XmlPath(f'{PATH}/NumCtrlIF/text()')]
    institution_ispb: Annotated[Ispb, XmlPath(f'{PATH}/ISPBIF/text()')]
    original_ldl_control_number: Annotated[LdlControlNumber, XmlPath(f'{PATH}/NumCtrlLDLOr/text()')]
    ldl_ispb: Annotated[Ispb, XmlPath(f'{PATH}/ISPBLDL/text()')]
    amount: Annotated[Decimal, XmlPath(f'{PATH}/VlrLanc/text()')]
    emission_event_group: Annotated[list[EmissionEventGroup], XmlPath(f'{PATH}')] = Field(default_factory=list)
    settlement_date: Annotated[date, XmlPath(f'{PATH}/DtMovto/text()')]


class LDL0008R1(BaseMessage):
    XML_NAMESPACE: ClassVar[str | None] = XML_NAMESPACE

    message_code: Annotated[Literal['LDL0008R1'], XmlPath(f'{PATH_R1}/CodMsg/text()')] = 'LDL0008R1'
    institution_control_number: Annotated[InstitutionControlNumber, XmlPath(f'{PATH_R1}/NumCtrlIF/text()')]
    institution_ispb: Annotated[Ispb, XmlPath(f'{PATH_R1}/ISPBIF/text()')]
    str_control_number: Annotated[StrControlNumber, XmlPath(f'{PATH_R1}/NumCtrlSTR/text()')]
    ldl_settlement_status: Annotated[LdlSettlementStatus, XmlPath(f'{PATH_R1}/SitLancLDL/text()')]
    settlement_timestamp: Annotated[datetime, XmlPath(f'{PATH_R1}/DtHrSit/text()')]
    settlement_date: Annotated[date, XmlPath(f'{PATH_R1}/DtMovto/text()')]


class EmissionEventGroupR2(BaseSubMessage):
    cnpj: Annotated[Cnpj, XmlPath(f'{PATH_GROUP_R2}/CNPJNLiqdant/text()')]
    amount: Annotated[Decimal, XmlPath(f'{PATH_GROUP_R2}/VlrNLiqdant/text()')]
    payment_type_ldl: Annotated[PaymentType | None, XmlPath(f'{PATH_GROUP_R2}/TpPgtoLDL/text()')] = None
    payment_number: Annotated[PaymentNumber | None, XmlPath(f'{PATH_GROUP_R2}/NumPgtoLDL/text()')] = None
    participant_identifier: Annotated[
        ParticipantIdentifier | None, XmlPath(f'{PATH_GROUP_R2}/IdentdPartCamr/text()')
    ] = None


class LDL0008R2(BaseMessage):
    XML_NAMESPACE: ClassVar[str | None] = XML_NAMESPACE

    message_code: Annotated[Literal['LDL0008R2'], XmlPath(f'{PATH_R2}/CodMsg/text()')] = 'LDL0008R2'
    str_control_number: Annotated[StrControlNumber, XmlPath(f'{PATH_R2}/NumCtrlSTR/text()')]
    original_ldl_control_number: Annotated[LdlControlNumber, XmlPath(f'{PATH_R2}/NumCtrlLDLOr/text()')]
    vendor_timestamp: Annotated[datetime, XmlPath(f'{PATH_R2}/DtHrBC/text()')]
    institution_ispb: Annotated[Ispb, XmlPath(f'{PATH_R2}/ISPBIF/text()')]
    ldl_ispb: Annotated[Ispb, XmlPath(f'{PATH_R2}/ISPBLDL/text()')]
    amount: Annotated[Decimal, XmlPath(f'{PATH_R2}/VlrLanc/text()')]
    emission_event_group: Annotated[list[EmissionEventGroupR2], XmlPath(f'{PATH_R2}')] = Field(default_factory=list)
    settlement_date: Annotated[date, XmlPath(f'{PATH_R2}/DtMovto/text()')]
