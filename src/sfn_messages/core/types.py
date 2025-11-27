from contextlib import suppress
from decimal import Decimal
from enum import Enum, StrEnum
from functools import cache
from typing import Annotated, Any, Protocol, Self, runtime_checkable
from xml.etree import ElementTree as ET

from pydantic import GetPydanticSchema
from pydantic_core import core_schema
from validate_docbr import CNPJ, CPF


def cnpj_validator(value: str) -> str:
    if not CNPJ().validate(value):
        msg = 'Invalid CNPJ format'
        raise ValueError(msg)
    return value


def cpf_validator(value: str) -> str:
    if not CPF().validate(value):
        msg = 'Invalid CPF format'
        raise ValueError(msg)
    return value


@runtime_checkable
class MappableToXmlValue(Protocol):
    def to_xml_value(self) -> str | ET.Element: ...

    @classmethod
    def from_xml_value(cls, xml_value: str | ET.Element) -> Self: ...


class EnumMixin(Enum):
    @classmethod
    def _missing_(cls, value: Any) -> Any:  # noqa: ANN401
        if isinstance(value, cls):
            return value
        with suppress(KeyError):
            return cls._value2member_map_[value]
        if isinstance(value, str):
            upper_value = value.upper()
            with suppress(KeyError):
                return cls._value2member_map_[upper_value]
            with suppress(KeyError):
                return cls._member_map_[value]
            with suppress(KeyError):
                return cls._member_map_[upper_value]
        return None

    @classmethod
    def _value_to_xml(cls) -> dict[Self, str] | None:
        return None

    @classmethod
    @cache
    def _xml_to_value(cls) -> dict[str, Self] | None:
        if value_to_xml := cls._value_to_xml():
            return {value: key for key, value in value_to_xml.items()}
        return None

    def to_xml_value(self) -> str:
        if value_to_xml := self._value_to_xml():
            return value_to_xml[self]
        return str(self)

    @classmethod
    def from_xml_value(cls, xml_value: str) -> Self:
        if xml_to_value := cls._xml_to_value():
            return cls(xml_to_value[xml_value])
        return cls(xml_value)


class AccountType(EnumMixin, StrEnum):
    CURRENT = 'CURRENT'
    DEPOSIT = 'DEPOSIT'
    OVERDRAFT = 'OVERDRAFT'
    PAYMENT = 'PAYMENT'
    SAVINGS = 'SAVINGS'

    @classmethod
    def _value_to_xml(cls) -> dict[AccountType, str] | None:
        return {
            cls.CURRENT: 'CC',
            cls.DEPOSIT: 'CD',
            cls.OVERDRAFT: 'CG',
            cls.PAYMENT: 'PG',
            cls.SAVINGS: 'PP',
        }


class PersonType(EnumMixin, StrEnum):
    BUSINESS = 'BUSINESS'
    INDIVIDUAL = 'INDIVIDUAL'

    @classmethod
    def _value_to_xml(cls) -> dict[PersonType, str]:
        return {
            cls.BUSINESS: 'J',
            cls.INDIVIDUAL: 'F',
        }


