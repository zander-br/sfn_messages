from decimal import Decimal

import pytest
from pydantic import BaseModel, ValidationError

from sfn_messages.core.types import (
    AccountNumber,
    AccountType,
    Amount,
    AssetDescription,
    AssetType,
    Branch,
    Cnpj,
    Cpf,
    CreditContractNumber,
    CreditDebitType,
    CustomerPurpose,
    DepositIdentifier,
    Description,
    Email,
    ErrorCode,
    GridCode,
    InformationSequenceNumber,
    InformationType,
    InstitutionControlNumber,
    Ispb,
    LdlControlNumber,
    LdlSettlementStatus,
    MessageCode,
    MovementType,
    Name,
    OperationNumber,
    ParticipantIdentifier,
    PaymentNumber,
    PaymentType,
    PersonType,
    Priority,
    ProductCode,
    ReconciliationType,
    StaProtocolNumber,
    StrControlNumber,
    StrSettlementStatus,
    SystemDomain,
    Telephone,
    TimeType,
    TransactionId,
    TransferReturnReason,
)


class AccountNumberModel(BaseModel):
    account_number: AccountNumber


class AmountModel(BaseModel):
    amount: Amount


class AssetDescriptionModel(BaseModel):
    asset_description: AssetDescription


class BranchModel(BaseModel):
    branch: Branch


class CnpjModel(BaseModel):
    cnpj: Cnpj


class CpfModel(BaseModel):
    cpf: Cpf


class DescriptionModel(BaseModel):
    description: Description


class DepositIdentifierModel(BaseModel):
    deposit_identifier: DepositIdentifier


class EmailModel(BaseModel):
    email: Email


class ErrorCodeModel(BaseModel):
    error_code: ErrorCode


class NameModel(BaseModel):
    name: Name


class CreditContractNumberModel(BaseModel):
    credit_contract_number: CreditContractNumber


class InstitutionControlNumberModel(BaseModel):
    institution_control_number: InstitutionControlNumber


class InformationSequenceNumberModel(BaseModel):
    information_sequence_number: InformationSequenceNumber


class IspbModel(BaseModel):
    ispb: Ispb


class LdlControlNumberModel(BaseModel):
    ldl_control_number: LdlControlNumber


class MessageCodeModel(BaseModel):
    message_code: MessageCode


class OperationNumberModel(BaseModel):
    operation_number: OperationNumber


class ParticipantIdentifierModel(BaseModel):
    participant_identifier: ParticipantIdentifier


class PaymentNumberModel(BaseModel):
    payment_number: PaymentNumber


class TelephoneModel(BaseModel):
    telephone: Telephone


class TransactionIdModel(BaseModel):
    transaction_id: TransactionId


class StaProtocolNumberModel(BaseModel):
    sta_protocol_number: StaProtocolNumber


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
    'name',
    [
        'A' * 1,
        'John Doe',
        'A' * 80,
    ],
)
def test_name_accepts_valid_values(name: str) -> None:
    model = NameModel(name=name)
    assert model.name == name


def test_name_accepts_whitespace() -> None:
    model = NameModel(name='  Jane Smith  ')
    assert model.name == 'Jane Smith'


@pytest.mark.parametrize(
    'name',
    [
        'A' * 81,  # Too long
    ],
)
def test_name_rejects_invalid_values(name: str) -> None:
    with pytest.raises(ValidationError) as exc:
        NameModel(name=name)
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
        'ABCDEFGH123456789000123',
        '1234567A123456789000123',
        'A1B2C3D4123456789000123',
        'HGFEDCBA987654321000123',
        '4D3C2B1A000000000000000',
    ],
)
def test_operation_number_accepts_valid_values(operation_number: str) -> None:
    model = OperationNumberModel(operation_number=operation_number)
    assert model.operation_number == operation_number


def test_operation_number_accepts_whitespace() -> None:
    model = OperationNumberModel(operation_number='  ABCDEFGH123456789000123  ')
    assert model.operation_number == 'ABCDEFGH123456789000123'


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
    assert "String should match pattern '^[0-9A-Z]{8}[0-9]{15}$'" in str(exc.value)


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


@pytest.mark.parametrize(
    'deposit_identifier',
    [
        '0' + '1' * 17,
        '1' + '0' * 17,
        '0' + '12345678901234567',
    ],
)
def test_deposit_identifier_accepts_valid_values(deposit_identifier: str) -> None:
    model = DepositIdentifierModel(deposit_identifier=deposit_identifier)
    assert model.deposit_identifier == deposit_identifier


def test_deposit_identifier_accepts_whitespace() -> None:
    model = DepositIdentifierModel(deposit_identifier='   0' + '1' * 17 + '   ')
    assert model.deposit_identifier == '0' + '1' * 17


@pytest.mark.parametrize(
    'deposit_identifier',
    [
        '0' * 17,  # Too short
        '0' * 19,  # Too long
        '2' + '0' * 17,  # First char not 0 or 1
        '0' + '1234567890123456a',  # Non-digit
        '0 12345678901234567',  # Space
        '',  # Empty
    ],
)
def test_deposit_identifier_rejects_invalid_values(deposit_identifier: str) -> None:
    with pytest.raises(ValidationError):
        DepositIdentifierModel(deposit_identifier=deposit_identifier)


@pytest.mark.parametrize(
    'email',
    [
        'john.doe@email.com',
        'john.2010.doe@email.com',
    ],
)
def test_email_accepts_valid_values(email: str) -> None:
    model = EmailModel(email=email)
    assert model.email == email


def test_email_accepts_whitespace() -> None:
    model = EmailModel(email='   john.doe@email.com   ')
    assert model.email == 'john.doe@email.com'


@pytest.mark.parametrize(
    'email',
    [
        'john',  # Too short
        'john' * 19,  # Too long
        '',  # Empty
    ],
)
def test_email_rejects_invalid_values(email: str) -> None:
    with pytest.raises(ValidationError):
        EmailModel(email=email)


@pytest.mark.parametrize(
    'telephone',
    [
        '68998551891',
    ],
)
def test_telephone_valid_values(telephone: str) -> None:
    model = TelephoneModel(telephone=telephone)
    assert model.telephone == telephone


def test_telephone_accepts_whitespace() -> None:
    model = TelephoneModel(telephone='   68998551891   ')
    assert model.telephone == '68998551891'


@pytest.mark.parametrize(
    'telephone',
    [
        '6899855189123',  # Too long
    ],
)
def test_telephone_rejects_invalid_values(telephone: str) -> None:
    with pytest.raises(ValidationError):
        TelephoneModel(telephone=telephone)


@pytest.mark.parametrize(
    ('input_value', 'expected_enum'),
    [
        ('AMEX_CREDIT_CARD', ProductCode.AMEX_CREDIT_CARD),
        ('BANESCARD_CREDIT_CARD', ProductCode.BANESCARD_CREDIT_CARD),
        ('BANESCARD_DEBIT_CARD', ProductCode.BANESCARD_DEBIT_CARD),
        ('BEN_VISA_VALE', ProductCode.BEN_VISA_VALE),
        ('CIELO_AMEX_CREDIT', ProductCode.CIELO_AMEX_CREDIT),
        ('CABAL_CREDIT', ProductCode.CABAL_CREDIT),
        ('CABAL_DEBIT', ProductCode.CABAL_DEBIT),
        ('CABAL_PREPAID', ProductCode.CABAL_PREPAID),
        ('CREDIT_ASSIGNMENT_CENTER', ProductCode.CREDIT_ASSIGNMENT_CENTER),
        ('CIELO_DINERS_CREDIT', ProductCode.CIELO_DINERS_CREDIT),
        ('CIELO_ELO_CREDIT', ProductCode.CIELO_ELO_CREDIT),
        ('CIELO_ELO_DEBIT', ProductCode.CIELO_ELO_DEBIT),
        ('CIELO_HIPERCARD_CREDIT', ProductCode.CIELO_HIPERCARD_CREDIT),
        ('CIELO_MASTERCARD_CREDIT', ProductCode.CIELO_MASTERCARD_CREDIT),
        ('CIELO_MASTERCARD_DEBIT', ProductCode.CIELO_MASTERCARD_DEBIT),
        ('COPASA', ProductCode.COPASA),
        ('CHINA_UNIONPAY_CREDIT', ProductCode.CHINA_UNIONPAY_CREDIT),
        ('CREDZ_CREDIT', ProductCode.CREDZ_CREDIT),
        ('DINERS_CROSSBORDER_SETTLEMENTS', ProductCode.DINERS_CROSSBORDER_SETTLEMENTS),
        ('ELO_BENEFITS_CARD', ProductCode.ELO_BENEFITS_CARD),
        ('ELO_CREDIT_CARD', ProductCode.ELO_CREDIT_CARD),
        ('ELO_DEBIT_CARD', ProductCode.ELO_DEBIT_CARD),
        ('GOODCARD_CREDIT', ProductCode.GOODCARD_CREDIT),
        ('GLOBALPAY_DINERS_CREDIT', ProductCode.GLOBALPAY_DINERS_CREDIT),
        ('GLOBALPAY_MASTERCARD_CREDIT', ProductCode.GLOBALPAY_MASTERCARD_CREDIT),
        ('GLOBALPAY_MASTERCARD_DEBIT', ProductCode.GLOBALPAY_MASTERCARD_DEBIT),
        ('GLOBALPAY_VISA_CREDIT', ProductCode.GLOBALPAY_VISA_CREDIT),
        ('GLOBALPAY_VISA_DEBIT', ProductCode.GLOBALPAY_VISA_DEBIT),
        ('HIPERCARD_CREDIT', ProductCode.HIPERCARD_CREDIT),
        ('JCB_CREDIT', ProductCode.JCB_CREDIT),
        ('MAIS_CREDIT', ProductCode.MAIS_CREDIT),
        ('MASTERCARD_ATM', ProductCode.MASTERCARD_ATM),
        ('MASTERCARD_BENEFITS', ProductCode.MASTERCARD_BENEFITS),
        ('MASTERCARD_CREDIT', ProductCode.MASTERCARD_CREDIT),
        ('MASTERCARD_DEBIT', ProductCode.MASTERCARD_DEBIT),
        ('MASTERCARD_PREPAID', ProductCode.MASTERCARD_PREPAID),
        ('NEOENERGIA_BAHIA', ProductCode.NEOENERGIA_BAHIA),
        ('NEOENERGIA_BRASILIA', ProductCode.NEOENERGIA_BRASILIA),
        ('NEOENERGIA_ELEKTRO', ProductCode.NEOENERGIA_ELEKTRO),
        ('NEOENERGIA_PERNAMBUCO', ProductCode.NEOENERGIA_PERNAMBUCO),
        ('NEOENERGIA_RIOGRANDEDONORTE', ProductCode.NEOENERGIA_RIOGRANDEDONORTE),
        ('OUROCARD_DEBIT', ProductCode.OUROCARD_DEBIT),
        ('OTHER_TRANSFERS', ProductCode.OTHER_TRANSFERS),
        ('CENTRALIZED_COLLECTION_PLATFORM', ProductCode.CENTRALIZED_COLLECTION_PLATFORM),
        ('SOROCRED_CREDIT', ProductCode.SOROCRED_CREDIT),
        ('SOROCRED_DEBIT', ProductCode.SOROCRED_DEBIT),
        ('CENTRALIZED_SETTLEMENT_SERVICE', ProductCode.CENTRALIZED_SETTLEMENT_SERVICE),
        ('SELTEC', ProductCode.SELTEC),
        ('TECBAN', ProductCode.TECBAN),
        ('TED_SETTLEMENT', ProductCode.TED_SETTLEMENT),
        ('CHINA_UNIONPAY_DEBIT', ProductCode.CHINA_UNIONPAY_DEBIT),
        ('CHINA_UNIONPAY_PREPAID', ProductCode.CHINA_UNIONPAY_PREPAID),
        ('VISA_ATM', ProductCode.VISA_ATM),
        ('VISA_BENEFITS', ProductCode.VISA_BENEFITS),
        ('VISA_CREDIT', ProductCode.VISA_CREDIT),
        ('VISA_DEBIT', ProductCode.VISA_DEBIT),
        ('VISA_PREPAID', ProductCode.VISA_PREPAID),
        ('VERDECARD_CREDIT', ProductCode.VERDECARD_CREDIT),
        ('VERDECARD_PREPAID', ProductCode.VERDECARD_PREPAID),
        ('VISA_INTL_ATM_WITHDRAW', ProductCode.VISA_INTL_ATM_WITHDRAW),
        ('VISA_INTL_CREDIT_PURCHASE', ProductCode.VISA_INTL_CREDIT_PURCHASE),
        ('VISA_INTL_DEBIT_PURCHASE', ProductCode.VISA_INTL_DEBIT_PURCHASE),
    ],
)
def test_product_code_accepts_exact_values(input_value: str, expected_enum: ProductCode) -> None:
    assert ProductCode(input_value) is expected_enum


@pytest.mark.parametrize(
    ('input_value', 'expected_enum'),
    [
        (ProductCode.AMEX_CREDIT_CARD, 'ACC'),
        (ProductCode.BANESCARD_CREDIT_CARD, 'BCC'),
        (ProductCode.BANESCARD_DEBIT_CARD, 'BCD'),
        (ProductCode.BEN_VISA_VALE, 'BVV'),
        (ProductCode.CIELO_AMEX_CREDIT, 'CAC'),
        (ProductCode.CABAL_CREDIT, 'CBC'),
        (ProductCode.CABAL_DEBIT, 'CBD'),
        (ProductCode.CABAL_PREPAID, 'CBP'),
        (ProductCode.CREDIT_ASSIGNMENT_CENTER, 'CC3'),
        (ProductCode.CIELO_DINERS_CREDIT, 'CDC'),
        (ProductCode.CIELO_ELO_CREDIT, 'CEC'),
        (ProductCode.CIELO_ELO_DEBIT, 'CED'),
        (ProductCode.CIELO_HIPERCARD_CREDIT, 'CHC'),
        (ProductCode.CIELO_MASTERCARD_CREDIT, 'CMC'),
        (ProductCode.CIELO_MASTERCARD_DEBIT, 'CMD'),
        (ProductCode.COPASA, 'COP'),
        (ProductCode.CHINA_UNIONPAY_CREDIT, 'CUP'),
        (ProductCode.CREDZ_CREDIT, 'CZC'),
        (ProductCode.DINERS_CROSSBORDER_SETTLEMENTS, 'DCC'),
        (ProductCode.ELO_BENEFITS_CARD, 'ECB'),
        (ProductCode.ELO_CREDIT_CARD, 'ECC'),
        (ProductCode.ELO_DEBIT_CARD, 'ECD'),
        (ProductCode.GOODCARD_CREDIT, 'GCC'),
        (ProductCode.GLOBALPAY_DINERS_CREDIT, 'GDC'),
        (ProductCode.GLOBALPAY_MASTERCARD_CREDIT, 'GMC'),
        (ProductCode.GLOBALPAY_MASTERCARD_DEBIT, 'GMD'),
        (ProductCode.GLOBALPAY_VISA_CREDIT, 'GVC'),
        (ProductCode.GLOBALPAY_VISA_DEBIT, 'GVD'),
        (ProductCode.HIPERCARD_CREDIT, 'HCC'),
        (ProductCode.JCB_CREDIT, 'JCC'),
        (ProductCode.MAIS_CREDIT, 'MAC'),
        (ProductCode.MASTERCARD_ATM, 'MCA'),
        (ProductCode.MASTERCARD_BENEFITS, 'MCB'),
        (ProductCode.MASTERCARD_CREDIT, 'MCC'),
        (ProductCode.MASTERCARD_DEBIT, 'MCD'),
        (ProductCode.MASTERCARD_PREPAID, 'MCP'),
        (ProductCode.NEOENERGIA_BAHIA, 'NBA'),
        (ProductCode.NEOENERGIA_BRASILIA, 'NBR'),
        (ProductCode.NEOENERGIA_ELEKTRO, 'NEK'),
        (ProductCode.NEOENERGIA_PERNAMBUCO, 'NPE'),
        (ProductCode.NEOENERGIA_RIOGRANDEDONORTE, 'NRN'),
        (ProductCode.OUROCARD_DEBIT, 'OCD'),
        (ProductCode.OTHER_TRANSFERS, 'OT'),
        (ProductCode.CENTRALIZED_COLLECTION_PLATFORM, 'PCA'),
        (ProductCode.SOROCRED_CREDIT, 'SCC'),
        (ProductCode.SOROCRED_DEBIT, 'SCD'),
        (ProductCode.CENTRALIZED_SETTLEMENT_SERVICE, 'SLC'),
        (ProductCode.SELTEC, 'STC'),
        (ProductCode.TECBAN, 'TCB'),
        (ProductCode.TED_SETTLEMENT, 'TED'),
        (ProductCode.CHINA_UNIONPAY_DEBIT, 'UPD'),
        (ProductCode.CHINA_UNIONPAY_PREPAID, 'UPP'),
        (ProductCode.VISA_ATM, 'VCA'),
        (ProductCode.VISA_BENEFITS, 'VCB'),
        (ProductCode.VISA_CREDIT, 'VCC'),
        (ProductCode.VISA_DEBIT, 'VCD'),
        (ProductCode.VISA_PREPAID, 'VCP'),
        (ProductCode.VERDECARD_CREDIT, 'VDC'),
        (ProductCode.VERDECARD_PREPAID, 'VDP'),
        (ProductCode.VISA_INTL_ATM_WITHDRAW, 'VIA'),
        (ProductCode.VISA_INTL_CREDIT_PURCHASE, 'VIC'),
        (ProductCode.VISA_INTL_DEBIT_PURCHASE, 'VID'),
    ],
)
def test_product_code_values_to_xml_value(input_value: ProductCode, expected_enum: str) -> None:
    assert input_value.to_xml_value() == expected_enum


@pytest.mark.parametrize(
    ('input_value', 'expected_enum'),
    [
        ('ACC', ProductCode.AMEX_CREDIT_CARD),
        ('BCC', ProductCode.BANESCARD_CREDIT_CARD),
        ('BCD', ProductCode.BANESCARD_DEBIT_CARD),
        ('BVV', ProductCode.BEN_VISA_VALE),
        ('CAC', ProductCode.CIELO_AMEX_CREDIT),
        ('CBC', ProductCode.CABAL_CREDIT),
        ('CBD', ProductCode.CABAL_DEBIT),
        ('CBP', ProductCode.CABAL_PREPAID),
        ('CC3', ProductCode.CREDIT_ASSIGNMENT_CENTER),
        ('CDC', ProductCode.CIELO_DINERS_CREDIT),
        ('CEC', ProductCode.CIELO_ELO_CREDIT),
        ('CED', ProductCode.CIELO_ELO_DEBIT),
        ('CHC', ProductCode.CIELO_HIPERCARD_CREDIT),
        ('CMC', ProductCode.CIELO_MASTERCARD_CREDIT),
        ('CMD', ProductCode.CIELO_MASTERCARD_DEBIT),
        ('COP', ProductCode.COPASA),
        ('CUP', ProductCode.CHINA_UNIONPAY_CREDIT),
        ('CZC', ProductCode.CREDZ_CREDIT),
        ('DCC', ProductCode.DINERS_CROSSBORDER_SETTLEMENTS),
        ('ECB', ProductCode.ELO_BENEFITS_CARD),
        ('ECC', ProductCode.ELO_CREDIT_CARD),
        ('ECD', ProductCode.ELO_DEBIT_CARD),
        ('GCC', ProductCode.GOODCARD_CREDIT),
        ('GDC', ProductCode.GLOBALPAY_DINERS_CREDIT),
        ('GMC', ProductCode.GLOBALPAY_MASTERCARD_CREDIT),
        ('GMD', ProductCode.GLOBALPAY_MASTERCARD_DEBIT),
        ('GVC', ProductCode.GLOBALPAY_VISA_CREDIT),
        ('GVD', ProductCode.GLOBALPAY_VISA_DEBIT),
        ('HCC', ProductCode.HIPERCARD_CREDIT),
        ('JCC', ProductCode.JCB_CREDIT),
        ('MAC', ProductCode.MAIS_CREDIT),
        ('MCA', ProductCode.MASTERCARD_ATM),
        ('MCB', ProductCode.MASTERCARD_BENEFITS),
        ('MCC', ProductCode.MASTERCARD_CREDIT),
        ('MCD', ProductCode.MASTERCARD_DEBIT),
        ('MCP', ProductCode.MASTERCARD_PREPAID),
        ('NBA', ProductCode.NEOENERGIA_BAHIA),
        ('NBR', ProductCode.NEOENERGIA_BRASILIA),
        ('NEK', ProductCode.NEOENERGIA_ELEKTRO),
        ('NPE', ProductCode.NEOENERGIA_PERNAMBUCO),
        ('NRN', ProductCode.NEOENERGIA_RIOGRANDEDONORTE),
        ('OCD', ProductCode.OUROCARD_DEBIT),
        ('OT', ProductCode.OTHER_TRANSFERS),
        ('PCA', ProductCode.CENTRALIZED_COLLECTION_PLATFORM),
        ('SCC', ProductCode.SOROCRED_CREDIT),
        ('SCD', ProductCode.SOROCRED_DEBIT),
        ('SLC', ProductCode.CENTRALIZED_SETTLEMENT_SERVICE),
        ('STC', ProductCode.SELTEC),
        ('TCB', ProductCode.TECBAN),
        ('TED', ProductCode.TED_SETTLEMENT),
        ('UPD', ProductCode.CHINA_UNIONPAY_DEBIT),
        ('UPP', ProductCode.CHINA_UNIONPAY_PREPAID),
        ('VCA', ProductCode.VISA_ATM),
        ('VCB', ProductCode.VISA_BENEFITS),
        ('VCC', ProductCode.VISA_CREDIT),
        ('VCD', ProductCode.VISA_DEBIT),
        ('VCP', ProductCode.VISA_PREPAID),
        ('VDC', ProductCode.VERDECARD_CREDIT),
        ('VDP', ProductCode.VERDECARD_PREPAID),
        ('VIA', ProductCode.VISA_INTL_ATM_WITHDRAW),
        ('VIC', ProductCode.VISA_INTL_CREDIT_PURCHASE),
        ('VID', ProductCode.VISA_INTL_DEBIT_PURCHASE),
    ],
)
def test_product_code_values_from_xml_value(input_value: str, expected_enum: ProductCode) -> None:
    assert ProductCode.from_xml_value(input_value) == expected_enum


@pytest.mark.parametrize(
    ('input_value', 'expected_enum'),
    [
        ('amex_credit_card', ProductCode.AMEX_CREDIT_CARD),
        ('banescard_credit_card', ProductCode.BANESCARD_CREDIT_CARD),
        ('banescard_debit_card', ProductCode.BANESCARD_DEBIT_CARD),
        ('ben_visa_vale', ProductCode.BEN_VISA_VALE),
        ('cielo_amex_credit', ProductCode.CIELO_AMEX_CREDIT),
        ('cabal_credit', ProductCode.CABAL_CREDIT),
        ('cabal_debit', ProductCode.CABAL_DEBIT),
        ('cabal_prepaid', ProductCode.CABAL_PREPAID),
        ('credit_assignment_center', ProductCode.CREDIT_ASSIGNMENT_CENTER),
        ('cielo_diners_credit', ProductCode.CIELO_DINERS_CREDIT),
        ('cielo_elo_credit', ProductCode.CIELO_ELO_CREDIT),
        ('cielo_elo_debit', ProductCode.CIELO_ELO_DEBIT),
        ('cielo_hipercard_credit', ProductCode.CIELO_HIPERCARD_CREDIT),
        ('cielo_mastercard_credit', ProductCode.CIELO_MASTERCARD_CREDIT),
        ('cielo_mastercard_debit', ProductCode.CIELO_MASTERCARD_DEBIT),
        ('copasa', ProductCode.COPASA),
        ('china_unionpay_credit', ProductCode.CHINA_UNIONPAY_CREDIT),
        ('credz_credit', ProductCode.CREDZ_CREDIT),
        ('diners_crossborder_settlements', ProductCode.DINERS_CROSSBORDER_SETTLEMENTS),
        ('elo_benefits_card', ProductCode.ELO_BENEFITS_CARD),
        ('elo_credit_card', ProductCode.ELO_CREDIT_CARD),
        ('elo_debit_card', ProductCode.ELO_DEBIT_CARD),
        ('goodcard_credit', ProductCode.GOODCARD_CREDIT),
        ('globalpay_diners_credit', ProductCode.GLOBALPAY_DINERS_CREDIT),
        ('globalpay_mastercard_credit', ProductCode.GLOBALPAY_MASTERCARD_CREDIT),
        ('globalpay_mastercard_debit', ProductCode.GLOBALPAY_MASTERCARD_DEBIT),
        ('globalpay_visa_credit', ProductCode.GLOBALPAY_VISA_CREDIT),
        ('globalpay_visa_debit', ProductCode.GLOBALPAY_VISA_DEBIT),
        ('hipercard_credit', ProductCode.HIPERCARD_CREDIT),
        ('jcb_credit', ProductCode.JCB_CREDIT),
        ('mais_credit', ProductCode.MAIS_CREDIT),
        ('mastercard_atm', ProductCode.MASTERCARD_ATM),
        ('mastercard_benefits', ProductCode.MASTERCARD_BENEFITS),
        ('mastercard_credit', ProductCode.MASTERCARD_CREDIT),
        ('mastercard_debit', ProductCode.MASTERCARD_DEBIT),
        ('mastercard_prepaid', ProductCode.MASTERCARD_PREPAID),
        ('neoenergia_bahia', ProductCode.NEOENERGIA_BAHIA),
        ('neoenergia_brasilia', ProductCode.NEOENERGIA_BRASILIA),
        ('neoenergia_elektro', ProductCode.NEOENERGIA_ELEKTRO),
        ('neoenergia_pernambuco', ProductCode.NEOENERGIA_PERNAMBUCO),
        ('neoenergia_riograndedonorte', ProductCode.NEOENERGIA_RIOGRANDEDONORTE),
        ('ourocard_debit', ProductCode.OUROCARD_DEBIT),
        ('other_transfers', ProductCode.OTHER_TRANSFERS),
        ('centralized_collection_platform', ProductCode.CENTRALIZED_COLLECTION_PLATFORM),
        ('sorocred_credit', ProductCode.SOROCRED_CREDIT),
        ('sorocred_debit', ProductCode.SOROCRED_DEBIT),
        ('centralized_settlement_service', ProductCode.CENTRALIZED_SETTLEMENT_SERVICE),
        ('seltec', ProductCode.SELTEC),
        ('tecban', ProductCode.TECBAN),
        ('ted_settlement', ProductCode.TED_SETTLEMENT),
        ('china_unionpay_debit', ProductCode.CHINA_UNIONPAY_DEBIT),
        ('china_unionpay_prepaid', ProductCode.CHINA_UNIONPAY_PREPAID),
        ('visa_atm', ProductCode.VISA_ATM),
        ('visa_benefits', ProductCode.VISA_BENEFITS),
        ('visa_credit', ProductCode.VISA_CREDIT),
        ('visa_debit', ProductCode.VISA_DEBIT),
        ('visa_prepaid', ProductCode.VISA_PREPAID),
        ('verdecard_credit', ProductCode.VERDECARD_CREDIT),
        ('verdecard_prepaid', ProductCode.VERDECARD_PREPAID),
        ('visa_intl_atm_withdraw', ProductCode.VISA_INTL_ATM_WITHDRAW),
        ('visa_intl_credit_purchase', ProductCode.VISA_INTL_CREDIT_PURCHASE),
        ('visa_intl_debit_purchase', ProductCode.VISA_INTL_DEBIT_PURCHASE),
    ],
)
def test_product_code_accepts_case_insensitive_values(input_value: str, expected_enum: ProductCode) -> None:
    assert ProductCode(input_value) is expected_enum


