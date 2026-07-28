from opentelemetry._logs import set_logger_provider
from opentelemetry.sdk._logs import LoggerProvider, LoggingHandler
from opentelemetry.sdk._logs.export import BatchLogRecordProcessor
from opentelemetry.exporter.otlp.proto.grpc._log_exporter import OTLPLogExporter
from opentelemetry.sdk.resources import Resource

import json
import logging
import os


class JsonFormatter(logging.Formatter):
    def format(self, record) -> dict:
        log_record = {
            "timestamp": record.created,
            "severity": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "pathname": record.pathname,
            "lineno": record.lineno,
        }
        return json.dumps(log_record)


def setup_otel_logging(otel_settings: dict) -> None:
    instance_id = os.getenv("POD_NAME"),
    if not instance_id:
        instance_id = '1'
    resource = Resource.create(
        {
            "service.name": "simpleservice",
            "service.instance.id": f"simpleservice-{instance_id}"
        }
    )
    logger_provider = LoggerProvider(resource=resource)
    set_logger_provider(logger_provider)

    exporter = OTLPLogExporter(
        endpoint = f"{otel_settings["host"]}:{otel_settings["port"]}",
        insecure = True
    )

    logger_provider.add_log_record_processor(BatchLogRecordProcessor(exporter))
    handler = LoggingHandler(level=logging.INFO, logger_provider=logger_provider)

    root = logging.getLogger()
    root.addHandler(handler)
