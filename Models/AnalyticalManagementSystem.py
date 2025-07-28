"""
The module that has the Analytical Management System.
"""
from typing import Dict, Union
from urllib import response
from Models.ClickModel import Click, Database_Handler, List
from Models.SearchSubmittedModel import Search_Submitted
from Models.ColorSchemeUpdatedModel import Color_Scheme_Updated
from Models.EventsModel import Event
from Models.DatabaseHandler import Extractio_Logger, Relational_Database_Error as DatabaseHandlerError, Tuple, Any
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
    __color_scheme: str
    """
    The color scheme to be updated in.
    """
    __search_term: str
    """
    The term to be searched.
    """
    __forwarded_uniform_resource_locator: str
    """
    The uniform resource locator on which the user to be
    forwarded on.
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

    def getForwardedUniformResourceLocator(self) -> str:
        return self.__forwarded_uniform_resource_locator

    def setForwardedUniformResourceLocator(self, forwarded_uniform_resource_locator: str) -> None:
        self.__forwarded_uniform_resource_locator = forwarded_uniform_resource_locator

    def getSearchTerm(self) -> str:
        return self.__search_term

    def setSearchTerm(self, search_term: str) -> None:
        self.__search_term = search_term

    def getColorScheme(self) -> str:
        return self.__color_scheme

    def setColorScheme(self, color_scheme: str) -> None:
        self.__color_scheme = color_scheme

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
        Processing an incoming event by validating its data and executing the corresponding handler.

        This function:
        - Verifies that all required keys are present.
        - Checks if the event name is allowed.
        - Logs an error and returns `503` if validation fails.
        - Sets internal attributes such as event name, timestamp, user agent, screen resolution, referrer, and IP address.
        - Performs additional data sanitization and enrichment.
        - Calls the appropriate event processing function based on the event name.
        - Logs an error and returns `503` if the event name is invalid.

        Parameters:
            data (Dict[str, Union[str, float]]): A dictionary containing event data.

        Returns:
            int
        """
        required_keys: List[str] = ["event_name", "page_url", "timestamp", "user_agent", "screen_resolution"]
        allowed_events: List[str] = ["page_view", "search_submitted", "color_scheme_updated", "click"]
        if not all(key in data for key in required_keys):
            self.getLogger().error(f"This request is forged as the required keys are missing and the required data will be logged. - IP Address: {data['ip_address']}")
            return self.service_unavailable
        if data["event_name"] not in allowed_events:
            self.getLogger().error(f"This request is forged as this event is not allowed and the required data will be logged. - IP Address: {data['ip_address']}")
            return self.service_unavailable
        self.setEventName(str(data["event_name"]))
        self.setUniformResourceLocator(str(data["page_url"]))
        self.setTimestamp(int(mktime(datetime.strptime(str(data["timestamp"]), "%Y/%m/%d %H:%M:%S").timetuple())))
        self.setUserAgent(str(data["user_agent"]))
        self.setScreenResolution(str(data["screen_resolution"]))
        self.setReferrer(str(data["referrer"]) if "referrer" in data and data["referrer"] != "" else None)
        self.setIpAddress("omnitechbros.ddns.net" if data["ip_address"] == "127.0.0.1" or str(data["ip_address"]).startswith("192.168.") else str(data["ip_address"]))
        status: int = self.getUserAgentData()
        status = self.getScreenResolutionData() if status == self.ok else status
        status = self.setDeviceType() if status == self.ok else status
        status = self.sanitizeIpAddress() if status == self.ok else status
        status = self.getGeolocationData() if status == self.ok else status
        if self.getEventName() == "page_view":
            status = self.processPageView(data, status)
        if self.getEventName() == "color_scheme_updated":
            status = self.processColorSchemeUpdated(data, status)
        if self.getEventName() == "search_submitted":
            status = self.processSearchSubmitted(data, status)
        if self.getEventName() == "click":
            status = self.processClick(data, status)
        return status

    def processClick(self, data: Dict[str, Union[str, float]], status: int) -> int:
        """
        Processing click events.

        Args:
            data: {event_name: string, page_url: string, timestamp: string, user_agent: string, screen_resolution: string, uniform_resource_locator: string}: The data that will be processed.
            status: int: The status of the previous processing.

        Returns:
            int
        """
        self.setForwardedUniformResourceLocator(str(data["uniform_resource_locator"]))
        device_response: Dict[str, int] = self.manageDevice(status)
        status = int(device_response["status"])
        device_identifier: int = int(device_response["identifier"])
        event_type_response: Dict[str, int] = self.manageEventType(status)
        status = int(event_type_response["status"])
        event_type_identifier: int = int(event_type_response["identifier"])
        network_location_response: Dict[str, int] = self.manageNetworkLocation(status)
        status = int(network_location_response["status"])
        network_location_identifier: int = int(network_location_response["identifier"])
        click_response: Dict[str, int] = self.manageClick(status)
        status = int(click_response["status"])
        click_identifier: int = int(click_response["identifier"])
        return self.postEvent(
            status=status,
            device=device_identifier,
            event_type=event_type_identifier,
            network_location=network_location_identifier,
            click=click_identifier
        )

    def manageClick(self, status: int) -> Dict[str, int]:
        """
        Managing the click of the event.

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
        return self.postClick()

    def postClick(self) -> Dict[str, int]:
        """
        Inserting a new click event into the `"Click"` table of the database.

        Steps:
            - Retrieves the forwarded URL.
            - Attempts to save the click event.
            - Logs appropriate messages.
            - Returns status and identifier.

        Returns:
            Dict[str, int]: A dictionary with the HTTP-like status code and the inserted row's identifier.
        """
        click: Click = Click(
            self.getDatabaseHandler(),
            uniform_resource_locator=self.getForwardedUniformResourceLocator()
        )
        response: bool = click.save()
        status: int = self.created if response else self.service_unavailable
        message: str = "The data has been successfully inserted in the Click table." if response else "An error occurred while inserting data in the Click table."
        if response:
            self.getLogger().inform(f"{message} - Status: {status}")
        else:
            self.getLogger().error(f"{message} - Status: {status}")
        identifier: int = Click.getLastRowIdentifier(self.getDatabaseHandler()) if response else 0
        return {
            "status": status,
            "identifier": identifier
        }

    def processSearchSubmitted(self, data: Dict[str, Union[str, float]], status: int) -> int:
        """
        Processing search submitted events.

        Args:
            data: {event_name: string, page_url: string, timestamp: string, user_agent: string, screen_resolution: string, search_term: string}: The data that will be processed.
            status: int: The status of the previous processing.

        Returns:
            int
        """
        self.setSearchTerm(str(data["search_term"]))
        device_response: Dict[str, int] = self.manageDevice(status)
        status = int(device_response["status"])
        device_identifier: int = int(device_response["identifier"])
        event_type_response: Dict[str, int] = self.manageEventType(status)
        status = int(event_type_response["status"])
        event_type_identifier: int = int(event_type_response["identifier"])
        network_location_response: Dict[str, int] = self.manageNetworkLocation(status)
        status = int(network_location_response["status"])
        network_location_identifier: int = int(network_location_response["identifier"])
        search_submitted_response: Dict[str, int] = self.manageSearchSubmitted(status)
        status = int(search_submitted_response["status"])
        search_submitted_identifier: int = int(search_submitted_response["identifier"])
        return self.postEvent(
            status=status,
            device=device_identifier,
            event_type=event_type_identifier,
            network_location=network_location_identifier,
            search_submitted=search_submitted_identifier
        )

    def manageSearchSubmitted(self, status: int) -> Dict[str, int]:
        """
        Managing the insertion or retrieval of a search submission event.

        This method:
            - Checks if the prior operation was successful based on the given status.
            - If successful, attempts to retrieve the most recent `Search_Submitted` entry.
            - If retrieval succeeds, returns its identifier.
            - If retrieval fails or the prior operation was not successful, inserts a new record.

        Args:
            status (int): The status of the previous processing.

        Returns:
            Dict[str, int]: A dictionary containing:
                - 'status': the final HTTP-like status code.
                - 'identifier': the ID of the relevant `Search_Submitted` row (or 0 if failed).
        """
        if status not in (self.ok, self.created):
            return {
                "status": status,
                "identifier": 0
            }
        database_response: Dict[str, Union[int, List[Search_Submitted]]] = self.getSearchSubmitted()
        if database_response["status"] == self.ok:
            latest_entry: Search_Submitted = database_response["data"][-1] # type: ignore
            return {
                "status": int(database_response["status"]), # type: ignore
                "identifier": latest_entry.identifier # type: ignore
            }
        return self.postSearchSubmitted()

    def postSearchSubmitted(self) -> Dict[str, int]:
        """
        Inserting a new search submission event into the `"SearchSubmitted"` table.

        Process:
            - Retrieves the user's search term.
            - Attempts to insert it into the database.
            - Logs a message based on the outcome.
            - Returns a dictionary containing the operation status and the inserted row's ID.

        Returns:
            Dict[str, int]: A dictionary with keys:
                - `"status"`: HTTP-like status code (e.g., 201 or 503)
                - `"identifier"`: The ID of the newly inserted row (or 0 if failed)
        """
        search_submitted: Search_Submitted = Search_Submitted(
            self.getDatabaseHandler(),
            search_term=self.getSearchTerm()
        )
        response: bool = search_submitted.save()
        status: int = self.created if response else self.service_unavailable
        message: str = "The data has been successfully inserted in the Search Submitted table." if response else "An error occurred while inserting data in the Search Submitted table."
        if response:
            self.getLogger().inform(f"{message} - Status: {status}")
        else:
            self.getLogger().error(f"{message} - Status: {status}")
        identifier: int = Search_Submitted.getLastRowIdentifier(self.getDatabaseHandler()) if response else 0
        return {
            "status": status,
            "identifier": identifier
        }

    def getSearchSubmitted(self) -> Dict[str, Union[int, List[Search_Submitted]]]:
        """
        Retrieving search submission entries from the `"SearchSubmitted"` table matching the current search term.

        This method:
            - Queries the database for entries matching `search_term`.
            - Returns a dictionary containing:
                - A status code: `200` if entries found, otherwise `204`.
                - A list of `Search_Submitted` model instances, or an empty list if none are found.

        Returns:
            Dict[str, Union[int, List[Search_Submitted]]]: Response with status and model data.
        """
        data: List[Search_Submitted] = Search_Submitted.getBySearchTerm(self.getDatabaseHandler(), self.getSearchTerm())
        status: int = self.ok if len(data) > 0 else self.no_content
        return {
            "status": status,
            "data": data
        }

    def processColorSchemeUpdated(self, data: Dict[str, Union[str, float]], status: int) -> int:
        """
        Processing color scheme updated events.

        Args:
            data: {event_name: string, page_url: string, timestamp: string, user_agent: string, screen_resolution: string, color_scheme: string}: The data that will be processed.
            status: int: The status of the previous processing.

        Returns:
            int
        """
        self.setColorScheme(str(data["color_scheme"]))
        device_response: Dict[str, int] = self.manageDevice(status)
        status = int(device_response["status"])
        device_identifier: int = int(device_response["identifier"])
        event_type_response: Dict[str, int] = self.manageEventType(status)
        status = int(event_type_response["status"])
        event_type_identifier: int = int(event_type_response["identifier"])
        network_location_response: Dict[str, int] = self.manageNetworkLocation(status)
        status = int(network_location_response["status"])
        network_location_identifier: int = int(network_location_response["identifier"])
        color_scheme_updated_response: Dict[str, int] = self.manageColorSchemeUpdated(status)
        status = int(color_scheme_updated_response["status"])
        color_scheme_updated_identifier: int = int(color_scheme_updated_response["identifier"])
        return self.postEvent(
            status=status,
            device=device_identifier,
            event_type=event_type_identifier,
            network_location=network_location_identifier,
            color_scheme=color_scheme_updated_identifier
        )

    def manageColorSchemeUpdated(self, status: int) -> Dict[str, int]:
        """
        Managing the color scheme updated of the event.

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
        return self.postColorSchemeUpdated()

    def postColorSchemeUpdated(self) -> Dict[str, int]:
        """
        Inserting a new color scheme update event into the `"ColorSchemeUpdated"` table of the database.

        This method:
            - Retrieves the updated color scheme.
            - Attempts to insert the color scheme into the database's `"ColorSchemeUpdated"` table.
            - Logs success or failure messages.
            - Returns a dictionary containing the status code and the last inserted row's identifier.

        Returns:
            Dict[str, int]: A dictionary with keys:
                - "status": HTTP-style status code indicating result (201 or 503).
                - "identifier": ID of the inserted row or 0 if failed.
        """
        color_scheme_updated: Color_Scheme_Updated = Color_Scheme_Updated(
            self.getDatabaseHandler(),
            color_scheme=self.getColorScheme()
        )
        response: bool = color_scheme_updated.save()
        status: int = self.created if response else self.service_unavailable
        identifier: int = Color_Scheme_Updated.getLastRowIdentifier(self.getDatabaseHandler()) if response else 0
        if response:
            self.getLogger().inform(f"The data has been successfully inserted in the Color Scheme table. - Status: {self.created}")
        else:
            self.getLogger().error(f"An error occurred while inserting data in the Color Scheme table. - Status: {self.service_unavailable}")
        return {
            "status": status,
            "identifier": identifier
        }

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
        return self.postEvent(
            status=status,
            device=device_identifier,
            event_type=event_type_identifier,
            network_location=network_location_identifier,
            page_view=page_view_identifier
        )

    def postEvent(self, status: int, device: int, event_type: int, network_location: int, page_view: int = 0, color_scheme: int = 0, search_submitted: int = 0, click: int = 0) -> int:
        """
        Posting an event based on the given parameters to the appropriate event handler.

        This function checks the status and other parameters to determine which specific event function should be triggered.  If the event is successfully processed, it will return a corresponding status, otherwise, it will return the status code indicating an error or an unavailable service.

        Parameters:
            status (int): The status of the event.
            device (int): The device identifier.
            event_type (int): The type of the event.
            network_location (int): The network location identifier.
            page_view (int, optional): The page view event identifier.
            color_scheme (int, optional): The color scheme event identifier.
            search_submitted (int, optional): The search submission event identifier.
            click (int, optional): The click event identifier.

        Returns:
            int
        """
        if status != self.ok and status != self.created:
            return status
        if page_view != 0:
            return self.postEventPageView(device, event_type, network_location, page_view)
        if color_scheme != 0:
            return self.postEventColorSchemeUpdated(device, event_type, network_location, color_scheme)
        if search_submitted != 0:
            return self.postEventSearchSubmitted(device, event_type, network_location, search_submitted)
        if click != 0:
            return self.postEventClick(device, event_type, network_location, click)
        return self.service_unavailable

    def postEventClick(
        self,
        device: int,
        event_type: int,
        network_location: int,
        click: int
    ) -> int:
        """
        Inserting a new event click record into the `"Events"` table of the database.

        This method:
            - Inserts data related to the click event into the `"Events"` table.
            - Logs success or failure messages.
            - Returns a status code representing the result of the operation.

        Parameters:
            device (int): The device identifier where the event occurred.
            event_type (int): The type of the event.
            network_location (int): The network location identifier.
            click (int): The identifier for the event.

        Returns:
            int: The status code indicating success (self.created) or failure (self.service_unavailable).
        """
        event: Event = Event(
            self.getDatabaseHandler(),
            uniform_resource_locator=self.getUniformResourceLocator(),
            referrer=self.getReferrer(),
            timestamp=self.getTimestamp(),
            Device=device,
            EventType=event_type,
            NetworkLocation=network_location,
            Click=click
        )
        response: bool = event.save()
        if response:
            self.getLogger().inform(f"The data has been successfully inserted in the Event table. - Status: {self.created}")
        else:
            self.getLogger().error(f"An error occurred while inserting data in the Event table. - Status: {self.service_unavailable}")
        return self.created if response else self.service_unavailable

    def postEventSearchSubmitted(
        self,
        device: int,
        event_type: int,
        network_location: int,
        search_submitted: int
    ) -> int:
        """
        Inserting a new event record indicating a search submission into the `"Events"` table.

        This method:
            - Constructs an `Event` model with relevant search submission data.
            - Persists it to the database using the `save()` method.
            - Logs the result of the operation.
            - Returns a corresponding HTTP-style status code.

        Parameters:
            device (int): Identifier of the device where the search was submitted.
            event_type (int): The type of event (e.g., "SearchSubmitted").
            network_location (int): Network location or IP context of the request.
            search_submitted (int): Identifier or flag indicating search submission details.

        Returns:
            int: Status code indicating success (`self.created`) or failure (`self.service_unavailable`).
        """
        event: Event = Event(
            self.getDatabaseHandler(),
            uniform_resource_locator=self.getUniformResourceLocator(),
            referrer=self.getReferrer(),
            timestamp=self.getTimestamp(),
            Device=device,
            EventType=event_type,
            NetworkLocation=network_location,
            SearchSubmitted=search_submitted
        )
        response: bool = event.save()
        if response:
            self.getLogger().inform(f"The data has been successfully inserted in the Event table. - Status: {self.created}")
        else:
            self.getLogger().error(f"An error occurred while inserting data in the Event table. - Status: {self.service_unavailable}")
        return self.created if response else self.service_unavailable

    def postEventColorSchemeUpdated(
        self,
        device: int,
        event_type: int,
        network_location: int,
        color_scheme: int
    ) -> int:
        """
        Inserting a new event color scheme updated record into the `"Events"` table of the database.

        This method:
            - Inserts data related to the color scheme updated event into the `"Events"` table.
            - Logs success or failure messages.
            - Returns a status code representing the result of the operation.

        Parameters:
            device (int): The device identifier where the event occurred.
            event_type (int): The type of the event.
            network_location (int): The network location identifier.
            color_scheme (int): The color scheme identifier.

        Returns:
            int: Status code indicating success (`self.created`) or failure (`self.service_unavailable`).
        """
        event: Event = Event(
            self.getDatabaseHandler(),
            uniform_resource_locator=self.getUniformResourceLocator(),
            referrer=self.getReferrer(),
            timestamp=self.getTimestamp(),
            Device=device,
            EventType=event_type,
            NetworkLocation=network_location,
            ColorSchemeUpdated=color_scheme
        )
        response: bool = event.save()
        if response:
            self.getLogger().inform(f"The data has been successfully inserted in the Event table. - Status: {self.created}")
        else:
            self.getLogger().error(f"An error occurred while inserting data in the Event table. - Status: {self.service_unavailable}")
        return self.created if response else self.service_unavailable

    def postEventPageView(
        self,
        device: int,
        event_type: int,
        network_location: int,
        page_view: int
    ) -> int:
        """
        Inserting a new page view event record into the `"Events"` table of the database.

        This method:
            - Creates an `Event` instance populated with page view event data.
            - Saves the event record to the database.
            - Logs success or failure messages accordingly.
            - Returns an HTTP-style status code representing the result.

        Parameters:
            device (int): The device identifier where the event occurred.
            event_type (int): The type of the event.
            network_location (int): The network location identifier.
            page_view (int): The page view identifier.

        Returns:
            int: Status code indicating success (`self.created`) or failure (`self.service_unavailable`).
        """
        event: Event = Event(
            self.getDatabaseHandler(),
            uniform_resource_locator=self.getUniformResourceLocator(),
            referrer=self.getReferrer(),
            timestamp=self.getTimestamp(),
            Device=device,
            EventType=event_type,
            NetworkLocation=network_location,
            PageView=page_view
        )
        response: bool = event.save()
        if response:
            self.getLogger().inform(f"The data has been successfully inserted in the Event table. - Status: {self.created}")
        else:
            self.getLogger().error(f"An error occurred while inserting data in the Event table. - Status: {self.service_unavailable}")
        return self.created if response else self.service_unavailable

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
        Inserting a new page view record into the `"PageView"` table of the database.

        This method:
        - Inserts the page loading time into the `"PageView"` table in the database.
        - Logs success or failure messages based on whether the insertion is successful.
        - Returns a dictionary with the status code and the identifier of the inserted record.

        Returns:
            Dict[str, int]
        """
        parameters: Tuple[float] = (self.getLoadingTime(),)
        response: bool = self.getDatabaseHandler().postData(
            table="PageView",
            columns="loading_time",
            values="%s",
            parameters=parameters
        )
        self.getLogger().inform(f"The data has been successfully inserted in the Page View table. - Status: {self.created}") if response else self.getLogger().error(f"An error occurred while inserting data in the Page View table. - Status: {self.service_unavailable}")
        return {
            "status": self.created if response else self.service_unavailable,
            "identifier": int(str(self.getDatabaseHandler().getLastRowIdentifier())) if response else 0
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
        database_response: Dict[str, Union[int, List[Dict[str, Union[int, str, float]]]]] = self.getDatabaseNetworkLocation()
        if database_response["status"] == self.ok:
            network_location: Dict[str, Union[int, str, float]] = database_response["data"][-1] # type: ignore
            return {
                "status": int(database_response["status"]), # type: ignore
                "identifier": int(network_location["identifier"]) # type: ignore
            }
        return self.postNetworkLocation()

    def getDatabaseNetworkLocation(self) -> Dict[str, Union[int, List[Dict[str, Union[int, str, float]]]]]:
        """
        Retrieving network location data from the `"NetworkLocation"` table in the database.

        This method:
        - Queries the `"NetworkLocation"` table based on the provided IP address, latitude, and longitude.
        - Returns a dictionary containing the status and the network location data.
        - If data is found, returns it along with a success status.
        - If no data is found, returns an empty list and a "no content" status.

        Returns:
            Dict[str, Union[int, List[Dict[str, Union[int, str, float]]]]]
        """
        parameters: Tuple[str, float, float] = (self.getIpAddress(), self.getLatitude(), self.getLongitude())
        data: List[Dict[str, Union[int, str, float]]] = self.getDatabaseHandler().getData(
            table_name="NetworkLocation",
            filter_condition="ip_address = %s AND latitude = %s AND longitude = %s",
            parameters=parameters # type: ignore
        )
        return {
            "status": self.ok if len(data) > 0 else self.no_content,
            "data": data if len(data) > 0 else []
        }

    def postNetworkLocation(self) -> Dict[str, int]:
        """
        Posting network location data to the `"NetworkLocation"` table in the database.

        This method:
        - Collects information regarding the network location.
        - Inserts the collected data into the `"NetworkLocation"` table in the database.
        - Returns a dictionary containing the status and the identifier of the inserted row.
        - The method conditionally includes the hostname based on whether the `AnalyticalManagementSystem` class has the 
        attribute `__hostname`.

        Returns:
            Dict[str, int]
        """
        parameters: Union[Tuple[str, Union[str, None], float, float, str, str, str, str, str], Tuple[str, float, float, str, str, str, str, str]] = (self.getIpAddress(), self.getHostname(), self.getLatitude(), self.getLongitude(), self.getCity(), self.getRegion(), self.getCountry(), self.getTimezone(), f"POINT({self.getLatitude()} {self.getLongitude()})") if hasattr(AnalyticalManagementSystem, "__hostname") else (self.getIpAddress(), self.getLatitude(), self.getLongitude(), self.getCity(), self.getRegion(), self.getCountry(), self.getTimezone(), f"POINT({self.getLatitude()} {self.getLongitude()})")
        columns: str = "ip_address, hostname, latitude, longitude, city, region, country, timezone, location" if hasattr(AnalyticalManagementSystem, "__hostname") else "ip_address, latitude, longitude, city, region, country, timezone, location"
        values: str = "%s, %s, %s, %s, %s, %s, %s, %s, ST_GeomFromText(%s, 4326)" if hasattr(AnalyticalManagementSystem, "__hostname") else "%s, %s, %s, %s, %s, %s, %s, ST_GeomFromText(%s, 4326)"
        response: bool = self.getDatabaseHandler().postData(
            table="NetworkLocation",
            columns=columns,
            values=values,
            parameters=parameters # type: ignore
        )
        self.getLogger().inform(f"The data has been successfully inserted in the Network and Location table. - Status: {self.created}") if response else self.getLogger().error(f"An error occurred while inserting data in the Network and Location table. - Status: {self.service_unavailable}")
        return {
            "status": self.created if response else self.service_unavailable,
            "identifier": int(str(self.getDatabaseHandler().getLastRowIdentifier())) if response else 0,
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
        database_response: Dict[str, Union[int, List[Dict[str, Union[int, str]]]]] = self.getDatabaseEventType()
        if database_response["status"] == self.ok:
            event_type: Dict[str, Union[int, str]] = database_response["data"][-1] # type: ignore
            return {
                "status": int(database_response["status"]), # type: ignore
                "identifier": int(event_type["identifier"]) # type: ignore
            }
        return self.postEventType()

    def getDatabaseEventType(self) -> Dict[str, Union[int, List[Dict[str, Union[int, str]]]]]:
        """
        Retrieving event type data from the `"EventTypes"` table based on the event name.

        This method:
        - Queries the `"EventTypes"` table in the database to retrieve event types corresponding to the provided event name.
        - Returns a dictionary containing the status of the operation and the event type data if found.

        Returns:
            Dict[str, Union[int, List[Dict[str, Union[int, str]]]]]
        """
        parameters: Tuple[str] = (self.getEventName(),)
        data: List[Dict[str, Union[int, str]]] = self.getDatabaseHandler().getData(
            table_name="EventTypes",
            filter_condition="name = %s",
            parameters=parameters # type: ignore
        )
        return {
            "status": self.ok if len(data) > 0 else self.no_content,
            "data": data if len(data) > 0 else []
        }

    def postEventType(self) -> Dict[str, int]:
        """
        Inserting event type data into the `"EventTypes"` table.

        This method:
        - Inserts a new event type into the `"EventTypes"` table, using the event name.
        - Returns a dictionary containing the status of the operation and the identifier of the inserted record.

        Returns:
            Dict[str, int]
        """
        parameters: Tuple[str] = (self.getEventName(),)
        response: bool = self.getDatabaseHandler().postData(
            table="EventTypes",
            columns="name",
            values="%s",
            parameters=parameters
        )
        self.getLogger().inform(f"The data has been successfully inserted in the Event Types table. - Status: {self.created}") if response else self.getLogger().error(f"An error occurred while inserting data in the Event Types table. - Status: {self.service_unavailable}")
        return {
            "status": self.created if response else self.service_unavailable,
            "identifier": int(str(self.getDatabaseHandler().getLastRowIdentifier())) if response else 0,
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
        database_response: Dict[str, Union[int, List[Dict[str, Union[int, str, None, float]]]]] = self.getDatabaseDevice()
        if database_response["status"] == self.ok:
            device: Dict[str, Union[int, str, None, float]] = database_response["data"][-1] # type: ignore
            return {
                "status": int(database_response["status"]), # type: ignore
                "identifier": int(device["identifier"]) # type: ignore
            }
        return self.postDevice()

    def postDevice(self) -> Dict[str, int]:
        """
        Inserting device information into the `"Devices"` table.

        This method:
        - Inserts a new device record into the `"Devices"` table using various device details.
        - Returns a dictionary containing the status of the operation and the identifier of the inserted device record.

        Returns:
            Dict[str, int]
        """
        parameters: Tuple[str, str, str, str, Union[str, None], str, str, int, int, Union[float, None]] = (self.getUserAgent(), self.getBrowser(), self.getBrowserVersion(), self.getOperatingSystem(), self.getOperatingSystemVersion(), self.getDevice(), self.getScreenResolution(), self.getWidth(), self.getHeight(), self.getAspectRatio())
        response: bool = self.getDatabaseHandler().postData(
            table="Devices",
            columns="user_agent, browser, browser_version, operating_system, operating_system_version, device, screen_resolution, width, height, aspect_ratio",
            values="%s, %s, %s, %s, %s, %s, %s, %s, %s, %s",
            parameters=parameters # type: ignore
        )
        self.getLogger().inform(f"The data has been successfully inserted in the Devices table. - Status: {self.created}") if response else self.getLogger().error(f"An error occurred while inserting data in the Devices table. - Status: {self.service_unavailable}")
        return {
            "status": self.created if response else self.service_unavailable,
            "identifier": int(str(self.getDatabaseHandler().getLastRowIdentifier())) if response else 0,
        }

    def getDatabaseDevice(self) -> Dict[str, Union[int, List[Dict[str, Union[int, str, None, float]]]]]:
        """
        Retrieving device information from the `"Devices"` table based on the user agent and screen resolution.

        This method:
        - Queries the `"Devices"` table to retrieve records where the user agent and screen resolution match the provided values.
        - Returns a dictionary containing the status of the operation and the retrieved device data.

        Returns:
            Dict[str, Union[int, List[Dict[str, Union[int, str, None, float]]]]]
        """
        parameters: Tuple[str, str] = (self.getUserAgent(), self.getScreenResolution())
        data: List[Dict[str, Union[int, str, None, float]]] = self.getDatabaseHandler().getData(
            table_name="Devices",
            filter_condition="user_agent = %s AND screen_resolution = %s",
            parameters=parameters # type: ignore
        )
        return {
            "status": self.ok if len(data) > 0 else self.no_content,
            "data": data if len(data) > 0 else []
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
            self.getLogger().error(f"The Analytical Management System cannot retrieve data from the IP Address. - Error: {error}")
            return self.service_unavailable
        except JSONDecodeError as error:
            self.getLogger().error(f"The Analytical Management System cannot decode the JSON response. - Error: {error}")
            return self.service_unavailable
        except Exception as error:
            self.getLogger().error(f"A general error occurred: {error}")
            return self.service_unavailable

    def sanitizeRealIpAddress(self) -> int:
        """
        Validating and sanitizing the stored IP address.

        This function:
        - Retrieves the stored IP address and attempts to validate it as either an IPv4 or IPv6 address.
        - If valid, updates the stored IP address in string format.
        - Logs success if the IP address is properly sanitized.
        - Logs an error and returns `self.service_unavailable` if the IP address is invalid.

        Returns:
            int

        Raises:
            ValueError: If the stored IP address is not a valid IPv4 or IPv6 address.
        """
        try:
            real_ip_address: Union[IPv4Address, IPv6Address] = ip_address(self.getIpAddress())
            self.setIpAddress(str(real_ip_address))
            self.getLogger().inform("The Analytical Management System has successfully sanitized the IP Address.")
            return self.ok
        except ValueError as error:
            self.getLogger().warn(f"The Analytical Management System cannot sanitize the IP Address as it is not an IP Address. - Error: {error}")
            return self.service_unavailable

    def sanitizeIpAddress(self) -> int:
        """
        Sanitizing the stored IP address for the Analytical Management System.

        This function:
        - Checks if an IP address is available.
        - Logs an error and returns `503` if no IP address is found.
        - Attempts to sanitize the IP address using `sanitizeRealIpAddress()`.
        - If successful, returns `200`.
        - Otherwise, tries to resolve the IP address using the hostname.
        - Logs success if the IP address is successfully resolved.
        - Logs an error and returns `503` if the IP address cannot be resolved.

        Returns:
            int

        Raises:
            gaierror: If the IP address is neither a valid IP nor a resolvable hostname.
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
            self.getLogger().error(f"The Analytical Management System cannot sanitize the IP Address as it is neither an IP Address nor a host name. - Error: {error}")
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
            self.getLogger().error(f"The Analytical Management System cannot parse the screen resolution data. - Error: {error}")
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
            self.getLogger().error(f"The Analytical Management System cannot parse the data from the User Agent. - Error: {error}")
            return self.service_unavailable
