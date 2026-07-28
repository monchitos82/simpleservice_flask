import os


def env_as_bool(value: str, default: bool = False) -> bool:
    """ os.getenv of a boolean will return a string that casts to True """
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
    USE_OTEL = env_as_bool("USE_OTEL")
    JAEGER_SETTINGS = {}
    HONEYCOMB_SETTINGS = {}


class DevelopmentConfig(Config):
    DEBUG = env_as_bool("DEBUG", False)
    USE_OTEL = env_as_bool("USE_OTEL", False)
    use_jaeger = env_as_bool("USE_JAEGER")
    JAEGER_SETTINGS = {
        "USE_JAEGER": env_as_bool("USE_JAEGER"),
        "host": os.getenv("JAEGER_SERVER", "host.containers.internal"),
        "port": int(os.getenv("JAEGER_PORT", 6831)),
    }
    HONEYCOMB_SETTINGS = {
        "USE_HONEYCOMB": env_as_bool("USE_HONEYCOMB"),
        "HONEYCOMB_API": os.getenv("HONEYCOMB_API", "https://api.honeycomb.io:443"),
        "HONEYCOMB_DATASET": os.getenv("HONEYCOMB_DATASET", "simpleservice"),
        "HONEYCOMB_API_KEY": os.getenv("HONEYCOMB_API_KEY", ""),
    }
    REMOTE_RANDOM_URL = os.getenv(
        "REMOTE_RANDOM_URL", "http://remote-service-fqdn/data"
    )


class TestConfig(Config):
    TESTING = True
    DEBUG = True
    USE_OTEL = False
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"  # Use SQLite for tests
    SQLALCHEMY_TRACK_MODIFICATIONS = False
