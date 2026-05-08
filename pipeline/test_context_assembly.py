from pipeline.structure.context.assembly_engine import ContextAssemblyEngine
from pipeline.structure.storage.sqlite_store import SQLiteStructuralStore
from pipeline.structure.structural_query import StructuralQuery

store = SQLiteStructuralStore()
query = StructuralQuery(store)

engine = ContextAssemblyEngine(query)

result = engine.build("symbol_id_exemplo")

print(result)
