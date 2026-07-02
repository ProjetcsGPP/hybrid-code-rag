# pipeline_v2/validation/main_validation.py

from pipeline_v2.validation.collectors.identity_metrics_collector import (
    IdentityMetricsCollector,
)
from pipeline_v2.validation.collectors.graph_metrics_collector import (
    GraphMetricsCollector,
)

from pipeline_v2.validation.reporters.console_reporter import ConsoleReporter
from pipeline_v2.validation.runner.validation_runner import ValidationRunner

runner = ValidationRunner()

runner.register_collector(GraphMetricsCollector())
runner.register_collector(IdentityMetricsCollector())

runner.register_reporter(ConsoleReporter())

result = runner.run(context)
