from datetime import date, datetime
from decimal import Decimal
from typing import Annotated, ClassVar, Literal

from sfn_messages.core.models import BaseMessage, XmlPath
from sfn_messages.core.types import (
    Description,
    ErrorCode,
    InstitutionControlNumber,
    Ispb,
    StrControlNumber,
    StrSettlementStatus,
)

PATH = 'DOC/SISMSG/LTR0006'
PATH_R1 = 'DOC/SISMSG/LTR0006R1'
PATH_R2 = 'DOC/SISMSG/LTR0006R2'
PATH_E = 'DOC/SISMSG/LTR0006'
XML_NAMESPACE = 'http://www.bcb.gov.br/SPB/LTR0006.xsd'
XML_NAMESPACE_ERROR = 'http://www.bcb.gov.br/SPB/LTR0006E.xsd'


class LTR0006(BaseMessage):
    XML_NAMESPACE: ClassVar[str | None] = XML_NAMESPACE

    message_code: Annotated[Literal['LTR0006'], XmlPath(f'{PATH}/CodMsg/text()')] = 'LTR0006'
    institution_or_ltr_control_number: Annotated[InstitutionControlNumber, XmlPath(f'{PATH}/NumCtrlIF_LTR/text()')]
    debtor_institution_or_ltr_ispb: Annotated[Ispb, XmlPath(f'{PATH}/ISPBIF_LTRDebtd/text()')]
    creditor_institution_or_ltr_ispb: Annotated[Ispb, XmlPath(f'{PATH}/ISPBIF_LTRCredtd/text()')]
    original_str_control_number: Annotated[StrControlNumber, XmlPath(f'{PATH}/NumCtrlSTROr/text()')]
    amount: Annotated[Decimal, XmlPath(f'{PATH}/VlrLanc/text()')]
    description: Annotated[Description | None, XmlPath(f'{PATH}/Hist/text()')] = None
    settlement_date: Annotated[date, XmlPath(f'{PATH}/DtMovto/text()')]


class LTR0006R1(BaseMessage):
    XML_NAMESPACE: ClassVar[str | None] = XML_NAMESPACE

    message_code: Annotated[Literal['LTR0006R1'], XmlPath(f'{PATH_R1}/CodMsg/text()')] = 'LTR0006R1'
    institution_or_ltr_control_number: Annotated[InstitutionControlNumber, XmlPath(f'{PATH_R1}/NumCtrlIF_LTR/text()')]
    debtor_institution_or_ltr_ispb: Annotated[Ispb, XmlPath(f'{PATH_R1}/ISPBIF_LTRDebtd/text()')]
    str_control_number: Annotated[StrControlNumber, XmlPath(f'{PATH_R1}/NumCtrlSTR/text()')]
    str_settlement_status: Annotated[StrSettlementStatus | None, XmlPath(f'{PATH_R1}/SitLancSTR/text()')] = None
    settlement_timestamp: Annotated[datetime, XmlPath(f'{PATH_R1}/DtHrSit/text()')]
    settlement_date: Annotated[date, XmlPath(f'{PATH_R1}/DtMovto/text()')]


class LTR0006R2(BaseMessage):
    XML_NAMESPACE: ClassVar[str | None] = XML_NAMESPACE

    message_code: Annotated[Literal['LTR0006R2'], XmlPath(f'{PATH_R2}/CodMsg/text()')] = 'LTR0006R2'
    str_control_number: Annotated[StrControlNumber, XmlPath(f'{PATH_R2}/NumCtrlSTR/text()')]
    debtor_institution_or_ltr_ispb: Annotated[Ispb, XmlPath(f'{PATH_R2}/ISPBIF_LTRDebtd/text()')]
    creditor_institution_or_ltr_ispb: Annotated[Ispb, XmlPath(f'{PATH_R2}/ISPBIF_LTRCredtd/text()')]
    amount: Annotated[Decimal, XmlPath(f'{PATH_R2}/VlrLanc/text()')]
    original_str_control_number: Annotated[StrControlNumber, XmlPath(f'{PATH_R2}/NumCtrlSTROr/text()')]
    description: Annotated[Description | None, XmlPath(f'{PATH_R2}/Hist/text()')] = None
    vendor_timestamp: Annotated[datetime, XmlPath(f'{PATH_R2}/DtHrBC/text()')]
    settlement_date: Annotated[date, XmlPath(f'{PATH_R2}/DtMovto/text()')]


class LTR0006E(BaseMessage):
    XML_NAMESPACE: ClassVar[str | None] = XML_NAMESPACE_ERROR

    message_code: Annotated[Literal['LTR0006E'], XmlPath(f'{PATH_E}/CodMsg/text()')] = 'LTR0006E'
    institution_or_ltr_control_number: Annotated[
        InstitutionControlNumber | None, XmlPath(f'{PATH_E}/NumCtrlIF_LTR/text()')
    ] = None
    debtor_institution_or_ltr_ispb: Annotated[Ispb | None, XmlPath(f'{PATH_E}/ISPBIF_LTRDebtd/text()')] = None
    creditor_institution_or_ltr_ispb: Annotated[Ispb | None, XmlPath(f'{PATH_E}/ISPBIF_LTRCredtd/text()')] = None
    original_str_control_number: Annotated[StrControlNumber | None, XmlPath(f'{PATH}/NumCtrlSTROr/text()')] = None
    amount: Annotated[Decimal | None, XmlPath(f'{PATH_E}/VlrLanc/text()')] = None
    description: Annotated[Description | None, XmlPath(f'{PATH_E}/Hist/text()')] = None
    settlement_date: Annotated[date | None, XmlPath(f'{PATH_E}/DtMovto/text()')] = None

    general_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH_E}/@CodErro')] = None
    institution_or_ltr_control_number_error_code: Annotated[
        ErrorCode | None, XmlPath(f'{PATH_E}/NumCtrlIF_LTR/@CodErro')
    ] = None
    debtor_institution_or_ltr_ispb_error_code: Annotated[
        ErrorCode | None, XmlPath(f'{PATH_E}/ISPBIF_LTRDebtd/@CodErro')
    ] = None
    creditor_institution_or_ltr_ispb_error_code: Annotated[
        ErrorCode | None, XmlPath(f'{PATH_E}/ISPBIF_LTRCredtd/@CodErro')
    ] = None
    original_str_control_number_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH_E}/NumCtrlSTROr/@CodErro')] = (
        None
    )
    amount_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH_E}/VlrLanc/@CodErro')] = None
    description_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH_E}/Hist/@CodErro')] = None
    settlement_date_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH_E}/DtMovto/@CodErro')] = None
