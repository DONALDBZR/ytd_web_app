"""
The Module provides a class to handle database operations such as connecting, executing queries, and managing transactions.

Author:
    Darkness4869
"""

from mysql.connector.connection import MySQLConnection
from mysql.connector.cursor import MySQLCursor
from Models.Logger import Extractio_Logger
from Environment import Environment
from mysql.connector.types import RowType
from typing import Tuple, Any, List, Optional
from mysql.connector import connect, Error as Relational_Database_Error
from Models.DataSanitizer import Data_Sanitizer


class Database_Handler:
    """
    A class to handle database operations such as connecting, executing queries, and managing transactions.
    
    Attributes:
        __logger (Extractio_Logger): A logger instance for logging database operations and errors.
        __env (Environment): An instance of the Environment class to retrieve database connection parameters.
        __connection (MySQLConnection): The MySQL connection object used to interact with the database.
        __cursor (Optional[MySQLCursor]): The MySQL cursor object used to execute database queries.
        __sanitizer (Data_Sanitizer): An instance of Data_Sanitizer for sanitizing user input data to prevent SQL injection attacks and ensure safe string usage.

    Methods:
        __connect() -> MySQLConnection: Establishes a connection to the MySQL database.
        _execute(query: str, parameters: Optional[Tuple[Any, ...]] = None) -> None: Executes a SQL query with optional parameters.
        _closeCursor() -> None: Closes the current cursor if it exists.
        _commit() -> None: Commits the current transaction to the database.
        _fetchAll() -> List[RowType]: Fetches all rows from the last executed query.
        _closeConnection() -> None: Closes the database connection.
        __sanitizeParameters(parameters: Optional[Tuple[Any, ...]]) -> Optional[Tuple[Any, ...]]: Sanitizes the parameters using the Data_Sanitizer instance.
        getData(query: str, parameters: Optional[Tuple[Any, ...]] = None) -> List[RowType]: Fetches data from the database by executing a query with optional parameters.
        postData(query: str, parameters: Optional[Tuple[Any, ...]] = None) -> bool: Posts data to the database by executing a query with optional parameters.
        updateData(query: str, parameters: Optional[Tuple[Any, ...]] = None) -> bool: Updates data in the database by executing a query with optional parameters.
        deleteData(query: str, parameters: Optional[Tuple[Any, ...]] = None) -> bool: Deletes data from the database by executing a query with optional parameters.
        createTable(query: str, parameters: Optional[Tuple[Any, ...]] = None) -> bool: Creates a table in the database by executing a query with optional parameters.
    """
    __logger: Extractio_Logger
    """
    A logger instance for logging database operations and errors.
    """
    __env: Environment
    """
    An instance of the Environment class to retrieve database connection parameters.
    """
    __connection: MySQLConnection
    """
    The MySQL connection object used to interact with the database.
    """
    __cursor: Optional[MySQLCursor]
    """
    The MySQL cursor object used to execute database queries.
    """
    __sanitizer: Data_Sanitizer
    """
    An instance of Data_Sanitizer for sanitizing user input data to prevent SQL injection attacks and ensure safe string usage.
    """

    def __init__(
        self,
        logger: Optional[Extractio_Logger] = None,
        environment: Optional[Environment] = None,
        sanitizer: Optional[Data_Sanitizer] = None
    ):
        """
        Initializing the database handler.

        Args:
            logger (ExtractioLogger): Logger instance.
            environment (Environment): Environment instance for DB config.
            sanitizer (Data_Sanitizer): Data sanitizer instance for sanitizing user input data.

        Raises:
            RelationalDatabaseError: If the database connection fails.
        """
        self.setLogger(logger or Extractio_Logger(__name__))
        self.setEnv(environment or Environment())
        self.setConnection(self.__connect())
        self.setCursor(None)
        self.setSanitizer(sanitizer or Data_Sanitizer())

    def getLogger(self) -> Extractio_Logger:
        return self.__logger

    def setLogger(self, logger: Extractio_Logger) -> None:
        self.__logger = logger

    def getEnv(self) -> Environment:
        return self.__env

    def setEnv(self, env: Environment) -> None:
        self.__env = env

    def getConnection(self) -> MySQLConnection:
        return self.__connection

    def setConnection(self, connection: MySQLConnection) -> None:
        self.__connection = connection

    def getCursor(self) -> Optional[MySQLCursor]:
        return self.__cursor

    def setCursor(self, cursor: Optional[MySQLCursor]) -> None:
        self.__cursor = cursor

    def getSanitizer(self) -> Data_Sanitizer:
        return self.__sanitizer

    def setSanitizer(self, sanitizer: Data_Sanitizer) -> None:
        self.__sanitizer = sanitizer

    def __sanitizeParameters(self, parameters: Optional[Tuple[Any, ...]]) -> Optional[Tuple[Any, ...]]:
        """
        Sanitizing a tuple of parameters using the `Data_Sanitizer` instance.

        This method processes each parameter in the provided tuple through the `Data_Sanitizer`'s `sanitize` method, ensuring that all parameters are safe for use in database operations.  If the parameter tuple is `None`, it returns `None`.

        Args:
            parameters (Optional[Tuple[Any, ...]]): A tuple of parameters to be sanitized.

        Returns:
            Optional[Tuple[Any, ...]]: A tuple of sanitized parameters, or `None` if input is `None`.

        Raises:
            Relational_Database_Error: If any parameter fails the sanitization process.
        """
        try:
            if parameters is None:
                return None
            return tuple(self.getSanitizer().sanitize(parameter) for parameter in parameters)
        except ValueError as error:
            self.getLogger().error(f"The database handler has failed to sanitize the parameters. - Parameters: {parameters} - Error: {error}")
            raise Relational_Database_Error(str(error))

    def __connect(self) -> MySQLConnection:
        """
        Establishing a connection to the MySQL database using the provided environment configuration.

        Returns:
            MySQLConnection: The established MySQL connection object.

        Raises:
            Relational_Database_Error: If the connection to the database fails.
        """
        try:
            connection: MySQLConnection = connect(
                host=self.getEnv().getDatabaseHost(),
                user=self.getEnv().getDatabaseUsername(),
                password=self.getEnv().getDatabasePassword(),
                database=self.getEnv().getDatabaseSchema()
            ) # type: ignore
            self.getLogger().inform("The application has successfully connected to the database.")
            return connection
        except Relational_Database_Error as error:
            self.getLogger().error(f"The application has failed to connect to the database. - Error: {error}")
            raise error

    def __ensureConnection(self) -> None:
        """
        Ensuring the database connection is active.

        This method checks if the database connection is active.  If no connection is present, it establishes a new connection.  If the connection is inactive, it attempts to reconnect up to 3 times with a 2-second delay between attempts.  Logs the outcome of the connection check and reconnection attempts.
        """
        if self.getConnection() is None:
            self.setConnection(self.__connect())
            self.getLogger().inform("The database handler has successfully reconnected to the database.")
            return
        if not self.getConnection().is_connected():
            self.getConnection().reconnect(
                attempts=3,
                delay=2
            )
            self.getLogger().inform("The database handler has successfully reconnected to the database.")
            return
        self.getLogger().inform("The database handler is already connected to the database.")

    def _execute(
        self,
        query: str,
        parameters: Optional[Tuple[Any, ...]] = None
    ) -> None:
        """
        Executing a SQL query with optional parameters.

        This method does the following:
            1. Ensures that the database connection is active.
            2. Establishes a new cursor.
            3. Executes the provided SQL query with optional parameters.
            4. Raises a `Relational_Database_Error` when the execution fails.

        Args:
            query (str): The SQL query to execute.
            parameters (Optional[Tuple[Any, ...]]): Parameters for the SQL query.

        Raises:
            Relational_Database_Error: If the execution of the query fails.
        """
        try:
            self.__ensureConnection()
            self.setCursor(
                self.getConnection().cursor( # type: ignore
                    prepared=True,
                    dictionary=True
                )
            )
            self.getCursor().execute(query, self.__sanitizeParameters(parameters)) # type: ignore
        except Relational_Database_Error as error:
            self.getLogger().error(f"The database handler has failed to execute the query. - Query: {query} - Parameters: {parameters} - Error: {error}")
            raise error

    def closeCursor(self) -> None:
        """
        Closing the current cursor if it exists.

        Raises:
            Relational_Database_Error: If the cursor closing operation fails.
        """
        if self.getCursor() is None:
            return
        try:
            self.getCursor().close() # type: ignore
            self.getLogger().inform("The database handler has successfully closed the cursor.")
            self.setCursor(None)
        except Relational_Database_Error as error:
            self.getLogger().error(f"The database handler has failed to close the cursor. - Error: {error}")
            raise error

    def _commit(self) -> None:
        """
        Committing the current database transaction.

        This method commits the current transaction.  If an error occurs during the commit operation, the transaction is rolled back.

        Raises:
            Relational_Database_Error: If the commit operation fails.
        """
        try:
            self.getConnection().commit()
            self.getLogger().inform("The transaction has been successfully committed.")
        except Relational_Database_Error as error:
            self.getConnection().rollback()
            self.getLogger().error(f"The database handler has failed to commit the transaction, hence, the trasaction will roolback. - Error: {error}")
            raise error

    def _fetchAll(self) -> List[RowType]:
        """
        Fetching all rows from the last executed query.

        Returns:
            List[RowType]: A list of rows returned by the last executed query.

        Raises:
            Relational_Database_Error: If fetching rows fails.
        """
        if self.getCursor() is None:
            raise Relational_Database_Error("No cursor available to fetch data.")
        try:
            response: List[RowType] = self.getCursor().fetchall() # type: ignore
            self.getLogger().inform(f"The database handler has successfully fetched the required data.")
            return response
        except Relational_Database_Error as error:
            self.getLogger().error(f"The database handler has failed to fetch all rows. - Error: {error}")
            raise error

    def closeConnection(self) -> None:
        """
        Closing the database connection.

        This method closes the established database connection.  If the connection is already closed, it logs a warning message.

        Raises:
            Relational_Database_Error: If the connection closing operation fails.
        """
        if not self.getConnection().is_connected():
            self.getLogger().warn("The database connection is already closed.")
            return
        try:
            self.getConnection().close()
            self.getLogger().inform("The database handler has successfully closed the connection.")
        except Relational_Database_Error as error:
            self.getLogger().error(f"The database handler has failed to close the connection. - Error: {error}")
            raise error

    def getData(
        self,
        query: str,
        parameters: Optional[Tuple[Any, ...]] = None
    ) -> List[RowType]:
        """
        Fetching data from the database by executing a query with optional parameters.

        This method does the following:
            1. Executes the provided SQL query with optional parameters.
            2. Returns a list of rows returned by the query.
            3. Returning an empty list when the execution fails.

        Args:
            query (str): The SQL query to execute.
            parameters (Optional[Tuple[Any, ...]]): Parameters for the SQL query.

        Returns:
            List[RowType]: A list of rows returned by the query.
        """
        try:
            self._execute(query, parameters)
            response: List[RowType] = self._fetchAll()
            return response
        except Relational_Database_Error as error:
            self.getLogger().error(f"The database handler has failed to get data. - Query: {query} - Parameters: {parameters} - Error: {error}")
            return []

    def _manipulateData(
        self,
        query: str,
        parameters: Optional[Tuple[Any, ...]] = None
    ) -> bool:
        """
        Executing the provided SQL query with optional parameters and committing the changes.

        This method does the following:
            1. Executes the provided SQL query with optional parameters.
            2. Commits the changes.
            3. Returns True if the operation is successful, False otherwise.

        Args:
            query (str): The SQL query to execute.
            parameters (Optional[Tuple[Any, ...]]): Parameters for the SQL query.

        Returns:
            bool: True if the operation is successful, False otherwise.
        """
        try:
            self._execute(query, parameters)
            self._commit()
            return True
        except Relational_Database_Error as error:
            self.getLogger().error(f"The database handler has failed to post data. - Query: {query} - Parameters: {parameters} - Error: {error}")
            return False

    def postData(
        self,
        query: str,
        parameters: Optional[Tuple[Any, ...]] = None
    ) -> bool:
        """
        Posting data to the database by executing a query with optional parameters.

        Args:
            query (str): The SQL query to execute.
            parameters (Optional[Tuple[Any, ...]]): Parameters for the SQL query.

        Returns:
            bool: True if the operation is successful, False otherwise.
        """
        return self._manipulateData(query, parameters)

    def updateData(
        self,
        query: str,
        parameters: Optional[Tuple[Any, ...]] = None
    ) -> bool:
        """
        Updating data in the database by executing a query with optional parameters.

        Args:
            query (str): The SQL query to execute.
            parameters (Optional[Tuple[Any, ...]]): Parameters for the SQL query.

        Returns:
            bool: True if the operation is successful, False otherwise.
        """
        return self._manipulateData(query, parameters)

    def deleteData(
        self,
        query: str,
        parameters: Optional[Tuple[Any, ...]] = None
    ) -> bool:
        """
        Deleting data from the database by executing a query with optional parameters.

        Args:
            query (str): The SQL query to execute.
            parameters (Optional[Tuple[Any, ...]]): Parameters for the SQL query.

        Returns:
            bool: True if the operation is successful, False otherwise.
        """
        return self._manipulateData(query, parameters)

    def createTable(
        self,
        query: str,
        parameters: Optional[Tuple[Any, ...]] = None
    ) -> bool:
        """
        Creating a table in the database by executing a query with optional parameters.

        Args:
            query (str): The SQL query to execute.
            parameters (Optional[Tuple[Any, ...]]): Parameters for the SQL query.

        Returns:
            bool: True if the operation is successful, False otherwise.
        """
        return self._manipulateData(query, parameters)
