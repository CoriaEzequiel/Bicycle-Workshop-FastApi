from logging.config import fileConfig
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.pool import NullPool
from alembic import context
from dotenv import load_dotenv
import os
import asyncio


load_dotenv()

import sys
#( Agrego la ruta del proyecto al sys.path)
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


# (Import settings to get DATABASE_URL)
from app.core.config import settings

# Import base and models
from app.db.base import Base
from app.db.models import user, product, services_bike, user_role # importa todos los modelos


DATABASE_URL = str(settings.DATABASE_URL)

# metadata para Alembic
target_metadata = Base.metadata

# Config de Alembic
config = context.config
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Setéo la URL para Alembic
config.set_main_option('sqlalchemy.url', DATABASE_URL)

def run_migrations_offline():
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(url=url, target_metadata=target_metadata, literal_binds=True)

    with context.begin_transaction():
        context.run_migrations()

def do_run_migrations(connection):
    context.configure(connection=connection, target_metadata=target_metadata)

    with context.begin_transaction():
        context.run_migrations()

async def run_migrations_online():
    """Run migrations in 'online' mode."""
    connectable = create_async_engine(DATABASE_URL, poolclass=NullPool)

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

if context.is_offline_mode():
    run_migrations_offline()
else:
    asyncio.run(run_migrations_online())