class CustomerPurpose(EnumMixin, StrEnum):
    TAX_PAYMENT = 'TAX_PAYMENT'
    CREDIT_IN_ACCOUNT = 'CREDIT_IN_ACCOUNT'
    JUDICIAL_DEPOSIT = 'JUDICIAL_DEPOSIT'
    ALIMONY = 'ALIMONY'
    CREDIT_ASSIGNMENT_CLIENT = 'CREDIT_ASSIGNMENT_CLIENT'
    CREDIT_ASSIGNMENT_FIDC = 'CREDIT_ASSIGNMENT_FIDC'
    CONTRACTUAL_CASHFLOW_CLIENT = 'CONTRACTUAL_CASHFLOW_CLIENT'
    ADVANCE_CASHFLOW_CLIENT = 'ADVANCE_CASHFLOW_CLIENT'
    CREDIT_ADJUSTMENTS = 'CREDIT_ADJUSTMENTS'
    PAYMENT_BROKERS = 'PAYMENT_BROKERS'
    TRANSFER_SAME_OWNER = 'TRANSFER_SAME_OWNER'
    CREDIT_TO_INVESTOR = 'CREDIT_TO_INVESTOR'
    DEBIT_FROM_INVESTOR = 'DEBIT_FROM_INVESTOR'
    CREDIT_OPERATIONS_CLIENT = 'CREDIT_OPERATIONS_CLIENT'
    FINANCIAL_REDEMPTION_CLIENT = 'FINANCIAL_REDEMPTION_CLIENT'
    FINANCIAL_INVESTMENT_SENDER = 'FINANCIAL_INVESTMENT_SENDER'
    PAYMENT_BANK_SLIP_REGISTRY = 'PAYMENT_BANK_SLIP_REGISTRY'
    TIR_PAYMENT_PIX = 'TIR_PAYMENT_PIX'
    CREDIT_ASSIGNMENT_REPURCHASE_CLIENT = 'CREDIT_ASSIGNMENT_REPURCHASE_CLIENT'
    CREDIT_ASSIGNMENT_REPURCHASE_FIDC = 'CREDIT_ASSIGNMENT_REPURCHASE_FIDC'
    SERVICE_FEE_PAYMENT = 'SERVICE_FEE_PAYMENT'
    FGCOOP_FUND_COLLECTION = 'FGCOOP_FUND_COLLECTION'
    FGCOOP_REFUND = 'FGCOOP_REFUND'
    FGTS_EMERGENCY_WITHDRAWAL = 'FGTS_EMERGENCY_WITHDRAWAL'
    CONSUMER_CREDIT_INCENTIVE = 'CONSUMER_CREDIT_INCENTIVE'
    REPAYMENT_REGISTRY_LIQUIDATION = 'REPAYMENT_REGISTRY_LIQUIDATION'
    EMERGENCY_AID = 'EMERGENCY_AID'
    FINANCIAL_SETTLEMENT_CARD = 'FINANCIAL_SETTLEMENT_CARD'
    BEM_EMPLOYMENT_BENEFIT = 'BEM_EMPLOYMENT_BENEFIT'
    MUNICIPAL_TAXES_ISS_LCP157 = 'MUNICIPAL_TAXES_ISS_LCP157'
    MUNICIPAL_TAXES_ISS_THIRD = 'MUNICIPAL_TAXES_ISS_THIRD'
    OPERATION_CANCELLATION = 'OPERATION_CANCELLATION'
    FINANCIAL_AGENT_FEE = 'FINANCIAL_AGENT_FEE'
    OPERATOR_SETTLEMENT_CREDITOR = 'OPERATOR_SETTLEMENT_CREDITOR'
    HOUSING_INSURANCE_SFH = 'HOUSING_INSURANCE_SFH'
    SPVAT_COLLECTION_TRANSFER = 'SPVAT_COLLECTION_TRANSFER'
    FDS_OPERATIONS = 'FDS_OPERATIONS'
    PUBLIC_SERVICE_PAYMENT = 'PUBLIC_SERVICE_PAYMENT'
    INTERNATIONAL_TRANSFER_REAIS = 'INTERNATIONAL_TRANSFER_REAIS'
    FUTURES_MARKET_ADJUSTMENT = 'FUTURES_MARKET_ADJUSTMENT'
    BNDES_VALUE_TRANSFER = 'BNDES_VALUE_TRANSFER'
    BNDES_COMMITMENT_SETTLEMENT = 'BNDES_COMMITMENT_SETTLEMENT'
    STOCK_MARKET_OPERATIONS = 'STOCK_MARKET_OPERATIONS'
    STOCK_INDEX_CONTRACTS = 'STOCK_INDEX_CONTRACTS'
    NON_INTERBANK_FOREX = 'NON_INTERBANK_FOREX'
    FIXED_VARIABLE_OPERATIONS = 'FIXED_VARIABLE_OPERATIONS'
    INTERBANK_FOREX_NO_RESERVE = 'INTERBANK_FOREX_NO_RESERVE'
    PAYMENT_FINAL_RECIPIENT = 'PAYMENT_FINAL_RECIPIENT'
    ADMINISTRATION_FEE = 'ADMINISTRATION_FEE'
    JUDICIAL_AGREEMENT_PAYMENT = 'JUDICIAL_AGREEMENT_PAYMENT'
    CONSIGNED_LOAN_SETTLEMENT = 'CONSIGNED_LOAN_SETTLEMENT'
    SCHOLARSHIP_PAYMENT = 'SCHOLARSHIP_PAYMENT'
    DIVIDEND_PAYMENT = 'DIVIDEND_PAYMENT'
    COOPERATIVE_REMUNERATION = 'COOPERATIVE_REMUNERATION'
    INCOME_TAX_REFUND = 'INCOME_TAX_REFUND'
    TREASURY_BANK_ORDER = 'TREASURY_BANK_ORDER'
    BACEN_FINES_PAYMENT = 'BACEN_FINES_PAYMENT'
    TAX_REFUND_RFB = 'TAX_REFUND_RFB'
    CLERICAL_REMUNERATION = 'CLERICAL_REMUNERATION'
    INTEREST_ON_EQUITY = 'INTEREST_ON_EQUITY'
    YIELD_AMORTIZATION = 'YIELD_AMORTIZATION'
    SERVICE_FEE = 'SERVICE_FEE'
    CHECK_PAYMENT_NON_ACCOUNT_HOLDER = 'CHECK_PAYMENT_NON_ACCOUNT_HOLDER'
    GUARANTEED_SECURITIES_INTEREST = 'GUARANTEED_SECURITIES_INTEREST'
    REVERSAL_OR_REFUND = 'REVERSAL_OR_REFUND'
    TRANSPORT_VOUCHER_PAYMENT = 'TRANSPORT_VOUCHER_PAYMENT'
    SALARY_PAYMENT = 'SALARY_PAYMENT'
    SIMPLES_NACIONAL = 'SIMPLES_NACIONAL'
    FUNDEB_TRANSFER = 'FUNDEB_TRANSFER'
    CENTRALIZED_AGREEMENT_TRANSFER = 'CENTRALIZED_AGREEMENT_TRANSFER'
    SPONSORSHIP_TAX_INCENTIVE = 'SPONSORSHIP_TAX_INCENTIVE'
    DONATION_TAX_INCENTIVE = 'DONATION_TAX_INCENTIVE'
    NONBANK_TO_LIQUIDATION_TRANSFER = 'NONBANK_TO_LIQUIDATION_TRANSFER'
    TERMINATION_PAYMENT = 'TERMINATION_PAYMENT'
    SUPPLIER_PAYMENT = 'SUPPLIER_PAYMENT'
    FIXED_VARIABLE_EXPENSE_REIMBURSEMENT = 'FIXED_VARIABLE_EXPENSE_REIMBURSEMENT'
    INSURANCE_PRIZE_REFUND = 'INSURANCE_PRIZE_REFUND'
    INSURANCE_CLAIM_PAYMENT = 'INSURANCE_CLAIM_PAYMENT'
    CO_INSURANCE_PREMIUM = 'CO_INSURANCE_PREMIUM'
    CO_INSURANCE_CLAIM_PAYMENT = 'CO_INSURANCE_CLAIM_PAYMENT'
    REINSURANCE_PREMIUM = 'REINSURANCE_PREMIUM'
    REINSURANCE_CLAIM_PAYMENT = 'REINSURANCE_CLAIM_PAYMENT'
    REINSURANCE_CLAIM_REFUND = 'REINSURANCE_CLAIM_REFUND'
    CLAIM_EXPENSE_PAYMENT = 'CLAIM_EXPENSE_PAYMENT'
    INSPECTION_PAYMENT = 'INSPECTION_PAYMENT'
    CAPITALIZATION_REDEMPTION = 'CAPITALIZATION_REDEMPTION'
    CAPITALIZATION_DRAW = 'CAPITALIZATION_DRAW'
    CAPITALIZATION_MONTHLY_REFUND = 'CAPITALIZATION_MONTHLY_REFUND'
    PENSION_CONTRIBUTION_REFUND = 'PENSION_CONTRIBUTION_REFUND'
    PENSION_PECCULUM_BENEFIT = 'PENSION_PECCULUM_BENEFIT'
    PENSION_PENSION_BENEFIT = 'PENSION_PENSION_BENEFIT'
    PENSION_RETIREMENT_BENEFIT = 'PENSION_RETIREMENT_BENEFIT'
    PENSION_REDEMPTION = 'PENSION_REDEMPTION'
    BROKERAGE_COMMISSION = 'BROKERAGE_COMMISSION'
    INSURANCE_PENSION_TRANSFER = 'INSURANCE_PENSION_TRANSFER'
    FEES_PAYMENT = 'FEES_PAYMENT'
    RENT_CONDOMINIUM = 'RENT_CONDOMINIUM'
    INVOICE_BILLS_PAYMENT = 'INVOICE_BILLS_PAYMENT'
    SCHOOL_FEE_PAYMENT = 'SCHOOL_FEE_PAYMENT'
    FOREIGN_CURRENCY_PURCHASE = 'FOREIGN_CURRENCY_PURCHASE'
    OTHERS = 'OTHERS'

    @classmethod
    def _value_to_xml(cls) -> dict[CustomerPurpose, str]:
        return {
            cls.TAX_PAYMENT: '1',
            cls.CREDIT_IN_ACCOUNT: '10',
            cls.JUDICIAL_DEPOSIT: '100',
            cls.ALIMONY: '101',
            cls.CREDIT_ASSIGNMENT_CLIENT: '103',
            cls.CREDIT_ASSIGNMENT_FIDC: '104',
            cls.CONTRACTUAL_CASHFLOW_CLIENT: '107',
            cls.ADVANCE_CASHFLOW_CLIENT: '108',
            cls.CREDIT_ADJUSTMENTS: '109',
            cls.PAYMENT_BROKERS: '11',
            cls.TRANSFER_SAME_OWNER: '110',
            cls.CREDIT_TO_INVESTOR: '111',
            cls.DEBIT_FROM_INVESTOR: '112',
            cls.CREDIT_OPERATIONS_CLIENT: '113',
            cls.FINANCIAL_REDEMPTION_CLIENT: '114',
            cls.FINANCIAL_INVESTMENT_SENDER: '117',
            cls.PAYMENT_BANK_SLIP_REGISTRY: '12',
            cls.TIR_PAYMENT_PIX: '121',
            cls.CREDIT_ASSIGNMENT_REPURCHASE_CLIENT: '123',
            cls.CREDIT_ASSIGNMENT_REPURCHASE_FIDC: '124',
            cls.SERVICE_FEE_PAYMENT: '13',
            cls.FGCOOP_FUND_COLLECTION: '131',
            cls.FGCOOP_REFUND: '132',
            cls.FGTS_EMERGENCY_WITHDRAWAL: '136',
            cls.CONSUMER_CREDIT_INCENTIVE: '139',
            cls.REPAYMENT_REGISTRY_LIQUIDATION: '14',
            cls.EMERGENCY_AID: '149',
            cls.FINANCIAL_SETTLEMENT_CARD: '15',
            cls.BEM_EMPLOYMENT_BENEFIT: '150',
            cls.MUNICIPAL_TAXES_ISS_LCP157: '157',
            cls.MUNICIPAL_TAXES_ISS_THIRD: '175',
            cls.OPERATION_CANCELLATION: '177',
            cls.FINANCIAL_AGENT_FEE: '178',
            cls.OPERATOR_SETTLEMENT_CREDITOR: '179',
            cls.HOUSING_INSURANCE_SFH: '18',
            cls.SPVAT_COLLECTION_TRANSFER: '180',
            cls.FDS_OPERATIONS: '19',
            cls.PUBLIC_SERVICE_PAYMENT: '2',
            cls.INTERNATIONAL_TRANSFER_REAIS: '200',
            cls.FUTURES_MARKET_ADJUSTMENT: '201',
            cls.BNDES_VALUE_TRANSFER: '202',
            cls.BNDES_COMMITMENT_SETTLEMENT: '203',
            cls.STOCK_MARKET_OPERATIONS: '204',
            cls.STOCK_INDEX_CONTRACTS: '205',
            cls.NON_INTERBANK_FOREX: '206',
            cls.FIXED_VARIABLE_OPERATIONS: '207',
            cls.INTERBANK_FOREX_NO_RESERVE: '208',
            cls.PAYMENT_FINAL_RECIPIENT: '209',
            cls.ADMINISTRATION_FEE: '23',
            cls.JUDICIAL_AGREEMENT_PAYMENT: '27',
            cls.CONSIGNED_LOAN_SETTLEMENT: '28',
            cls.SCHOLARSHIP_PAYMENT: '29',
            cls.DIVIDEND_PAYMENT: '3',
            cls.COOPERATIVE_REMUNERATION: '30',
            cls.INCOME_TAX_REFUND: '300',
            cls.TREASURY_BANK_ORDER: '301',
            cls.BACEN_FINES_PAYMENT: '302',
            cls.TAX_REFUND_RFB: '303',
            cls.CLERICAL_REMUNERATION: '31',
            cls.INTEREST_ON_EQUITY: '33',
            cls.YIELD_AMORTIZATION: '34',
            cls.SERVICE_FEE: '35',
            cls.CHECK_PAYMENT_NON_ACCOUNT_HOLDER: '36',
            cls.GUARANTEED_SECURITIES_INTEREST: '37',
            cls.REVERSAL_OR_REFUND: '38',
            cls.TRANSPORT_VOUCHER_PAYMENT: '39',
            cls.SALARY_PAYMENT: '4',
            cls.SIMPLES_NACIONAL: '40',
            cls.FUNDEB_TRANSFER: '41',
            cls.CENTRALIZED_AGREEMENT_TRANSFER: '42',
            cls.SPONSORSHIP_TAX_INCENTIVE: '43',
            cls.DONATION_TAX_INCENTIVE: '44',
            cls.NONBANK_TO_LIQUIDATION_TRANSFER: '45',
            cls.TERMINATION_PAYMENT: '47',
            cls.SUPPLIER_PAYMENT: '5',
            cls.FIXED_VARIABLE_EXPENSE_REIMBURSEMENT: '50',
            cls.INSURANCE_PRIZE_REFUND: '500',
            cls.INSURANCE_CLAIM_PAYMENT: '501',
            cls.CO_INSURANCE_PREMIUM: '502',
            cls.CO_INSURANCE_CLAIM_PAYMENT: '504',
            cls.REINSURANCE_PREMIUM: '505',
            cls.REINSURANCE_CLAIM_PAYMENT: '507',
            cls.REINSURANCE_CLAIM_REFUND: '508',
            cls.CLAIM_EXPENSE_PAYMENT: '509',
            cls.INSPECTION_PAYMENT: '510',
            cls.CAPITALIZATION_REDEMPTION: '511',
            cls.CAPITALIZATION_DRAW: '512',
            cls.CAPITALIZATION_MONTHLY_REFUND: '513',
            cls.PENSION_CONTRIBUTION_REFUND: '514',
            cls.PENSION_PECCULUM_BENEFIT: '515',
            cls.PENSION_PENSION_BENEFIT: '516',
            cls.PENSION_RETIREMENT_BENEFIT: '517',
            cls.PENSION_REDEMPTION: '518',
            cls.BROKERAGE_COMMISSION: '519',
            cls.INSURANCE_PENSION_TRANSFER: '520',
            cls.FEES_PAYMENT: '6',
            cls.RENT_CONDOMINIUM: '7',
            cls.INVOICE_BILLS_PAYMENT: '8',
            cls.SCHOOL_FEE_PAYMENT: '9',
            cls.FOREIGN_CURRENCY_PURCHASE: '97',
            cls.OTHERS: '99999',
        }


