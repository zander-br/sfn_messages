from typing import Annotated

from pydantic import GetPydanticSchema
from pydantic_core import core_schema

type SmeControlNumber = Annotated[
    str,
    GetPydanticSchema(
        lambda _tp, _handler: core_schema.str_schema(
            pattern=r'^SME\d{4}(0[1-9]|1[0-2])(0[1-9]|[12]\d|3[01])\d{9}$',
            strip_whitespace=True,
            to_upper=True,
        )
    ),
]
