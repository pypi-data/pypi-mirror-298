from sqlalchemy import MetaData
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine
from sqlalchemy.sql import Select
from urllib.parse import urlparse
from database_helper.database.constants_conn import MAX_CONNECTIONS, MIN_CONNECTIONS
import logging  # Import logging for error handling


class AsyncDatabase:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(AsyncDatabase, cls).__new__(cls)
        return cls._instance

    def __init__(self, connection_string, db_type=None, pool_size=MIN_CONNECTIONS, max_overflow=MAX_CONNECTIONS,
                 logger=None):
        if not hasattr(self, "initialized"):
            self.connection_string = connection_string
            self.pool_size = pool_size
            self.max_overflow = max_overflow

            # Initialize logger
            self.logger = logger or logging.getLogger(__name__)

            # Extract the database name from the connection string
            self.current_db = self.extract_dbname()

            self.engine: AsyncEngine = None
            self.tables = {}
            self.engines = {}  # Cache engines for different databases
            self.is_connected = False
            self.initialized = True

    def extract_dbname(self):
        """
        Extract the database name from the connection string.
        Assumes the connection string is in the format '.../dbname?...'.
        """
        try:
            # Split the connection string to get the database name
            parsed_url = urlparse(self.connection_string)
            dbname = parsed_url.path.strip('/')  # Remove leading '/'
            return dbname
        except Exception as e:
            self.logger.error(f"Error extracting database name: {e}")
            return None  # Fallback if dbname extraction fails

    async def connect(self, dbname=None):
        """
        Connects to the specified database using the provided connection string.
        If no database is provided, the current connection is reused.
        """
        try:
            if dbname:
                # Check if engine for dbname exists
                if dbname in self.engines:
                    # Reuse the existing engine for this database
                    self.engine = self.engines[dbname]
                    self.current_db = dbname
                else:
                    # Create a new engine for this database using the full connection string
                    new_connection_string = self.connection_string.replace(self.current_db or '',
                                                                           dbname) if self.current_db else self.connection_string
                    self.engine = create_async_engine(
                        new_connection_string,
                        pool_size=self.pool_size,
                        max_overflow=self.max_overflow
                    )
                    self.engines[dbname] = self.engine
                    self.current_db = dbname

                self.logger.info(f"Connected to database: {dbname}")
                self.is_connected = True
            else:
                # Connect using the default connection string if no dbname is provided
                if not self.is_connected:
                    self.engine = create_async_engine(
                        self.connection_string,
                        pool_size=self.pool_size,
                        max_overflow=self.max_overflow
                    )
                    self.engines[self.current_db or 'default'] = self.engine
                    self.logger.info(f"Connected to database: {self.current_db or 'default'}")
                    self.is_connected = True
        except Exception as e:
            self.logger.error(f"Error connecting to the database: {e}")

    async def disconnect(self):
        """
        Dispose of the engine, closing all connections.
        """
        if self.engine:
            await self.engine.dispose()
            self.logger.info(f'Database {self.current_db} disconnected')
            self.is_connected = False

    async def switch_database(self, dbname):
        """
        Switches to the provided database if not already connected.
        Creates a new engine for the new database if it's not already cached.
        """
        if self.current_db == dbname:
            self.logger.info(f"Already connected to {dbname}")
            return

        self.logger.info(f"Switching to database {dbname}")
        await self.connect(dbname)

    async def initialize_tables(self, table_names, dbname=None):
        """
        Initializes metadata for tables. Optionally, it can switch databases before initializing tables.
        """
        try:
            if dbname:
                await self.switch_database(dbname)  # Switch database if required
            if not self.is_connected:
                await self.connect()
            metadata = MetaData()
            async with self.engine.connect() as connection:
                for table_name in table_names:
                    if table_name not in self.tables:
                        await connection.run_sync(metadata.reflect, only=[table_name], views=True)
                        self.tables[table_name] = metadata.tables[table_name]
            self.logger.info("Tables initialized: %s", list(self.tables.keys()))
        except Exception as e:
            self.logger.error(f"Error in initializing tables: {e}")
            raise Exception(f"Error in initializing tables: {e}")

    async def execute_query(self, query, dbname=None):
        """
        Executes a query on the specified database. Optionally switches databases if required.
        """
        try:
            if dbname:
                await self.switch_database(dbname)  # Switch database if required
            if not self.is_connected:
                await self.connect()

            async with self.engine.connect() as connection:
                result = await connection.execute(query)
                if isinstance(query, Select):
                    return result # Return all rows for select queries asynchronously
                else:
                    await connection.commit()
                    return result.rowcount  # Return number of rows affected for update/insert/delete queries
        except Exception as e:
            self.logger.error(f"Error in query execution: {e}")
            raise Exception(f"Error in query execution: {e}")

    async def __aenter__(self):
        if not self.is_connected:
            await self.connect()
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.disconnect()  # Optionally disconnect when exiting

    def get_current_db(self):
        """
        Returns the name of the currently connected database.
        """
        return self.current_db
