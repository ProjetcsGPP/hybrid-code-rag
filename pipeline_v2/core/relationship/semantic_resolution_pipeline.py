# pipeline_v2/core/relationship/semantic_resolution_pipeline.py


class SemanticResolutionPipeline:

    def __init__(self, symbol_resolver, semantic_engine):
        self.symbol_resolver = symbol_resolver
        self.semantic_engine = semantic_engine

    def resolve(self, chunk, call, symbol_table, semantic_context):

        # 1. semantic inference
        inference = self.semantic_engine.resolve_call(call, semantic_context)

        # 2. target resolution
        resolved = self.symbol_resolver.resolve(inference.get("resolved_call", call))

        return {
            "target": resolved["target"] if resolved else None,
            "inference": inference,
            "confidence": inference.get("confidence", 0.5),
        }
