# pipeline_v2/core/context/semantic_resolution_payload.py

from dataclasses import dataclass, field
from typing import Any

from pipeline_v2.core.contract.semantic_inference_result import (
    SemanticInferenceResult,
)


@dataclass(frozen=True)
class SemanticResolutionPayload:

    resolved_owner: str | None = None

    semantic_type: str = "unknown"

    model: str | None = None

    dispatch: str = "DIRECT"

    inferred_symbol: str | None = None

    framework_hint: str | None = None

    confidence: float = 0.0

    provenance: str = "UNKNOWN"

    resolved_call: str | None = None

    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self):

        return {
            "resolved_owner": self.resolved_owner,
            "semantic_type": self.semantic_type,
            "model": self.model,
            "dispatch": self.dispatch,
            "inferred_symbol": self.inferred_symbol,
            "framework_hint": self.framework_hint,
            "confidence": self.confidence,
            "provenance": self.provenance,
            "resolved_call": self.resolved_call,
            "metadata": self.metadata,
        }

    def merge_inference(
        self,
        inference: SemanticInferenceResult,
    ):

        return SemanticResolutionPayload(
            resolved_owner=(inference.semantic_owner or self.resolved_owner),
            semantic_type=self.semantic_type,
            model=self.model,
            dispatch=inference.dispatch or self.dispatch,
            inferred_symbol=(inference.inferred_symbol or self.inferred_symbol),
            framework_hint=(inference.framework_hint or self.framework_hint),
            confidence=max(
                self.confidence,
                inference.confidence,
            ),
            provenance=(inference.provenance or self.provenance),
            resolved_call=(inference.resolved_call or self.resolved_call),
            metadata=self.metadata,
        )
