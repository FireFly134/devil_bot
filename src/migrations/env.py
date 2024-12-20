"""Generated alembic env file.
Modified to read data from ENV variables instead of static config file
"""
import logging
from logging.config import fileConfig
from typing import Dict, Union

from alembic import context
from sqlalchemy import engine_from_config, pool
from sqlalchemy.engine import Engine

from src import migrations
from src.config import DB_URL
from src.tables import pg_tables  # pyling: disable=unused-import

# todo исправить тип
ENGINE = Dict[str, Union[Dict[str, Engine], Dict[str, Dict[str, Engine]]]]
USE_TWOPHASE: bool = False

CONFIG = context.config

fileConfig(CONFIG.config_file_name)
LOGGER = logging.getLogger("alembic.env")

TARGET_METADATA = {"write": migrations.METADATA}


def run_migrations_offline():
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    # for the --sql use case, run migrations for each URL into
    # individual files.
    engines = {
        "write": {"url": DB_URL},
    }

    for name, rec in engines.items():
        LOGGER.info("Migrating database %s", name)
        file_ = "%s.sql" % name
        LOGGER.info("Writing output to %s", file_)
        with open(file_, "w") as buffer:
            context.configure(
                url=rec["url"],
                output_buffer=buffer,
                target_metadata=TARGET_METADATA.get(name),
                literal_binds=True,
                dialect_opts={"paramstyle": "named"},
            )
            with context.begin_transaction():
                context.run_migrations(engine_name=name)


def run_migrations_online():
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """

    # for the direct-to-DB use case, start a transaction on all
    # engines, then run all migrations, then commit all transactions.

    engines = {
        "write": {
            "engine": engine_from_config(
                {
                    "sqlalchemy.url": DB_URL,
                },
                prefix="sqlalchemy.",
                poolclass=pool.NullPool,
            )
        },
    }

    for name, rec in engines.items():
        engine: Engine = rec["engine"]
        rec["connection"] = conn = engine.connect()

        if USE_TWOPHASE:
            rec["transaction"] = conn.begin_twophase()
        else:
            rec["transaction"] = conn.begin()

    def commit_transaction(engines: ENGINE, is_twophase: bool):
        if is_twophase:
            for rec in engines.values():
                rec["transaction"].prepare()

        for rec in engines.values():
            rec["transaction"].commit()

    try:
        for name, rec in engines.items():
            LOGGER.info("Migrating database %s", name)
            context.configure(
                connection=rec["connection"],
                upgrade_token="%s_upgrades" % name,
                downgrade_token="%s_downgrades" % name,
                target_metadata=TARGET_METADATA.get(name),
            )
            context.run_migrations(engine_name=name)

            commit_transaction(engines, USE_TWOPHASE)
    except:
        for rec in engines.values():
            rec["transaction"].rollback()
        raise
    finally:
        for rec in engines.values():
            rec["connection"].close()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
