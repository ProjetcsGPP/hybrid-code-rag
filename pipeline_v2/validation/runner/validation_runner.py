# pipeline_v2/validation/runner/validation_runner.py

from pipeline_v2.validation.contracts.validation_result import ValidationResult


class ValidationRunner:

    def __init__(self):
        self.collectors = []
        self.auditors = []
        self.reporters = []

    def register_collector(self, collector):
        self.collectors.append(collector)

    def register_auditor(self, auditor):
        self.auditors.append(auditor)

    def register_reporter(self, reporter):
        self.reporters.append(reporter)

    def run(self, context):

        result = ValidationResult()

        for collector in self.collectors:
            collector.collect(context, result)

        for auditor in self.auditors:
            auditor.audit(context, result)

        for reporter in self.reporters:
            reporter.report(result)

        return result
