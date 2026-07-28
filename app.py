import logging
import sys

from faker import Faker
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text
from sqlalchemy import exc

from blueprints.simplistic import simplistic_bp
from otel import setup_otel_logging, setup_otel_tracing
from config import DevelopmentConfig
from otel import JsonFormatter


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
                otel_settings = app.config.get("OTEL_SETTINGS")
                if otel_settings.get("traces", False):
                    setup_otel_tracing(otel_settings, app)

                if otel_settings.get("logging", False):
                    setup_otel_logging(otel_settings, app)
        except Exception as error:
            app.logger.error(f"OTEL instrumentation setup failed: {error}")

    @app.route("/health")
    def health():
        return {"status": "healthy"}, 200

    @app.route("/ready")
    def ready():
        try:
            app.db.session.execute(text("SELECT 1"))
        except exc.SQLAlchemyError:
            return {"status": "not ready"}, 503
        else:
            return {"status": "ready"}, 200

    return app
