from datetime import date, datetime
from decimal import Decimal
from typing import Annotated, ClassVar, Literal

from sfn_messages.core.models import BaseMessage, XmlPath
from sfn_messages.core.types import (
    AssetDescription,
    AssetType,
    Description,
    InstitutionControlNumber,
    Ispb,
    StrControlNumber,
    StrSettlementStatus,
)

PATH = 'DOC/SISMSG/LTR0004'
PATH_R1 = 'DOC/SISMSG/LTR0004R1'
PATH_R2 = 'DOC/SISMSG/LTR0004R2'
XML_NAMESPACE = 'http://www.bcb.gov.br/LTR/LTR0004.xsd'


class LTR0004(BaseMessage):
    XML_NAMESPACE: ClassVar[str | None] = XML_NAMESPACE

    message_code: Annotated[Literal['LTR0004'], XmlPath(f'{PATH}/CodMsg/text()')] = 'LTR0004'
    institution_control_number: Annotated[InstitutionControlNumber, XmlPath(f'{PATH}/NumCtrlIF/text()')]
    institution_ispb: Annotated[Ispb, XmlPath(f'{PATH}/ISPBIF/text()')]
    ltr_ispb: Annotated[Ispb, XmlPath(f'{PATH}/ISPBLTR/text()')]
    original_ltr_control_number: Annotated[InstitutionControlNumber, XmlPath(f'{PATH}/NumCtrlLTROr/text()')]
    amount: Annotated[Decimal, XmlPath(f'{PATH}/VlrLanc/text()')]
    sub_asset_type: Annotated[AssetType, XmlPath(f'{PATH}/SubTpAtv/text()')]
    asset_description: Annotated[AssetDescription | None, XmlPath(f'{PATH}/DescAtv/text()')] = None
    description: Annotated[Description | None, XmlPath(f'{PATH}/Hist/text()')] = None
    settlement_date: Annotated[date, XmlPath(f'{PATH}/DtMovto/text()')]


class LTR0004R1(BaseMessage):
    XML_NAMESPACE: ClassVar[str | None] = XML_NAMESPACE

    message_code: Annotated[Literal['LTR0004R1'], XmlPath(f'{PATH_R1}/CodMsg/text()')] = 'LTR0004R1'
    institution_control_number: Annotated[InstitutionControlNumber, XmlPath(f'{PATH_R1}/NumCtrlIF/text()')]
    institution_ispb: Annotated[Ispb, XmlPath(f'{PATH_R1}/ISPBIF/text()')]
    str_control_number: Annotated[StrControlNumber, XmlPath(f'{PATH_R1}/NumCtrlSTR/text()')]
    str_settlement_status: Annotated[StrSettlementStatus, XmlPath(f'{PATH_R1}/SitLancSTR/text()')]
    settlement_timestamp: Annotated[datetime, XmlPath(f'{PATH_R1}/DtHrSit/text()')]
    settlement_date: Annotated[date, XmlPath(f'{PATH_R1}/DtMovto/text()')]


class LTR0004R2(BaseMessage):
    XML_NAMESPACE: ClassVar[str | None] = XML_NAMESPACE

    message_code: Annotated[Literal['LTR0004R2'], XmlPath(f'{PATH_R2}/CodMsg/text()')] = 'LTR0004R2'
    str_control_number: Annotated[StrControlNumber, XmlPath(f'{PATH_R2}/NumCtrlSTR/text()')]
    institution_ispb: Annotated[Ispb, XmlPath(f'{PATH_R2}/ISPBIF/text()')]
    original_ltr_control_number: Annotated[InstitutionControlNumber, XmlPath(f'{PATH_R2}/NumCtrlLTROr/text()')]
    ltr_ispb: Annotated[Ispb, XmlPath(f'{PATH_R2}/ISPBLTR/text()')]
    amount: Annotated[Decimal, XmlPath(f'{PATH_R2}/VlrLanc/text()')]
    sub_asset_type: Annotated[AssetType, XmlPath(f'{PATH_R2}/SubTpAtv/text()')]
    asset_description: Annotated[AssetDescription | None, XmlPath(f'{PATH_R2}/DescAtv/text()')] = None
    description: Annotated[Description | None, XmlPath(f'{PATH_R2}/Hist/text()')] = None
    vendor_timestamp: Annotated[datetime, XmlPath(f'{PATH_R2}/DtHrBC/text()')]
    settlement_date: Annotated[date, XmlPath(f'{PATH_R2}/DtMovto/text()')]
