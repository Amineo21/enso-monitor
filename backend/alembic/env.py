
import os
from pathlib import Path
from logging.config import fileConfig

from alembic import context
from dotenv import load_dotenv
from sqlalchemy import engine_from_config, pool

from app.db.base import Base
from app.db import models  # Charge les modèles dans les métadonnées


# Configuration Alembic
config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)


# Chargement du .env situé à la racine du projet
ROOT_DIR = Path(__file__).resolve().parents[2]
load_dotenv(ROOT_DIR / ".env")

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL est absente du fichier .env")


# URL de connexion
config.set_main_option(
    "sqlalchemy.url",
    DATABASE_URL.replace("%", "%%")
)


# Métadonnées SQLAlchemy
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """Génération des migrations sans connexion directe."""

    url = config.get_main_option("sqlalchemy.url")

    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Exécution des migrations avec une connexion."""

    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
