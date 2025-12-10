from datetime import date, datetime
from decimal import Decimal
from typing import Annotated, ClassVar, Literal

from sfn_messages.core.models import BaseMessage, XmlPath
from sfn_messages.core.types import (
    InstitutionControlNumber,
    Ispb,
    LdlSettlementStatus,
    ProductCode,
    StrControlNumber,
)

PATH = 'DOC/SISMSG/LDL0022'
PATH_R1 = 'DOC/SISMSG/LDL0022R1'
PATH_R2 = 'DOC/SISMSG/LDL0022R2'
XML_NAMESPACE = 'http://www.bcb.gov.br/LDL/LDL0022.xsd'


class LDL0022(BaseMessage):
    XML_NAMESPACE: ClassVar[str | None] = XML_NAMESPACE

    message_code: Annotated[Literal['LDL0022'], XmlPath(f'{PATH}/CodMsg/text()')] = 'LDL0022'
    institution_control_number: Annotated[InstitutionControlNumber, XmlPath(f'{PATH}/NumCtrlIF/text()')]
    institution_ispb: Annotated[Ispb, XmlPath(f'{PATH}/ISPBIF/text()')]
    ldl_ispb: Annotated[Ispb, XmlPath(f'{PATH}/ISPBLDL/text()')]
    product_code: Annotated[ProductCode, XmlPath(f'{PATH}/CodProdt/text()')]
    amount: Annotated[Decimal, XmlPath(f'{PATH}/VlrLanc/text()')]
    settlement_date: Annotated[date, XmlPath(f'{PATH}/DtMovto/text()')]


class LDL0022R1(BaseMessage):
    XML_NAMESPACE: ClassVar[str | None] = XML_NAMESPACE

    message_code: Annotated[Literal['LDL0022R1'], XmlPath(f'{PATH_R1}/CodMsg/text()')] = 'LDL0022R1'
    institution_control_number: Annotated[InstitutionControlNumber, XmlPath(f'{PATH_R1}/NumCtrlIF/text()')]
    institution_ispb: Annotated[Ispb, XmlPath(f'{PATH_R1}/ISPBIF/text()')]
    str_control_number: Annotated[StrControlNumber, XmlPath(f'{PATH_R1}/NumCtrlSTR/text()')]
    ldl_settlement_status: Annotated[LdlSettlementStatus, XmlPath(f'{PATH_R1}/SitLancLDL/text()')]
    settlement_timestamp: Annotated[datetime, XmlPath(f'{PATH_R1}/DtHrSit/text()')]
    settlement_date: Annotated[date, XmlPath(f'{PATH_R1}/DtMovto/text()')]


class LDL0022R2(BaseMessage):
    XML_NAMESPACE: ClassVar[str | None] = XML_NAMESPACE

    message_code: Annotated[Literal['LDL0022R2'], XmlPath(f'{PATH_R2}/CodMsg/text()')] = 'LDL0022R2'
    str_control_number: Annotated[StrControlNumber, XmlPath(f'{PATH_R2}/NumCtrlSTR/text()')]
    vendor_timestamp: Annotated[datetime, XmlPath(f'{PATH_R2}/DtHrBC/text()')]
    institution_ispb: Annotated[Ispb, XmlPath(f'{PATH_R2}/ISPBIF/text()')]
    ldl_ispb: Annotated[Ispb, XmlPath(f'{PATH_R2}/ISPBLDL/text()')]
    product_code: Annotated[ProductCode, XmlPath(f'{PATH_R2}/CodProdt/text()')]
    amount: Annotated[Decimal, XmlPath(f'{PATH_R2}/VlrLanc/text()')]
    settlement_date: Annotated[date, XmlPath(f'{PATH_R2}/DtMovto/text()')]
