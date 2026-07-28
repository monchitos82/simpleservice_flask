import os
from logging.config import fileConfig

from alembic import context
from sqlalchemy import engine_from_config, pool

from models import Base

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)


DATABASE_USER = os.getenv("DATABASE_USER", "simpleservice")
DATABASE_NAME = os.getenv("DATABASE_NAME", "simpleservice")
DATABASE_PASS = os.getenv("DATABASE_PASS", "simpleservice")
DATABASE_PORT = int(os.getenv("DATABASE_PORT", 5432))
DATABASE_HOST = os.getenv("DATABASE_HOST", "localhost")
SQLALCHEMY_DATABASE_URI = os.getenv(
    "SQLALCHEMY_DATABASE_URI",
    (
        f"postgresql+psycopg2://{DATABASE_USER}:{DATABASE_PASS}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}"
    ),
)


config.set_main_option("sqlalchemy.url", SQLALCHEMY_DATABASE_URI)

target_metadata = Base.metadata


def run_migrations_offline():
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Run migrations in 'online' mode."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()

