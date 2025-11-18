# SFN Messages

```python
from sfn_messages import from_xml, to_xml

data = {
    'from_ispb': '31680151',
    'to_ispb': '00038166',
    'internal_ispb': '31680151',
    'system_domain': 'spb01',
    'operation_number': '316801512509080000001',
    'internal_control_number': '123',
    'provider_control_number': 'ABC123',
    'certificate_issue': 'serpro',
    'certificate_serial_number': '12345678901234567890123456789000',
    'settlement_date': '2025-11-08'
}

xml = to_xml(data, message_code='GEN0006')
print(xml)

gen0006 = from_xml(xml)
print(gen0006)
```