class SystemDomain(EnumMixin, StrEnum):
    SPB01 = 'SPB01'
    SPB02 = 'SPB02'
    MES01 = 'MES01'
    MES02 = 'MES02'
    MES03 = 'MES03'


class Priority(EnumMixin, StrEnum):
    HIGH = 'HIGH'
    HIGHEST = 'HIGHEST'
    LOW = 'LOW'
    MEDIUM = 'MEDIUM'

    @classmethod
    def _value_to_xml(cls) -> dict[Priority, str]:
        return {
            cls.HIGH: 'B',
            cls.HIGHEST: 'A',
            cls.LOW: 'D',
            cls.MEDIUM: 'C',
        }


class StrSettlementStatus(EnumMixin, StrEnum):
    CANCELED = 'CANCELED'
    CANCELED_CONTINGENCY = 'CANCELED_CONTINGENCY'
    EFFECTIVE = 'EFFECTIVE'
    EFFECTIVE_CONTINGENCY = 'EFFECTIVE_CONTINGENCY'
    EFFECTIVE_OPTIMIZATION = 'EFFECTIVE_OPTIMIZATION'
    EFFECTIVE_SCHEDULED = 'EFFECTIVE_SCHEDULED'
    PENDING_INSUFFICIENT_FUNDS = 'PENDING_INSUFFICIENT_FUNDS'
    PENDING_INSUFFICIENT_FUNDS_CONTINGENCY = 'PENDING_INSUFFICIENT_FUNDS_CONTINGENCY'
    PENDING_INSUFFICIENT_FUNDS_REJECTED_AFTER_DEADLINE = 'PENDING_INSUFFICIENT_FUNDS_REJECTED_AFTER_DEADLINE'
    PENDING_INSUFFICIENT_FUNDS_REJECTED_AFTER_DEADLINE_CONTINGENCY = (
        'PENDING_INSUFFICIENT_FUNDS_REJECTED_AFTER_DEADLINE_CONTINGENCY'
    )
    PENDING_REJECTED_EXCLUSION_SUSPENSION = 'PENDING_REJECTED_EXCLUSION_SUSPENSION'
    PENDING_REJECTED_EXCLUSION_SUSPENSION_CONTINGENCY = 'PENDING_REJECTED_EXCLUSION_SUSPENSION_CONTINGENCY'
    PENDING_SCHEDULED = 'PENDING_SCHEDULED'
    PENDING_SCHEDULED_CONTINGENCY = 'PENDING_SCHEDULED_CONTINGENCY'
    REJECTED_INSUFFICIENT_FUNDS_CONTINGENCY = 'REJECTED_INSUFFICIENT_FUNDS_CONTINGENCY'
    REJECTED_NO_FUNDS = 'REJECTED_NO_FUNDS'

    @classmethod
    def _value_to_xml(cls) -> dict[StrSettlementStatus, str]:
        return {
            cls.CANCELED: '14',
            cls.CANCELED_CONTINGENCY: '15',
            cls.EFFECTIVE: '1',
            cls.EFFECTIVE_CONTINGENCY: '2',
            cls.EFFECTIVE_OPTIMIZATION: '3',
            cls.EFFECTIVE_SCHEDULED: '4',
            cls.PENDING_INSUFFICIENT_FUNDS: '17',
            cls.PENDING_INSUFFICIENT_FUNDS_CONTINGENCY: '19',
            cls.PENDING_INSUFFICIENT_FUNDS_REJECTED_AFTER_DEADLINE: '24',
            cls.PENDING_INSUFFICIENT_FUNDS_REJECTED_AFTER_DEADLINE_CONTINGENCY: '25',
            cls.PENDING_REJECTED_EXCLUSION_SUSPENSION: '22',
            cls.PENDING_REJECTED_EXCLUSION_SUSPENSION_CONTINGENCY: '23',
            cls.PENDING_SCHEDULED: '18',
            cls.PENDING_SCHEDULED_CONTINGENCY: '20',
            cls.REJECTED_INSUFFICIENT_FUNDS_CONTINGENCY: '9',
            cls.REJECTED_NO_FUNDS: '5',
        }


