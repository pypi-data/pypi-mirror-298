from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy import create_engine, text, select
from sqlalchemy.orm import sessionmaker, declarative_base
import logging
import pkg_resources
import importlib
import os
import psycopg2

# Create a base class for models to inherit from
Base = declarative_base()

def ensure_database_exists(database_url):
    """Ensure that the database exists. If it doesn't, create it."""
    db_info = _parse_database_url(database_url)
    system_db_url = f"postgresql://{db_info['user']}:{db_info['password']}@{db_info['host']}:{db_info['port']}/postgres"

    try:
        engine = create_engine(system_db_url)
        conn = engine.connect()

        # Check if the database exists
        result = conn.execute(text(f"SELECT 1 FROM pg_database WHERE datname = '{db_info['dbname']}'"))
        exists = result.fetchone() is not None

        if not exists:
            conn.execute(text(f"CREATE DATABASE {db_info['dbname']}'"))
            logging.info(f"Database '{db_info['dbname']}' created.")
        else:
            logging.info(f"Database '{db_info['dbname']}' already exists.")

        conn.close()
    except Exception as e:
        logging.error(f"Error while ensuring database exists: {e}")
    finally:
        engine.dispose()

def _parse_database_url(database_url):
    """Parse the database URL to extract components (user, password, host, port, dbname)."""
    connection_params = psycopg2.extensions.parse_dsn(database_url)
    return {
        "user": connection_params.get("user"),
        "password": connection_params.get("password"),
        "host": connection_params.get("host"),
        "port": connection_params.get("port"),
        "dbname": connection_params.get("dbname"),
    }

async def setup_database(bot):
    """Set up the database connection and import models from all plugins."""
    database_url = f"postgresql+asyncpg://{bot.config['database']['user']}:" \
                   f"{bot.config['database']['password']}@{bot.config['database']['host']}" \
                   f":{bot.config['database']['port']}/{bot.config['database']['database']}"

    # Ensure that the database exists
    ensure_database_exists(database_url.replace('+asyncpg', ''))

    # Create the async database engine
    engine = create_async_engine(database_url, echo=True)

    # Create a session factory for the bot
    bot.db_session = sessionmaker(
        engine, expire_on_commit=False, class_=AsyncSession
    )

    # Discover and import all models from installed plugins and modules/dev
    _discover_and_import_models()

    # Create all tables in the database (if they don't already exist)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    bot.engine = engine

def _discover_and_import_models():
    """Automatically discover and import models from both installed plugins and modules/dev."""
    logger = logging.getLogger("database")
    logger.info("Discovering and importing models from installed plugins and local modules...")
    # Load models from modules
    # Loop through folders in modules/ and load all .py files that don't start with __init__
    for folders in os.listdir('modules'):
        if os.path.isdir(folders):
            _import_local_models(f'modules.{folders}')

    # Load models from installed plugins (pip-installed)
    for dist in pkg_resources.working_set:
        if dist.project_name.startswith("obyn-"):  # Assuming plugin naming convention
            plugin_name = dist.project_name.replace("obyn-", "")
            _import_plugin_models(f"{plugin_name}")

def _import_local_models(module_name):
    """Import models from a local module like modules/dev."""
    logger = logging.getLogger("database")
    try:
        models_module = importlib.import_module(f"{module_name}.models")
        logger.info(f"Imported models from {module_name}")
    except ModuleNotFoundError:
        logger.warning(f"No models found in {module_name}")
    except Exception as e:
        logger.error(f"Failed to import models from {module_name}: {e}")

def _import_plugin_models(plugin_name):
    """Import models from a pip-installed plugin."""
    logger = logging.getLogger("database")
    try:
        models_module = importlib.import_module(f"{plugin_name}.models")
        logger.info(f"Imported models from {plugin_name}")
    except ModuleNotFoundError:
        logger.warning(f"No models found in {plugin_name}")
    except Exception as e:
        logger.error(f"Failed to import models from {plugin_name}: {e}")


# Utility functions for database interactions
async def get_record(session: AsyncSession, model, **filters):
    """
    Retrieve a single record that matches the filters.

    :param session: AsyncSession object.
    :param model: SQLAlchemy model class.
    :param filters: Filter conditions (as keyword arguments).
    :return: The first matching record or None.
    """
    async with session.begin():
        query = select(model).filter_by(**filters)
        result = await session.execute(query)
        return result.scalar()

async def get_all_records(session: AsyncSession, model, **filters):
    """
    Retrieve all records that match the filters.

    :param session: AsyncSession object.
    :param model: SQLAlchemy model class.
    :param filters: Filter conditions (as keyword arguments).
    :return: List of matching records.
    """
    async with session.begin():
        query = select(model).filter_by(**filters)
        result = await session.execute(query)
        return result.scalars().all()

async def set_record(session: AsyncSession, model, data: dict):
    """
    Insert a new record into the database.

    :param session: AsyncSession object.
    :param model: SQLAlchemy model class.
    :param data: A dictionary of field values for the new record.
    :return: The newly created record.
    """
    async with session.begin():
        new_record = model(**data)
        session.add(new_record)
        await session.commit()
        return new_record

async def update_record(session: AsyncSession, model, filters: dict, data: dict):
    """
    Update an existing record in the database.

    :param session: AsyncSession object.
    :param model: SQLAlchemy model class.
    :param filters: A dictionary of filter conditions to find the record.
    :param data: A dictionary of field values to update.
    :return: The updated record or None if not found.
    """
    async with session.begin():
        query = select(model).filter_by(**filters)
        result = await session.execute(query)
        record = result.scalar()

        if record:
            for key, value in data.items():
                setattr(record, key, value)
            await session.commit()
            return record
        return None

async def delete_record(session: AsyncSession, model, **filters):
    """
    Delete a record from the database that matches the filters.

    :param session: AsyncSession object.
    :param model: SQLAlchemy model class.
    :param filters: Filter conditions (as keyword arguments).
    :return: True if deletion was successful, False otherwise.
    """
    async with session.begin():
        query = select(model).filter_by(**filters)
        result = await session.execute(query)
        record = result.scalar()

        if record:
            await session.delete(record)
            await session.commit()
            return True
        return False