"""
The module that will contain the model of the Videos.

Authors:
    Darkness4869
"""
from Environment import Environment
from Models.Logger import Extractio_Logger
from Models.DatabaseHandler import Database_Handler


class Video:
    """
    It will handle any I/O operations that are related with the
    video contents as well as the databases operations.
    """
    __identifier: str
    """
    The identifier of the video
    """
    __directory: str
    """
    The directory of the content
    """
    __logger: Extractio_Logger
    """
    The logger that will all the action of the application.
    """
    __database_handler: Database_Handler
    """
    The database handler that will communicate with the database
    server.
    """
    __table_name: str
    """
    The table to be affected by the management system.
    """

    def __init__(self, identifier: str):
        """
        Initializing the management system as well as all of its
        dependencies.

        Parameters:
            identifier: string: The identifier of the video.
        """
        ENV: Environment = Environment()
        self.setLogger(Extractio_Logger(__name__))
        self.setDatabaseHandler(Database_Handler())
        self.setDirectory(f"{ENV.getDirectory()}/Public/Video")
        self.setTableName("MediaFile")
        self.getLogger().inform("The Video Management System has been successfully initialized!")

    def getTableName(self) -> str:
        return self.__table_name

    def setTableName(self, table_name: str) -> None:
        self.__table_name = table_name

    def getDatabaseHandler(self) -> Database_Handler:
        return self.__database_handler

    def setDatabaseHandler(self, database_handler: Database_Handler) -> None:
        self.__database_handler = database_handler

    def getLogger(self) -> Extractio_Logger:
        return self.__logger

    def setLogger(self, logger: Extractio_Logger) -> None:
        self.__logger = logger

    def getDirectory(self) -> str:
        return self.__directory

    def setDirectory(self, directory: str) -> None:
        self.__directory = directory

    def getIdentifier(self) -> str:
        return self.__identifier

    def setIdentifier(self, identifier: str) -> None:
        self.__identifier = identifier