class TransferReturnReason(EnumMixin, StrEnum):
    DESTINATION_ACCOUNT_CLOSED = 'DESTINATION_ACCOUNT_CLOSED'
    INVALID_JUDICIAL_DEPOSIT_ID = 'INVALID_JUDICIAL_DEPOSIT_ID'
    OUT_OF_BUSINESS_HOURS = 'OUT_OF_BUSINESS_HOURS'
    INVALID_CONTRACT_NUMBER = 'INVALID_CONTRACT_NUMBER'
    DUPLICATE_VALUE = 'DUPLICATE_VALUE'
    TERRORISM_FINANCING_ACTIVITY = 'TERRORISM_FINANCING_ACTIVITY'
    INVALID_DESTINATION_AGENCY_OR_ACCOUNT = 'INVALID_DESTINATION_AGENCY_OR_ACCOUNT'
    FGTS_DOCUMENT_NOT_PRESENTED = 'FGTS_DOCUMENT_NOT_PRESENTED'
    TREASURY_PAYMENT_RETURN = 'TREASURY_PAYMENT_RETURN'
    TREASURY_BANK_ORDER_RETURN = 'TREASURY_BANK_ORDER_RETURN'
    RETURN_FILLING_ERROR = 'RETURN_FILLING_ERROR'
    WITHHOLDING_DOCUMENT_FILLING_ERROR = 'WITHHOLDING_DOCUMENT_FILLING_ERROR'
    DIRECT_DEPOSIT_FILLING_ERROR = 'DIRECT_DEPOSIT_FILLING_ERROR'
    TAX_PAYMENT_RETURN_AT_BANK_REQUEST = 'TAX_PAYMENT_RETURN_AT_BANK_REQUEST'
    OVERPAID_TAX_RETURN_AUTHORIZED_BY_RFB = 'OVERPAID_TAX_RETURN_AUTHORIZED_BY_RFB'
    UNWITHDRAWN_CREDIT_EXPIRED = 'UNWITHDRAWN_CREDIT_EXPIRED'
    MISSING_OR_MISMATCHED_TAX_ID = 'MISSING_OR_MISMATCHED_TAX_ID'
    INAPT_TAX_ID_AT_RFB = 'INAPT_TAX_ID_AT_RFB'
    INVALID_MESSAGE_FOR_TRANSACTION_TYPE = 'INVALID_MESSAGE_FOR_TRANSACTION_TYPE'
    INVALID_CURRENCY_CODE_BARCODE = 'INVALID_CURRENCY_CODE_BARCODE'
    TITLE_MISMATCH = 'TITLE_MISMATCH'
    OVER_OR_UNDERPAID_BARCODE_BOLETO = 'OVER_OR_UNDERPAID_BARCODE_BOLETO'
    LATE_BARCODE_BOLETO_WITHOUT_CHARGES = 'LATE_BARCODE_BOLETO_WITHOUT_CHARGES'
    IMPROPER_PRESENTATION_BARCODE = 'IMPROPER_PRESENTATION_BARCODE'
    INSUFFICIENT_AMOUNT_FOR_PURPOSE = 'INSUFFICIENT_AMOUNT_FOR_PURPOSE'
    TRANSFER_ABOVE_DESTINATION_ACCOUNT_LIMIT = 'TRANSFER_ABOVE_DESTINATION_ACCOUNT_LIMIT'
    BARCODE_NOT_COMPLIANT_WITH_SPECS = 'BARCODE_NOT_COMPLIANT_WITH_SPECS'
    BOLETO_ALREADY_PAID = 'BOLETO_ALREADY_PAID'
    BOLETO_DUPLICATE_PAYMENT_SAME_DAY = 'BOLETO_DUPLICATE_PAYMENT_SAME_DAY'
    OVERPAYMENT_DIFFERENCE = 'OVERPAYMENT_DIFFERENCE'
    CUSTOMER_REQUEST_RETURN = 'CUSTOMER_REQUEST_RETURN'
    BARCODE_BOLETO_UNPLANNED_DISCOUNT = 'BARCODE_BOLETO_UNPLANNED_DISCOUNT'
    NON_COMPLIANT_PAYMENT = 'NON_COMPLIANT_PAYMENT'
    BENEFICIARY_NOT_IDENTIFIED_BARCODE = 'BENEFICIARY_NOT_IDENTIFIED_BARCODE'
    INVALID_OR_MISMATCHED_BENEFICIARY_TAX_ID = 'INVALID_OR_MISMATCHED_BENEFICIARY_TAX_ID'
    INVALID_OR_MISMATCHED_PAYER_TAX_ID = 'INVALID_OR_MISMATCHED_PAYER_TAX_ID'
    COPY_NOT_SENT_BY_RECEIVING_BANK = 'COPY_NOT_SENT_BY_RECEIVING_BANK'
    BOLETO_IN_COLLECTION_OR_PROTEST = 'BOLETO_IN_COLLECTION_OR_PROTEST'
    INVALID_TRANSFER_IDENTIFIER = 'INVALID_TRANSFER_IDENTIFIER'
    PORTABILITY_NOT_REGISTERED_CREDIT_CENTER = 'PORTABILITY_NOT_REGISTERED_CREDIT_CENTER'
    BARCODE_BOLETO_DIVERGENT_FROM_CENTRAL_BASE = 'BARCODE_BOLETO_DIVERGENT_FROM_CENTRAL_BASE'
    BARCODE_BOLETO_NOT_FOUND_IN_CENTRAL_BASE = 'BARCODE_BOLETO_NOT_FOUND_IN_CENTRAL_BASE'
    INVALID_DESTINATION_ACCOUNT_FOR_TYPE_OR_PURPOSE = 'INVALID_DESTINATION_ACCOUNT_FOR_TYPE_OR_PURPOSE'
    OPEN_FINANCE_PORTABILITY_NOT_COMPLETED = 'OPEN_FINANCE_PORTABILITY_NOT_COMPLETED'
    FRAUD_RETURN = 'FRAUD_RETURN'

    @classmethod
    def _value_to_xml(cls) -> dict[TransferReturnReason, str]:
        return {
            cls.DESTINATION_ACCOUNT_CLOSED: '1',
            cls.INVALID_JUDICIAL_DEPOSIT_ID: '15',
            cls.OUT_OF_BUSINESS_HOURS: '16',
            cls.INVALID_CONTRACT_NUMBER: '17',
            cls.DUPLICATE_VALUE: '18',
            cls.TERRORISM_FINANCING_ACTIVITY: '19',
            cls.INVALID_DESTINATION_AGENCY_OR_ACCOUNT: '2',
            cls.FGTS_DOCUMENT_NOT_PRESENTED: '20',
            cls.TREASURY_PAYMENT_RETURN: '21',
            cls.TREASURY_BANK_ORDER_RETURN: '22',
            cls.RETURN_FILLING_ERROR: '23',
            cls.WITHHOLDING_DOCUMENT_FILLING_ERROR: '24',
            cls.DIRECT_DEPOSIT_FILLING_ERROR: '25',
            cls.TAX_PAYMENT_RETURN_AT_BANK_REQUEST: '26',
            cls.OVERPAID_TAX_RETURN_AUTHORIZED_BY_RFB: '27',
            cls.UNWITHDRAWN_CREDIT_EXPIRED: '28',
            cls.MISSING_OR_MISMATCHED_TAX_ID: '3',
            cls.INAPT_TAX_ID_AT_RFB: '31',
            cls.INVALID_MESSAGE_FOR_TRANSACTION_TYPE: '4',
            cls.INVALID_CURRENCY_CODE_BARCODE: '40',
            cls.TITLE_MISMATCH: '5',
            cls.OVER_OR_UNDERPAID_BARCODE_BOLETO: '51',
            cls.LATE_BARCODE_BOLETO_WITHOUT_CHARGES: '52',
            cls.IMPROPER_PRESENTATION_BARCODE: '53',
            cls.INSUFFICIENT_AMOUNT_FOR_PURPOSE: '6',
            cls.TRANSFER_ABOVE_DESTINATION_ACCOUNT_LIMIT: '61',
            cls.BARCODE_NOT_COMPLIANT_WITH_SPECS: '63',
            cls.BOLETO_ALREADY_PAID: '68',
            cls.BOLETO_DUPLICATE_PAYMENT_SAME_DAY: '69',
            cls.OVERPAYMENT_DIFFERENCE: '7',
            cls.CUSTOMER_REQUEST_RETURN: '70',
            cls.BARCODE_BOLETO_UNPLANNED_DISCOUNT: '71',
            cls.NON_COMPLIANT_PAYMENT: '72',
            cls.BENEFICIARY_NOT_IDENTIFIED_BARCODE: '73',
            cls.INVALID_OR_MISMATCHED_BENEFICIARY_TAX_ID: '74',
            cls.INVALID_OR_MISMATCHED_PAYER_TAX_ID: '75',
            cls.COPY_NOT_SENT_BY_RECEIVING_BANK: '76',
            cls.BOLETO_IN_COLLECTION_OR_PROTEST: '77',
            cls.INVALID_TRANSFER_IDENTIFIER: '8',
            cls.PORTABILITY_NOT_REGISTERED_CREDIT_CENTER: '80',
            cls.BARCODE_BOLETO_DIVERGENT_FROM_CENTRAL_BASE: '82',
            cls.BARCODE_BOLETO_NOT_FOUND_IN_CENTRAL_BASE: '83',
            cls.INVALID_DESTINATION_ACCOUNT_FOR_TYPE_OR_PURPOSE: '84',
            cls.OPEN_FINANCE_PORTABILITY_NOT_COMPLETED: '85',
            cls.FRAUD_RETURN: '9',
        }


