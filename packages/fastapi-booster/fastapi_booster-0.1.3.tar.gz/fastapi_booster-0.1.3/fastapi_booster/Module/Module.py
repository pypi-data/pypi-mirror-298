from contextlib import contextmanager
from sqlalchemy import Engine, MetaData, Table, create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from fastapi import APIRouter

from fastapi_booster import logger
from fastapi_booster.ModuleManager import module_manager


class Module:
    """
    A base class for creating modules in the FastAPI Booster framework.

    This class provides functionality for managing database connections,
    handling API routes, and managing module metadata.

    Attributes:
        name (str): The name of the module.
        description (str): A brief description of the module's purpose.

    Args:
        name (str): The name of the module.
        description (str): A brief description of the module's purpose.
        sql_url (str, optional): The SQL connection URL. Defaults to "sqlite:///.db".

    Raises:
        ValueError: If a module with the same name already exists.
    """

    def __init__(
        self,
        name: str,
        description: str,
        sql_url: str = "sqlite:///.db",
    ):
        # Check if the module already exists
        if module_manager.modules.get(name):
            module_manager.modules[name] = self

        # Initialize the module
        self.name: str = name
        self.description: str = description

        # Initialize the database objects
        self._model = declarative_base()
        self._sql_url: str = sql_url
        self._sql_engine: Engine = create_engine(sql_url)
        self._sql_session = sessionmaker(
            autocommit=False, autoflush=True, bind=self._sql_engine
        )
        self._metadata: MetaData = self._model.metadata

        # Initialize the API router
        self._router = APIRouter()

        # Add the module to the module manager
        module_manager.modules[self.name] = self

    def update_all_tables_schema(self):
        """
        Updates the database schema for all tables in the module.

        This method reflects the current database schema, compares it with the
        defined schema, and makes necessary updates including creating new tables,
        adding new columns, and modifying existing columns.

        Raises:
            Exception: If there's an error during the schema update process.
        """
        metadata = MetaData()
        metadata.reflect(bind=self._sql_engine)
        for table_name, defined_table in self._metadata.tables.items():

            existing_table = metadata.tables.get(table_name)
            if existing_table is None:
                defined_table.create(self._sql_engine)
                logger.info(
                    f"\tTable {table_name} created in the database"
                )
                continue

            if existing_table is not None:
                # Table exists in the database, check for new columns and modified columns
                new_columns = [
                    column
                    for column in defined_table.columns
                    if column.name not in existing_table.columns
                ]

                modified_columns = [
                    column
                    for column in defined_table.columns
                    if column.name in existing_table.columns
                    and (
                        str(column.type) != str(existing_table.columns[column.name].type) or
                        self._foreign_keys_changed(column, existing_table.columns[column.name])
                    )
                ]

                with self._sql_engine.connect() as connection:
                    trans = connection.begin()
                    try:
                        connection.execute(
                                text(f"DROP TABLE IF EXISTS {table_name}_temp")
                            )
                        # Add new columns to the existing table
                        if new_columns:
                            columns_str = ", ".join(
                                f"ADD COLUMN {column.name} {column.type.compile(self._sql_engine.dialect)}"
                                for column in new_columns
                            )
                            connection.execute(
                                text(f"ALTER TABLE {table_name} {columns_str}")
                            )
                            logger.info(
                                f"\tNew columns {[column.name for column in new_columns]} added to table {table_name}"
                            )
                        # Modify existing columns if the type has changed
                        if modified_columns:
                            # Create a temporary table with the new schema
                            temp_table_name = f"{table_name}_temp"
                            defined_table.name = temp_table_name
                            defined_table.create(self._sql_engine)
                            logger.debug(f"\tTable {table_name}_temp created")
                            defined_table.name = table_name
                            # Copy data from the old table to the new table, excluding the modified columns
                            columns = [
                                col.name
                                for col in existing_table.columns
                                if col.name not in [col.name for col in modified_columns]
                            ]
                            columns_str = ", ".join(columns)
                            connection.execute(
                                text(
                                    f"INSERT INTO {temp_table_name} ({columns_str}) SELECT {columns_str} FROM {table_name}"
                                )
                            )
                            logger.debug(f"\tData copied from {table_name} to {temp_table_name}")
                            # Drop the old table and rename the new table
                            connection.execute(text(f"DROP TABLE {table_name}"))
                            logger.debug(f"\tTable {table_name} dropped")
                            connection.execute(
                                text(
                                    f"ALTER TABLE {temp_table_name} RENAME TO {table_name}"
                                )
                            )
                            logger.debug(f"\tTable {temp_table_name} renamed to {table_name}")
                            connection.execute(
                                text(f"DROP TABLE IF EXISTS {table_name}_temp")
                            )
                            logger.debug(f"\tTable {table_name}_temp dropped")
                            logger.info(
                                f"\tTable {table_name} updated on columns {[column.name for column in modified_columns]}"
                            )
                        trans.commit()
                    except Exception as e:
                        trans.rollback()
                        logger.error(f"Error updating table {table_name}: {e}")
                        raise

        # Reflect the new schema in the metadata
        self._metadata.clear()
        self._metadata.reflect(bind=self._sql_engine)

    def _foreign_keys_changed(self, new_column, existing_column):
        """
        Checks if the foreign keys of a column have changed.

        Args:
            new_column: The new column definition.
            existing_column: The existing column in the database.

        Returns:
            bool: True if foreign keys have changed, False otherwise.
        """
        new_fks = {fk.target_fullname for fk in new_column.foreign_keys}
        existing_fks = {fk.target_fullname for fk in existing_column.foreign_keys}
        return new_fks != existing_fks

    @contextmanager
    def db_session(self):
        """
        A context manager for database sessions.

        Yields:
            Session: A SQLAlchemy session object.

        Raises:
            Exception: If there's an error during the session.
        """
        db: Session = self._sql_session()
        try:
            yield db
        finally:
            db.close()

    def db(self):
        """
        A generator for database sessions.

        Yields:
            Session: A SQLAlchemy session object.
        """
        with self.db_session() as db:
            yield db

    @property
    def router(self):
        """
        Gets the FastAPI router for this module.

        Returns:
            APIRouter: The FastAPI router associated with this module.
        """
        return self._router

    @property
    def model(self):
        """
        Gets the SQLAlchemy model base for this module.

        Returns:
            DeclarativeMeta: The SQLAlchemy declarative base for defining models.
        """
        return self._model