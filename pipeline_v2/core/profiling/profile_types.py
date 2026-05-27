# pipeline_v2/core/profiling/profile_types.py

from enum import Enum


class LanguageFamily(str, Enum):

    PYTHON = "python"
    JAVASCRIPT = "javascript"
    JVM = "jvm"
    DOTNET = "dotnet"
    NATIVE = "native"
    DATA = "data"
    CONFIG = "config"
    UNKNOWN = "unknown"


class FrameworkType(str, Enum):

    DJANGO = "django"
    FASTAPI = "fastapi"
    FLASK = "flask"

    REACT = "react"
    NEXTJS = "nextjs"
    ANGULAR = "angular"
    VUE = "vue"

    SPRING = "spring"

    UNKNOWN = "unknown"


class DocumentType(str, Enum):

    CODE = "code"
    MARKUP = "markup"
    STYLE = "style"
    CONFIG = "config"
    DATA = "data"
    TEXT = "text"
    UNKNOWN = "unknown"
