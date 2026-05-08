import ast
import logging
from pathlib import Path

logger = logging.getLogger(__name__)


class ASTChunker:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.module_name = Path(file_path).stem

        self.source = Path(file_path).read_text(encoding="utf-8")
        self.tree = ast.parse(self.source)

        self.imports_context = self._extract_imports()

    def chunk(self):
        chunks = []

        for node in self.tree.body:

            # classes
            if isinstance(node, ast.ClassDef):

                if self._is_noise(node, node.name):
                    continue

                class_chunk = self._build_chunk(
                    node=node,
                    node_type="class",
                    parent_class=None,
                    parent_chunk_id=None,
                    siblings=[],
                )

                chunks.append(class_chunk)

                class_chunk_id = class_chunk["metadata"]["chunk_id"]

                class_methods = [
                    child.name
                    for child in node.body
                    if isinstance(child, ast.FunctionDef)
                    and not self._is_noise(child, child.name)
                ]

                for child in node.body:

                    if not isinstance(child, ast.FunctionDef):
                        continue

                    if self._is_noise(child, child.name):
                        continue

                    siblings = [
                        m for m in class_methods if m != child.name
                    ]

                    method_chunk = self._build_chunk(
                        node=child,
                        node_type="function",
                        parent_class=node.name,
                        parent_chunk_id=class_chunk_id,
                        siblings=siblings,
                    )

                    chunks.append(method_chunk)

            # funções globais
            elif isinstance(node, ast.FunctionDef):

                if self._is_noise(node, node.name):
                    continue

                function_chunk = self._build_chunk(
                    node=node,
                    node_type="function",
                    parent_class=None,
                    parent_chunk_id=f"{self.module_name}::GLOBAL",
                    siblings=[],
                )

                chunks.append(function_chunk)

        return chunks

    # -----------------------------
    # AST helpers
    # -----------------------------

    def _extract_calls(self, node):
        calls = []

        for child in ast.walk(node):
            if isinstance(child, ast.Call):

                if isinstance(child.func, ast.Attribute):
                    calls.append(child.func.attr)

                elif isinstance(child.func, ast.Name):
                    calls.append(child.func.id)

        return list(set(calls))

    def _extract_imports(self):
        imports = []

        for node in ast.walk(self.tree):

            if isinstance(node, ast.Import):
                for alias in node.names:
                    imports.append(alias.name)

            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    imports.append(node.module)

        return sorted(list(set(imports)))

    def _extract_decorators(self, node):
        decorators = []

        for dec in getattr(node, "decorator_list", []):

            if isinstance(dec, ast.Name):
                decorators.append(dec.id)

            elif isinstance(dec, ast.Call):

                if isinstance(dec.func, ast.Name):
                    decorators.append(dec.func.id)

                elif isinstance(dec.func, ast.Attribute):
                    decorators.append(dec.func.attr)

            elif isinstance(dec, ast.Attribute):
                decorators.append(dec.attr)

        return decorators

    # -----------------------------
    # Structure helpers
    # -----------------------------

    def _build_hierarchy_path(self, node_type, parent_class, name):
        path = [f"Module({self.module_name})"]

        if node_type == "class":
            path.append(f"Class({name})")

        elif node_type == "function":
            if parent_class:
                path.append(f"Class({parent_class})")
            path.append(f"Function({name})")

        return " > ".join(path)

    def _build_chunk_id(self, node_type, name, parent_class=None):
        base = Path(self.file_path).name

        if node_type == "class":
            return f"{base}::{name}"

        if parent_class:
            return f"{base}::{parent_class}::{name}"

        return f"{base}::{name}"

    def _build_symbol_path(self, parent_class, name):
        base = Path(self.file_path).stem

        if parent_class:
            return f"{base}.{parent_class}.{name}"

        return f"{base}.{name}"

    def _is_noise(self, node, name: str) -> bool:
        if not name:
            return True

        noise_patterns = {"__str__", "__repr__", "__eq__", "__hash__"}

        if name in noise_patterns:
            return True

        if isinstance(node, ast.ClassDef) and name == "Meta":
            return True

        return False

    # -----------------------------
    # Semantic layer
    # -----------------------------

    def _infer_semantic(self, name: str) -> str:
        name_lower = name.lower()

        if any(k in name_lower for k in ["validate", "check", "clean"]):
            return "validation"

        if any(k in name_lower for k in ["auth", "permission", "role"]):
            return "authorization"

        if any(
            k in name_lower
            for k in ["create", "save", "insert", "update", "delete"]
        ):
            return "mutation"

        if any(k in name_lower for k in ["get", "fetch", "list", "query"]):
            return "query"

        return "general"

    def _calculate_importance(self, semantic, node_type, name, decorators):
        score = 1.0

        if semantic == "authorization":
            score += 0.5
        elif semantic == "validation":
            score += 0.4
        elif semantic == "mutation":
            score += 0.3
        elif semantic == "query":
            score += 0.1

        if node_type == "class" and semantic != "general":
            score += 0.2

        if name.startswith(("get_", "fetch_")):
            score -= 0.2

        if decorators:
            score += 0.2

        return float(score)

    # -----------------------------
    # Chunk builder
    # -----------------------------

    def _build_chunk(
        self,
        node,
        node_type,
        parent_class=None,
        parent_chunk_id=None,
        siblings=None,
    ):
        start_line = node.lineno
        end_line = getattr(node, "end_lineno", start_line + 1)

        source_lines = self.source.splitlines()
        code = "\n".join(source_lines[start_line - 1 : end_line])

        name = getattr(node, "name", "") or ""

        semantic = self._infer_semantic(name)
        decorators = self._extract_decorators(node)

        chunk_id = self._build_chunk_id(
            node_type=node_type,
            name=name,
            parent_class=parent_class,
        )

        hierarchy_path = self._build_hierarchy_path(
            node_type=node_type,
            parent_class=parent_class,
            name=name,
        )

        symbol_path = self._build_symbol_path(
            parent_class=parent_class,
            name=name,
        )

        importance_score = self._calculate_importance(
            semantic, node_type, name, decorators
        )

        return {
            "text": code,
            "metadata": {
                "type": node_type,
                "name": name,
                "file": self.file_path,
                "start_line": start_line,
                "end_line": end_line,
                "symbol_path": symbol_path,
                "semantic_type": semantic,
                "importance_score": importance_score,
                "chunk_id": chunk_id,
                "parent_chunk_id": parent_chunk_id,
                "parent_class": parent_class,
                "module_name": self.module_name,
                "ast_hierarchy_path": hierarchy_path,
                "decorators": decorators,
                "imports_context": self.imports_context,
                "siblings": siblings or [],
                "calls": self._extract_calls(node),
                "semantic_matches": [],
                "semantic_confidence": 0.0,
            },
        }