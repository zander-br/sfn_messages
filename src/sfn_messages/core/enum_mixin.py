from enum import Enum
from typing import Any


class EnumMixin(Enum):
    @classmethod
    def _missing_(cls, value: Any) -> Any:
        if isinstance(value, cls):
            return value

        if isinstance(value, str):
            v = value.strip().upper()

            if v in cls.__members__:
                return cls.__members__[v]

            if v.isdigit():
                try:
                    return cls(int(v))
                except ValueError:
                    pass

        return None
