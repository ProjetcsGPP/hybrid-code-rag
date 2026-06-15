# pipeline_v2/tests/test_inheritance_resolver_v2.py

from pipeline_v2.core.semantic.inheritance.inheritance_resolver_v2 import (
    InheritanceResolverV2,
)

from pipeline_v2.core.contract.graph_contracts import (
    InheritanceEdgeV2,
)


def test_resolve_exact_match():

    resolver = InheritanceResolverV2(
        symbol_index={
            "BaseService": "symbol_123",
        }
    )

    result = resolver.resolve(
        [
            InheritanceEdgeV2(
                base_symbol_name="BaseService",
            )
        ]
    )

    assert len(result) == 1
    assert result[0].resolved_base_symbol_id == "symbol_123"


def test_resolve_normalized_match():

    resolver = InheritanceResolverV2(
        symbol_index={
            "BaseService": "symbol_123",
        }
    )

    result = resolver.resolve(
        [
            InheritanceEdgeV2(
                base_symbol_name=" BaseService ",
            )
        ]
    )

    assert len(result) == 1
    assert result[0].resolved_base_symbol_id == "symbol_123"


def test_unresolved_returns_none():

    resolver = InheritanceResolverV2(symbol_index={})

    result = resolver.resolve(
        [
            InheritanceEdgeV2(
                base_symbol_name="UnknownBase",
            )
        ]
    )

    assert len(result) == 1
    assert result[0].resolved_base_symbol_id is None
