# pipeline_v2/validation/contracts/base_auditor.py

from abc import ABC, abstractmethod


class BaseAuditor(ABC):

    @abstractmethod
    def audit(self, context, result):
        """Execute architectural audit."""
        raise NotImplementedError
