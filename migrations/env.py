"""
env.py
------------------------------------------------
Author: William Richmond
Created on: 30 June 2024
File name: env.py
Revised: [Add revised date]

Description:
This module configures the Alembic environment for database migrations.
It includes functions for running migrations in offline and online modes,
and sets up the necessary configurations for the migration process.

Usage:
    This file is used by Alembic to manage database migrations.
    It should not be executed directly.

Example:
    Run the Alembic migration commands:
    $ alembic revision --autogenerate -m "Initial migration"
    $ alembic upgrade head
"""

from __future__ import with_statement

from logging.config import fileConfig

from alembic import context
from sqlalchemy import engine_from_config, pool

# Import your models here
from app.models import *

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
target_metadata = db.metadata


def run_migrations_offline():
    """Run migrations in 'offline' mode.
    This configures the context with just a URL
    and not an Engine, though an Engine is also acceptable
    here. By skipping the Engine creation we don't even need a
    DBAPI to be available.
    Calls to context.execute() here emit the given string to the
    script output.
    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url, target_metadata=target_metadata, literal_binds=True
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Run migrations in 'online' mode.
    In this scenario we need to create an Engine
    and associate a connection with the context.
    """
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
