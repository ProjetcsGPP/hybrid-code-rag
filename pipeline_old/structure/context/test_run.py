# pipeline/structure/context/test_run.py

from pipeline.structure.context.assembly_engine import ContextAssemblyEngine
from pipeline.structure.structural_query import StructuralQuery
from pipeline.structure.storage.sqlite_store import SQLiteStructuralStore
from pipeline.contracts import Symbol

store = SQLiteStructuralStore()
store.reset()

# 🔥 seed mínimo
store.save_symbol(Symbol(
    symbol_id="test_1",
    symbol_path="test.module.func",
    name="func",
    symbol_type="function",
    module_name="test_module",
    file_path="test.py",
    parent_symbol_id=None,
    semantic_type="test",
    start_line=1,
    end_line=10
))

query = StructuralQuery(store)
engine = ContextAssemblyEngine(query)

symbol = store.conn.execute(
    "SELECT symbol_id FROM symbols LIMIT 1"
).fetchone()

print(engine.build(symbol["symbol_id"]))