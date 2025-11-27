from decimal import Decimal

import pytest
from pydantic import BaseModel, ValidationError

from sfn_messages.core.types import (
    AccountNumber,
    AccountType,
    Amount,
    Branch,
    Cnpj,
    Cpf,
    CreditContractNumber,
    CreditorName,
    CustomerPurpose,
    DebtorName,
    Description,
    InstitutionControlNumber,
    Ispb,
    OperationNumber,
    PersonType,
    Priority,
    SenderName,
    StrControlNumber,
    StrSettlementStatus,
    SystemDomain,
    TransactionId,
    TransferReturnReason,
)


class AccountNumberModel(BaseModel):
    account_number: AccountNumber


class AmountModel(BaseModel):
    amount: Amount


class BranchModel(BaseModel):
    branch: Branch


class CnpjModel(BaseModel):
    cnpj: Cnpj


class CpfModel(BaseModel):
    cpf: Cpf


class DescriptionModel(BaseModel):
    description: Description


class SenderNameModel(BaseModel):
    sender_name: SenderName


class DebtorNameModel(BaseModel):
    debtor_name: DebtorName


class CreditorNameModel(BaseModel):
    creditor_name: CreditorName


class CreditContractNumberModel(BaseModel):
    credit_contract_number: CreditContractNumber


class InstitutionControlNumberModel(BaseModel):
    institution_control_number: InstitutionControlNumber


class IspbModel(BaseModel):
    ispb: Ispb


class OperationNumberModel(BaseModel):
    operation_number: OperationNumber


class TransactionIdModel(BaseModel):
    transaction_id: TransactionId


class StrControlNumberModel(BaseModel):
    str_control_number: StrControlNumber


@pytest.mark.parametrize(
    'account_number',
    [
        '1',  # minimum valid (1 digit, not zero)
        '9',  # single digit, upper limit
        '12',  # 2 digits
        '999',  # 3 digits
        '123456',  # mid-range
        '1234567890123',  # max length (13 digits)
        '9876543210123',  # another 13-digit value
    ],
)
def test_account_number_accepts_valid_values(account_number: str) -> None:
    model = AccountNumberModel(account_number=account_number)
    assert model.account_number == account_number


@pytest.mark.parametrize(
    'account_number',
    [
        '0',  # cannot start with 0
        '00',  # still invalid
        '0123',  # leading zero not allowed
        '',  # empty string
        '12345678901234',  # too long (14 digits)
        '-123',  # sign not allowed
        '+5',  # sign not allowed
        '1.23',  # dot not allowed
        '1 23',  # space not allowed
    ],
)
def test_account_number_rejects_invalid_values(account_number: str) -> None:
    with pytest.raises(ValidationError) as exc:
        AccountNumberModel(account_number=account_number)
    assert "String should match pattern '^[1-9][0-9]{0,12}$'" in str(exc.value)


@pytest.mark.parametrize(
    'branch',
    [
        '0',  # minimum allowed length (1 digit)
        '5',  # single digit, generic valid case
        '09',  # leading zero, 2 digits
        '42',  # normal 2-digit value
        '123',  # 3-digit valid value
        '007',  # 3 digits with leading zeros
        '9999',  # maximum allowed length (4 digits)
        '0001',  # 4 digits with leading zeros
    ],
)
def test_branch_accepts_valid_values(branch: str) -> None:
    model = BranchModel(branch=branch)
    assert model.branch == branch


def test_branch_accepts_whitespace() -> None:
    model = BranchModel(branch='  007  ')
    assert model.branch == '007'


@pytest.mark.parametrize(
    'branch',
    [
        '',  # empty string (no digits)
        '12345',  # too many digits (5 digits)
        'abcd',  # non-numeric characters
        '12a3',  # mixed digits and letters
        '-123',  # negative sign not allowed
        '12 34',  # internal space
        '01.2',  # decimal point not allowed
        '💥',  # unicode symbol, non-digit
    ],
)
def test_branch_rejects_invalid_values(branch: str) -> None:
    with pytest.raises(ValidationError) as exc:
        BranchModel(branch=branch)
    assert "String should match pattern '^[0-9]{1,4}$'" in str(exc.value)


@pytest.mark.parametrize(
    'creditor_name',
    [
        'A' * 1,
        'John Doe',
        'A' * 80,
    ],
)
def test_creditor_name_accepts_valid_values(creditor_name: str) -> None:
    model = CreditorNameModel(creditor_name=creditor_name)
    assert model.creditor_name == creditor_name


def test_creditor_name_accepts_whitespace() -> None:
    model = CreditorNameModel(creditor_name='  Jane Smith  ')
    assert model.creditor_name == 'Jane Smith'


@pytest.mark.parametrize(
    'creditor_name',
    [
        'A' * 81,  # Too long
    ],
)
def test_creditor_name_rejects_invalid_values(creditor_name: str) -> None:
    with pytest.raises(ValidationError) as exc:
        CreditorNameModel(creditor_name=creditor_name)
    assert 'String should have at most 80 characters' in str(exc.value)


@pytest.mark.parametrize(
    'description',
    [
        'A' * 1,
        'This is a valid description.',
        'A' * 200,
    ],
)
def test_description_accepts_valid_values(description: str) -> None:
    model = DescriptionModel(description=description)
    assert model.description == description


def test_description_accepts_whitespace() -> None:
    model = DescriptionModel(description='  Valid description with spaces.  ')
    assert model.description == 'Valid description with spaces.'


@pytest.mark.parametrize(
    'description',
    [
        'A' * 201,  # Too long
    ],
)
def test_description_rejects_invalid_values(description: str) -> None:
    with pytest.raises(ValidationError) as exc:
        DescriptionModel(description=description)
    assert 'String should have at most 200 characters' in str(exc.value)


@pytest.mark.parametrize(
    'debtor_name',
    [
        'A' * 1,
        'John Doe',
        'A' * 80,
    ],
)
def test_debtor_name_accepts_valid_values(debtor_name: str) -> None:
    model = DebtorNameModel(debtor_name=debtor_name)
    assert model.debtor_name == debtor_name


def test_debtor_name_accepts_whitespace() -> None:
    model = DebtorNameModel(debtor_name='  Jane Smith  ')
    assert model.debtor_name == 'Jane Smith'


@pytest.mark.parametrize(
    'debtor_name',
    [
        'A' * 81,  # Too long
    ],
)
def test_debtor_name_rejects_invalid_values(debtor_name: str) -> None:
    with pytest.raises(ValidationError) as exc:
        DebtorNameModel(debtor_name=debtor_name)
    assert 'String should have at most 80 characters' in str(exc.value)


@pytest.mark.parametrize(
    'sender_name',
    [
        'A' * 1,
        'John Doe',
        'A' * 80,
    ],
)
def test_sender_name_accepts_valid_values(sender_name: str) -> None:
    model = SenderNameModel(sender_name=sender_name)
    assert model.sender_name == sender_name


def test_sender_name_accepts_whitespace() -> None:
    model = SenderNameModel(sender_name='  Jane Smith  ')
    assert model.sender_name == 'Jane Smith'


@pytest.mark.parametrize(
    'sender_name',
    [
        'A' * 81,  # Too long
    ],
)
def test_sender_name_rejects_invalid_values(sender_name: str) -> None:
    with pytest.raises(ValidationError) as exc:
        SenderNameModel(sender_name=sender_name)
    assert 'String should have at most 80 characters' in str(exc.value)


@pytest.mark.parametrize(
    'institution_control_number',
    [
        'A' * 1,
        '1234567890',
        'ABCDEFGHIJ',
        'A1B2C3D4E5F6G7H8I9J0',
    ],
)
def test_institution_control_number_accepts_valid_values(institution_control_number: str) -> None:
    model = InstitutionControlNumberModel(institution_control_number=institution_control_number)
    assert model.institution_control_number == institution_control_number


def test_institution_control_number_accepts_whitespace() -> None:
    model = InstitutionControlNumberModel(institution_control_number='  ABC123  ')
    assert model.institution_control_number == 'ABC123'


@pytest.mark.parametrize(
    'control_number',
    [
        '',  # Too short
        'A' * 21,  # Too long,
        '  ',  # Only whitespace
    ],
)
def test_institution_control_number_rejects_invalid_values(control_number: str) -> None:
    with pytest.raises(ValidationError) as exc:
        InstitutionControlNumberModel(institution_control_number=control_number)
    assert 'String should have at least 1 character' in str(
        exc.value
    ) or 'String should have at most 20 characters' in str(exc.value)


@pytest.mark.parametrize(
    'ispb',
    [
        '12345678',
        'ABCDEFGH',
        'A1B2C3D4',
        '87654321',
        'HGFEDCBA',
        '4D3C2B1A',
    ],
)
def test_ispb_accepts_valid_values(ispb: str) -> None:
    model = IspbModel(ispb=ispb)
    assert model.ispb == ispb


def test_ispb_accepts_whitespace_and_case_insensitivity() -> None:
    model = IspbModel(ispb='  a1b2c3d4  ')
    assert model.ispb == 'A1B2C3D4'


@pytest.mark.parametrize(
    'ispb',
    [
        '1234567',  # Too short
        '123456789',  # Too long
        '1234 5678',  # Contains space
        '1234-5678',  # Contains special character
        '1234567!',  # Contains special character
        '12345@678',  # Contains special character
        '1234\n5678',  # Contains newline
    ],
)
def test_ispb_rejects_invalid_values(ispb: str) -> None:
    with pytest.raises(ValidationError) as exc:
        IspbModel(ispb=ispb)
    assert "String should match pattern '^[0-9A-Za-z]{8}$'" in str(exc.value)


@pytest.mark.parametrize(
    'operation_number',
    [
        'ABCDEFGH1234567890123',
        '1234567A1234567890123',
        'A1B2C3D41234567890123',
        'HGFEDCBA9876543210123',
        '4D3C2B1A0000000000000',
    ],
)
def test_operation_number_accepts_valid_values(operation_number: str) -> None:
    model = OperationNumberModel(operation_number=operation_number)
    assert model.operation_number == operation_number


def test_operation_number_accepts_whitespace() -> None:
    model = OperationNumberModel(operation_number='  ABCDEFGH1234567890123  ')
    assert model.operation_number == 'ABCDEFGH1234567890123'


@pytest.mark.parametrize(
    'operation_number',
    [
        'ABCDEFGH123456789012',  # Too short
        'ABCDEFGH12345678901234',  # Too long
        'ABCDEFGH 1234567890123',  # Contains space
        'ABCDEFGH-1234567890123',  # Contains special character
        'ABCDEFGH12345!67890123',  # Contains special character
        'ABCDEFGH1234@67890123',  # Contains special character
        'ABCDEFGH1234\n67890123',  # Contains newline
    ],
)
def test_operation_number_rejects_invalid_values(operation_number: str) -> None:
    with pytest.raises(ValidationError) as exc:
        OperationNumberModel(operation_number=operation_number)
    assert "String should match pattern '^[0-9A-Z]{8}[0-9]{13}$'" in str(exc.value)


