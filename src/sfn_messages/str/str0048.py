from datetime import date, datetime, time
from decimal import Decimal
from typing import Annotated, ClassVar, Literal

from sfn_messages.core.models import BaseMessage, XmlPath
from sfn_messages.core.types import (
    Description,
    InstitutionControlNumber,
    Ispb,
    Priority,
    StrControlNumber,
    StrSettlementStatus,
)

from .types import PortabilityReturnReason

PATH = 'DOC/SISMSG/STR0008'
PATH_R1 = 'DOC/SISMSG/STR0008R1'
PATH_R2 = 'DOC/SISMSG/STR0008R2'
XML_NAMESPACE = 'http://www.bcb.gov.br/SPB/STR0048.xsd'


class STR0048(BaseMessage):
    XML_NAMESPACE: ClassVar[str | None] = XML_NAMESPACE

    message_code: Annotated[Literal['STR0048'], XmlPath(f'{PATH}/CodMsg/text()')] = 'STR0048'
    institution_control_number: Annotated[InstitutionControlNumber, XmlPath(f'{PATH}/NumCtrlIF/text()')]
    debtor_institution_ispb: Annotated[Ispb, XmlPath(f'{PATH}/ISPBIFDebtd/text()')]
    creditor_institution_ispb: Annotated[Ispb, XmlPath(f'{PATH}/ISPBIFCredtd/text()')]
    amount: Annotated[Decimal, XmlPath(f'{PATH}/VlrLanc/text()')]
    portability_return_reason: Annotated[PortabilityReturnReason, XmlPath(f'{PATH}/CodDevPortdd/text()')]
    original_str_control_number: Annotated[StrControlNumber, XmlPath(f'{PATH}/NumCtrlSTROr/text()')]
    provider_ispb: Annotated[Ispb, XmlPath(f'{PATH}/ISPBPrestd/text()')]
    description: Annotated[Description | None, XmlPath(f'{PATH}/Hist/text()')] = None
    scheduled_date: Annotated[date | None, XmlPath(f'{PATH}/DtAgendt/text()')] = None
    scheduled_time: Annotated[time | None, XmlPath(f'{PATH}/HrAgendt/text()')] = None
    priority: Annotated[Priority | None, XmlPath(f'{PATH}/NivelPref/text()')] = None
    settlement_date: Annotated[date, XmlPath(f'{PATH}/DtMovto/text()')]


class STR0048R1(BaseMessage):
    XML_NAMESPACE: ClassVar[str | None] = XML_NAMESPACE

    message_code: Annotated[Literal['STR0048R1'], XmlPath(f'{PATH_R1}/CodMsg/text()')] = 'STR0048R1'
    institution_control_number: Annotated[InstitutionControlNumber, XmlPath(f'{PATH_R1}/NumCtrlIF/text()')]
    debtor_institution_ispb: Annotated[Ispb, XmlPath(f'{PATH_R1}/ISPBIFDebtd/text()')]
    str_control_number: Annotated[StrControlNumber, XmlPath(f'{PATH_R1}/NumCtrlSTR/text()')]
    str_settlement_status: Annotated[StrSettlementStatus, XmlPath(f'{PATH_R1}/SitLancSTR/text()')]
    settlement_timestamp: Annotated[datetime, XmlPath(f'{PATH_R1}/DtHrSit/text()')]
    settlement_date: Annotated[date, XmlPath(f'{PATH_R1}/DtMovto/text()')]


class STR0048R2(BaseMessage):
    XML_NAMESPACE: ClassVar[str | None] = XML_NAMESPACE

    message_code: Annotated[Literal['STR0048R2'], XmlPath(f'{PATH_R2}/CodMsg/text()')] = 'STR0048R2'
    str_control_number: Annotated[StrControlNumber, XmlPath(f'{PATH_R2}/NumCtrlSTR/text()')]
    vendor_timestamp: Annotated[datetime, XmlPath(f'{PATH_R2}/DtHrBC/text()')]
    debtor_institution_ispb: Annotated[Ispb, XmlPath(f'{PATH_R2}/ISPBIFDebtd/text()')]
    creditor_institution_ispb: Annotated[Ispb, XmlPath(f'{PATH_R2}/ISPBIFCredtd/text()')]
    amount: Annotated[Decimal, XmlPath(f'{PATH_R2}/VlrLanc/text()')]
    portability_return_reason: Annotated[PortabilityReturnReason, XmlPath(f'{PATH_R2}/CodDevPortdd/text()')]
    original_str_control_number: Annotated[StrControlNumber, XmlPath(f'{PATH_R2}/NumCtrlSTROr/text()')]
    provider_ispb: Annotated[Ispb, XmlPath(f'{PATH_R2}/ISPBPrestd/text()')]
    description: Annotated[Description | None, XmlPath(f'{PATH_R2}/Hist/text()')] = None
    settlement_date: Annotated[date, XmlPath(f'{PATH_R2}/DtMovto/text()')]
