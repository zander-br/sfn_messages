from contextlib import suppress
from enum import Enum, StrEnum
from typing import Annotated, Any

from pydantic import GetPydanticSchema
from pydantic_core import core_schema


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


class SystemDomain(EnumMixin, StrEnum):
    SPB01 = 'SPB01'
    SPB02 = 'SPB02'
    MES01 = 'MES01'
    MES02 = 'MES02'
    MES03 = 'MES03'


type Description = Annotated[
    str,
    GetPydanticSchema(
        lambda _tp, _handler: core_schema.str_schema(
            max_length=200,
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