@pytest.mark.parametrize(
    ('input_value', 'expected_enum'),
    [
        ('PAYMENT_ORDER_SCHEDULING', GridCode.PAYMENT_ORDER_SCHEDULING),
        ('SCHEDULED_PAYMENT_ORDER_SETTLEMENT', GridCode.SCHEDULED_PAYMENT_ORDER_SETTLEMENT),
        ('BMA_OPERATIONS', GridCode.BMA_OPERATIONS),
        ('BMA_ASSET_MOVEMENT', GridCode.BMA_ASSET_MOVEMENT),
        ('BMA_REPO_D0_DM', GridCode.BMA_REPO_D0_DM),
        ('BMA_REPO_DN_DM', GridCode.BMA_REPO_DN_DM),
        ('BMA_SPOT_TRADES_D0', GridCode.BMA_SPOT_TRADES_D0),
        ('BMA_FORWARD_TRADES_DN', GridCode.BMA_FORWARD_TRADES_DN),
        ('BMA_PHONE_ORDER_RELOCATION_REJECTION_D0', GridCode.BMA_PHONE_ORDER_RELOCATION_REJECTION_D0),
        ('BMA_PHONE_ORDER_RELOCATION_REJECTION_DN', GridCode.BMA_PHONE_ORDER_RELOCATION_REJECTION_DN),
        ('BMA_COVERED_OPERATIONS_SPEC_D0', GridCode.BMA_COVERED_OPERATIONS_SPEC_D0),
        ('BMA_COLLATERAL_SPEC_REPO_UNCOMP_D0', GridCode.BMA_COLLATERAL_SPEC_REPO_UNCOMP_D0),
        ('BMA_COLLATERAL_SPEC_REPO_UNCOMP_DN', GridCode.BMA_COLLATERAL_SPEC_REPO_UNCOMP_DN),
        ('BMA_COLLATERAL_SPEC_REPO_COMP', GridCode.BMA_COLLATERAL_SPEC_REPO_COMP),
        ('BMA_DIRECTION_ACCEPTANCE', GridCode.BMA_DIRECTION_ACCEPTANCE),
        ('BMA_BL_CONFIRM_LIQUID_RESULT', GridCode.BMA_BL_CONFIRM_LIQUID_RESULT),
        ('BMA_PARTICIPANT_DELIVERY_PAYMENT', GridCode.BMA_PARTICIPANT_DELIVERY_PAYMENT),
        ('BMA_CLEARINGHOUSE_DELIVERY_PAYMENT', GridCode.BMA_CLEARINGHOUSE_DELIVERY_PAYMENT),
        ('BMA_REQUEST_DELIVERY_RESTRICTION', GridCode.BMA_REQUEST_DELIVERY_RESTRICTION),
        ('BMA_CONFIRM_RELEASE_DELIVERY_RESTRICTION', GridCode.BMA_CONFIRM_RELEASE_DELIVERY_RESTRICTION),
        ('BMA_PARTIAL_DELIVERY_REQUEST', GridCode.BMA_PARTIAL_DELIVERY_REQUEST),
        ('BMA_PAYMENT_WITH_COLLATERAL', GridCode.BMA_PAYMENT_WITH_COLLATERAL),
        ('BMA_COLLATERAL_RESTORATION_REQUEST', GridCode.BMA_COLLATERAL_RESTORATION_REQUEST),
        ('BMA_PAYMENT_DELIVERY_REGULARIZATION_D0', GridCode.BMA_PAYMENT_DELIVERY_REGULARIZATION_D0),
        ('BMA_PAYMENT_DELIVERY_REGULARIZATION_D1', GridCode.BMA_PAYMENT_DELIVERY_REGULARIZATION_D1),
        ('BMC_GENERAL', GridCode.BMC_GENERAL),
        ('BMD_GENERAL', GridCode.BMD_GENERAL),
        ('BMD_DERIVATIVES_OPENING', GridCode.BMD_DERIVATIVES_OPENING),
        ('BMD_PROVISIONAL_NETTING', GridCode.BMD_PROVISIONAL_NETTING),
        ('BMD_FINAL_NETTING', GridCode.BMD_FINAL_NETTING),
        ('BMD_CLEARING_BANK_CONFIRMATION', GridCode.BMD_CLEARING_BANK_CONFIRMATION),
        ('BMD_RECEIPT_OF_PAYMENTS', GridCode.BMD_RECEIPT_OF_PAYMENTS),
        ('BMD_PAYMENT_SETTLEMENT', GridCode.BMD_PAYMENT_SETTLEMENT),
        ('BMD_CLOSE_MESSAGE', GridCode.BMD_CLOSE_MESSAGE),
        ('BMD_COLLATERAL_DEPOSIT', GridCode.BMD_COLLATERAL_DEPOSIT),
        ('BMD_COLLATERAL_DEPOSIT_D1', GridCode.BMD_COLLATERAL_DEPOSIT_D1),
        ('BVF_GENERAL', GridCode.BVF_GENERAL),
        ('BVF_UNIFIED_CE_OPENING', GridCode.BVF_UNIFIED_CE_OPENING),
        ('BVF_PROVISIONAL_NETTING', GridCode.BVF_PROVISIONAL_NETTING),
        ('BVF_FINAL_NETTING', GridCode.BVF_FINAL_NETTING),
        ('BVF_CLEARING_BANK_CONFIRMATION', GridCode.BVF_CLEARING_BANK_CONFIRMATION),
        ('BVF_RECEIPT_OF_PAYMENTS', GridCode.BVF_RECEIPT_OF_PAYMENTS),
        ('BVF_PAYMENT_SETTLEMENT', GridCode.BVF_PAYMENT_SETTLEMENT),
        ('BVF_CLOSE_MESSAGE', GridCode.BVF_CLOSE_MESSAGE),
        ('BVF_COLLATERAL_DEPOSIT', GridCode.BVF_COLLATERAL_DEPOSIT),
        ('BVF_COLLATERAL_DEPOSIT_D1', GridCode.BVF_COLLATERAL_DEPOSIT_D1),
        ('FX_PRIMARY_MARKET', GridCode.FX_PRIMARY_MARKET),
        ('FX_INTERBANK_MARKET', GridCode.FX_INTERBANK_MARKET),
        ('FX_SYSTEM_QUERIES', GridCode.FX_SYSTEM_QUERIES),
        ('FX_SYSTEM_SERVICES', GridCode.FX_SYSTEM_SERVICES),
        ('CBLC_GENERAL', GridCode.CBLC_GENERAL),
        ('CBLC_FIXED_INCOME_VARIABLE_INFORM_SETTLEMENT_03', GridCode.CBLC_FIXED_INCOME_VARIABLE_INFORM_SETTLEMENT_03),
        ('CBLC_FIXED_INCOME_VARIABLE_INFORM_SETTLEMENT_04', GridCode.CBLC_FIXED_INCOME_VARIABLE_INFORM_SETTLEMENT_04),
        ('CBLC_FIXED_INCOME_VARIABLE_BACEN', GridCode.CBLC_FIXED_INCOME_VARIABLE_BACEN),
        ('CBLC_IF_CONFIRM_DIVERGE_SETTLEMENT', GridCode.CBLC_IF_CONFIRM_DIVERGE_SETTLEMENT),
        ('CBLC_DISCREPANCY_ADJUSTMENT_LIMIT', GridCode.CBLC_DISCREPANCY_ADJUSTMENT_LIMIT),
        (
            'CBLC_IF_REQUEST_RESERVE_TRANSFER_FOR_DEBIT_SETTLEMENT',
            GridCode.CBLC_IF_REQUEST_RESERVE_TRANSFER_FOR_DEBIT_SETTLEMENT,
        ),
        ('CBLC_DVP_CREDITOR_SETTLEMENT_AND_DELIVERY', GridCode.CBLC_DVP_CREDITOR_SETTLEMENT_AND_DELIVERY),
        ('CBLC_CUSTODY_PAYMENT_EVENTS', GridCode.CBLC_CUSTODY_PAYMENT_EVENTS),
        ('CBLC_CUSTODY_IF_REQUEST_TRANSFER', GridCode.CBLC_CUSTODY_IF_REQUEST_TRANSFER),
        ('CBLC_CUSTODY_REPASS_EVENTS', GridCode.CBLC_CUSTODY_REPASS_EVENTS),
        ('CBLC_EQUITY_SETTLEMENT_SPEC', GridCode.CBLC_EQUITY_SETTLEMENT_SPEC),
        ('CBLC_EQUITY_MOVEMENT_AUTHORIZATION', GridCode.CBLC_EQUITY_MOVEMENT_AUTHORIZATION),
        ('CBLC_EQUITY_DELIVERY_BY_DEBTORS', GridCode.CBLC_EQUITY_DELIVERY_BY_DEBTORS),
        ('CBLC_EQUITY_DELIVERY_FAILURE_HANDLING', GridCode.CBLC_EQUITY_DELIVERY_FAILURE_HANDLING),
        ('CBLC_EQUITY_RESTRICTION_REQUEST_LIMIT', GridCode.CBLC_EQUITY_RESTRICTION_REQUEST_LIMIT),
        ('CBLC_EQUITY_DELIVERY_BY_CBLC', GridCode.CBLC_EQUITY_DELIVERY_BY_CBLC),
        ('CBLC_EQUITY_RESTRICTION_RELEASE', GridCode.CBLC_EQUITY_RESTRICTION_RELEASE),
        ('CBLC_PRIVATE_FIXED_INCOME_NEGOTIATION_LIMIT_D0', GridCode.CBLC_PRIVATE_FIXED_INCOME_NEGOTIATION_LIMIT_D0),
        ('CBLC_PRIVATE_FIXED_INCOME_CANCEL_LIMIT_D0', GridCode.CBLC_PRIVATE_FIXED_INCOME_CANCEL_LIMIT_D0),
        ('CBLC_PRIVATE_FIXED_INCOME_SPEC_LIMIT_D0', GridCode.CBLC_PRIVATE_FIXED_INCOME_SPEC_LIMIT_D0),
        ('CBLC_PRIVATE_FIXED_INCOME_DIRECTION_AUTH_D0', GridCode.CBLC_PRIVATE_FIXED_INCOME_DIRECTION_AUTH_D0),
        ('CBLC_PRIVATE_FIXED_INCOME_NEGOTIATION_LIMIT_D1', GridCode.CBLC_PRIVATE_FIXED_INCOME_NEGOTIATION_LIMIT_D1),
        ('CBLC_PRIVATE_FIXED_INCOME_CANCEL_LIMIT_D1', GridCode.CBLC_PRIVATE_FIXED_INCOME_CANCEL_LIMIT_D1),
        ('CBLC_PRIVATE_FIXED_INCOME_SPEC_LIMIT_D1', GridCode.CBLC_PRIVATE_FIXED_INCOME_SPEC_LIMIT_D1),
        ('CBLC_PRIVATE_FIXED_INCOME_DIRECTION_AUTH_D1', GridCode.CBLC_PRIVATE_FIXED_INCOME_DIRECTION_AUTH_D1),
        ('CBLC_PRIVATE_FIXED_INCOME_CLEARING', GridCode.CBLC_PRIVATE_FIXED_INCOME_CLEARING),
        ('CBLC_PRIVATE_FIXED_INCOME_DELIVERY', GridCode.CBLC_PRIVATE_FIXED_INCOME_DELIVERY),
        ('CBLC_PRIVATE_FIXED_INCOME_DELIVERY_FAILURE', GridCode.CBLC_PRIVATE_FIXED_INCOME_DELIVERY_FAILURE),
        (
            'CBLC_PRIVATE_FIXED_INCOME_RESTRICTION_REQUEST_LIMIT',
            GridCode.CBLC_PRIVATE_FIXED_INCOME_RESTRICTION_REQUEST_LIMIT,
        ),
        ('CBLC_PRIVATE_FIXED_INCOME_RESTRICTION_CONFIRM', GridCode.CBLC_PRIVATE_FIXED_INCOME_RESTRICTION_CONFIRM),
        ('CBLC_GROSS_SETTLEMENT_PREPARE_SEND_LTR_VALUES', GridCode.CBLC_GROSS_SETTLEMENT_PREPARE_SEND_LTR_VALUES),
        ('CBLC_GROSS_SETTLEMENT_IF_CONFIRM_OR_DIVERGE_LTR', GridCode.CBLC_GROSS_SETTLEMENT_IF_CONFIRM_OR_DIVERGE_LTR),
        (
            'CBLC_GROSS_SETTLEMENT_IF_REQUEST_TRANSFER_RESERVES',
            GridCode.CBLC_GROSS_SETTLEMENT_IF_REQUEST_TRANSFER_RESERVES,
        ),
        ('CBLC_GROSS_SETTLEMENT_CREDITOR_RESULTS', GridCode.CBLC_GROSS_SETTLEMENT_CREDITOR_RESULTS),
        ('CBLC_COLLATERAL_MOVEMENT', GridCode.CBLC_COLLATERAL_MOVEMENT),
        ('CBLC_LIMITS_DEALLOCATION', GridCode.CBLC_LIMITS_DEALLOCATION),
        ('CBLC_PUBLIC_TITLES_TRANSFER_FOR_MARGIN_REVERSAL', GridCode.CBLC_PUBLIC_TITLES_TRANSFER_FOR_MARGIN_REVERSAL),
        ('CBLC_PUBLIC_FIXED_INCOME_NEGOTIATION_LIMIT_D0', GridCode.CBLC_PUBLIC_FIXED_INCOME_NEGOTIATION_LIMIT_D0),
        ('CBLC_PUBLIC_FIXED_INCOME_CANCEL_LIMIT_D0', GridCode.CBLC_PUBLIC_FIXED_INCOME_CANCEL_LIMIT_D0),
        ('CBLC_PUBLIC_FIXED_INCOME_SPEC_LIMIT_D0', GridCode.CBLC_PUBLIC_FIXED_INCOME_SPEC_LIMIT_D0),
        ('CBLC_PUBLIC_FIXED_INCOME_DIRECTION_AUTH_D0', GridCode.CBLC_PUBLIC_FIXED_INCOME_DIRECTION_AUTH_D0),
        ('CBLC_PUBLIC_FIXED_INCOME_NEGOTIATION_LIMIT_D1', GridCode.CBLC_PUBLIC_FIXED_INCOME_NEGOTIATION_LIMIT_D1),
        ('CBLC_PUBLIC_FIXED_INCOME_CANCEL_LIMIT_D1', GridCode.CBLC_PUBLIC_FIXED_INCOME_CANCEL_LIMIT_D1),
        ('CBLC_PUBLIC_FIXED_INCOME_SPEC_LIMIT_D1', GridCode.CBLC_PUBLIC_FIXED_INCOME_SPEC_LIMIT_D1),
        ('CBLC_PUBLIC_FIXED_INCOME_DIRECTION_AUTH_D1', GridCode.CBLC_PUBLIC_FIXED_INCOME_DIRECTION_AUTH_D1),
        ('CBLC_PUBLIC_FIXED_INCOME_CLEARING', GridCode.CBLC_PUBLIC_FIXED_INCOME_CLEARING),
        ('CBLC_PUBLIC_FIXED_INCOME_DELIVERY', GridCode.CBLC_PUBLIC_FIXED_INCOME_DELIVERY),
        ('CBLC_PUBLIC_FIXED_INCOME_DELIVERY_FAILURE', GridCode.CBLC_PUBLIC_FIXED_INCOME_DELIVERY_FAILURE),
        (
            'CBLC_PUBLIC_FIXED_INCOME_RESTRICTION_REQUEST_LIMIT',
            GridCode.CBLC_PUBLIC_FIXED_INCOME_RESTRICTION_REQUEST_LIMIT,
        ),
        ('CBLC_PUBLIC_FIXED_INCOME_RESTRICTION_CONFIRM', GridCode.CBLC_PUBLIC_FIXED_INCOME_RESTRICTION_CONFIRM),
        ('CC_OPEN_CLOSE_NOTICE', GridCode.CC_OPEN_CLOSE_NOTICE),
        ('CC_INTERBANK_SETTLEMENT_SCHEDULE', GridCode.CC_INTERBANK_SETTLEMENT_SCHEDULE),
        ('CC_INTRABANK_SETTLEMENT_SCHEDULE', GridCode.CC_INTRABANK_SETTLEMENT_SCHEDULE),
        ('CC_CESSION_FILE_SCHEDULE_INTERBANK', GridCode.CC_CESSION_FILE_SCHEDULE_INTERBANK),
        ('CC_CESSION_FILE_SCHEDULE_INTRA', GridCode.CC_CESSION_FILE_SCHEDULE_INTRA),
        ('CCS_DAILY_UPDATE_FILE_RECEIPT', GridCode.CCS_DAILY_UPDATE_FILE_RECEIPT),
        ('CCS_DETAIL_REQUEST_MESSAGE', GridCode.CCS_DETAIL_REQUEST_MESSAGE),
        ('CCS_DETAIL_RESPONSE_MESSAGE', GridCode.CCS_DETAIL_RESPONSE_MESSAGE),
        ('CCS_REQUESTS_TO_BACEN', GridCode.CCS_REQUESTS_TO_BACEN),
        ('CCS_GRADE_CHANGE_NOTICE', GridCode.CCS_GRADE_CHANGE_NOTICE),
        ('CIR_GENERAL', GridCode.CIR_GENERAL),
        ('CIR_CUSTODIAN_SHIPMENTS', GridCode.CIR_CUSTODIAN_SHIPMENTS),
        ('CIR_QUERIES', GridCode.CIR_QUERIES),
        ('CIR_CASH_SHIPMENTS_FOR_EXAM', GridCode.CIR_CASH_SHIPMENTS_FOR_EXAM),
        ('CLI_INFO_REQUEST', GridCode.CLI_INFO_REQUEST),
        ('CLI_BOOK_TRANSFERS', GridCode.CLI_BOOK_TRANSFERS),
        ('CLI_INTERBANK_TRANSFERS', GridCode.CLI_INTERBANK_TRANSFERS),
        ('CLI_PAYMENT_DOCUMENT_TRANSFERS', GridCode.CLI_PAYMENT_DOCUMENT_TRANSFERS),
        ('CMP_COMPE_SETTLEMENT', GridCode.CMP_COMPE_SETTLEMENT),
        ('CTP_GENERAL', GridCode.CTP_GENERAL),
        ('CTP_GROSS_RECORDING_STR', GridCode.CTP_GROSS_RECORDING_STR),
        ('CTP_CETIP_WINDOW_RECORD', GridCode.CTP_CETIP_WINDOW_RECORD),
        ('CTP_CETIP_FINANCIAL_CONFIRM_FOR_CLEARING_BANKS', GridCode.CTP_CETIP_FINANCIAL_CONFIRM_FOR_CLEARING_BANKS),
        ('CTP_CENTRAL_RECORD_D0', GridCode.CTP_CENTRAL_RECORD_D0),
        ('CTP_CENTRAL_RECORD_D1', GridCode.CTP_CENTRAL_RECORD_D1),
        ('CTP_CETIP_DEBIT_TRANSFER_WINDOW', GridCode.CTP_CETIP_DEBIT_TRANSFER_WINDOW),
        ('CTP_CETIP_CREDIT_TRANSFER_WINDOW', GridCode.CTP_CETIP_CREDIT_TRANSFER_WINDOW),
        ('CTP_CENTRAL_COVERED_RECORD_D0', GridCode.CTP_CENTRAL_COVERED_RECORD_D0),
        ('CTP_CETIP_DEBIT_TRANSFER_BRUTA_STR', GridCode.CTP_CETIP_DEBIT_TRANSFER_BRUTA_STR),
        ('CTP_BILATERAL_RECORD', GridCode.CTP_BILATERAL_RECORD),
        ('CTP_CENTRAL_BILATERAL_RECORD', GridCode.CTP_CENTRAL_BILATERAL_RECORD),
        ('CTP_CETIP_DEBIT_TRANSFER_BILATERAL', GridCode.CTP_CETIP_DEBIT_TRANSFER_BILATERAL),
        ('CTP_REG_OPER_FILES_MORNING', GridCode.CTP_REG_OPER_FILES_MORNING),
        ('CTP_REG_OPER_FILES_AFTERNOON', GridCode.CTP_REG_OPER_FILES_AFTERNOON),
        ('CTP_FINANCIAL_CONFIRM_NO_SETTLEMENT_STR', GridCode.CTP_FINANCIAL_CONFIRM_NO_SETTLEMENT_STR),
        ('CTP_LIBERATE_D0_EVENTS_SELIC_DI', GridCode.CTP_LIBERATE_D0_EVENTS_SELIC_DI),
        ('CTP_RECORD_SCHEDULE_MESSAGE', GridCode.CTP_RECORD_SCHEDULE_MESSAGE),
        ('CTP_RECORD_SCHEDULE_MESSAGE_AFTERNOON', GridCode.CTP_RECORD_SCHEDULE_MESSAGE_AFTERNOON),
        ('CTP_RECORD_SCHEDULE_MESSAGE_NIGHT', GridCode.CTP_RECORD_SCHEDULE_MESSAGE_NIGHT),
        ('CTP_ACCESS_CONTROL_MAINTENANCE', GridCode.CTP_ACCESS_CONTROL_MAINTENANCE),
        ('CTP_RECORD_SCHEDULE_MESSAGE_MADRUGADA', GridCode.CTP_RECORD_SCHEDULE_MESSAGE_MADRUGADA),
        ('CTP_SCHEDULE_TRANSF_FILES_NIGHT_IDENTIFICATION', GridCode.CTP_SCHEDULE_TRANSF_FILES_NIGHT_IDENTIFICATION),
        ('DDA_PAYER_MAINTENANCE_BY_MESSAGE', GridCode.DDA_PAYER_MAINTENANCE_BY_MESSAGE),
        ('DDA_PAYER_MAINTENANCE_BY_FILE', GridCode.DDA_PAYER_MAINTENANCE_BY_FILE),
        ('DDA_QUERIES_AND_STATEMENTS', GridCode.DDA_QUERIES_AND_STATEMENTS),
        ('DDA_CALC_VALUE_NEXT_BUSINESS_DAY', GridCode.DDA_CALC_VALUE_NEXT_BUSINESS_DAY),
        ('DDA_BILL_MAINTENANCE_BY_MESSAGE', GridCode.DDA_BILL_MAINTENANCE_BY_MESSAGE),
        ('DDA_BILL_MAINTENANCE_BY_FILE', GridCode.DDA_BILL_MAINTENANCE_BY_FILE),
        ('DDA_BENEFICIARIES_BY_MESSAGE', GridCode.DDA_BENEFICIARIES_BY_MESSAGE),
        ('DDA_BENEFICIARIES_BY_FILE', GridCode.DDA_BENEFICIARIES_BY_FILE),
        ('DDA_LOW_BY_MESSAGE', GridCode.DDA_LOW_BY_MESSAGE),
        ('DDA_LOW_BY_FILE', GridCode.DDA_LOW_BY_FILE),
        ('DDA_LOW_CONTINGENCY', GridCode.DDA_LOW_CONTINGENCY),
        ('DDA_PAYMENT_QUERY', GridCode.DDA_PAYMENT_QUERY),
        ('GEN_GENERAL', GridCode.GEN_GENERAL),
        ('GEN_CONNECTION_CERTIFICATION', GridCode.GEN_CONNECTION_CERTIFICATION),
        ('LDL_GENERAL', GridCode.LDL_GENERAL),
        ('LDL_CREDITS_TO_CHAMBER', GridCode.LDL_CREDITS_TO_CHAMBER),
        ('LFL_FINANCIAL_MOVEMENTS', GridCode.LFL_FINANCIAL_MOVEMENTS),
        ('LFL_QUERIES', GridCode.LFL_QUERIES),
        ('LFL_COLLATERAL_WITHDRAWAL_REQUEST', GridCode.LFL_COLLATERAL_WITHDRAWAL_REQUEST),
        ('LPI_PAYMENTS_INSTANT_ACCOUNT_WITHDRAWALS', GridCode.LPI_PAYMENTS_INSTANT_ACCOUNT_WITHDRAWALS),
        ('LPI_PAYMENTS_INSTANT_ACCOUNT_DEPOSITS', GridCode.LPI_PAYMENTS_INSTANT_ACCOUNT_DEPOSITS),
        ('LTR_GENERAL', GridCode.LTR_GENERAL),
        ('PAG_MAIN_CYCLE_01_MANDATORY_DEPOSIT', GridCode.PAG_MAIN_CYCLE_01_MANDATORY_DEPOSIT),
        ('PAG_MAIN_CYCLE_01_MESSAGE_SEND_RECEIVE_PAYMENT', GridCode.PAG_MAIN_CYCLE_01_MESSAGE_SEND_RECEIVE_PAYMENT),
        ('PAG_MAIN_CYCLE_01_SETTLEMENT', GridCode.PAG_MAIN_CYCLE_01_SETTLEMENT),
        ('PAG_COMPLEMENTARY_CANCEL_PAYMENT_MSG', GridCode.PAG_COMPLEMENTARY_CANCEL_PAYMENT_MSG),
        ('PAG_COMPLEMENTARY_MANDATORY_DEPOSIT', GridCode.PAG_COMPLEMENTARY_MANDATORY_DEPOSIT),
        ('PAG_COMPLEMENTARY_SETTLEMENT', GridCode.PAG_COMPLEMENTARY_SETTLEMENT),
        ('PAG_REAL_TIME_GROSS_SETTLEMENT_SLC', GridCode.PAG_REAL_TIME_GROSS_SETTLEMENT_SLC),
        ('PAGD1_MAIN_CYCLE1_MANDATORY_DEPOSIT', GridCode.PAGD1_MAIN_CYCLE1_MANDATORY_DEPOSIT),
        ('PAGD2_MAIN_CYCLE1_PROCESSING_PERIOD', GridCode.PAGD2_MAIN_CYCLE1_PROCESSING_PERIOD),
        ('PAGD3_MAIN_CYCLE1_SETTLEMENT', GridCode.PAGD3_MAIN_CYCLE1_SETTLEMENT),
        ('PAGE1_MAIN_CYCLE2_MANDATORY_DEPOSIT', GridCode.PAGE1_MAIN_CYCLE2_MANDATORY_DEPOSIT),
        ('PAGE2_MAIN_CYCLE2_PROCESSING_PERIOD', GridCode.PAGE2_MAIN_CYCLE2_PROCESSING_PERIOD),
        ('PAGE3_MAIN_CYCLE2_SETTLEMENT', GridCode.PAGE3_MAIN_CYCLE2_SETTLEMENT),
        ('RCO_GENERAL', GridCode.RCO_GENERAL),
        ('RCO_QUERIES', GridCode.RCO_QUERIES),
        ('RDC_GENERAL', GridCode.RDC_GENERAL),
        ('RDC_INTRADAY_GRANTED_AND_SETTLEMENTS', GridCode.RDC_INTRADAY_GRANTED_AND_SETTLEMENTS),
        ('RDC_ONE_DAY_TERM_GRANTED', GridCode.RDC_ONE_DAY_TERM_GRANTED),
        ('SEL_GENERAL', GridCode.SEL_GENERAL),
        ('SEL_TERM_REGISTRATION', GridCode.SEL_TERM_REGISTRATION),
        ('SEL_SPI_LIQUIDITY_REQUESTS', GridCode.SEL_SPI_LIQUIDITY_REQUESTS),
        ('SEL_NOTICE', GridCode.SEL_NOTICE),
        ('SLB_GENERAL', GridCode.SLB_GENERAL),
        ('SLB_QUERIES', GridCode.SLB_QUERIES),
        ('SLB_D0_MATURITY_CHARGES', GridCode.SLB_D0_MATURITY_CHARGES),
        ('SME_GENERAL', GridCode.SME_GENERAL),
        ('SME_QUERIES', GridCode.SME_QUERIES),
        ('SML_OPERATIONS', GridCode.SML_OPERATIONS),
        ('SML_CREDITS', GridCode.SML_CREDITS),
        ('STR_GENERAL', GridCode.STR_GENERAL),
        ('STR_CUSTOMER_ACCOUNT_INTERBANK_ENTRIES', GridCode.STR_CUSTOMER_ACCOUNT_INTERBANK_ENTRIES),
        ('STR_QUERIES', GridCode.STR_QUERIES),
        ('TEC_CYCLE1_START', GridCode.TEC_CYCLE1_START),
        ('TEC_CYCLE1_DEBTORS_PAYMENT', GridCode.TEC_CYCLE1_DEBTORS_PAYMENT),
        ('TEC_CYCLE1_CREDITORS_PAYMENT', GridCode.TEC_CYCLE1_CREDITORS_PAYMENT),
        ('TEC_CYCLE2_START', GridCode.TEC_CYCLE2_START),
        ('TEC_CYCLE2_DEBTORS_PAYMENT', GridCode.TEC_CYCLE2_DEBTORS_PAYMENT),
        ('TEC_CYCLE2_CREDITORS_PAYMENT', GridCode.TEC_CYCLE2_CREDITORS_PAYMENT),
        ('TES_GENERAL', GridCode.TES_GENERAL),
        ('TES_QUERY', GridCode.TES_QUERY),
        ('TES_TREASURY_INFORMATION', GridCode.TES_TREASURY_INFORMATION),
        ('TES_COLLECTION_QUERY', GridCode.TES_COLLECTION_QUERY),
        ('TES_RETURN_OF_COLLECTION', GridCode.TES_RETURN_OF_COLLECTION),
    ],
)
def test_grid_code_accepts_exact_values(input_value: str, expected_enum: GridCode) -> None:
    assert GridCode(input_value) is expected_enum


