from datetime import date, datetime
from typing import Annotated, ClassVar, Literal

from sfn_messages.core.models import BaseMessage, XmlPath
from sfn_messages.core.types import ErrorCode, Ispb, LdlControlNumber, ReconciliationType

PATH = 'DOC/SISMSG/LTR0002'
PATH_R1 = 'DOC/SISMSG/LTR0002R1'
PATH_E = 'DOC/SISMSG/LTR0002E'
XML_NAMESPACE = 'http://www.bcb.gov.br/SPB/LTR0002.xsd'
XML_NAMESPACE_ERROR = 'http://www.bcb.gov.br/SPB/LTR0002E.xsd'


class LTR0002(BaseMessage):
    XML_NAMESPACE: ClassVar[str | None] = XML_NAMESPACE

    message_code: Annotated[Literal['LTR0002'], XmlPath(f'{PATH}/CodMsg/text()')] = 'LTR0002'
    institution_control_number: Annotated[LdlControlNumber, XmlPath(f'{PATH}/NumCtrlIF/text()')]
    institution_ispb: Annotated[Ispb, XmlPath(f'{PATH}/ISPBIF/text()')]
    original_ltr_control_number: Annotated[LdlControlNumber, XmlPath(f'{PATH}/NumCtrlLTROr/text()')]
    ltr_ispb: Annotated[Ispb, XmlPath(f'{PATH_E}/ISPBLTR/text()')]
    institution_datetime: Annotated[datetime, XmlPath(f'{PATH_R1}/DtHrIF/text()')]
    reconciliation_type: Annotated[ReconciliationType, XmlPath(f'{PATH}/TpConf_Divg/text()')]
    settlement_date: Annotated[date, XmlPath(f'{PATH}/DtMovto/text()')]


class LTR0002R1(BaseMessage):
    XML_NAMESPACE: ClassVar[str | None] = XML_NAMESPACE

    message_code: Annotated[Literal['LTR0002R1'], XmlPath(f'{PATH}/CodMsg/text()')] = 'LTR0002R1'
    institution_control_number: Annotated[LdlControlNumber, XmlPath(f'{PATH}/NumCtrlIF/text()')]
    ltr_ispb: Annotated[Ispb, XmlPath(f'{PATH_E}/ISPBLTR/text()')]
    ltr_datetime: Annotated[datetime, XmlPath(f'{PATH_R1}/DtHrLTR/text()')]
    settlement_date: Annotated[date, XmlPath(f'{PATH}/DtMovto/text()')]


class LTR0002E(BaseMessage):
    XML_NAMESPACE: ClassVar[str | None] = XML_NAMESPACE_ERROR

    message_code: Annotated[Literal['LTR0002'], XmlPath(f'{PATH_E}/CodMsg/text()')] = 'LTR0002'
    institution_control_number: Annotated[LdlControlNumber, XmlPath(f'{PATH_E}/NumCtrlIF/text()')]
    institution_ispb: Annotated[Ispb, XmlPath(f'{PATH_E}/ISPBIF/text()')]
    original_ltr_control_number: Annotated[LdlControlNumber, XmlPath(f'{PATH_E}/NumCtrlLTROr/text()')]
    ltr_ispb: Annotated[Ispb, XmlPath(f'{PATH_E}/ISPBLTR/text()')]
    institution_datetime: Annotated[datetime, XmlPath(f'{PATH_R1}/DtHrIF/text()')]
    reconciliation_type: Annotated[ReconciliationType, XmlPath(f'{PATH_E}/TpConf_Divg/text()')]
    settlement_date: Annotated[date, XmlPath(f'{PATH_E}/DtMovto/text()')]

    general_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH_E}/@CodErro')] = None
    institution_control_number_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH_E}/NumCtrlIF/@CodErro')] = None
    institution_ispb_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH_E}/ISPBIF/@CodErro')] = None
    original_ltr_control_number_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH_E}/NumCtrlLTROr/@CodErro')] = (
        None
    )
    ltr_ispb_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH_E}/ISPBLTR/@CodErro')] = None
    institution_datetime_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH_R1}/DtHrIF/@CodErro')] = None
    reconciliation_type_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH_E}/TpConf_Divg/@CodErro')] = None
    settlement_date_error_code: Annotated[ErrorCode | None, XmlPath(f'{PATH_E}/DtMovto/@CodErro')] = None
