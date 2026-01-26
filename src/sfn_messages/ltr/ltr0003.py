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
    ErrorCode,
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
PATH_E = 'DOC/SISMSG/LTR0003'
XML_NAMESPACE = 'http://www.bcb.gov.br/SPB/LTR0003.xsd'
XML_NAMESPACE_ERROR = 'http://www.bcb.gov.br/SPB/LTR0003E.xsd'


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


class LTR0003E(BaseMessage):
    XML_NAMESPACE: ClassVar[str | None] = XML_NAMESPACE_ERROR

    message_code: Annotated[Literal['LTR0003E'], XmlPath(f'{PATH_E}/CodMsg/text()')] = 'LTR0003E'
    institution_control_number: Annotated[InstitutionControlNumber | None, XmlPath(f'{PATH_E}/NumCtrlIF/text()')] = (
        None
    )
    debtor_institution_ispb: Annotated[Ispb | None, XmlPath(f'{PATH_E}/ISPBIFDebtd/text()')] = None
    creditor_institution_ispb: Annotated[Ispb | None, XmlPath(f'{PATH_E}/ISPBIFCredtd/text()')] = None
    ltr_ispb: Annotated[Ispb | None, XmlPath(f'{PATH_E}/ISPBLTR/text()')] = None
    original_ltr_control_number: Annotated[
        InstitutionControlNumber | None, XmlPath(f'{PATH_E}/NumCtrlLTROr/text()')
    ] = None
    branch: Annotated[Branch | None, XmlPath(f'{PATH_E}/AgCredtd/text()')] = None
    account_number: Annotated[AccountNumber | None, XmlPath(f'{PATH_E}/CtCredtd/text()')] = None
    amount: Annotated[Decimal | None, XmlPath(f'{PATH_E}/VlrLanc/text()')] = None
    sub_asset_type: Annotated[AssetType | None, XmlPath(f'{PATH_E}/SubTpAtv/text()')] = None
    asset_description: Annotated[AssetDescription | None, XmlPath(f'{PATH_E}/DescAtv/text()')] = None
    description: Annotated[Description | None, XmlPath(f'{PATH_E}/Hist/text()')] = None
    priority: Annotated[Priority | None, XmlPath(f'{PATH_E}/NivelPref/text()')] = None
    settlement_date: Annotated[date | None, XmlPath(f'{PATH_E}/DtMovto/text()')] = None

    general_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH_E}/@CodErro')] = None
    institution_control_number_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH_E}/NumCtrlIF/@CodErro')] = None
    debtor_institution_ispb_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH_E}/ISPBIFDebtd/@CodErro')] = None
    creditor_institution_ispb_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH_E}/ISPBIFCredtd/@CodErro')] = (
        None
    )
    ltr_ispb_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH_E}/ISPBLTR/@CodErro')] = None
    original_ltr_control_number_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH_E}/NumCtrlLTROr/@CodErro')] = (
        None
    )
    branch_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH_E}/AgCredtd/@CodErro')] = None
    account_number_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH_E}/CtCredtd/@CodErro')] = None
    amount_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH_E}/VlrLanc/@CodErro')] = None
    sub_asset_type_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH_E}/SubTpAtv/@CodErro')] = None
    asset_description_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH_E}/DescAtv/@CodErro')] = None
    description_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH_E}/Hist/@CodErro')] = None
    priority_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH_E}/NivelPref/@CodErro')] = None
    settlement_date_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH_E}/DtMovto/@CodErro')] = None
