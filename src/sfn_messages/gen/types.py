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


class TransmissionType(EnumMixin, StrEnum):
    EXTERNAL_AND_USERMSG_ATTACHED = 'EXTERNAL_AND_USERMSG_ATTACHED'
    EXTERNAL = 'EXTERNAL'
    USERMSG_ATTACHED = 'USERMSG_ATTACHED'

    @classmethod
    def _value_to_xml(cls) -> dict[TransmissionType, str]:
        return {
            cls.EXTERNAL_AND_USERMSG_ATTACHED: 'A',
            cls.EXTERNAL: 'E',
            cls.USERMSG_ATTACHED: 'U',
        }


type SelectionCriteria = Annotated[
    str,
    GetPydanticSchema(
        lambda _tp, _handler: core_schema.str_schema(min_length=0, max_length=10240, strip_whitespace=True)
    ),
]


type Certificate = Annotated[
    str,
    GetPydanticSchema(
        lambda _tp, _handler: core_schema.str_schema(min_length=0, max_length=10240, strip_whitespace=True)
    ),
]


type IndividualIdentificationNumber = Annotated[
    str,
    GetPydanticSchema(
        lambda _tp, _handler: core_schema.str_schema(min_length=1, max_length=20, strip_whitespace=True)
    ),
]


class ResponsibleType(EnumMixin, StrEnum):
    CONTINGENCY_STR = 'CONTINGENCY_STR'
    SPB_DIRECTOR = 'SPB_DIRECTOR'
    INFRASTRUCTURE = 'INFRASTRUCTURE'
    MONITOR = 'MONITOR'
    HOLDER = 'HOLDER'
    ISSUER = 'ISSUER'

    @classmethod
    def _value_to_xml(cls) -> dict[ResponsibleType, str]:
        return {
            cls.CONTINGENCY_STR: 'C',
            cls.SPB_DIRECTOR: 'D',
            cls.INFRASTRUCTURE: 'I',
            cls.MONITOR: 'M',
            cls.HOLDER: 'PD',
            cls.ISSUER: 'PE',
        }


type MqMessageNumber = Annotated[
    str,
    GetPydanticSchema(
        lambda _tp, _handler: core_schema.str_schema(
            pattern=r'^[0-9A-F]{24}$',
            min_length=24,
            max_length=24,
            strip_whitespace=True,
            to_upper=True,
        )
    ),
]
