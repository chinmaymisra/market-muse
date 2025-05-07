from logging.config import fileConfig
import os
from alembic import context
from sqlalchemy import engine_from_config, pool
from dotenv import load_dotenv
from sqlalchemy import pool




# Load environment variables from .env
load_dotenv()

# This is the Alembic Config object
config = context.config
config.set_main_option("sqlalchemy.url", os.getenv("DATABASE_URL"))

# Optional: Inject DB URL from .env
db_url = os.getenv("DATABASE_URL")
if db_url:
    config.set_main_option("sqlalchemy.url", db_url)

# Set up loggers
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# ✅ Import your SQLAlchemy Base and models
from app.database import Base
from app.models import user, stock_cache  # import all models to register them

# ✅ Let Alembic generate schema diffs
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
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
