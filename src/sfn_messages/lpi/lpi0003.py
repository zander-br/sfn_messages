from datetime import date, datetime
from decimal import Decimal
from typing import Annotated, ClassVar, Literal

from sfn_messages.core.models import BaseMessage, BaseSubMessage, XmlPath
from sfn_messages.core.types import (
    AccountNumber,
    Branch,
    Cnpj,
    ErrorCode,
    Ispb,
    StrControlNumber,
    StrSettlementStatus,
)

from .types import LpiPurpose

PATH = 'DOC/SISMSG/LPI0003'
PATH_GROUP = 'Grupo_LPI0003_CliCredtd'
PATH_R1 = 'DOC/SISMSG/LPI0003R1'
PATH_R2 = 'DOC/SISMSG/LPI0003R2'
PATH_R2_GROUP = 'Grupo_LPI0003R2_CliCredtd'
PATH_E = 'DOC/SISMSG/LPI0003'
XML_NAMESPACE = 'http://www.bcb.gov.br/SPB/LPI0003.xsd'
XML_NAMESPACE_ERROR = 'http://www.bcb.gov.br/SPB/LPI0003E.xsd'


class CreditorClientGroup(BaseSubMessage):
    branch: Annotated[Branch | None, XmlPath(f'{PATH_GROUP}/AgCredtd/text()')] = None
    account_number: Annotated[AccountNumber | None, XmlPath(f'{PATH_GROUP}/CtCredtd/text()')] = None
    creditor_payment_account_number: Annotated[AccountNumber | None, XmlPath(f'{PATH_GROUP}/CtPgtoCredtd/text()')] = (
        None
    )
    cnpj: Annotated[Cnpj, XmlPath(f'{PATH_GROUP}/CNPJCliCredtd/text()')]


class LPI0003(BaseMessage):
    XML_NAMESPACE: ClassVar[str | None] = XML_NAMESPACE

    message_code: Annotated[Literal['LPI0003'], XmlPath(f'{PATH}/CodMsg/text()')] = 'LPI0003'
    pspi_ispb: Annotated[Ispb, XmlPath(f'{PATH}/ISPBPSPI/text()')]
    creditor_institution_ispb: Annotated[Ispb, XmlPath(f'{PATH}/ISPBIFCredtd/text()')]
    creditor_client_group: Annotated[CreditorClientGroup | None, XmlPath(f'{PATH}')] = None
    lpi_purpose: Annotated[LpiPurpose, XmlPath(f'{PATH}/FinlddLPI/text()')]
    original_str_control_number: Annotated[StrControlNumber | None, XmlPath(f'{PATH}/NumCtrlSTROr/text()')] = None
    amount: Annotated[Decimal, XmlPath(f'{PATH}/VlrLanc/text()')]
    settlement_date: Annotated[date, XmlPath(f'{PATH}/DtMovto/text()')]


class LPI0003R1(BaseMessage):
    XML_NAMESPACE: ClassVar[str | None] = XML_NAMESPACE

    message_code: Annotated[Literal['LPI0003R1'], XmlPath(f'{PATH_R1}/CodMsg/text()')] = 'LPI0003R1'
    pspi_control_number: Annotated[str, XmlPath(f'{PATH_R1}/NumCtrlPSPI/text()')]
    pspi_ispb: Annotated[Ispb, XmlPath(f'{PATH_R1}/ISPBPSPI/text()')]
    str_control_number: Annotated[StrControlNumber, XmlPath(f'{PATH_R1}/NumCtrlSTR/text()')]
    str_settlement_status: Annotated[StrSettlementStatus, XmlPath(f'{PATH_R1}/SitLancSTR/text()')]
    settlement_timestamp: Annotated[datetime, XmlPath(f'{PATH_R1}/DtHrSit/text()')]
    settlement_date: Annotated[date, XmlPath(f'{PATH_R1}/DtMovto/text()')]


class CreditorClientR2Group(BaseSubMessage):
    branch: Annotated[Branch | None, XmlPath(f'{PATH_R2_GROUP}/AgCredtd/text()')] = None
    account_number: Annotated[AccountNumber | None, XmlPath(f'{PATH_R2_GROUP}/CtCredtd/text()')] = None
    creditor_payment_account_number: Annotated[
        AccountNumber | None, XmlPath(f'{PATH_R2_GROUP}/CtPgtoCredtd/text()')
    ] = None
    cnpj: Annotated[Cnpj, XmlPath(f'{PATH_R2_GROUP}/CNPJCliCredtd/text()')]


