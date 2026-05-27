# pipeline_v2/experimental_engine/experimental_facade.py


class ExperimentalFacade:

    def __init__(self, runtime_engine, trace_analyzer, reasoning_engine):
        self.runtime = runtime_engine
        self.trace = trace_analyzer
        self.reasoning = reasoning_engine

    def analyze(self, node_id: str):

        runtime = self.runtime.execute(node_id)
        trace = self.trace.analyze(runtime)
        reasoning = self.reasoning.reason(runtime)

        return {"runtime": runtime, "trace": trace, "reasoning": reasoning}
