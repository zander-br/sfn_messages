from datetime import date
from decimal import Decimal
from typing import Annotated, ClassVar, Literal

from sfn_messages.core.models import BaseMessage, XmlPath
from sfn_messages.core.types import (
    AccountNumber,
    AccountType,
    Branch,
    Cnpj,
    Cpf,
    Description,
    ErrorCode,
    Ispb,
    PersonType,
)

from .types import SlbControlNumber, SlbPurpose

PATH = 'DOC/SISMSG/SLB0001'
PATH_R1 = 'DOC/SISMSG/SLB0001R1'
PATH_E = 'DOC/SISMSG/SLB0001'
XML_NAMESPACE = 'http://www.bcb.gov.br/SPB/SLB0001.xsd'
XML_NAMESPACE_ERROR = 'http://www.bcb.gov.br/SPB/SLB0001E.xsd'


class SLB0001(BaseMessage):
    XML_NAMESPACE: ClassVar[str | None] = XML_NAMESPACE

    message_code: Annotated[Literal['SLB0001'], XmlPath(f'{PATH}/CodMsg/text()')] = 'SLB0001'
    slb_control_number: Annotated[SlbControlNumber, XmlPath(f'{PATH}/NumCtrlSLB/text()')]
    participant_ispb: Annotated[Ispb, XmlPath(f'{PATH}/ISPBPart/text()')]
    original_slb_control_number: Annotated[SlbControlNumber | None, XmlPath(f'{PATH}/NumCtrlSLBOr/text()')] = None
    partner_cnpj: Annotated[Cnpj | None, XmlPath(f'{PATH}/CNPJConv/text()')] = None
    due_date: Annotated[date, XmlPath(f'{PATH}/DtVenc/text()')]
    description: Annotated[Description | None, XmlPath(f'{PATH}/Hist/text()')] = None
    amount: Annotated[Decimal, XmlPath(f'{PATH}/VlrLanc/text()')]
    slb_purpose: Annotated[SlbPurpose | None, XmlPath(f'{PATH}/FinlddSLB/text()')] = None
    branch: Annotated[Branch | None, XmlPath(f'{PATH}/AgDebtd/text()')] = None
    debtor_account_type: Annotated[AccountType | None, XmlPath(f'{PATH}/TpCtDebtd/text()')] = None
    account_number: Annotated[AccountNumber | None, XmlPath(f'{PATH}/CtDebtd/text()')] = None
    debtor_type: Annotated[PersonType | None, XmlPath(f'{PATH}/TpPessoaDebtd/text()')] = None
    debtor_document: Annotated[Cnpj | Cpf | None, XmlPath(f'{PATH}/CNPJ_CPFCliDebtd/text()')] = None
    settlement_date: Annotated[date, XmlPath(f'{PATH}/DtMovto/text()')]


class SLB0001E(BaseMessage):
    XML_NAMESPACE: ClassVar[str | None] = XML_NAMESPACE_ERROR

    message_code: Annotated[Literal['SLB0001E'], XmlPath(f'{PATH}/CodMsg/text()')] = 'SLB0001E'
    slb_control_number: Annotated[SlbControlNumber | None, XmlPath(f'{PATH}/NumCtrlSLB/text()')] = None
    participant_ispb: Annotated[Ispb | None, XmlPath(f'{PATH}/ISPBPart/text()')] = None
    original_slb_control_number: Annotated[SlbControlNumber | None, XmlPath(f'{PATH}/NumCtrlSLBOr/text()')] = None
    partner_cnpj: Annotated[Cnpj | None, XmlPath(f'{PATH}/CNPJConv/text()')] = None
    due_date: Annotated[date | None, XmlPath(f'{PATH}/DtVenc/text()')] = None
    description: Annotated[Description | None, XmlPath(f'{PATH}/Hist/text()')] = None
    amount: Annotated[Decimal | None, XmlPath(f'{PATH}/VlrLanc/text()')] = None
    slb_purpose: Annotated[SlbPurpose | None, XmlPath(f'{PATH}/FinlddSLB/text()')] = None
    branch: Annotated[Branch | None, XmlPath(f'{PATH}/AgDebtd/text()')] = None
    debtor_account_type: Annotated[AccountType | None, XmlPath(f'{PATH}/TpCtDebtd/text()')] = None
    account_number: Annotated[AccountNumber | None, XmlPath(f'{PATH}/CtDebtd/text()')] = None
    debtor_type: Annotated[PersonType | None, XmlPath(f'{PATH}/TpPessoaDebtd/text()')] = None
    debtor_document: Annotated[Cnpj | Cpf | None, XmlPath(f'{PATH}/CNPJ_CPFCliDebtd/text()')] = None
    settlement_date: Annotated[date | None, XmlPath(f'{PATH}/DtMovto/text()')] = None

    general_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH}/@CodErro')] = None
    slb_control_number_error_code: Annotated[SlbControlNumber | None, XmlPath(f'{PATH}/NumCtrlSLB/@CodErro')] = None
    participant_ispb_error_code: Annotated[Ispb | None, XmlPath(f'{PATH}/ISPBPart/@CodErro')] = None
    original_slb_control_number_error_code: Annotated[
        SlbControlNumber | None, XmlPath(f'{PATH}/NumCtrlSLBOr/@CodErro')
    ] = None
    partner_cnpj_error_code: Annotated[Cnpj | None, XmlPath(f'{PATH}/CNPJConv/@CodErro')] = None
    due_date_error_code: Annotated[date | None, XmlPath(f'{PATH}/DtVenc/@CodErro')] = None
    description_error_code: Annotated[Description | None, XmlPath(f'{PATH}/Hist/@CodErro')] = None
    amount_error_code: Annotated[Decimal | None, XmlPath(f'{PATH}/VlrLanc/@CodErro')] = None
    slb_purpose_error_code: Annotated[SlbPurpose | None, XmlPath(f'{PATH}/FinlddSLB/@CodErro')] = None
    branch_error_code: Annotated[Branch | None, XmlPath(f'{PATH}/AgDebtd/@CodErro')] = None
    debtor_account_type_error_code: Annotated[AccountType | None, XmlPath(f'{PATH}/TpCtDebtd/@CodErro')] = None
    account_number_error_code: Annotated[AccountNumber | None, XmlPath(f'{PATH}/CtDebtd/@CodErro')] = None
    debtor_type_error_code: Annotated[PersonType | None, XmlPath(f'{PATH}/TpPessoaDebtd/@CodErro')] = None
    debtor_document_error_code: Annotated[Cnpj | Cpf | None, XmlPath(f'{PATH}/CNPJ_CPFCliDebtd/@CodErro')] = None
    settlement_date_error_code: Annotated[date | None, XmlPath(f'{PATH}/DtMovto/@CodErro')] = None
