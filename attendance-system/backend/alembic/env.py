import asyncio
from logging.config import fileConfig

from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import create_async_engine

from alembic import context
from alembic.autogenerate import renderers
from pgvector.sqlalchemy import Vector

# Tell Alembic how to render Vector columns in migrations
@renderers.dispatch_for(Vector)
def render_vector(type_, autogen_context):
    # Ensure the import is added to the migration
    autogen_context.imports.add("from pgvector.sqlalchemy import Vector")
    return f"Vector(dim={type_.dim})"

# Import the centralized URL function and the Base for models
from db.base import get_database_url, Base
from db.models.account import Account
from db.models.user import User
from db.models.attendance import Attendance
from db.models.student_profile import StudentProfile

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Set the models' metadata for autogenerate support
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    url = get_database_url()
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection: Connection) -> None:
    context.configure(connection=connection, target_metadata=target_metadata)

    with context.begin_transaction():
        context.run_migrations()


async def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    
    # Get the URL from our centralized function
    url = get_database_url()

    # Manually create the async engine to ensure correct settings
    connectable = create_async_engine(
        url,
        poolclass=pool.NullPool,
        connect_args={"statement_cache_size": 0}, # For Supabase transaction pooler
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


if context.is_offline_mode():
    run_migrations_offline()
else:
    asyncio.run(run_migrations_online())