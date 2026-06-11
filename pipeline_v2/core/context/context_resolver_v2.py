from dataclasses import dataclass
from typing import Dict, Any, Optional, List


@dataclass
class ContextResultV2:
    language: str
    framework: Optional[str]
    confidence: float
    hints: Dict[str, Any]
    inheritance_model: str  # e.g. "django_model", "oop_class", "unknown"
    metadata: Dict[str, Any]


class ContextResolverV2:
    """
    Detecta o contexto estrutural do código SEM assumir regras fixas de framework.

    Não resolve herança diretamente.
    Apenas classifica o ambiente.
    """

    def resolve(
        self,
        chunks: List[Dict[str, Any]],
        symbols: List[Any] = None,
    ) -> ContextResultV2:

        language = self._detect_language(chunks)
        framework, fw_conf = self._detect_framework(chunks, symbols)

        inheritance_model = self._infer_inheritance_model(framework, symbols)

        return ContextResultV2(
            language=language,
            framework=framework,
            confidence=fw_conf,
            hints={
                "has_orm": self._detect_orm(chunks),
                "has_models": self._detect_models(symbols),
                "has_import_patterns": self._detect_import_patterns(chunks),
            },
            inheritance_model=inheritance_model,
            metadata={
                "chunks": len(chunks),
                "symbols": len(symbols) if symbols else 0,
            },
        )

    # =========================================================
    # LANGUAGE DETECTION
    # =========================================================

    def _detect_language(self, chunks) -> str:
        for c in chunks:
            metadata = c["metadata"] if "metadata" in c else {}
            path = metadata["file"] if "file" in metadata else ""
            if path.endswith(".py"):
                return "python"
        return "unknown"

    # =========================================================
    # FRAMEWORK DETECTION (NO HARDCODE RULES)
    # =========================================================

    def _detect_framework(self, chunks, symbols):
        """
        Heurística leve — SEM assumir Django.
        """

        score = {}

        for c in chunks:
            code = c["code"] if "code" in c else ""

            if "models.Model" in code:
                score["django"] = (
                    score["django"] if "django" in score else 0
                ) + 0.4

            if "BaseModel" in code:
                score["pydantic"] = (
                    score["pydantic"] if "pydantic" in score else 0
                ) + 0.4

            if "FastAPI" in code:
                score["fastapi"] = (
                    score["fastapi"] if "fastapi" in score else 0
                ) + 0.3

        if not score:
            return None, 0.0

        framework = max(score, key=score.get)
        confidence = min(score[framework], 1.0)

        return framework, confidence

    # =========================================================
    # INHERITANCE MODEL INFERENCE
    # =========================================================

    def _infer_inheritance_model(self, framework, symbols):
        """
        NÃO decide regras de herança.
        Só classifica o tipo de sistema.
        """

        if framework == "django":
            return "django_model"

        if framework == "pydantic":
            return "dataclass_model"

        if symbols:
            for s in symbols:
                if getattr(s, "symbol_type", None) == "class":
                    return "oop_class"

        return "unknown"

    # =========================================================
    # SIGNAL DETECTORS
    # =========================================================

    def _detect_orm(self, chunks) -> bool:
        return any("objects." in (c["code"] if "code" in c else "") for c in chunks)

    def _detect_models(self, symbols) -> bool:
        if not symbols:
            return False
        return any("Model" in getattr(s, "name", "") for s in symbols)

    def _detect_import_patterns(self, chunks) -> bool:
        return any("import" in (c["code"] if "code" in c else "") for c in chunks)
