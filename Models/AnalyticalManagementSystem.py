"""
The module that has the Analytical Management System.
"""
from typing import Union, Dict
from Models.DatabaseHandler import Database_Handler, Extractio_Logger
from time import mktime
from datetime import datetime
from user_agents import parse
from user_agents.parsers import UserAgent
from re import match


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
    The loading time of the page in seconds.
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
    service_unavailable: int = 503
    """
    The status code for the service unavailable.
    """
    __browser: str
    """
    The family of the browser.
    """
    __browser_version: str
    """
    The version of the browser.
    """
    __operating_system: str
    """
    The family of the operating system.
    """
    __operating_system_version: Union[str, None]
    """
    The version of the operating system.
    """
    __device: str
    """
    The type of the device.
    """
    ok: int = 200
    """
    The status code for ok.
    """
    __width: int
    """
    The width of the screen resolution in pixels.
    """
    __height: int
    """
    The height of the screen resolution in pixels.
    """
    __aspect_ratio: Union[float, None]
    """
    The aspect ration of the screen resolution.
    """

    def __init__(self):
        """
        Initializing the management system and injecting any
        dependency needed.
        """
        self.setDatabaseHandler(Database_Handler())
        self.setLogger(Extractio_Logger(__name__))
        self.getLogger().inform("Analytical Management System has been initialized.")

    def getAspectRatio(self) -> Union[float, None]:
        return self.__aspect_ratio

    def setAspectRatio(self, aspect_ratio: Union[float, None]) -> None:
        self.__aspect_ratio = aspect_ratio

    def getHeight(self) -> int:
        return self.__height

    def setHeight(self, height: int) -> None:
        self.__height = height

    def getWidth(self) -> int:
        return self.__width

    def setWidth(self, width: int) -> None:
        self.__width = width

    def getDevice(self) -> str:
        return self.__device

    def setDevice(self, device: str) -> None:
        self.__device = device

    def getOperatingSystemVersion(self) -> Union[str, None]:
        return self.__operating_system_version

    def setOperatingSystemVersion(self, operating_system_version: Union[str, None]) -> None:
        self.__operating_system_version = operating_system_version

    def getOperatingSystem(self) -> str:
        return self.__operating_system

    def setOperatingSystem(self, operating_system: str) -> None:
        self.__operating_system = operating_system

    def getBrowserVersion(self) -> str:
        return self.__browser_version

    def setBrowserVersion(self, browser_version: str) -> None:
        self.__browser_version = browser_version

    def getBrowser(self) -> str:
        return self.__browser

    def setBrowser(self, browser: str) -> None:
        self.__browser = browser

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

    def processEvent(self, data: Dict[str, Union[str, float]]) -> int:
        """
        Processing the event and sending it to the relational
        database server.

        Args:
            data: {event_name: string, page_url: string, timestamp: string, user_agent: string, screen_resolution: string, referrer: string, loading_time: float, ip_address: string}: The data that will be processed.

        Returns:
            int
        """
        self.setEventName(str(data["event_name"]))
        self.setUniformResourceLocator(str(data["page_url"]))
        self.setTimestamp(int(mktime(datetime.strptime(str(data["timestamp"]), "%Y/%m/%d %H:%M:%S").timetuple())))
        self.setUserAgent(str(data["user_agent"]))
        self.setScreenResolution(str(data["screen_resolution"]))
        self.setReferrer(str(data["referrer"]) if data["referrer"] != "" else None)
        self.setLoadingTime(float(data["loading_time"]) / 1000)
        self.setIpAddress(str(data["ip_address"]) if data["ip_address"] != "127.0.0.1" else "omnitechbros.ddns.net")
        status: int = self.getUserAgentData()
        status = self.getScreenResolutionData() if status == self.ok else status
        status = 418
        print(f"{self.__dict__=}")
        return status

    def getScreenResolutionData(self) -> int:
        """
        Retrieving the screen resolution data.

        Returns:
            int
        """
        if not self.getScreenResolution():
            self.getLogger().error("The Analytical Management System cannot retrieve the screen resolution data.")
            return self.service_unavailable
        resolution_pattern_match = match(r"(\d+)x(\d+)", self.getScreenResolution())
        if not resolution_pattern_match:
            self.getLogger().error("The Analytical Management System cannot parse the screen resolution data.")
            return self.service_unavailable
        try:
            self.setWidth(int(resolution_pattern_match.group(1)))
            self.setHeight(int(resolution_pattern_match.group(2)))
            self.setAspectRatio(self.getWidth() / self.getHeight() if self.getHeight() != 0 else None)
            return self.ok
        except ValueError as error:
            self.getLogger().error(f"The Analytical Management System cannot parse the screen resolution data.\nError: {error}")
            return self.service_unavailable

    def getUserAgentData(self) -> int:
        """
        Retrieving the data of the user agent.

        Returns:
            int
        """
        try:
            user_agent: UserAgent = parse(self.getUserAgent())
            self.setBrowser(str(user_agent.browser.family))
            self.setBrowserVersion(str(user_agent.browser.version_string))
            self.setOperatingSystem(str(user_agent.os.family))
            self.setOperatingSystemVersion(str(user_agent.os.version_string) if user_agent.os.version_string != "" else None)
            self.setDevice(str(user_agent.device.family))
            self.getLogger().inform("The Analytical Management System has successfully parsed the data from the User Agent.")
            return self.ok
        except Exception as error:
            self.getLogger().error(f"The Analytical Management System cannot parse the data from the User Agent.\nError: {error}")
            return self.service_unavailable
