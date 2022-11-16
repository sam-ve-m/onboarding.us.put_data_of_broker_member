# STANDARD IMPORTS
from enum import IntEnum


class InternalCode(IntEnum):
    SUCCESS = 0
    JWT_INVALID = 30
    INTERNAL_SERVER_ERROR = 100
    NOT_SENT_TO_PERSEPHONE = 60
    INVALID_PARAMS = 10
    TRANSPORT_LAYER_ERROR = 69
    UNIQUE_ID_WAS_NOT_UPDATED = 88
    USER_WAS_NOT_FOUND = 99

    def __repr__(self):
        return self.value
