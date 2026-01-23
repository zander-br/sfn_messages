from datetime import date
from decimal import Decimal
from typing import Annotated, ClassVar, Literal

from sfn_messages.core.models import BaseMessage, XmlPath
from sfn_messages.core.types import (
    AccountNumber,
    AssetDescription,
    AssetType,
    Branch,
    Cnpj,
    Description,
    ErrorCode,
    Ispb,
    LdlControlNumber,
    ParticipantIdentifier,
)

PATH = 'DOC/SISMSG/LTR0001'
PATH_E = 'DOC/SISMSG/LTR0001E'
XML_NAMESPACE = 'http://www.bcb.gov.br/SPB/LTR0001.xsd'
XML_NAMESPACE_ERROR = 'http://www.bcb.gov.br/SPB/LTR0001E.xsd'


class LTR0001(BaseMessage):
    XML_NAMESPACE: ClassVar[str | None] = XML_NAMESPACE

    message_code: Annotated[Literal['LTR0001'], XmlPath(f'{PATH}/CodMsg/text()')] = 'LTR0001'
    ltr_control_number: Annotated[LdlControlNumber, XmlPath(f'{PATH}/NumCtrlLTR/text()')]
    ltr_ispb: Annotated[Ispb, XmlPath(f'{PATH}/ISPBLTR/text()')]
    debtor_institution_ispb: Annotated[Ispb, XmlPath(f'{PATH_E}/ISPBIFDebtd/text()')]
    creditor_institution_ispb: Annotated[Ispb, XmlPath(f'{PATH_E}/ISPBIFCredtd/text()')]
    cnpj: Annotated[Cnpj, XmlPath(f'{PATH}/CNPJNLiqdant/text()')]
    participant_identifier: Annotated[ParticipantIdentifier | None, XmlPath(f'{PATH}/IdentdPartCamr/text()')] = None
    debtor_branch: Annotated[Branch | None, XmlPath(f'{PATH}/AgDebtd/text()')] = None
    debtor_account_number: Annotated[AccountNumber | None, XmlPath(f'{PATH}/CtDebtd/text()')] = None
    amount: Annotated[Decimal, XmlPath(f'{PATH}/VlrLanc/text()')]
    tipo: Annotated[str, XmlPath(f'{PATH}/TpOpLTR/text()')]
    numero: Annotated[str, XmlPath(f'{PATH}/NumOpLTR/text()')]
    sub_asset_type: Annotated[AssetType, XmlPath(f'{PATH}/SubTpAtv/text()')]
    asset_description: Annotated[AssetDescription | None, XmlPath(f'{PATH}/DescAtv/text()')] = None
    description: Annotated[Description | None, XmlPath(f'{PATH}/Hist/text()')] = None
    settlement_date: Annotated[date, XmlPath(f'{PATH}/DtMovto/text()')]


class LTR0001E(BaseMessage):
    XML_NAMESPACE: ClassVar[str | None] = XML_NAMESPACE_ERROR

    message_code: Annotated[Literal['LTR0001'], XmlPath(f'{PATH_E}/CodMsg/text()')] = 'LTR0001'
    ltr_control_number: Annotated[LdlControlNumber, XmlPath(f'{PATH_E}/NumCtrlLTR/text()')]
    ltr_ispb: Annotated[Ispb, XmlPath(f'{PATH_E}/ISPBLTR/text()')]
    debtor_institution_ispb: Annotated[Ispb, XmlPath(f'{PATH_E}/ISPBIFDebtd/text()')]
    creditor_institution_ispb: Annotated[Ispb, XmlPath(f'{PATH_E}/ISPBIFCredtd/text()')]
    cnpj: Annotated[Cnpj, XmlPath(f'{PATH_E}/CNPJNLiqdant/text()')]
    participant_identifier: Annotated[ParticipantIdentifier | None, XmlPath(f'{PATH_E}/IdentdPartCamr/text()')] = None
    debtor_branch: Annotated[Branch | None, XmlPath(f'{PATH_E}/AgDebtd/text()')] = None
    debtor_account_number: Annotated[AccountNumber | None, XmlPath(f'{PATH_E}/CtDebtd/text()')] = None
    amount: Annotated[Decimal, XmlPath(f'{PATH_E}/VlrLanc/text()')]
    tipo: Annotated[str, XmlPath(f'{PATH_E}/TpOpLTR/text()')]
    numero: Annotated[str, XmlPath(f'{PATH_E}/NumOpLTR/text()')]
    sub_asset_type: Annotated[AssetType, XmlPath(f'{PATH_E}/SubTpAtv/text()')]
    asset_description: Annotated[AssetDescription | None, XmlPath(f'{PATH_E}/DescAtv/text()')] = None
    description: Annotated[Description | None, XmlPath(f'{PATH_E}/Hist/text()')] = None
    settlement_date: Annotated[date, XmlPath(f'{PATH_E}/DtMovto/text()')]

    general_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH_E}/@CodErro')] = None
    ltr_control_number_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH_E}/NumCtrlLTR/@CodErro')] = None
    ltr_ispb_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH_E}/ISPBLTR/@CodErro')] = None
    debtor_institution_ispb_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH_E}/ISPBIFDebtd/@CodErro')] = None
    creditor_institution_ispb_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH_E}/ISPBIFCredtd/@CodErro')] = (
        None
    )
    cnpj_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH_E}/CNPJNLiqdant/@CodErro')] = None
    participant_identifier_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH_E}/IdentdPartCamr/@CodErro')] = None
    debtor_branch_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH_E}/AgDebtd/@CodErro')] = None
    debtor_account_number_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH_E}/CtDebtd/@CodErro')] = None
    amount_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH_E}/VlrLanc/@CodErro')] = None
    tipo_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH_E}/TpOpLTR/@CodErro')] = None
    numero_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH_E}/NumOpLTR/@CodErro')] = None
    sub_asset_type_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH_E}/SubTpAtv/@CodErro')] = None
    asset_description_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH_E}/DescAtv/@CodErro')] = None
    description_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH_E}/Hist/@CodErro')] = None
    settlement_date_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH_E}/DtMovto/@CodErro')] = None
