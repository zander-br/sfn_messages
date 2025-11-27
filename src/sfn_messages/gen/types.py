from enum import StrEnum
from typing import Annotated

from pydantic import GetPydanticSchema
from pydantic_core import core_schema

from sfn_messages.core.types import EnumMixin


class CertificateIssue(EnumMixin, StrEnum):
    SERPRO = 'SERPRO'
    CERTISIGN = 'CERTISIGN'
    SERASA = 'SERASA'
    AC_CAIXA = 'AC_CAIXA'
    AC_VALIDA = 'AC_VALIDA'
    AC_SOLUTI = 'AC_SOLUTI'

    @classmethod
    def _value_to_xml(cls) -> dict[CertificateIssue, str]:
        return {
            cls.SERPRO: '1',
            cls.CERTISIGN: '2',
            cls.SERASA: '4',
            cls.AC_CAIXA: '5',
            cls.AC_VALIDA: '6',
            cls.AC_SOLUTI: '7',
        }


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


type Message = Annotated[
    str,
    GetPydanticSchema(
        lambda _tp, _handler: core_schema.str_schema(
            max_length=50,
            strip_whitespace=True,
        )
    ),
]


type LastOperationNumber = Annotated[
    str,
    GetPydanticSchema(
        lambda _tp, _handler: core_schema.str_schema(
            pattern=r'^[0-9A-Z]{8}[0-9]{15}$',
            strip_whitespace=True,
            to_upper=True,
        )
    ),
]


type TransmissionType = Annotated[
    str,
    GetPydanticSchema(
        lambda _tp, _handler: core_schema.str_schema(
            min_length=1,
            max_length=1,
            strip_whitespace=True,
        )
    ),
]


type SelectionCriteria = Annotated[
    str,
    GetPydanticSchema(
        lambda _tp, _handler: core_schema.str_schema(min_length=0, max_length=10240, strip_whitespace=True)
    ),
]