@pytest.mark.parametrize(
    ('input_value', 'expected_enum'),
    [
        ('CURRENT', AccountType.CURRENT),
        ('DEPOSIT', AccountType.DEPOSIT),
        ('OVERDRAFT', AccountType.OVERDRAFT),
        ('PAYMENT', AccountType.PAYMENT),
        ('SAVINGS', AccountType.SAVINGS),
    ],
)
def test_account_type_accepts_exact_values(input_value: str, expected_enum: AccountType) -> None:
    assert AccountType(input_value) is expected_enum


@pytest.mark.parametrize(
    ('input_value', 'expected_enum'),
    [
        ('current', AccountType.CURRENT),
        ('deposit', AccountType.DEPOSIT),
        ('overdraft', AccountType.OVERDRAFT),
        ('payment', AccountType.PAYMENT),
        ('savings', AccountType.SAVINGS),
    ],
)
def test_account_type_accepts_case_insensitive_values(input_value: str, expected_enum: AccountType) -> None:
    assert AccountType(input_value) is expected_enum


@pytest.mark.parametrize(
    ('input_value', 'expected_enum'),
    [
        (AccountType.CURRENT, 'CC'),
        (AccountType.DEPOSIT, 'CD'),
        (AccountType.OVERDRAFT, 'CG'),
        (AccountType.PAYMENT, 'PG'),
        (AccountType.SAVINGS, 'PP'),
    ],
)
def test_account_type_values_to_xml_value(input_value: AccountType, expected_enum: str) -> None:
    assert input_value.to_xml_value() == expected_enum


@pytest.mark.parametrize(
    ('input_value', 'expected_enum'),
    [
        ('CC', AccountType.CURRENT),
        ('CD', AccountType.DEPOSIT),
        ('CG', AccountType.OVERDRAFT),
        ('PG', AccountType.PAYMENT),
        ('PP', AccountType.SAVINGS),
    ],
)
def test_account_type_values_from_xml_value(input_value: str, expected_enum: AccountType) -> None:
    assert AccountType.from_xml_value(input_value) is expected_enum


@pytest.mark.parametrize(
    'invalid_value',
    [
        'CURR',  # Invalid abbreviation
        'DEP',  # Invalid abbreviation
        'OVER',  # Invalid abbreviation
        'PAY',  # Invalid abbreviation
        'SAVE',  # Invalid abbreviation
        '123',  # Numeric string
    ],
)
def test_account_type_rejects_invalid_value(invalid_value: str) -> None:
    with pytest.raises(ValueError, match=invalid_value):
        AccountType(invalid_value)


@pytest.mark.parametrize(
    ('input_value', 'expected_enum'),
    [
        ('BUSINESS', PersonType.BUSINESS),
        ('INDIVIDUAL', PersonType.INDIVIDUAL),
    ],
)
def test_person_type_accepts_exact_values(input_value: str, expected_enum: PersonType) -> None:
    assert PersonType(input_value) is expected_enum


@pytest.mark.parametrize(
    ('input_value', 'expected_enum'),
    [
        ('business', PersonType.BUSINESS),
        ('individual', PersonType.INDIVIDUAL),
    ],
)
def test_person_type_accepts_case_insensitive_values(input_value: str, expected_enum: PersonType) -> None:
    assert PersonType(input_value) is expected_enum


@pytest.mark.parametrize(
    ('input_value', 'expected_enum'),
    [
        (PersonType.BUSINESS, 'J'),
        (PersonType.INDIVIDUAL, 'F'),
    ],
)
def test_person_type_values_to_xml_value(input_value: PersonType, expected_enum: str) -> None:
    assert input_value.to_xml_value() == expected_enum


@pytest.mark.parametrize(
    'invalid_value',
    [
        'BUS',  # Invalid abbreviation
        'IND',  # Invalid abbreviation
        '123',  # Numeric string
    ],
)
def test_person_type_rejects_invalid_value(invalid_value: str) -> None:
    with pytest.raises(ValueError, match=invalid_value):
        PersonType(invalid_value)


@pytest.mark.parametrize(
    ('input_value', 'expected_enum'),
    [
        ('SPB01', SystemDomain.SPB01),
        ('SPB02', SystemDomain.SPB02),
        ('MES01', SystemDomain.MES01),
        ('MES02', SystemDomain.MES02),
        ('MES03', SystemDomain.MES03),
    ],
)
def test_system_domain_accepts_exact_values(input_value: str, expected_enum: SystemDomain) -> None:
    assert SystemDomain(input_value) is expected_enum


@pytest.mark.parametrize(
    ('input_value', 'expected_enum'),
    [
        ('spb01', SystemDomain.SPB01),
        ('spb02', SystemDomain.SPB02),
        ('mes01', SystemDomain.MES01),
        ('mes02', SystemDomain.MES02),
        ('mes03', SystemDomain.MES03),
    ],
)
def test_system_domain_accepts_case_insensitive_values(input_value: str, expected_enum: SystemDomain) -> None:
    assert SystemDomain(input_value) is expected_enum


@pytest.mark.parametrize(
    ('input_value', 'expected_enum'),
    [
        (SystemDomain.SPB01, 'SPB01'),
        (SystemDomain.SPB02, 'SPB02'),
        (SystemDomain.MES01, 'MES01'),
        (SystemDomain.MES02, 'MES02'),
        (SystemDomain.MES03, 'MES03'),
    ],
)
def test_system_domain_values_to_xml_value(input_value: SystemDomain, expected_enum: str) -> None:
    assert input_value.to_xml_value() == expected_enum


@pytest.mark.parametrize(
    ('input_value', 'expected_enum'),
    [
        ('SPB01', SystemDomain.SPB01),
        ('SPB02', SystemDomain.SPB02),
        ('MES01', SystemDomain.MES01),
        ('MES02', SystemDomain.MES02),
        ('MES03', SystemDomain.MES03),
    ],
)
def test_system_domain_values_from_xml_value(input_value: str, expected_enum: SystemDomain) -> None:
    assert SystemDomain(input_value) is expected_enum


@pytest.mark.parametrize(
    'invalid_value',
    [
        'SPB0',  # Too short
        'SPB001',  # Too long
        'MES04',  # Invalid MES code
        'ABC01',  # Invalid prefix
    ],
)
def test_system_domain_rejects_invalid_value(invalid_value: str) -> None:
    with pytest.raises(ValueError, match=invalid_value):
        SystemDomain(invalid_value)


