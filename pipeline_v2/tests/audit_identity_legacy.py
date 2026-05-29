# pipeline_v2/tests/audit_identity_legacy.py

import importlib

modules = [
    "pipeline_v2.core.identity.identity_registry",
    "pipeline_v2.core.identity.identity_service_v2",
]


for m in modules:

    try:

        importlib.import_module(m)

        print("OK:", m)

    except Exception as e:

        print("BROKEN:", m, e)
