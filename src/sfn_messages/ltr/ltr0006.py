from datetime import date, datetime
from decimal import Decimal
from typing import Annotated, ClassVar, Literal

from sfn_messages.core.models import BaseMessage, XmlPath
from sfn_messages.core.types import Description, InstitutionControlNumber, Ispb, StrControlNumber, StrSettlementStatus

PATH = 'DOC/SISMSG/LTR0006'
PATH_R1 = 'DOC/SISMSG/LTR0006R1'
PATH_R2 = 'DOC/SISMSG/LTR0006R2'
XML_NAMESPACE = 'http://www.bcb.gov.br/LTR/LTR0006.xsd'


class LTR0006(BaseMessage):
    XML_NAMESPACE: ClassVar[str | None] = XML_NAMESPACE

    message_code: Annotated[Literal['LTR0006'], XmlPath(f'{PATH}/CodMsg/text()')] = 'LTR0006'
    institution_or_ltr_control_number: Annotated[InstitutionControlNumber, XmlPath(f'{PATH}/NumCtrlIF_LTR/text()')]
    debtor_institution_or_ltr_ispb: Annotated[Ispb, XmlPath(f'{PATH}/ISPBIF_LTRDebtd/text()')]
    creditor_institution_or_ltr_ispb: Annotated[Ispb, XmlPath(f'{PATH}/ISPBIF_LTRCredtd/text()')]
    original_ltr_control_number: Annotated[InstitutionControlNumber, XmlPath(f'{PATH}/NumCtrlLTROr/text()')]
    amount: Annotated[Decimal, XmlPath(f'{PATH}/VlrLanc/text()')]
    description: Annotated[Description | None, XmlPath(f'{PATH}/Hist/text()')] = None
    settlement_date: Annotated[date, XmlPath(f'{PATH}/DtMovto/text()')]


class LTR0006R1(BaseMessage):
    XML_NAMESPACE: ClassVar[str | None] = XML_NAMESPACE

    message_code: Annotated[Literal['LTR0006R1'], XmlPath(f'{PATH_R1}/CodMsg/text()')] = 'LTR0006R1'
    institution_or_ltr_control_number: Annotated[InstitutionControlNumber, XmlPath(f'{PATH_R1}/NumCtrlIF_LTR/text()')]
    debtor_institution_or_ltr_ispb: Annotated[Ispb, XmlPath(f'{PATH_R1}/ISPBIF_LTRDebtd/text()')]
    str_control_number: Annotated[StrControlNumber, XmlPath(f'{PATH_R1}/NumCtrlSTR/text()')]
    str_settlement_status: Annotated[StrSettlementStatus, XmlPath(f'{PATH_R1}/SitLancSTR/text()')]
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
