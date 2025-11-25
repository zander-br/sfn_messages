from datetime import date, datetime, time
from decimal import Decimal
from typing import Annotated, Literal

from pydantic import model_validator
from validate_docbr import CNPJ, CPF

from sfn_messages.core.models import BaseMessage, XmlPath
from sfn_messages.core.types import (
    AccountNumber,
    AccountType,
    Branch,
    Cnpj,
    Cpf,
    CreditorName,
    CustomerPurpose,
    DebtorName,
    Description,
    InstitutionControlNumber,
    Ispb,
    PersonType,
    Priority,
    StrControlNumber,
    StrSettlementStatus,
    TransactionId,
)

STR0008_PATH = 'DOC/SISMSG/STR0008'
STR0008R1_PATH = 'DOC/SISMSG/STR0008R1'
STR0008R2_PATH = 'DOC/SISMSG/STR0008R2'


class STR0008(BaseMessage):
    message_code: Annotated[Literal['STR0008'], XmlPath(f'{STR0008_PATH}/CodMsg/text()')] = 'STR0008'
    institution_control_number: Annotated[InstitutionControlNumber, XmlPath(f'{STR0008_PATH}/NumCtrlIF/text()')]
    debtor_institution_ispb: Annotated[Ispb, XmlPath(f'{STR0008_PATH}/ISPBIFDebtd/text()')]
    debtor_branch: Annotated[Branch | None, XmlPath(f'{STR0008_PATH}/AgDebtd/text()')] = None
    debtor_account_type: Annotated[AccountType, XmlPath(f'{STR0008_PATH}/TpCtDebtd/text()')]
    debtor_account_number: Annotated[AccountNumber | None, XmlPath(f'{STR0008_PATH}/CtDebtd/text()')] = None
    debtor_payment_account_number: Annotated[AccountNumber | None, XmlPath(f'{STR0008_PATH}/CtPgtoDebtd/text()')] = (
        None
    )
    debtor_type: Annotated[PersonType, XmlPath(f'{STR0008_PATH}/TpPessoaDebtd/text()')]
    debtor_document: Annotated[Cnpj | Cpf, XmlPath(f'{STR0008_PATH}/CNPJ_CPFCliDebtd/text()')]
    debtor_name: Annotated[DebtorName, XmlPath(f'{STR0008_PATH}/NomCliDebtd/text()')]
    creditor_institution_ispb: Annotated[Ispb, XmlPath(f'{STR0008_PATH}/ISPBIFCredtd/text()')]
    creditor_branch: Annotated[Branch | None, XmlPath(f'{STR0008_PATH}/AgCredtd/text()')] = None
    creditor_account_type: Annotated[AccountType, XmlPath(f'{STR0008_PATH}/TpCtCredtd/text()')]
    creditor_account_number: Annotated[AccountNumber | None, XmlPath(f'{STR0008_PATH}/CtCredtd/text()')] = None
    creditor_payment_account_number: Annotated[
        AccountNumber | None, XmlPath(f'{STR0008_PATH}/CtPgtoCredtd/text()')
    ] = None
    creditor_type: Annotated[PersonType, XmlPath(f'{STR0008_PATH}/TpPessoaCredtd/text()')]
    creditor_document: Annotated[Cnpj | Cpf, XmlPath(f'{STR0008_PATH}/CNPJ_CPFCliCredtd/text()')]
    creditor_name: Annotated[CreditorName, XmlPath(f'{STR0008_PATH}/NomCliCredtd/text()')]
    amount: Annotated[Decimal, XmlPath(f'{STR0008_PATH}/VlrLanc/text()')]
    purpose: Annotated[CustomerPurpose, XmlPath(f'{STR0008_PATH}/FinlddCli/text()')]
    transaction_id: Annotated[TransactionId | None, XmlPath(f'{STR0008_PATH}/CodIdentdTransf/text()')] = None
    description: Annotated[Description | None, XmlPath(f'{STR0008_PATH}/Hist/text()')] = None
    scheduled_date: Annotated[date | None, XmlPath(f'{STR0008_PATH}/DtAgendt/text()')] = None
    scheduled_time: Annotated[time | None, XmlPath(f'{STR0008_PATH}/HrAgendt/text()')] = None
    priority: Annotated[Priority | None, XmlPath(f'{STR0008_PATH}/NivelPref/text()')] = None
    settlement_date: Annotated[date, XmlPath(f'{STR0008_PATH}/DtMovto/text()')]

    @model_validator(mode='after')
    def validate_business_rules(self) -> STR0008:
        errors: list[str] = []
        self._validate_party_document(party='debtor', errors=errors)
        self._validate_party_document(party='creditor', errors=errors)
        self._validate_account_requirements(party='debtor', errors=errors)
        self._validate_account_requirements(party='creditor', errors=errors)

        if self.purpose == CustomerPurpose.OTHERS and not self.description:
            errors.append('description is required when purpose is OTHER')

        if errors:
            raise ValueError('; '.join(errors))

        return self

    def _validate_party_document(self, party: str, errors: list[str]) -> None:
        prefix = f'{party}_'

        person_type = getattr(self, prefix + 'type')
        document = getattr(self, prefix + 'document')

        if person_type == PersonType.BUSINESS and not CNPJ().validate(document):
            errors.append(f'Invalid CNPJ for {party}_type BUSINESS')
        if person_type == PersonType.INDIVIDUAL and not CPF().validate(document):
            errors.append(f'Invalid CPF for {party}_type INDIVIDUAL')

    def _validate_account_requirements(self, party: str, errors: list[str]) -> None:
        prefix = f'{party}_'

        account_type = getattr(self, prefix + 'account_type')
        branch = getattr(self, prefix + 'branch')
        account_number = getattr(self, prefix + 'account_number')
        payment_account_number = getattr(self, prefix + 'payment_account_number')

        if account_type == AccountType.PAYMENT:
            if payment_account_number is None:
                errors.append(f'{party}_payment_account_number is required when {party}_account_type is PAYMENT')
            return

        if branch is None:
            errors.append(f'{party}_branch is required when {party}_account_type is not PAYMENT')

        if account_number is None:
            errors.append(f'{party}_account_number is required when {party}_account_type is not PAYMENT')


