from enum import Enum


class FrameworkHint(str, Enum):

    DJANGO_MODEL = "DJANGO_MODEL"

    DJANGO_QUERYSET = "DJANGO_QUERYSET"

    DJANGO_MANAGER = "DJANGO_MANAGER"

    UNKNOWN = "UNKNOWN"