@pytest.mark.parametrize(
    ('input_value', 'expected_enum'),
    [
        (GridCode.PAYMENT_ORDER_SCHEDULING, 'AGE01'),
        (GridCode.SCHEDULED_PAYMENT_ORDER_SETTLEMENT, 'AGE02'),
        (GridCode.BMA_OPERATIONS, 'BMA01'),
        (GridCode.BMA_ASSET_MOVEMENT, 'BMA02'),
        (GridCode.BMA_REPO_D0_DM, 'BMA05'),
        (GridCode.BMA_REPO_DN_DM, 'BMA06'),
        (GridCode.BMA_SPOT_TRADES_D0, 'BMA07'),
        (GridCode.BMA_FORWARD_TRADES_DN, 'BMA08'),
        (GridCode.BMA_PHONE_ORDER_RELOCATION_REJECTION_D0, 'BMA09'),
        (GridCode.BMA_PHONE_ORDER_RELOCATION_REJECTION_DN, 'BMA10'),
        (GridCode.BMA_COVERED_OPERATIONS_SPEC_D0, 'BMA11'),
        (GridCode.BMA_COLLATERAL_SPEC_REPO_UNCOMP_D0, 'BMA12'),
        (GridCode.BMA_COLLATERAL_SPEC_REPO_UNCOMP_DN, 'BMA13'),
        (GridCode.BMA_COLLATERAL_SPEC_REPO_COMP, 'BMA14'),
        (GridCode.BMA_DIRECTION_ACCEPTANCE, 'BMA15'),
        (GridCode.BMA_BL_CONFIRM_LIQUID_RESULT, 'BMA16'),
        (GridCode.BMA_PARTICIPANT_DELIVERY_PAYMENT, 'BMA17'),
        (GridCode.BMA_CLEARINGHOUSE_DELIVERY_PAYMENT, 'BMA18'),
        (GridCode.BMA_REQUEST_DELIVERY_RESTRICTION, 'BMA19'),
        (GridCode.BMA_CONFIRM_RELEASE_DELIVERY_RESTRICTION, 'BMA20'),
        (GridCode.BMA_PARTIAL_DELIVERY_REQUEST, 'BMA21'),
        (GridCode.BMA_PAYMENT_WITH_COLLATERAL, 'BMA22'),
        (GridCode.BMA_COLLATERAL_RESTORATION_REQUEST, 'BMA23'),
        (GridCode.BMA_PAYMENT_DELIVERY_REGULARIZATION_D0, 'BMA24'),
        (GridCode.BMA_PAYMENT_DELIVERY_REGULARIZATION_D1, 'BMA25'),
        (GridCode.BMC_GENERAL, 'BMC01'),
        (GridCode.BMD_GENERAL, 'BMD01'),
        (GridCode.BMD_DERIVATIVES_OPENING, 'BMD05'),
        (GridCode.BMD_PROVISIONAL_NETTING, 'BMD10'),
        (GridCode.BMD_FINAL_NETTING, 'BMD15'),
        (GridCode.BMD_CLEARING_BANK_CONFIRMATION, 'BMD20'),
        (GridCode.BMD_RECEIPT_OF_PAYMENTS, 'BMD25'),
        (GridCode.BMD_PAYMENT_SETTLEMENT, 'BMD30'),
        (GridCode.BMD_CLOSE_MESSAGE, 'BMD35'),
        (GridCode.BMD_COLLATERAL_DEPOSIT, 'BMD40'),
        (GridCode.BMD_COLLATERAL_DEPOSIT_D1, 'BMD45'),
        (GridCode.BVF_GENERAL, 'BVF01'),
        (GridCode.BVF_UNIFIED_CE_OPENING, 'BVF05'),
        (GridCode.BVF_PROVISIONAL_NETTING, 'BVF10'),
        (GridCode.BVF_FINAL_NETTING, 'BVF15'),
        (GridCode.BVF_CLEARING_BANK_CONFIRMATION, 'BVF20'),
        (GridCode.BVF_RECEIPT_OF_PAYMENTS, 'BVF25'),
        (GridCode.BVF_PAYMENT_SETTLEMENT, 'BVF30'),
        (GridCode.BVF_CLOSE_MESSAGE, 'BVF35'),
        (GridCode.BVF_COLLATERAL_DEPOSIT, 'BVF40'),
        (GridCode.BVF_COLLATERAL_DEPOSIT_D1, 'BVF45'),
        (GridCode.FX_PRIMARY_MARKET, 'CAM04'),
        (GridCode.FX_INTERBANK_MARKET, 'CAM05'),
        (GridCode.FX_SYSTEM_QUERIES, 'CAM06'),
        (GridCode.FX_SYSTEM_SERVICES, 'CAM07'),
        (GridCode.CBLC_GENERAL, 'CBL01'),
        (GridCode.CBLC_FIXED_INCOME_VARIABLE_INFORM_SETTLEMENT_03, 'CBL03'),
        (GridCode.CBLC_FIXED_INCOME_VARIABLE_INFORM_SETTLEMENT_04, 'CBL04'),
        (GridCode.CBLC_FIXED_INCOME_VARIABLE_BACEN, 'CBL05'),
        (GridCode.CBLC_IF_CONFIRM_DIVERGE_SETTLEMENT, 'CBL06'),
        (GridCode.CBLC_DISCREPANCY_ADJUSTMENT_LIMIT, 'CBL07'),
        (GridCode.CBLC_IF_REQUEST_RESERVE_TRANSFER_FOR_DEBIT_SETTLEMENT, 'CBL08'),
        (GridCode.CBLC_DVP_CREDITOR_SETTLEMENT_AND_DELIVERY, 'CBL09'),
        (GridCode.CBLC_CUSTODY_PAYMENT_EVENTS, 'CBL20'),
        (GridCode.CBLC_CUSTODY_IF_REQUEST_TRANSFER, 'CBL21'),
        (GridCode.CBLC_CUSTODY_REPASS_EVENTS, 'CBL22'),
        (GridCode.CBLC_EQUITY_SETTLEMENT_SPEC, 'CBL30'),
        (GridCode.CBLC_EQUITY_MOVEMENT_AUTHORIZATION, 'CBL31'),
        (GridCode.CBLC_EQUITY_DELIVERY_BY_DEBTORS, 'CBL32'),
        (GridCode.CBLC_EQUITY_DELIVERY_FAILURE_HANDLING, 'CBL33'),
        (GridCode.CBLC_EQUITY_RESTRICTION_REQUEST_LIMIT, 'CBL35'),
        (GridCode.CBLC_EQUITY_DELIVERY_BY_CBLC, 'CBL36'),
        (GridCode.CBLC_EQUITY_RESTRICTION_RELEASE, 'CBL37'),
        (GridCode.CBLC_PRIVATE_FIXED_INCOME_NEGOTIATION_LIMIT_D0, 'CBL50'),
        (GridCode.CBLC_PRIVATE_FIXED_INCOME_CANCEL_LIMIT_D0, 'CBL51'),
        (GridCode.CBLC_PRIVATE_FIXED_INCOME_SPEC_LIMIT_D0, 'CBL52'),
        (GridCode.CBLC_PRIVATE_FIXED_INCOME_DIRECTION_AUTH_D0, 'CBL53'),
        (GridCode.CBLC_PRIVATE_FIXED_INCOME_NEGOTIATION_LIMIT_D1, 'CBL54'),
        (GridCode.CBLC_PRIVATE_FIXED_INCOME_CANCEL_LIMIT_D1, 'CBL55'),
        (GridCode.CBLC_PRIVATE_FIXED_INCOME_SPEC_LIMIT_D1, 'CBL56'),
        (GridCode.CBLC_PRIVATE_FIXED_INCOME_DIRECTION_AUTH_D1, 'CBL57'),
        (GridCode.CBLC_PRIVATE_FIXED_INCOME_CLEARING, 'CBL58'),
        (GridCode.CBLC_PRIVATE_FIXED_INCOME_DELIVERY, 'CBL59'),
        (GridCode.CBLC_PRIVATE_FIXED_INCOME_DELIVERY_FAILURE, 'CBL60'),
        (GridCode.CBLC_PRIVATE_FIXED_INCOME_RESTRICTION_REQUEST_LIMIT, 'CBL61'),
        (GridCode.CBLC_PRIVATE_FIXED_INCOME_RESTRICTION_CONFIRM, 'CBL62'),
        (GridCode.CBLC_GROSS_SETTLEMENT_PREPARE_SEND_LTR_VALUES, 'CBL65'),
        (GridCode.CBLC_GROSS_SETTLEMENT_IF_CONFIRM_OR_DIVERGE_LTR, 'CBL66'),
        (GridCode.CBLC_GROSS_SETTLEMENT_IF_REQUEST_TRANSFER_RESERVES, 'CBL67'),
        (GridCode.CBLC_GROSS_SETTLEMENT_CREDITOR_RESULTS, 'CBL68'),
        (GridCode.CBLC_COLLATERAL_MOVEMENT, 'CBL75'),
        (GridCode.CBLC_LIMITS_DEALLOCATION, 'CBL76'),
        (GridCode.CBLC_PUBLIC_TITLES_TRANSFER_FOR_MARGIN_REVERSAL, 'CBL77'),
        (GridCode.CBLC_PUBLIC_FIXED_INCOME_NEGOTIATION_LIMIT_D0, 'CBL81'),
        (GridCode.CBLC_PUBLIC_FIXED_INCOME_CANCEL_LIMIT_D0, 'CBL82'),
        (GridCode.CBLC_PUBLIC_FIXED_INCOME_SPEC_LIMIT_D0, 'CBL83'),
        (GridCode.CBLC_PUBLIC_FIXED_INCOME_DIRECTION_AUTH_D0, 'CBL84'),
        (GridCode.CBLC_PUBLIC_FIXED_INCOME_NEGOTIATION_LIMIT_D1, 'CBL85'),
        (GridCode.CBLC_PUBLIC_FIXED_INCOME_CANCEL_LIMIT_D1, 'CBL86'),
        (GridCode.CBLC_PUBLIC_FIXED_INCOME_SPEC_LIMIT_D1, 'CBL87'),
        (GridCode.CBLC_PUBLIC_FIXED_INCOME_DIRECTION_AUTH_D1, 'CBL88'),
        (GridCode.CBLC_PUBLIC_FIXED_INCOME_CLEARING, 'CBL89'),
        (GridCode.CBLC_PUBLIC_FIXED_INCOME_DELIVERY, 'CBL90'),
        (GridCode.CBLC_PUBLIC_FIXED_INCOME_DELIVERY_FAILURE, 'CBL91'),
        (GridCode.CBLC_PUBLIC_FIXED_INCOME_RESTRICTION_REQUEST_LIMIT, 'CBL92'),
        (GridCode.CBLC_PUBLIC_FIXED_INCOME_RESTRICTION_CONFIRM, 'CBL93'),
        (GridCode.CC_OPEN_CLOSE_NOTICE, 'CC300'),
        (GridCode.CC_INTERBANK_SETTLEMENT_SCHEDULE, 'CC301'),
        (GridCode.CC_INTRABANK_SETTLEMENT_SCHEDULE, 'CC302'),
        (GridCode.CC_CESSION_FILE_SCHEDULE_INTERBANK, 'CC303'),
        (GridCode.CC_CESSION_FILE_SCHEDULE_INTRA, 'CC304'),
        (GridCode.CCS_DAILY_UPDATE_FILE_RECEIPT, 'CCS01'),
        (GridCode.CCS_DETAIL_REQUEST_MESSAGE, 'CCS02'),
        (GridCode.CCS_DETAIL_RESPONSE_MESSAGE, 'CCS03'),
        (GridCode.CCS_REQUESTS_TO_BACEN, 'CCS04'),
        (GridCode.CCS_GRADE_CHANGE_NOTICE, 'CCS05'),
        (GridCode.CIR_GENERAL, 'CIR01'),
        (GridCode.CIR_CUSTODIAN_SHIPMENTS, 'CIR02'),
        (GridCode.CIR_QUERIES, 'CIR03'),
        (GridCode.CIR_CASH_SHIPMENTS_FOR_EXAM, 'CIR04'),
        (GridCode.CLI_INFO_REQUEST, 'CLI01'),
        (GridCode.CLI_BOOK_TRANSFERS, 'CLI02'),
        (GridCode.CLI_INTERBANK_TRANSFERS, 'CLI03'),
        (GridCode.CLI_PAYMENT_DOCUMENT_TRANSFERS, 'CLI04'),
        (GridCode.CMP_COMPE_SETTLEMENT, 'CMP03'),
        (GridCode.CTP_GENERAL, 'CTP01'),
        (GridCode.CTP_GROSS_RECORDING_STR, 'CTP02'),
        (GridCode.CTP_CETIP_WINDOW_RECORD, 'CTP03'),
        (GridCode.CTP_CETIP_FINANCIAL_CONFIRM_FOR_CLEARING_BANKS, 'CTP04'),
        (GridCode.CTP_CENTRAL_RECORD_D0, 'CTP05'),
        (GridCode.CTP_CENTRAL_RECORD_D1, 'CTP06'),
        (GridCode.CTP_CETIP_DEBIT_TRANSFER_WINDOW, 'CTP07'),
        (GridCode.CTP_CETIP_CREDIT_TRANSFER_WINDOW, 'CTP08'),
        (GridCode.CTP_CENTRAL_COVERED_RECORD_D0, 'CTP09'),
        (GridCode.CTP_CETIP_DEBIT_TRANSFER_BRUTA_STR, 'CTP10'),
        (GridCode.CTP_BILATERAL_RECORD, 'CTP11'),
        (GridCode.CTP_CENTRAL_BILATERAL_RECORD, 'CTP12'),
        (GridCode.CTP_CETIP_DEBIT_TRANSFER_BILATERAL, 'CTP13'),
        (GridCode.CTP_REG_OPER_FILES_MORNING, 'CTP17'),
        (GridCode.CTP_REG_OPER_FILES_AFTERNOON, 'CTP18'),
        (GridCode.CTP_FINANCIAL_CONFIRM_NO_SETTLEMENT_STR, 'CTP23'),
        (GridCode.CTP_LIBERATE_D0_EVENTS_SELIC_DI, 'CTP24'),
        (GridCode.CTP_RECORD_SCHEDULE_MESSAGE, 'CTP25'),
        (GridCode.CTP_RECORD_SCHEDULE_MESSAGE_AFTERNOON, 'CTP26'),
        (GridCode.CTP_RECORD_SCHEDULE_MESSAGE_NIGHT, 'CTP27'),
        (GridCode.CTP_ACCESS_CONTROL_MAINTENANCE, 'CTP28'),
        (GridCode.CTP_RECORD_SCHEDULE_MESSAGE_MADRUGADA, 'CTP29'),
        (GridCode.CTP_SCHEDULE_TRANSF_FILES_NIGHT_IDENTIFICATION, 'CTP31'),
        (GridCode.DDA_PAYER_MAINTENANCE_BY_MESSAGE, 'DDA01'),
        (GridCode.DDA_PAYER_MAINTENANCE_BY_FILE, 'DDA02'),
        (GridCode.DDA_QUERIES_AND_STATEMENTS, 'DDA03'),
        (GridCode.DDA_CALC_VALUE_NEXT_BUSINESS_DAY, 'DDA04'),
        (GridCode.DDA_BILL_MAINTENANCE_BY_MESSAGE, 'DDA05'),
        (GridCode.DDA_BILL_MAINTENANCE_BY_FILE, 'DDA06'),
        (GridCode.DDA_BENEFICIARIES_BY_MESSAGE, 'DDA07'),
        (GridCode.DDA_BENEFICIARIES_BY_FILE, 'DDA08'),
        (GridCode.DDA_LOW_BY_MESSAGE, 'DDA09'),
        (GridCode.DDA_LOW_BY_FILE, 'DDA10'),
        (GridCode.DDA_LOW_CONTINGENCY, 'DDA11'),
        (GridCode.DDA_PAYMENT_QUERY, 'DDA12'),
        (GridCode.GEN_GENERAL, 'GEN01'),
        (GridCode.GEN_CONNECTION_CERTIFICATION, 'GEN02'),
        (GridCode.LDL_GENERAL, 'LDL01'),
        (GridCode.LDL_CREDITS_TO_CHAMBER, 'LDL04'),
        (GridCode.LFL_FINANCIAL_MOVEMENTS, 'LFL01'),
        (GridCode.LFL_QUERIES, 'LFL02'),
        (GridCode.LFL_COLLATERAL_WITHDRAWAL_REQUEST, 'LFL03'),
        (GridCode.LPI_PAYMENTS_INSTANT_ACCOUNT_WITHDRAWALS, 'LPI01'),
        (GridCode.LPI_PAYMENTS_INSTANT_ACCOUNT_DEPOSITS, 'LPI02'),
        (GridCode.LTR_GENERAL, 'LTR01'),
        (GridCode.PAG_MAIN_CYCLE_01_MANDATORY_DEPOSIT, 'PAG01'),
        (GridCode.PAG_MAIN_CYCLE_01_MESSAGE_SEND_RECEIVE_PAYMENT, 'PAG02'),
        (GridCode.PAG_MAIN_CYCLE_01_SETTLEMENT, 'PAG03'),
        (GridCode.PAG_COMPLEMENTARY_CANCEL_PAYMENT_MSG, 'PAG91'),
        (GridCode.PAG_COMPLEMENTARY_MANDATORY_DEPOSIT, 'PAG92'),
        (GridCode.PAG_COMPLEMENTARY_SETTLEMENT, 'PAG93'),
        (GridCode.PAG_REAL_TIME_GROSS_SETTLEMENT_SLC, 'PAG94'),
        (GridCode.PAGD1_MAIN_CYCLE1_MANDATORY_DEPOSIT, 'PAGD1'),
        (GridCode.PAGD2_MAIN_CYCLE1_PROCESSING_PERIOD, 'PAGD2'),
        (GridCode.PAGD3_MAIN_CYCLE1_SETTLEMENT, 'PAGD3'),
        (GridCode.PAGE1_MAIN_CYCLE2_MANDATORY_DEPOSIT, 'PAGE1'),
        (GridCode.PAGE2_MAIN_CYCLE2_PROCESSING_PERIOD, 'PAGE2'),
        (GridCode.PAGE3_MAIN_CYCLE2_SETTLEMENT, 'PAGE3'),
        (GridCode.RCO_GENERAL, 'RCO01'),
        (GridCode.RCO_QUERIES, 'RCO02'),
        (GridCode.RDC_GENERAL, 'RDC01'),
        (GridCode.RDC_INTRADAY_GRANTED_AND_SETTLEMENTS, 'RDC02'),
        (GridCode.RDC_ONE_DAY_TERM_GRANTED, 'RDC03'),
        (GridCode.SEL_GENERAL, 'SEL01'),
        (GridCode.SEL_TERM_REGISTRATION, 'SEL03'),
        (GridCode.SEL_SPI_LIQUIDITY_REQUESTS, 'SEL04'),
        (GridCode.SEL_NOTICE, 'SEL05'),
        (GridCode.SLB_GENERAL, 'SLB01'),
        (GridCode.SLB_QUERIES, 'SLB02'),
        (GridCode.SLB_D0_MATURITY_CHARGES, 'SLB04'),
        (GridCode.SME_GENERAL, 'SME01'),
        (GridCode.SME_QUERIES, 'SME02'),
        (GridCode.SML_OPERATIONS, 'SML01'),
        (GridCode.SML_CREDITS, 'SML02'),
        (GridCode.STR_GENERAL, 'STR01'),
        (GridCode.STR_CUSTOMER_ACCOUNT_INTERBANK_ENTRIES, 'STR02'),
        (GridCode.STR_QUERIES, 'STR03'),
        (GridCode.TEC_CYCLE1_START, 'TEC01'),
        (GridCode.TEC_CYCLE1_DEBTORS_PAYMENT, 'TEC02'),
        (GridCode.TEC_CYCLE1_CREDITORS_PAYMENT, 'TEC03'),
        (GridCode.TEC_CYCLE2_START, 'TEC04'),
        (GridCode.TEC_CYCLE2_DEBTORS_PAYMENT, 'TEC05'),
        (GridCode.TEC_CYCLE2_CREDITORS_PAYMENT, 'TEC06'),
        (GridCode.TES_GENERAL, 'TES01'),
        (GridCode.TES_QUERY, 'TES04'),
        (GridCode.TES_TREASURY_INFORMATION, 'TES10'),
        (GridCode.TES_COLLECTION_QUERY, 'TES11'),
        (GridCode.TES_RETURN_OF_COLLECTION, 'TES12'),
    ],
)
def test_grid_code_values_to_xml_value(input_value: GridCode, expected_enum: str) -> None:
    assert input_value.to_xml_value() == expected_enum


