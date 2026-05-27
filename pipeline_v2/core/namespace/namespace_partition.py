# pipeline_v2/core/namespace/namespace_partition.py


class NamespacePartitionBuilder:
    """
    Responsável por criar:

    - graph partition
    - vector partition
    - semantic routing keys
    """

    def build_partition_key(
        self,
        namespace_id: str,
    ) -> str:

        return f"graph::{namespace_id}"
