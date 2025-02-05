"""
The module that has the Analytical Management System.
"""
from typing import Union, Dict, Any, Tuple, List
from Models.DatabaseHandler import Database_Handler, Extractio_Logger, Error as DatabaseHandlerError, RowType
from time import mktime
from datetime import datetime
from user_agents import parse
from user_agents.parsers import UserAgent
from re import match
from ipaddress import IPv4Address, IPv6Address, ip_address
from socket import gethostbyname, gaierror
from subprocess import run
from requests import get, Response
from requests.exceptions import RequestException
from json import JSONDecodeError


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
    The IP Address or hostname of the user.
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
    The aspect ratio of the screen resolution.
    """
    __hostname: Union[str, None]
    """
    The host name of the IP Address.
    """
    __ip_information_api: str
    """
    The API to be used for retrieving data from the IP Address.
    """
    not_found: int = 404
    """
    The status code for not found.
    """
    __latitude: float
    """
    The latitude of the geolocation.
    """
    __longitude: float
    """
    The longitude of the geolocation.
    """
    __city: str
    """
    The city of the geolocation.
    """
    __region: str
    """
    The region of the geolocation.
    """
    __country: str
    """
    The country of the geolocation.
    """
    __timezone: str
    """
    The timezone of the geolocation.
    """
    created: int = 201
    """
    The status code for created.
    """
    no_content: int = 204
    """
    The status code for no content.
    """

    def __init__(self):
        """
        Initializing the management system and injecting any
        dependency needed.
        """
        self.setDatabaseHandler(Database_Handler())
        self.setLogger(Extractio_Logger(__name__))
        self.setIpInformationApi("https://ipinfo.io")
        self.getLogger().inform("Analytical Management System has been initialized.")

    def getTimezone(self) -> str:
        return self.__timezone

    def setTimezone(self, timezone: str) -> None:
        self.__timezone = timezone

    def getCountry(self) -> str:
        return self.__country

    def setCountry(self, country: str) -> None:
        self.__country = country

    def getRegion(self) -> str:
        return self.__region

    def setRegion(self, region: str) -> None:
        self.__region = region

    def getCity(self) -> str:
        return self.__city

    def setCity(self, city: str) -> None:
        self.__city = city

    def getLongitude(self) -> float:
        return self.__longitude

    def setLongitude(self, longitude: float) -> None:
        self.__longitude = longitude

    def getLatitude(self) -> float:
        return self.__latitude

    def setLatitude(self, latitude: float) -> None:
        self.__latitude = latitude

    def getIpInformationApi(self) -> str:
        return self.__ip_information_api

    def setIpInformationApi(self, ip_information_api: str) -> None:
        self.__ip_information_api = ip_information_api

    def getHostname(self) -> Union[str, None]:
        return self.__hostname

    def setHostname(self, hostname: Union[str, None]) -> None:
        self.__hostname = hostname

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
        self.setReferrer(str(data["referrer"]) if "referrer" in data and data["referrer"] != "" else None)
        self.setIpAddress(str(data["ip_address"]) if data["ip_address"] != "127.0.0.1" else "omnitechbros.ddns.net")
        status: int = self.getUserAgentData()
        status = self.getScreenResolutionData() if status == self.ok else status
        status = self.setDeviceType() if status == self.ok else status
        status = self.sanitizeIpAddress() if status == self.ok else status
        status = self.getGeolocationData() if status == self.ok else status
        if self.getEventName() == "page_view":
            return self.processPageView(data, status)
        if self.getEventName() == "color_scheme_updated":
            return self.processColorSchemeUpdated(data, status)
        print(f"{self.__dict__=}")
        return self.service_unavailable

    def processPageView(self, data: Dict[str, Union[str, float]], status: int) -> int:
        """
        Processing page view events.

        Args:
            data: {event_name: string, page_url: string, timestamp: string, user_agent: string, screen_resolution: string, referrer: string, loading_time: float, ip_address: string}: The data that will be processed.
            status: int: The status of the previous processing.

        Returns:
            int
        """
        self.setLoadingTime(float(data["loading_time"]) / 1000)
        device_response: Dict[str, int] = self.manageDevice(status)
        status = int(device_response["status"])
        device_identifier: int = int(device_response["identifier"])
        event_type_response: Dict[str, int] = self.manageEventType(status)
        status = int(event_type_response["status"])
        event_type_identifier: int = int(event_type_response["identifier"])
        network_location_response: Dict[str, int] = self.manageNetworkLocation(status)
        status = int(network_location_response["status"])
        network_location_identifier: int = int(network_location_response["identifier"])
        page_view_response: Dict[str, int] = self.managePageView(status)
        status = int(page_view_response["status"])
        page_view_identifier: int = int(page_view_response["identifier"])
        status = self.postEvent(status, device_identifier, event_type_identifier, network_location_identifier, page_view_identifier)
        return status

    def postEvent(self, status: int, device: int, event_type: int, network_location: int, page_view: int) -> int:
        """
        Adding a new event.

        Returns:
            int
        """
        if status != self.ok and status != self.created:
            return status
        parameters: Tuple[str, Union[str, None], int, int, int, int, int] = (self.getUniformResourceLocator(), self.getReferrer(), self.getTimestamp(), device, event_type, network_location, page_view)
        try:
            self.getDatabaseHandler().postData(
                table="Events",
                columns="uniform_resource_locator, referrer, timestamp, Device, EventType, NetworkLocation, PageView",
                values="%s, %s, %s, %s, %s, %s, %s",
                parameters=parameters # type: ignore
            )
            self.getLogger().inform(f"The data has been successfully inserted in the Event table.\nStatus: {self.created}")
            return self.created
        except DatabaseHandlerError as error:
            self.getLogger().error(f"An error occurred while inserting data in the Event table.\nError: {error}")
            return self.service_unavailable

    def managePageView(self, status: int) -> Dict[str, int]:
        """
        Managing the page view of the event.

        Parameters:
            status: int: The status of the previous processing.

        Returns:
            {status: int, identifier: int}
        """
        if status != self.ok and status != self.created:
            return {
                "status": status,
                "identifier": 0
            }
        return self.postPageView()

    def postPageView(self) -> Dict[str, int]:
        """
        Adding a new page view.

        Returns:
            {status: int, identifier: int}
        """
        parameters: Tuple[float] = (self.getLoadingTime(),)
        try:
            self.getDatabaseHandler().postData(
                table="PageView",
                columns="loading_time",
                values="%s",
                parameters=parameters # type: ignore
            )
            self.getLogger().inform(f"The data has been successfully inserted in the Page View table.\nStatus: {self.created}")
            return {
                "status": self.created,
                "identifier": int(self.getDatabaseHandler().getLastRowIdentifier()), # type: ignore
            }
        except DatabaseHandlerError as error:
            self.getLogger().error(f"An error occurred while inserting data in the Page View table.\nError: {error}")
            return {
                "status": self.service_unavailable,
                "identifier": 0
            }

    def manageNetworkLocation(self, status: int) -> Dict[str, int]:
        """
        Managing the network and location of the event.

        Parameters:
            status: int: The status of the previous processing.

        Returns:
            {status: int, identifier: int}
        """
        if status != self.ok and status != self.created:
            return {
                "status": status,
                "identifier": 0
            }
        database_response: Dict[str, Union[int, List[Union[RowType, Dict[str, Union[int, str, float]]]]]] = self.getDatabaseNetworkLocation()
        if database_response["status"] == self.ok:
            network_location: Dict[str, Union[int, str, float]] = database_response["data"][-1] # type: ignore
            return {
                "status": int(database_response["status"]), # type: ignore
                "identifier": int(network_location["identifier"]) # type: ignore
            }
        return self.postNetworkLocation()

    def getDatabaseNetworkLocation(self) -> Dict[str, Union[int, List[Union[RowType, Dict[str, Union[int, str, float]]]]]]:
        """
        Retrieving the network and location data from the database.

        Returns:
            {status: int, data: [{identifier: int, ip_address: string, hostname: string, latitude: float, longitude: float, city: string, region: string, country: string, timezone: string, location: string}]}
        """
        try:
            parameters: Tuple[str, float, float] = (self.getIpAddress(), self.getLatitude(), self.getLongitude())
            data: List[Union[RowType, Dict[str, Union[int, str, float]]]] = self.getDatabaseHandler().getData(
                table_name="NetworkLocation",
                filter_condition="ip_address = %s AND latitude = %s AND longitude = %s",
                parameters=parameters # type: ignore
            )
            return {
                "status": self.ok if len(data) > 0 else self.no_content,
                "data": data if len(data) > 0 else []
            }
        except DatabaseHandlerError as error:
            self.getLogger().error(f"An error occurred while retrieving data from the Network and Location table.\nError: {error}")
            return {
                "status": self.service_unavailable,
                "data": []
            }

    def postNetworkLocation(self) -> Dict[str, int]:
        """
        Adding a new network and location.

        Returns:
            {status: int, identifier: int}
        """
        parameters: Union[Tuple[str, Union[str, None], float, float, str, str, str, str, str], Tuple[str, float, float, str, str, str, str, str]] = (self.getIpAddress(), self.getHostname(), self.getLatitude(), self.getLongitude(), self.getCity(), self.getRegion(), self.getCountry(), self.getTimezone(), f"POINT({self.getLatitude()} {self.getLongitude()})") if hasattr(AnalyticalManagementSystem, "__hostname") else (self.getIpAddress(), self.getLatitude(), self.getLongitude(), self.getCity(), self.getRegion(), self.getCountry(), self.getTimezone(), f"POINT({self.getLatitude()} {self.getLongitude()})")
        try:
            columns: str = "ip_address, hostname, latitude, longitude, city, region, country, timezone, location" if hasattr(AnalyticalManagementSystem, "__hostname") else "ip_address, latitude, longitude, city, region, country, timezone, location"
            values: str = "%s, %s, %s, %s, %s, %s, %s, %s, ST_GeomFromText(%s, 4326)" if hasattr(AnalyticalManagementSystem, "__hostname") else "%s, %s, %s, %s, %s, %s, %s, ST_GeomFromText(%s, 4326)"
            self.getDatabaseHandler().postData(
                table="NetworkLocation",
                columns=columns,
                values=values,
                parameters=parameters # type: ignore
            )
            self.getLogger().inform(f"The data has been successfully inserted in the Network and Location table.\nStatus: {self.created}")
            return {
                "status": self.created,
                "identifier": int(self.getDatabaseHandler().getLastRowIdentifier()), # type: ignore
            }
        except DatabaseHandlerError as error:
            self.getLogger().error(f"An error occurred while inserting data in the Network and Location table.\nError: {error}")
            return {
                "status": self.service_unavailable,
                "identifier": 0
            }

    def manageEventType(self, status: int) -> Dict[str, int]:
        """
        Managing the type of the event.

        Parameters:
            status: int: The status of the previous processing.

        Returns:
            {status: int, identifier: int}
        """
        if status != self.ok and status != self.created:
            return {
                "status": status,
                "identifier": 0
            }
        database_response: Dict[str, Union[int, List[Union[RowType, Dict[str, Union[int, str]]]]]] = self.getDatabaseEventType()
        if database_response["status"] == self.ok:
            event_type: Dict[str, Union[int, str]] = database_response["data"][-1] # type: ignore
            return {
                "status": int(database_response["status"]), # type: ignore
                "identifier": int(event_type["identifier"]) # type: ignore
            }
        return self.postEventType()

    def getDatabaseEventType(self) -> Dict[str, Union[int, List[Union[RowType, Dict[str, Union[int, str]]]]]]:
        """
        Retrieving the event type data from the database.

        Returns:
            {status: int, data: [{identifier: int, name: string}]}
        """
        try:
            parameters: Tuple[str] = (self.getEventName(),)
            data: List[Union[RowType, Dict[str, Union[int, str]]]] = self.getDatabaseHandler().getData(
                table_name="EventTypes",
                filter_condition="name = %s",
                parameters=parameters # type: ignore
            )
            return {
                "status": self.ok if len(data) > 0 else self.no_content,
                "data": data if len(data) > 0 else []
            }
        except DatabaseHandlerError as error:
            self.getLogger().error(f"An error occurred while retrieving data from the Event Types table.\nError: {error}")
            return {
                "status": self.service_unavailable,
                "data": []
            }

    def postEventType(self) -> Dict[str, int]:
        """
        Adding a new event type.

        Returns:
            {status: int, identifier: int}
        """
        parameters: Tuple[str] = (self.getEventName(),)
        try:
            self.getDatabaseHandler().postData(
                table="EventTypes",
                columns="name",
                values="%s",
                parameters=parameters # type: ignore
            )
            self.getLogger().inform(f"The data has been successfully inserted in the Event Types table.\nStatus: {self.created}")
            return {
                "status": self.created,
                "identifier": int(self.getDatabaseHandler().getLastRowIdentifier()), # type: ignore
            }
        except DatabaseHandlerError as error:
            self.getLogger().error(f"An error occurred while inserting data in the Event Types table.\nError: {error}")
            return {
                "status": self.service_unavailable,
                "identifier": 0
            }

    def manageDevice(self, status: int) -> Dict[str, int]:
        """
        Managing the device of the event.

        Parameters:
            status: int: The status of the previous processing.

        Returns:
            {status: int, identifier: int}
        """
        if status != self.ok and status != self.created:
            return {
                "status": status,
                "identifier": 0
            }
        database_response: Dict[str, Union[int, List[Union[RowType, Dict[str, Union[int, str, None, float]]]]]] = self.getDatabaseDevice()
        if database_response["status"] == self.ok:
            device: Dict[str, Union[int, str, None, float]] = database_response["data"][-1] # type: ignore
            return {
                "status": int(database_response["status"]), # type: ignore
                "identifier": int(device["identifier"]) # type: ignore
            }
        return self.postDevice()

    def postDevice(self) -> Dict[str, int]:
        """
        Adding a new device.

        Returns:
            {status: int, identifier: int}
        """
        parameters: Tuple[str, str, str, str, Union[str, None], str, str, int, int, Union[float, None]] = (self.getUserAgent(), self.getBrowser(), self.getBrowserVersion(), self.getOperatingSystem(), self.getOperatingSystemVersion(), self.getDevice(), self.getScreenResolution(), self.getWidth(), self.getHeight(), self.getAspectRatio())
        try:
            self.getDatabaseHandler().postData(
                table="Devices",
                columns="user_agent, browser, browser_version, operating_system, operating_system_version, device, screen_resolution, width, height, aspect_ratio",
                values="%s, %s, %s, %s, %s, %s, %s, %s, %s, %s",
                parameters=parameters # type: ignore
            )
            self.getLogger().inform(f"The data has been successfully inserted in the Devices table.\nStatus: {self.created}")
            return {
                "status": self.created,
                "identifier": int(self.getDatabaseHandler().getLastRowIdentifier()), # type: ignore
            }
        except DatabaseHandlerError as error:
            self.getLogger().error(f"An error occurred while inserting data in the Devices table.\nError: {error}")
            return {
                "status": self.service_unavailable,
                "identifier": 0
            }

    def getDatabaseDevice(self) -> Dict[str, Union[int, List[Union[RowType, Dict[str, Union[int, str, None, float]]]]]]:
        """
        Retrieving the device data from the database.

        Returns:
            {status: int, data: [{identifier: int, user_agent: string, browser: string, browser_version: string, operating_system: string, operating_system_version: string, device: string, screen_resolution: string, width: int, height: int, aspect_ratio: float}]}
        """
        try:
            parameters: Tuple[str, str] = (self.getUserAgent(), self.getScreenResolution())
            data: List[Union[RowType, Dict[str, Union[int, str, None, float]]]] = self.getDatabaseHandler().getData(
                table_name="Devices",
                filter_condition="user_agent = %s AND screen_resolution = %s",
                parameters=parameters # type: ignore
            )
            return {
                "status": self.ok if len(data) > 0 else self.no_content,
                "data": data if len(data) > 0 else []
            }
        except DatabaseHandlerError as error:
            self.getLogger().error(f"An error occurred while retrieving data from the Devices table.\nError: {error}")
            return {
                "status": self.service_unavailable,
                "data": []
            }

    def getGeolocationData(self) -> int:
        """
        Retrieving geolocation data from the IP address.

        Returns:
            int
        """
        if not self.getIpAddress():
            self.getLogger().error("The Analytical Management System cannot retrieve data from the IP Address.")
            return self.service_unavailable
        try:
            route: str = f"{self.getIpInformationApi()}/{self.getIpAddress()}/json"
            response: Response = get(route)
            response.raise_for_status()
            geolocation_data: Any = response.json()
            self.setLatitude(float(str(geolocation_data.get("loc")).split(",")[0]))
            self.setLongitude(float(str(geolocation_data.get("loc")).split(",")[1]))
            self.setCity(str(geolocation_data.get("city")))
            self.setRegion(str(geolocation_data.get("region")))
            self.setCountry(str(geolocation_data.get("country")))
            self.setTimezone(str(geolocation_data.get("timezone")))
            return self.ok
        except RequestException as error:
            self.getLogger().error(f"The Analytical Management System cannot retrieve data from the IP Address.\nError: {error}")
            return self.service_unavailable
        except JSONDecodeError as error:
            self.getLogger().error(f"The Analytical Management System cannot decode the JSON response.\nError: {error}")
            return self.service_unavailable
        except Exception as error:
            self.getLogger().error(f"A general error occurred: {error}")
            return self.service_unavailable

    def sanitizeRealIpAddress(self) -> int:
        """
        Sanitizing the IP Address by checking it is an IP Address or
        a hostname.

        Returns:
            int
        """
        try:
            real_ip_address: Union[IPv4Address, IPv6Address] = ip_address(self.getIpAddress())
            self.setIpAddress(str(real_ip_address))
            self.getLogger().inform("The Analytical Management System has successfully sanitized the IP Address.")
            return self.ok
        except ValueError as error:
            self.getLogger().error(f"The Analytical Management System cannot sanitize the IP Address as it is not an IP Address.\nError: {error}")
            return self.service_unavailable

    def sanitizeIpAddress(self) -> int:
        """
        Sanitizing the IP Address by checking it is an IP Address.

        Returns:
            int
        """
        if not self.getIpAddress():
            self.getLogger().error("The Analytical Management System cannot retrieve the IP Address.")
            return self.service_unavailable
        if self.sanitizeRealIpAddress() == self.ok:
            return self.ok
        try:
            self.setHostname(self.getIpAddress())
            self.setIpAddress(gethostbyname(str(self.getHostname())))
            self.setIpAddress(run(["curl", "ifconfig.me"], capture_output=True, text=True, check=True).stdout.strip() if self.getIpAddress() == "127.0.0.1" else self.getIpAddress())
            self.getLogger().inform("The Analytical Management System has successfully sanitized the IP Address.")
            return self.ok
        except gaierror as error:
            self.getLogger().error(f"The Analytical Management System cannot sanitize the IP Address as it is neither an IP Address nor a host name.\nError: {error}")
            return self.service_unavailable

    def setDeviceType(self) -> int:
        """
        Setting the device type.

        Returns:
            int
        """
        if self.getDevice() != "Other":
            self.getLogger().inform("The Analytical Management System has determined the device type earlier.")
            return self.ok
        if self.getWidth() >= 1024:
            self.setDevice("Desktop")
            self.getLogger().inform("The Analytical Management System has determined the device type.")
            return self.ok
        if self.getWidth() >= 640 and self.getWidth() < 1024:
            self.setDevice("Tablet")
            self.getLogger().inform("The Analytical Management System has determined the device type.")
            return self.ok
        self.setDevice("Mobile")
        self.getLogger().inform("The Analytical Management System has determined the device type.")
        return self.ok

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
