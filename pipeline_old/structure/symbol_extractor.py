# pipeline/structure/symbol_extractor.py

from pipeline.contracts import Symbol


class SymbolExtractor:

    def extract(self, chunk: dict) -> Symbol:

        metadata = chunk["metadata"]

        calls = metadata.get("calls") or []
        imports = metadata.get("imports_context") or []

        chunk_id = metadata["chunk_id"]

        symbol_type = metadata.get("type", "unknown")

        assignments = metadata.get("assignments") or []

        # -------------------------------------------------
        # FALLBACK AUTOMÁTICO PARA parent_symbol_id
        # -------------------------------------------------

        parent_symbol_id = metadata.get("parent_chunk_id")

        # método de classe:
        # models.py::Classe::metodo
        if (
            not parent_symbol_id
            and symbol_type == "function"
            and chunk_id.count("::") >= 2
        ):

            parent_symbol_id = "::".join(chunk_id.split("::")[:-1])

        print("\nSYMBOL EXTRACTOR:")
        print("CHUNK ID:", chunk_id)
        print("TYPE:", symbol_type)
        print("PARENT:", parent_symbol_id)
        print("BASES:", metadata.get("bases"))
        print("ASSIGNMENTS:", assignments)

        return Symbol(
            symbol_id=chunk_id,
            symbol_path=metadata.get("symbol_path", ""),
            canonical_name=metadata.get("symbol_path", ""),
            name=metadata.get("name", ""),
            symbol_type=symbol_type,
            module_name=metadata.get("module_name", ""),
            file_path=metadata.get("file", ""),
            parent_symbol_id=parent_symbol_id,
            semantic_type=metadata.get("semantic_type", "general"),
            start_line=int(metadata.get("start_line", 0)),
            end_line=int(metadata.get("end_line", 0)),
            calls=calls,
            imports=imports,
            bases=metadata.get("bases", []),
            assignments=assignments,
        )
