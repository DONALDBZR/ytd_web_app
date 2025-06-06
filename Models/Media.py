"""
The module which has the model of the Media Management System.

Authors:
    Darkness4869
"""
from Models.YouTubeDownloader import YouTube_Downloader, Database_Handler, Extractio_Logger, Environment, RowType, Dict, Union, List, Tuple, Relational_Database_Error
from datetime import datetime
from json import dumps
from re import match, Match
from html import escape
from typing import Optional


class Media:
    """
    It allows the application to manage the media.
    """
    __search: str
    """
    The uniform resource locator to be searched.
    """
    _YouTubeDownloader: YouTube_Downloader
    """
    It will handle every operations related to YouTube.
    """
    __referer: Union[str, None]
    """
    The http referrer which is the uniform resource locator that is needed to be able to allow the user to download the required media.
    """
    __database_handler: Database_Handler
    """
    It is the object relational mapper that will be used to simplify the process to entering queries.
    """
    __identifier: int
    """
    The identifier of the required media
    """
    __value: str
    """
    The value of the required media which have to correspond to the name of the platform from which the media comes from.
    """
    __timestamp: str
    """
    The timestamp at which the session has been created
    """
    __directory: str
    """
    The directory of the JSON files
    """
    __ip_address: str
    """
    The IP Address of the user
    """
    __logger: Extractio_Logger
    """
    The logger that will all the action of the application.
    """
    __ENV: Environment
    """
    ENV File of the application
    """

    def __init__(self, request: Dict[str, Union[str, None]]) -> None:
        """
        Initializing the Media Management System.

        This constructor sets up the necessary environment, logging, database handler, and validates the incoming request data.  It also ensures that the required database table (`Media`) exists before proceeding.

        Parameters:
            request (Dict[str, Union[str, None]]): A dictionary containing the request details with the following keys:
                - "referer" (Optional[str]): The referring uniform resource locator.
                - "search" (str): The search query or target uniform resource locator.
                - "platform" (str): The media platform.
                - "ip_address" (str): The client's IP address.

        Raises:
            ValueError: If the request dictionary does not contain all required keys.
        """
        self.__setEnvironment(Environment())
        self.setDirectory(f"{self.__getEnvironment().getDirectory()}/Cache/Media")
        self.setLogger(Extractio_Logger(__name__))
        self.setDatabaseHandler(Database_Handler())
        self.getDatabaseHandler()._query(
            query="CREATE TABLE IF NOT EXISTS `Media` (identifier INT PRIMARY KEY AUTO_INCREMENT, `value` VARCHAR(8))",
            parameters=None
        )
        self.getDatabaseHandler()._execute()
        if not all(key in request for key in ("referer", "search", "platform", "ip_address")):
            self.getLogger().error(f"The request does not contain the correct keys.\nRequest: {request}")
            raise ValueError("The request does not contain the correct keys.")
        self.setSearch(str(request["search"]))
        self.setReferer(request["referer"])
        self.setValue(str(request["platform"]))
        self.setIpAddress(str(request["ip_address"]))
        self.getLogger().inform("The Media Management System has been successfully been initialized!")

    def getSearch(self) -> str:
        return self.__search

    def setSearch(self, search: str) -> None:
        self.__search = search

    def __getEnvironment(self) -> Environment:
        return self.__ENV

    def __setEnvironment(self, ENV: Environment) -> None:
        self.__ENV = ENV

    def getReferer(self) -> Union[str, None]:
        return self.__referer

    def setReferer(self, referer: Union[str, None]) -> None:
        self.__referer = referer

    def getDatabaseHandler(self) -> Database_Handler:
        return self.__database_handler

    def setDatabaseHandler(self, database_handler: Database_Handler) -> None:
        self.__database_handler = database_handler

    def getIdentifier(self) -> int:
        return self.__identifier

    def setIdentifier(self, identifier: int) -> None:
        self.__identifier = identifier

    def getValue(self) -> str:
        return self.__value

    def setValue(self, value: str) -> None:
        self.__value = value

    def getTimestamp(self) -> str:
        return self.__timestamp

    def setTimestamp(self, timestamp: str) -> None:
        self.__timestamp = timestamp

    def getDirectory(self) -> str:
        return self.__directory

    def setDirectory(self, directory: str) -> None:
        self.__directory = directory

    def getIpAddress(self) -> str:
        return self.__ip_address

    def setIpAddress(self, ip_address: str) -> None:
        self.__ip_address = ip_address

    def getLogger(self) -> Extractio_Logger:
        return self.__logger

    def setLogger(self, logger: Extractio_Logger) -> None:
        self.__logger = logger

    def __verifyPlatform(self, status: int) -> Dict[str, Union[int, Dict[str, Union[str, int, None]]]]:
        """
        Handling platform verification based on the provided status code.

        This private method checks if the provided status code is `503` (Service Unavailable).  If so, it returns a response indicating failure. Otherwise, it re-attempts platform verification by calling `verifyPlatform()`.

        Parameters:
            status (int): The HTTP status code from a previous media verification attempt.

        Returns:
            Dict[str, Union[int, Dict[str, Union[str, int, None]]]]
        """
        if status == 503:
            return {
                "status": status,
                "data": {}
            }
        return self.verifyPlatform()

    def verifyPlatform(self) -> Dict[str, Union[int, Dict[str, Union[str, int, None]]]]:
        """
        Verifying the media platform and process the request accordingly.

        This method sanitizes input values, retrieves media information, and determines whether the requested platform is supported.  If the media is not found, it attempts to post the media and verify its platform again. Currently, only YouTube links are processed.

        Returns:
            Dict[str, Union[int, Dict[str, Union[str, int, None]]]]

        Raises:
            ValueError: The platform cannot be verified.
        """
        try:
            self.sanitizeValue()
            self.sanitizeSearch()
            media: Dict[str, Union[int, List[RowType], str]] = self.getMedia()
            self.handleVerifyPlatform(int(str(media["status"])))
            self.setIdentifier(int(media["data"][0]["identifier"])) # type: ignore
            return self.__handleVerifyPlatform()
        except ValueError as error:
            self.getLogger().error(f"An error occurred while verifying the platform.\nError: {error}")
            return {
                "status": 400,
                "data": {}
            }

    def __handleVerifyPlatform(self) -> Dict[str, Union[int, Dict[str, Union[str, int, None]]]]:
        """
        Handling platform verification based on the URL provided by the user.

        If the platform matches YouTube, it delegates to the appropriate YouTube handler.  Otherwise, it logs an error and raises
        a `ValueError` indicating that the platform is not supported.

        Returns:
            Dict[str, Union[int, Dict[str, Union[str, int, None]]]]

        Raises:
            ValueError: If the platform is not supported by the application.
        """
        if "youtube" in self.getValue() or "youtu.be" in self.getValue():
            return self.handleYouTube()
        self.getLogger().error(f"This platform is not supported by the application!\nStatus: 403")
        raise ValueError("This platform is not supported by the application!")

    def handleVerifyPlatform(self, status: int) -> Optional[Dict[str, Union[int, Dict[str, Union[str, int, None]]]]]:
        """
        Handling platform verification based on the provided status code.

        If the status is 200, the platform is assumed to be already verified and the method exits early.  Otherwise, it triggers a media posting operation followed by platform verification.

        Args:
            status (int): The HTTP status code indicating the current state of the platform.

        Returns:
            Optional[Dict[str, Union[int, Dict[str, Union[str, int, None]]]]]
        """
        if status == 200:
            return None
        status = self.postMedia()
        return self.__verifyPlatform(status)

    def getMedia(self) -> Dict[str, Union[int, List[RowType], str]]:
        """
        Retrieving media data from the Media table in the database based on a specified value.

        The function filters the data by a given value and returns the status of the query along with the retrieved data.  The function also captures the current timestamp when the data is retrieved and returns it along with the result.

        Returns:
            Dict[str, Union[int, List[RowType], str]]

        Raises:
            Relational_Database_Error: If there is an issue with the database query, an error will be logged, and the function will return a 503 status with an empty data list.
        """
        filter_data: Tuple[str] = (self.getValue(),)
        self.setTimestamp(datetime.now().strftime("%Y-%m-%d - %H:%M:%S"))
        try:
            media: List[RowType] = self.getDatabaseHandler().getData(
                parameters=filter_data,
                table_name="Media",
                filter_condition="value = %s"
            )
            status: int = 404 if len(media) == 0 else 200
            return {
                "status": status,
                "data": media,
                "timestamp": self.getTimestamp()
            }
        except Relational_Database_Error as error:
            self.getLogger().error(f"There is an error between the model and the relational database server.\nError: {error}")
            return {
                "status": 503,
                "data": [],
                "timestamp": self.getTimestamp()
            }

    def postMedia(self) -> int:
        """
        Creating a record in the Media table of the database with the provided media value.

        The function inserts the media value into the "Media" table and logs the result.  If the data is successfully inserted, it returns a status code of 201 (Created).  In case of an error during the database interaction, it returns a status code of 503 (Service Unavailable).

        Returns:
            int

        Raises:
            Relational_Database_Error: If there is an error while posting the data to the database, the error is logged, and the function returns a 503 status code.
        """
        data: Tuple[str] = (self.getValue(),)
        try:
            self.getDatabaseHandler().postData(
                table="Media",
                columns="value",
                values="%s",
                parameters=data
            )
            self.getLogger().inform("The data has been inserted in the relational database server.")
            return 201
        except Relational_Database_Error as error:
            self.getLogger().error(f"There is an error between the model and the relational database server.\nError: {error}")
            return 503

    def handleYouTube(self) -> Dict[str, Union[int, Dict[str, Union[str, int, None]]]]:
        """
        Processing YouTube media retrieval and store metadata.

        This method initializes a YouTube downloader instance, retrieves media details, and saves them as a JSON file.  If the request has a referer, it fetches available streams; otherwise, it performs a search.

        Returns:
            Dict[str, Union[int, Dict[str, Union[str, int, None]]]]
        """
        response: Dict[str, Union[int, Dict[str, Union[str, int, None]]]]
        self._YouTubeDownloader: YouTube_Downloader = YouTube_Downloader(self.getSearch(), self.getIdentifier())
        identifier: str = self._getIdentifier()
        filename: str = f"{self.getDirectory()}/{identifier}.json"
        status: int = 200 if self.getReferer() is None else 201
        youtube: Dict[str, Union[str, int, None]] = self._YouTubeDownloader.search() if self.getReferer() is None else self._YouTubeDownloader.retrievingStreams() # type: ignore
        media: Dict[str, Dict[str, Dict[str, Union[str, int, None]]]] = {
            "Media": {
                "YouTube": youtube
            }
        }
        file = open(filename, "w")
        file.write(dumps(media, indent=4))
        file.close()
        response = {
            "status": status,
            "data": youtube
        }
        return response

    def _getIdentifier(self) -> str:
        """
        Extracting the YouTube video identifier from the search URL.

        This method verifies that the search URL belongs to YouTube and extracts the video identifier (an 11-character string) from it.  If the URL is not supported or does not match the expected pattern, an error is logged and a `ValueError` is raised.

        Returns:
            str

        Raises:
            ValueError: If the search URL is not a valid YouTube link or does not contain a valid video identifier.
        """
        if "youtube" not in self.getSearch():
            self.getLogger().error(f"The uniform resource locator is not supported!\nStatus: 400\nSearch: {self.getSearch()}")
            raise ValueError("The uniform resource locator is not supported.")
        identifier_regex: str = r"(?:https?:\/\/)?(?:www\.)?(?:youtube\.com\/(?:watch\?v=|embed\/|v\/|shorts\/)|youtu\.be\/)([a-zA-Z0-9_-]{11})"
        match_identifier: Union[Match[str], None] = match(identifier_regex, self.getSearch())
        if not match_identifier:
            self.getLogger().error(f"The uniform resource locator is not supported.\nStatus: 400\nSearch: {self.getSearch()}")
            raise ValueError(f"The uniform resource locator is not supported.\nStatus: 400\nSearch: {self.getSearch()}")
        return f"shorts/{match_identifier.group(1)}" if "/shorts/" in self.getSearch() else match_identifier.group(1)

    def getRelatedContents(self, identifier: str) -> Dict[str, Union[int, List[Dict[str, str]]]]:
        """
        Retrieving related media content based on an identifier.

        This method fetches related content from both the media's channel and its author(s).  It merges and deduplicates the results before returning them.

        Parameters:
            identifier (str): The unique identifier of the media item.

        Returns:
            Dict[str, Union[int, List[Dict[str, str]]]]
        """
        payload: Dict[str, str] = self._getPayload(identifier)
        related_channel_contents: List[Dict[str, Union[str, int]]] = self.getRelatedChannelContents(payload["channel"])
        related_author_contents: List[Dict[str, Union[str, int]]] = []
        payload["author"] = payload["author"].split(", ") # type: ignore
        for author in payload["author"]:
            related_author_contents = list({value["identifier"]: value for value in related_author_contents + self.getRelatedAuthorContents(author)}.values())
        related_contents: List[Dict[str, Union[str, int]]] = list({value["identifier"]: value for value in related_author_contents + related_channel_contents}.values())
        return self._getRelatedContents(related_contents)

    def _getRelatedContents(self, related_contents: List[Dict[str, Union[str, int]]]) -> Dict[str, Union[int, List[Dict[str, str]]]]:
        """
        Processing and returning metadata for related media content.

        This method takes a list of related media entries, retrieves additional metadata using `YouTube_Downloader`, and formats the response.

        Parameters:
            related_contents (List[Dict[str, Union[str, int]]]): A list of dictionaries containing media details, including `uniform_resource_locator`, `media_identifier`, `duration`, `channel`, and `title`.

        Returns:
            Dict[str, Union[int, List[Dict[str, str]]]]
        """
        status: int = 200 if len(related_contents) > 0 else 204
        data: List[Dict[str, str]] = []
        for related_content in related_contents:
            self._YouTubeDownloader = YouTube_Downloader(str(related_content["uniform_resource_locator"]), int(related_content["media_identifier"]))
            metadata: Dict[str, Union[str, int, None]] = self._YouTubeDownloader.search()
            data.append({
                "duration": escape(str(related_content["duration"])),
                "channel": escape(str(related_content["channel"])),
                "title": escape(str(related_content["title"])),
                "uniform_resource_locator": escape(str(related_content["uniform_resource_locator"])),
                "author_channel": escape(str(metadata["author_channel"])),
                "thumbnail": escape(str(metadata["thumbnail"]))
            })
        return {
            "status": status,
            "data": data
        }

    def getRelatedAuthorContents(self, author: str) -> List[Dict[str, Union[str, int]]]:
        """
        Retrieving the related content for a given author from the YouTube database.

        This function queries the database to find content associated with the provided author's name.  It returns a list of dictionaries with the content's identifier, duration, channel name, title, URL, and media identifier.

        Parameters:
            author (string): The name of the author whose related content is being retrieved.

        Returns:
            List[Dict[string, Union[string, int]]]

        Raises:
            Relational_Database_Error: If there is an issue with querying the database, an error will be logged, and the function will return an empty list.
        """
        parameters: Tuple[str] = (author,)
        try:
            database_response: List[Dict[str, Union[str, int]]] = self.getDatabaseHandler().getData(
                parameters=parameters,
                table_name="YouTube",
                filter_condition=f"title LIKE %s",
                column_names="identifier, CONCAT(LPAD(FLOOR(length / 3600), 2, '0'), ':', LPAD(FLOOR(length / 60), 2, '0'), ':', LPAD(length % 60, 2, '0')) AS duration, author AS channel, title, CONCAT('https://www.youtube.com/watch?v=', identifier) AS uniform_resource_locator, Media AS media_identifier"
            ) # type: ignore
            response: List[Dict[str, Union[str, int]]] = [{"identifier": escape(str(author_content["identifier"])), "duration": escape(str(author_content["duration"])), "channel": escape(str(author_content["channel"])), "title": escape(str(author_content["title"])), "uniform_resource_locator": escape(str(author_content["uniform_resource_locator"])), "media_identifier": int(author_content["media_identifier"])} for author_content in database_response]
            self.getLogger().inform(f"The related author contents have been successfully retrieved.\nStatus: 200\nAuthor: {author}\nAmount: {len(response)}")
            return response
        except Relational_Database_Error as error:
            self.getLogger().error(f"There is an error between the model and the relational database server.\nError: {error}")
            return []

    def getRelatedChannelContents(self, channel: str) -> List[Dict[str, Union[str, int]]]:
        """
        Retrieving the related content for a given channel from the YouTube database.

        This function queries the database to find content associated with the provided channel name.  It returns a list of dictionaries with the content's identifier, duration, channel name, title, URL, and media identifier.

        Parameters:
            channel (string): The name of the channel whose related content is being retrieved.

        Returns:
            List[Dict[string, Union[string, int]]]

        Raises:
            Relational_Database_Error: If there is an issue with querying the database, an error will be logged, and the function will return an empty list.
        """
        parameters: Tuple[str] = (channel,)
        try:
            database_response: List[Dict[str, Union[str, int]]] = self.getDatabaseHandler().getData(
                parameters=parameters,
                table_name="YouTube",
                filter_condition="author = %s",
                column_names="identifier, CONCAT(LPAD(FLOOR(length / 3600), 2, '0'), ':', LPAD(FLOOR(length / 60), 2, '0'), ':', LPAD(length % 60, 2, '0')) AS duration, author AS channel, title, CASE WHEN identifier LIKE 'shorts/%' THEN CONCAT('https://www.youtube.com/', identifier) ELSE CONCAT('https://www.youtube.com/watch?v=', identifier) END AS uniform_resource_locator, Media AS media_identifier"
            ) # type: ignore
            response: List[Dict[str, Union[str, int]]] = [{"identifier": escape(str(channel_content["identifier"])), "duration": escape(str(channel_content["duration"])), "channel": escape(str(channel_content["channel"])), "title": escape(str(channel_content["title"])), "uniform_resource_locator": escape(str(channel_content["uniform_resource_locator"])), "media_identifier": int(channel_content["media_identifier"])} for channel_content in database_response]
            self.getLogger().inform(f"The related channel contents have been successfully retrieved.\nStatus: 200\nChannel: {channel}\nAmount: {len(response)}")
            return response
        except Relational_Database_Error as error:
            self.getLogger().error(f"There is an error between the model and the relational database server.\nError: {error}")
            return response

    def _getPayload(self, identifier: str) -> Dict[str, str]:
        """
        Retrieving and processing metadata payload for a given YouTube video identifier.

        This method queries the database to fetch the video's author and title using the provided video identifier.  It then extracts the channel name and author from the retrieved data.

        Parameters:
            identifier (string): The YouTube video identifier.

        Returns:
            Dict[string, string]: A dictionary containing:
                - "channel" (string): The escaped channel name from the database.
                - "author" (string): The author's name extracted from the title.

        Raises:
            KeyError: If the expected keys ("author", "title") are missing in the database response.
            IndexError: If no data is returned from the database query.
        """
        parameters: Tuple[str] = (identifier,)
        try:
            database_response: Union[RowType, Dict[str, str]] = self.getDatabaseHandler().getData(
                parameters=parameters,
                table_name="YouTube",
                filter_condition="identifier = %s",
                column_names="author, title",
                limit_condition=1
            )[0]
        except IndexError as error:
            self.getLogger().error(f"There is no data for a given identifier.\nError: {error}\nIdentifier: {identifier}")
            raise IndexError("There is no data for a given identifier.")
        try:
            channel: str = escape(str(database_response["author"])) # type: ignore
            title: str = escape(str(database_response["title"])) # type: ignore
        except KeyError as error:
            self.getLogger().error(f"Missing expected keys in database response: {error}")
            raise KeyError(f"Missing expected keys in database response: {error}")
        author: str = title.split(" - ")[0]
        return {
            "channel": channel,
            "author": author
        }

    def sanitizeValue(self) -> None:
        """
        Validating and sanitizing the platform value.

        This method ensures that the platform value is valid by performing the following checks:
        1. It must not be empty.
        2. It must be one of the allowed platforms: "youtube" or "youtu.be".
        3. It must contain only lowercase alphabetic characters.

        If any of these conditions fail, an error is logged, and a `ValueError` is raised.

        Returns:
            void

        Raises:
            ValueError: If the platform value is missing, unsupported, or contains invalid characters.
        """
        allowed_platforms: List[str] = ["youtube", "youtu.be"]
        if not self.getValue():
            self.getLogger().error(f"Failed to sanitize the value.\nStatus: 400\nValue: {self.getValue()}")
            raise ValueError("Failed to sanitize the value.")
        if not self.getValue() in allowed_platforms:
            self.getLogger().error(f"The platform is not supported!\nStatus: 400\nValue: {self.getValue()}")
            raise ValueError("The platform is not supported!")
        if not match(r"^[a-z.]+$", self.getValue()):
            self.getLogger().error(f"Incorrect characters in value!\nStatus: 400\nValue: {self.getValue()}")
            raise ValueError("Incorrect characters in value!")
        self.setValue(self.getValue())

    def sanitizeSearch(self) -> None:
        """
        Validating and sanitizing the search query.

        This method ensures that the search query meets the following criteria:
        1. It must not be empty.
        2. It must only contain valid characters.
        3. It must not exceed 64 characters in length.

        If any of these conditions fail, an error is logged, and a `ValueError` is raised.

        Raises:
            ValueError: If the search query is empty, contains invalid characters, or exceeds the allowed length.
        """
        regular_expression: str = r"^[a-zA-Z0-9\s\-_.,:/?=&]*$"
        if not self.getSearch():
            self.getLogger().error(f"The value to be searched is empty.\nStatus: 400\nSearch: {self.getSearch()}")
            raise ValueError("The value to be searched is empty.")
        if not match(regular_expression, self.getSearch()):
            self.getLogger().error(f"Invalid characters in search term!\nStatus: 400\nSearch: {self.getSearch()}")
            raise ValueError("Invalid characters in search term")
        if len(self.getSearch()) > 64:
            self.getLogger().error(f"The search query is too long.\nStatus: 400\nSearch: {self.getSearch()}")
            raise ValueError("The search query is too long.")
        self.setSearch(self.getSearch())
