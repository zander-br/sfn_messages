from enum import StrEnum

from sfn_messages.core.types import EnumMixin


class LtrOperationType(EnumMixin, StrEnum):
    NORMAL = 'NORMAL'
    COAST = 'COAST'
    ASSOCIATED = 'ASSOCIATED'
    EVENT_ASSOCIATION = 'EVENT_ASSOCIATION'

    @classmethod
    def _value_to_xml(cls) -> dict[LtrOperationType, str]:
        return {cls.NORMAL: '0', cls.COAST: '1', cls.ASSOCIATED: '2', cls.EVENT_ASSOCIATION: '3'}
