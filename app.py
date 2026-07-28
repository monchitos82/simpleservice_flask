import logging
import sys

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
from opentelemetry.sdk.trace.export import SimpleSpanProcessor

from blueprints.simplistic import simplistic_bp
from logs import setup_otel_logging
from config import DevelopmentConfig
from logs import JsonFormatter


def create_app(config_class: object = DevelopmentConfig) -> object:
    root = logging.getLogger()
    root.setLevel(logging.INFO)
    use_otel = DevelopmentConfig.USE_OTEL
    json_handler = logging.StreamHandler(sys.stdout)
    json_handler.setFormatter(JsonFormatter())
    root.addHandler(json_handler)
    app = Flask(__name__)
    app.db = SQLAlchemy()
    app.config.from_object(config_class)
    app.logger = root
    app.faker = Faker()
    app.db.init_app(app)
    app.register_blueprint(simplistic_bp)
    if use_otel:
        try:
            with app.app_context():
                resource = Resource.create({"service.name": "simpleservice"})
                trace.set_tracer_provider(TracerProvider(resource=resource))
                otel_settings = app.config.get("OTEL_SETTINGS")
                if otel_settings.get("traces", False):
                    otlp_tracing_exporter = OTLPSpanExporter(
                        endpoint=f"{otel_settings["host"]}:{otel_settings["port"]}",
                        insecure=True
                    )
                    trace.get_tracer_provider().add_span_processor(
                        SimpleSpanProcessor(otlp_tracing_exporter)
                    )

                    RequestsInstrumentor().instrument()
                    FlaskInstrumentor().instrument_app(app)
                    SQLAlchemyInstrumentor().instrument(engine=app.db.engine)

                if otel_settings.get("logging", False):
                    setup_otel_logging(otel_settings)
        except Exception as error:
            app.logger.error(f"OTEL instrumentation setup failed: {error}")
    return app
