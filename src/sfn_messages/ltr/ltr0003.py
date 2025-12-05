from datetime import date, datetime
from decimal import Decimal
from typing import Annotated, ClassVar, Literal

from sfn_messages.core.models import BaseMessage, XmlPath
from sfn_messages.core.types import (
    AccountNumber,
    AssetDescription,
    AssetType,
    Branch,
    Description,
    InstitutionControlNumber,
    Ispb,
    Priority,
    StrControlNumber,
    StrSettlementStatus,
)

PATH = 'DOC/SISMSG/LTR0003'
PATH_R1 = 'DOC/SISMSG/LTR0003R1'
PATH_R2 = 'DOC/SISMSG/LTR0003R2'
PATH_R3 = 'DOC/SISMSG/LTR0003R3'
XML_NAMESPACE = 'http://www.bcb.gov.br/LTR/LTR0003.xsd'


class LTR0003(BaseMessage):
    XML_NAMESPACE: ClassVar[str | None] = XML_NAMESPACE

    message_code: Annotated[Literal['LTR0003'], XmlPath(f'{PATH}/CodMsg/text()')] = 'LTR0003'
    institution_control_number: Annotated[InstitutionControlNumber, XmlPath(f'{PATH}/NumCtrlIF/text()')]
    debtor_institution_ispb: Annotated[Ispb, XmlPath(f'{PATH}/ISPBIFDebtd/text()')]
    creditor_institution_ispb: Annotated[Ispb, XmlPath(f'{PATH}/ISPBIFCredtd/text()')]
    ltr_ispb: Annotated[Ispb, XmlPath(f'{PATH}/ISPBLTR/text()')]
    original_ltr_control_number: Annotated[InstitutionControlNumber, XmlPath(f'{PATH}/NumCtrlLTROr/text()')]
    branch: Annotated[Branch | None, XmlPath(f'{PATH}/AgCredtd/text()')] = None
    account_number: Annotated[AccountNumber | None, XmlPath(f'{PATH}/CtCredtd/text()')] = None
    amount: Annotated[Decimal, XmlPath(f'{PATH}/VlrLanc/text()')]
    sub_asset_type: Annotated[AssetType, XmlPath(f'{PATH}/SubTpAtv/text()')]
    asset_description: Annotated[AssetDescription | None, XmlPath(f'{PATH}/DescAtv/text()')] = None
    description: Annotated[Description | None, XmlPath(f'{PATH}/Hist/text()')] = None
    priority: Annotated[Priority | None, XmlPath(f'{PATH}/NivelPref/text()')] = None
    settlement_date: Annotated[date, XmlPath(f'{PATH}/DtMovto/text()')]


class LTR0003R1(BaseMessage):
    XML_NAMESPACE: ClassVar[str | None] = XML_NAMESPACE

    message_code: Annotated[Literal['LTR0003R1'], XmlPath(f'{PATH_R1}/CodMsg/text()')] = 'LTR0003R1'
    institution_control_number: Annotated[InstitutionControlNumber, XmlPath(f'{PATH_R1}/NumCtrlIF/text()')]
    institution_ispb: Annotated[Ispb, XmlPath(f'{PATH_R1}/ISPBIF/text()')]
    str_control_number: Annotated[StrControlNumber, XmlPath(f'{PATH_R1}/NumCtrlSTR/text()')]
    str_settlement_status: Annotated[StrSettlementStatus, XmlPath(f'{PATH_R1}/SitLancSTR/text()')]
    settlement_timestamp: Annotated[datetime, XmlPath(f'{PATH_R1}/DtHrSit/text()')]
    settlement_date: Annotated[date, XmlPath(f'{PATH_R1}/DtMovto/text()')]


class LTR0003R2(BaseMessage):
    XML_NAMESPACE: ClassVar[str | None] = XML_NAMESPACE

    message_code: Annotated[Literal['LTR0003R2'], XmlPath(f'{PATH_R2}/CodMsg/text()')] = 'LTR0003R2'
    str_control_number: Annotated[StrControlNumber, XmlPath(f'{PATH_R2}/NumCtrlSTR/text()')]
    debtor_institution_ispb: Annotated[Ispb, XmlPath(f'{PATH_R2}/ISPBIFDebtd/text()')]
    creditor_institution_ispb: Annotated[Ispb, XmlPath(f'{PATH_R2}/ISPBIFCredtd/text()')]
    ltr_ispb: Annotated[Ispb, XmlPath(f'{PATH_R2}/ISPBLTR/text()')]
    original_ltr_control_number: Annotated[InstitutionControlNumber, XmlPath(f'{PATH_R2}/NumCtrlLTROr/text()')]
    branch: Annotated[Branch, XmlPath(f'{PATH_R2}/AgCredtd/text()')]
    account_number: Annotated[AccountNumber, XmlPath(f'{PATH_R2}/CtCredtd/text()')]
    amount: Annotated[Decimal, XmlPath(f'{PATH_R2}/VlrLanc/text()')]
    sub_asset_type: Annotated[AssetType, XmlPath(f'{PATH_R2}/SubTpAtv/text()')]
    asset_description: Annotated[AssetDescription | None, XmlPath(f'{PATH_R2}/DescAtv/text()')] = None
    description: Annotated[Description | None, XmlPath(f'{PATH_R2}/Hist/text()')] = None
    priority: Annotated[Priority | None, XmlPath(f'{PATH_R2}/NivelPref/text()')] = None
    vendor_timestamp: Annotated[datetime, XmlPath(f'{PATH_R2}/DtHrBC/text()')]
    settlement_date: Annotated[date, XmlPath(f'{PATH_R2}/DtMovto/text()')]


class LTR0003R3(BaseMessage):
    XML_NAMESPACE: ClassVar[str | None] = XML_NAMESPACE

    message_code: Annotated[Literal['LTR0003R3'], XmlPath(f'{PATH_R3}/CodMsg/text()')] = 'LTR0003R3'
    str_control_number: Annotated[StrControlNumber, XmlPath(f'{PATH_R3}/NumCtrlSTR/text()')]
    debtor_institution_ispb: Annotated[Ispb, XmlPath(f'{PATH_R3}/ISPBIFDebtd/text()')]
    creditor_institution_ispb: Annotated[Ispb, XmlPath(f'{PATH_R3}/ISPBIFCredtd/text()')]
    ltr_ispb: Annotated[Ispb, XmlPath(f'{PATH_R3}/ISPBLTR/text()')]
    original_ltr_control_number: Annotated[InstitutionControlNumber, XmlPath(f'{PATH_R3}/NumCtrlLTROr/text()')]
    branch: Annotated[Branch, XmlPath(f'{PATH_R3}/AgCredtd/text()')]
    account_number: Annotated[AccountNumber, XmlPath(f'{PATH_R3}/CtCredtd/text()')]
    amount: Annotated[Decimal, XmlPath(f'{PATH_R3}/VlrLanc/text()')]
    description: Annotated[Description | None, XmlPath(f'{PATH_R3}/Hist/text()')] = None
    vendor_timestamp: Annotated[datetime, XmlPath(f'{PATH_R3}/DtHrBC/text()')]
    settlement_date: Annotated[date, XmlPath(f'{PATH_R3}/DtMovto/text()')]
