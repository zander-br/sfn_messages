from datetime import date, datetime
from decimal import Decimal
from typing import Annotated, ClassVar, Literal

from pydantic import Field

from sfn_messages.core.models import BaseMessage, BaseSubMessage, XmlPath
from sfn_messages.core.types import (
    CreditDebitType,
    ErrorCode,
    InstitutionControlNumber,
    Ispb,
    MessageCode,
    StrControlNumber,
)

from .types import SmeControlNumber

PATH = 'DOC/SISMSG/SME0003'
PATH_R1 = 'DOC/SISMSG/SME0003R1'
PATH_R1_GROUP = 'Grupo_SME0003R1_Lanc'
PATH_E = 'DOC/SISMSG/SME0003E'
XML_NAMESPACE = 'http://www.bcb.gov.br/SME/SME0003.xsd'
XML_NAMESPACE_ERROR = 'http://www.bcb.gov.br/SME/SME0003E.xsd'


class SME0003(BaseMessage):
    XML_NAMESPACE: ClassVar[str | None] = XML_NAMESPACE

    message_code: Annotated[Literal['SME0003'], XmlPath(f'{PATH}/CodMsg/text()')] = 'SME0003'
    ieme_control_number: Annotated[InstitutionControlNumber, XmlPath(f'{PATH}/NumCtrlIEME/text()')]
    ieme_ispb: Annotated[Ispb, XmlPath(f'{PATH}/ISPBIEME/text()')]
    settlement_date: Annotated[date, XmlPath(f'{PATH}/DtMovto/text()')]


class LaunchGroup(BaseSubMessage):
    XML_NAMESPACE: ClassVar[str | None] = XML_NAMESPACE

    original_message_code: Annotated[MessageCode, XmlPath(f'{PATH_R1_GROUP}/CodMsgOr/text()')]
    ieme_control_number: Annotated[
        InstitutionControlNumber | None, XmlPath(f'{PATH_R1_GROUP}/NumCtrlIEMEOr/text()')
    ] = None
    counterparty_ispb: Annotated[Ispb | None, XmlPath(f'{PATH_R1_GROUP}/ISPBCtrapart/text()')] = None
    original_str_control_number: Annotated[StrControlNumber, XmlPath(f'{PATH_R1_GROUP}/NumCtrlSTROr/text()')]
    original_sme_control_number: Annotated[SmeControlNumber, XmlPath(f'{PATH_R1_GROUP}/NumCtrlSMEOr/text()')]
    settlement_timestamp: Annotated[datetime, XmlPath(f'{PATH_R1_GROUP}/DtHrSit/text()')]
    credit_debit_type: Annotated[CreditDebitType, XmlPath(f'{PATH_R1_GROUP}/TpDeb_Cred/text()')]
    amount: Annotated[Decimal, XmlPath(f'{PATH_R1_GROUP}/VlrLanc/text()')]


class SME0003R1(BaseMessage):
    XML_NAMESPACE: ClassVar[str | None] = XML_NAMESPACE

    message_code: Annotated[Literal['SME0003R1'], XmlPath(f'{PATH_R1}/CodMsg/text()')] = 'SME0003R1'
    ieme_control_number: Annotated[InstitutionControlNumber, XmlPath(f'{PATH_R1}/NumCtrlIEME/text()')]
    ieme_ispb: Annotated[Ispb, XmlPath(f'{PATH_R1}/ISPBIEME/text()')]
    initial_amount: Annotated[Decimal, XmlPath(f'{PATH_R1}/SldInial/text()')]
    launch_group: Annotated[list[LaunchGroup], XmlPath(f'{PATH_R1}')] = Field(default_factory=list)
    final_amount: Annotated[Decimal, XmlPath(f'{PATH_R1}/SldFinl/text()')]
    vendor_timestamp: Annotated[datetime, XmlPath(f'{PATH_R1}/DtHrBC/text()')]
    settlement_date: Annotated[date, XmlPath(f'{PATH_R1}/DtMovto/text()')]


class SME0003E(BaseMessage):
    XML_NAMESPACE: ClassVar[str | None] = XML_NAMESPACE_ERROR

    message_code: Annotated[Literal['SME0003'], XmlPath(f'{PATH_E}/CodMsg/text()')] = 'SME0003'
    ieme_control_number: Annotated[InstitutionControlNumber, XmlPath(f'{PATH_E}/NumCtrlIEME/text()')]
    ieme_ispb: Annotated[Ispb, XmlPath(f'{PATH_E}/ISPBIEME/text()')]
    settlement_date: Annotated[date, XmlPath(f'{PATH_E}/DtMovto/text()')]

    general_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH_E}/@CodErro')] = None
    ieme_control_number_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH_E}/NumCtrlIEME/@CodErro')] = None
    ieme_ispb_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH_E}/ISPBIEME/@CodErro')] = None
    settlement_date_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH_E}/DtMovto/@CodErro')] = None
