from enum import IntEnum
from typing import Annotated

from pydantic import GetPydanticSchema
from pydantic_core import core_schema

from sfn_messages.core.types import EnumMixin


class CertificateIssue(EnumMixin, IntEnum):
    SERPRO = 1
    CERTISIGN = 2
    SERASA = 4
    AC_CAIXA = 5
    AC_VALIDA = 6
    AC_SOLUTI = 7


type CertificateSerialNumber = Annotated[
    str,
    GetPydanticSchema(
        lambda _tp, _handler: core_schema.str_schema(
            pattern=r'^[0-9A-Fa-f]{32}$',
            strip_whitespace=True,
            to_upper=True,
        )
    ),
]
