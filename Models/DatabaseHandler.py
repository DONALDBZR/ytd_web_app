from mysql.connector.pooling import PooledMySQLConnection
from mysql.connector.connection import MySQLConnection
from mysql.connector.abstracts import MySQLConnectionAbstract, MySQLCursorAbstract
from mysql.connector.cursor import MySQLCursor
from Models.Logger import Extractio_Logger
from Environment import Environment
from mysql.connector.types import RowType
from typing import Union, Tuple, Any, List, Optional
from mysql.connector import connect, Error as Relational_Database_Error
from inspect import stack
from re import match


class Database_Handler:
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

    def __init__(
        self,
        logger: Optional[Extractio_Logger] = None,
        environment: Optional[Environment] = None
    ):
        """
        Initializing the database handler.

        Args:
            logger (ExtractioLogger): Logger instance.
            environment (Environment): Environment instance for DB config.

        Raises:
            RelationalDatabaseError: If the database connection fails.
        """
        self.setLogger(logger or Extractio_Logger(__name__))
        self.setEnv(environment or Environment())
        self.setConnection(self.__connect())
        self.setCursor(None)

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
            self.getLogger().error(f"The application has failed to connect to the database.\nError: {error}")
            raise error

    def _execute(
        self,
        query: str,
        parameters: Optional[Tuple[Any, ...]] = None
    ) -> None:
        """
        Executing a SQL query with optional parameters.

        Args:
            query (str): The SQL query to execute.
            parameters (Optional[Tuple[Any, ...]]): Parameters for the SQL query.

        Raises:
            Relational_Database_Error: If the execution of the query fails.
        """
        if self.getCursor() is None:
            self.setCursor(
                self.getConnection().cursor(
                    prepared=True,
                    dictionary=True
                )
            )
        try:
            self.getCursor().execute(query, parameters) # type: ignore
        except Relational_Database_Error as error:
            self.getLogger().error(f"The database handler has failed to execute the query. - Query: {query} - Parameters: {parameters} - Error: {error}")
            raise error

    def _closeCursor(self) -> None:
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
        Committing the current transaction to the database.

        Raises:
            Relational_Database_Error: If the commit operation fails.
        """
        try:
            self.getConnection().commit()
            self.getLogger().inform("The transaction has been successfully committed.")
        except Relational_Database_Error as error:
            self.getLogger().error(f"The database handler has failed to commit the transaction. - Error: {error}")
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
            self._closeCursor()
            return response
        except Relational_Database_Error as error:
            self.getLogger().error(f"The database handler has failed to fetch all rows. - Error: {error}")
            raise error

    def _closeConnection(self) -> None:
        """
        Closing the database connection.

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

        Args:
            query (str): The SQL query to execute.
            parameters (Optional[Tuple[Any, ...]]): Parameters for the SQL query.

        Returns:
            List[RowType]: A list of rows returned by the executed query.

        Raises:
            Relational_Database_Error: If the execution or fetching of data fails.
        """
        try:
            self._execute(query, parameters)
            response: List[RowType] = self._fetchAll()
            self._closeCursor()
            self._closeConnection()
            return response
        except Relational_Database_Error as error:
            self.getLogger().error(f"The database handler has failed to get data. - Query: {query} - Parameters: {parameters} - Error: {error}")
            return []

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

        Raises:
            Relational_Database_Error: If the execution or commit operation fails.
        """
        try:
            self._execute(query, parameters)
            self._commit()
            self._closeCursor()
            self._closeConnection()
            return True
        except Relational_Database_Error as error:
            self.getLogger().error(f"The database handler has failed to post data. - Query: {query} - Parameters: {parameters} - Error: {error}")
            return False