type AccountNumber = Annotated[
    str,
    GetPydanticSchema(
        lambda _tp, _handler: core_schema.str_schema(
            pattern=r'^[1-9][0-9]{0,12}$',
            strip_whitespace=True,
        )
    ),
]

type Branch = Annotated[
    str,
    GetPydanticSchema(
        lambda _tp, _handler: core_schema.str_schema(
            pattern=r'^[0-9]{1,4}$',
            strip_whitespace=True,
        )
    ),
]

type Description = Annotated[
    str,
    GetPydanticSchema(
        lambda _tp, _handler: core_schema.str_schema(
            max_length=200,
            strip_whitespace=True,
        )
    ),
]

type Name = Annotated[
    str,
    GetPydanticSchema(
        lambda _tp, _handler: core_schema.str_schema(
            max_length=80,
            strip_whitespace=True,
        )
    ),
]


type InstitutionControlNumber = Annotated[
    str,
    GetPydanticSchema(
        lambda _tp, _handler: core_schema.str_schema(min_length=1, max_length=20, strip_whitespace=True)
    ),
]

type Ispb = Annotated[
    str,
    GetPydanticSchema(
        lambda _tp, _handler: core_schema.str_schema(
            pattern=r'^[0-9A-Za-z]{8}$',
            strip_whitespace=True,
            to_upper=True,
        )
    ),
]

