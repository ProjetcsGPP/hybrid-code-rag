# pipeline/__init__.py

import sys
import importlib

# redirecionamento temporário
_old = importlib.import_module("pipeline_old")
sys.modules["pipeline_old"] = _old
