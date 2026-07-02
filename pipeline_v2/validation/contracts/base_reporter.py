# pipeline_v2/validation/contracts/base_reporter.py

from abc import ABC, abstractmethod


class BaseReporter(ABC):

    @abstractmethod
    def report(self, result):
        """Render ValidationResult."""
        raise NotImplementedError