@pytest.mark.parametrize(
    ('input_value', 'expected_enum'),
    [
        ('TAX_PAYMENT', CustomerPurpose.TAX_PAYMENT),
        ('CREDIT_IN_ACCOUNT', CustomerPurpose.CREDIT_IN_ACCOUNT),
        ('JUDICIAL_DEPOSIT', CustomerPurpose.JUDICIAL_DEPOSIT),
        ('ALIMONY', CustomerPurpose.ALIMONY),
        ('CREDIT_ASSIGNMENT_CLIENT', CustomerPurpose.CREDIT_ASSIGNMENT_CLIENT),
        ('CREDIT_ASSIGNMENT_FIDC', CustomerPurpose.CREDIT_ASSIGNMENT_FIDC),
        ('CONTRACTUAL_CASHFLOW_CLIENT', CustomerPurpose.CONTRACTUAL_CASHFLOW_CLIENT),
        ('ADVANCE_CASHFLOW_CLIENT', CustomerPurpose.ADVANCE_CASHFLOW_CLIENT),
        ('CREDIT_ADJUSTMENTS', CustomerPurpose.CREDIT_ADJUSTMENTS),
        ('PAYMENT_BROKERS', CustomerPurpose.PAYMENT_BROKERS),
        ('TRANSFER_SAME_OWNER', CustomerPurpose.TRANSFER_SAME_OWNER),
        ('CREDIT_TO_INVESTOR', CustomerPurpose.CREDIT_TO_INVESTOR),
        ('DEBIT_FROM_INVESTOR', CustomerPurpose.DEBIT_FROM_INVESTOR),
        ('CREDIT_OPERATIONS_CLIENT', CustomerPurpose.CREDIT_OPERATIONS_CLIENT),
        ('FINANCIAL_REDEMPTION_CLIENT', CustomerPurpose.FINANCIAL_REDEMPTION_CLIENT),
        ('FINANCIAL_INVESTMENT_SENDER', CustomerPurpose.FINANCIAL_INVESTMENT_SENDER),
        ('PAYMENT_BANK_SLIP_REGISTRY', CustomerPurpose.PAYMENT_BANK_SLIP_REGISTRY),
        ('TIR_PAYMENT_PIX', CustomerPurpose.TIR_PAYMENT_PIX),
        ('CREDIT_ASSIGNMENT_REPURCHASE_CLIENT', CustomerPurpose.CREDIT_ASSIGNMENT_REPURCHASE_CLIENT),
        ('CREDIT_ASSIGNMENT_REPURCHASE_FIDC', CustomerPurpose.CREDIT_ASSIGNMENT_REPURCHASE_FIDC),
        ('SERVICE_FEE_PAYMENT', CustomerPurpose.SERVICE_FEE_PAYMENT),
        ('FGCOOP_FUND_COLLECTION', CustomerPurpose.FGCOOP_FUND_COLLECTION),
        ('FGCOOP_REFUND', CustomerPurpose.FGCOOP_REFUND),
        ('FGTS_EMERGENCY_WITHDRAWAL', CustomerPurpose.FGTS_EMERGENCY_WITHDRAWAL),
        ('CONSUMER_CREDIT_INCENTIVE', CustomerPurpose.CONSUMER_CREDIT_INCENTIVE),
        ('REPAYMENT_REGISTRY_LIQUIDATION', CustomerPurpose.REPAYMENT_REGISTRY_LIQUIDATION),
        ('EMERGENCY_AID', CustomerPurpose.EMERGENCY_AID),
        ('FINANCIAL_SETTLEMENT_CARD', CustomerPurpose.FINANCIAL_SETTLEMENT_CARD),
        ('BEM_EMPLOYMENT_BENEFIT', CustomerPurpose.BEM_EMPLOYMENT_BENEFIT),
        ('MUNICIPAL_TAXES_ISS_LCP157', CustomerPurpose.MUNICIPAL_TAXES_ISS_LCP157),
        ('MUNICIPAL_TAXES_ISS_THIRD', CustomerPurpose.MUNICIPAL_TAXES_ISS_THIRD),
        ('OPERATION_CANCELLATION', CustomerPurpose.OPERATION_CANCELLATION),
        ('FINANCIAL_AGENT_FEE', CustomerPurpose.FINANCIAL_AGENT_FEE),
        ('OPERATOR_SETTLEMENT_CREDITOR', CustomerPurpose.OPERATOR_SETTLEMENT_CREDITOR),
        ('HOUSING_INSURANCE_SFH', CustomerPurpose.HOUSING_INSURANCE_SFH),
        ('SPVAT_COLLECTION_TRANSFER', CustomerPurpose.SPVAT_COLLECTION_TRANSFER),
        ('FDS_OPERATIONS', CustomerPurpose.FDS_OPERATIONS),
        ('PUBLIC_SERVICE_PAYMENT', CustomerPurpose.PUBLIC_SERVICE_PAYMENT),
        ('INTERNATIONAL_TRANSFER_REAIS', CustomerPurpose.INTERNATIONAL_TRANSFER_REAIS),
        ('FUTURES_MARKET_ADJUSTMENT', CustomerPurpose.FUTURES_MARKET_ADJUSTMENT),
        ('BNDES_VALUE_TRANSFER', CustomerPurpose.BNDES_VALUE_TRANSFER),
        ('BNDES_COMMITMENT_SETTLEMENT', CustomerPurpose.BNDES_COMMITMENT_SETTLEMENT),
        ('STOCK_MARKET_OPERATIONS', CustomerPurpose.STOCK_MARKET_OPERATIONS),
        ('STOCK_INDEX_CONTRACTS', CustomerPurpose.STOCK_INDEX_CONTRACTS),
        ('NON_INTERBANK_FOREX', CustomerPurpose.NON_INTERBANK_FOREX),
        ('FIXED_VARIABLE_OPERATIONS', CustomerPurpose.FIXED_VARIABLE_OPERATIONS),
        ('INTERBANK_FOREX_NO_RESERVE', CustomerPurpose.INTERBANK_FOREX_NO_RESERVE),
        ('PAYMENT_FINAL_RECIPIENT', CustomerPurpose.PAYMENT_FINAL_RECIPIENT),
        ('ADMINISTRATION_FEE', CustomerPurpose.ADMINISTRATION_FEE),
        ('JUDICIAL_AGREEMENT_PAYMENT', CustomerPurpose.JUDICIAL_AGREEMENT_PAYMENT),
        ('CONSIGNED_LOAN_SETTLEMENT', CustomerPurpose.CONSIGNED_LOAN_SETTLEMENT),
        ('SCHOLARSHIP_PAYMENT', CustomerPurpose.SCHOLARSHIP_PAYMENT),
        ('DIVIDEND_PAYMENT', CustomerPurpose.DIVIDEND_PAYMENT),
        ('COOPERATIVE_REMUNERATION', CustomerPurpose.COOPERATIVE_REMUNERATION),
        ('INCOME_TAX_REFUND', CustomerPurpose.INCOME_TAX_REFUND),
        ('TREASURY_BANK_ORDER', CustomerPurpose.TREASURY_BANK_ORDER),
        ('BACEN_FINES_PAYMENT', CustomerPurpose.BACEN_FINES_PAYMENT),
        ('TAX_REFUND_RFB', CustomerPurpose.TAX_REFUND_RFB),
        ('CLERICAL_REMUNERATION', CustomerPurpose.CLERICAL_REMUNERATION),
        ('INTEREST_ON_EQUITY', CustomerPurpose.INTEREST_ON_EQUITY),
        ('YIELD_AMORTIZATION', CustomerPurpose.YIELD_AMORTIZATION),
        ('SERVICE_FEE', CustomerPurpose.SERVICE_FEE),
        ('CHECK_PAYMENT_NON_ACCOUNT_HOLDER', CustomerPurpose.CHECK_PAYMENT_NON_ACCOUNT_HOLDER),
        ('GUARANTEED_SECURITIES_INTEREST', CustomerPurpose.GUARANTEED_SECURITIES_INTEREST),
        ('REVERSAL_OR_REFUND', CustomerPurpose.REVERSAL_OR_REFUND),
        ('TRANSPORT_VOUCHER_PAYMENT', CustomerPurpose.TRANSPORT_VOUCHER_PAYMENT),
        ('SALARY_PAYMENT', CustomerPurpose.SALARY_PAYMENT),
        ('SIMPLES_NACIONAL', CustomerPurpose.SIMPLES_NACIONAL),
        ('FUNDEB_TRANSFER', CustomerPurpose.FUNDEB_TRANSFER),
        ('CENTRALIZED_AGREEMENT_TRANSFER', CustomerPurpose.CENTRALIZED_AGREEMENT_TRANSFER),
        ('SPONSORSHIP_TAX_INCENTIVE', CustomerPurpose.SPONSORSHIP_TAX_INCENTIVE),
        ('DONATION_TAX_INCENTIVE', CustomerPurpose.DONATION_TAX_INCENTIVE),
        ('NONBANK_TO_LIQUIDATION_TRANSFER', CustomerPurpose.NONBANK_TO_LIQUIDATION_TRANSFER),
        ('TERMINATION_PAYMENT', CustomerPurpose.TERMINATION_PAYMENT),
        ('SUPPLIER_PAYMENT', CustomerPurpose.SUPPLIER_PAYMENT),
        ('FIXED_VARIABLE_EXPENSE_REIMBURSEMENT', CustomerPurpose.FIXED_VARIABLE_EXPENSE_REIMBURSEMENT),
        ('INSURANCE_PRIZE_REFUND', CustomerPurpose.INSURANCE_PRIZE_REFUND),
        ('INSURANCE_CLAIM_PAYMENT', CustomerPurpose.INSURANCE_CLAIM_PAYMENT),
        ('CO_INSURANCE_PREMIUM', CustomerPurpose.CO_INSURANCE_PREMIUM),
        ('CO_INSURANCE_CLAIM_PAYMENT', CustomerPurpose.CO_INSURANCE_CLAIM_PAYMENT),
        ('REINSURANCE_PREMIUM', CustomerPurpose.REINSURANCE_PREMIUM),
        ('REINSURANCE_CLAIM_PAYMENT', CustomerPurpose.REINSURANCE_CLAIM_PAYMENT),
        ('REINSURANCE_CLAIM_REFUND', CustomerPurpose.REINSURANCE_CLAIM_REFUND),
        ('CLAIM_EXPENSE_PAYMENT', CustomerPurpose.CLAIM_EXPENSE_PAYMENT),
        ('INSPECTION_PAYMENT', CustomerPurpose.INSPECTION_PAYMENT),
        ('CAPITALIZATION_REDEMPTION', CustomerPurpose.CAPITALIZATION_REDEMPTION),
        ('CAPITALIZATION_DRAW', CustomerPurpose.CAPITALIZATION_DRAW),
        ('CAPITALIZATION_MONTHLY_REFUND', CustomerPurpose.CAPITALIZATION_MONTHLY_REFUND),
        ('PENSION_CONTRIBUTION_REFUND', CustomerPurpose.PENSION_CONTRIBUTION_REFUND),
        ('PENSION_PECCULUM_BENEFIT', CustomerPurpose.PENSION_PECCULUM_BENEFIT),
        ('PENSION_PENSION_BENEFIT', CustomerPurpose.PENSION_PENSION_BENEFIT),
        ('PENSION_RETIREMENT_BENEFIT', CustomerPurpose.PENSION_RETIREMENT_BENEFIT),
        ('PENSION_REDEMPTION', CustomerPurpose.PENSION_REDEMPTION),
        ('BROKERAGE_COMMISSION', CustomerPurpose.BROKERAGE_COMMISSION),
        ('INSURANCE_PENSION_TRANSFER', CustomerPurpose.INSURANCE_PENSION_TRANSFER),
        ('FEES_PAYMENT', CustomerPurpose.FEES_PAYMENT),
        ('RENT_CONDOMINIUM', CustomerPurpose.RENT_CONDOMINIUM),
        ('INVOICE_BILLS_PAYMENT', CustomerPurpose.INVOICE_BILLS_PAYMENT),
        ('SCHOOL_FEE_PAYMENT', CustomerPurpose.SCHOOL_FEE_PAYMENT),
        ('FOREIGN_CURRENCY_PURCHASE', CustomerPurpose.FOREIGN_CURRENCY_PURCHASE),
        ('OTHERS', CustomerPurpose.OTHERS),
    ],
)
def test_customer_purpose_accepts_exact_values(input_value: str, expected_enum: CustomerPurpose) -> None:
    assert CustomerPurpose(input_value) is expected_enum


