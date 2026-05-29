# pipeline_v2/core/identity/identity_mode.py

from enum import Enum


class IdentityMode(str, Enum):
    STRICT = "STRICT"
    INFERRED = "INFERRED"
    EXTERNAL = "EXTERNAL"
