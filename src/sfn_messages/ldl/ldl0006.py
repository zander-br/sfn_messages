from datetime import date, datetime
from decimal import Decimal
from typing import Annotated, ClassVar, Literal

from pydantic import Field

from sfn_messages.core.models import BaseMessage, BaseSubMessage, XmlPath
from sfn_messages.core.types import (
    Cnpj,
    Description,
    InstitutionControlNumber,
    Ispb,
    MovementType,
    ParticipantIdentifier,
    PaymentNumber,
    PaymentType,
    ProductCode,
    StrControlNumber,
    StrSettlementStatus,
)

PATH = 'DOC/SISMSG/LDL0006'
PATH_GROUP = 'Grupo_LDL0006_DevCred'
PATH_R1 = 'DOC/SISMSG/LDL0006R1'
PATH_R2 = 'DOC/SISMSG/LDL0006R2'
PATH_GROUP_R2 = 'Grupo_LDL0006R2_DevCred'
XML_NAMESPACE = 'http://www.bcb.gov.br/LDL/LDL0006.xsd'


class CreditRefundGroup(BaseSubMessage):
    cnpj: Annotated[Cnpj, XmlPath(f'{PATH_GROUP}/CNPJNLiqdant/text()')]
    participant_identifier: Annotated[ParticipantIdentifier | None, XmlPath(f'{PATH_GROUP}/IdentdPartCamr/text()')] = (
        None
    )
    amount: Annotated[Decimal, XmlPath(f'{PATH_GROUP}/VlrNLiqdant/text()')]
    payment_type_ldl: Annotated[PaymentType | None, XmlPath(f'{PATH_GROUP}/TpPgtoLDL/text()')] = None
    movement_type: Annotated[MovementType | None, XmlPath(f'{PATH_GROUP}/TpMovtc/text()')] = None
    payment_number: Annotated[PaymentNumber | None, XmlPath(f'{PATH_GROUP}/NumPgtoLDL/text()')] = None
    description: Annotated[Description | None, XmlPath(f'{PATH_GROUP}/Hist/text()')] = None


class LDL0006(BaseMessage):
    XML_NAMESPACE: ClassVar[str | None] = XML_NAMESPACE

    message_code: Annotated[Literal['LDL0006'], XmlPath(f'{PATH}/CodMsg/text()')] = 'LDL0006'
    institution_or_ldl_control_number: Annotated[InstitutionControlNumber, XmlPath(f'{PATH}/NumCtrlIF_LDL/text()')]
    debitor_institution_ispb: Annotated[Ispb, XmlPath(f'{PATH}/ISPBIF_LDLDebtd/text()')]
    creditor_institution_ispb: Annotated[Ispb, XmlPath(f'{PATH}/ISPBIF_LDLCredtd/text()')]
    product_code: Annotated[ProductCode | None, XmlPath(f'{PATH}/CodProdt/text()')] = None
    original_str_control_number: Annotated[StrControlNumber, XmlPath(f'{PATH}/NumCtrlSTROr/text()')]
    amount: Annotated[Decimal, XmlPath(f'{PATH}/VlrLanc/text()')]
    credit_refund_group: Annotated[list[CreditRefundGroup], XmlPath(f'{PATH}')] = Field(default_factory=list)
    settlement_date: Annotated[date, XmlPath(f'{PATH}/DtMovto/text()')]


class LDL0006R1(BaseMessage):
    XML_NAMESPACE: ClassVar[str | None] = XML_NAMESPACE

    message_code: Annotated[Literal['LDL0006R1'], XmlPath(f'{PATH_R1}/CodMsg/text()')] = 'LDL0006R1'
    institution_or_ldl_control_number: Annotated[InstitutionControlNumber, XmlPath(f'{PATH_R1}/NumCtrlIF_LDL/text()')]
    debitor_institution_ispb: Annotated[Ispb, XmlPath(f'{PATH_R1}/ISPBIF_LDLDebtd/text()')]
    str_control_number: Annotated[StrControlNumber, XmlPath(f'{PATH_R1}/NumCtrlSTR/text()')]
    str_settlement_status: Annotated[StrSettlementStatus, XmlPath(f'{PATH_R1}/SitLancSTR/text()')]
    settlement_timestamp: Annotated[datetime, XmlPath(f'{PATH_R1}/DtHrSit/text()')]
    settlement_date: Annotated[date, XmlPath(f'{PATH_R1}/DtMovto/text()')]


class CreditRefundGroupR2(BaseSubMessage):
    cnpj: Annotated[Cnpj, XmlPath(f'{PATH_GROUP_R2}/CNPJNLiqdant/text()')]
    participant_identifier: Annotated[
        ParticipantIdentifier | None, XmlPath(f'{PATH_GROUP_R2}/IdentdPartCamr/text()')
    ] = None
    amount: Annotated[Decimal, XmlPath(f'{PATH_GROUP_R2}/VlrNLiqdant/text()')]
    payment_type_ldl: Annotated[PaymentType | None, XmlPath(f'{PATH_GROUP_R2}/TpPgtoLDL/text()')] = None
    movement_type: Annotated[MovementType | None, XmlPath(f'{PATH_GROUP_R2}/TpMovtc/text()')] = None
    payment_number: Annotated[PaymentNumber | None, XmlPath(f'{PATH_GROUP_R2}/NumPgtoLDL/text()')] = None
    description: Annotated[Description | None, XmlPath(f'{PATH_GROUP_R2}/Hist/text()')] = None


class LDL0006R2(BaseMessage):
    XML_NAMESPACE: ClassVar[str | None] = XML_NAMESPACE

    message_code: Annotated[Literal['LDL0006R2'], XmlPath(f'{PATH_R2}/CodMsg/text()')] = 'LDL0006R2'
    str_control_number: Annotated[StrControlNumber, XmlPath(f'{PATH_R2}/NumCtrlSTR/text()')]
    vendor_timestamp: Annotated[datetime, XmlPath(f'{PATH_R2}/DtHrBC/text()')]
    debitor_institution_ispb: Annotated[Ispb, XmlPath(f'{PATH_R2}/ISPBIF_LDLDebtd/text()')]
    creditor_institution_ispb: Annotated[Ispb, XmlPath(f'{PATH_R2}/ISPBIF_LDLCredtd/text()')]
    product_code: Annotated[ProductCode | None, XmlPath(f'{PATH_R2}/CodProdt/text()')] = None
    amount: Annotated[Decimal, XmlPath(f'{PATH_R2}/VlrLanc/text()')]
    original_str_control_number: Annotated[StrControlNumber, XmlPath(f'{PATH_R2}/NumCtrlSTROr/text()')]
    credit_refund_group: Annotated[list[CreditRefundGroupR2], XmlPath(f'{PATH_R2}')] = Field(default_factory=list)
    settlement_date: Annotated[date, XmlPath(f'{PATH_R2}/DtMovto/text()')]