@pytest.mark.parametrize(
    ('input_value', 'expected_enum'),
    [
        (CustomerPurpose.TAX_PAYMENT, '1'),
        (CustomerPurpose.CREDIT_IN_ACCOUNT, '10'),
        (CustomerPurpose.JUDICIAL_DEPOSIT, '100'),
        (CustomerPurpose.ALIMONY, '101'),
        (CustomerPurpose.CREDIT_ASSIGNMENT_CLIENT, '103'),
        (CustomerPurpose.CREDIT_ASSIGNMENT_FIDC, '104'),
        (CustomerPurpose.CONTRACTUAL_CASHFLOW_CLIENT, '107'),
        (CustomerPurpose.ADVANCE_CASHFLOW_CLIENT, '108'),
        (CustomerPurpose.CREDIT_ADJUSTMENTS, '109'),
        (CustomerPurpose.PAYMENT_BROKERS, '11'),
        (CustomerPurpose.TRANSFER_SAME_OWNER, '110'),
        (CustomerPurpose.CREDIT_TO_INVESTOR, '111'),
        (CustomerPurpose.DEBIT_FROM_INVESTOR, '112'),
        (CustomerPurpose.CREDIT_OPERATIONS_CLIENT, '113'),
        (CustomerPurpose.FINANCIAL_REDEMPTION_CLIENT, '114'),
        (CustomerPurpose.FINANCIAL_INVESTMENT_SENDER, '117'),
        (CustomerPurpose.PAYMENT_BANK_SLIP_REGISTRY, '12'),
        (CustomerPurpose.TIR_PAYMENT_PIX, '121'),
        (CustomerPurpose.CREDIT_ASSIGNMENT_REPURCHASE_CLIENT, '123'),
        (CustomerPurpose.CREDIT_ASSIGNMENT_REPURCHASE_FIDC, '124'),
        (CustomerPurpose.SERVICE_FEE_PAYMENT, '13'),
        (CustomerPurpose.FGCOOP_FUND_COLLECTION, '131'),
        (CustomerPurpose.FGCOOP_REFUND, '132'),
        (CustomerPurpose.FGTS_EMERGENCY_WITHDRAWAL, '136'),
        (CustomerPurpose.CONSUMER_CREDIT_INCENTIVE, '139'),
        (CustomerPurpose.REPAYMENT_REGISTRY_LIQUIDATION, '14'),
        (CustomerPurpose.EMERGENCY_AID, '149'),
        (CustomerPurpose.FINANCIAL_SETTLEMENT_CARD, '15'),
        (CustomerPurpose.BEM_EMPLOYMENT_BENEFIT, '150'),
        (CustomerPurpose.MUNICIPAL_TAXES_ISS_LCP157, '157'),
        (CustomerPurpose.MUNICIPAL_TAXES_ISS_THIRD, '175'),
        (CustomerPurpose.OPERATION_CANCELLATION, '177'),
        (CustomerPurpose.FINANCIAL_AGENT_FEE, '178'),
        (CustomerPurpose.OPERATOR_SETTLEMENT_CREDITOR, '179'),
        (CustomerPurpose.HOUSING_INSURANCE_SFH, '18'),
        (CustomerPurpose.SPVAT_COLLECTION_TRANSFER, '180'),
        (CustomerPurpose.FDS_OPERATIONS, '19'),
        (CustomerPurpose.PUBLIC_SERVICE_PAYMENT, '2'),
        (CustomerPurpose.INTERNATIONAL_TRANSFER_REAIS, '200'),
        (CustomerPurpose.FUTURES_MARKET_ADJUSTMENT, '201'),
        (CustomerPurpose.BNDES_VALUE_TRANSFER, '202'),
        (CustomerPurpose.BNDES_COMMITMENT_SETTLEMENT, '203'),
        (CustomerPurpose.STOCK_MARKET_OPERATIONS, '204'),
        (CustomerPurpose.STOCK_INDEX_CONTRACTS, '205'),
        (CustomerPurpose.NON_INTERBANK_FOREX, '206'),
        (CustomerPurpose.FIXED_VARIABLE_OPERATIONS, '207'),
        (CustomerPurpose.INTERBANK_FOREX_NO_RESERVE, '208'),
        (CustomerPurpose.PAYMENT_FINAL_RECIPIENT, '209'),
        (CustomerPurpose.ADMINISTRATION_FEE, '23'),
        (CustomerPurpose.JUDICIAL_AGREEMENT_PAYMENT, '27'),
        (CustomerPurpose.CONSIGNED_LOAN_SETTLEMENT, '28'),
        (CustomerPurpose.SCHOLARSHIP_PAYMENT, '29'),
        (CustomerPurpose.DIVIDEND_PAYMENT, '3'),
        (CustomerPurpose.COOPERATIVE_REMUNERATION, '30'),
        (CustomerPurpose.INCOME_TAX_REFUND, '300'),
        (CustomerPurpose.TREASURY_BANK_ORDER, '301'),
        (CustomerPurpose.BACEN_FINES_PAYMENT, '302'),
        (CustomerPurpose.TAX_REFUND_RFB, '303'),
        (CustomerPurpose.CLERICAL_REMUNERATION, '31'),
        (CustomerPurpose.INTEREST_ON_EQUITY, '33'),
        (CustomerPurpose.YIELD_AMORTIZATION, '34'),
        (CustomerPurpose.SERVICE_FEE, '35'),
        (CustomerPurpose.CHECK_PAYMENT_NON_ACCOUNT_HOLDER, '36'),
        (CustomerPurpose.GUARANTEED_SECURITIES_INTEREST, '37'),
        (CustomerPurpose.REVERSAL_OR_REFUND, '38'),
        (CustomerPurpose.TRANSPORT_VOUCHER_PAYMENT, '39'),
        (CustomerPurpose.SALARY_PAYMENT, '4'),
        (CustomerPurpose.SIMPLES_NACIONAL, '40'),
        (CustomerPurpose.FUNDEB_TRANSFER, '41'),
        (CustomerPurpose.CENTRALIZED_AGREEMENT_TRANSFER, '42'),
        (CustomerPurpose.SPONSORSHIP_TAX_INCENTIVE, '43'),
        (CustomerPurpose.DONATION_TAX_INCENTIVE, '44'),
        (CustomerPurpose.NONBANK_TO_LIQUIDATION_TRANSFER, '45'),
        (CustomerPurpose.TERMINATION_PAYMENT, '47'),
        (CustomerPurpose.SUPPLIER_PAYMENT, '5'),
        (CustomerPurpose.FIXED_VARIABLE_EXPENSE_REIMBURSEMENT, '50'),
        (CustomerPurpose.INSURANCE_PRIZE_REFUND, '500'),
        (CustomerPurpose.INSURANCE_CLAIM_PAYMENT, '501'),
        (CustomerPurpose.CO_INSURANCE_PREMIUM, '502'),
        (CustomerPurpose.CO_INSURANCE_CLAIM_PAYMENT, '504'),
        (CustomerPurpose.REINSURANCE_PREMIUM, '505'),
        (CustomerPurpose.REINSURANCE_CLAIM_PAYMENT, '507'),
        (CustomerPurpose.REINSURANCE_CLAIM_REFUND, '508'),
        (CustomerPurpose.CLAIM_EXPENSE_PAYMENT, '509'),
        (CustomerPurpose.INSPECTION_PAYMENT, '510'),
        (CustomerPurpose.CAPITALIZATION_REDEMPTION, '511'),
        (CustomerPurpose.CAPITALIZATION_DRAW, '512'),
        (CustomerPurpose.CAPITALIZATION_MONTHLY_REFUND, '513'),
        (CustomerPurpose.PENSION_CONTRIBUTION_REFUND, '514'),
        (CustomerPurpose.PENSION_PECCULUM_BENEFIT, '515'),
        (CustomerPurpose.PENSION_PENSION_BENEFIT, '516'),
        (CustomerPurpose.PENSION_RETIREMENT_BENEFIT, '517'),
        (CustomerPurpose.PENSION_REDEMPTION, '518'),
        (CustomerPurpose.BROKERAGE_COMMISSION, '519'),
        (CustomerPurpose.INSURANCE_PENSION_TRANSFER, '520'),
        (CustomerPurpose.FEES_PAYMENT, '6'),
        (CustomerPurpose.RENT_CONDOMINIUM, '7'),
        (CustomerPurpose.INVOICE_BILLS_PAYMENT, '8'),
        (CustomerPurpose.SCHOOL_FEE_PAYMENT, '9'),
        (CustomerPurpose.FOREIGN_CURRENCY_PURCHASE, '97'),
        (CustomerPurpose.OTHERS, '99999'),
    ],
)
def test_customer_purpose_enum_values_to_xml_value(input_value: CustomerPurpose, expected_enum: str) -> None:
    assert input_value.to_xml_value() == expected_enum


@pytest.mark.parametrize(
    ('input_value', 'expected_enum'),
    [
        ('1', CustomerPurpose.TAX_PAYMENT),
        ('10', CustomerPurpose.CREDIT_IN_ACCOUNT),
        ('100', CustomerPurpose.JUDICIAL_DEPOSIT),
        ('101', CustomerPurpose.ALIMONY),
        ('103', CustomerPurpose.CREDIT_ASSIGNMENT_CLIENT),
        ('104', CustomerPurpose.CREDIT_ASSIGNMENT_FIDC),
        ('107', CustomerPurpose.CONTRACTUAL_CASHFLOW_CLIENT),
        ('108', CustomerPurpose.ADVANCE_CASHFLOW_CLIENT),
        ('109', CustomerPurpose.CREDIT_ADJUSTMENTS),
        ('11', CustomerPurpose.PAYMENT_BROKERS),
        ('110', CustomerPurpose.TRANSFER_SAME_OWNER),
        ('111', CustomerPurpose.CREDIT_TO_INVESTOR),
        ('112', CustomerPurpose.DEBIT_FROM_INVESTOR),
        ('113', CustomerPurpose.CREDIT_OPERATIONS_CLIENT),
        ('114', CustomerPurpose.FINANCIAL_REDEMPTION_CLIENT),
        ('117', CustomerPurpose.FINANCIAL_INVESTMENT_SENDER),
        ('12', CustomerPurpose.PAYMENT_BANK_SLIP_REGISTRY),
        ('121', CustomerPurpose.TIR_PAYMENT_PIX),
        ('123', CustomerPurpose.CREDIT_ASSIGNMENT_REPURCHASE_CLIENT),
        ('124', CustomerPurpose.CREDIT_ASSIGNMENT_REPURCHASE_FIDC),
        ('13', CustomerPurpose.SERVICE_FEE_PAYMENT),
        ('131', CustomerPurpose.FGCOOP_FUND_COLLECTION),
        ('132', CustomerPurpose.FGCOOP_REFUND),
        ('136', CustomerPurpose.FGTS_EMERGENCY_WITHDRAWAL),
        ('139', CustomerPurpose.CONSUMER_CREDIT_INCENTIVE),
        ('14', CustomerPurpose.REPAYMENT_REGISTRY_LIQUIDATION),
        ('149', CustomerPurpose.EMERGENCY_AID),
        ('15', CustomerPurpose.FINANCIAL_SETTLEMENT_CARD),
        ('150', CustomerPurpose.BEM_EMPLOYMENT_BENEFIT),
        ('157', CustomerPurpose.MUNICIPAL_TAXES_ISS_LCP157),
        ('175', CustomerPurpose.MUNICIPAL_TAXES_ISS_THIRD),
        ('177', CustomerPurpose.OPERATION_CANCELLATION),
        ('178', CustomerPurpose.FINANCIAL_AGENT_FEE),
        ('179', CustomerPurpose.OPERATOR_SETTLEMENT_CREDITOR),
        ('18', CustomerPurpose.HOUSING_INSURANCE_SFH),
        ('180', CustomerPurpose.SPVAT_COLLECTION_TRANSFER),
        ('19', CustomerPurpose.FDS_OPERATIONS),
        ('2', CustomerPurpose.PUBLIC_SERVICE_PAYMENT),
        ('200', CustomerPurpose.INTERNATIONAL_TRANSFER_REAIS),
        ('201', CustomerPurpose.FUTURES_MARKET_ADJUSTMENT),
        ('202', CustomerPurpose.BNDES_VALUE_TRANSFER),
        ('203', CustomerPurpose.BNDES_COMMITMENT_SETTLEMENT),
        ('204', CustomerPurpose.STOCK_MARKET_OPERATIONS),
        ('205', CustomerPurpose.STOCK_INDEX_CONTRACTS),
        ('206', CustomerPurpose.NON_INTERBANK_FOREX),
        ('207', CustomerPurpose.FIXED_VARIABLE_OPERATIONS),
        ('208', CustomerPurpose.INTERBANK_FOREX_NO_RESERVE),
        ('209', CustomerPurpose.PAYMENT_FINAL_RECIPIENT),
        ('23', CustomerPurpose.ADMINISTRATION_FEE),
        ('27', CustomerPurpose.JUDICIAL_AGREEMENT_PAYMENT),
        ('28', CustomerPurpose.CONSIGNED_LOAN_SETTLEMENT),
        ('29', CustomerPurpose.SCHOLARSHIP_PAYMENT),
        ('3', CustomerPurpose.DIVIDEND_PAYMENT),
        ('30', CustomerPurpose.COOPERATIVE_REMUNERATION),
        ('300', CustomerPurpose.INCOME_TAX_REFUND),
        ('301', CustomerPurpose.TREASURY_BANK_ORDER),
        ('302', CustomerPurpose.BACEN_FINES_PAYMENT),
        ('303', CustomerPurpose.TAX_REFUND_RFB),
        ('31', CustomerPurpose.CLERICAL_REMUNERATION),
        ('33', CustomerPurpose.INTEREST_ON_EQUITY),
        ('34', CustomerPurpose.YIELD_AMORTIZATION),
        ('35', CustomerPurpose.SERVICE_FEE),
        ('36', CustomerPurpose.CHECK_PAYMENT_NON_ACCOUNT_HOLDER),
        ('37', CustomerPurpose.GUARANTEED_SECURITIES_INTEREST),
        ('38', CustomerPurpose.REVERSAL_OR_REFUND),
        ('39', CustomerPurpose.TRANSPORT_VOUCHER_PAYMENT),
        ('4', CustomerPurpose.SALARY_PAYMENT),
        ('40', CustomerPurpose.SIMPLES_NACIONAL),
        ('41', CustomerPurpose.FUNDEB_TRANSFER),
        ('42', CustomerPurpose.CENTRALIZED_AGREEMENT_TRANSFER),
        ('43', CustomerPurpose.SPONSORSHIP_TAX_INCENTIVE),
        ('44', CustomerPurpose.DONATION_TAX_INCENTIVE),
        ('45', CustomerPurpose.NONBANK_TO_LIQUIDATION_TRANSFER),
        ('47', CustomerPurpose.TERMINATION_PAYMENT),
        ('5', CustomerPurpose.SUPPLIER_PAYMENT),
        ('50', CustomerPurpose.FIXED_VARIABLE_EXPENSE_REIMBURSEMENT),
        ('500', CustomerPurpose.INSURANCE_PRIZE_REFUND),
        ('501', CustomerPurpose.INSURANCE_CLAIM_PAYMENT),
        ('502', CustomerPurpose.CO_INSURANCE_PREMIUM),
        ('504', CustomerPurpose.CO_INSURANCE_CLAIM_PAYMENT),
        ('505', CustomerPurpose.REINSURANCE_PREMIUM),
        ('507', CustomerPurpose.REINSURANCE_CLAIM_PAYMENT),
        ('508', CustomerPurpose.REINSURANCE_CLAIM_REFUND),
        ('509', CustomerPurpose.CLAIM_EXPENSE_PAYMENT),
        ('510', CustomerPurpose.INSPECTION_PAYMENT),
        ('511', CustomerPurpose.CAPITALIZATION_REDEMPTION),
        ('512', CustomerPurpose.CAPITALIZATION_DRAW),
        ('513', CustomerPurpose.CAPITALIZATION_MONTHLY_REFUND),
        ('514', CustomerPurpose.PENSION_CONTRIBUTION_REFUND),
        ('515', CustomerPurpose.PENSION_PECCULUM_BENEFIT),
        ('516', CustomerPurpose.PENSION_PENSION_BENEFIT),
        ('517', CustomerPurpose.PENSION_RETIREMENT_BENEFIT),
        ('518', CustomerPurpose.PENSION_REDEMPTION),
        ('519', CustomerPurpose.BROKERAGE_COMMISSION),
        ('520', CustomerPurpose.INSURANCE_PENSION_TRANSFER),
        ('6', CustomerPurpose.FEES_PAYMENT),
        ('7', CustomerPurpose.RENT_CONDOMINIUM),
        ('8', CustomerPurpose.INVOICE_BILLS_PAYMENT),
        ('9', CustomerPurpose.SCHOOL_FEE_PAYMENT),
        ('97', CustomerPurpose.FOREIGN_CURRENCY_PURCHASE),
        ('99999', CustomerPurpose.OTHERS),
    ],
)
def test_customer_purpose_enum_values_from_xml_value(input_value: str, expected_enum: CustomerPurpose) -> None:
    assert CustomerPurpose.from_xml_value(input_value) == expected_enum


