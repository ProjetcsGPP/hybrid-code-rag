from pipeline.contracts import Symbol


class SymbolExtractor:

    def extract(self, chunk: dict) -> Symbol:

        metadata = chunk["metadata"]

        calls = metadata.get("calls", None)

        return Symbol(
            symbol_id=metadata["chunk_id"],
            symbol_path=metadata.get("symbol_path", ""),
            name=metadata.get("name", ""),
            symbol_type=metadata.get("type", "unknown"),
            module_name=metadata.get("module_name", ""),
            file_path=metadata.get("file", ""),
            parent_symbol_id=metadata.get("parent_chunk_id"),
            semantic_type=metadata.get("semantic_type", "general"),
            start_line=int(metadata.get("start_line", 0)),
            end_line=int(metadata.get("end_line", 0)),
            calls=calls,   # 🔥 AGORA SIM
        )