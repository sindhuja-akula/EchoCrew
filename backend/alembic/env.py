import os
import sys
from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context

# Add project root to sys.path so both `backend` and `database` packages resolve
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
# Add backend dir so `app.*` imports resolve
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.config import settings
from app.database import Base  # noqa: F401 - shared declarative Base

# Import ALL models so their tables register on Base.metadata
# Phase 1
from database.models.user import User  # noqa: F401
from database.models.garbage_report import GarbageReport  # noqa: F401
# Phase 2
from database.models.worker import Worker  # noqa: F401
from database.models.vehicle import Vehicle  # noqa: F401
from database.models.work_order import WorkOrder  # noqa: F401
from database.models.work_unit import WorkUnit  # noqa: F401
from database.models.work_assignment import WorkAssignment  # noqa: F401
from database.models.cleaning_evidence import CleaningEvidence  # noqa: F401
from database.models.verification import Verification  # noqa: F401
from database.models.compensation import Compensation  # noqa: F401
from database.models.collection_batch import CollectionBatch  # noqa: F401

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Set database connection URL from settings (overrides alembic.ini static value)
config.set_main_option("sqlalchemy.url", settings.DATABASE_URL)

target_metadata = Base.metadata


def run_migrations_offline() -> None:
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


def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
