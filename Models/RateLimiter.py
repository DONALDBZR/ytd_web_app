from time import time
from typing import Optional
from Models.DatabaseHandler import Database_Handler, Extractio_Logger


class Rate_Limiter:
    """
    It will handle any rate limiting needed for the application.
    """
    __database_handler: Database_Handler
    """
    A class to handle database operations such as connecting, executing queries, and managing transactions.
    """
    __logger: Extractio_Logger
    """
    This class manages a logger instance for the Extractio application.
    """

    def __init__(
        self,
        database_handler: Optional[Database_Handler] = None
    ):
        """
        Initializing the rate limiter.

        Parameters:
            database_handler (Database_Handler): The database handler to use for rate limiting.
        """
        self.setDatabaseHandler(database_handler or Database_Handler())
        self.setLogger(Extractio_Logger(__name__))

    def getDatabaseHandler(self) -> Database_Handler:
        return self.__database_handler

    def setDatabaseHandler(self, database_handler: Database_Handler) -> None:
        self.__database_handler = database_handler

    def getLogger(self) -> Extractio_Logger:
        return self.__logger

    def setLogger(self, logger: Extractio_Logger) -> None:
        self.__logger = logger