class LPI0003R2(BaseMessage):
    XML_NAMESPACE: ClassVar[str | None] = XML_NAMESPACE

    message_code: Annotated[Literal['LPI0003R2'], XmlPath(f'{PATH_R2}/CodMsg/text()')] = 'LPI0003R2'
    str_control_number: Annotated[StrControlNumber, XmlPath(f'{PATH_R2}/NumCtrlSTR/text()')]
    vendor_timestamp: Annotated[datetime, XmlPath(f'{PATH_R2}/DtHrBC/text()')]
    pspi_ispb: Annotated[Ispb, XmlPath(f'{PATH_R2}/ISPBPSPI/text()')]
    creditor_institution_ispb: Annotated[Ispb, XmlPath(f'{PATH_R2}/ISPBIFCredtd/text()')]
    creditor_client_group: Annotated[CreditorClientR2Group | None, XmlPath(f'{PATH_R2}')] = None
    lpi_purpose: Annotated[LpiPurpose, XmlPath(f'{PATH_R2}/FinlddLPI/text()')]
    original_str_control_number: Annotated[StrControlNumber | None, XmlPath(f'{PATH_R2}/NumCtrlSTROr/text()')] = None
    amount: Annotated[Decimal, XmlPath(f'{PATH_R2}/VlrLanc/text()')]
    settlement_date: Annotated[date, XmlPath(f'{PATH_R2}/DtMovto/text()')]


class CreditorClientGroupError(BaseSubMessage):
    branch: Annotated[Branch | None, XmlPath(f'{PATH_GROUP}/AgCredtd/text()')] = None
    account_number: Annotated[AccountNumber | None, XmlPath(f'{PATH_GROUP}/CtCredtd/text()')] = None
    creditor_payment_account_number: Annotated[AccountNumber | None, XmlPath(f'{PATH_GROUP}/CtPgtoCredtd/text()')] = (
        None
    )
    cnpj: Annotated[Cnpj | None, XmlPath(f'{PATH_GROUP}/CNPJCliCredtd/text()')] = None

    branch_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH_GROUP}/AgCredtd/@CodErro')] = None
    account_number_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH_GROUP}/CtCredtd/@CodErro')] = None
    creditor_payment_account_number_error_code: Annotated[
        ErrorCode | None, XmlPath(f'{PATH_GROUP}/CtPgtoCredtd/@CodErro')
    ] = None
    cnpj_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH_GROUP}/CNPJCliCredtd/@CodErro')] = None


class LPI0003E(BaseMessage):
    XML_NAMESPACE: ClassVar[str | None] = XML_NAMESPACE_ERROR

    message_code: Annotated[Literal['LPI0003E'], XmlPath(f'{PATH_E}/CodMsg/text()')] = 'LPI0003E'
    pspi_ispb: Annotated[Ispb | None, XmlPath(f'{PATH_E}/ISPBPSPI/text()')] = None
    creditor_institution_ispb: Annotated[Ispb | None, XmlPath(f'{PATH_E}/ISPBIFCredtd/text()')] = None
    creditor_client_group: Annotated[CreditorClientGroupError | None, XmlPath(f'{PATH_E}')] = None
    lpi_purpose: Annotated[LpiPurpose | None, XmlPath(f'{PATH_E}/FinlddLPI/text()')] = None
    original_str_control_number: Annotated[StrControlNumber | None, XmlPath(f'{PATH_E}/NumCtrlSTROr/text()')] = None
    amount: Annotated[Decimal | None, XmlPath(f'{PATH_E}/VlrLanc/text()')] = None
    settlement_date: Annotated[date | None, XmlPath(f'{PATH_E}/DtMovto/text()')] = None

    general_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH_E}/@CodErro')] = None
    pspi_ispb_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH_E}/ISPBPSPI/@CodErro')] = None
    creditor_institution_ispb_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH_E}/ISPBIFCredtd/@CodErro')] = (
        None
    )
    lpi_purpose_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH_E}/FinlddLPI/@CodErro')] = None
    original_str_control_number_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH_E}/NumCtrlSTROr/@CodErro')] = (
        None
    )
    amount_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH_E}/VlrLanc/@CodErro')] = None
    settlement_date_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH_E}/DtMovto/@CodErro')] = None
