# pipeline_v2/core/graph/graph_index.py

from collections import defaultdict


class GraphIndexV2:
    def __init__(self):
        self.by_name = {}
        self.by_canonical = {}
        self.by_type = defaultdict(list)

    def index_node(self, node):
        self.by_name[node.name] = node.id
        self.by_canonical[node.canonical] = node.id
        self.by_type[node.type].append(node.id)

    def resolve_by_name(self, name: str):
        return self.by_name.get(name)

    def resolve_by_canonical(self, canonical: str):
        return self.by_canonical.get(canonical)
