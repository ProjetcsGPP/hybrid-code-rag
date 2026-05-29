# pipeline_v2/application/bootstrap_runtime.py

from pipeline_v2.application.config.settings import Settings

from pipeline_v2.application.runtime_context import (
    RuntimeContextV2,
)

from pipeline_v2.core.storage.postgres.postgres_connection import (
    PostgresConnection,
)

from pipeline_v2.core.storage.postgres.postgres_repository import (
    PostgresRepository,
)

from pipeline_v2.core.graph.graph_core import GraphCoreV2

from pipeline_v2.core.identity.identity_registry import (
    IdentityRegistryV2,
)

from pipeline_v2.core.audit.graph_mutation_auditor_v2 import (
    GraphMutationAuditorV2,
)

# =========================================================
# RUNTIME FACTORY
# =========================================================


def create_runtime_context():

    # Factory oficial de runtime isolado.#

    # Cada chamada cria:
    # - registry independente
    # - graph independente
    # - auditor independente#

    # Permitindo:
    # - harnesses determinísticos
    # - testes isolados
    # - múltiplos runtimes
    # - replay seguro

    identity_registry = IdentityRegistryV2()

    mutation_auditor = GraphMutationAuditorV2(
        identity_registry=identity_registry,
    )

    graph_runtime = GraphCoreV2(
        mutation_auditor=mutation_auditor,
    )

    return RuntimeContextV2(
        identity_registry=identity_registry,
        graph_runtime=graph_runtime,
        mutation_auditor=mutation_auditor,
    )


# =========================================================
# GLOBAL RUNTIME (TRANSITIONAL COMPATIBILITY)
# =========================================================

global_runtime = create_runtime_context()

identity_registry = global_runtime.identity_registry

graph_runtime = global_runtime.graph_runtime

mutation_auditor = global_runtime.mutation_auditor

# =========================================================
# LEGACY BOOTSTRAP API
# =========================================================


def bootstrap_runtime():

    return {
        "identity_registry": identity_registry,
        "graph_runtime": graph_runtime,
        "mutation_auditor": mutation_auditor,
    }


# =========================================================
# POSTGRES
# =========================================================


def build_postgres_repository():

    conn = PostgresConnection(
        host=Settings.DB_HOST,
        port=Settings.DB_PORT,
        database=Settings.DB_NAME,
        user=Settings.DB_USER,
        password=Settings.DB_PASSWORD,
    )

    conn.execute()

    return PostgresRepository(conn)