@pytest.mark.parametrize(
    ('input_value', 'expected_enum'),
    [
        ('tax_payment', CustomerPurpose.TAX_PAYMENT),
        ('credit_in_account', CustomerPurpose.CREDIT_IN_ACCOUNT),
        ('judicial_deposit', CustomerPurpose.JUDICIAL_DEPOSIT),
        ('alimony', CustomerPurpose.ALIMONY),
    ],
)
def test_customer_purpose_accepts_case_insensitive_values(input_value: str, expected_enum: CustomerPurpose) -> None:
    assert CustomerPurpose(input_value) is expected_enum


@pytest.mark.parametrize(
    'invalid_value',
    [
        'TAX',  # Invalid abbreviation
        'CREDIT',  # Invalid abbreviation
        '12345',  # Numeric string
        'INVALID_PURPOSE',  # Completely invalid
    ],
)
def test_customer_purpose_rejects_invalid_value(invalid_value: str) -> None:
    with pytest.raises(ValueError, match=invalid_value):
        CustomerPurpose(invalid_value)


@pytest.mark.parametrize(
    'cnpj',
    [
        '81415129000162',
        '07205272000177',
        '00895553000150',
        '00028986000108',
        '12ABC34501DE35',
    ],
)
def test_cnpj_accepts_valid_values(cnpj: str) -> None:
    model = CnpjModel(cnpj=cnpj)
    assert model.cnpj == cnpj


def test_cnpj_accepts_whitespace() -> None:
    model = CnpjModel(cnpj='  81415129000162  ')
    assert model.cnpj == '81415129000162'


@pytest.mark.parametrize(
    'cnpj',
    [
        '8141512900016',  # Too short
        '814151290001622',  # Too long
        '81415!29000162',  # Contains special character
        '81415 29000162',  # Contains space
    ],
)
def test_cnpj_rejects_invalid_formats(cnpj: str) -> None:
    with pytest.raises(ValidationError) as exc:
        CnpjModel(cnpj=cnpj)
    assert "String should match pattern '^[0-9A-Z]{12}[0-9]{2}$'" in str(exc.value)


@pytest.mark.parametrize(
    'cnpj',
    [
        '81415129000161',
        '02345678000195',
        '12ABC34501DE38',
    ],
)
def test_cnpj_rejects_invalid_values(cnpj: str) -> None:
    with pytest.raises(ValidationError) as exc:
        CnpjModel(cnpj=cnpj)
    assert 'Value error, Invalid CNPJ format' in str(exc.value)


@pytest.mark.parametrize(
    'cpf',
    [
        '52423987013',
        '04033224050',
    ],
)
def test_cpf_accepts_valid_values(cpf: str) -> None:
    model = CpfModel(cpf=cpf)
    assert model.cpf == cpf


def test_cpf_accepts_whitespace() -> None:
    model = CpfModel(cpf='  52423987013  ')
    assert model.cpf == '52423987013'


@pytest.mark.parametrize(
    'cpf',
    [
        '52423987014',
        '04033224051',
    ],
)
def test_cpf_rejects_invalid_values(cpf: str) -> None:
    with pytest.raises(ValidationError) as exc:
        CpfModel(cpf=cpf)
    assert 'Value error, Invalid CPF format' in str(exc.value)


@pytest.mark.parametrize(
    'transaction_id',
    [
        'A',
        'A' * 25,
    ],
)
def test_string_max_length_accepts_valid_values(transaction_id: str) -> None:
    model = TransactionIdModel(transaction_id=transaction_id)
    assert model.transaction_id == transaction_id


def test_string_max_length_rejects_too_long_value() -> None:
    too_long_value = 'A' * 26
    with pytest.raises(ValidationError) as exc:
        TransactionIdModel(transaction_id=too_long_value)
    assert 'String should have at most 25 characters' in str(exc.value)


@pytest.mark.parametrize(
    ('input_value', 'expected_enum'),
    [
        ('HIGH', Priority.HIGH),
        ('HIGHEST', Priority.HIGHEST),
        ('LOW', Priority.LOW),
        ('MEDIUM', Priority.MEDIUM),
    ],
)
def test_priority_accepts_exact_values(input_value: str, expected_enum: Priority) -> None:
    assert Priority(input_value) is expected_enum


@pytest.mark.parametrize(
    ('input_value', 'expected_enum'),
    [
        ('high', Priority.HIGH),
        ('highest', Priority.HIGHEST),
        ('low', Priority.LOW),
        ('medium', Priority.MEDIUM),
    ],
)
def test_priority_accepts_case_insensitive_values(input_value: str, expected_enum: Priority) -> None:
    assert Priority(input_value) is expected_enum


@pytest.mark.parametrize(
    ('input_value', 'expected_enum'),
    [
        (Priority.HIGH, 'B'),
        (Priority.HIGHEST, 'A'),
        (Priority.LOW, 'D'),
        (Priority.MEDIUM, 'C'),
    ],
)
def test_priority_values_to_xml_value(input_value: Priority, expected_enum: str) -> None:
    assert input_value.to_xml_value() == expected_enum


@pytest.mark.parametrize(
    ('input_value', 'expected_enum'),
    [
        ('B', Priority.HIGH),
        ('A', Priority.HIGHEST),
        ('D', Priority.LOW),
        ('C', Priority.MEDIUM),
    ],
)
def test_priority_values_from_xml_value(input_value: str, expected_enum: Priority) -> None:
    assert Priority.from_xml_value(input_value) is expected_enum


@pytest.mark.parametrize(
    'priority',
    [
        'MED',  # Invalid abbreviation
        'HIGHER',  # Invalid abbreviation
        '123',  # Numeric string
    ],
)
def test_priority_rejects_invalid_value(priority: str) -> None:
    with pytest.raises(ValueError, match=priority):
        Priority(priority)


@pytest.mark.parametrize(
    'str_control_number',
    [
        'STR20250101000000001',  # 2025-01-01, minimal sequence
        'STR19991231999999999',  # 1999-12-31, max sequence
        'STR20240229000000001',  # 2024-02-29 (valid leap day syntactically)
        'STR20251130012345678',  # 2025-11-30
        'STR00000101000000000',  # year 0000, 01-01, sequence all zeros
        'STR20251201000000099',  # 2025-12-01
        'STR20250930098765432',  # 2025-09-30
    ],
)
def test_str_control_number_accepts_valid_values(str_control_number: str) -> None:
    model = StrControlNumberModel(str_control_number=str_control_number)
    assert model.str_control_number == str_control_number


def test_str_control_number_accepts_whitespace() -> None:
    model = StrControlNumberModel(str_control_number='  STR20250101000000001  ')
    assert model.str_control_number == 'STR20250101000000001'


@pytest.mark.parametrize(
    'str_control_number',
    [
        'STX20250101000000001',  # invalid prefix
        'STR20251301000000001',  # invalid month 13
        'STR20250001000000001',  # invalid month 00
        'STR20251232000000001',  # invalid day 32
        'STR20251200000000001',  # invalid day 00
        'STR2025010100000001',  # too short (8-digit sequence)
        'STR202501010000000001',  # too long (10-digit sequence)
        'STR2025A101000000001',  # non-digit in date part
        'STR20250101A00000001',  # non-digit in sequence part
        '202520101000000001',  # missing STR prefix
        'STR2025010100000000A',  # letter at the end
    ],
)
def test_str_control_number_rejects_invalid_formats(str_control_number: str) -> None:
    with pytest.raises(ValidationError) as exc:
        StrControlNumberModel(str_control_number=str_control_number)
    assert "String should match pattern '^STR\\d{4}(0[1-9]|1[0-2])(0[1-9]|[12]\\d|3[01])\\d{9}$'" in str(exc.value)


