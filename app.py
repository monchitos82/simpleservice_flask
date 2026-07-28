import logging

from faker import Faker
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import \
    OTLPSpanExporter
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor
from opentelemetry.instrumentation.sqlalchemy import SQLAlchemyInstrumentor
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import (BatchSpanProcessor,
                                            SimpleSpanProcessor)
from prometheus_client import CollectorRegistry

from blueprints.simplistic import simplistic_bp
from config import DevelopmentConfig


def create_app(config_class: object = DevelopmentConfig) -> object:
    app = Flask(__name__)
    app.db = SQLAlchemy()
    app.config.from_object(config_class)
    app.logger = logging.getLogger(__name__)
    registry = CollectorRegistry()
    app.faker = Faker()
    app.db.init_app(app)
    app.register_blueprint(simplistic_bp)
    use_otel = app.config.get("USE_OTEL", False)
    if use_otel:
        try:
            with app.app_context():

                resource = Resource.create({"service.name": "simpleservice"})
                trace.set_tracer_provider(TracerProvider(resource=resource))
                tracer = trace.get_tracer(__name__)

                jaeger_config = app.config.get("JAEGER_SETTINGS", {})

                if jaeger_config.get("USE_JAEGER"):
                    jaeger_config = app.config.get("JAEGER_SETTINGS")
                    jaeger_host = jaeger_config.get("host")
                    jaeger_port = jaeger_config.get("port")
                    jaeger_otlp_exporter = OTLPSpanExporter(
                        endpoint=f"http://{jaeger_host}:{jaeger_port}",
                        insecure=True
                    )
                    trace.get_tracer_provider().add_span_processor(
                        SimpleSpanProcessor(jaeger_otlp_exporter)
                    )

                honeycomb_config = app.config.get("HONEYCOMB_SETTINGS")
                if honeycomb_config.get("USE_HONEYCOMB"):
                    honeycomb_exporter = OTLPSpanExporter(
                        endpoint=honeycomb_config.get("HONEYCOMB_API"),
                        headers={
                            "x-honeycomb-team": honeycomb_config.get("HONEYCOMB_API_KEY"),
                            "x-honeycomb-dataset": honeycomb_config.get(
                                "HONEYCOMB_DATASET"
                            ),
                        },
                    )
                    trace.get_tracer_provider().add_span_processor(
                        BatchSpanProcessor(honeycomb_exporter)
                    )

                RequestsInstrumentor().instrument()
                FlaskInstrumentor().instrument_app(app)
                SQLAlchemyInstrumentor().instrument(engine=app.db.engine)
        except Exception as error:
            app.logger.error(f"OTEL instrumentation setup failed: {error}")
    return app
