import mysql.connector
from mysql.connector.pooling import PooledMySQLConnection
from mysql.connector.connection import MySQLConnection
from mysql.connector.cursor import MySQLCursor


class Database_Handler:
    """
    The database handler that will communicate with the database server.
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
    The password that allows the required user to connect to the database.

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
    The statement to be used to execute all of the requests to the database server

    Type: MySQLCursor
    visibility: private
    """

    def __init__(self):
        """
        Instantiating the class which will try to connect to the database.
        """
        self.setHost(Environment.HOST)
        self.setDatabase(Environment.DATABASE)
        self.setUsername(Environment.USERNAME)
        self.setPassword(Environment.PASSWORD)
        try:
            self.setDatabaseHandler(mysql.connector.connect(host=self.getHost(
            ), database=self.getDatabase(), username=self.getUsername(), password=self.getPassword()))
        except mysql.connector.Error as error:
            print("Connection Failed: " + str(error))

    def getHost(self) -> str:
        return self.__host

    def setHost(self, host: str) -> None:
        self.__host = host

    def getDatabase(self) -> str:
        return self.__database

    def setDatabase(self, database: str) -> None:
        self.__database = database

    def getUsername(self) -> str:
        return self.__username

    def setUsername(self, username: str) -> None:
        self.__username = username

    def getPassword(self) -> str:
        return self.__password

    def setPassword(self, password: str) -> None:
        self.__password = password

    def getDatabaseHandler(self) -> "PooledMySQLConnection | MySQLConnection":
        return self.__database_handler

    def setDatabaseHandler(self, database_handler: "PooledMySQLConnection | MySQLConnection") -> None:
        self.__database_handler = database_handler

    def getStatement(self) -> "MySQLCursor":
        return self.__statement

    def setStatement(self, statement: "MySQLCursor") -> None:
        self.__statement = statement

    def query(self, query: str, parameters: None | tuple):
        """
        Preparing the SQL query that is going to be handled by the database handler

        Returns: Generator[MySQLCursor, None, None] | None
        """
        self.setStatement(self.getDatabaseHandler().cursor(prepared=True))
        self.getStatement().execute(query, parameters)

    def execute(self) -> None:
        """
        Executing the SQL query which will send a command to the database server

        Returns: None
        """
        self.getDatabaseHandler().commit()

    def resultSet(self) -> list:
        """
        Fetching all the data that is requested from the command that was sent to the database server

        Returns: (Any | List[RowType])
        """
        return self.getStatement().fetchall()
