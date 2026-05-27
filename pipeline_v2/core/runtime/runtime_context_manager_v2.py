# pipeline_v2/core/runtime/runtime_context_manager_v2.py


class RuntimeContextManagerV2:

    def __init__(
        self,
        runtime_graph,
    ):

        self.runtime_graph = runtime_graph

    # =====================================================
    # CONTEXT
    # =====================================================

    def ensure_context(
        self,
        context,
    ):

        if not self.runtime_graph.has_context(context.context_id):
            return True

        return False

    def clear_context(
        self,
        context,
    ):

        self.runtime_graph.clear_context(context.context_id)

    def stats(
        self,
        context,
    ):

        return self.runtime_graph.stats(context.context_id)
