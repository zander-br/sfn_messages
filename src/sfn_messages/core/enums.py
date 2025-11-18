from contextlib import suppress
from enum import Enum
from typing import Any


class EnumMixin(Enum):
    @classmethod
    def _missing_(cls, value: Any) -> Any:  # noqa: ANN401
        if isinstance(value, cls):
            return value

        if isinstance(value, str):
            v = value.strip().upper()

            if v in cls.__members__:
                return cls.__members__[v]

            if v.isdigit():
                with suppress(ValueError):
                    return cls(int(v))

        return None


class SystemDomain(EnumMixin):
    SPB01 = 'SPB01'
    SPB02 = 'SPB02'
    MES01 = 'MES01'
    MES02 = 'MES02'
    MES03 = 'MES03'
