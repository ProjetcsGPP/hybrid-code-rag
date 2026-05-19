# pipeline_v2/adapters/openwebui/graph_tool.py

from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional, Dict, Any

from pipeline_v2.adapters.openwebui.handler import GraphToolHandler

router = APIRouter()
handler = GraphToolHandler()


# -----------------------------
# INPUT MODEL (OpenWebUI TOOL CONTRACT)
# -----------------------------
class GraphToolRequest(BaseModel):
    node_id: str
    depth: int = 2
    filters: Optional[Dict[str, Any]] = None


# -----------------------------
# TOOL ENDPOINT
# -----------------------------
@router.post("/graph-context")
def graph_context_tool(payload: GraphToolRequest):

    return handler.run(
        node_id=payload.node_id, depth=payload.depth, filters=payload.filters
    )
