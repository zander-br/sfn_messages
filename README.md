# SFN Messages

```python
from sfn_messages.core import from_xml, to_xml

data = {
    'from_ispb': '31680151',
    'to_ispb': '00038166',
    'institution_ispb': '31680151',
    'system_domain': 'spb01',
    'operation_number': '316801512509080000001',
    'institution_control_number': '123',
    'provider_control_number': 'ABC123',
    'certificate_issue': 'serpro',
    'certificate_serial_number': '12345678901234567890123456789000',
    'settlement_date': '2025-11-08'
}

xml = to_xml('GEN0006', data)
print(xml)

gen0006 = from_xml(xml)
print('%r' % gen0006)
```
