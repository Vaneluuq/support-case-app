# alembic/env.py
import os
import sys
from pathlib import Path

# Añadir el directorio 'app' al PYTHONPATH para que Alembic pueda encontrar tus módulos
# Esto asume que el comando alembic se ejecuta desde el directorio 'backend'.
sys.path.append(str(Path(__file__).resolve().parents[1] / "app"))

from app.db.session import Base
from app.core.config import settings

# Importar todos tus modelos aquí para que Alembic los detecte
# SQLAlchemy Base.metadata.bind necesita conocer todos los modelos
from app.models import support_case

from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
target_metadata = Base.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
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
    # Obtener la configuración general de Alembic
    alembic_config_section = config.get_section(config.config_ini_section)

    # Crear un diccionario de opciones para engine_from_config
    # La URL de SQLAlchemy la sacamos directamente de nuestras settings de la app
    connectable_options = {
        "url": settings.DATABASE_URL,  # <-- ¡Aquí inyectamos la URL de forma explícita!
        "poolclass": pool.NullPool,
    }

    # Pasar todas las demás opciones de sqlalchemy.* que puedan estar en alembic.ini
    # a engine_from_config. Pero aseguramos que 'url' prevalezca.
    for key, value in alembic_config_section.items():
        if key.startswith("sqlalchemy.") and key != "sqlalchemy.url":
            connectable_options[key.replace("sqlalchemy.", "")] = value

    connectable = engine_from_config(
        connectable_options, # Pasamos las opciones con la URL ya definida
        prefix="",           # No necesitamos prefix, ya que las claves están limpias
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            # Añade estas dos líneas para manejar los ENUMs de SQLAlchemy/Postgres en SQLite
            # Esto es una solución común para que Alembic no intente recrear los ENUMs
            # como tipos de DB nativos en SQLite, donde no existen.
            # Si usas Postgres, no necesitarías esto.
            compare_type=True,
            include_object=lambda obj, name, type, reflected, comparable_by_type: True if type.__class__.__name__ not in ('CaseStatus', 'CasePriority') else False,

            # version_table_schema=target_metadata.schema, # Si usas schemas en Postgres
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
