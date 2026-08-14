from enum import StrEnum
from typing import Annotated, Self

from pydantic import GetPydanticSchema
from pydantic_core import core_schema

from sfn_messages.core.types import EnumMixin

type SrcControlNumber = Annotated[
    str,
    GetPydanticSchema(
        lambda _tp, _handler: core_schema.str_schema(
            min_length=1,
            max_length=20,
            strip_whitespace=True,
        )
    ),
]


class ProtectionType(EnumMixin, StrEnum):
    """Tipo de proteção (TpProtc) do grupo de serviços SRC."""

    ACCOUNT_OPENING = 'ACCOUNT_OPENING'
    OWNERSHIP_CHANGE = 'OWNERSHIP_CHANGE'

    @classmethod
    def _value_to_xml(cls) -> dict[Self, str]:
        return {
            cls.ACCOUNT_OPENING: 'ACT',
            cls.OWNERSHIP_CHANGE: 'ATT',
        }


class ProductPermissionIndicator(EnumMixin, StrEnum):
    """Indicador de permissão de produto (IndrPermsProdt)."""

    ALLOWED = 'ALLOWED'
    NOT_ALLOWED = 'NOT_ALLOWED'

    @classmethod
    def _value_to_xml(cls) -> dict[Self, str]:
        return {
            cls.ALLOWED: 'S',
            cls.NOT_ALLOWED: 'N',
        }