@pytest.mark.parametrize(
    ('input_value', 'expected_enum'),
    [
        ('AGE01', GridCode.PAYMENT_ORDER_SCHEDULING),
        ('AGE02', GridCode.SCHEDULED_PAYMENT_ORDER_SETTLEMENT),
        ('BMA01', GridCode.BMA_OPERATIONS),
        ('BMA02', GridCode.BMA_ASSET_MOVEMENT),
        ('BMA05', GridCode.BMA_REPO_D0_DM),
        ('BMA06', GridCode.BMA_REPO_DN_DM),
        ('BMA07', GridCode.BMA_SPOT_TRADES_D0),
        ('BMA08', GridCode.BMA_FORWARD_TRADES_DN),
        ('BMA09', GridCode.BMA_PHONE_ORDER_RELOCATION_REJECTION_D0),
        ('BMA10', GridCode.BMA_PHONE_ORDER_RELOCATION_REJECTION_DN),
        ('BMA11', GridCode.BMA_COVERED_OPERATIONS_SPEC_D0),
        ('BMA12', GridCode.BMA_COLLATERAL_SPEC_REPO_UNCOMP_D0),
        ('BMA13', GridCode.BMA_COLLATERAL_SPEC_REPO_UNCOMP_DN),
        ('BMA14', GridCode.BMA_COLLATERAL_SPEC_REPO_COMP),
        ('BMA15', GridCode.BMA_DIRECTION_ACCEPTANCE),
        ('BMA16', GridCode.BMA_BL_CONFIRM_LIQUID_RESULT),
        ('BMA17', GridCode.BMA_PARTICIPANT_DELIVERY_PAYMENT),
        ('BMA18', GridCode.BMA_CLEARINGHOUSE_DELIVERY_PAYMENT),
        ('BMA19', GridCode.BMA_REQUEST_DELIVERY_RESTRICTION),
        ('BMA20', GridCode.BMA_CONFIRM_RELEASE_DELIVERY_RESTRICTION),
        ('BMA21', GridCode.BMA_PARTIAL_DELIVERY_REQUEST),
        ('BMA22', GridCode.BMA_PAYMENT_WITH_COLLATERAL),
        ('BMA23', GridCode.BMA_COLLATERAL_RESTORATION_REQUEST),
        ('BMA24', GridCode.BMA_PAYMENT_DELIVERY_REGULARIZATION_D0),
        ('BMA25', GridCode.BMA_PAYMENT_DELIVERY_REGULARIZATION_D1),
        ('BMC01', GridCode.BMC_GENERAL),
        ('BMD01', GridCode.BMD_GENERAL),
        ('BMD05', GridCode.BMD_DERIVATIVES_OPENING),
        ('BMD10', GridCode.BMD_PROVISIONAL_NETTING),
        ('BMD15', GridCode.BMD_FINAL_NETTING),
        ('BMD20', GridCode.BMD_CLEARING_BANK_CONFIRMATION),
        ('BMD25', GridCode.BMD_RECEIPT_OF_PAYMENTS),
        ('BMD30', GridCode.BMD_PAYMENT_SETTLEMENT),
        ('BMD35', GridCode.BMD_CLOSE_MESSAGE),
        ('BMD40', GridCode.BMD_COLLATERAL_DEPOSIT),
        ('BMD45', GridCode.BMD_COLLATERAL_DEPOSIT_D1),
        ('BVF01', GridCode.BVF_GENERAL),
        ('BVF05', GridCode.BVF_UNIFIED_CE_OPENING),
        ('BVF10', GridCode.BVF_PROVISIONAL_NETTING),
        ('BVF15', GridCode.BVF_FINAL_NETTING),
        ('BVF20', GridCode.BVF_CLEARING_BANK_CONFIRMATION),
        ('BVF25', GridCode.BVF_RECEIPT_OF_PAYMENTS),
        ('BVF30', GridCode.BVF_PAYMENT_SETTLEMENT),
        ('BVF35', GridCode.BVF_CLOSE_MESSAGE),
        ('BVF40', GridCode.BVF_COLLATERAL_DEPOSIT),
        ('BVF45', GridCode.BVF_COLLATERAL_DEPOSIT_D1),
        ('CAM04', GridCode.FX_PRIMARY_MARKET),
        ('CAM05', GridCode.FX_INTERBANK_MARKET),
        ('CAM06', GridCode.FX_SYSTEM_QUERIES),
        ('CAM07', GridCode.FX_SYSTEM_SERVICES),
        ('CBL01', GridCode.CBLC_GENERAL),
        ('CBL03', GridCode.CBLC_FIXED_INCOME_VARIABLE_INFORM_SETTLEMENT_03),
        ('CBL04', GridCode.CBLC_FIXED_INCOME_VARIABLE_INFORM_SETTLEMENT_04),
        ('CBL05', GridCode.CBLC_FIXED_INCOME_VARIABLE_BACEN),
        ('CBL06', GridCode.CBLC_IF_CONFIRM_DIVERGE_SETTLEMENT),
        ('CBL07', GridCode.CBLC_DISCREPANCY_ADJUSTMENT_LIMIT),
        ('CBL08', GridCode.CBLC_IF_REQUEST_RESERVE_TRANSFER_FOR_DEBIT_SETTLEMENT),
        ('CBL09', GridCode.CBLC_DVP_CREDITOR_SETTLEMENT_AND_DELIVERY),
        ('CBL20', GridCode.CBLC_CUSTODY_PAYMENT_EVENTS),
        ('CBL21', GridCode.CBLC_CUSTODY_IF_REQUEST_TRANSFER),
        ('CBL22', GridCode.CBLC_CUSTODY_REPASS_EVENTS),
        ('CBL30', GridCode.CBLC_EQUITY_SETTLEMENT_SPEC),
        ('CBL31', GridCode.CBLC_EQUITY_MOVEMENT_AUTHORIZATION),
        ('CBL32', GridCode.CBLC_EQUITY_DELIVERY_BY_DEBTORS),
        ('CBL33', GridCode.CBLC_EQUITY_DELIVERY_FAILURE_HANDLING),
        ('CBL35', GridCode.CBLC_EQUITY_RESTRICTION_REQUEST_LIMIT),
        ('CBL36', GridCode.CBLC_EQUITY_DELIVERY_BY_CBLC),
        ('CBL37', GridCode.CBLC_EQUITY_RESTRICTION_RELEASE),
        ('CBL50', GridCode.CBLC_PRIVATE_FIXED_INCOME_NEGOTIATION_LIMIT_D0),
        ('CBL51', GridCode.CBLC_PRIVATE_FIXED_INCOME_CANCEL_LIMIT_D0),
        ('CBL52', GridCode.CBLC_PRIVATE_FIXED_INCOME_SPEC_LIMIT_D0),
        ('CBL53', GridCode.CBLC_PRIVATE_FIXED_INCOME_DIRECTION_AUTH_D0),
        ('CBL54', GridCode.CBLC_PRIVATE_FIXED_INCOME_NEGOTIATION_LIMIT_D1),
        ('CBL55', GridCode.CBLC_PRIVATE_FIXED_INCOME_CANCEL_LIMIT_D1),
        ('CBL56', GridCode.CBLC_PRIVATE_FIXED_INCOME_SPEC_LIMIT_D1),
        ('CBL57', GridCode.CBLC_PRIVATE_FIXED_INCOME_DIRECTION_AUTH_D1),
        ('CBL58', GridCode.CBLC_PRIVATE_FIXED_INCOME_CLEARING),
        ('CBL59', GridCode.CBLC_PRIVATE_FIXED_INCOME_DELIVERY),
        ('CBL60', GridCode.CBLC_PRIVATE_FIXED_INCOME_DELIVERY_FAILURE),
        ('CBL61', GridCode.CBLC_PRIVATE_FIXED_INCOME_RESTRICTION_REQUEST_LIMIT),
        ('CBL62', GridCode.CBLC_PRIVATE_FIXED_INCOME_RESTRICTION_CONFIRM),
        ('CBL65', GridCode.CBLC_GROSS_SETTLEMENT_PREPARE_SEND_LTR_VALUES),
        ('CBL66', GridCode.CBLC_GROSS_SETTLEMENT_IF_CONFIRM_OR_DIVERGE_LTR),
        ('CBL67', GridCode.CBLC_GROSS_SETTLEMENT_IF_REQUEST_TRANSFER_RESERVES),
        ('CBL68', GridCode.CBLC_GROSS_SETTLEMENT_CREDITOR_RESULTS),
        ('CBL75', GridCode.CBLC_COLLATERAL_MOVEMENT),
        ('CBL76', GridCode.CBLC_LIMITS_DEALLOCATION),
        ('CBL77', GridCode.CBLC_PUBLIC_TITLES_TRANSFER_FOR_MARGIN_REVERSAL),
        ('CBL81', GridCode.CBLC_PUBLIC_FIXED_INCOME_NEGOTIATION_LIMIT_D0),
        ('CBL82', GridCode.CBLC_PUBLIC_FIXED_INCOME_CANCEL_LIMIT_D0),
        ('CBL83', GridCode.CBLC_PUBLIC_FIXED_INCOME_SPEC_LIMIT_D0),
        ('CBL84', GridCode.CBLC_PUBLIC_FIXED_INCOME_DIRECTION_AUTH_D0),
        ('CBL85', GridCode.CBLC_PUBLIC_FIXED_INCOME_NEGOTIATION_LIMIT_D1),
        ('CBL86', GridCode.CBLC_PUBLIC_FIXED_INCOME_CANCEL_LIMIT_D1),
        ('CBL87', GridCode.CBLC_PUBLIC_FIXED_INCOME_SPEC_LIMIT_D1),
        ('CBL88', GridCode.CBLC_PUBLIC_FIXED_INCOME_DIRECTION_AUTH_D1),
        ('CBL89', GridCode.CBLC_PUBLIC_FIXED_INCOME_CLEARING),
        ('CBL90', GridCode.CBLC_PUBLIC_FIXED_INCOME_DELIVERY),
        ('CBL91', GridCode.CBLC_PUBLIC_FIXED_INCOME_DELIVERY_FAILURE),
        ('CBL92', GridCode.CBLC_PUBLIC_FIXED_INCOME_RESTRICTION_REQUEST_LIMIT),
        ('CBL93', GridCode.CBLC_PUBLIC_FIXED_INCOME_RESTRICTION_CONFIRM),
        ('CC300', GridCode.CC_OPEN_CLOSE_NOTICE),
        ('CC301', GridCode.CC_INTERBANK_SETTLEMENT_SCHEDULE),
        ('CC302', GridCode.CC_INTRABANK_SETTLEMENT_SCHEDULE),
        ('CC303', GridCode.CC_CESSION_FILE_SCHEDULE_INTERBANK),
        ('CC304', GridCode.CC_CESSION_FILE_SCHEDULE_INTRA),
        ('CCS01', GridCode.CCS_DAILY_UPDATE_FILE_RECEIPT),
        ('CCS02', GridCode.CCS_DETAIL_REQUEST_MESSAGE),
        ('CCS03', GridCode.CCS_DETAIL_RESPONSE_MESSAGE),
        ('CCS04', GridCode.CCS_REQUESTS_TO_BACEN),
        ('CCS05', GridCode.CCS_GRADE_CHANGE_NOTICE),
        ('CIR01', GridCode.CIR_GENERAL),
        ('CIR02', GridCode.CIR_CUSTODIAN_SHIPMENTS),
        ('CIR03', GridCode.CIR_QUERIES),
        ('CIR04', GridCode.CIR_CASH_SHIPMENTS_FOR_EXAM),
        ('CLI01', GridCode.CLI_INFO_REQUEST),
        ('CLI02', GridCode.CLI_BOOK_TRANSFERS),
        ('CLI03', GridCode.CLI_INTERBANK_TRANSFERS),
        ('CLI04', GridCode.CLI_PAYMENT_DOCUMENT_TRANSFERS),
        ('CMP03', GridCode.CMP_COMPE_SETTLEMENT),
        ('CTP01', GridCode.CTP_GENERAL),
        ('CTP02', GridCode.CTP_GROSS_RECORDING_STR),
        ('CTP03', GridCode.CTP_CETIP_WINDOW_RECORD),
        ('CTP04', GridCode.CTP_CETIP_FINANCIAL_CONFIRM_FOR_CLEARING_BANKS),
        ('CTP05', GridCode.CTP_CENTRAL_RECORD_D0),
        ('CTP06', GridCode.CTP_CENTRAL_RECORD_D1),
        ('CTP07', GridCode.CTP_CETIP_DEBIT_TRANSFER_WINDOW),
        ('CTP08', GridCode.CTP_CETIP_CREDIT_TRANSFER_WINDOW),
        ('CTP09', GridCode.CTP_CENTRAL_COVERED_RECORD_D0),
        ('CTP10', GridCode.CTP_CETIP_DEBIT_TRANSFER_BRUTA_STR),
        ('CTP11', GridCode.CTP_BILATERAL_RECORD),
        ('CTP12', GridCode.CTP_CENTRAL_BILATERAL_RECORD),
        ('CTP13', GridCode.CTP_CETIP_DEBIT_TRANSFER_BILATERAL),
        ('CTP17', GridCode.CTP_REG_OPER_FILES_MORNING),
        ('CTP18', GridCode.CTP_REG_OPER_FILES_AFTERNOON),
        ('CTP23', GridCode.CTP_FINANCIAL_CONFIRM_NO_SETTLEMENT_STR),
        ('CTP24', GridCode.CTP_LIBERATE_D0_EVENTS_SELIC_DI),
        ('CTP25', GridCode.CTP_RECORD_SCHEDULE_MESSAGE),
        ('CTP26', GridCode.CTP_RECORD_SCHEDULE_MESSAGE_AFTERNOON),
        ('CTP27', GridCode.CTP_RECORD_SCHEDULE_MESSAGE_NIGHT),
        ('CTP28', GridCode.CTP_ACCESS_CONTROL_MAINTENANCE),
        ('CTP29', GridCode.CTP_RECORD_SCHEDULE_MESSAGE_MADRUGADA),
        ('CTP31', GridCode.CTP_SCHEDULE_TRANSF_FILES_NIGHT_IDENTIFICATION),
        ('DDA01', GridCode.DDA_PAYER_MAINTENANCE_BY_MESSAGE),
        ('DDA02', GridCode.DDA_PAYER_MAINTENANCE_BY_FILE),
        ('DDA03', GridCode.DDA_QUERIES_AND_STATEMENTS),
        ('DDA04', GridCode.DDA_CALC_VALUE_NEXT_BUSINESS_DAY),
        ('DDA05', GridCode.DDA_BILL_MAINTENANCE_BY_MESSAGE),
        ('DDA06', GridCode.DDA_BILL_MAINTENANCE_BY_FILE),
        ('DDA07', GridCode.DDA_BENEFICIARIES_BY_MESSAGE),
        ('DDA08', GridCode.DDA_BENEFICIARIES_BY_FILE),
        ('DDA09', GridCode.DDA_LOW_BY_MESSAGE),
        ('DDA10', GridCode.DDA_LOW_BY_FILE),
        ('DDA11', GridCode.DDA_LOW_CONTINGENCY),
        ('DDA12', GridCode.DDA_PAYMENT_QUERY),
        ('GEN01', GridCode.GEN_GENERAL),
        ('GEN02', GridCode.GEN_CONNECTION_CERTIFICATION),
        ('LDL01', GridCode.LDL_GENERAL),
        ('LDL04', GridCode.LDL_CREDITS_TO_CHAMBER),
        ('LFL01', GridCode.LFL_FINANCIAL_MOVEMENTS),
        ('LFL02', GridCode.LFL_QUERIES),
        ('LFL03', GridCode.LFL_COLLATERAL_WITHDRAWAL_REQUEST),
        ('LPI01', GridCode.LPI_PAYMENTS_INSTANT_ACCOUNT_WITHDRAWALS),
        ('LPI02', GridCode.LPI_PAYMENTS_INSTANT_ACCOUNT_DEPOSITS),
        ('LTR01', GridCode.LTR_GENERAL),
        ('PAG01', GridCode.PAG_MAIN_CYCLE_01_MANDATORY_DEPOSIT),
        ('PAG02', GridCode.PAG_MAIN_CYCLE_01_MESSAGE_SEND_RECEIVE_PAYMENT),
        ('PAG03', GridCode.PAG_MAIN_CYCLE_01_SETTLEMENT),
        ('PAG91', GridCode.PAG_COMPLEMENTARY_CANCEL_PAYMENT_MSG),
        ('PAG92', GridCode.PAG_COMPLEMENTARY_MANDATORY_DEPOSIT),
        ('PAG93', GridCode.PAG_COMPLEMENTARY_SETTLEMENT),
        ('PAG94', GridCode.PAG_REAL_TIME_GROSS_SETTLEMENT_SLC),
        ('PAGD1', GridCode.PAGD1_MAIN_CYCLE1_MANDATORY_DEPOSIT),
        ('PAGD2', GridCode.PAGD2_MAIN_CYCLE1_PROCESSING_PERIOD),
        ('PAGD3', GridCode.PAGD3_MAIN_CYCLE1_SETTLEMENT),
        ('PAGE1', GridCode.PAGE1_MAIN_CYCLE2_MANDATORY_DEPOSIT),
        ('PAGE2', GridCode.PAGE2_MAIN_CYCLE2_PROCESSING_PERIOD),
        ('PAGE3', GridCode.PAGE3_MAIN_CYCLE2_SETTLEMENT),
        ('RCO01', GridCode.RCO_GENERAL),
        ('RCO02', GridCode.RCO_QUERIES),
        ('RDC01', GridCode.RDC_GENERAL),
        ('RDC02', GridCode.RDC_INTRADAY_GRANTED_AND_SETTLEMENTS),
        ('RDC03', GridCode.RDC_ONE_DAY_TERM_GRANTED),
        ('SEL01', GridCode.SEL_GENERAL),
        ('SEL03', GridCode.SEL_TERM_REGISTRATION),
        ('SEL04', GridCode.SEL_SPI_LIQUIDITY_REQUESTS),
        ('SEL05', GridCode.SEL_NOTICE),
        ('SLB01', GridCode.SLB_GENERAL),
        ('SLB02', GridCode.SLB_QUERIES),
        ('SLB04', GridCode.SLB_D0_MATURITY_CHARGES),
        ('SME01', GridCode.SME_GENERAL),
        ('SME02', GridCode.SME_QUERIES),
        ('SML01', GridCode.SML_OPERATIONS),
        ('SML02', GridCode.SML_CREDITS),
        ('STR01', GridCode.STR_GENERAL),
        ('STR02', GridCode.STR_CUSTOMER_ACCOUNT_INTERBANK_ENTRIES),
        ('STR03', GridCode.STR_QUERIES),
        ('TEC01', GridCode.TEC_CYCLE1_START),
        ('TEC02', GridCode.TEC_CYCLE1_DEBTORS_PAYMENT),
        ('TEC03', GridCode.TEC_CYCLE1_CREDITORS_PAYMENT),
        ('TEC04', GridCode.TEC_CYCLE2_START),
        ('TEC05', GridCode.TEC_CYCLE2_DEBTORS_PAYMENT),
        ('TEC06', GridCode.TEC_CYCLE2_CREDITORS_PAYMENT),
        ('TES01', GridCode.TES_GENERAL),
        ('TES04', GridCode.TES_QUERY),
        ('TES10', GridCode.TES_TREASURY_INFORMATION),
        ('TES11', GridCode.TES_COLLECTION_QUERY),
        ('TES12', GridCode.TES_RETURN_OF_COLLECTION),
    ],
)
def test_grid_code_values_from_xml_value(input_value: str, expected_enum: GridCode) -> None:
    assert GridCode.from_xml_value(input_value) == expected_enum


