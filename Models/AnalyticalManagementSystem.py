"""
The module that has the Analytical Management System.
"""
from typing import Union


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

    # def __init__(self):
    #     """
    #     Initializing the management system and injecting any
    #     dependency needed.
    #     """
    #     pass

    # def processEvent(self, data: Dict[str, str]) -> None:
    #     """
    #     Processing the event and sending it to the relational
    #     database server.

    #     Args:
    #         data (Dict[str, str]): The data that will be processed.

    #     Returns:
    #         None
    #     """
    #     pass