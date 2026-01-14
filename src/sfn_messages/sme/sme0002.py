from datetime import date, datetime
from decimal import Decimal
from typing import Annotated, ClassVar, Literal

from sfn_messages.core.models import BaseMessage, BaseSubMessage, XmlPath
from sfn_messages.core.types import (
    AccountNumber,
    Branch,
    Cnpj,
    ErrorCode,
    InstitutionControlNumber,
    Ispb,
    StrControlNumber,
    StrSettlementStatus,
)

PATH = 'DOC/SISMSG/SME0002'
PATH_GROUP = 'Grupo_SME0002_CtCredtd'
PATH_R1 = 'DOC/SISMSG/SME0002R1'
PATH_R2 = 'DOC/SISMSG/SME0002R2'
PATH_E = 'DOC/SISMSG/SME0002E'
XML_NAMESPACE = 'http://www.bcb.gov.br/SME/SME0002.xsd'
XML_NAMESPACE_ERROR = 'http://www.bcb.gov.br/SME/SME0002E.xsd'


class CreditorGroup(BaseSubMessage):
    institution_ispb: Annotated[Ispb, XmlPath(f'{PATH_GROUP}/ISPBIFCredtd/text()')]
    branch: Annotated[Branch, XmlPath(f'{PATH_GROUP}/AgCredtd/text()')]
    account_number: Annotated[AccountNumber, XmlPath(f'{PATH_GROUP}/CtCredtd/text()')]
    cnpj: Annotated[Cnpj, XmlPath(f'{PATH_GROUP}/CNPJCliCredtd/text()')]


class SME0002(BaseMessage):
    XML_NAMESPACE: ClassVar[str | None] = XML_NAMESPACE

    message_code: Annotated[Literal['SME0002'], XmlPath(f'{PATH}/CodMsg/text()')] = 'SME0002'
    ieme_ispb: Annotated[Ispb, XmlPath(f'{PATH}/ISPBIEME/text()')]
    creditor_account_group: Annotated[CreditorGroup | None, XmlPath(f'{PATH}')] = None
    amount: Annotated[Decimal, XmlPath(f'{PATH}/VlrLanc/text()')]
    settlement_date: Annotated[date, XmlPath(f'{PATH}/DtMovto/text()')]


class SME0002R1(BaseMessage):
    XML_NAMESPACE: ClassVar[str | None] = XML_NAMESPACE

    message_code: Annotated[Literal['SME0002R1'], XmlPath(f'{PATH_R1}/CodMsg/text()')] = 'SME0002R1'
    institution_control_number_ieme: Annotated[InstitutionControlNumber, XmlPath(f'{PATH_R1}/NumCtrlIEME/text()')]
    ieme_ispb: Annotated[Ispb, XmlPath(f'{PATH_R1}/ISPBIEME/text()')]
    str_control_number: Annotated[StrControlNumber, XmlPath(f'{PATH_R1}/NumCtrlSTR/text()')]
    str_settlement_status: Annotated[StrSettlementStatus, XmlPath(f'{PATH_R1}/SitLancSTR/text()')]
    settlement_timestamp: Annotated[datetime, XmlPath(f'{PATH_R1}/DtHrSit/text()')]
    settlement_date: Annotated[date, XmlPath(f'{PATH_R1}/DtMovto/text()')]


class SME0002R2(BaseMessage):
    XML_NAMESPACE: ClassVar[str | None] = XML_NAMESPACE

    message_code: Annotated[Literal['SME0002R2'], XmlPath(f'{PATH_R2}/CodMsg/text()')] = 'SME0002R2'
    str_control_number: Annotated[StrControlNumber, XmlPath(f'{PATH_R2}/NumCtrlSTR/text()')]
    vendor_timestamp: Annotated[datetime, XmlPath(f'{PATH_R2}/DtHrBC/text()')]
    ieme_ispb: Annotated[Ispb, XmlPath(f'{PATH_R2}/ISPBIEME/text()')]
    institution_ispb: Annotated[Ispb, XmlPath(f'{PATH_R2}/ISPBIFCredtd/text()')]
    creditor_branch: Annotated[Branch, XmlPath(f'{PATH_R2}/AgCredtd/text()')]
    creditor_account_number: Annotated[AccountNumber, XmlPath(f'{PATH_R2}/CtCredtd/text()')]
    creditor_cnpj: Annotated[Cnpj, XmlPath(f'{PATH_R2}/CNPJCliCredtd/text()')]
    settlement_date: Annotated[date, XmlPath(f'{PATH_R2}/DtMovto/text()')]


class CreditorGroupError(BaseSubMessage):
    institution_ispb: Annotated[Ispb, XmlPath(f'{PATH_GROUP}/ISPBIFCredtd/text()')]
    branch: Annotated[Branch, XmlPath(f'{PATH_GROUP}/AgCredtd/text()')]
    account_number: Annotated[AccountNumber, XmlPath(f'{PATH_GROUP}/CtCredtd/text()')]
    cnpj: Annotated[Cnpj, XmlPath(f'{PATH_GROUP}/CNPJCliCredtd/text()')]

    institution_ispb_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH_GROUP}/ISPBIFCredtd/@CodErro')] = None
    branch_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH_GROUP}/AgCredtd/@CodErro')] = None
    account_number_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH_GROUP}/CtCredtd/@CodErro')] = None
    cnpj_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH_GROUP}/CNPJCliCredtd/@CodErro')] = None


class SME0002E(BaseMessage):
    XML_NAMESPACE: ClassVar[str | None] = XML_NAMESPACE_ERROR

    message_code: Annotated[Literal['SME0002'], XmlPath(f'{PATH_E}/CodMsg/text()')] = 'SME0002'
    ieme_ispb: Annotated[Ispb, XmlPath(f'{PATH_E}/ISPBIEME/text()')]
    creditor_account_group: Annotated[CreditorGroupError | None, XmlPath(f'{PATH_E}')] = None
    amount: Annotated[Decimal, XmlPath(f'{PATH_E}/VlrLanc/text()')]
    settlement_date: Annotated[date, XmlPath(f'{PATH_E}/DtMovto/text()')]

    general_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH_E}/@CodErro')] = None
    ieme_ispb_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH_E}/ISPBIEME/@CodErro')] = None
    amount_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH_E}/VlrLanc/@CodErro')] = None
    settlement_date_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH_E}/DtMovto/@CodErro')] = None
