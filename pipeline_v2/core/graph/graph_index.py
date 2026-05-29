# pipeline_v2/core/graph/graph_index.py

from collections import defaultdict


class GraphIndexV2:

    def __init__(self):

        self.reset()

    # =====================================================
    # RESET
    # =====================================================

    def reset(self):

        self.by_name = {}

        self.by_canonical = {}

        self.by_type = defaultdict(list)

    # =====================================================
    # INDEXING
    # =====================================================

    def index_node(self, node):

        if getattr(node, "name", None):

            self.by_name[node.name] = node.id

        if getattr(node, "canonical", None):

            self.by_canonical[node.canonical] = node.id

        if getattr(node, "type", None):

            self.by_type[node.type].append(node.id)

    # =====================================================
    # RESOLUTION
    # =====================================================

    def resolve_by_name(self, name: str):

        return self.by_name.get(name)

    def resolve_by_canonical(self, canonical: str):

        return self.by_canonical.get(canonical)
