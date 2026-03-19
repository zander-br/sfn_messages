from decimal import Decimal

from sfn_messages.gen.gen0006 import GEN0006E
from sfn_messages.gen.gen0019 import GEN0019E
from sfn_messages.ldl.ldl0006 import LDL0006E
from sfn_messages.str.str0008 import STR0008E
from sfn_messages.str.str0010 import STR0010E


def test_str0010e_error_mapping() -> None:
    params = {
        'from_ispb': '31680151',
        'to_ispb': '00038166',
        'system_domain': 'SPB01',
        'operation_number': '31680151250908000000001',
        'institution_control_number': '31680151202509090425',
        'original_str_control_number': 'STR20250101000000001',
        'amount': Decimal('100.00'),
        'original_str_control_number_error_code': 'ETES0165',
        'amount_error_code': 'EBMC0050',
    }
    msg = STR0010E.model_validate(params)
    error_dict = msg.to_error()

    assert error_dict['from_ispb'] == '31680151'
    assert error_dict['operation_number'] == '31680151250908000000001'
    expected_errors_count = 2
    assert len(error_dict['errors']) == expected_errors_count

    # Check first error
    error1 = next(e for e in error_dict['errors'] if e['field'] == 'original_str_control_number')
    assert error1['errorCode'] == 'ETES0165'
    assert error1['description'] == 'Número de Controle STR inexistente'
    assert error1['value'] == 'STR20250101000000001'

    # Check second error
    error2 = next(e for e in error_dict['errors'] if e['field'] == 'amount')
    assert error2['errorCode'] == 'EBMC0050'
    assert error2['description'] == 'Valor Inválido'
    assert error2['value'] == '100.00'
    assert error2['field'] == 'amount'


def test_str0010e_general_error_mapping() -> None:
    params = {
        'from_ispb': '31680151',
        'to_ispb': '00038166',
        'system_domain': 'SPB01',
        'operation_number': '31680151250908000000001',
        'general_error_code': 'EGEN0050',
    }
    msg = STR0010E.model_validate(params)
    error_dict = msg.to_error()

    assert len(error_dict['errors']) == 1
    error = error_dict['errors'][0]
    assert error['errorCode'] == 'EGEN0050'
    assert error['description'] == 'Erro de Processamento'
    assert error['field'] is None
    assert error['value'] is None


def test_str0008e_error_mapping() -> None:
    params = {
        'from_ispb': '31680151',
        'to_ispb': '00038166',
        'system_domain': 'SPB01',
        'operation_number': '31680151250908000000001',
        'general_error_code': 'EBMC0001',
    }
    msg = STR0008E.model_validate(params)
    error_dict = msg.to_error()

    assert len(error_dict['errors']) == 1
    error = error_dict['errors'][0]
    assert error['errorCode'] == 'EBMC0001'
    assert error['description'] == 'Campo Obrigatório Não Informado'
    assert error['field'] is None
    assert error['value'] is None


def test_ldl0006e_error_mapping() -> None:
    params = {
        'from_ispb': '31680151',
        'to_ispb': '00038166',
        'system_domain': 'SPB01',
        'operation_number': '31680151250908000000001',
        'amount': Decimal('100.50'),
        'amount_error_code': 'EBMC0050',
    }
    msg = LDL0006E.model_validate(params)
    error_dict = msg.to_error()

    assert len(error_dict['errors']) == 1
    error = error_dict['errors'][0]
    assert error['errorCode'] == 'EBMC0050'
    assert error['description'] == 'Valor Inválido'
    assert error['field'] == 'amount'
    assert error['value'] == '100.50'


def test_gen0006e_error_mapping() -> None:
    params = {
        'from_ispb': '31680151',
        'to_ispb': '00038166',
        'system_domain': 'SPB01',
        'operation_number': '31680151250908000000001',
        'institution_ispb': '31680151',
        'institution_ispb_error_code': 'EBMC0003',
    }
    msg = GEN0006E.model_validate(params)
    error_dict = msg.to_error()

    assert len(error_dict['errors']) == 1
    error = error_dict['errors'][0]
    assert error['errorCode'] == 'EBMC0003'
    assert error['description'] == 'ISPBIF Inválido'
    assert error['field'] == 'institution_ispb'
    assert error['value'] == '31680151'


def test_gen0019e_error_mapping() -> None:
    params = {
        'from_ispb': '31680151',
        'to_ispb': '00038166',
        'system_domain': 'SPB01',
        'operation_number': '31680151250908000000001',
        'participant_ispb': '31680151',
        'participant_ispb_error_code': 'EBMC0004',
    }
    msg = GEN0019E.model_validate(params)
    error_dict = msg.to_error()

    assert len(error_dict['errors']) == 1
    error = error_dict['errors'][0]
    assert error['errorCode'] == 'EBMC0004'
    assert error['description'] == 'ISPBIF Não Pertence ao Emissor da Mensagem'
    assert error['field'] == 'participant_ispb'
    assert error['value'] == '31680151'
