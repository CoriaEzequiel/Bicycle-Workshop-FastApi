from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context

# Importo base y models
from app.db.base import Base
from app.db.models import user, product, appointment, services_bike  # importa todos los modelos

# metadata para Alembic
target_metadata = Base.metadata

# Config de Alembic
config = context.config
fileConfig(config.config_file_name)

# Obtén la URL de la DB desde .env (usando settings)
from app.core.config import settings
DATABASE_URL = settings.DATABASE_URL

def run_migrations_offline():
    """Run migrations in 'offline' mode."""
    context.configure(
        url=DATABASE_URL,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Run migrations in 'online' mode."""
    connectable = engine_from_config(
        {"sqlalchemy.url": DATABASE_URL},
        prefix='',
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