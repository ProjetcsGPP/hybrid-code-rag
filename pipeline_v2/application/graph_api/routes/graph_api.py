# pipeline_v2/application/graph_api/routes/graph_api.py

from fastapi import APIRouter

from pipeline_v2.core.graph.runtime_graph import graph_runtime
from pipeline_v2.application.graph_api.dto.graph_serializer import GraphSerializer

from pydantic import BaseModel

from pipeline_v2.application.pipeline_bridge import PipelineBridgeV2

from pipeline_v2.application.bootstrap_runtime import global_runtime

router = APIRouter()
graph = graph_runtime
serializer = GraphSerializer()


# -------------------------
# NODE
# -------------------------
@router.get("/node/{node_id}")
def get_node(node_id: str):
    node = graph.get_node(node_id)

    if not node:
        return None

    return serializer.node(node)


# -------------------------
# TRACE
# -------------------------
@router.get("/trace/{node_id}")
def trace(node_id: str):

    result = graph.trace(node_id)

    return {
        "from": [serializer.edge(e) for e in result["from"]],
        "to": [serializer.edge(e) for e in result["to"]],
    }


# -------------------------
# SUBGRAPH (MUITO IMPORTANTE PARA NEXT.JS)
# -------------------------
@router.get("/subgraph/{node_id}")
def subgraph(node_id: str, depth: int = 1):

    sg = graph.subgraph(node_id, depth)

    return {
        "nodes": [serializer.node(n) for n in sg["nodes"]],
        "edges": [serializer.edge(e) for e in sg["edges"]],
    }


# -------------------------
# SEMANTIC TRACE
# -------------------------
@router.get("/trace/semantic/{node_id}")
def semantic_trace(node_id: str, layer: str = None, status: str = None):

    edges = graph.semantic_trace(node_id, layer=layer, status=status)

    return [serializer.edge(e) for e in edges]


# -------------------------
# EDGE TYPE FILTER
# -------------------------
@router.get("/edges/type/{edge_type}")
def edges_by_type(edge_type: str):

    edges = graph.get_edges_by_type(edge_type)

    return [serializer.edge(e) for e in edges]


# -------------------------
# INGEST FILE
# -------------------------


class IngestRequest(BaseModel):
    file_path: str


@router.post("/ingest")
def ingest_file(req: IngestRequest):

    bridge = PipelineBridgeV2(global_runtime)

    result = bridge.run(req.file_path)

    return result