@pytest.mark.parametrize(
    ('input_value', 'expected_enum'),
    [
        ('scheduled_payment_order_settlement', GridCode.SCHEDULED_PAYMENT_ORDER_SETTLEMENT),
        ('bma_operations', GridCode.BMA_OPERATIONS),
        ('bma_asset_movement', GridCode.BMA_ASSET_MOVEMENT),
        ('bma_repo_d0_dm', GridCode.BMA_REPO_D0_DM),
        ('bma_repo_dn_dm', GridCode.BMA_REPO_DN_DM),
        ('bma_spot_trades_d0', GridCode.BMA_SPOT_TRADES_D0),
        ('bma_forward_trades_dn', GridCode.BMA_FORWARD_TRADES_DN),
        ('bma_phone_order_relocation_rejection_d0', GridCode.BMA_PHONE_ORDER_RELOCATION_REJECTION_D0),
        ('bma_phone_order_relocation_rejection_dn', GridCode.BMA_PHONE_ORDER_RELOCATION_REJECTION_DN),
        ('bma_covered_operations_spec_d0', GridCode.BMA_COVERED_OPERATIONS_SPEC_D0),
        ('bma_collateral_spec_repo_uncomp_d0', GridCode.BMA_COLLATERAL_SPEC_REPO_UNCOMP_D0),
        ('bma_collateral_spec_repo_uncomp_dn', GridCode.BMA_COLLATERAL_SPEC_REPO_UNCOMP_DN),
        ('bma_collateral_spec_repo_comp', GridCode.BMA_COLLATERAL_SPEC_REPO_COMP),
        ('bma_direction_acceptance', GridCode.BMA_DIRECTION_ACCEPTANCE),
        ('bma_bl_confirm_liquid_result', GridCode.BMA_BL_CONFIRM_LIQUID_RESULT),
        ('bma_participant_delivery_payment', GridCode.BMA_PARTICIPANT_DELIVERY_PAYMENT),
        ('bma_clearinghouse_delivery_payment', GridCode.BMA_CLEARINGHOUSE_DELIVERY_PAYMENT),
        ('bma_request_delivery_restriction', GridCode.BMA_REQUEST_DELIVERY_RESTRICTION),
        ('bma_confirm_release_delivery_restriction', GridCode.BMA_CONFIRM_RELEASE_DELIVERY_RESTRICTION),
        ('bma_partial_delivery_request', GridCode.BMA_PARTIAL_DELIVERY_REQUEST),
        ('bma_payment_with_collateral', GridCode.BMA_PAYMENT_WITH_COLLATERAL),
        ('bma_collateral_restoration_request', GridCode.BMA_COLLATERAL_RESTORATION_REQUEST),
        ('bma_payment_delivery_regularization_d0', GridCode.BMA_PAYMENT_DELIVERY_REGULARIZATION_D0),
        ('bma_payment_delivery_regularization_d1', GridCode.BMA_PAYMENT_DELIVERY_REGULARIZATION_D1),
        ('bmc_general', GridCode.BMC_GENERAL),
        ('bmd_general', GridCode.BMD_GENERAL),
        ('bmd_derivatives_opening', GridCode.BMD_DERIVATIVES_OPENING),
        ('bmd_provisional_netting', GridCode.BMD_PROVISIONAL_NETTING),
        ('bmd_final_netting', GridCode.BMD_FINAL_NETTING),
        ('bmd_clearing_bank_confirmation', GridCode.BMD_CLEARING_BANK_CONFIRMATION),
        ('bmd_receipt_of_payments', GridCode.BMD_RECEIPT_OF_PAYMENTS),
        ('bmd_payment_settlement', GridCode.BMD_PAYMENT_SETTLEMENT),
        ('bmd_close_message', GridCode.BMD_CLOSE_MESSAGE),
        ('bmd_collateral_deposit', GridCode.BMD_COLLATERAL_DEPOSIT),
        ('bmd_collateral_deposit_d1', GridCode.BMD_COLLATERAL_DEPOSIT_D1),
        ('bvf_general', GridCode.BVF_GENERAL),
        ('bvf_unified_ce_opening', GridCode.BVF_UNIFIED_CE_OPENING),
        ('bvf_provisional_netting', GridCode.BVF_PROVISIONAL_NETTING),
        ('bvf_final_netting', GridCode.BVF_FINAL_NETTING),
        ('bvf_clearing_bank_confirmation', GridCode.BVF_CLEARING_BANK_CONFIRMATION),
        ('bvf_receipt_of_payments', GridCode.BVF_RECEIPT_OF_PAYMENTS),
        ('bvf_payment_settlement', GridCode.BVF_PAYMENT_SETTLEMENT),
        ('bvf_close_message', GridCode.BVF_CLOSE_MESSAGE),
        ('bvf_collateral_deposit', GridCode.BVF_COLLATERAL_DEPOSIT),
        ('bvf_collateral_deposit_d1', GridCode.BVF_COLLATERAL_DEPOSIT_D1),
        ('fx_primary_market', GridCode.FX_PRIMARY_MARKET),
        ('fx_interbank_market', GridCode.FX_INTERBANK_MARKET),
        ('fx_system_queries', GridCode.FX_SYSTEM_QUERIES),
        ('fx_system_services', GridCode.FX_SYSTEM_SERVICES),
        ('cblc_general', GridCode.CBLC_GENERAL),
        ('cblc_fixed_income_variable_inform_settlement_03', GridCode.CBLC_FIXED_INCOME_VARIABLE_INFORM_SETTLEMENT_03),
        ('cblc_fixed_income_variable_inform_settlement_04', GridCode.CBLC_FIXED_INCOME_VARIABLE_INFORM_SETTLEMENT_04),
        ('cblc_fixed_income_variable_bacen', GridCode.CBLC_FIXED_INCOME_VARIABLE_BACEN),
        ('cblc_if_confirm_diverge_settlement', GridCode.CBLC_IF_CONFIRM_DIVERGE_SETTLEMENT),
        ('cblc_discrepancy_adjustment_limit', GridCode.CBLC_DISCREPANCY_ADJUSTMENT_LIMIT),
        (
            'cblc_if_request_reserve_transfer_for_debit_settlement',
            GridCode.CBLC_IF_REQUEST_RESERVE_TRANSFER_FOR_DEBIT_SETTLEMENT,
        ),
        ('cblc_dvp_creditor_settlement_and_delivery', GridCode.CBLC_DVP_CREDITOR_SETTLEMENT_AND_DELIVERY),
        ('cblc_custody_payment_events', GridCode.CBLC_CUSTODY_PAYMENT_EVENTS),
        ('cblc_custody_if_request_transfer', GridCode.CBLC_CUSTODY_IF_REQUEST_TRANSFER),
        ('cblc_custody_repass_events', GridCode.CBLC_CUSTODY_REPASS_EVENTS),
        ('cblc_equity_settlement_spec', GridCode.CBLC_EQUITY_SETTLEMENT_SPEC),
        ('cblc_equity_movement_authorization', GridCode.CBLC_EQUITY_MOVEMENT_AUTHORIZATION),
        ('cblc_equity_delivery_by_debtors', GridCode.CBLC_EQUITY_DELIVERY_BY_DEBTORS),
        ('cblc_equity_delivery_failure_handling', GridCode.CBLC_EQUITY_DELIVERY_FAILURE_HANDLING),
        ('cblc_equity_restriction_request_limit', GridCode.CBLC_EQUITY_RESTRICTION_REQUEST_LIMIT),
        ('cblc_equity_delivery_by_cblc', GridCode.CBLC_EQUITY_DELIVERY_BY_CBLC),
        ('cblc_equity_restriction_release', GridCode.CBLC_EQUITY_RESTRICTION_RELEASE),
        ('cblc_private_fixed_income_negotiation_limit_d0', GridCode.CBLC_PRIVATE_FIXED_INCOME_NEGOTIATION_LIMIT_D0),
        ('cblc_private_fixed_income_cancel_limit_d0', GridCode.CBLC_PRIVATE_FIXED_INCOME_CANCEL_LIMIT_D0),
        ('cblc_private_fixed_income_spec_limit_d0', GridCode.CBLC_PRIVATE_FIXED_INCOME_SPEC_LIMIT_D0),
        ('cblc_private_fixed_income_direction_auth_d0', GridCode.CBLC_PRIVATE_FIXED_INCOME_DIRECTION_AUTH_D0),
        ('cblc_private_fixed_income_negotiation_limit_d1', GridCode.CBLC_PRIVATE_FIXED_INCOME_NEGOTIATION_LIMIT_D1),
        ('cblc_private_fixed_income_cancel_limit_d1', GridCode.CBLC_PRIVATE_FIXED_INCOME_CANCEL_LIMIT_D1),
        ('cblc_private_fixed_income_spec_limit_d1', GridCode.CBLC_PRIVATE_FIXED_INCOME_SPEC_LIMIT_D1),
        ('cblc_private_fixed_income_direction_auth_d1', GridCode.CBLC_PRIVATE_FIXED_INCOME_DIRECTION_AUTH_D1),
        ('cblc_private_fixed_income_clearing', GridCode.CBLC_PRIVATE_FIXED_INCOME_CLEARING),
        ('cblc_private_fixed_income_delivery', GridCode.CBLC_PRIVATE_FIXED_INCOME_DELIVERY),
        ('cblc_private_fixed_income_delivery_failure', GridCode.CBLC_PRIVATE_FIXED_INCOME_DELIVERY_FAILURE),
        (
            'cblc_private_fixed_income_restriction_request_limit',
            GridCode.CBLC_PRIVATE_FIXED_INCOME_RESTRICTION_REQUEST_LIMIT,
        ),
        ('cblc_private_fixed_income_restriction_confirm', GridCode.CBLC_PRIVATE_FIXED_INCOME_RESTRICTION_CONFIRM),
        ('cblc_gross_settlement_prepare_send_ltr_values', GridCode.CBLC_GROSS_SETTLEMENT_PREPARE_SEND_LTR_VALUES),
        ('cblc_gross_settlement_if_confirm_or_diverge_ltr', GridCode.CBLC_GROSS_SETTLEMENT_IF_CONFIRM_OR_DIVERGE_LTR),
        (
            'cblc_gross_settlement_if_request_transfer_reserves',
            GridCode.CBLC_GROSS_SETTLEMENT_IF_REQUEST_TRANSFER_RESERVES,
        ),
        ('cblc_gross_settlement_creditor_results', GridCode.CBLC_GROSS_SETTLEMENT_CREDITOR_RESULTS),
        ('cblc_collateral_movement', GridCode.CBLC_COLLATERAL_MOVEMENT),
        ('cblc_limits_deallocation', GridCode.CBLC_LIMITS_DEALLOCATION),
        ('cblc_public_titles_transfer_for_margin_reversal', GridCode.CBLC_PUBLIC_TITLES_TRANSFER_FOR_MARGIN_REVERSAL),
        ('cblc_public_fixed_income_negotiation_limit_d0', GridCode.CBLC_PUBLIC_FIXED_INCOME_NEGOTIATION_LIMIT_D0),
        ('cblc_public_fixed_income_cancel_limit_d0', GridCode.CBLC_PUBLIC_FIXED_INCOME_CANCEL_LIMIT_D0),
        ('cblc_public_fixed_income_spec_limit_d0', GridCode.CBLC_PUBLIC_FIXED_INCOME_SPEC_LIMIT_D0),
        ('cblc_public_fixed_income_direction_auth_d0', GridCode.CBLC_PUBLIC_FIXED_INCOME_DIRECTION_AUTH_D0),
        ('cblc_public_fixed_income_negotiation_limit_d1', GridCode.CBLC_PUBLIC_FIXED_INCOME_NEGOTIATION_LIMIT_D1),
        ('cblc_public_fixed_income_cancel_limit_d1', GridCode.CBLC_PUBLIC_FIXED_INCOME_CANCEL_LIMIT_D1),
        ('cblc_public_fixed_income_spec_limit_d1', GridCode.CBLC_PUBLIC_FIXED_INCOME_SPEC_LIMIT_D1),
        ('cblc_public_fixed_income_direction_auth_d1', GridCode.CBLC_PUBLIC_FIXED_INCOME_DIRECTION_AUTH_D1),
        ('cblc_public_fixed_income_clearing', GridCode.CBLC_PUBLIC_FIXED_INCOME_CLEARING),
        ('cblc_public_fixed_income_delivery', GridCode.CBLC_PUBLIC_FIXED_INCOME_DELIVERY),
        ('cblc_public_fixed_income_delivery_failure', GridCode.CBLC_PUBLIC_FIXED_INCOME_DELIVERY_FAILURE),
        (
            'cblc_public_fixed_income_restriction_request_limit',
            GridCode.CBLC_PUBLIC_FIXED_INCOME_RESTRICTION_REQUEST_LIMIT,
        ),
        ('cblc_public_fixed_income_restriction_confirm', GridCode.CBLC_PUBLIC_FIXED_INCOME_RESTRICTION_CONFIRM),
        ('cc_open_close_notice', GridCode.CC_OPEN_CLOSE_NOTICE),
        ('cc_interbank_settlement_schedule', GridCode.CC_INTERBANK_SETTLEMENT_SCHEDULE),
        ('cc_intrabank_settlement_schedule', GridCode.CC_INTRABANK_SETTLEMENT_SCHEDULE),
        ('cc_cession_file_schedule_interbank', GridCode.CC_CESSION_FILE_SCHEDULE_INTERBANK),
        ('cc_cession_file_schedule_intra', GridCode.CC_CESSION_FILE_SCHEDULE_INTRA),
        ('ccs_daily_update_file_receipt', GridCode.CCS_DAILY_UPDATE_FILE_RECEIPT),
        ('ccs_detail_request_message', GridCode.CCS_DETAIL_REQUEST_MESSAGE),
        ('ccs_detail_response_message', GridCode.CCS_DETAIL_RESPONSE_MESSAGE),
        ('ccs_requests_to_bacen', GridCode.CCS_REQUESTS_TO_BACEN),
        ('ccs_grade_change_notice', GridCode.CCS_GRADE_CHANGE_NOTICE),
        ('cir_general', GridCode.CIR_GENERAL),
        ('cir_custodian_shipments', GridCode.CIR_CUSTODIAN_SHIPMENTS),
        ('cir_queries', GridCode.CIR_QUERIES),
        ('cir_cash_shipments_for_exam', GridCode.CIR_CASH_SHIPMENTS_FOR_EXAM),
        ('cli_info_request', GridCode.CLI_INFO_REQUEST),
        ('cli_book_transfers', GridCode.CLI_BOOK_TRANSFERS),
        ('cli_interbank_transfers', GridCode.CLI_INTERBANK_TRANSFERS),
        ('cli_payment_document_transfers', GridCode.CLI_PAYMENT_DOCUMENT_TRANSFERS),
        ('cmp_compe_settlement', GridCode.CMP_COMPE_SETTLEMENT),
        ('ctp_general', GridCode.CTP_GENERAL),
        ('ctp_gross_recording_str', GridCode.CTP_GROSS_RECORDING_STR),
        ('ctp_cetip_window_record', GridCode.CTP_CETIP_WINDOW_RECORD),
        ('ctp_cetip_financial_confirm_for_clearing_banks', GridCode.CTP_CETIP_FINANCIAL_CONFIRM_FOR_CLEARING_BANKS),
        ('ctp_central_record_d0', GridCode.CTP_CENTRAL_RECORD_D0),
        ('ctp_central_record_d1', GridCode.CTP_CENTRAL_RECORD_D1),
        ('ctp_cetip_debit_transfer_window', GridCode.CTP_CETIP_DEBIT_TRANSFER_WINDOW),
        ('ctp_cetip_credit_transfer_window', GridCode.CTP_CETIP_CREDIT_TRANSFER_WINDOW),
        ('ctp_central_covered_record_d0', GridCode.CTP_CENTRAL_COVERED_RECORD_D0),
        ('ctp_cetip_debit_transfer_bruta_str', GridCode.CTP_CETIP_DEBIT_TRANSFER_BRUTA_STR),
        ('ctp_bilateral_record', GridCode.CTP_BILATERAL_RECORD),
        ('ctp_central_bilateral_record', GridCode.CTP_CENTRAL_BILATERAL_RECORD),
        ('ctp_cetip_debit_transfer_bilateral', GridCode.CTP_CETIP_DEBIT_TRANSFER_BILATERAL),
        ('ctp_reg_oper_files_morning', GridCode.CTP_REG_OPER_FILES_MORNING),
        ('ctp_reg_oper_files_afternoon', GridCode.CTP_REG_OPER_FILES_AFTERNOON),
        ('ctp_financial_confirm_no_settlement_str', GridCode.CTP_FINANCIAL_CONFIRM_NO_SETTLEMENT_STR),
        ('ctp_liberate_d0_events_selic_di', GridCode.CTP_LIBERATE_D0_EVENTS_SELIC_DI),
        ('ctp_record_schedule_message', GridCode.CTP_RECORD_SCHEDULE_MESSAGE),
        ('ctp_record_schedule_message_afternoon', GridCode.CTP_RECORD_SCHEDULE_MESSAGE_AFTERNOON),
        ('ctp_record_schedule_message_night', GridCode.CTP_RECORD_SCHEDULE_MESSAGE_NIGHT),
        ('ctp_access_control_maintenance', GridCode.CTP_ACCESS_CONTROL_MAINTENANCE),
        ('ctp_record_schedule_message_madrugada', GridCode.CTP_RECORD_SCHEDULE_MESSAGE_MADRUGADA),
        ('ctp_schedule_transf_files_night_identification', GridCode.CTP_SCHEDULE_TRANSF_FILES_NIGHT_IDENTIFICATION),
        ('dda_payer_maintenance_by_message', GridCode.DDA_PAYER_MAINTENANCE_BY_MESSAGE),
        ('dda_payer_maintenance_by_file', GridCode.DDA_PAYER_MAINTENANCE_BY_FILE),
        ('dda_queries_and_statements', GridCode.DDA_QUERIES_AND_STATEMENTS),
        ('dda_calc_value_next_business_day', GridCode.DDA_CALC_VALUE_NEXT_BUSINESS_DAY),
        ('dda_bill_maintenance_by_message', GridCode.DDA_BILL_MAINTENANCE_BY_MESSAGE),
        ('dda_bill_maintenance_by_file', GridCode.DDA_BILL_MAINTENANCE_BY_FILE),
        ('dda_beneficiaries_by_message', GridCode.DDA_BENEFICIARIES_BY_MESSAGE),
        ('dda_beneficiaries_by_file', GridCode.DDA_BENEFICIARIES_BY_FILE),
        ('dda_low_by_message', GridCode.DDA_LOW_BY_MESSAGE),
        ('dda_low_by_file', GridCode.DDA_LOW_BY_FILE),
        ('dda_low_contingency', GridCode.DDA_LOW_CONTINGENCY),
        ('dda_payment_query', GridCode.DDA_PAYMENT_QUERY),
        ('gen_general', GridCode.GEN_GENERAL),
        ('gen_connection_certification', GridCode.GEN_CONNECTION_CERTIFICATION),
        ('ldl_general', GridCode.LDL_GENERAL),
        ('ldl_credits_to_chamber', GridCode.LDL_CREDITS_TO_CHAMBER),
        ('lfl_financial_movements', GridCode.LFL_FINANCIAL_MOVEMENTS),
        ('lfl_queries', GridCode.LFL_QUERIES),
        ('lfl_collateral_withdrawal_request', GridCode.LFL_COLLATERAL_WITHDRAWAL_REQUEST),
        ('lpi_payments_instant_account_withdrawals', GridCode.LPI_PAYMENTS_INSTANT_ACCOUNT_WITHDRAWALS),
        ('lpi_payments_instant_account_deposits', GridCode.LPI_PAYMENTS_INSTANT_ACCOUNT_DEPOSITS),
        ('ltr_general', GridCode.LTR_GENERAL),
        ('pag_main_cycle_01_mandatory_deposit', GridCode.PAG_MAIN_CYCLE_01_MANDATORY_DEPOSIT),
        ('pag_main_cycle_01_message_send_receive_payment', GridCode.PAG_MAIN_CYCLE_01_MESSAGE_SEND_RECEIVE_PAYMENT),
        ('pag_main_cycle_01_settlement', GridCode.PAG_MAIN_CYCLE_01_SETTLEMENT),
        ('pag_complementary_cancel_payment_msg', GridCode.PAG_COMPLEMENTARY_CANCEL_PAYMENT_MSG),
        ('pag_complementary_mandatory_deposit', GridCode.PAG_COMPLEMENTARY_MANDATORY_DEPOSIT),
        ('pag_complementary_settlement', GridCode.PAG_COMPLEMENTARY_SETTLEMENT),
        ('pag_real_time_gross_settlement_slc', GridCode.PAG_REAL_TIME_GROSS_SETTLEMENT_SLC),
        ('pagd1_main_cycle1_mandatory_deposit', GridCode.PAGD1_MAIN_CYCLE1_MANDATORY_DEPOSIT),
        ('pagd2_main_cycle1_processing_period', GridCode.PAGD2_MAIN_CYCLE1_PROCESSING_PERIOD),
        ('pagd3_main_cycle1_settlement', GridCode.PAGD3_MAIN_CYCLE1_SETTLEMENT),
        ('page1_main_cycle2_mandatory_deposit', GridCode.PAGE1_MAIN_CYCLE2_MANDATORY_DEPOSIT),
        ('page2_main_cycle2_processing_period', GridCode.PAGE2_MAIN_CYCLE2_PROCESSING_PERIOD),
        ('page3_main_cycle2_settlement', GridCode.PAGE3_MAIN_CYCLE2_SETTLEMENT),
        ('rco_general', GridCode.RCO_GENERAL),
        ('rco_queries', GridCode.RCO_QUERIES),
        ('rdc_general', GridCode.RDC_GENERAL),
        ('rdc_intraday_granted_and_settlements', GridCode.RDC_INTRADAY_GRANTED_AND_SETTLEMENTS),
        ('rdc_one_day_term_granted', GridCode.RDC_ONE_DAY_TERM_GRANTED),
        ('sel_general', GridCode.SEL_GENERAL),
        ('sel_term_registration', GridCode.SEL_TERM_REGISTRATION),
        ('sel_spi_liquidity_requests', GridCode.SEL_SPI_LIQUIDITY_REQUESTS),
        ('sel_notice', GridCode.SEL_NOTICE),
        ('slb_general', GridCode.SLB_GENERAL),
        ('slb_queries', GridCode.SLB_QUERIES),
        ('slb_d0_maturity_charges', GridCode.SLB_D0_MATURITY_CHARGES),
        ('sme_general', GridCode.SME_GENERAL),
        ('sme_queries', GridCode.SME_QUERIES),
        ('sml_operations', GridCode.SML_OPERATIONS),
        ('sml_credits', GridCode.SML_CREDITS),
        ('str_general', GridCode.STR_GENERAL),
        ('str_customer_account_interbank_entries', GridCode.STR_CUSTOMER_ACCOUNT_INTERBANK_ENTRIES),
        ('str_queries', GridCode.STR_QUERIES),
        ('tec_cycle1_start', GridCode.TEC_CYCLE1_START),
        ('tec_cycle1_debtors_payment', GridCode.TEC_CYCLE1_DEBTORS_PAYMENT),
        ('tec_cycle1_creditors_payment', GridCode.TEC_CYCLE1_CREDITORS_PAYMENT),
        ('tec_cycle2_start', GridCode.TEC_CYCLE2_START),
        ('tec_cycle2_debtors_payment', GridCode.TEC_CYCLE2_DEBTORS_PAYMENT),
        ('tec_cycle2_creditors_payment', GridCode.TEC_CYCLE2_CREDITORS_PAYMENT),
        ('tes_general', GridCode.TES_GENERAL),
        ('tes_query', GridCode.TES_QUERY),
        ('tes_treasury_information', GridCode.TES_TREASURY_INFORMATION),
        ('tes_collection_query', GridCode.TES_COLLECTION_QUERY),
        ('tes_return_of_collection', GridCode.TES_RETURN_OF_COLLECTION),
    ],
)
def test_grid_code_accepts_case_insensitive_values(input_value: str, expected_enum: GridCode) -> None:
    assert GridCode(input_value) is expected_enum


@pytest.mark.parametrize(
    ('input_value', 'expected_enum'),
    [
        ('EVENTUAL_EXCEPTION', TimeType.EVENTUAL_EXCEPTION),
        ('STANDARD', TimeType.STANDARD),
    ],
)
def test_time_type_accepts_exact_values(input_value: str, expected_enum: TimeType) -> None:
    assert TimeType(input_value) is expected_enum


@pytest.mark.parametrize(
    ('input_value', 'expected_enum'),
    [
        (TimeType.EVENTUAL_EXCEPTION, 'E'),
        (TimeType.STANDARD, 'P'),
    ],
)
def test_time_type_values_to_xml_value(input_value: TimeType, expected_enum: str) -> None:
    assert input_value.to_xml_value() == expected_enum


@pytest.mark.parametrize(
    ('input_value', 'expected_enum'),
    [
        ('E', TimeType.EVENTUAL_EXCEPTION),
        ('P', TimeType.STANDARD),
    ],
)
def test_time_type_values_from_xml_value(input_value: str, expected_enum: TimeType) -> None:
    assert TimeType.from_xml_value(input_value) == expected_enum


@pytest.mark.parametrize(
    ('input_value', 'expected_enum'),
    [
        ('eventual_exception', TimeType.EVENTUAL_EXCEPTION),
        ('standard', TimeType.STANDARD),
    ],
)
def test_time_type_accepts_case_insensitive_values(input_value: str, expected_enum: TimeType) -> None:
    assert TimeType(input_value) is expected_enum


@pytest.mark.parametrize(
    ('input_value', 'expected_enum'),
    [
        ('CREDIT', CreditDebitType.CREDIT),
        ('DEBIT', CreditDebitType.DEBIT),
    ],
)
def test_credit_debit_type_accepts_exact_values(input_value: str, expected_enum: CreditDebitType) -> None:
    assert CreditDebitType(input_value) is expected_enum


@pytest.mark.parametrize(
    ('input_value', 'expected_enum'),
    [
        (CreditDebitType.CREDIT, 'C'),
        (CreditDebitType.DEBIT, 'D'),
    ],
)
def test_credit_debit_type_values_to_xml_value(input_value: CreditDebitType, expected_enum: str) -> None:
    assert input_value.to_xml_value() == expected_enum


@pytest.mark.parametrize(
    ('input_value', 'expected_enum'),
    [
        ('C', CreditDebitType.CREDIT),
        ('D', CreditDebitType.DEBIT),
    ],
)
def test_credit_debit_type_values_from_xml_value(input_value: str, expected_enum: CreditDebitType) -> None:
    assert CreditDebitType.from_xml_value(input_value) == expected_enum


@pytest.mark.parametrize(
    ('input_value', 'expected_enum'),
    [
        ('credit', CreditDebitType.CREDIT),
        ('debit', CreditDebitType.DEBIT),
    ],
)
def test_credit_debit_type_accepts_case_insensitive_values(input_value: str, expected_enum: CreditDebitType) -> None:
    assert CreditDebitType(input_value) is expected_enum


@pytest.mark.parametrize(
    'message_code',
    [
        'MES0123',
        'MES012345',
        'mes012345',
        'mes0123',
    ],
)
def test_message_code_accepts_valid_values(message_code: str) -> None:
    model = MessageCodeModel(message_code=message_code)
    assert model.message_code == message_code


def test_message_code_accepts_whitespace() -> None:
    model = MessageCodeModel(message_code='   MES0123   ')
    assert model.message_code == 'MES0123'


@pytest.mark.parametrize(
    'message_code',
    [
        'MES012',  # Too short
        'MES' + '0' * 19,  # Too long
        '',  # Empty
    ],
)
def test_message_code_rejects_invalid_values(message_code: str) -> None:
    with pytest.raises(ValidationError):
        MessageCodeModel(message_code=message_code)


