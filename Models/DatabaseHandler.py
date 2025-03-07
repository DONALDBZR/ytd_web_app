"""
The module of the database handler which will act as the
object-relational mapper.
"""
from mysql.connector.pooling import PooledMySQLConnection
from mysql.connector.connection import MySQLConnection
from mysql.connector.cursor import MySQLCursor
from Models.Logger import Extractio_Logger, Environment
from mysql.connector.types import RowType
from typing import Union, Tuple, Any, List
from mysql.connector import connect, Error as Relational_Database_Error
from inspect import stack
from re import match


class Database_Handler:
    """
    The database handler that will communicate with the database
    server.
    """
    __host: str
    """
    The host of the application.
    """
    __database: str
    """
    The database of the application.
    """
    __username: str
    """
    The user that have access to the database.
    """
    __password: str
    """
    The password that allows the required user to connect to the
    database.
    """
    __database_handler: Union[PooledMySQLConnection, MySQLConnection]
    """
    The database handler needed to execute the queries needed.
    """
    __statement: MySQLCursor
    """
    The statement to be used to execute all of the requests to
    the database server.
    """
    __query: str
    """
    The query to be used to be sent to the database server to
    either get, post, update or delete data.
    """
    __parameters: Union[Tuple[Any], None]
    """
    Parameters that the will be used to sanitize the query which
    is either get, post, update or delete.
    """
    __Logger: Extractio_Logger
    """
    The logger that will all the action of the application.
    """

    def __init__(self):
        """
        Initializing the database connection and logging for the
        application.  This constructor sets up the logger, retrieves
        database connection parameters from the `Environment`
        instance, and attempts to establish a database connection.
        If the connection fails, an error is logged and the
        exception is raised.
        
        Raises:
            Relational_Database_Error: If the database connection fails.
        """
        self.setLogger(Extractio_Logger(__name__))
        self.__setDatabaseConnectionParameters(Environment())
        try:
            self.__connectDatabase()
            self.getLogger().inform("The application has been successfully connected to the database server!")
        except Relational_Database_Error as error:
            self.getLogger().error(f"Database Connection Failed!\nError: {error}")
            raise

    def __setDatabaseConnectionParameters(self, environment: Environment) -> None:
        """
        Setting the database connection parameters from the provided
        environment instance.  This method retrieves the database
        host, schema, username, and password from the `Environment`
        instance and assigns them to the respective internal
        attributes.

        Parameters:
            environment (Environment): An instance of the `Environment` class containing the database connection details.

        Returns:
            None
        """
        self.__setHost(environment.getDatabaseHost())
        self.__setDatabase(environment.getDatabaseSchema())
        self.__setUsername(environment.getDatabaseUsername())
        self.__setPassword(environment.getDatabasePassword())

    def __connectDatabase(self) -> None:
        """
        Establishing a connection to the database server and sets up
        the database handler.  This method uses the connection
        details retrieved from the environment to establish the
        connection to the database and initialize the database
        handler for interacting with the database.

        Returns:
            void

        Raises:
            Relational_Database_Error: If the connection to the database server fails.
        """
        self.__setDatabaseHandler(
            connect(
                host=self.__getHost(),
                database=self.__getDatabase(),
                username=self.__getUsername(),
                password=self.__getPassword(),
                connect_timeout=10
            )
        )

    def __getHost(self) -> str:
        return self.__host

    def __setHost(self, host: str) -> None:
        self.__host = host

    def __getDatabase(self) -> str:
        return self.__database

    def __setDatabase(self, database: str) -> None:
        self.__database = database

    def __getUsername(self) -> str:
        return self.__username

    def __setUsername(self, username: str) -> None:
        self.__username = username

    def __getPassword(self) -> str:
        return self.__password

    def __setPassword(self, password: str) -> None:
        self.__password = password

    def __getDatabaseHandler(self) -> Union[PooledMySQLConnection, MySQLConnection]:
        return self.__database_handler

    def __setDatabaseHandler(self, database_handler: Union[PooledMySQLConnection, MySQLConnection]) -> None:
        self.__database_handler = database_handler

    def __getStatement(self) -> MySQLCursor:
        return self.__statement

    def __setStatement(self, statement: MySQLCursor) -> None:
        self.__statement = statement

    def getQuery(self) -> str:
        return self.__query

    def setQuery(self, query: str) -> None:
        self.__query = query

    def getParameters(self) -> Union[Tuple[Any], None]:
        return self.__parameters

    def setParameters(self, parameters: Union[Tuple[Any], None]) -> None:
        self.__parameters = parameters

    def getLogger(self) -> Extractio_Logger:
        return self.__Logger

    def setLogger(self, logger: Extractio_Logger) -> None:
        self.__Logger = logger

    def _query(self, query: str, parameters: Union[Tuple[Any], None]) -> None:
        """
        Executing a database query with the provided parameters.

        This method prepares a database statement, executes the query, and logs relevant debugging information.  If an error occurs, it logs the error and raises an exception.  The database cursor is closed in the `finally` block to ensure proper resource management.

        Parameters:
            query (string): The SQL query to be executed.
            parameters (Union[Tuple[Any], None]): The parameters to be used in the query.

        Raises:
            Relational_Database_Error: If the query execution fails.

        Returns:
            void
        """
        referrer: str = stack()[1][3]
        self.getLogger().debug(f"Query to be executed!\nQuery: {query}\nParameters: {parameters}")
        try:
            self.__setStatement(
                self.__getDatabaseHandler().cursor(
                    prepared=True,
                    dictionary=True
                )
            )
            self.__getStatement().execute(query, parameters)
        except Relational_Database_Error as error:
            self.getLogger().error(f"Query Execution Failed!\nError: {error}\nQuery: {query}\nParameters: {parameters}")
            raise error
        finally:
            self._closeCursor() if referrer != "getData" else self.getLogger().warn(f"The cursor cannot be closed at the moment as it is being called to retrieve data.\nFunction: {referrer}")

    def _execute(self) -> None:
        """
        Committing the current database transaction.  If the commit
        operation is successful, an informational message is logged.
        If the commit fails, the transaction is rolled back to
        maintain data integrity, and an error message is logged.

        Raises:
            Relational_Database_Error: If the commit operation fails.

        Returns:
            void
        """
        try:
            self.__getDatabaseHandler().commit()
            self.getLogger().inform("The database transaction has been successfully committed!")
        except Relational_Database_Error as error:
            self.__getDatabaseHandler().rollback()
            self.getLogger().error(f"The database transaction has failed to be committed.  It has been rolled back.\nError: {error}")
            raise

    def _resultSet(self) -> List[RowType]:
        """
        Retrieving all rows from the executed query result set.
        This method fetches all rows from the database statement
        cursor.  If an error occurs, it logs the failure and raises
        an exception.  The cursor is always closed after execution.

        Returns:
            List[RowType]: The fetched result set from the database.

        Raises:
            Relational_Database_Error: If fetching the result set fails.
        """
        try:
            result_set: List[RowType] = self.__getStatement().fetchall()
            self.getLogger().debug("The data has been successfully retrieved!")
            return result_set
        except Relational_Database_Error as error:
            self.getLogger().error(f"Failed to retrieve data from the database.\nError: {error}")
            raise
        finally:
            self._closeCursor()

    def _closeCursor(self) -> None:
        """
        Closing the database statement cursor if it is open.  This
        method checks if the statement cursor is open by calling the
        private method `__getStatement()`.  If the cursor is open,
        it will be closed using the `close()` method.  If the cursor
        has already been closed, a warning will be logged using the
        `getLogger().warn()` method.

        Returns:
            void
        """
        if self.__getStatement():
            self.__getStatement().close()
        else:
            self.getLogger().warn("The database statement cursor has already been closed.")

    def getData(self, parameters: Union[Tuple[Any], None], table_name: str, join_condition: str = "", filter_condition: str = "", column_names: str = "*", sort_condition: str = "", limit_condition: int = 0, group_condition: str = "") -> List[RowType]:
        """
        Retrieving data from the specified database table using a SQL query.  The query is dynamically constructed based on the provided parameters, such as join conditions, filter conditions, sorting, and limits.

        This method constructs an SQL SELECT query with the following components:
        - `SELECT` clause: Specifies which columns to select.
        - `FROM` clause: Specifies the table to retrieve data from.
        - `LEFT JOIN` clause (optional): Joins the specified tables.
        - `WHERE` clause (optional): Filters the data based on the given conditions.
        - `GROUP BY` clause (optional): Groups the data based on the specified columns.
        - `ORDER BY` clause (optional): Sorts the data based on the specified columns.
        - `LIMIT` clause (optional): Limits the number of results returned.

        Parameters:
            parameters (Union[Tuple[Any], None]): The parameters to be used in the query.
            table_name (string): The name of the table to retrieve data from.
            join_condition (string, optional): The condition for joining tables.
            filter_condition (string, optional): The condition to filter results.
            column_names (string, optional): The columns to select.
            sort_condition (string, optional): The condition for sorting results.
            limit_condition (int, optional): The maximum number of results to return.
            group_condition (string, optional): The condition for grouping results.

        Returns:
            List[RowType]

        Raises:
            ValueError: If the provided conditions or parameters are invalid.
        """
        try:
            self.setQuery(f"SELECT {column_names} FROM {table_name}")
            self.setParameters(self.sanitize(parameters))
            self.setQuery(self.getQuery() if join_condition == "" else f"{self.getQuery()} LEFT JOIN {self.sanitize(join_condition)}")
            self.setQuery(self.getQuery() if filter_condition == "" else f"{self.getQuery()} WHERE {self.sanitize(filter_condition)}")
            self.setQuery(self.getQuery() if group_condition == "" else f"{self.getQuery()} GROUP BY {self.sanitize(group_condition)}")
            self.setQuery(self.getQuery() if sort_condition == "" else f"{self.getQuery()} ORDER BY {self.sanitize(sort_condition)}")
            self.setQuery(f"{self.getQuery()} LIMIT {self.sanitize(limit_condition)}" if limit_condition > 0 else self.getQuery())
            self._query(self.getQuery(), self.getParameters())
            return self._resultSet()
        except (ValueError, Relational_Database_Error) as error:
            self.getLogger().error(f"An error occurred in the relational database server.\nError: {error}")
            return []

    def postData(self, table: str, columns: str, values: str, parameters: Tuple[Any]) -> None:
        """
        Creating records to store data into the database server.

        Parameters:
            table: string: Table Name
            columns: string: Column names
            values: string: Data to be inserted

        Returns:
            void
        """
        self.setQuery(f"INSERT INTO {table}({columns}) VALUES ({values})")
        self.setParameters(parameters)
        self._query(self.getQuery(), self.getParameters())
        self._execute()

    def updateData(self, table: str, values: str, parameters: Union[Tuple[Any], None], condition: str = "") -> None:
        """
        Updating a specific table in the database.

        Parameters:
            table: string: Table name
            values: string: Columns to be modified and data to be put within
            condition: string: Condition for the data to be modified
            parameters: array: Data to be used for data manipulation.

        Returns:
            void
        """
        self.setQuery(f"UPDATE {table} SET {values}")
        self.setParameters(parameters)
        self.setQuery(self.getQuery() if condition == "" else f"{self.getQuery()} WHERE {condition}")
        self._query(self.getQuery(), self.getParameters())
        self._execute()

    def deleteData(self, table: str, parameters: Union[Tuple[Any], None], condition: str = "") -> None:
        """
        Deleting data from the database.

        Parameters:
            table: string: Table name
            parameters: array: Data to be used for data manipulation.
            condition: string: Specification

        Returns:
            void
        """
        self.setQuery(f"DELETE FROM {table}")
        self.setParameters(parameters)
        self.setQuery(self.getQuery() if condition == "" else f"{self.getQuery()} WHERE {condition}")
        self._query(self.getQuery(), self.getParameters())
        self._execute()

    def getLastRowIdentifier(self) -> Union[int, None]:
        """
        Fetching the last inserted row identifier.

        Returns:
            int
        """
        return self.__getStatement().lastrowid

    def close(self) -> None:
        """
        Attempting to close the database connection.  This method
        calls the internal `__close` method to safely close the
        database connection.  If an error occurs during the process,
        a log message is generated with the error details.

        Returns:
            void
        
        Raises:
            Relational_Database_Error: If an error occurs while closing the connection, it is logged and re-raised.
        """
        try:
            self.__close()
        except Relational_Database_Error as error:
            self.getLogger().error(f"Failed to close the database connection.\nError: {error}")
            raise

    def __close(self) -> None:
        """
        Closing the database connection if it is currently open and
        connected.  This method checks whether the database handler
        is initialized and whether the connection is active.  If the
        connection is open, it is safely closed, and a success
        message is logged.  If the connection is already closed or
        was never established, a warning is logged instead.

        Returns:
            void
        """
        if self.__getDatabaseHandler() and self.__getDatabaseHandler().is_connected():
            self.__getDatabaseHandler().close()
            self.getLogger().inform("Database connection successfully closed.")
        else:
            self.getLogger().warn("Database connection is already closed or was never established.")

    def sanitize(self, data: Any) -> Any:
        """
        Sanitizing the provided data by checking if it is a valid string or a valid non-string value.  If the data is a string, it ensures the string only contains safe characters.  If the data is invalid, it raises a ValueError.

        This method performs the following:
        1. If the data is None, it returns an empty string.
        2. If the data is not None and is not a string, it returns the data as-is.
        3. If the data is a string, it checks if it contains only safe characters (letters, 
        numbers, spaces, and certain symbols). If valid, it returns the data.
        4. If the data is invalid, it logs an error and raises a ValueError.

        Parameters:
            data (Any): The data to be sanitized.

        Returns:
            Any

        Raises:
            ValueError: If the provided string contains invalid characters.
        """
        if data is None:
            return ""
        if data is not None and not isinstance(data, str):
            return data
        if match(r"^[a-zA-Z0-9\s\-_.,:/?=<>!%+\(\)\"\']*$", data):
            return data
        self.getLogger().error("The provided value is invalid.")
        raise ValueError("The provided value is invalid.")
