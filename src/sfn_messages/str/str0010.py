from datetime import date, time
from decimal import Decimal
from typing import Annotated, Literal

from sfn_messages.core.models import BaseMessage, XmlPath
from sfn_messages.core.types import (
    Description,
    InstitutionControlNumber,
    Ispb,
    Priority,
    StrControlNumber,
    TransferReturnReason,
)

PATH = 'DOC/SISMSG/STR0010'


class STR0010(BaseMessage):
    message_code: Annotated[Literal['STR0010'], XmlPath(f'{PATH}/CodMsg/text()')] = 'STR0010'
    institution_control_number: Annotated[InstitutionControlNumber, XmlPath(f'{PATH}/NumCtrlIF/text()')]
    debtor_institution_ispb: Annotated[Ispb, XmlPath(f'{PATH}/ISPBIFDebtd/text()')]
    creditor_institution_ispb: Annotated[Ispb, XmlPath(f'{PATH}/ISPBIFCredtd/text()')]
    amount: Annotated[Decimal, XmlPath(f'{PATH}/VlrLanc/text()')]
    transfer_return_reason: Annotated[TransferReturnReason, XmlPath(f'{PATH}/CodDevTransf/text()')]
    original_str_control_number: Annotated[StrControlNumber, XmlPath(f'{PATH}/NumCtrlSTR/text()')]
    description: Annotated[Description | None, XmlPath(f'{PATH}/Hist/text()')] = None
    scheduled_date: Annotated[date | None, XmlPath(f'{PATH}/DtAgendt/text()')] = None
    scheduled_time: Annotated[time | None, XmlPath(f'{PATH}/HrAgendt/text()')] = None
    priority: Annotated[Priority | None, XmlPath(f'{PATH}/NivelPref/text()')] = None
    settlement_date: Annotated[date, XmlPath(f'{PATH}/DtMovto/text()')]
