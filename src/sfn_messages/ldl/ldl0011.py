from datetime import date, datetime
from decimal import Decimal
from typing import Annotated, ClassVar, Literal

from sfn_messages.core.models import BaseMessage, XmlPath
from sfn_messages.core.types import (
    AccountNumber,
    Branch,
    ErrorCode,
    InstitutionControlNumber,
    Ispb,
    LdlControlNumber,
    LdlSettlementStatus,
    StrControlNumber,
)

PATH = 'DOC/SISMSG/LDL0011'
PATH_R1 = 'DOC/SISMSG/LDL0011R1'
PATH_R2 = 'DOC/SISMSG/LDL0011R2'
PATH_E = 'DOC/SISMSG/LDL0011E'
XML_NAMESPACE = 'http://www.bcb.gov.br/LDL/LDL0011.xsd'
XML_NAMESPACE_ERROR = 'http://www.bcb.gov.br/LDL/LDL0011E.xsd'


class LDL0011(BaseMessage):
    XML_NAMESPACE: ClassVar[str | None] = XML_NAMESPACE

    message_code: Annotated[Literal['LDL0011'], XmlPath(f'{PATH}/CodMsg/text()')] = 'LDL0011'
    institution_control_number: Annotated[InstitutionControlNumber, XmlPath(f'{PATH}/NumCtrlIF/text()')]
    institution_ispb: Annotated[Ispb, XmlPath(f'{PATH}/ISPBIF/text()')]
    original_ldl_control_number: Annotated[LdlControlNumber, XmlPath(f'{PATH}/NumCtrlLDLOr/text()')]
    branch: Annotated[Branch, XmlPath(f'{PATH}/AgDebtd/text()')]
    account_number: Annotated[AccountNumber, XmlPath(f'{PATH}/CtDebtd/text()')]
    ldl_ispb: Annotated[Ispb, XmlPath(f'{PATH}/ISPBLDL/text()')]
    amount: Annotated[Decimal, XmlPath(f'{PATH}/VlrLanc/text()')]
    settlement_date: Annotated[date, XmlPath(f'{PATH}/DtMovto/text()')]


class LDL0011R1(BaseMessage):
    XML_NAMESPACE: ClassVar[str | None] = XML_NAMESPACE

    message_code: Annotated[Literal['LDL0011R1'], XmlPath(f'{PATH_R1}/CodMsg/text()')] = 'LDL0011R1'
    institution_control_number: Annotated[InstitutionControlNumber, XmlPath(f'{PATH_R1}/NumCtrlIF/text()')]
    debtor_institution_ispb: Annotated[Ispb, XmlPath(f'{PATH_R1}/ISPBIFDebtd/text()')]
    str_control_number: Annotated[StrControlNumber, XmlPath(f'{PATH_R1}/NumCtrlSTR/text()')]
    ldl_settlement_status: Annotated[LdlSettlementStatus, XmlPath(f'{PATH_R1}/SitLancLDL/text()')]
    settlement_timestamp: Annotated[datetime, XmlPath(f'{PATH_R1}/DtHrSit/text()')]
    settlement_date: Annotated[date, XmlPath(f'{PATH_R1}/DtMovto/text()')]


class LDL0011R2(BaseMessage):
    XML_NAMESPACE: ClassVar[str | None] = XML_NAMESPACE

    message_code: Annotated[Literal['LDL0011R2'], XmlPath(f'{PATH_R2}/CodMsg/text()')] = 'LDL0011R2'
    str_control_number: Annotated[StrControlNumber, XmlPath(f'{PATH_R2}/NumCtrlSTR/text()')]
    vendor_timestamp: Annotated[datetime, XmlPath(f'{PATH_R2}/DtHrBC/text()')]
    original_ldl_control_number: Annotated[LdlControlNumber, XmlPath(f'{PATH_R2}/NumCtrlLDLOr/text()')]
    institution_ispb: Annotated[Ispb, XmlPath(f'{PATH_R2}/ISPBIF/text()')]
    branch: Annotated[Branch, XmlPath(f'{PATH_R2}/AgDebtd/text()')]
    account_number: Annotated[AccountNumber, XmlPath(f'{PATH_R2}/CtDebtd/text()')]
    ldl_ispb: Annotated[Ispb, XmlPath(f'{PATH_R2}/ISPBLDL/text()')]
    amount: Annotated[Decimal, XmlPath(f'{PATH_R2}/VlrLanc/text()')]
    settlement_date: Annotated[date, XmlPath(f'{PATH_R2}/DtMovto/text()')]


class LDL0011E(BaseMessage):
    XML_NAMESPACE: ClassVar[str | None] = XML_NAMESPACE_ERROR

    message_code: Annotated[Literal['LDL0011'], XmlPath(f'{PATH_E}/CodMsg/text()')] = 'LDL0011'
    institution_control_number: Annotated[InstitutionControlNumber, XmlPath(f'{PATH_E}/NumCtrlIF/text()')]
    institution_ispb: Annotated[Ispb, XmlPath(f'{PATH_E}/ISPBIF/text()')]
    original_ldl_control_number: Annotated[LdlControlNumber, XmlPath(f'{PATH_E}/NumCtrlLDLOr/text()')]
    branch: Annotated[Branch, XmlPath(f'{PATH_E}/AgDebtd/text()')]
    account_number: Annotated[AccountNumber, XmlPath(f'{PATH_E}/CtDebtd/text()')]
    ldl_ispb: Annotated[Ispb, XmlPath(f'{PATH_E}/ISPBLDL/text()')]
    amount: Annotated[Decimal, XmlPath(f'{PATH_E}/VlrLanc/text()')]
    settlement_date: Annotated[date, XmlPath(f'{PATH_E}/DtMovto/text()')]

    general_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH_E}/@CodErro')] = None
    institution_control_number_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH_E}/NumCtrlIF/@CodErro')] = None
    institution_ispb_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH_E}/ISPBIF/@CodErro')] = None
    original_ldl_control_number_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH_E}/NumCtrlLDLOr/@CodErro')] = (
        None
    )
    branch_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH_E}/AgDebtd/@CodErro')] = None
    account_number_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH_E}/CtDebtd/@CodErro')] = None
    ldl_ispb_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH_E}/ISPBLDL/@CodErro')] = None
    amount_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH_E}/VlrLanc/@CodErro')] = None
    settlement_date_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH_E}/DtMovto/@CodErro')] = None
