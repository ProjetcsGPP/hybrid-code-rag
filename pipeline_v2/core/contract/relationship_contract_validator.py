# pipeline_v2/core/contract/relationship_contract_validator.py

from .semantic_contract import RelationshipContract


class RelationshipContractValidator:

    @staticmethod
    def validate(rel: RelationshipContract):

        if not rel.source:
            raise ValueError("Relationship missing source")

        if not rel.target:
            raise ValueError("Relationship missing target")

        if rel.confidence < 0:
            raise ValueError("Invalid confidence")

        if rel.confidence > 1:
            raise ValueError("Invalid confidence")

        return rel
