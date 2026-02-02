from datetime import date, datetime
from decimal import Decimal
from typing import Annotated, ClassVar, Literal

from pydantic import Field

from sfn_messages.core.models import BaseMessage, BaseSubMessage, XmlPath
from sfn_messages.core.types import (
    CreditDebitType,
    ErrorCode,
    FileIdentifier,
    FileSizeInBytes,
    InstitutionControlNumber,
    Ispb,
    MessageCode,
    ReturnType,
    StrControlNumber,
)

PATH = 'DOC/SISMSG/STR0014'
PATH_R1 = 'DOC/SISMSG/STR0014R1'
PATH_R1_GROUP = 'Grupo_STR0014R1_Lanc'
PATH_E = 'DOC/SISMSG/STR0014'
XML_NAMESPACE = 'http://www.bcb.gov.br/SPB/STR0014.xsd'
XML_NAMESPACE_ERROR = 'http://www.bcb.gov.br/SPB/STR0014E.xsd'


class STR0014(BaseMessage):
    XML_NAMESPACE: ClassVar[str | None] = XML_NAMESPACE

    message_code: Annotated[Literal['STR0014'], XmlPath(f'{PATH}/CodMsg/text()')] = 'STR0014'
    institution_control_number: Annotated[InstitutionControlNumber, XmlPath(f'{PATH}/NumCtrlIF_LDL/text()')]
    institution_ispb: Annotated[Ispb, XmlPath(f'{PATH}/ISPBIF_LDL/text()')]
    return_type: Annotated[ReturnType, XmlPath(f'{PATH}/TpRet/text()')]
    start_timestamp: Annotated[datetime | None, XmlPath(f'{PATH}/DtHrIni/text()')] = None
    finish_timestamp: Annotated[datetime | None, XmlPath(f'{PATH}/DtHrFim/text()')] = None
    settlement_date: Annotated[date, XmlPath(f'{PATH}/DtMovto/text()')]


class LaunchGroup(BaseSubMessage):
    XML_NAMESPACE: ClassVar[str | None] = XML_NAMESPACE

    original_message_code: Annotated[MessageCode | None, XmlPath(f'{PATH_R1_GROUP}/CodMsgOr/text()')] = None
    original_if_or_ldl_control_number: Annotated[
        InstitutionControlNumber | None, XmlPath(f'{PATH_R1_GROUP}/NumCtrlIF_LDLOr/text()')
    ] = None
    counterparty_ispb: Annotated[Ispb | None, XmlPath(f'{PATH_R1_GROUP}/ISPBCtrapart/text()')] = None
    original_str_control_number: Annotated[
        StrControlNumber | None, XmlPath(f'{PATH_R1_GROUP}/NumCtrlSTROr/text()')
    ] = None
    settlement_timestamp: Annotated[datetime, XmlPath(f'{PATH_R1_GROUP}/DtHrSit/text()')]
    credit_debit_type: Annotated[CreditDebitType, XmlPath(f'{PATH_R1_GROUP}/TpDeb_Cred/text()')]
    amount: Annotated[Decimal, XmlPath(f'{PATH_R1_GROUP}/VlrLanc/text()')]


class STR0014R1(BaseMessage):
    XML_NAMESPACE: ClassVar[str | None] = XML_NAMESPACE

    message_code: Annotated[Literal['STR0014R1'], XmlPath(f'{PATH_R1}/CodMsg/text()')] = 'STR0014R1'
    institution_control_number: Annotated[InstitutionControlNumber, XmlPath(f'{PATH_R1}/NumCtrlIF_LDL/text()')]
    institution_ispb: Annotated[Ispb, XmlPath(f'{PATH_R1}/ISPBIF_LDL/text()')]
    start_timestamp: Annotated[datetime | None, XmlPath(f'{PATH_R1}/DtHrIni/text()')] = None
    initial_amount: Annotated[Decimal, XmlPath(f'{PATH_R1}/SldInial/text()')]
    launch_group: Annotated[list[LaunchGroup], XmlPath(f'{PATH_R1}')] = Field(default_factory=list)
    final_amount: Annotated[Decimal, XmlPath(f'{PATH_R1}/SldFinl/text()')]
    vendor_timestamp: Annotated[datetime, XmlPath(f'{PATH_R1}/DtHrBC/text()')]
    settlement_date: Annotated[date, XmlPath(f'{PATH_R1}/DtMovto/text()')]
    file_size: Annotated[FileSizeInBytes | None, XmlPath(f'{PATH_R1}/TamArq/text()')] = None
    file_identifier: Annotated[FileIdentifier | None, XmlPath(f'{PATH_R1}/IdentdArq/text()')] = None


class STR0014E(BaseMessage):
    XML_NAMESPACE: ClassVar[str | None] = XML_NAMESPACE_ERROR

    message_code: Annotated[Literal['STR0014E'], XmlPath(f'{PATH_E}/CodMsg/text()')] = 'STR0014E'
    institution_control_number: Annotated[
        InstitutionControlNumber | None, XmlPath(f'{PATH_E}/NumCtrlIF_LDL/text()')
    ] = None
    institution_ispb: Annotated[Ispb | None, XmlPath(f'{PATH_E}/ISPBIF_LDL/text()')] = None
    return_type: Annotated[ReturnType | None, XmlPath(f'{PATH_E}/TpRet/text()')] = None
    start_timestamp: Annotated[datetime | None, XmlPath(f'{PATH_E}/DtHrIni/text()')] = None
    finish_timestamp: Annotated[datetime | None, XmlPath(f'{PATH_E}/DtHrFim/text()')] = None
    settlement_date: Annotated[date | None, XmlPath(f'{PATH_E}/DtMovto/text()')] = None

    general_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH_E}/@CodErro')] = None
    institution_control_number_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH_E}/NumCtrlIF_LDL/@CodErro')] = (
        None
    )
    institution_ispb_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH_E}/ISPBIF_LDL/@CodErro')] = None
    return_type_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH_E}/TpRet/@CodErro')] = None
    start_timestamp_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH_E}/DtHrIni/@CodErro')] = None
    finish_timestamp_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH_E}/DtHrFim/@CodErro')] = None
    settlement_date_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH_E}/DtMovto/@CodErro')] = None