@pytest.mark.parametrize(
    ('input_value', 'expected_enum'),
    [
        ('STOCKS', AssetType.STOCKS),
        ('INVESTMENT_PORTFOLIO_ASSETS', AssetType.INVESTMENT_PORTFOLIO_ASSETS),
        ('AGRICULTURAL_DEBT_EXTENSION', AssetType.AGRICULTURAL_DEBT_EXTENSION),
        ('RECEIVABLES_ADVANCE_ISSUER', AssetType.RECEIVABLES_ADVANCE_ISSUER),
        ('RECEIVABLES_ADVANCE_ACQUIRER', AssetType.RECEIVABLES_ADVANCE_ACQUIRER),
        ('CENTRAL_BANK_BOND', AssetType.CENTRAL_BANK_BOND),
        ('CENTRAL_BANK_BOND_SERIES_A', AssetType.CENTRAL_BANK_BOND_SERIES_A),
        ('BOX_TWO_LEGS', AssetType.BOX_TWO_LEGS),
        ('NATIONAL_TREASURY_BOND_BTN', AssetType.NATIONAL_TREASURY_BOND_BTN),
        ('CREDIT_OPENING_CONTRACT', AssetType.CREDIT_OPENING_CONTRACT),
        ('CREDIT_ASSIGNMENT', AssetType.CREDIT_ASSIGNMENT),
        ('BANK_CREDIT_NOTE', AssetType.BANK_CREDIT_NOTE),
        ('COMMERCIAL_CREDIT_NOTE', AssetType.COMMERCIAL_CREDIT_NOTE),
        ('BANK_CREDIT_NOTE_CERTIFICATE', AssetType.BANK_CREDIT_NOTE_CERTIFICATE),
        ('EXPORT_CREDIT_NOTE', AssetType.EXPORT_CREDIT_NOTE),
        ('INDUSTRIAL_CREDIT_NOTE', AssetType.INDUSTRIAL_CREDIT_NOTE),
        ('INDUSTRIAL_CREDIT_NOTE_ID', AssetType.INDUSTRIAL_CREDIT_NOTE_ID),
        ('REAL_ESTATE_CREDIT_CERTIFICATE', AssetType.REAL_ESTATE_CREDIT_CERTIFICATE),
        ('THIRD_PARTY_CREDIT_CONTRACT', AssetType.THIRD_PARTY_CREDIT_CONTRACT),
        ('AGRICULTURAL_DEPOSIT_CERTIFICATE', AssetType.AGRICULTURAL_DEPOSIT_CERTIFICATE),
        ('BANK_DEPOSIT_CERTIFICATE', AssetType.BANK_DEPOSIT_CERTIFICATE),
        ('BANK_DEPOSIT_CERTIFICATE_RURAL', AssetType.BANK_DEPOSIT_CERTIFICATE_RURAL),
        ('BANK_DEPOSIT_CERTIFICATE_SUBORDINATED', AssetType.BANK_DEPOSIT_CERTIFICATE_SUBORDINATED),
        ('BANK_DEPOSIT_CERTIFICATE_LINKED', AssetType.BANK_DEPOSIT_CERTIFICATE_LINKED),
        ('AGRIBUSINESS_RECEIVABLES_CERTIFICATE', AssetType.AGRIBUSINESS_RECEIVABLES_CERTIFICATE),
        ('DEBENTURE_NOTE', AssetType.DEBENTURE_NOTE),
        ('PUBLIC_DEBT_CERTIFICATE', AssetType.PUBLIC_DEBT_CERTIFICATE),
        ('OPEN_FUND_QUOTA', AssetType.OPEN_FUND_QUOTA),
        ('CLOSED_FUND_QUOTA', AssetType.CLOSED_FUND_QUOTA),
        ('NATIONAL_TREASURY_FINANCIAL_CERTIFICATE', AssetType.NATIONAL_TREASURY_FINANCIAL_CERTIFICATE),
        ('AUDIOVISUAL_INVESTMENT_CERTIFICATE', AssetType.AUDIOVISUAL_INVESTMENT_CERTIFICATE),
        ('MERCHANDISE_CERTIFICATE', AssetType.MERCHANDISE_CERTIFICATE),
        ('MERCHANT_CONTRACT', AssetType.MERCHANT_CONTRACT),
        ('STRUCTURED_OPERATIONS_CERTIFICATE', AssetType.STRUCTURED_OPERATIONS_CERTIFICATE),
        ('AGRICULTURAL_PRODUCT_SALE_OPTION', AssetType.AGRICULTURAL_PRODUCT_SALE_OPTION),
        ('PRIVATIZATION_CERTIFICATE', AssetType.PRIVATIZATION_CERTIFICATE),
        ('RURAL_PRODUCT_NOTE', AssetType.RURAL_PRODUCT_NOTE),
        ('AGRIBUSINESS_RECEIVABLES_CERTIFICATE_CRA', AssetType.AGRIBUSINESS_RECEIVABLES_CERTIFICATE_CRA),
        ('CARD_SETTLEMENT_CONTINGENCY', AssetType.CARD_SETTLEMENT_CONTINGENCY),
        ('RURAL_MORTGAGE_NOTE', AssetType.RURAL_MORTGAGE_NOTE),
        ('REAL_ESTATE_RECEIVABLES_CERTIFICATE', AssetType.REAL_ESTATE_RECEIVABLES_CERTIFICATE),
        ('RURAL_PLEDGE_NOTE', AssetType.RURAL_PLEDGE_NOTE),
        ('RURAL_PLEDGE_AND_MORTGAGE_NOTE', AssetType.RURAL_PLEDGE_AND_MORTGAGE_NOTE),
        ('SECURITIZED_CREDIT', AssetType.SECURITIZED_CREDIT),
        ('ELECTRIC_ENERGY_FORWARD_CERTIFICATE', AssetType.ELECTRIC_ENERGY_FORWARD_CERTIFICATE),
        ('CREDIT_RIGHT', AssetType.CREDIT_RIGHT),
        ('CREDIT_DERIVATIVES_CONTRACT', AssetType.CREDIT_DERIVATIVES_CONTRACT),
        ('DEBENTURE', AssetType.DEBENTURE),
        ('INTERBANK_DEPOSIT', AssetType.INTERBANK_DEPOSIT),
        ('INTERBANK_DEPOSIT_RENEGOTIATED', AssetType.INTERBANK_DEPOSIT_RENEGOTIATED),
        ('INTERBANK_DEPOSIT_HOUSING', AssetType.INTERBANK_DEPOSIT_HOUSING),
        ('INTERBANK_DEPOSIT_REAL_ESTATE', AssetType.INTERBANK_DEPOSIT_REAL_ESTATE),
        ('INTERBANK_DEPOSIT_MICROFINANCE', AssetType.INTERBANK_DEPOSIT_MICROFINANCE),
        ('INTERBANK_DEPOSIT_RURAL', AssetType.INTERBANK_DEPOSIT_RURAL),
        ('INTERBANK_DEPOSIT_COOPERATIVE', AssetType.INTERBANK_DEPOSIT_COOPERATIVE),
        ('INTERBANK_DEPOSIT_PROGER', AssetType.INTERBANK_DEPOSIT_PROGER),
        ('INTERBANK_DEPOSIT_PRONAF', AssetType.INTERBANK_DEPOSIT_PRONAF),
        ('INTERBANK_DEPOSIT_RURAL_SAVINGS', AssetType.INTERBANK_DEPOSIT_RURAL_SAVINGS),
        ('TERM_DEPOSIT_FGC', AssetType.TERM_DEPOSIT_FGC),
        ('EXPORT_NOTES', AssetType.EXPORT_NOTES),
        ('SOCIAL_DEVELOPMENT_FUND_QUOTA', AssetType.SOCIAL_DEVELOPMENT_FUND_QUOTA),
        ('LEASING_LETTER', AssetType.LEASING_LETTER),
        ('CENTRAL_BANK_BILL', AssetType.CENTRAL_BANK_BILL),
        ('EXCHANGE_BILL', AssetType.EXCHANGE_BILL),
        ('AGRIBUSINESS_CREDIT_LETTER', AssetType.AGRIBUSINESS_CREDIT_LETTER),
        ('DEVELOPMENT_CREDIT_LETTER', AssetType.DEVELOPMENT_CREDIT_LETTER),
        ('REAL_ESTATE_CREDIT_LETTER', AssetType.REAL_ESTATE_CREDIT_LETTER),
        ('WARRANT_EXCHANGE_BILL', AssetType.WARRANT_EXCHANGE_BILL),
        ('FINANCIAL_BILL', AssetType.FINANCIAL_BILL),
        ('FINANCIAL_BILL_COMPLEMENTARY_CAPITAL', AssetType.FINANCIAL_BILL_COMPLEMENTARY_CAPITAL),
        ('FINANCIAL_BILL_LEVEL_II', AssetType.FINANCIAL_BILL_LEVEL_II),
        ('FINANCIAL_BILL_PRIMARY_CAPITAL', AssetType.FINANCIAL_BILL_PRIMARY_CAPITAL),
        ('FINANCIAL_BILL_SUBORDINATED', AssetType.FINANCIAL_BILL_SUBORDINATED),
        ('TREASURY_FINANCIAL_BILL', AssetType.TREASURY_FINANCIAL_BILL),
        ('TREASURY_FINANCIAL_BILL_SERIES_A', AssetType.TREASURY_FINANCIAL_BILL_SERIES_A),
        ('TREASURY_FINANCIAL_BILL_SERIES_B', AssetType.TREASURY_FINANCIAL_BILL_SERIES_B),
        ('STATE_TREASURY_FINANCIAL_BILL', AssetType.STATE_TREASURY_FINANCIAL_BILL),
        ('MUNICIPAL_TREASURY_FINANCIAL_BILL', AssetType.MUNICIPAL_TREASURY_FINANCIAL_BILL),
        ('LINKED_FINANCIAL_BILL', AssetType.LINKED_FINANCIAL_BILL),
        ('MORTGAGE_LETTER', AssetType.MORTGAGE_LETTER),
        ('COVERED_REAL_ESTATE_LETTER', AssetType.COVERED_REAL_ESTATE_LETTER),
        ('NATIONAL_TREASURY_BILL', AssetType.NATIONAL_TREASURY_BILL),
        ('CENTRAL_BANK_NOTES_SERIES_A', AssetType.CENTRAL_BANK_NOTES_SERIES_A),
        ('CENTRAL_BANK_NOTES_SERIES_E', AssetType.CENTRAL_BANK_NOTES_SERIES_E),
        ('CENTRAL_BANK_NOTES_SERIES_F', AssetType.CENTRAL_BANK_NOTES_SERIES_F),
        ('COMMERCIAL_NOTE', AssetType.COMMERCIAL_NOTE),
        ('AGRIBUSINESS_COMMERCIAL_NOTE', AssetType.AGRIBUSINESS_COMMERCIAL_NOTE),
        ('COMMERCIAL_CREDIT_NOTE_NCC', AssetType.COMMERCIAL_CREDIT_NOTE_NCC),
        ('EXPORT_CREDIT_NOTE_NCE', AssetType.EXPORT_CREDIT_NOTE_NCE),
        ('INDUSTRIAL_CREDIT_NOTE_NCI', AssetType.INDUSTRIAL_CREDIT_NOTE_NCI),
        ('RURAL_CREDIT_NOTE', AssetType.RURAL_CREDIT_NOTE),
        ('NETTING_AGREEMENT', AssetType.NETTING_AGREEMENT),
        ('PROMISSORY_NOTE', AssetType.PROMISSORY_NOTE),
        ('NATIONAL_TREASURY_NOTES_SERIES_A', AssetType.NATIONAL_TREASURY_NOTES_SERIES_A),
        ('NATIONAL_TREASURY_NOTES_SERIES_B', AssetType.NATIONAL_TREASURY_NOTES_SERIES_B),
        ('NATIONAL_TREASURY_NOTES_SERIES_C', AssetType.NATIONAL_TREASURY_NOTES_SERIES_C),
        ('NATIONAL_TREASURY_NOTES_SERIES_D', AssetType.NATIONAL_TREASURY_NOTES_SERIES_D),
        ('NATIONAL_TREASURY_NOTES_SERIES_E', AssetType.NATIONAL_TREASURY_NOTES_SERIES_E),
        ('NATIONAL_TREASURY_NOTES_SERIES_F', AssetType.NATIONAL_TREASURY_NOTES_SERIES_F),
        ('NATIONAL_TREASURY_NOTES_SERIES_H', AssetType.NATIONAL_TREASURY_NOTES_SERIES_H),
        ('NATIONAL_TREASURY_NOTES_SERIES_I', AssetType.NATIONAL_TREASURY_NOTES_SERIES_I),
        ('NATIONAL_TREASURY_NOTES_SERIES_L', AssetType.NATIONAL_TREASURY_NOTES_SERIES_L),
        ('NATIONAL_TREASURY_NOTES_SERIES_M', AssetType.NATIONAL_TREASURY_NOTES_SERIES_M),
        ('NATIONAL_TREASURY_NOTES_SERIES_P', AssetType.NATIONAL_TREASURY_NOTES_SERIES_P),
        ('NATIONAL_TREASURY_NOTES_SERIES_R', AssetType.NATIONAL_TREASURY_NOTES_SERIES_R),
        ('NATIONAL_TREASURY_NOTES_SERIES_S', AssetType.NATIONAL_TREASURY_NOTES_SERIES_S),
        ('NATIONAL_TREASURY_NOTES_SERIES_T', AssetType.NATIONAL_TREASURY_NOTES_SERIES_T),
        ('NATIONAL_TREASURY_NOTES_SERIES_U', AssetType.NATIONAL_TREASURY_NOTES_SERIES_U),
        ('IFC_OBLIGATIONS', AssetType.IFC_OBLIGATIONS),
        ('FLEXIBLE_CURRENCY_CALL_OPTION', AssetType.FLEXIBLE_CURRENCY_CALL_OPTION),
        ('NATIONAL_DEVELOPMENT_FUND_OBLIGATIONS', AssetType.NATIONAL_DEVELOPMENT_FUND_OBLIGATIONS),
        ('FLEXIBLE_CURRENCY_PUT_OPTION', AssetType.FLEXIBLE_CURRENCY_PUT_OPTION),
        ('GOLD', AssetType.GOLD),
        ('OTHERS', AssetType.OTHERS),
        ('BANK_DEPOSIT_RECEIPT', AssetType.BANK_DEPOSIT_RECEIPT),
        ('COOPERATIVE_DEPOSIT_RECEIPT', AssetType.COOPERATIVE_DEPOSIT_RECEIPT),
        ('SWAP_CONTRACT', AssetType.SWAP_CONTRACT),
        ('MERCHANDISE_FORWARD_CONTRACT', AssetType.MERCHANDISE_FORWARD_CONTRACT),
        ('AGRARIAN_DEBT_SECURITY', AssetType.AGRARIAN_DEBT_SECURITY),
        ('ECONOMIC_DEVELOPMENT_SECURITY', AssetType.ECONOMIC_DEVELOPMENT_SECURITY),
        ('TERM21', AssetType.TERM21),
        ('CURRENCY_FORWARD_CONTRACT', AssetType.CURRENCY_FORWARD_CONTRACT),
        ('MONETARY_UNIT', AssetType.MONETARY_UNIT),
        ('AGRICULTURAL_WARRANT', AssetType.AGRICULTURAL_WARRANT),
        ('WARRANT', AssetType.WARRANT),
    ],
)
def test_asset_type_accepts_exact_values(input_value: str, expected_enum: AssetType) -> None:
    assert AssetType(input_value) is expected_enum


@pytest.mark.parametrize(
    ('input_value', 'expected_enum'),
    [
        (AssetType.STOCKS, 'ACAO'),
        (AssetType.INVESTMENT_PORTFOLIO_ASSETS, 'ACI'),
        (AssetType.AGRICULTURAL_DEBT_EXTENSION, 'ADA'),
        (AssetType.RECEIVABLES_ADVANCE_ISSUER, 'ANTE'),
        (AssetType.RECEIVABLES_ADVANCE_ACQUIRER, 'ANTR'),
        (AssetType.CENTRAL_BANK_BOND, 'BBC'),
        (AssetType.CENTRAL_BANK_BOND_SERIES_A, 'BBCA'),
        (AssetType.BOX_TWO_LEGS, 'BOX2'),
        (AssetType.NATIONAL_TREASURY_BOND_BTN, 'BTN'),
        (AssetType.CREDIT_OPENING_CONTRACT, 'CAC'),
        (AssetType.CREDIT_ASSIGNMENT, 'CC3'),
        (AssetType.BANK_CREDIT_NOTE, 'CCB'),
        (AssetType.COMMERCIAL_CREDIT_NOTE, 'CCC'),
        (AssetType.BANK_CREDIT_NOTE_CERTIFICATE, 'CCCB'),
        (AssetType.EXPORT_CREDIT_NOTE, 'CCE'),
        (AssetType.INDUSTRIAL_CREDIT_NOTE, 'CCI'),
        (AssetType.INDUSTRIAL_CREDIT_NOTE_ID, 'CCID'),
        (AssetType.REAL_ESTATE_CREDIT_CERTIFICATE, 'CCIM'),
        (AssetType.THIRD_PARTY_CREDIT_CONTRACT, 'CCT'),
        (AssetType.AGRICULTURAL_DEPOSIT_CERTIFICATE, 'CDA'),
        (AssetType.BANK_DEPOSIT_CERTIFICATE, 'CDB'),
        (AssetType.BANK_DEPOSIT_CERTIFICATE_RURAL, 'CDBR'),
        (AssetType.BANK_DEPOSIT_CERTIFICATE_SUBORDINATED, 'CDBS'),
        (AssetType.BANK_DEPOSIT_CERTIFICATE_LINKED, 'CDBV'),
        (AssetType.AGRIBUSINESS_RECEIVABLES_CERTIFICATE, 'CDCA'),
        (AssetType.DEBENTURE_NOTE, 'CDEB'),
        (AssetType.PUBLIC_DEBT_CERTIFICATE, 'CDP'),
        (AssetType.OPEN_FUND_QUOTA, 'CFA'),
        (AssetType.CLOSED_FUND_QUOTA, 'CFF'),
        (AssetType.NATIONAL_TREASURY_FINANCIAL_CERTIFICATE, 'CFT'),
        (AssetType.AUDIOVISUAL_INVESTMENT_CERTIFICATE, 'CIAV'),
        (AssetType.MERCHANDISE_CERTIFICATE, 'CM'),
        (AssetType.MERCHANT_CONTRACT, 'CMER'),
        (AssetType.STRUCTURED_OPERATIONS_CERTIFICATE, 'COE'),
        (AssetType.AGRICULTURAL_PRODUCT_SALE_OPTION, 'COPV'),
        (AssetType.PRIVATIZATION_CERTIFICATE, 'CP'),
        (AssetType.RURAL_PRODUCT_NOTE, 'CPR'),
        (AssetType.AGRIBUSINESS_RECEIVABLES_CERTIFICATE_CRA, 'CRA'),
        (AssetType.CARD_SETTLEMENT_CONTINGENCY, 'CRC'),
        (AssetType.RURAL_MORTGAGE_NOTE, 'CRH'),
        (AssetType.REAL_ESTATE_RECEIVABLES_CERTIFICATE, 'CRI'),
        (AssetType.RURAL_PLEDGE_NOTE, 'CRP'),
        (AssetType.RURAL_PLEDGE_AND_MORTGAGE_NOTE, 'CRPH'),
        (AssetType.SECURITIZED_CREDIT, 'CSEC'),
        (AssetType.ELECTRIC_ENERGY_FORWARD_CERTIFICATE, 'CTEE'),
        (AssetType.CREDIT_RIGHT, 'CTRA'),
        (AssetType.CREDIT_DERIVATIVES_CONTRACT, 'DCRD'),
        (AssetType.DEBENTURE, 'DEB'),
        (AssetType.INTERBANK_DEPOSIT, 'DI'),
        (AssetType.INTERBANK_DEPOSIT_RENEGOTIATED, 'DIDR'),
        (AssetType.INTERBANK_DEPOSIT_HOUSING, 'DIH'),
        (AssetType.INTERBANK_DEPOSIT_REAL_ESTATE, 'DII'),
        (AssetType.INTERBANK_DEPOSIT_MICROFINANCE, 'DIM'),
        (AssetType.INTERBANK_DEPOSIT_RURAL, 'DIR'),
        (AssetType.INTERBANK_DEPOSIT_COOPERATIVE, 'DIRC'),
        (AssetType.INTERBANK_DEPOSIT_PROGER, 'DIRG'),
        (AssetType.INTERBANK_DEPOSIT_PRONAF, 'DIRP'),
        (AssetType.INTERBANK_DEPOSIT_RURAL_SAVINGS, 'DIRR'),
        (AssetType.TERM_DEPOSIT_FGC, 'DPGE'),
        (AssetType.EXPORT_NOTES, 'EXPN'),
        (AssetType.SOCIAL_DEVELOPMENT_FUND_QUOTA, 'FDS'),
        (AssetType.LEASING_LETTER, 'LAM'),
        (AssetType.CENTRAL_BANK_BILL, 'LBC'),
        (AssetType.EXCHANGE_BILL, 'LC'),
        (AssetType.AGRIBUSINESS_CREDIT_LETTER, 'LCA'),
        (AssetType.DEVELOPMENT_CREDIT_LETTER, 'LCD'),
        (AssetType.REAL_ESTATE_CREDIT_LETTER, 'LCI'),
        (AssetType.WARRANT_EXCHANGE_BILL, 'LCW'),
        (AssetType.FINANCIAL_BILL, 'LF'),
        (AssetType.FINANCIAL_BILL_COMPLEMENTARY_CAPITAL, 'LFSC'),
        (AssetType.FINANCIAL_BILL_LEVEL_II, 'LFSN'),
        (AssetType.FINANCIAL_BILL_PRIMARY_CAPITAL, 'LFSP'),
        (AssetType.FINANCIAL_BILL_SUBORDINATED, 'LFS'),
        (AssetType.TREASURY_FINANCIAL_BILL, 'LFT'),
        (AssetType.TREASURY_FINANCIAL_BILL_SERIES_A, 'LFTA'),
        (AssetType.TREASURY_FINANCIAL_BILL_SERIES_B, 'LFTB'),
        (AssetType.STATE_TREASURY_FINANCIAL_BILL, 'LFTE'),
        (AssetType.MUNICIPAL_TREASURY_FINANCIAL_BILL, 'LFTM'),
        (AssetType.LINKED_FINANCIAL_BILL, 'LFV'),
        (AssetType.MORTGAGE_LETTER, 'LH'),
        (AssetType.COVERED_REAL_ESTATE_LETTER, 'LIG'),
        (AssetType.NATIONAL_TREASURY_BILL, 'LTN'),
        (AssetType.CENTRAL_BANK_NOTES_SERIES_A, 'NBCA'),
        (AssetType.CENTRAL_BANK_NOTES_SERIES_E, 'NBCE'),
        (AssetType.CENTRAL_BANK_NOTES_SERIES_F, 'NBCF'),
        (AssetType.COMMERCIAL_NOTE, 'NC'),
        (AssetType.AGRIBUSINESS_COMMERCIAL_NOTE, 'NCA'),
        (AssetType.COMMERCIAL_CREDIT_NOTE_NCC, 'NCC'),
        (AssetType.EXPORT_CREDIT_NOTE_NCE, 'NCE'),
        (AssetType.INDUSTRIAL_CREDIT_NOTE_NCI, 'NCI'),
        (AssetType.RURAL_CREDIT_NOTE, 'NCR'),
        (AssetType.NETTING_AGREEMENT, 'NET'),
        (AssetType.PROMISSORY_NOTE, 'NP'),
        (AssetType.NATIONAL_TREASURY_NOTES_SERIES_A, 'NTNA'),
        (AssetType.NATIONAL_TREASURY_NOTES_SERIES_B, 'NTNB'),
        (AssetType.NATIONAL_TREASURY_NOTES_SERIES_C, 'NTNC'),
        (AssetType.NATIONAL_TREASURY_NOTES_SERIES_D, 'NTND'),
        (AssetType.NATIONAL_TREASURY_NOTES_SERIES_E, 'NTNE'),
        (AssetType.NATIONAL_TREASURY_NOTES_SERIES_F, 'NTNF'),
        (AssetType.NATIONAL_TREASURY_NOTES_SERIES_H, 'NTNH'),
        (AssetType.NATIONAL_TREASURY_NOTES_SERIES_I, 'NTNI'),
        (AssetType.NATIONAL_TREASURY_NOTES_SERIES_L, 'NTNL'),
        (AssetType.NATIONAL_TREASURY_NOTES_SERIES_M, 'NTNM'),
        (AssetType.NATIONAL_TREASURY_NOTES_SERIES_P, 'NTNP'),
        (AssetType.NATIONAL_TREASURY_NOTES_SERIES_R, 'NTNR'),
        (AssetType.NATIONAL_TREASURY_NOTES_SERIES_S, 'NTNS'),
        (AssetType.NATIONAL_TREASURY_NOTES_SERIES_T, 'NTNT'),
        (AssetType.NATIONAL_TREASURY_NOTES_SERIES_U, 'NTNU'),
        (AssetType.IFC_OBLIGATIONS, 'OBR'),
        (AssetType.FLEXIBLE_CURRENCY_CALL_OPTION, 'OFCC'),
        (AssetType.NATIONAL_DEVELOPMENT_FUND_OBLIGATIONS, 'OFND'),
        (AssetType.FLEXIBLE_CURRENCY_PUT_OPTION, 'OFVC'),
        (AssetType.GOLD, 'OURO'),
        (AssetType.OTHERS, 'OUT'),
        (AssetType.BANK_DEPOSIT_RECEIPT, 'RDB'),
        (AssetType.COOPERATIVE_DEPOSIT_RECEIPT, 'RDC'),
        (AssetType.SWAP_CONTRACT, 'SWAP'),
        (AssetType.MERCHANDISE_FORWARD_CONTRACT, 'TCO'),
        (AssetType.AGRARIAN_DEBT_SECURITY, 'TDA'),
        (AssetType.ECONOMIC_DEVELOPMENT_SECURITY, 'TDE'),
        (AssetType.TERM21, 'TER'),
        (AssetType.CURRENCY_FORWARD_CONTRACT, 'TMO'),
        (AssetType.MONETARY_UNIT, 'UM'),
        (AssetType.AGRICULTURAL_WARRANT, 'WA'),
        (AssetType.WARRANT, 'WARR'),
    ],
)
def test_asset_type_values_to_xml_value(input_value: AssetType, expected_enum: str) -> None:
    assert input_value.to_xml_value() == expected_enum


