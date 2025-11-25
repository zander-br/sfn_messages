from datetime import date, time
from decimal import Decimal
from typing import Annotated, Literal

from sfn_messages.core.models import BaseMessage, XmlPath
from sfn_messages.core.types import Branch, Description, InstitutionControlNumber, Ispb, Priority, TransactionId

from .types import InstitutionPurpose

PATH = 'DOC/SISMSG/STR0004'


class STR0004(BaseMessage):
    message_code: Annotated[Literal['STR0004'], XmlPath(f'{PATH}/CodMsg/text()')] = 'STR0004'
    institution_control_number: Annotated[InstitutionControlNumber, XmlPath(f'{PATH}/NumCtrlIF/text()')]
    debtor_institution_ispb: Annotated[Ispb, XmlPath(f'{PATH}/ISPBIFDebtd/text()')]
    creditor_institution_ispb: Annotated[Ispb, XmlPath(f'{PATH}/ISPBIFCredtd/text()')]
    creditor_branch: Annotated[Branch | None, XmlPath(f'{PATH}/AgCredtd/text()')] = None
    purpose: Annotated[InstitutionPurpose, XmlPath(f'{PATH}/FinlddIF/text()')]
    transaction_id: Annotated[TransactionId | None, XmlPath(f'{PATH}/CodIdentdTransf/text()')] = None
    amount: Annotated[Decimal, XmlPath(f'{PATH}/VlrLanc/text()')]
    description: Annotated[Description, XmlPath(f'{PATH}/Hist/text()')]
    scheduled_date: Annotated[date | None, XmlPath(f'{PATH}/DtAgendt/text()')] = None
    scheduled_time: Annotated[time | None, XmlPath(f'{PATH}/HrAgendt/text()')] = None
    priority: Annotated[Priority | None, XmlPath(f'{PATH}/NivelPref/text()')] = None
    settlement_date: Annotated[date, XmlPath(f'{PATH}/DtMovto/text()')]
