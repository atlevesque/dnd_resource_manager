from enum import Enum


class RestTypes(Enum):
    SHORT = "sr"
    LONG = "lr"
    CUSTOM = "custom"

REST_TYPE_MAPPINGS = {
    "short": RestTypes.SHORT,
    "long": RestTypes.LONG,
    "custom": RestTypes.CUSTOM,
}