@pytest.mark.parametrize(
    ('input_value', 'expected_enum'),
    [
        ('ACAO', AssetType.STOCKS),
        ('ACI', AssetType.INVESTMENT_PORTFOLIO_ASSETS),
        ('ADA', AssetType.AGRICULTURAL_DEBT_EXTENSION),
        ('ANTE', AssetType.RECEIVABLES_ADVANCE_ISSUER),
        ('ANTR', AssetType.RECEIVABLES_ADVANCE_ACQUIRER),
        ('BBC', AssetType.CENTRAL_BANK_BOND),
        ('BBCA', AssetType.CENTRAL_BANK_BOND_SERIES_A),
        ('BOX2', AssetType.BOX_TWO_LEGS),
        ('BTN', AssetType.NATIONAL_TREASURY_BOND_BTN),
        ('CAC', AssetType.CREDIT_OPENING_CONTRACT),
        ('CC3', AssetType.CREDIT_ASSIGNMENT),
        ('CCB', AssetType.BANK_CREDIT_NOTE),
        ('CCC', AssetType.COMMERCIAL_CREDIT_NOTE),
        ('CCCB', AssetType.BANK_CREDIT_NOTE_CERTIFICATE),
        ('CCE', AssetType.EXPORT_CREDIT_NOTE),
        ('CCI', AssetType.INDUSTRIAL_CREDIT_NOTE),
        ('CCID', AssetType.INDUSTRIAL_CREDIT_NOTE_ID),
        ('CCIM', AssetType.REAL_ESTATE_CREDIT_CERTIFICATE),
        ('CCT', AssetType.THIRD_PARTY_CREDIT_CONTRACT),
        ('CDA', AssetType.AGRICULTURAL_DEPOSIT_CERTIFICATE),
        ('CDB', AssetType.BANK_DEPOSIT_CERTIFICATE),
        ('CDBR', AssetType.BANK_DEPOSIT_CERTIFICATE_RURAL),
        ('CDBS', AssetType.BANK_DEPOSIT_CERTIFICATE_SUBORDINATED),
        ('CDBV', AssetType.BANK_DEPOSIT_CERTIFICATE_LINKED),
        ('CDCA', AssetType.AGRIBUSINESS_RECEIVABLES_CERTIFICATE),
        ('CDEB', AssetType.DEBENTURE_NOTE),
        ('CDP', AssetType.PUBLIC_DEBT_CERTIFICATE),
        ('CFA', AssetType.OPEN_FUND_QUOTA),
        ('CFF', AssetType.CLOSED_FUND_QUOTA),
        ('CFT', AssetType.NATIONAL_TREASURY_FINANCIAL_CERTIFICATE),
        ('CIAV', AssetType.AUDIOVISUAL_INVESTMENT_CERTIFICATE),
        ('CM', AssetType.MERCHANDISE_CERTIFICATE),
        ('CMER', AssetType.MERCHANT_CONTRACT),
        ('COE', AssetType.STRUCTURED_OPERATIONS_CERTIFICATE),
        ('COPV', AssetType.AGRICULTURAL_PRODUCT_SALE_OPTION),
        ('CP', AssetType.PRIVATIZATION_CERTIFICATE),
        ('CPR', AssetType.RURAL_PRODUCT_NOTE),
        ('CRA', AssetType.AGRIBUSINESS_RECEIVABLES_CERTIFICATE_CRA),
        ('CRC', AssetType.CARD_SETTLEMENT_CONTINGENCY),
        ('CRH', AssetType.RURAL_MORTGAGE_NOTE),
        ('CRI', AssetType.REAL_ESTATE_RECEIVABLES_CERTIFICATE),
        ('CRP', AssetType.RURAL_PLEDGE_NOTE),
        ('CRPH', AssetType.RURAL_PLEDGE_AND_MORTGAGE_NOTE),
        ('CSEC', AssetType.SECURITIZED_CREDIT),
        ('CTEE', AssetType.ELECTRIC_ENERGY_FORWARD_CERTIFICATE),
        ('CTRA', AssetType.CREDIT_RIGHT),
        ('DCRD', AssetType.CREDIT_DERIVATIVES_CONTRACT),
        ('DEB', AssetType.DEBENTURE),
        ('DI', AssetType.INTERBANK_DEPOSIT),
        ('DIDR', AssetType.INTERBANK_DEPOSIT_RENEGOTIATED),
        ('DIH', AssetType.INTERBANK_DEPOSIT_HOUSING),
        ('DII', AssetType.INTERBANK_DEPOSIT_REAL_ESTATE),
        ('DIM', AssetType.INTERBANK_DEPOSIT_MICROFINANCE),
        ('DIR', AssetType.INTERBANK_DEPOSIT_RURAL),
        ('DIRC', AssetType.INTERBANK_DEPOSIT_COOPERATIVE),
        ('DIRG', AssetType.INTERBANK_DEPOSIT_PROGER),
        ('DIRP', AssetType.INTERBANK_DEPOSIT_PRONAF),
        ('DIRR', AssetType.INTERBANK_DEPOSIT_RURAL_SAVINGS),
        ('DPGE', AssetType.TERM_DEPOSIT_FGC),
        ('EXPN', AssetType.EXPORT_NOTES),
        ('FDS', AssetType.SOCIAL_DEVELOPMENT_FUND_QUOTA),
        ('LAM', AssetType.LEASING_LETTER),
        ('LBC', AssetType.CENTRAL_BANK_BILL),
        ('LC', AssetType.EXCHANGE_BILL),
        ('LCA', AssetType.AGRIBUSINESS_CREDIT_LETTER),
        ('LCD', AssetType.DEVELOPMENT_CREDIT_LETTER),
        ('LCI', AssetType.REAL_ESTATE_CREDIT_LETTER),
        ('LCW', AssetType.WARRANT_EXCHANGE_BILL),
        ('LF', AssetType.FINANCIAL_BILL),
        ('LFSC', AssetType.FINANCIAL_BILL_COMPLEMENTARY_CAPITAL),
        ('LFSN', AssetType.FINANCIAL_BILL_LEVEL_II),
        ('LFSP', AssetType.FINANCIAL_BILL_PRIMARY_CAPITAL),
        ('LFS', AssetType.FINANCIAL_BILL_SUBORDINATED),
        ('LFT', AssetType.TREASURY_FINANCIAL_BILL),
        ('LFTA', AssetType.TREASURY_FINANCIAL_BILL_SERIES_A),
        ('LFTB', AssetType.TREASURY_FINANCIAL_BILL_SERIES_B),
        ('LFTE', AssetType.STATE_TREASURY_FINANCIAL_BILL),
        ('LFTM', AssetType.MUNICIPAL_TREASURY_FINANCIAL_BILL),
        ('LFV', AssetType.LINKED_FINANCIAL_BILL),
        ('LH', AssetType.MORTGAGE_LETTER),
        ('LIG', AssetType.COVERED_REAL_ESTATE_LETTER),
        ('LTN', AssetType.NATIONAL_TREASURY_BILL),
        ('NBCA', AssetType.CENTRAL_BANK_NOTES_SERIES_A),
        ('NBCE', AssetType.CENTRAL_BANK_NOTES_SERIES_E),
        ('NBCF', AssetType.CENTRAL_BANK_NOTES_SERIES_F),
        ('NC', AssetType.COMMERCIAL_NOTE),
        ('NCA', AssetType.AGRIBUSINESS_COMMERCIAL_NOTE),
        ('NCC', AssetType.COMMERCIAL_CREDIT_NOTE_NCC),
        ('NCE', AssetType.EXPORT_CREDIT_NOTE_NCE),
        ('NCI', AssetType.INDUSTRIAL_CREDIT_NOTE_NCI),
        ('NCR', AssetType.RURAL_CREDIT_NOTE),
        ('NET', AssetType.NETTING_AGREEMENT),
        ('NP', AssetType.PROMISSORY_NOTE),
        ('NTNA', AssetType.NATIONAL_TREASURY_NOTES_SERIES_A),
        ('NTNB', AssetType.NATIONAL_TREASURY_NOTES_SERIES_B),
        ('NTNC', AssetType.NATIONAL_TREASURY_NOTES_SERIES_C),
        ('NTND', AssetType.NATIONAL_TREASURY_NOTES_SERIES_D),
        ('NTNE', AssetType.NATIONAL_TREASURY_NOTES_SERIES_E),
        ('NTNF', AssetType.NATIONAL_TREASURY_NOTES_SERIES_F),
        ('NTNH', AssetType.NATIONAL_TREASURY_NOTES_SERIES_H),
        ('NTNI', AssetType.NATIONAL_TREASURY_NOTES_SERIES_I),
        ('NTNL', AssetType.NATIONAL_TREASURY_NOTES_SERIES_L),
        ('NTNM', AssetType.NATIONAL_TREASURY_NOTES_SERIES_M),
        ('NTNP', AssetType.NATIONAL_TREASURY_NOTES_SERIES_P),
        ('NTNR', AssetType.NATIONAL_TREASURY_NOTES_SERIES_R),
        ('NTNS', AssetType.NATIONAL_TREASURY_NOTES_SERIES_S),
        ('NTNT', AssetType.NATIONAL_TREASURY_NOTES_SERIES_T),
        ('NTNU', AssetType.NATIONAL_TREASURY_NOTES_SERIES_U),
        ('OBR', AssetType.IFC_OBLIGATIONS),
        ('OFCC', AssetType.FLEXIBLE_CURRENCY_CALL_OPTION),
        ('OFND', AssetType.NATIONAL_DEVELOPMENT_FUND_OBLIGATIONS),
        ('OFVC', AssetType.FLEXIBLE_CURRENCY_PUT_OPTION),
        ('OURO', AssetType.GOLD),
        ('OUT', AssetType.OTHERS),
        ('RDB', AssetType.BANK_DEPOSIT_RECEIPT),
        ('RDC', AssetType.COOPERATIVE_DEPOSIT_RECEIPT),
        ('SWAP', AssetType.SWAP_CONTRACT),
        ('TCO', AssetType.MERCHANDISE_FORWARD_CONTRACT),
        ('TDA', AssetType.AGRARIAN_DEBT_SECURITY),
        ('TDE', AssetType.ECONOMIC_DEVELOPMENT_SECURITY),
        ('TER', AssetType.TERM21),
        ('TMO', AssetType.CURRENCY_FORWARD_CONTRACT),
        ('UM', AssetType.MONETARY_UNIT),
        ('WA', AssetType.AGRICULTURAL_WARRANT),
        ('WARR', AssetType.WARRANT),
    ],
)
def test_asset_type_values_from_xml_value(input_value: str, expected_enum: AssetType) -> None:
    assert AssetType.from_xml_value(input_value) == expected_enum


@pytest.mark.parametrize(
    ('input_value', 'expected_enum'),
    [
        ('stocks', AssetType.STOCKS),
        ('investment_portfolio_assets', AssetType.INVESTMENT_PORTFOLIO_ASSETS),
        ('agricultural_debt_extension', AssetType.AGRICULTURAL_DEBT_EXTENSION),
        ('receivables_advance_issuer', AssetType.RECEIVABLES_ADVANCE_ISSUER),
        ('receivables_advance_acquirer', AssetType.RECEIVABLES_ADVANCE_ACQUIRER),
        ('central_bank_bond', AssetType.CENTRAL_BANK_BOND),
        ('central_bank_bond_series_a', AssetType.CENTRAL_BANK_BOND_SERIES_A),
        ('box_two_legs', AssetType.BOX_TWO_LEGS),
        ('national_treasury_bond_btn', AssetType.NATIONAL_TREASURY_BOND_BTN),
        ('credit_opening_contract', AssetType.CREDIT_OPENING_CONTRACT),
        ('credit_assignment', AssetType.CREDIT_ASSIGNMENT),
        ('bank_credit_note', AssetType.BANK_CREDIT_NOTE),
        ('commercial_credit_note', AssetType.COMMERCIAL_CREDIT_NOTE),
        ('bank_credit_note_certificate', AssetType.BANK_CREDIT_NOTE_CERTIFICATE),
        ('export_credit_note', AssetType.EXPORT_CREDIT_NOTE),
        ('industrial_credit_note', AssetType.INDUSTRIAL_CREDIT_NOTE),
        ('industrial_credit_note_id', AssetType.INDUSTRIAL_CREDIT_NOTE_ID),
        ('real_estate_credit_certificate', AssetType.REAL_ESTATE_CREDIT_CERTIFICATE),
        ('third_party_credit_contract', AssetType.THIRD_PARTY_CREDIT_CONTRACT),
        ('agricultural_deposit_certificate', AssetType.AGRICULTURAL_DEPOSIT_CERTIFICATE),
        ('bank_deposit_certificate', AssetType.BANK_DEPOSIT_CERTIFICATE),
        ('bank_deposit_certificate_rural', AssetType.BANK_DEPOSIT_CERTIFICATE_RURAL),
        ('bank_deposit_certificate_subordinated', AssetType.BANK_DEPOSIT_CERTIFICATE_SUBORDINATED),
        ('bank_deposit_certificate_linked', AssetType.BANK_DEPOSIT_CERTIFICATE_LINKED),
        ('agribusiness_receivables_certificate', AssetType.AGRIBUSINESS_RECEIVABLES_CERTIFICATE),
        ('debenture_note', AssetType.DEBENTURE_NOTE),
        ('public_debt_certificate', AssetType.PUBLIC_DEBT_CERTIFICATE),
        ('open_fund_quota', AssetType.OPEN_FUND_QUOTA),
        ('closed_fund_quota', AssetType.CLOSED_FUND_QUOTA),
        ('national_treasury_financial_certificate', AssetType.NATIONAL_TREASURY_FINANCIAL_CERTIFICATE),
        ('audiovisual_investment_certificate', AssetType.AUDIOVISUAL_INVESTMENT_CERTIFICATE),
        ('merchandise_certificate', AssetType.MERCHANDISE_CERTIFICATE),
        ('merchant_contract', AssetType.MERCHANT_CONTRACT),
        ('structured_operations_certificate', AssetType.STRUCTURED_OPERATIONS_CERTIFICATE),
        ('agricultural_product_sale_option', AssetType.AGRICULTURAL_PRODUCT_SALE_OPTION),
        ('privatization_certificate', AssetType.PRIVATIZATION_CERTIFICATE),
        ('rural_product_note', AssetType.RURAL_PRODUCT_NOTE),
        ('agribusiness_receivables_certificate_cra', AssetType.AGRIBUSINESS_RECEIVABLES_CERTIFICATE_CRA),
        ('card_settlement_contingency', AssetType.CARD_SETTLEMENT_CONTINGENCY),
        ('rural_mortgage_note', AssetType.RURAL_MORTGAGE_NOTE),
        ('real_estate_receivables_certificate', AssetType.REAL_ESTATE_RECEIVABLES_CERTIFICATE),
        ('rural_pledge_note', AssetType.RURAL_PLEDGE_NOTE),
        ('rural_pledge_and_mortgage_note', AssetType.RURAL_PLEDGE_AND_MORTGAGE_NOTE),
        ('securitized_credit', AssetType.SECURITIZED_CREDIT),
        ('electric_energy_forward_certificate', AssetType.ELECTRIC_ENERGY_FORWARD_CERTIFICATE),
        ('credit_right', AssetType.CREDIT_RIGHT),
        ('credit_derivatives_contract', AssetType.CREDIT_DERIVATIVES_CONTRACT),
        ('debenture', AssetType.DEBENTURE),
        ('interbank_deposit', AssetType.INTERBANK_DEPOSIT),
        ('interbank_deposit_renegotiated', AssetType.INTERBANK_DEPOSIT_RENEGOTIATED),
        ('interbank_deposit_housing', AssetType.INTERBANK_DEPOSIT_HOUSING),
        ('interbank_deposit_real_estate', AssetType.INTERBANK_DEPOSIT_REAL_ESTATE),
        ('interbank_deposit_microfinance', AssetType.INTERBANK_DEPOSIT_MICROFINANCE),
        ('interbank_deposit_rural', AssetType.INTERBANK_DEPOSIT_RURAL),
        ('interbank_deposit_cooperative', AssetType.INTERBANK_DEPOSIT_COOPERATIVE),
        ('interbank_deposit_proger', AssetType.INTERBANK_DEPOSIT_PROGER),
        ('interbank_deposit_pronaf', AssetType.INTERBANK_DEPOSIT_PRONAF),
        ('interbank_deposit_rural_savings', AssetType.INTERBANK_DEPOSIT_RURAL_SAVINGS),
        ('term_deposit_fgc', AssetType.TERM_DEPOSIT_FGC),
        ('export_notes', AssetType.EXPORT_NOTES),
        ('social_development_fund_quota', AssetType.SOCIAL_DEVELOPMENT_FUND_QUOTA),
        ('leasing_letter', AssetType.LEASING_LETTER),
        ('central_bank_bill', AssetType.CENTRAL_BANK_BILL),
        ('exchange_bill', AssetType.EXCHANGE_BILL),
        ('agribusiness_credit_letter', AssetType.AGRIBUSINESS_CREDIT_LETTER),
        ('development_credit_letter', AssetType.DEVELOPMENT_CREDIT_LETTER),
        ('real_estate_credit_letter', AssetType.REAL_ESTATE_CREDIT_LETTER),
        ('warrant_exchange_bill', AssetType.WARRANT_EXCHANGE_BILL),
        ('financial_bill', AssetType.FINANCIAL_BILL),
        ('financial_bill_complementary_capital', AssetType.FINANCIAL_BILL_COMPLEMENTARY_CAPITAL),
        ('financial_bill_level_ii', AssetType.FINANCIAL_BILL_LEVEL_II),
        ('financial_bill_primary_capital', AssetType.FINANCIAL_BILL_PRIMARY_CAPITAL),
        ('financial_bill_subordinated', AssetType.FINANCIAL_BILL_SUBORDINATED),
        ('treasury_financial_bill', AssetType.TREASURY_FINANCIAL_BILL),
        ('treasury_financial_bill_series_a', AssetType.TREASURY_FINANCIAL_BILL_SERIES_A),
        ('treasury_financial_bill_series_b', AssetType.TREASURY_FINANCIAL_BILL_SERIES_B),
        ('state_treasury_financial_bill', AssetType.STATE_TREASURY_FINANCIAL_BILL),
        ('municipal_treasury_financial_bill', AssetType.MUNICIPAL_TREASURY_FINANCIAL_BILL),
        ('linked_financial_bill', AssetType.LINKED_FINANCIAL_BILL),
        ('mortgage_letter', AssetType.MORTGAGE_LETTER),
        ('covered_real_estate_letter', AssetType.COVERED_REAL_ESTATE_LETTER),
        ('national_treasury_bill', AssetType.NATIONAL_TREASURY_BILL),
        ('central_bank_notes_series_a', AssetType.CENTRAL_BANK_NOTES_SERIES_A),
        ('central_bank_notes_series_e', AssetType.CENTRAL_BANK_NOTES_SERIES_E),
        ('central_bank_notes_series_f', AssetType.CENTRAL_BANK_NOTES_SERIES_F),
        ('commercial_note', AssetType.COMMERCIAL_NOTE),
        ('agribusiness_commercial_note', AssetType.AGRIBUSINESS_COMMERCIAL_NOTE),
        ('commercial_credit_note_ncc', AssetType.COMMERCIAL_CREDIT_NOTE_NCC),
        ('export_credit_note_nce', AssetType.EXPORT_CREDIT_NOTE_NCE),
        ('industrial_credit_note_nci', AssetType.INDUSTRIAL_CREDIT_NOTE_NCI),
        ('rural_credit_note', AssetType.RURAL_CREDIT_NOTE),
        ('netting_agreement', AssetType.NETTING_AGREEMENT),
        ('promissory_note', AssetType.PROMISSORY_NOTE),
        ('national_treasury_notes_series_a', AssetType.NATIONAL_TREASURY_NOTES_SERIES_A),
        ('national_treasury_notes_series_b', AssetType.NATIONAL_TREASURY_NOTES_SERIES_B),
        ('national_treasury_notes_series_c', AssetType.NATIONAL_TREASURY_NOTES_SERIES_C),
        ('national_treasury_notes_series_d', AssetType.NATIONAL_TREASURY_NOTES_SERIES_D),
        ('national_treasury_notes_series_e', AssetType.NATIONAL_TREASURY_NOTES_SERIES_E),
        ('national_treasury_notes_series_f', AssetType.NATIONAL_TREASURY_NOTES_SERIES_F),
        ('national_treasury_notes_series_h', AssetType.NATIONAL_TREASURY_NOTES_SERIES_H),
        ('national_treasury_notes_series_i', AssetType.NATIONAL_TREASURY_NOTES_SERIES_I),
        ('national_treasury_notes_series_l', AssetType.NATIONAL_TREASURY_NOTES_SERIES_L),
        ('national_treasury_notes_series_m', AssetType.NATIONAL_TREASURY_NOTES_SERIES_M),
        ('national_treasury_notes_series_p', AssetType.NATIONAL_TREASURY_NOTES_SERIES_P),
        ('national_treasury_notes_series_r', AssetType.NATIONAL_TREASURY_NOTES_SERIES_R),
        ('national_treasury_notes_series_s', AssetType.NATIONAL_TREASURY_NOTES_SERIES_S),
        ('national_treasury_notes_series_t', AssetType.NATIONAL_TREASURY_NOTES_SERIES_T),
        ('national_treasury_notes_series_u', AssetType.NATIONAL_TREASURY_NOTES_SERIES_U),
        ('ifc_obligations', AssetType.IFC_OBLIGATIONS),
        ('flexible_currency_call_option', AssetType.FLEXIBLE_CURRENCY_CALL_OPTION),
        ('national_development_fund_obligations', AssetType.NATIONAL_DEVELOPMENT_FUND_OBLIGATIONS),
        ('flexible_currency_put_option', AssetType.FLEXIBLE_CURRENCY_PUT_OPTION),
        ('gold', AssetType.GOLD),
        ('others', AssetType.OTHERS),
        ('bank_deposit_receipt', AssetType.BANK_DEPOSIT_RECEIPT),
        ('cooperative_deposit_receipt', AssetType.COOPERATIVE_DEPOSIT_RECEIPT),
        ('swap_contract', AssetType.SWAP_CONTRACT),
        ('merchandise_forward_contract', AssetType.MERCHANDISE_FORWARD_CONTRACT),
        ('agrarian_debt_security', AssetType.AGRARIAN_DEBT_SECURITY),
        ('economic_development_security', AssetType.ECONOMIC_DEVELOPMENT_SECURITY),
        ('term21', AssetType.TERM21),
        ('currency_forward_contract', AssetType.CURRENCY_FORWARD_CONTRACT),
        ('monetary_unit', AssetType.MONETARY_UNIT),
        ('agricultural_warrant', AssetType.AGRICULTURAL_WARRANT),
        ('warrant', AssetType.WARRANT),
    ],
)
def test_asset_type_accepts_case_insensitive_values(input_value: str, expected_enum: AssetType) -> None:
    assert AssetType(input_value) is expected_enum


@pytest.mark.parametrize(
    'asset_description',
    [
        'Asset description valid',
        'Asset Description Valid 123',
    ],
)
def test_asset_description_accepts_valid_values(asset_description: str) -> None:
    model = AssetDescriptionModel(asset_description=asset_description)
    assert model.asset_description == asset_description


def test_asset_description_accepts_whitespace() -> None:
    model = AssetDescriptionModel(asset_description='   Asset Description   ')
    assert model.asset_description == 'Asset Description'


@pytest.mark.parametrize(
    'asset_description',
    [
        'Description' + '0' * 99,  # Too long
    ],
)
def test_asset_description_rejects_invalid_values(asset_description: str) -> None:
    with pytest.raises(ValidationError):
        AssetDescriptionModel(asset_description=asset_description)


@pytest.mark.parametrize(
    'participant_identifier',
    [
        '01234567',
        '12345678',
        '00000011',
    ],
)
def test_participant_identifier_accepts_valid_values(participant_identifier: str) -> None:
    model = ParticipantIdentifierModel(participant_identifier=participant_identifier)
    assert model.participant_identifier == participant_identifier


def test_participant_identifier_accepts_whitespace() -> None:
    model = ParticipantIdentifierModel(participant_identifier='   12345678   ')
    assert model.participant_identifier == '12345678'


@pytest.mark.parametrize(
    'participant_identifier',
    [
        '8678' + '0' * 9,  # Too long
    ],
)
def test_participant_identifier_rejects_invalid_values(participant_identifier: str) -> None:
    with pytest.raises(ValidationError):
        ParticipantIdentifierModel(participant_identifier=participant_identifier)


