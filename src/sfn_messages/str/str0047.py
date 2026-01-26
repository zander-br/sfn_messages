from datetime import date, datetime, time
from decimal import Decimal
from typing import Annotated, ClassVar, Literal

from sfn_messages.core.models import BaseMessage, XmlPath
from sfn_messages.core.types import (
    AccountNumber,
    Branch,
    Cnpj,
    Cpf,
    Description,
    ErrorCode,
    InstitutionControlNumber,
    Ispb,
    Name,
    Priority,
    StrControlNumber,
    StrSettlementStatus,
)

from .types import PortabilityReturnReason

PATH = 'DOC/SISMSG/STR0047'
PATH_R1 = 'DOC/SISMSG/STR0047R1'
PATH_R2 = 'DOC/SISMSG/STR0047R2'
PATH_R3 = 'DOC/SISMSG/STR0047R3'
PATH_E = 'DOC/SISMSG/STR0047'
XML_NAMESPACE = 'http://www.bcb.gov.br/SPB/STR0047.xsd'
XML_NAMESPACE_ERROR = 'http://www.bcb.gov.br/SPB/STR0047E.xsd'


class STR0047(BaseMessage):
    XML_NAMESPACE: ClassVar[str | None] = XML_NAMESPACE

    message_code: Annotated[Literal['STR0047'], XmlPath(f'{PATH}/CodMsg/text()')] = 'STR0047'
    institution_control_number: Annotated[InstitutionControlNumber, XmlPath(f'{PATH}/NumCtrlIF/text()')]
    debtor_institution_ispb: Annotated[Ispb, XmlPath(f'{PATH}/ISPBIFDebtd/text()')]
    debtor_branch: Annotated[Branch | None, XmlPath(f'{PATH}/AgDebtd/text()')] = None
    debtor_account_number: Annotated[
        AccountNumber | None, XmlPath(f'{PATH}/Grupo_STR0047_AgtFinancDebtd/CtDebtd/text()')
    ] = None
    debtor_document: Annotated[
        Cnpj | Cpf | None, XmlPath(f'{PATH}/Grupo_STR0047_AgtFinancDebtd/CNPJ_CPFCliDebtd/text()')
    ] = None
    debtor_name: Annotated[Name | None, XmlPath(f'{PATH}/Grupo_STR0047_AgtFinancDebtd/NomeCliDebtd/text()')] = None
    creditor_institution_ispb: Annotated[Ispb, XmlPath(f'{PATH}/ISPBIFCredtd/text()')]
    creditor_branch: Annotated[Branch, XmlPath(f'{PATH}/AgCredtd/text()')]
    creditor_account_number: Annotated[
        AccountNumber | None, XmlPath(f'{PATH}/Grupo_STR0047_AgtFinancCredtd/CtCredtd/text()')
    ] = None
    creditor_document: Annotated[
        Cnpj | None, XmlPath(f'{PATH}/Grupo_STR0047_AgtFinancCredtd/CNPJCliCredtd/text()')
    ] = None
    creditor_name: Annotated[Name | None, XmlPath(f'{PATH}/Grupo_STR0047_AgtFinancCredtd/NomCliCredtd/text()')] = None
    amount: Annotated[Decimal, XmlPath(f'{PATH}/VlrLanc/text()')]

    portability_return_reason: Annotated[PortabilityReturnReason, XmlPath(f'{PATH}/CodDevPortdd/text()')]
    original_str_control_number: Annotated[StrControlNumber, XmlPath(f'{PATH}/NumCtrlSTROr/text()')]
    provider_ispb: Annotated[Ispb, XmlPath(f'{PATH}/ISPBPrestd/text()')]
    description: Annotated[Description | None, XmlPath(f'{PATH}/Hist/text()')] = None
    scheduled_date: Annotated[date | None, XmlPath(f'{PATH}/DtAgendt/text()')] = None
    scheduled_time: Annotated[time | None, XmlPath(f'{PATH}/HrAgendt/text()')] = None
    priority: Annotated[Priority | None, XmlPath(f'{PATH}/NivelPref/text()')] = None
    settlement_date: Annotated[date, XmlPath(f'{PATH}/DtMovto/text()')]


