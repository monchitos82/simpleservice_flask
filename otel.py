from opentelemetry._logs import set_logger_provider
from opentelemetry.sdk._logs import LoggerProvider, LoggingHandler
from opentelemetry.sdk._logs.export import BatchLogRecordProcessor
from opentelemetry.exporter.otlp.proto.grpc._log_exporter import OTLPLogExporter
from opentelemetry.sdk.resources import Resource
from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor
from opentelemetry.instrumentation.sqlalchemy import SQLAlchemyInstrumentor
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import SimpleSpanProcessor
from opentelemetry import metrics
from opentelemetry.exporter.otlp.proto.grpc.metric_exporter import OTLPMetricExporter
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
from flask import Flask


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


def setup_otel_logging(otel_settings: dict, app: Flask) -> None:
    instance_id = os.getenv("POD_NAME", 1)
    resource = Resource.create(
        {
            "service.name": otel_settings["service_name"],
            "service.instance.id": f"{otel_settings['service_name']}-{instance_id}",
        }
    )
    logger_provider = LoggerProvider(resource=resource)
    set_logger_provider(logger_provider)

    exporter = OTLPLogExporter(
        endpoint=f"{otel_settings["host"]}:{otel_settings["port"]}", insecure=True
    )

    logger_provider.add_log_record_processor(BatchLogRecordProcessor(exporter))
    handler = LoggingHandler(level=logging.INFO, logger_provider=logger_provider)

    app.logger.addHandler(handler)


def setup_otel_tracing(otel_settings: dict, app: Flask) -> None:
    resource = Resource.create(
        {
            "service.name": otel_settings["service_name"],
            "service.instance.id": os.getenv("POD_NAME", "Undefined"),
            "k8s.pod.name": os.getenv("POD_NAME", "Undefined"),
            "k8s.namespace.name": os.getenv("POD_NAMESPACE", "Undefined"),
            "k8s.pod.ip": os.getenv("POD_IP", "Undefined"),
            "k8s.node.name": os.getenv("NODE_NAME", "Undefined"),
        }
    )
    trace.set_tracer_provider(TracerProvider(resource=resource))

    otlp_tracing_exporter = OTLPSpanExporter(
        endpoint=f"{otel_settings["host"]}:{otel_settings["port"]}",
        insecure=True,
    )
    trace.get_tracer_provider().add_span_processor(
        SimpleSpanProcessor(otlp_tracing_exporter)
    )

    RequestsInstrumentor().instrument()
    FlaskInstrumentor().instrument_app(app)
    SQLAlchemyInstrumentor().instrument(engine=app.db.engine)


def setup_otel_metrics(otel_settings: dict, app: Flask) -> None:
    instance_id = os.getenv("POD_NAME", 1)
    resource = Resource.create(
        {
            "service.name": otel_settings["service_name"],
            "service.instance.id": f"{otel_settings['service_name']}-{instance_id}",
        }
    )
    metric_exporter = OTLPMetricExporter(
        endpoint=f"{otel_settings["host"]}:{otel_settings["port"]}",
        insecure=True,
    )
    reader = PeriodicExportingMetricReader(
        exporter=metric_exporter,
        export_interval_millis=3000.0,
        export_timeout_millis=5000.0,
    )
    meter_provider = MeterProvider(metric_readers=[reader], resource=resource)
    metrics.set_meter_provider(meter_provider)
    meter = metrics.get_meter(__name__)
    counter = meter.create_counter(
        name="requests", description="Number of requests", unit="1"
    )
    app.counter = counter
