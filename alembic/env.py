from logging.config import fileConfig

from sqlalchemy import create_engine, pool
from sqlalchemy.engine import make_url

from alembic import context

# Alembic Config object — access values from alembic.ini
config = context.config

# Set up Python logging from the ini file
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# ---------------------------------------------------------------------------
# Import settings AFTER logging setup so any import-time log calls are fine.
# We intentionally do NOT push the URL into configparser (set_main_option)
# because configparser uses % for interpolation, which breaks URLs that
# contain percent-encoded characters (e.g. %40 for @, %23 for #).
# ---------------------------------------------------------------------------
from features.core.config import settings  # noqa: E402

# Import Base and all models so autogenerate can detect schema changes
from features.core.database import Base  # noqa: E402, F401
import features.core.models  # noqa: E402, F401  — registers models on Base

target_metadata = Base.metadata


def get_url():
    """Return a SQLAlchemy URL object parsed from settings.

    Using make_url() ensures that percent-encoded characters in the password
    (e.g. %40 → @) are handled by SQLAlchemy's own URL parser rather than
    being touched by configparser's interpolation engine.
    """
    return make_url(settings.database_url)


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode (no live DB connection needed)."""
    context.configure(
        url=get_url(),
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode (live DB connection)."""
    connectable = create_engine(
        get_url(),
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
