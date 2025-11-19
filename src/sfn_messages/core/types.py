from contextlib import suppress
from enum import Enum, IntEnum, StrEnum
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


class CertificateIssue(EnumMixin, IntEnum):
    SERPRO = 1
    CERTISIGN = 2
    SERASA = 4
    AC_CAIXA = 5
    AC_VALIDA = 6
    AC_SOLUTI = 7


class SystemDomain(EnumMixin, StrEnum):
    SPB01 = 'SPB01'
    SPB02 = 'SPB02'
    MES01 = 'MES01'
    MES02 = 'MES02'
    MES03 = 'MES03'


type Ispb = Annotated[
    str,
    GetPydanticSchema(
        lambda _tp, _handler: core_schema.str_schema(
            pattern=r'^[0-9A-Za-z]{8}$',
            min_length=8,
            max_length=8,
            strip_whitespace=True,
            to_upper=True,
        )
    ),
]