@pytest.mark.parametrize(
    ('input_value', 'expected_enum'),
    [
        ('EFFECTIVE', LdlSettlementStatus.EFFECTIVE),
        ('CANCELLED', LdlSettlementStatus.CANCELLED),
        ('CANCELLED_CONTINGENCY', LdlSettlementStatus.CANCELLED_CONTINGENCY),
        ('PENDING_STR', LdlSettlementStatus.PENDING_STR),
        ('PENDING_STR_CONTINGENCY', LdlSettlementStatus.PENDING_STR_CONTINGENCY),
        ('EFFECTIVE_CONTINGENCY', LdlSettlementStatus.EFFECTIVE_CONTINGENCY),
        ('REJECTED_IF_CONDITION', LdlSettlementStatus.REJECTED_IF_CONDITION),
        ('REJECTED_IF_CONDITION_CONTINGENCY', LdlSettlementStatus.REJECTED_IF_CONDITION_CONTINGENCY),
        ('REJECTED_AFTER_HOURS', LdlSettlementStatus.REJECTED_AFTER_HOURS),
        ('REJECTED_AFTER_HOURS_CONTINGENCY', LdlSettlementStatus.REJECTED_AFTER_HOURS_CONTINGENCY),
        ('PENDING_REJECTED_AFTER_HOURS_CONTINGENCY', LdlSettlementStatus.PENDING_REJECTED_AFTER_HOURS_CONTINGENCY),
        ('EFFECTIVE_OPTIMIZATION', LdlSettlementStatus.EFFECTIVE_OPTIMIZATION),
        ('REJECTED_NO_BALANCE', LdlSettlementStatus.REJECTED_NO_BALANCE),
        ('REJECTED_AFTER_HOURS_SIMPLE', LdlSettlementStatus.REJECTED_AFTER_HOURS_SIMPLE),
        ('REJECTED_NO_BALANCE_CONTINGENCY', LdlSettlementStatus.REJECTED_NO_BALANCE_CONTINGENCY),
    ],
)
def test_ldl_settlement_status_accepts_exact_values(input_value: str, expected_enum: LdlSettlementStatus) -> None:
    assert LdlSettlementStatus(input_value) is expected_enum


@pytest.mark.parametrize(
    ('input_value', 'expected_enum'),
    [
        (LdlSettlementStatus.EFFECTIVE, '1'),
        (LdlSettlementStatus.CANCELLED, '14'),
        (LdlSettlementStatus.CANCELLED_CONTINGENCY, '15'),
        (LdlSettlementStatus.PENDING_STR, '17'),
        (LdlSettlementStatus.PENDING_STR_CONTINGENCY, '19'),
        (LdlSettlementStatus.EFFECTIVE_CONTINGENCY, '2'),
        (LdlSettlementStatus.REJECTED_IF_CONDITION, '22'),
        (LdlSettlementStatus.REJECTED_IF_CONDITION_CONTINGENCY, '23'),
        (LdlSettlementStatus.REJECTED_AFTER_HOURS, '24'),
        (LdlSettlementStatus.PENDING_REJECTED_AFTER_HOURS_CONTINGENCY, '25'),
        (LdlSettlementStatus.EFFECTIVE_OPTIMIZATION, '3'),
        (LdlSettlementStatus.REJECTED_NO_BALANCE, '5'),
        (LdlSettlementStatus.REJECTED_AFTER_HOURS_SIMPLE, '6'),
        (LdlSettlementStatus.REJECTED_AFTER_HOURS_CONTINGENCY, '8'),
        (LdlSettlementStatus.REJECTED_NO_BALANCE_CONTINGENCY, '9'),
    ],
)
def test_ldl_settlement_status_values_to_xml_value(input_value: LdlSettlementStatus, expected_enum: str) -> None:
    assert input_value.to_xml_value() == expected_enum


@pytest.mark.parametrize(
    ('input_value', 'expected_enum'),
    [
        ('1', LdlSettlementStatus.EFFECTIVE),
        ('14', LdlSettlementStatus.CANCELLED),
        ('15', LdlSettlementStatus.CANCELLED_CONTINGENCY),
        ('17', LdlSettlementStatus.PENDING_STR),
        ('19', LdlSettlementStatus.PENDING_STR_CONTINGENCY),
        ('2', LdlSettlementStatus.EFFECTIVE_CONTINGENCY),
        ('22', LdlSettlementStatus.REJECTED_IF_CONDITION),
        ('23', LdlSettlementStatus.REJECTED_IF_CONDITION_CONTINGENCY),
        ('24', LdlSettlementStatus.REJECTED_AFTER_HOURS),
        ('25', LdlSettlementStatus.PENDING_REJECTED_AFTER_HOURS_CONTINGENCY),
        ('3', LdlSettlementStatus.EFFECTIVE_OPTIMIZATION),
        ('5', LdlSettlementStatus.REJECTED_NO_BALANCE),
        ('6', LdlSettlementStatus.REJECTED_AFTER_HOURS_SIMPLE),
        ('8', LdlSettlementStatus.REJECTED_AFTER_HOURS_CONTINGENCY),
        ('9', LdlSettlementStatus.REJECTED_NO_BALANCE_CONTINGENCY),
    ],
)
def test_ldl_settlement_status_values_from_xml_value(input_value: str, expected_enum: LdlSettlementStatus) -> None:
    assert LdlSettlementStatus.from_xml_value(input_value) == expected_enum


@pytest.mark.parametrize(
    ('input_value', 'expected_enum'),
    [
        ('effective', LdlSettlementStatus.EFFECTIVE),
        ('cancelled', LdlSettlementStatus.CANCELLED),
        ('cancelled_contingency', LdlSettlementStatus.CANCELLED_CONTINGENCY),
        ('pending_str', LdlSettlementStatus.PENDING_STR),
        ('pending_str_contingency', LdlSettlementStatus.PENDING_STR_CONTINGENCY),
        ('effective_contingency', LdlSettlementStatus.EFFECTIVE_CONTINGENCY),
        ('rejected_if_condition', LdlSettlementStatus.REJECTED_IF_CONDITION),
        ('rejected_if_condition_contingency', LdlSettlementStatus.REJECTED_IF_CONDITION_CONTINGENCY),
        ('rejected_after_hours', LdlSettlementStatus.REJECTED_AFTER_HOURS),
        ('rejected_after_hours_contingency', LdlSettlementStatus.REJECTED_AFTER_HOURS_CONTINGENCY),
        ('pending_rejected_after_hours_contingency', LdlSettlementStatus.PENDING_REJECTED_AFTER_HOURS_CONTINGENCY),
        ('effective_optimization', LdlSettlementStatus.EFFECTIVE_OPTIMIZATION),
        ('rejected_no_balance', LdlSettlementStatus.REJECTED_NO_BALANCE),
        ('rejected_after_hours_simple', LdlSettlementStatus.REJECTED_AFTER_HOURS_SIMPLE),
        ('rejected_no_balance_contingency', LdlSettlementStatus.REJECTED_NO_BALANCE_CONTINGENCY),
    ],
)
def test_ldl_settlement_status_accepts_case_insensitive_values(
    input_value: str, expected_enum: LdlSettlementStatus
) -> None:
    assert LdlSettlementStatus(input_value) is expected_enum


@pytest.mark.parametrize(
    ('input_value', 'expected_enum'),
    [
        ('NOT_APPLICABLE', PaymentType.NOT_APPLICABLE),
        ('INTEREST_PAYMENT', PaymentType.INTEREST_PAYMENT),
        ('REMUNERATION', PaymentType.REMUNERATION),
        ('EARNING', PaymentType.EARNING),
        ('DIVIDENDS', PaymentType.DIVIDENDS),
        ('SUBSCRIPTION', PaymentType.SUBSCRIPTION),
        ('REDEMPTION', PaymentType.REDEMPTION),
        ('AMORTIZATION', PaymentType.AMORTIZATION),
        ('PROFIT_SHARING', PaymentType.PROFIT_SHARING),
        ('NO_REPACTUATION', PaymentType.NO_REPACTUATION),
        ('PREMIUM_PAYMENT', PaymentType.PREMIUM_PAYMENT),
        ('ISSUANCE', PaymentType.ISSUANCE),
        ('OTHER', PaymentType.OTHER),
    ],
)
def test_payment_type_accepts_exact_values(input_value: str, expected_enum: PaymentType) -> None:
    assert PaymentType(input_value) is expected_enum


@pytest.mark.parametrize(
    ('input_value', 'expected_enum'),
    [
        (PaymentType.NOT_APPLICABLE, '0'),
        (PaymentType.INTEREST_PAYMENT, '1'),
        (PaymentType.DIVIDENDS, '2'),
        (PaymentType.SUBSCRIPTION, '3'),
        (PaymentType.REDEMPTION, '4'),
        (PaymentType.AMORTIZATION, '5'),
        (PaymentType.PROFIT_SHARING, '6'),
        (PaymentType.NO_REPACTUATION, '7'),
        (PaymentType.PREMIUM_PAYMENT, '8'),
        (PaymentType.ISSUANCE, '9'),
        (PaymentType.REMUNERATION, '10'),
        (PaymentType.EARNING, '11'),
        (PaymentType.OTHER, '99'),
    ],
)
def test_payment_type_values_to_xml_value(input_value: PaymentType, expected_enum: str) -> None:
    assert input_value.to_xml_value() == expected_enum


@pytest.mark.parametrize(
    ('input_value', 'expected_enum'),
    [
        ('0', PaymentType.NOT_APPLICABLE),
        ('1', PaymentType.INTEREST_PAYMENT),
        ('2', PaymentType.DIVIDENDS),
        ('3', PaymentType.SUBSCRIPTION),
        ('4', PaymentType.REDEMPTION),
        ('5', PaymentType.AMORTIZATION),
        ('6', PaymentType.PROFIT_SHARING),
        ('7', PaymentType.NO_REPACTUATION),
        ('8', PaymentType.PREMIUM_PAYMENT),
        ('9', PaymentType.ISSUANCE),
        ('10', PaymentType.REMUNERATION),
        ('11', PaymentType.EARNING),
        ('99', PaymentType.OTHER),
    ],
)
def test_payment_type_values_from_xml_value(input_value: str, expected_enum: PaymentType) -> None:
    assert PaymentType.from_xml_value(input_value) == expected_enum


@pytest.mark.parametrize(
    ('input_value', 'expected_enum'),
    [
        ('not_applicable', PaymentType.NOT_APPLICABLE),
        ('interest_payment', PaymentType.INTEREST_PAYMENT),
        ('remuneration', PaymentType.REMUNERATION),
        ('earning', PaymentType.EARNING),
        ('dividends', PaymentType.DIVIDENDS),
        ('subscription', PaymentType.SUBSCRIPTION),
        ('redemption', PaymentType.REDEMPTION),
        ('amortization', PaymentType.AMORTIZATION),
        ('profit_sharing', PaymentType.PROFIT_SHARING),
        ('no_repactuation', PaymentType.NO_REPACTUATION),
        ('premium_payment', PaymentType.PREMIUM_PAYMENT),
        ('issuance', PaymentType.ISSUANCE),
        ('other', PaymentType.OTHER),
    ],
)
def test_payment_type_accepts_case_insensitive_values(input_value: str, expected_enum: PaymentType) -> None:
    assert PaymentType(input_value) is expected_enum


@pytest.mark.parametrize(
    ('input_value', 'expected_enum'),
    [
        ('DEPOSIT_OF_ASSET', MovementType.DEPOSIT_OF_ASSET),
        ('ISIN_CODE_UPDATE', MovementType.ISIN_CODE_UPDATE),
        ('DIVIDENDS_AND_CASH_BENEFITS', MovementType.DIVIDENDS_AND_CASH_BENEFITS),
        ('BONUS_AND_SPLIT_RIGHTS', MovementType.BONUS_AND_SPLIT_RIGHTS),
        ('SUBSCRIPTION_RIGHT', MovementType.SUBSCRIPTION_RIGHT),
        ('SUBSCRIPTION_RECEIPTS', MovementType.SUBSCRIPTION_RECEIPTS),
        ('INCORPORATION', MovementType.INCORPORATION),
        ('MERGER', MovementType.MERGER),
        ('FRACTION_TREATMENT', MovementType.FRACTION_TREATMENT),
        ('PROVISIONED_SUBSCRIPTION_RIGHTS', MovementType.PROVISIONED_SUBSCRIPTION_RIGHTS),
        ('BALANCE_UPDATE_COM', MovementType.BALANCE_UPDATE_COM),
        ('WITHDRAWAL_OF_ASSET', MovementType.WITHDRAWAL_OF_ASSET),
        ('BALANCE_UPDATE_EX', MovementType.BALANCE_UPDATE_EX),
        ('FINANCIAL_RESOURCES_TRANSFER', MovementType.FINANCIAL_RESOURCES_TRANSFER),
        ('RETURN', MovementType.RETURN),
        ('REDEMPTION', MovementType.REDEMPTION),
        ('EARNINGS', MovementType.EARNINGS),
        ('ASSET_AND_RIGHTS_TRANSFER', MovementType.ASSET_AND_RIGHTS_TRANSFER),
        ('SETTLEMENT', MovementType.SETTLEMENT),
        ('REVERSE_SPLIT', MovementType.REVERSE_SPLIT),
        ('SPIN_OFF', MovementType.SPIN_OFF),
    ],
)
def test_movement_type_accepts_exact_values(input_value: str, expected_enum: MovementType) -> None:
    assert MovementType(input_value) is expected_enum


@pytest.mark.parametrize(
    ('input_value', 'expected_enum'),
    [
        (MovementType.DEPOSIT_OF_ASSET, '1'),
        (MovementType.ISIN_CODE_UPDATE, '10'),
        (MovementType.DIVIDENDS_AND_CASH_BENEFITS, '11'),
        (MovementType.BONUS_AND_SPLIT_RIGHTS, '12'),
        (MovementType.SUBSCRIPTION_RIGHT, '13'),
        (MovementType.SUBSCRIPTION_RECEIPTS, '14'),
        (MovementType.INCORPORATION, '15'),
        (MovementType.MERGER, '16'),
        (MovementType.FRACTION_TREATMENT, '17'),
        (MovementType.PROVISIONED_SUBSCRIPTION_RIGHTS, '18'),
        (MovementType.BALANCE_UPDATE_COM, '19'),
        (MovementType.WITHDRAWAL_OF_ASSET, '2'),
        (MovementType.BALANCE_UPDATE_EX, '20'),
        (MovementType.FINANCIAL_RESOURCES_TRANSFER, '21'),
        (MovementType.RETURN, '3'),
        (MovementType.REDEMPTION, '4'),
        (MovementType.EARNINGS, '5'),
        (MovementType.ASSET_AND_RIGHTS_TRANSFER, '6'),
        (MovementType.SETTLEMENT, '7'),
        (MovementType.REVERSE_SPLIT, '8'),
        (MovementType.SPIN_OFF, '9'),
    ],
)
def test_movement_type_values_to_xml_value(input_value: MovementType, expected_enum: str) -> None:
    assert input_value.to_xml_value() == expected_enum


@pytest.mark.parametrize(
    ('input_value', 'expected_enum'),
    [
        ('1', MovementType.DEPOSIT_OF_ASSET),
        ('10', MovementType.ISIN_CODE_UPDATE),
        ('11', MovementType.DIVIDENDS_AND_CASH_BENEFITS),
        ('12', MovementType.BONUS_AND_SPLIT_RIGHTS),
        ('13', MovementType.SUBSCRIPTION_RIGHT),
        ('14', MovementType.SUBSCRIPTION_RECEIPTS),
        ('15', MovementType.INCORPORATION),
        ('16', MovementType.MERGER),
        ('17', MovementType.FRACTION_TREATMENT),
        ('18', MovementType.PROVISIONED_SUBSCRIPTION_RIGHTS),
        ('19', MovementType.BALANCE_UPDATE_COM),
        ('2', MovementType.WITHDRAWAL_OF_ASSET),
        ('20', MovementType.BALANCE_UPDATE_EX),
        ('21', MovementType.FINANCIAL_RESOURCES_TRANSFER),
        ('3', MovementType.RETURN),
        ('4', MovementType.REDEMPTION),
        ('5', MovementType.EARNINGS),
        ('6', MovementType.ASSET_AND_RIGHTS_TRANSFER),
        ('7', MovementType.SETTLEMENT),
        ('8', MovementType.REVERSE_SPLIT),
        ('9', MovementType.SPIN_OFF),
    ],
)
def test_movement_type_values_from_xml_value(input_value: str, expected_enum: MovementType) -> None:
    assert MovementType.from_xml_value(input_value) == expected_enum


@pytest.mark.parametrize(
    ('input_value', 'expected_enum'),
    [
        ('deposit_of_asset', MovementType.DEPOSIT_OF_ASSET),
        ('isin_code_update', MovementType.ISIN_CODE_UPDATE),
        ('dividends_and_cash_benefits', MovementType.DIVIDENDS_AND_CASH_BENEFITS),
        ('bonus_and_split_rights', MovementType.BONUS_AND_SPLIT_RIGHTS),
        ('subscription_right', MovementType.SUBSCRIPTION_RIGHT),
        ('subscription_receipts', MovementType.SUBSCRIPTION_RECEIPTS),
        ('incorporation', MovementType.INCORPORATION),
        ('merger', MovementType.MERGER),
        ('fraction_treatment', MovementType.FRACTION_TREATMENT),
        ('provisioned_subscription_rights', MovementType.PROVISIONED_SUBSCRIPTION_RIGHTS),
        ('balance_update_com', MovementType.BALANCE_UPDATE_COM),
        ('withdrawal_of_asset', MovementType.WITHDRAWAL_OF_ASSET),
        ('balance_update_ex', MovementType.BALANCE_UPDATE_EX),
        ('financial_resources_transfer', MovementType.FINANCIAL_RESOURCES_TRANSFER),
        ('return', MovementType.RETURN),
        ('redemption', MovementType.REDEMPTION),
        ('earnings', MovementType.EARNINGS),
        ('asset_and_rights_transfer', MovementType.ASSET_AND_RIGHTS_TRANSFER),
        ('settlement', MovementType.SETTLEMENT),
        ('reverse_split', MovementType.REVERSE_SPLIT),
        ('spin_off', MovementType.SPIN_OFF),
    ],
)
def test_movement_type_accepts_case_insensitive_values(input_value: str, expected_enum: MovementType) -> None:
    assert MovementType(input_value) is expected_enum


@pytest.mark.parametrize(
    'payment_number',
    [
        '1',  # minimum valid (1 digit, not zero)
        '9',  # single digit, upper limit
        '12',  # 2 digits
        '999',  # 3 digits
        '123456',  # mid-range
        '12345678901234567890',  # max length (20 digits)
        '98765432101234567890',  # another 20-digit value
    ],
)
def test_payment_number_accepts_valid_values(payment_number: str) -> None:
    model = PaymentNumberModel(payment_number=payment_number)
    assert model.payment_number == payment_number


@pytest.mark.parametrize(
    'payment_number',
    [
        '',  # empty string
        '12345678901234567890123',  # too long (23 digits)
    ],
)
def test_payment_number_rejects_invalid_values(payment_number: str) -> None:
    with pytest.raises(ValidationError):
        PaymentNumberModel(payment_number=payment_number)


@pytest.mark.parametrize(
    'ldl_control_number',
    [
        '1',  # minimum valid (1 digit, not zero)
        '9',  # single digit, upper limit
        '12',  # 2 digits
        '999',  # 3 digits
        '123456',  # mid-range
        '12345678901234567890',  # max length (20 digits)
        '98765432101234567890',  # another 20-digit value
    ],
)
def test_ldl_control_number_accepts_valid_values(ldl_control_number: str) -> None:
    model = LdlControlNumberModel(ldl_control_number=ldl_control_number)
    assert model.ldl_control_number == ldl_control_number


@pytest.mark.parametrize(
    'ldl_control_number',
    [
        '',  # empty string
        '12345678901234567890123',  # too long (23 digits)
    ],
)
def test_ldl_control_number_rejects_invalid_values(ldl_control_number: str) -> None:
    with pytest.raises(ValidationError):
        LdlControlNumberModel(ldl_control_number=ldl_control_number)


@pytest.mark.parametrize(
    'error_code',
    ['EGEN0050', 'ESTR0047', 'ESPB0011'],
)
def test_error_code_accepts_valid_values(error_code: str) -> None:
    model = ErrorCodeModel(error_code=error_code)
    assert model.error_code == error_code


@pytest.mark.parametrize(
    'error_code',
    ['', '12345678901234567890123', 'EGENE0000', 'ASTR0050', '123456789'],
)
def test_error_code_rejects_invalid_values(error_code: str) -> None:
    with pytest.raises(ValidationError):
        ErrorCodeModel(error_code=error_code)


@pytest.mark.parametrize(
    'protocol_number',
    ['00505500', '470047007897866977', '101000112314112'],
)
def test_sta_protocol_number_accepts_valid_values(protocol_number: str) -> None:
    model = StaProtocolNumberModel(sta_protocol_number=protocol_number)
    assert model.sta_protocol_number == protocol_number


@pytest.mark.parametrize(
    'protocol_number',
    ['', '12345678901234567890123', 'COD0980987755', '123', '0333-6678750333.667875'],
)
def test_sta_protocol_number_rejects_invalid_values(protocol_number: str) -> None:
    with pytest.raises(ValidationError):
        StaProtocolNumberModel(sta_protocol_number=protocol_number)


@pytest.mark.parametrize(
    ('input_value', 'expected_enum'),
    [
        ('COMPLEMENTARY', InformationType.COMPLEMENTARY),
        ('DEFINITIVE', InformationType.DEFINITIVE),
        ('SPECIAL', InformationType.SPECIAL),
        ('PRELIMINARY', InformationType.PRELIMINARY),
        ('RECALCULATION', InformationType.RECALCULATION),
    ],
)
def test_information_type_accepts_exact_values(input_value: str, expected_enum: InformationType) -> None:
    assert InformationType(input_value) is expected_enum


@pytest.mark.parametrize(
    ('input_value', 'expected_enum'),
    [
        (InformationType.COMPLEMENTARY, 'C'),
        (InformationType.DEFINITIVE, 'D'),
        (InformationType.SPECIAL, 'E'),
        (InformationType.PRELIMINARY, 'P'),
        (InformationType.RECALCULATION, 'R'),
    ],
)
def test_information_type_values_to_xml_value(input_value: InformationType, expected_enum: str) -> None:
    assert input_value.to_xml_value() == expected_enum


@pytest.mark.parametrize(
    ('input_value', 'expected_enum'),
    [
        ('C', InformationType.COMPLEMENTARY),
        ('D', InformationType.DEFINITIVE),
        ('E', InformationType.SPECIAL),
        ('P', InformationType.PRELIMINARY),
        ('R', InformationType.RECALCULATION),
    ],
)
def test_information_type_values_from_xml_value(input_value: str, expected_enum: InformationType) -> None:
    assert InformationType.from_xml_value(input_value) == expected_enum


@pytest.mark.parametrize(
    ('input_value', 'expected_enum'),
    [
        ('complementary', InformationType.COMPLEMENTARY),
        ('definitive', InformationType.DEFINITIVE),
        ('special', InformationType.SPECIAL),
        ('preliminary', InformationType.PRELIMINARY),
        ('recalculation', InformationType.RECALCULATION),
    ],
)
def test_information_type_accepts_case_insensitive_values(input_value: str, expected_enum: InformationType) -> None:
    assert InformationType(input_value) is expected_enum


@pytest.mark.parametrize(
    'sequence_number',
    ['0', '7', '42', '999'],
)
def test_sequence_number_accepts_valid_values(sequence_number: str) -> None:
    model = InformationSequenceNumberModel(information_sequence_number=sequence_number)
    assert model.information_sequence_number == sequence_number


@pytest.mark.parametrize(
    'sequence_number',
    [
        '',
        '1000',
        '-1',
        '12a',
        '12.2',
    ],
)
def test_sequence_number_rejects_invalid_values(sequence_number: str) -> None:
    with pytest.raises(ValidationError):
        InformationSequenceNumberModel(information_sequence_number=sequence_number)


@pytest.mark.parametrize(
    ('input_value', 'expected_enum'),
    [
        ('CONFIRM', ReconciliationType.CONFIRM),
        ('DIFFER', ReconciliationType.DIFFER),
    ],
)
def test_reconciliation_type_accepts_exact_values(input_value: str, expected_enum: ReconciliationType) -> None:
    assert ReconciliationType(input_value) is expected_enum


@pytest.mark.parametrize(
    ('input_value', 'expected_enum'),
    [
        (ReconciliationType.CONFIRM, 'C'),
        (ReconciliationType.DIFFER, 'D'),
    ],
)
def test_reconciliation_type_values_to_xml_value(input_value: ReconciliationType, expected_enum: str) -> None:
    assert input_value.to_xml_value() == expected_enum


@pytest.mark.parametrize(
    ('input_value', 'expected_enum'),
    [
        ('C', ReconciliationType.CONFIRM),
        ('D', ReconciliationType.DIFFER),
    ],
)
def test_reconciliation_type_values_from_xml_value(input_value: str, expected_enum: ReconciliationType) -> None:
    assert ReconciliationType.from_xml_value(input_value) == expected_enum


@pytest.mark.parametrize(
    ('input_value', 'expected_enum'),
    [
        ('confirm', ReconciliationType.CONFIRM),
        ('differ', ReconciliationType.DIFFER),
    ],
)
def test_reconciliation_type_accepts_case_insensitive_values(
    input_value: str, expected_enum: ReconciliationType
) -> None:
    assert ReconciliationType(input_value) is expected_enum