@pytest.mark.parametrize(
    ('input_value', 'expected_enum'),
    [
        ('CANCELED', StrSettlementStatus.CANCELED),
        ('CANCELED_CONTINGENCY', StrSettlementStatus.CANCELED_CONTINGENCY),
        ('EFFECTIVE', StrSettlementStatus.EFFECTIVE),
        ('EFFECTIVE_CONTINGENCY', StrSettlementStatus.EFFECTIVE_CONTINGENCY),
        ('EFFECTIVE_OPTIMIZATION', StrSettlementStatus.EFFECTIVE_OPTIMIZATION),
        ('EFFECTIVE_SCHEDULED', StrSettlementStatus.EFFECTIVE_SCHEDULED),
        ('PENDING_INSUFFICIENT_FUNDS', StrSettlementStatus.PENDING_INSUFFICIENT_FUNDS),
        ('PENDING_INSUFFICIENT_FUNDS_CONTINGENCY', StrSettlementStatus.PENDING_INSUFFICIENT_FUNDS_CONTINGENCY),
        (
            'PENDING_INSUFFICIENT_FUNDS_REJECTED_AFTER_DEADLINE',
            StrSettlementStatus.PENDING_INSUFFICIENT_FUNDS_REJECTED_AFTER_DEADLINE,
        ),
        (
            'PENDING_INSUFFICIENT_FUNDS_REJECTED_AFTER_DEADLINE_CONTINGENCY',
            StrSettlementStatus.PENDING_INSUFFICIENT_FUNDS_REJECTED_AFTER_DEADLINE_CONTINGENCY,
        ),
        ('PENDING_REJECTED_EXCLUSION_SUSPENSION', StrSettlementStatus.PENDING_REJECTED_EXCLUSION_SUSPENSION),
        (
            'PENDING_REJECTED_EXCLUSION_SUSPENSION_CONTINGENCY',
            StrSettlementStatus.PENDING_REJECTED_EXCLUSION_SUSPENSION_CONTINGENCY,
        ),
        ('PENDING_SCHEDULED', StrSettlementStatus.PENDING_SCHEDULED),
        ('PENDING_SCHEDULED_CONTINGENCY', StrSettlementStatus.PENDING_SCHEDULED_CONTINGENCY),
        ('REJECTED_INSUFFICIENT_FUNDS_CONTINGENCY', StrSettlementStatus.REJECTED_INSUFFICIENT_FUNDS_CONTINGENCY),
        ('REJECTED_NO_FUNDS', StrSettlementStatus.REJECTED_NO_FUNDS),
    ],
)
def test_str_settlement_status_accepts_exact_values(input_value: str, expected_enum: StrSettlementStatus) -> None:
    assert StrSettlementStatus(input_value) is expected_enum


@pytest.mark.parametrize(
    ('input_value', 'expected_enum'),
    [
        (StrSettlementStatus.CANCELED, '14'),
        (StrSettlementStatus.CANCELED_CONTINGENCY, '15'),
        (StrSettlementStatus.EFFECTIVE, '1'),
        (StrSettlementStatus.EFFECTIVE_CONTINGENCY, '2'),
        (StrSettlementStatus.EFFECTIVE_OPTIMIZATION, '3'),
        (StrSettlementStatus.EFFECTIVE_SCHEDULED, '4'),
        (StrSettlementStatus.PENDING_INSUFFICIENT_FUNDS, '17'),
        (StrSettlementStatus.PENDING_INSUFFICIENT_FUNDS_CONTINGENCY, '19'),
        (StrSettlementStatus.PENDING_INSUFFICIENT_FUNDS_REJECTED_AFTER_DEADLINE, '24'),
        (StrSettlementStatus.PENDING_INSUFFICIENT_FUNDS_REJECTED_AFTER_DEADLINE_CONTINGENCY, '25'),
        (StrSettlementStatus.PENDING_REJECTED_EXCLUSION_SUSPENSION, '22'),
        (StrSettlementStatus.PENDING_REJECTED_EXCLUSION_SUSPENSION_CONTINGENCY, '23'),
        (StrSettlementStatus.PENDING_SCHEDULED, '18'),
        (StrSettlementStatus.PENDING_SCHEDULED_CONTINGENCY, '20'),
        (StrSettlementStatus.REJECTED_INSUFFICIENT_FUNDS_CONTINGENCY, '9'),
        (StrSettlementStatus.REJECTED_NO_FUNDS, '5'),
    ],
)
def test_str_settlement_status_values_to_xml_value(input_value: StrSettlementStatus, expected_enum: str) -> None:
    assert input_value.to_xml_value() == expected_enum


@pytest.mark.parametrize(
    ('input_value', 'expected_enum'),
    [
        ('14', StrSettlementStatus.CANCELED),
        ('15', StrSettlementStatus.CANCELED_CONTINGENCY),
        ('1', StrSettlementStatus.EFFECTIVE),
        ('2', StrSettlementStatus.EFFECTIVE_CONTINGENCY),
        ('3', StrSettlementStatus.EFFECTIVE_OPTIMIZATION),
        ('4', StrSettlementStatus.EFFECTIVE_SCHEDULED),
        ('17', StrSettlementStatus.PENDING_INSUFFICIENT_FUNDS),
        ('19', StrSettlementStatus.PENDING_INSUFFICIENT_FUNDS_CONTINGENCY),
        ('24', StrSettlementStatus.PENDING_INSUFFICIENT_FUNDS_REJECTED_AFTER_DEADLINE),
        ('25', StrSettlementStatus.PENDING_INSUFFICIENT_FUNDS_REJECTED_AFTER_DEADLINE_CONTINGENCY),
        ('22', StrSettlementStatus.PENDING_REJECTED_EXCLUSION_SUSPENSION),
        ('23', StrSettlementStatus.PENDING_REJECTED_EXCLUSION_SUSPENSION_CONTINGENCY),
        ('18', StrSettlementStatus.PENDING_SCHEDULED),
        ('20', StrSettlementStatus.PENDING_SCHEDULED_CONTINGENCY),
        ('9', StrSettlementStatus.REJECTED_INSUFFICIENT_FUNDS_CONTINGENCY),
        ('5', StrSettlementStatus.REJECTED_NO_FUNDS),
    ],
)
def test_str_settlement_status_values_from_xml_value(input_value: str, expected_enum: StrSettlementStatus) -> None:
    assert StrSettlementStatus.from_xml_value(input_value) == expected_enum


@pytest.mark.parametrize(
    ('input_value', 'expected_enum'),
    [
        ('canceled', StrSettlementStatus.CANCELED),
        ('canceled_contingency', StrSettlementStatus.CANCELED_CONTINGENCY),
        ('effective', StrSettlementStatus.EFFECTIVE),
        ('effective_contingency', StrSettlementStatus.EFFECTIVE_CONTINGENCY),
        ('effective_optimization', StrSettlementStatus.EFFECTIVE_OPTIMIZATION),
        ('effective_scheduled', StrSettlementStatus.EFFECTIVE_SCHEDULED),
        ('pending_insufficient_funds', StrSettlementStatus.PENDING_INSUFFICIENT_FUNDS),
        ('pending_insufficient_funds_contingency', StrSettlementStatus.PENDING_INSUFFICIENT_FUNDS_CONTINGENCY),
        (
            'pending_insufficient_funds_rejected_after_deadline',
            StrSettlementStatus.PENDING_INSUFFICIENT_FUNDS_REJECTED_AFTER_DEADLINE,
        ),
        (
            'pending_insufficient_funds_rejected_after_deadline_contingency',
            StrSettlementStatus.PENDING_INSUFFICIENT_FUNDS_REJECTED_AFTER_DEADLINE_CONTINGENCY,
        ),
        ('pending_rejected_exclusion_suspension', StrSettlementStatus.PENDING_REJECTED_EXCLUSION_SUSPENSION),
        (
            'pending_rejected_exclusion_suspension_contingency',
            StrSettlementStatus.PENDING_REJECTED_EXCLUSION_SUSPENSION_CONTINGENCY,
        ),
        ('pending_scheduled', StrSettlementStatus.PENDING_SCHEDULED),
        ('pending_scheduled_contingency', StrSettlementStatus.PENDING_SCHEDULED_CONTINGENCY),
        ('rejected_insufficient_funds_contingency', StrSettlementStatus.REJECTED_INSUFFICIENT_FUNDS_CONTINGENCY),
        ('rejected_no_funds', StrSettlementStatus.REJECTED_NO_FUNDS),
    ],
)
def test_str_settlement_status_accepts_case_insensitive_values(
    input_value: str, expected_enum: StrSettlementStatus
) -> None:
    assert StrSettlementStatus(input_value) is expected_enum


@pytest.mark.parametrize(
    'invalid_value',
    [
        'CANCEL',  # Invalid abbreviation
        'EFFECT',  # Invalid abbreviation
        '12345',  # Numeric string
        'INVALID_STATUS',  # Completely invalid
    ],
)
def test_str_settlement_status_rejects_invalid_value(invalid_value: str) -> None:
    with pytest.raises(ValueError, match=invalid_value):
        StrSettlementStatus(invalid_value)


