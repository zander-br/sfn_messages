from datetime import date, datetime
from typing import Annotated, ClassVar, Literal

from sfn_messages.core.models import BaseMessage, XmlPath
from sfn_messages.core.types import ErrorCode, InstitutionControlNumber, Ispb

PATH = 'DOC/SISMSG/GEN0008'
PATH_R1 = 'DOC/SISMSG/GEN0008R1'
PATH_E = 'DOC/SISMSG/GEN0008'
XML_NAMESPACE = 'http://www.bcb.gov.br/GEN/GEN0008.xsd'
XML_NAMESPACE_ERROR = 'http://www.bcb.gov.br/GEN/GEN0008E.xsd'


class GEN0008(BaseMessage):
    XML_NAMESPACE: ClassVar[str | None] = XML_NAMESPACE

    message_code: Annotated[Literal['GEN0008'], XmlPath(f'{PATH}/CodMsg/text()')] = 'GEN0008'
    institution_control_number: Annotated[InstitutionControlNumber, XmlPath(f'{PATH}/NumCtrlIF/text()')]
    institution_ispb: Annotated[Ispb, XmlPath(f'{PATH}/ISPBIF/text()')]
    instituition_certificate: Annotated[Ispb, XmlPath(f'{PATH}/ISPBIFCertif/text()')]
    settlement_date: Annotated[date, XmlPath(f'{PATH}/DtMovto/text()')]


class GEN0008R1(BaseMessage):
    XML_NAMESPACE: ClassVar[str | None] = XML_NAMESPACE

    message_code: Annotated[Literal['GEN0008R1'], XmlPath(f'{PATH_R1}/CodMsg/text()')] = 'GEN0008R1'
    institution_control_number: Annotated[InstitutionControlNumber, XmlPath(f'{PATH_R1}/NumCtrlIF/text()')]
    institution_ispb: Annotated[Ispb, XmlPath(f'{PATH_R1}/ISPBIF/text()')]
    instituition_certificate: Annotated[Ispb, XmlPath(f'{PATH_R1}/ISPBIFCertif/text()')]
    settlement_date: Annotated[date | None, XmlPath(f'{PATH_R1}/DtMovto/text()')] = None
    vendor_timestamp: Annotated[datetime, XmlPath(f'{PATH_R1}/DtHrBC/text()')]


class GEN0008E(BaseMessage):
    XML_NAMESPACE: ClassVar[str | None] = XML_NAMESPACE_ERROR

    message_code: Annotated[Literal['GEN0008E'], XmlPath(f'{PATH_E}/CodMsg/text()')] = 'GEN0008E'
    institution_control_number: Annotated[InstitutionControlNumber | None, XmlPath(f'{PATH_E}/NumCtrlIF/text()')] = (
        None
    )
    institution_ispb: Annotated[Ispb | None, XmlPath(f'{PATH_E}/ISPBIF/text()')] = None
    instituition_certificate: Annotated[Ispb | None, XmlPath(f'{PATH_E}/ISPBIFCertif/text()')] = None
    settlement_date: Annotated[date | None, XmlPath(f'{PATH_E}/DtMovto/text()')] = None

    general_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH_E}/@CodErro')] = None
    institution_control_number_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH_E}/NumCtrlIF/@CodErro')] = None
    institution_ispb_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH_E}/ISPBIF/@CodErro')] = None
    instituition_certificate_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH_E}/ISPBIFCertif/@CodErro')] = None
    settlement_date_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH_E}/DtMovto/@CodErro')] = None
