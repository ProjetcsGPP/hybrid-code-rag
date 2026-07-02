# pipeline_v2/validation/contracts/base_collector.py

from abc import ABC, abstractmethod


class BaseCollector(ABC):

    @abstractmethod
    def collect(self, context, result):
        """Collect metrics into ValidationResult."""
        raise NotImplementedError