class STR0008R1(BaseMessage):
    message_code: Annotated[Literal['STR0008R1'], XmlPath(f'{STR0008R1_PATH}/CodMsg/text()')] = 'STR0008R1'
    institution_control_number: Annotated[InstitutionControlNumber, XmlPath(f'{STR0008R1_PATH}/NumCtrlIF/text()')]
    debtor_institution_ispb: Annotated[Ispb, XmlPath(f'{STR0008R1_PATH}/ISPBIFDebtd/text()')]
    str_control_number: Annotated[StrControlNumber, XmlPath(f'{STR0008R1_PATH}/NumCtrlSTR/text()')]
    str_settlement_status: Annotated[StrSettlementStatus, XmlPath(f'{STR0008R1_PATH}/SitLancSTR/text()')]
    provider_timestamp: Annotated[datetime, XmlPath(f'{STR0008R1_PATH}/DtHrSit/text()')]
    settlement_date: Annotated[date, XmlPath(f'{STR0008R1_PATH}/DtMovto/text()')]


class STR0008R2(BaseMessage):
    message_code: Annotated[Literal['STR0008R2'], XmlPath(f'{STR0008R2_PATH}/CodMsg/text()')] = 'STR0008R2'
    str_control_number: Annotated[StrControlNumber, XmlPath(f'{STR0008R2_PATH}/NumCtrlSTR/text()')]
    provider_timestamp: Annotated[datetime, XmlPath(f'{STR0008R2_PATH}/DtHrBC/text()')]
    debtor_institution_ispb: Annotated[Ispb, XmlPath(f'{STR0008R2_PATH}/ISPBIFDebtd/text()')]
    debtor_branch: Annotated[Branch | None, XmlPath(f'{STR0008R2_PATH}/AgDebtd/text()')] = None
    debtor_account_type: Annotated[AccountType, XmlPath(f'{STR0008R2_PATH}/TpCtDebtd/text()')]
    debtor_account_number: Annotated[AccountNumber | None, XmlPath(f'{STR0008R2_PATH}/CtDebtd/text()')] = None
    debtor_payment_account_number: Annotated[AccountNumber | None, XmlPath(f'{STR0008R2_PATH}/CtPgtoDebtd/text()')] = (
        None
    )
    debtor_type: Annotated[PersonType, XmlPath(f'{STR0008R2_PATH}/TpPessoaDebtd/text()')]
    debtor_document: Annotated[Cnpj | Cpf, XmlPath(f'{STR0008R2_PATH}/CNPJ_CPFCliDebtd/text()')]
    debtor_name: Annotated[DebtorName, XmlPath(f'{STR0008R2_PATH}/NomCliDebtd/text()')]
    creditor_institution_ispb: Annotated[Ispb, XmlPath(f'{STR0008R2_PATH}/ISPBIFCredtd/text()')]
    creditor_branch: Annotated[Branch | None, XmlPath(f'{STR0008R2_PATH}/AgCredtd/text()')] = None
    creditor_account_type: Annotated[AccountType, XmlPath(f'{STR0008R2_PATH}/TpCtCredtd/text()')]
    creditor_account_number: Annotated[AccountNumber | None, XmlPath(f'{STR0008R2_PATH}/CtCredtd/text()')] = None
    creditor_payment_account_number: Annotated[
        AccountNumber | None, XmlPath(f'{STR0008R2_PATH}/CtPgtoCredtd/text()')
    ] = None
    creditor_type: Annotated[PersonType, XmlPath(f'{STR0008R2_PATH}/TpPessoaCredtd/text()')]
    creditor_document: Annotated[Cnpj | Cpf, XmlPath(f'{STR0008R2_PATH}/CNPJ_CPFCliCredtd/text()')]
    creditor_name: Annotated[CreditorName, XmlPath(f'{STR0008R2_PATH}/NomCliCredtd/text()')]
    amount: Annotated[Decimal, XmlPath(f'{STR0008R2_PATH}/VlrLanc/text()')]
    purpose: Annotated[CustomerPurpose, XmlPath(f'{STR0008R2_PATH}/FinlddCli/text()')]
    transaction_id: Annotated[TransactionId | None, XmlPath(f'{STR0008R2_PATH}/CodIdentdTransf/text()')] = None
    description: Annotated[Description | None, XmlPath(f'{STR0008R2_PATH}/Hist/text()')] = None
    settlement_date: Annotated[date, XmlPath(f'{STR0008R2_PATH}/DtMovto/text()')]

    @model_validator(mode='after')
    def validate_business_rules(self) -> STR0008R2:
        errors: list[str] = []
        self._validate_party_document(party='debtor', errors=errors)
        self._validate_party_document(party='creditor', errors=errors)
        self._validate_account_requirements(party='debtor', errors=errors)
        self._validate_account_requirements(party='creditor', errors=errors)

        if self.purpose == CustomerPurpose.OTHERS and not self.description:
            errors.append('description is required when purpose is OTHER')

        if errors:
            raise ValueError('; '.join(errors))

        return self

    def _validate_party_document(self, party: str, errors: list[str]) -> None:
        prefix = f'{party}_'

        person_type = getattr(self, prefix + 'type')
        document = getattr(self, prefix + 'document')

        if person_type == PersonType.BUSINESS and not CNPJ().validate(document):
            errors.append(f'Invalid CNPJ for {party}_type BUSINESS')
        if person_type == PersonType.INDIVIDUAL and not CPF().validate(document):
            errors.append(f'Invalid CPF for {party}_type INDIVIDUAL')

    def _validate_account_requirements(self, party: str, errors: list[str]) -> None:
        prefix = f'{party}_'

        account_type = getattr(self, prefix + 'account_type')
        branch = getattr(self, prefix + 'branch')
        account_number = getattr(self, prefix + 'account_number')
        payment_account_number = getattr(self, prefix + 'payment_account_number')

        if account_type == AccountType.PAYMENT:
            if payment_account_number is None:
                errors.append(f'{party}_payment_account_number is required when {party}_account_type is PAYMENT')
            return

        if branch is None:
            errors.append(f'{party}_branch is required when {party}_account_type is not PAYMENT')

        if account_number is None:
            errors.append(f'{party}_account_number is required when {party}_account_type is not PAYMENT')