class STR0047R1(BaseMessage):
    XML_NAMESPACE: ClassVar[str | None] = XML_NAMESPACE

    message_code: Annotated[Literal['STR0047R1'], XmlPath(f'{PATH_R1}/CodMsg/text()')] = 'STR0047R1'
    institution_control_number: Annotated[InstitutionControlNumber, XmlPath(f'{PATH_R1}/NumCtrlIF/text()')]
    debtor_institution_ispb: Annotated[Ispb, XmlPath(f'{PATH_R1}/ISPBIFDebtd/text()')]
    str_control_number: Annotated[StrControlNumber, XmlPath(f'{PATH_R1}/NumCtrlSTR/text()')]
    str_settlement_status: Annotated[StrSettlementStatus, XmlPath(f'{PATH_R1}/SitLancSTR/text()')]
    settlement_timestamp: Annotated[datetime, XmlPath(f'{PATH_R1}/DtHrSit/text()')]
    settlement_date: Annotated[date, XmlPath(f'{PATH_R1}/DtMovto/text()')]


class STR0047R2(BaseMessage):
    XML_NAMESPACE: ClassVar[str | None] = XML_NAMESPACE

    message_code: Annotated[Literal['STR0047R2'], XmlPath(f'{PATH_R2}/CodMsg/text()')] = 'STR0047R2'
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


class STR0047E(BaseMessage):
    XML_NAMESPACE: ClassVar[str | None] = XML_NAMESPACE_ERROR

    message_code: Annotated[Literal['STR0047E'], XmlPath(f'{PATH_E}/CodMsg/text()')] = 'STR0047E'
    institution_control_number: Annotated[InstitutionControlNumber | None, XmlPath(f'{PATH_E}/NumCtrlIF/text()')] = (
        None
    )
    debtor_institution_ispb: Annotated[Ispb | None, XmlPath(f'{PATH_E}/ISPBIFDebtd/text()')] = None
    creditor_institution_ispb: Annotated[Ispb | None, XmlPath(f'{PATH_E}/ISPBIFCredtd/text()')] = None
    amount: Annotated[Decimal | None, XmlPath(f'{PATH_E}/VlrLanc/text()')] = None
    portability_return_reason: Annotated[PortabilityReturnReason | None, XmlPath(f'{PATH_E}/CodDevPortdd/text()')] = (
        None
    )
    original_str_control_number: Annotated[StrControlNumber | None, XmlPath(f'{PATH_E}/NumCtrlSTROr/text()')] = None
    provider_ispb: Annotated[Ispb | None, XmlPath(f'{PATH_E}/ISPBPrestd/text()')] = None
    description: Annotated[Description | None, XmlPath(f'{PATH_E}/Hist/text()')] = None
    scheduled_date: Annotated[date | None, XmlPath(f'{PATH_E}/DtAgendt/text()')] = None
    scheduled_time: Annotated[time | None, XmlPath(f'{PATH_E}/HrAgendt/text()')] = None
    priority: Annotated[Priority | None, XmlPath(f'{PATH_E}/NivelPref/text()')] = None
    settlement_date: Annotated[date | None, XmlPath(f'{PATH_E}/DtMovto/text()')] = None

    general_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH_E}/@CodErro')] = None
    institution_control_number_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH_E}/NumCtrlIF/@CodErro')] = None
    debtor_institution_ispb_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH_E}/ISPBIFDebtd/@CodErro')] = None
    creditor_institution_ispb_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH_E}/ISPBIFCredtd/@CodErro')] = (
        None
    )
    amount_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH_E}/VlrLanc/@CodErro')] = None
    portability_return_reason_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH_E}/CodDevPortdd/@CodErro')] = (
        None
    )
    original_str_control_number_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH_E}/NumCtrlSTROr/@CodErro')] = (
        None
    )
    provider_ispb_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH_E}/ISPBPrestd/@CodErro')] = None
    description_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH_E}/Hist/@CodErro')] = None
    scheduled_date_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH_E}/DtAgendt/@CodErro')] = None
    scheduled_time_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH_E}/HrAgendt/@CodErro')] = None
    priority_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH_E}/NivelPref/@CodErro')] = None
    settlement_date_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH_E}/DtMovto/@CodErro')] = None
