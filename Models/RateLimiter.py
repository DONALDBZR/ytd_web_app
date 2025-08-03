from time import time
from typing import Optional
from Models.DatabaseHandler import Database_Handler, Extractio_Logger
from Models.EventsModel import Event, List


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

    def isLimited(
        self,
        ip_address: str,
        endpoint: str,
        limit: int,
        time_window: int
    ) -> bool:
        """
        Checking if the rate limit has been exceeded for the given IP address and endpoint.

        Args:
            ip_address (str): The IP address to check.
            endpoint (str): The endpoint to check.
            limit (int): The rate limit.
            time_window (int): The time window in seconds.

        Returns:
            bool: True if the rate limit has been exceeded, False otherwise.
        """
        current_time: int = int(time())
        start_window: int = current_time - time_window
        connections: int = Event.countConnections(
            database_handler=self.getDatabaseHandler(),
            ip_address=ip_address,
            endpoint=endpoint,
            limit=limit,
            start_window=start_window
        )
        return connections >= limit
