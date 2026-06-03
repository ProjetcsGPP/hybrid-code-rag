# pipeline_v2/core/writer/relationship_writer_v2.py

from pipeline_v2.core.repository.scoped_relationship_repository_v2 import (
    ScopedRelationshipRepositoryV2,
)
from pipeline_v2.core.contract.contract_enforcer import (
    ContractEnforcer,
)


class RelationshipWriterV2:

    def __init__(
        self,
        graph_store,
    ):

        self.repository = ScopedRelationshipRepositoryV2(
            graph_store,
        )

    def write(
        self,
        relationship,
        scope,
    ):

        relationship = ContractEnforcer.enforce_relationship(relationship)

        self.repository.write_relationship(
            relationship,
            scope,
        )
