import mysql.connector
from mysql.connector.pooling import PooledMySQLConnection
from mysql.connector.connection import MySQLConnection
from mysql.connector.cursor import MySQLCursor
from Environment import Environment


class Database_Handler:
    """
    The database handler that will communicate with the database
    server.
    """
    __host: str
    """
    The host of the application

    Type: string
    visibility: private
    """
    __database: str
    """
    The database of the application

    Type: string
    visibility: private
    """
    __username: str
    """
    The user that have access to the database

    Type: string
    visibility: private
    """
    __password: str
    """
    The password that allows the required user to connect to the
    database.

    Type: string
    visibility: private
    """
    __database_handler: "PooledMySQLConnection | MySQLConnection"
    """
    The database handler needed to execute the queries needed

    Type: PooledMySQLConnection | MySQLConnection
    visibility: private
    """
    __statement: "MySQLCursor"
    """
    The statement to be used to execute all of the requests to
    the database server

    Type: MySQLCursor
    visibility: private
    """
    __query: str
    """
    The query to be used to be sent to the database server to
    either get, post, update or delete data.

    Type: string
    Visibility: private
    """
    __parameters: tuple | None
    """
    Parameters that the will be used to sanitize the query which
    is either  get, post, update or delete.

    Type: array|null
    Visibility: private
    """

    def __init__(self):
        """
        Instantiating the class which will try to connect to the
        database.
        """
        self.__setHost(Environment.HOST)
        self.__setDatabase(Environment.DATABASE)
        self.__setUsername(Environment.USERNAME)
        self.__setPassword(Environment.PASSWORD)
        try:
            self.__setDatabaseHandler(mysql.connector.connect(host=self.__getHost(
            ), database=self.__getDatabase(), username=self.__getUsername(), password=self.__getPassword()))
        except mysql.connector.Error as error:
            print("Connection Failed: " + str(error))

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

    def __getDatabaseHandler(self) -> "PooledMySQLConnection | MySQLConnection":
        return self.__database_handler

    def __setDatabaseHandler(self, database_handler: "PooledMySQLConnection | MySQLConnection") -> None:
        self.__database_handler = database_handler

    def __getStatement(self) -> "MySQLCursor":
        return self.__statement

    def __setStatement(self, statement: "MySQLCursor") -> None:
        self.__statement = statement

    def getQuery(self) -> str:
        return self.__query

    def setQuery(self, query: str) -> None:
        self.__query = query

    def getParameters(self) -> tuple | None:
        return self.__parameters

    def setParameters(self, parameters: tuple | None) -> None:
        self.__parameters = parameters

    def query(self, query: str, parameters: None | tuple):
        """
        Preparing the SQL query that is going to be handled by the
        database handler.

        Returns: Generator[MySQLCursor, None, None] | None
        """
        self.__setStatement(self.__getDatabaseHandler().cursor(prepared=True))
        self.__getStatement().execute(query, parameters)

    def execute(self) -> None:
        """
        Executing the SQL query which will send a command to the
        database server

        Returns: None
        """
        self.__getDatabaseHandler().commit()

    def resultSet(self) -> list:
        """
        Fetching all the data that is requested from the command that
        was sent to the database server

        Returns: array
        """
        return self.__getStatement().fetchall()
