from enum import Enum


class DispatchType(str, Enum):

    DIRECT = "DIRECT"

    SELF = "SELF"

    SUPER = "SUPER"

    CLASSMETHOD = "CLASSMETHOD"

    STATICMETHOD = "STATICMETHOD"

    DYNAMIC = "DYNAMIC"

    MODULE_FUNCTION = "MODULE_FUNCTION"

    EXTERNAL = "EXTERNAL"