@pytest.mark.parametrize(
    ('input_value', 'expected_enum'),
    [
        ('DESTINATION_ACCOUNT_CLOSED', TransferReturnReason.DESTINATION_ACCOUNT_CLOSED),
        ('INVALID_JUDICIAL_DEPOSIT_ID', TransferReturnReason.INVALID_JUDICIAL_DEPOSIT_ID),
        ('OUT_OF_BUSINESS_HOURS', TransferReturnReason.OUT_OF_BUSINESS_HOURS),
        ('INVALID_CONTRACT_NUMBER', TransferReturnReason.INVALID_CONTRACT_NUMBER),
        ('DUPLICATE_VALUE', TransferReturnReason.DUPLICATE_VALUE),
        ('TERRORISM_FINANCING_ACTIVITY', TransferReturnReason.TERRORISM_FINANCING_ACTIVITY),
        ('INVALID_DESTINATION_AGENCY_OR_ACCOUNT', TransferReturnReason.INVALID_DESTINATION_AGENCY_OR_ACCOUNT),
        ('FGTS_DOCUMENT_NOT_PRESENTED', TransferReturnReason.FGTS_DOCUMENT_NOT_PRESENTED),
        ('TREASURY_PAYMENT_RETURN', TransferReturnReason.TREASURY_PAYMENT_RETURN),
        ('TREASURY_BANK_ORDER_RETURN', TransferReturnReason.TREASURY_BANK_ORDER_RETURN),
        ('RETURN_FILLING_ERROR', TransferReturnReason.RETURN_FILLING_ERROR),
        ('WITHHOLDING_DOCUMENT_FILLING_ERROR', TransferReturnReason.WITHHOLDING_DOCUMENT_FILLING_ERROR),
        ('DIRECT_DEPOSIT_FILLING_ERROR', TransferReturnReason.DIRECT_DEPOSIT_FILLING_ERROR),
        ('TAX_PAYMENT_RETURN_AT_BANK_REQUEST', TransferReturnReason.TAX_PAYMENT_RETURN_AT_BANK_REQUEST),
        ('OVERPAID_TAX_RETURN_AUTHORIZED_BY_RFB', TransferReturnReason.OVERPAID_TAX_RETURN_AUTHORIZED_BY_RFB),
        ('UNWITHDRAWN_CREDIT_EXPIRED', TransferReturnReason.UNWITHDRAWN_CREDIT_EXPIRED),
        ('MISSING_OR_MISMATCHED_TAX_ID', TransferReturnReason.MISSING_OR_MISMATCHED_TAX_ID),
        ('INAPT_TAX_ID_AT_RFB', TransferReturnReason.INAPT_TAX_ID_AT_RFB),
        ('INVALID_MESSAGE_FOR_TRANSACTION_TYPE', TransferReturnReason.INVALID_MESSAGE_FOR_TRANSACTION_TYPE),
        ('INVALID_CURRENCY_CODE_BARCODE', TransferReturnReason.INVALID_CURRENCY_CODE_BARCODE),
        ('TITLE_MISMATCH', TransferReturnReason.TITLE_MISMATCH),
        ('OVER_OR_UNDERPAID_BARCODE_BOLETO', TransferReturnReason.OVER_OR_UNDERPAID_BARCODE_BOLETO),
        ('LATE_BARCODE_BOLETO_WITHOUT_CHARGES', TransferReturnReason.LATE_BARCODE_BOLETO_WITHOUT_CHARGES),
        ('IMPROPER_PRESENTATION_BARCODE', TransferReturnReason.IMPROPER_PRESENTATION_BARCODE),
        ('INSUFFICIENT_AMOUNT_FOR_PURPOSE', TransferReturnReason.INSUFFICIENT_AMOUNT_FOR_PURPOSE),
        ('TRANSFER_ABOVE_DESTINATION_ACCOUNT_LIMIT', TransferReturnReason.TRANSFER_ABOVE_DESTINATION_ACCOUNT_LIMIT),
        ('BARCODE_NOT_COMPLIANT_WITH_SPECS', TransferReturnReason.BARCODE_NOT_COMPLIANT_WITH_SPECS),
        ('BOLETO_ALREADY_PAID', TransferReturnReason.BOLETO_ALREADY_PAID),
        ('BOLETO_DUPLICATE_PAYMENT_SAME_DAY', TransferReturnReason.BOLETO_DUPLICATE_PAYMENT_SAME_DAY),
        ('OVERPAYMENT_DIFFERENCE', TransferReturnReason.OVERPAYMENT_DIFFERENCE),
        ('CUSTOMER_REQUEST_RETURN', TransferReturnReason.CUSTOMER_REQUEST_RETURN),
        ('BARCODE_BOLETO_UNPLANNED_DISCOUNT', TransferReturnReason.BARCODE_BOLETO_UNPLANNED_DISCOUNT),
        ('NON_COMPLIANT_PAYMENT', TransferReturnReason.NON_COMPLIANT_PAYMENT),
        ('BENEFICIARY_NOT_IDENTIFIED_BARCODE', TransferReturnReason.BENEFICIARY_NOT_IDENTIFIED_BARCODE),
        ('INVALID_OR_MISMATCHED_BENEFICIARY_TAX_ID', TransferReturnReason.INVALID_OR_MISMATCHED_BENEFICIARY_TAX_ID),
        ('INVALID_OR_MISMATCHED_PAYER_TAX_ID', TransferReturnReason.INVALID_OR_MISMATCHED_PAYER_TAX_ID),
        ('COPY_NOT_SENT_BY_RECEIVING_BANK', TransferReturnReason.COPY_NOT_SENT_BY_RECEIVING_BANK),
        ('BOLETO_IN_COLLECTION_OR_PROTEST', TransferReturnReason.BOLETO_IN_COLLECTION_OR_PROTEST),
        ('INVALID_TRANSFER_IDENTIFIER', TransferReturnReason.INVALID_TRANSFER_IDENTIFIER),
        ('PORTABILITY_NOT_REGISTERED_CREDIT_CENTER', TransferReturnReason.PORTABILITY_NOT_REGISTERED_CREDIT_CENTER),
        (
            'BARCODE_BOLETO_DIVERGENT_FROM_CENTRAL_BASE',
            TransferReturnReason.BARCODE_BOLETO_DIVERGENT_FROM_CENTRAL_BASE,
        ),
        ('BARCODE_BOLETO_NOT_FOUND_IN_CENTRAL_BASE', TransferReturnReason.BARCODE_BOLETO_NOT_FOUND_IN_CENTRAL_BASE),
        (
            'INVALID_DESTINATION_ACCOUNT_FOR_TYPE_OR_PURPOSE',
            TransferReturnReason.INVALID_DESTINATION_ACCOUNT_FOR_TYPE_OR_PURPOSE,
        ),
        ('OPEN_FINANCE_PORTABILITY_NOT_COMPLETED', TransferReturnReason.OPEN_FINANCE_PORTABILITY_NOT_COMPLETED),
        ('FRAUD_RETURN', TransferReturnReason.FRAUD_RETURN),
    ],
)
def test_transfer_return_reason_accepts_exact_values(input_value: str, expected_enum: TransferReturnReason) -> None:
    assert TransferReturnReason(input_value) is expected_enum


@pytest.mark.parametrize(
    ('input_value', 'expected_enum'),
    [
        (TransferReturnReason.DESTINATION_ACCOUNT_CLOSED, '1'),
        (TransferReturnReason.INVALID_JUDICIAL_DEPOSIT_ID, '15'),
        (TransferReturnReason.OUT_OF_BUSINESS_HOURS, '16'),
        (TransferReturnReason.INVALID_CONTRACT_NUMBER, '17'),
        (TransferReturnReason.DUPLICATE_VALUE, '18'),
        (TransferReturnReason.TERRORISM_FINANCING_ACTIVITY, '19'),
        (TransferReturnReason.INVALID_DESTINATION_AGENCY_OR_ACCOUNT, '2'),
        (TransferReturnReason.FGTS_DOCUMENT_NOT_PRESENTED, '20'),
        (TransferReturnReason.TREASURY_PAYMENT_RETURN, '21'),
        (TransferReturnReason.TREASURY_BANK_ORDER_RETURN, '22'),
        (TransferReturnReason.RETURN_FILLING_ERROR, '23'),
        (TransferReturnReason.WITHHOLDING_DOCUMENT_FILLING_ERROR, '24'),
        (TransferReturnReason.DIRECT_DEPOSIT_FILLING_ERROR, '25'),
        (TransferReturnReason.TAX_PAYMENT_RETURN_AT_BANK_REQUEST, '26'),
        (TransferReturnReason.OVERPAID_TAX_RETURN_AUTHORIZED_BY_RFB, '27'),
        (TransferReturnReason.UNWITHDRAWN_CREDIT_EXPIRED, '28'),
        (TransferReturnReason.MISSING_OR_MISMATCHED_TAX_ID, '3'),
        (TransferReturnReason.INAPT_TAX_ID_AT_RFB, '31'),
        (TransferReturnReason.INVALID_MESSAGE_FOR_TRANSACTION_TYPE, '4'),
        (TransferReturnReason.INVALID_CURRENCY_CODE_BARCODE, '40'),
        (TransferReturnReason.TITLE_MISMATCH, '5'),
        (TransferReturnReason.OVER_OR_UNDERPAID_BARCODE_BOLETO, '51'),
        (TransferReturnReason.LATE_BARCODE_BOLETO_WITHOUT_CHARGES, '52'),
        (TransferReturnReason.IMPROPER_PRESENTATION_BARCODE, '53'),
        (TransferReturnReason.INSUFFICIENT_AMOUNT_FOR_PURPOSE, '6'),
        (TransferReturnReason.TRANSFER_ABOVE_DESTINATION_ACCOUNT_LIMIT, '61'),
        (TransferReturnReason.BARCODE_NOT_COMPLIANT_WITH_SPECS, '63'),
        (TransferReturnReason.BOLETO_ALREADY_PAID, '68'),
        (TransferReturnReason.BOLETO_DUPLICATE_PAYMENT_SAME_DAY, '69'),
        (TransferReturnReason.OVERPAYMENT_DIFFERENCE, '7'),
        (TransferReturnReason.CUSTOMER_REQUEST_RETURN, '70'),
        (TransferReturnReason.BARCODE_BOLETO_UNPLANNED_DISCOUNT, '71'),
        (TransferReturnReason.NON_COMPLIANT_PAYMENT, '72'),
        (TransferReturnReason.BENEFICIARY_NOT_IDENTIFIED_BARCODE, '73'),
        (TransferReturnReason.INVALID_OR_MISMATCHED_BENEFICIARY_TAX_ID, '74'),
        (TransferReturnReason.INVALID_OR_MISMATCHED_PAYER_TAX_ID, '75'),
        (TransferReturnReason.COPY_NOT_SENT_BY_RECEIVING_BANK, '76'),
        (TransferReturnReason.BOLETO_IN_COLLECTION_OR_PROTEST, '77'),
        (TransferReturnReason.INVALID_TRANSFER_IDENTIFIER, '8'),
        (TransferReturnReason.PORTABILITY_NOT_REGISTERED_CREDIT_CENTER, '80'),
        (TransferReturnReason.BARCODE_BOLETO_DIVERGENT_FROM_CENTRAL_BASE, '82'),
        (TransferReturnReason.BARCODE_BOLETO_NOT_FOUND_IN_CENTRAL_BASE, '83'),
        (TransferReturnReason.INVALID_DESTINATION_ACCOUNT_FOR_TYPE_OR_PURPOSE, '84'),
        (TransferReturnReason.OPEN_FINANCE_PORTABILITY_NOT_COMPLETED, '85'),
        (TransferReturnReason.FRAUD_RETURN, '9'),
    ],
)
def test_transfer_return_reason_values_to_xml_value(input_value: TransferReturnReason, expected_enum: str) -> None:
    assert input_value.to_xml_value() == expected_enum


