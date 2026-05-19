# pipeline_v2/application/main.py

from fastapi import FastAPI

from pipeline_v2.application.bootstrap_runtime import bootstrap_runtime

from pipeline_v2.application.graph_api.routes.graph_api import (
    router as graph_router,
)

from pipeline_v2.adapters.openwebui.graph_tool import (
    router as openwebui_router,
)

from pipeline_v2.application.startup import preload_graph

app = FastAPI(title="CODE-RAG Graph API V2")

preload_graph()

bootstrap_runtime()

app.include_router(openwebui_router, prefix="/tools")

app.include_router(graph_router, prefix="/graph")
