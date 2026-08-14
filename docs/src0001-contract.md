# Contrato JSON — SRC0001 / SRC0001R1

Mapeamento dos campos tipados da `sfn_messages` para o payload JSON usado ao enviar/receber o evento SRC0001 (domínio `MES02`).

Catálogo: SFN Volume III v5.11 — domínio `MES02`.

## Request — `SRC0001`

Campos de envelope normalmente preenchidos pelo transporte (`from_ispb`, `to_ispb`, `system_domain`, `operation_number`, `message_code`) não precisam ir no body de negócio — ou podem ser sobrescritos conforme o cliente.

| Campo JSON | XML | Obrigatório | Notas |
| --- | --- | --- | --- |
| `institution_control_number` | `NumCtrlIF` | sim | Controle da IF |
| `responsible_entity_base_cnpj` | `CNPJBaseEntRespons` | sim | CNPJ base 8 dígitos (ISPB do emissor) |
| `institution_base_cnpj` | `CNPJBaseIF` | não | Conglomerado: IF participante |
| `document` | `CNPJ_CPF` | sim | CPF (11) ou CNPJ (14) |
| `protection_type` | `TpProtc` | sim | `ACCOUNT_OPENING` (`ACT`) ou `OWNERSHIP_CHANGE` (`ATT`) |
| `settlement_date` | `DtMovto` | sim | `YYYY-MM-DD` |

Exemplo:

```json
{
  "institution_control_number": "00001",
  "responsible_entity_base_cnpj": "12345678",
  "document": "39053344705",
  "protection_type": "ACCOUNT_OPENING",
  "settlement_date": "2026-08-11"
}
```

## Response — `SRC0001R1`

| Campo | XML | Notas |
| --- | --- | --- |
| `institution_control_number` | `NumCtrlIF` | Eco do request |
| `responsible_entity_base_cnpj` | `CNPJBaseEntRespons` | |
| `src_control_number` | `NumCtrlSRC` | Controle SRC |
| `product_permissions[]` | `Grupo_SRC0001R1_PermsProdt` | catálogo 1..n; parser aceita ausência (`[]`) |
| `product_permissions[].protection_type` | `TpProtc` | `ACCOUNT_OPENING` / `OWNERSHIP_CHANGE` |
| `product_permissions[].product_permission_indicator` | `IndrPermsProdt` | `ALLOWED` (`S`) / `NOT_ALLOWED` (`N`) |
| `vendor_timestamp` | `DtHrBC` | |
| `settlement_date` | `DtMovto` | |

Quando a resposta trouxer mais de um grupo, o consumidor escolhe o `protection_type` relevante à consulta (ex.: `ACCOUNT_OPENING`).