@pytest.mark.parametrize(
    ('input_value', 'expected_enum'),
    [
        ('1', TransferReturnReason.DESTINATION_ACCOUNT_CLOSED),
        ('15', TransferReturnReason.INVALID_JUDICIAL_DEPOSIT_ID),
        ('16', TransferReturnReason.OUT_OF_BUSINESS_HOURS),
        ('17', TransferReturnReason.INVALID_CONTRACT_NUMBER),
        ('18', TransferReturnReason.DUPLICATE_VALUE),
        ('19', TransferReturnReason.TERRORISM_FINANCING_ACTIVITY),
        ('2', TransferReturnReason.INVALID_DESTINATION_AGENCY_OR_ACCOUNT),
        ('20', TransferReturnReason.FGTS_DOCUMENT_NOT_PRESENTED),
        ('21', TransferReturnReason.TREASURY_PAYMENT_RETURN),
        ('22', TransferReturnReason.TREASURY_BANK_ORDER_RETURN),
        ('23', TransferReturnReason.RETURN_FILLING_ERROR),
        ('24', TransferReturnReason.WITHHOLDING_DOCUMENT_FILLING_ERROR),
        ('25', TransferReturnReason.DIRECT_DEPOSIT_FILLING_ERROR),
        ('26', TransferReturnReason.TAX_PAYMENT_RETURN_AT_BANK_REQUEST),
        ('27', TransferReturnReason.OVERPAID_TAX_RETURN_AUTHORIZED_BY_RFB),
        ('28', TransferReturnReason.UNWITHDRAWN_CREDIT_EXPIRED),
        ('3', TransferReturnReason.MISSING_OR_MISMATCHED_TAX_ID),
        ('31', TransferReturnReason.INAPT_TAX_ID_AT_RFB),
        ('4', TransferReturnReason.INVALID_MESSAGE_FOR_TRANSACTION_TYPE),
        ('40', TransferReturnReason.INVALID_CURRENCY_CODE_BARCODE),
        ('5', TransferReturnReason.TITLE_MISMATCH),
        ('51', TransferReturnReason.OVER_OR_UNDERPAID_BARCODE_BOLETO),
        ('52', TransferReturnReason.LATE_BARCODE_BOLETO_WITHOUT_CHARGES),
        ('53', TransferReturnReason.IMPROPER_PRESENTATION_BARCODE),
        ('6', TransferReturnReason.INSUFFICIENT_AMOUNT_FOR_PURPOSE),
        ('61', TransferReturnReason.TRANSFER_ABOVE_DESTINATION_ACCOUNT_LIMIT),
        ('63', TransferReturnReason.BARCODE_NOT_COMPLIANT_WITH_SPECS),
        ('68', TransferReturnReason.BOLETO_ALREADY_PAID),
        ('69', TransferReturnReason.BOLETO_DUPLICATE_PAYMENT_SAME_DAY),
        ('7', TransferReturnReason.OVERPAYMENT_DIFFERENCE),
        ('70', TransferReturnReason.CUSTOMER_REQUEST_RETURN),
        ('71', TransferReturnReason.BARCODE_BOLETO_UNPLANNED_DISCOUNT),
        ('72', TransferReturnReason.NON_COMPLIANT_PAYMENT),
        ('73', TransferReturnReason.BENEFICIARY_NOT_IDENTIFIED_BARCODE),
        ('74', TransferReturnReason.INVALID_OR_MISMATCHED_BENEFICIARY_TAX_ID),
        ('75', TransferReturnReason.INVALID_OR_MISMATCHED_PAYER_TAX_ID),
        ('76', TransferReturnReason.COPY_NOT_SENT_BY_RECEIVING_BANK),
        ('77', TransferReturnReason.BOLETO_IN_COLLECTION_OR_PROTEST),
        ('8', TransferReturnReason.INVALID_TRANSFER_IDENTIFIER),
        ('80', TransferReturnReason.PORTABILITY_NOT_REGISTERED_CREDIT_CENTER),
        ('82', TransferReturnReason.BARCODE_BOLETO_DIVERGENT_FROM_CENTRAL_BASE),
        ('83', TransferReturnReason.BARCODE_BOLETO_NOT_FOUND_IN_CENTRAL_BASE),
        ('84', TransferReturnReason.INVALID_DESTINATION_ACCOUNT_FOR_TYPE_OR_PURPOSE),
        ('85', TransferReturnReason.OPEN_FINANCE_PORTABILITY_NOT_COMPLETED),
        ('9', TransferReturnReason.FRAUD_RETURN),
    ],
)
def test_transfer_return_reason_values_from_xml_value(input_value: str, expected_enum: TransferReturnReason) -> None:
    assert TransferReturnReason.from_xml_value(input_value) == expected_enum


@pytest.mark.parametrize(
    ('input_value', 'expected_enum'),
    [
        ('destination_account_closed', TransferReturnReason.DESTINATION_ACCOUNT_CLOSED),
        ('invalid_judicial_deposit_id', TransferReturnReason.INVALID_JUDICIAL_DEPOSIT_ID),
        ('out_of_business_hours', TransferReturnReason.OUT_OF_BUSINESS_HOURS),
        ('invalid_contract_number', TransferReturnReason.INVALID_CONTRACT_NUMBER),
        ('duplicate_value', TransferReturnReason.DUPLICATE_VALUE),
        ('terrorism_financing_activity', TransferReturnReason.TERRORISM_FINANCING_ACTIVITY),
        ('invalid_destination_agency_or_account', TransferReturnReason.INVALID_DESTINATION_AGENCY_OR_ACCOUNT),
        ('fgts_document_not_presented', TransferReturnReason.FGTS_DOCUMENT_NOT_PRESENTED),
        ('treasury_payment_return', TransferReturnReason.TREASURY_PAYMENT_RETURN),
        ('treasury_bank_order_return', TransferReturnReason.TREASURY_BANK_ORDER_RETURN),
        ('return_filling_error', TransferReturnReason.RETURN_FILLING_ERROR),
        ('withholding_document_filling_error', TransferReturnReason.WITHHOLDING_DOCUMENT_FILLING_ERROR),
        ('direct_deposit_filling_error', TransferReturnReason.DIRECT_DEPOSIT_FILLING_ERROR),
        ('tax_payment_return_at_bank_request', TransferReturnReason.TAX_PAYMENT_RETURN_AT_BANK_REQUEST),
        ('overpaid_tax_return_authorized_by_rfb', TransferReturnReason.OVERPAID_TAX_RETURN_AUTHORIZED_BY_RFB),
        ('unwithdrawn_credit_expired', TransferReturnReason.UNWITHDRAWN_CREDIT_EXPIRED),
        ('missing_or_mismatched_tax_id', TransferReturnReason.MISSING_OR_MISMATCHED_TAX_ID),
        ('inapt_tax_id_at_rfb', TransferReturnReason.INAPT_TAX_ID_AT_RFB),
        ('invalid_message_for_transaction_type', TransferReturnReason.INVALID_MESSAGE_FOR_TRANSACTION_TYPE),
        ('invalid_currency_code_barcode', TransferReturnReason.INVALID_CURRENCY_CODE_BARCODE),
        ('title_mismatch', TransferReturnReason.TITLE_MISMATCH),
        ('over_or_underpaid_barcode_boleto', TransferReturnReason.OVER_OR_UNDERPAID_BARCODE_BOLETO),
        ('late_barcode_boleto_without_charges', TransferReturnReason.LATE_BARCODE_BOLETO_WITHOUT_CHARGES),
        ('improper_presentation_barcode', TransferReturnReason.IMPROPER_PRESENTATION_BARCODE),
        ('insufficient_amount_for_purpose', TransferReturnReason.INSUFFICIENT_AMOUNT_FOR_PURPOSE),
        ('transfer_above_destination_account_limit', TransferReturnReason.TRANSFER_ABOVE_DESTINATION_ACCOUNT_LIMIT),
        ('barcode_not_compliant_with_specs', TransferReturnReason.BARCODE_NOT_COMPLIANT_WITH_SPECS),
        ('boleto_already_paid', TransferReturnReason.BOLETO_ALREADY_PAID),
        ('boleto_duplicate_payment_same_day', TransferReturnReason.BOLETO_DUPLICATE_PAYMENT_SAME_DAY),
        ('overpayment_difference', TransferReturnReason.OVERPAYMENT_DIFFERENCE),
        ('customer_request_return', TransferReturnReason.CUSTOMER_REQUEST_RETURN),
        ('barcode_boleto_unplanned_discount', TransferReturnReason.BARCODE_BOLETO_UNPLANNED_DISCOUNT),
        ('non_compliant_payment', TransferReturnReason.NON_COMPLIANT_PAYMENT),
        ('beneficiary_not_identified_barcode', TransferReturnReason.BENEFICIARY_NOT_IDENTIFIED_BARCODE),
        ('invalid_or_mismatched_beneficiary_tax_id', TransferReturnReason.INVALID_OR_MISMATCHED_BENEFICIARY_TAX_ID),
        ('invalid_or_mismatched_payer_tax_id', TransferReturnReason.INVALID_OR_MISMATCHED_PAYER_TAX_ID),
        ('copy_not_sent_by_receiving_bank', TransferReturnReason.COPY_NOT_SENT_BY_RECEIVING_BANK),
        ('boleto_in_collection_or_protest', TransferReturnReason.BOLETO_IN_COLLECTION_OR_PROTEST),
        ('invalid_transfer_identifier', TransferReturnReason.INVALID_TRANSFER_IDENTIFIER),
        ('portability_not_registered_credit_center', TransferReturnReason.PORTABILITY_NOT_REGISTERED_CREDIT_CENTER),
        (
            'barcode_boleto_divergent_from_central_base',
            TransferReturnReason.BARCODE_BOLETO_DIVERGENT_FROM_CENTRAL_BASE,
        ),
        ('barcode_boleto_not_found_in_central_base', TransferReturnReason.BARCODE_BOLETO_NOT_FOUND_IN_CENTRAL_BASE),
        (
            'invalid_destination_account_for_type_or_purpose',
            TransferReturnReason.INVALID_DESTINATION_ACCOUNT_FOR_TYPE_OR_PURPOSE,
        ),
        ('open_finance_portability_not_completed', TransferReturnReason.OPEN_FINANCE_PORTABILITY_NOT_COMPLETED),
        ('fraud_return', TransferReturnReason.FRAUD_RETURN),
    ],
)
def test_transfer_return_reason_accepts_case_insensitive_values(
    input_value: str, expected_enum: TransferReturnReason
) -> None:
    assert TransferReturnReason(input_value) is expected_enum


@pytest.mark.parametrize(
    'invalid_value',
    [
        'ACCOUNT_CLOSED',  # Invalid abbreviation
        'INVALID_ID',  # Invalid abbreviation
        '123',  # Numeric string
        'INVALID_REASON',  # Completely invalid
    ],
)
def test_transfer_return_reason_rejects_invalid_value(invalid_value: str) -> None:
    with pytest.raises(ValueError, match=invalid_value):
        TransferReturnReason(invalid_value)


@pytest.mark.parametrize(
    'credit_contract_number',
    [
        'A' * 20 + '1' * 20,
        'a' * 20 + '1' * 20,
        'A' * 1,
    ],
)
def test_credit_contract_number_accepts_valid_values(credit_contract_number: str) -> None:
    model = CreditContractNumberModel(credit_contract_number=credit_contract_number)
    assert model.credit_contract_number == credit_contract_number


def test_credit_contract_number_accepts_whitespace() -> None:
    model = CreditContractNumberModel(credit_contract_number='  AAAAAAAAAAAAAAAAAAAA11111111111111111111  ')
    assert model.credit_contract_number == 'AAAAAAAAAAAAAAAAAAAA11111111111111111111'


@pytest.mark.parametrize(
    'credit_contract_number',
    [
        'A' * 41,  # Too long
        'A' * 20 + '!' * 20,  # Special character
    ],
)
def test_credit_contract_number_rejects_invalid_formats(credit_contract_number: str) -> None:
    with pytest.raises(ValidationError) as exc:
        CreditContractNumberModel(credit_contract_number=credit_contract_number)
    msg = str(exc.value)
    assert 'String should have at most 40 characters' in msg or "String should match pattern '^[A-Za-z0-9]+$'" in msg


@pytest.mark.parametrize(
    'amount',
    [
        '0',
        '100',
        '100.0',
        '100.10',
        '100.11',
        '-100.11',
        '99999999999999999.99',  # Maximum valid (< 1e17)
        '-99999999999999999.99',  # Minimum valid (> -1e17)
    ],
)
def test_amount_accepts_valid_values(amount: str) -> None:
    model = AmountModel(amount=amount)
    assert model.amount == Decimal(amount)


def test_amount_accepts_whitespace() -> None:
    model = AmountModel(amount='   100.10   ')
    assert model.amount == Decimal('100.10')


@pytest.mark.parametrize(
    'amount',
    [
        '100.111',  # Too many decimal places
        '100.1.1',  # Invalid format
        'abc',  # Not numeric
        '999999999999999999.99',  # Too many digits (20 integers)
        '100000000000000000.00',  # == 1e17 (should be < 1e17)
        '-100000000000000000.00',  # == -1e17 (should be > -1e17)
    ],
)
def test_amount_rejects_invalid_values(amount: str) -> None:
    with pytest.raises(ValidationError):
        AmountModel(amount=amount)
