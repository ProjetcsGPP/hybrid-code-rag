# pipeline_v2/core/state/confidence_engine.py


class ConfidenceEngineV2:
    """
    Calcula confidence semântico incremental.
    """

    @staticmethod
    def propagate(base: float, delta: float):

        value = base + delta

        if value > 1.0:
            value = 1.0

        if value < 0.0:
            value = 0.0

        return round(value, 4)
