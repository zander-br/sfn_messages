from datetime import date, datetime
from decimal import Decimal
from typing import Annotated, ClassVar, Literal

from sfn_messages.core.models import BaseMessage, XmlPath
from sfn_messages.core.types import InstitutionControlNumber, Ispb, StrControlNumber, StrSettlementStatus

PATH = 'DOC/SISMSG/SME0001'
PATH_R1 = 'DOC/SISMSG/SME0001R1'
PATH_R2 = 'DOC/SISMSG/SME0001R2'
XML_NAMESPACE = 'http://www.bcb.gov.br/SME/SME0001.xsd'


class SME0001(BaseMessage):
    XML_NAMESPACE: ClassVar[str | None] = XML_NAMESPACE

    message_code: Annotated[Literal['SME0001'], XmlPath(f'{PATH}/CodMsg/text()')] = 'SME0001'
    institution_control_number: Annotated[InstitutionControlNumber, XmlPath(f'{PATH}/NumCtrlIF/text()')]
    institution_ispb: Annotated[Ispb, XmlPath(f'{PATH}/ISPBIF/text()')]
    ieme_ispb: Annotated[Ispb | None, XmlPath(f'{PATH}/ISPBIEME/text()')] = None
    amount: Annotated[Decimal, XmlPath(f'{PATH}/VlrLanc/text()')]
    settlement_date: Annotated[date, XmlPath(f'{PATH}/DtMovto/text()')]


class SME0001R1(BaseMessage):
    XML_NAMESPACE: ClassVar[str | None] = XML_NAMESPACE

    message_code: Annotated[Literal['SME0001R1'], XmlPath(f'{PATH_R1}/CodMsg/text()')] = 'SME0001R1'
    institution_control_number: Annotated[InstitutionControlNumber, XmlPath(f'{PATH_R1}/NumCtrlIF/text()')]
    institution_ispb: Annotated[Ispb, XmlPath(f'{PATH_R1}/ISPBIF/text()')]
    str_control_number: Annotated[StrControlNumber, XmlPath(f'{PATH_R1}/NumCtrlSTR/text()')]
    str_settlement_status: Annotated[StrSettlementStatus, XmlPath(f'{PATH_R1}/SitLancSTR/text()')]
    settlement_date: Annotated[date, XmlPath(f'{PATH_R1}/DtMovto/text()')]


class SME0001R2(BaseMessage):
    XML_NAMESPACE: ClassVar[str | None] = XML_NAMESPACE

    message_code: Annotated[Literal['SME0001R2'], XmlPath(f'{PATH_R2}/CodMsg/text()')] = 'SME0001R2'
    str_control_number: Annotated[StrControlNumber, XmlPath(f'{PATH_R2}/NumCtrlSTR/text()')]
    vendor_timestamp: Annotated[datetime, XmlPath(f'{PATH_R2}/DtHrBC/text()')]
    institution_ispb: Annotated[Ispb, XmlPath(f'{PATH_R2}/ISPBIF/text()')]
    ieme_ispb: Annotated[Ispb, XmlPath(f'{PATH_R2}/ISPBIEME/text()')]
    amount: Annotated[Decimal, XmlPath(f'{PATH_R2}/VlrLanc/text()')]
    settlement_date: Annotated[date, XmlPath(f'{PATH_R2}/DtMovto/text()')]
