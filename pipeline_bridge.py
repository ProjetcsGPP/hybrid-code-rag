# pipeline_bridge.py

from pipeline.structure.structural_indexer import StructuralIndexer

# futuro import (quando existir)
# from pipeline_v2.application.indexing_service import IndexingService


class PipelineBridge:
    """
    Camada de transição entre pipeline legado e pipeline_v2.
    Permite rodar os dois sistemas em paralelo.
    """

    def __init__(self, mode="legacy"):
        self.mode = mode
        self.legacy = StructuralIndexer()

        # self.new = IndexingService()

    def run_indexer(self, *args, **kwargs):
        """
        Executa indexação em modo legado ou novo pipeline.
        """
        if self.mode == "legacy":
            return self.legacy.run(*args, **kwargs)

        # return self.new.run(*args, **kwargs)
        raise NotImplementedError("pipeline_v2 ainda não ativo")
