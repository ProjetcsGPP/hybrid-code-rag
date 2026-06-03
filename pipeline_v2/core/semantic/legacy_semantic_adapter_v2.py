# pipeline_v2/core/semantic/legacy_semantic_adapter_v2.py


class LegacySemanticAdapterV2:
    """
    Traduz saída do legacy para contrato canônico da V2.
    """

    def adapt(self, legacy_output: dict) -> dict:

        if not isinstance(legacy_output, dict):
            raise TypeError(f"Expected dict, got {type(legacy_output)}")

        required = [
            "symbols",
            "relationships",
            "inheritance_edges",
        ]

        for key in required:
            legacy_output.setdefault(key, [])

        return {
            "symbols": self._adapt_symbols(legacy_output.get("symbols", [])),
            "relationships": self._adapt_relationships(
                legacy_output.get("relationships", [])
            ),
            "inheritance_edges": self._adapt_inheritance(
                legacy_output.get("inheritance_edges", [])
            ),
        }

    def _adapt_symbols(self, symbols):
        return symbols  # por enquanto pass-through controlado

    def _adapt_relationships(self, rels):
        return rels  # futuro: normalização tipada

    def _adapt_inheritance(self, edges):
        return edges