type OperationNumber = Annotated[
    str,
    GetPydanticSchema(
        lambda _tp, _handler: core_schema.str_schema(
            pattern=r'^[0-9A-Z]{8}[0-9]{13}$',
            strip_whitespace=True,
            to_upper=True,
        )
    ),
]

type Cnpj = Annotated[
    str,
    GetPydanticSchema(
        lambda _tp, _handler: core_schema.no_info_after_validator_function(
            cnpj_validator,
            core_schema.str_schema(
                pattern=r'^[0-9A-Z]{12}[0-9]{2}$',
                strip_whitespace=True,
            ),
        )
    ),
]

type Cpf = Annotated[
    str,
    GetPydanticSchema(
        lambda _tp, _handler: core_schema.no_info_after_validator_function(
            cpf_validator,
            core_schema.str_schema(
                pattern=r'^[0-9]{11}$',
                strip_whitespace=True,
            ),
        )
    ),
]

type TransactionId = Annotated[
    str,
    GetPydanticSchema(
        lambda _tp, _handler: core_schema.str_schema(min_length=1, max_length=25, strip_whitespace=True)
    ),
]

type StrControlNumber = Annotated[
    str,
    GetPydanticSchema(
        lambda _tp, _handler: core_schema.str_schema(
            pattern=r'^STR\d{4}(0[1-9]|1[0-2])(0[1-9]|[12]\d|3[01])\d{9}$',
            strip_whitespace=True,
            to_upper=True,
        )
    ),
]

type CreditContractNumber = Annotated[
    str,
    GetPydanticSchema(
        lambda _tp, _handler: core_schema.str_schema(
            max_length=40,
            strip_whitespace=True,
            pattern=r'^[A-Za-z0-9]+$',
        )
    ),
]

type Amount = Annotated[
    Decimal,
    GetPydanticSchema(
        lambda _tp, _handler: core_schema.decimal_schema(
            max_digits=19,
            decimal_places=2,
            gt=Decimal('-1e17'),
            lt=Decimal('1e17'),
        )
    ),
]


type FileIdentifier = Annotated[
    str,
    GetPydanticSchema(
        lambda _tp, _handler: core_schema.str_schema(min_length=1, max_length=255, strip_whitespace=True)
    ),
]

type DepositIdentifier = Annotated[
    str,
    GetPydanticSchema(
        lambda _tp, _handler: core_schema.str_schema(
            min_length=18,
            max_length=18,
            strip_whitespace=True,
            pattern=r'^[01][0-9]{17}$',
        )
    ),
]
