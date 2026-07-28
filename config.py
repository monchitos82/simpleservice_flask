import os


def env_as_bool(value: str, default: bool = False) -> bool:
    """os.getenv of a boolean will return a string that casts to True"""
    str_val = os.getenv(value, "False")
    if str_val.lower() == "true":
        return True
    return False


class Config:
    DEBUG = False
    TESTING = False
    LOGFILE = ""
    REMOTE_RANDOM_URL = os.getenv("REMOTE_RANDOM_URL", "http://localhost/data")
    DATABASE_USER = os.getenv("DATABASE_USER", "user")
    DATABASE_NAME = os.getenv("DATABASE_NAME", "simpleservice")
    DATABASE_PASS = os.getenv("DATABASE_PASS", "")
    DATABASE_PORT = int(os.getenv("DATABASE_PORT", 5432))
    DATABASE_HOST = os.getenv("DATABASE_HOST", "host.containers.internal")
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "SQLALCHEMY_DATABASE_URI",
        (
            f"postgresql+psycopg2://{DATABASE_USER}:{DATABASE_PASS}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}"
        ),
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = bool(
        os.getenv("SQLALCHEMY_TRACK_MODIFICATIONS", False)
    )
    USE_OTEL = env_as_bool("USE_OTEL", False)


class DevelopmentConfig(Config):
    DEBUG = env_as_bool("DEBUG", False)
    USE_OTEL = env_as_bool("USE_OTEL", False)
    OTEL_SETTINGS = {
        "service_name": "simpleservice_flask",
        "host": os.getenv("OTEL_SERVER", "host.containers.internal"),
        "port": os.getenv("OTEL_PORT", 6831),
        "traces": True,
        "logging": True,
        "metrics": True,
    }
    REMOTE_RANDOM_URL = os.getenv(
        "REMOTE_RANDOM_URL", "http://remote-service-fqdn/data"
    )
    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_size": 30,
        "max_overflow": 10,
        "echo": True,
        "pool_recycle": 3600
    }


class TestConfig(Config):
    TESTING = True
    DEBUG = True
    USE_OTEL = False
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"  # Use SQLite for tests
    SQLALCHEMY_TRACK_MODIFICATIONS = False
