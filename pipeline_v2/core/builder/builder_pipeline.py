# pipeline_v2/core/builder/builder_pipeline.py

from .graph_builder import GraphBuilderV2
from .build_context import BuildContextV2


class BuilderPipelineV2:

    def __init__(self):
        self.builder = GraphBuilderV2()

    def process(self, file_path, symbols, relationships):

        context = BuildContextV2(
            file_path=file_path, symbols=symbols, relationships=relationships
        )

        graph = self.builder.ingest_file(context)

        return graph
