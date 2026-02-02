from enum import StrEnum

from sfn_messages.core.types import EnumMixin


class LpiPurpose(EnumMixin, StrEnum):
    OWN_MOVEMENT_OR_TO_SETTLER_ACCOUNT_ON_STR = 'OWN_MOVEMENT_OR_TO_SETTLER_ACCOUNT_ON_STR'
    RETURN_OF_IMPROPERLY_RECEIVED_CONTRIBUTION = 'RETURN_OF_IMPROPERLY_RECEIVED_CONTRIBUTION'

    @classmethod
    def _value_to_xml(cls) -> dict[LpiPurpose, str]:
        return {
            cls.OWN_MOVEMENT_OR_TO_SETTLER_ACCOUNT_ON_STR: '1',
            cls.RETURN_OF_IMPROPERLY_RECEIVED_CONTRIBUTION: '2',
        }
