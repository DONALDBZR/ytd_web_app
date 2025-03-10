"""
The module of the database handler which will act as the
object-relational mapper.
"""


from mysql.connector.pooling import PooledMySQLConnection
from mysql.connector.connection import MySQLConnection
from mysql.connector.cursor import MySQLCursor
from Environment import Environment
from Models.Logger import Extractio_Logger
from mysql.connector.types import RowType
from typing import Union, Tuple, Any, List
from mysql.connector import connect, Error


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
        Instantiating the class which will try to connect to the
        database.
        """
        ENV: Environment = Environment()
        self.setLogger(Extractio_Logger(__name__))
        self.__setHost(ENV.getDatabaseHost())
        self.__setDatabase(ENV.getDatabaseSchema())
        self.__setUsername(ENV.getDatabaseUsername())
        self.__setPassword(ENV.getDatabasePassword())
        try:
            self.__setDatabaseHandler(
                connect(
                    host=self.__getHost(),
                    database=self.__getDatabase(),
                    username=self.__getUsername(),
                    password=self.__getPassword()
                )
            )
            self.getLogger().inform("The application has been successfully connected to the database server!")
        except Error as error:
            print(f"Connection Failed!\nError: {error}")
            self.getLogger().error(f"Connection Failed!\nError: {error}")

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

    def _query(self, query: str, parameters: Union[Tuple[Any], None]):
        """
        Preparing the SQL query that is going to be handled by the
        database handler.

        Returns:
            Generator[MySQLCursor, None, None] | None
        """
        self.getLogger().debug(f"Query to be executed!\nQuery: {query}\nParameters: {parameters}")
        self.__setStatement(
            self.__getDatabaseHandler().cursor(
                prepared=True,
                dictionary=True
            )
        )
        self.__getStatement().execute(query, parameters)

    def _execute(self) -> None:
        """
        Executing the SQL query which will send a command to the
        database server

        Returns:
            void
        """
        self.__getDatabaseHandler().commit()
        self.getLogger().inform("The query has been executed!")

    def _resultSet(self) -> List[RowType]:
        """
        Fetching all the data that is requested from the command
        that was sent to the database server.

        Returns:
            [RowType]
        """
        result_set: List[RowType] = self.__getStatement().fetchall()
        self.getLogger().debug("The data has been successfully retrieved!")
        self.__getStatement().close()
        self.getLogger().inform("The connection between the application and the database server will be closed!")
        return result_set

    def getData(self, parameters: Union[Tuple[Any], None], table_name: str, join_condition: str = "", filter_condition: str = "", column_names: str = "*", sort_condition: str = "", limit_condition: int = 0, group_condition: str = "") -> List[RowType]:
        """
        Retrieving data from the database.

        Parameters:
            parameters: array|null: The parameters to be passed into the query.
            table_name: string: The name of the table.
            column_names: string: The name of the columns.
            join_condition: string: Joining table condition.
            filter_condition: string: Items to be filtered with.
            sort_condition: string: The items to be sorted.
            limit_condition: int: The amount of items to be returned
            group_condition: string: The items to be grouped by.

        Returns:
            [RowType]
        """
        self.setQuery(f"SELECT {column_names} FROM {table_name}")
        self.setParameters(parameters)
        self.setQuery(self.getQuery() if join_condition == "" else f"{self.getQuery()} LEFT JOIN {join_condition}")
        self.setQuery(self.getQuery() if filter_condition == "" else f"{self.getQuery()} WHERE {filter_condition}")
        self.setQuery(self.getQuery() if group_condition == "" else f"{self.getQuery()} GROUP BY {group_condition}")
        self.setQuery(self.getQuery() if sort_condition == "" else f"{self.getQuery()} ORDER BY {sort_condition}")
        self.setQuery(f"{self.getQuery()} LIMIT {limit_condition}" if limit_condition > 0 else self.getQuery())
        self._query(self.getQuery(), self.getParameters())
        return self._resultSet()

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
