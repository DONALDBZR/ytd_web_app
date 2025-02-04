"""
The module that has the Analytical Management System.
"""
from typing import Union, Dict
from Models.DatabaseHandler import Database_Handler, Extractio_Logger


class AnalyticalManagementSystem:
    """
    The class that will manage all the analytics of the
    application.
    """
    __event_name: str
    """
    The name of the event.
    """
    __uniform_resource_locator: str
    """
    The uniform resource locator of the page.
    """
    __timestamp: int
    """
    The UNIX timestamp of the event.
    """
    __user_agent: str
    """
    The User Agent containing the information of the client.
    """
    __screen_resolution: str
    """
    The screen resolution of the client.
    """
    __referrer: Union[str, None]
    """
    The referrer of the client.
    """
    __loading_time: float
    """
    The loading time of the page.
    """
    __ip_address: str
    """
    The IP Address of the user.
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

    def __init__(self):
        """
        Initializing the management system and injecting any
        dependency needed.
        """
        self.setDatabaseHandler(Database_Handler())
        self.setLogger(Extractio_Logger(__name__))
        self.getLogger().inform("Analytical Management System has been initialized.")

    def getDatabaseHandler(self) -> Database_Handler:
        return self.__database_handler

    def setDatabaseHandler(self, database_handler: Database_Handler) -> None:
        self.__database_handler = database_handler

    def getLogger(self) -> Extractio_Logger:
        return self.__logger

    def setLogger(self, logger: Extractio_Logger) -> None:
        self.__logger = logger

    def getEventName(self) -> str:
        return self.__event_name

    def setEventName(self, event_name: str) -> None:
        self.__event_name = event_name

    def getUniformResourceLocator(self) -> str:
        return self.__uniform_resource_locator

    def setUniformResourceLocator(self, uniform_resource_locator: str) -> None:
        self.__uniform_resource_locator = uniform_resource_locator

    def getTimestamp(self) -> int:
        return self.__timestamp

    def setTimestamp(self, timestamp: int) -> None:
        self.__timestamp = timestamp

    def getUserAgent(self) -> str:
        return self.__user_agent

    def setUserAgent(self, user_agent: str) -> None:
        self.__user_agent = user_agent

    def getScreenResolution(self) -> str:
        return self.__screen_resolution

    def setScreenResolution(self, screen_resolution: str) -> None:
        self.__screen_resolution = screen_resolution

    def getReferrer(self) -> Union[str, None]:
        return self.__referrer

    def setReferrer(self, referrer: Union[str, None]) -> None:
        self.__referrer = referrer

    def getLoadingTime(self) -> float:
        return self.__loading_time

    def setLoadingTime(self, loading_time: float) -> None:
        self.__loading_time = loading_time

    def getIpAddress(self) -> str:
        return self.__ip_address

    def setIpAddress(self, ip_address: str) -> None:
        self.__ip_address = ip_address

    def processEvent(self, data: Dict[str, str]) -> int:
        """
        Processing the event and sending it to the relational
        database server.

        Args:
            data (Dict[str, str]): The data that will be processed.

        Returns:
            None
        """
        print(f"{data=}")
        return 503