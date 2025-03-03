from Models.DatabaseHandler import Database_Handler
from Models.YouTubeDownloader import YouTube_Downloader
from Models.Logger import Extractio_Logger
from datetime import datetime
from Environment import Environment
from mysql.connector.types import RowType
from typing import Dict, Union, List, Tuple
from mysql.connector import Error
from json import dumps
from re import match


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
    The http referrer which is the uniform resource locator that
    is needed to be able to allow the user to download the
    required media.
    """
    __database_handler: Database_Handler
    """
    It is the object relational mapper that will be used to
    simplify the process to entering queries.
    """
    __identifier: int
    """
    The identifier of the required media
    """
    __value: str
    """
    The value of the required media which have to correspond to
    the name of the platform from which the media comes from.
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

    def __init__(self, request: Dict[str, Union[str, None]]) -> None:
        """
        Instantiating the media's manager which will interact with
        the media's dataset and do the required processing.

        Parameters:
            request: {referer: string|null, search: string, platform: string, ip_address: string, port: string}: The request from the user.
        """
        ENV: Environment = Environment()
        self.setDirectory(f"{ENV.getDirectory()}/Cache/Media")
        self.setLogger(Extractio_Logger(__name__))
        self.setDatabaseHandler(Database_Handler())
        self.getDatabaseHandler()._query(
            query="CREATE TABLE IF NOT EXISTS `Media` (identifier INT PRIMARY KEY AUTO_INCREMENT, `value` VARCHAR(8))",
            parameters=None
        )
        self.getDatabaseHandler()._execute()
        self.setSearch(str(request["search"]))
        self.setReferer(request["referer"])
        self.setValue(str(request["platform"]))
        self.setIpAddress(str(request["ip_address"]))
        self.getLogger().inform("The Media Management System has been successfully been initialized!")

    def getSearch(self) -> str:
        return self.__search

    def setSearch(self, search: str) -> None:
        self.__search = search

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
        Verifying that the media platform data has been sucessfully
        inserted in order to process the data needed.

        Parameters:
            status: int: The status of the HTTP request.

        Returns:
            {status: int, data: {status: int, data: {uniform_resource_locator: string, author: string, title: string, identifier: string, author_channel: string, views: int, published_at: string | Datetime | null, thumbnail: string, duration: string, audio_file: string, video_file: string}}}
        """
        if status == 503:
            return {
                "status": status,
                "data": {}
            }
        return self.verifyPlatform()

    def verifyPlatform(self) -> Dict[str, Union[int, Dict[str, Union[str, int, None]]]]:
        """
        Verifies the uniform resource locator to determine the
        correct system and selects the appropriate response based on
        the platform. It ensures that the uniform resource locator
        is valid, sanitizes the input, and processes the media
        information accordingly.  If the platform is recognized, it
        handles the platform-specific logic. If the platform is
        unsupported or the uniform resource locator is invalid, an
        error response is returned.

        Returns:
            {"status": int, "data": {"status": int, "data": {"uniform_resource_locator": string, "author": string, "title": string, "identifier": string, "author_channel": string, "views": int, "published_at": string | Datetime | null, "thumbnail": string, "duration": string, "audio_file": string, "video_file": string}}}

        Raises:
            ValueError: If there is an error while verifying the platform.
        """
        try:
            self.sanitizeValue()
            self.sanitizeSearch()
            media: Dict[str, Union[int, List[RowType], str]] = self.getMedia()
            status: int = int(str(media["status"]))
            if status != 200:
                status = self.postMedia()
                return self.__verifyPlatform(status)
            self.setIdentifier(int(media["data"][0]["identifier"])) # type: ignore
            if "youtube" in self.getValue() or "youtu.be" in self.getValue():
                return self.handleYouTube()
            self.getLogger().error(f"This platform is not supported by the application!\nStatus: 403")
            return {
                "status": 403,
                "data": {}
            }
        except ValueError as error:
            self.getLogger().error(f"An error occurred while verifying the platform.\nError: {error}")
            return {
                "status": 400,
                "data": {}
            }

    def getMedia(self) -> Dict[str, Union[int, List[RowType], str]]:
        """
        Retrieving the Media data from the Media table.

        Returns:
            {status: int, data: [{identifier: int, value: string}], timestamp: string}
        """
        filter_data: Tuple[str] = (self.getValue(),)
        media: List[RowType] = self.getDatabaseHandler().getData(
            parameters=filter_data,
            table_name="Media",
            filter_condition="value = %s"
        )
        self.setTimestamp(datetime.now().strftime("%Y-%m-%d - %H:%M:%S"))
        status: int = 404 if len(media) == 0 else 200
        return {
            "status": status,
            "data": media,
            "timestamp": self.getTimestamp()
        }

    def postMedia(self) -> int:
        """
        Creating a record for the media with its data.

        Returns:
            int
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
        except Error as relational_database_server_error:
            self.getLogger().error(f"There is an error between the model and the relational database server.\nError: {relational_database_server_error}")
            return 503

    def handleYouTube(self) -> Dict[str, Union[int, Dict[str, Union[str, int, None]]]]:
        """
        Handling the data throughout the You Tube Downloader which
        will depend on the referer.

        Returns:
            {status: int, data: {uniform_resource_locator: string, author: string, title: string, identifier: string, author_channel: string, views: int, published_at: string | Datetime | null, thumbnail: string, duration: string, audio_file: string, video_file: string}}
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
        Extracting the identifier from the uniform resource locator.

        Returns:
            string
        """
        identifier: str
        if "youtube" in self.getSearch():
            identifier = self.getSearch().replace("https://www.youtube.com/watch?v=", "")
        else:
            identifier = self.getSearch().replace("https://youtu.be/", "").rsplit("?")[0]
        return identifier

    def getRelatedContents(self, identifier: str) -> Dict[str, Union[int, List[Dict[str, str]]]]:
        """
        Retrieving the related contents which is based on the
        identifier of a specific content.

        Parameters:
            identifier: string: The identifier of the content to be looked upon.

        Returns:
            {status: int, data: [{duration: string, channel: string, title: string, uniform_resource_locator: string, author_channel: string, thumbnail: string}]}
        """
        payload: Dict[str, str] = self._getPayload(identifier)
        related_channel_contents: List[Dict[str, Union[str, int]]] = self.getRelatedChannelContents(payload["channel"])
        related_author_contents: List[Dict[str, Union[str, int]]] = []
        payload["author"] = payload["author"].split(", ") # type: ignore
        for index in range(0, len(payload["author"]), 1):
            related_author_contents = list({value["identifier"]: value for value in related_author_contents + self.getRelatedAuthorContents(payload["author"][index])}.values())
        related_contents: List[Dict[str, Union[str, int]]] = list({value["identifier"]: value for value in related_author_contents + related_channel_contents}.values())
        return self._getRelatedContents(related_contents)

    def _getRelatedContents(self, related_contents: List[Dict[str, Union[str, int]]]) -> Dict[str, Union[int, List[Dict[str, str]]]]:
        """
        Retrieving all of the data needed based on the related
        contents to build the response needed for the API.

        Parameters:
            related_contents: [{identifier: string, duration: string, channel: string, title: string, uniform_resource_locator: string, media_identifier: int}]: The related contents

        Returns:
            {status: int, data: [{duration: string, channel: string, title: string, uniform_resource_locator: string, author_channel: string, thumbnail: string}]}
        """
        status: int = 200 if len(related_contents) > 0 else 204
        data: List[Dict[str, str]] = []
        for index in range(0, len(related_contents), 1):
            self._YouTubeDownloader = YouTube_Downloader(str(related_contents[index]["uniform_resource_locator"]), int(related_contents[index]["media_identifier"]))
            metadata: Dict[str, Union[str, int, None]] = self._YouTubeDownloader.search()
            data.append({
                "duration": str(related_contents[index]["duration"]),
                "channel": str(related_contents[index]["channel"]),
                "title": str(related_contents[index]["title"]),
                "uniform_resource_locator": str(related_contents[index]["uniform_resource_locator"]),
                "author_channel": str(metadata["author_channel"]),
                "thumbnail": str(metadata["thumbnail"])
            })
        return {
            "status": status,
            "data": data
        }

    def getRelatedAuthorContents(self, author: str) -> List[Dict[str, Union[str, int]]]:
        """
        Retrieving the related content for the author.

        Parameters:
            author: string: The name of the author.

        Returns:
            [{identifier: string, duration: string, channel: string, title: string, uniform_resource_locator: string, media_identifier: int}]
        """
        response: List[Dict[str, Union[str, int]]] = []
        database_response: Union[List[RowType], List[Dict[str, Union[str, int]]]] = self.getDatabaseHandler().getData(
            parameters=None,
            table_name="YouTube",
            filter_condition=f"title LIKE '%{author}%'",
            column_names="identifier, CONCAT(LPAD(FLOOR(length / 3600), 2, '0'), ':', LPAD(FLOOR(length / 60), 2, '0'), ':', LPAD(length % 60, 2, '0')) AS duration, author AS channel, title, CONCAT('https://www.youtube.com/watch?v=', identifier) AS uniform_resource_locator, Media AS media_identifier"
        )
        for index in range(0, len(database_response), 1):
            response.append({
                "identifier": str(database_response[index]["identifier"]), # type: ignore
                "duration": str(database_response[index]["duration"]), # type: ignore
                "channel": str(database_response[index]["channel"]), # type: ignore
                "title": str(database_response[index]["title"]), # type: ignore
                "uniform_resource_locator": str(database_response[index]["uniform_resource_locator"]), # type: ignore
                "media_identifier": int(database_response[index]["media_identifier"]) # type: ignore
            })
        return response

    def getRelatedChannelContents(self, channel: str) -> List[Dict[str, Union[str, int]]]:
        """
        Retrieving the related content for the channel.

        Parameters:
            channel: string: The name of the channel.

        Returns:
            [{identifier: string, duration: string, channel: string, title: string, uniform_resource_locator: string, media_identifier: int}]
        """
        parameters: Tuple[str] = (channel,)
        response: List[Dict[str, Union[str, int]]] = []
        database_response: Union[List[RowType], List[Dict[str, Union[str, int]]]] = self.getDatabaseHandler().getData(
            parameters=parameters,
            table_name="YouTube",
            filter_condition="author = %s",
            column_names="identifier, CONCAT(LPAD(FLOOR(length / 3600), 2, '0'), ':', LPAD(FLOOR(length / 60), 2, '0'), ':', LPAD(length % 60, 2, '0')) AS duration, author AS channel, title, CONCAT('https://www.youtube.com/watch?v=', identifier) AS uniform_resource_locator, Media AS media_identifier"
        )
        for index in range(0, len(database_response), 1):
            response.append({
                "identifier": str(database_response[index]["identifier"]), # type: ignore
                "duration": str(database_response[index]["duration"]), # type: ignore
                "channel": str(database_response[index]["channel"]), # type: ignore
                "title": str(database_response[index]["title"]), # type: ignore
                "uniform_resource_locator": str(database_response[index]["uniform_resource_locator"]), # type: ignore
                "media_identifier": int(database_response[index]["media_identifier"]) # type: ignore
            })
        return response

    def _getPayload(self, identifier: str) -> Dict[str, str]:
        """
        Retrieving the payload of the content.

        Parameters:
            identifier: string: The identifier of the content to be looked upon.

        Returns:
            {channel: string, author: string}
        """
        parameters: Tuple[str] = (identifier,)
        database_response: Union[RowType, Dict[str, str]] = self.getDatabaseHandler().getData(
            parameters=parameters,
            table_name="YouTube",
            filter_condition="identifier = %s",
            column_names="author AS channel, title",
            limit_condition=1
        )[0]
        return {
            "channel": str(database_response["channel"]), # type: ignore
            "author": str(database_response["title"]).split(" - ")[0] # type: ignore
        }

    def sanitizeValue(self) -> None:
        """
        Sanitizing the platform value.

        Raises:
            ValueError: If the platform value is empty or contains incorrect characters.

        Returns:
            void
        """
        if not self.getValue():
            self.setValue("")
            self.getLogger().error(f"Failed to sanitize the value.\nStatus: 400\nValue: {self.getValue()}")
            raise ValueError("Failed to sanitize the value.")
        if not match(r"^[a-z]+$", self.getValue()):
            self.setValue("")
            self.getLogger().error(f"Incorrect characters in value!\nStatus: 400\nValue: {self.getValue()}")
            raise ValueError("Incorrect characters in value!")
        self.setValue(self.getValue())

    def sanitizeSearch(self) -> None:
        """
        Sanitizing the search value.

        Raises:
            ValueError: If the search value is empty, contains incorrect characters, or exceeds the maximum length.

        Returns:
            void
        """
        if not self.getSearch():
            self.getLogger().error(f"Failed to sanitize the search value.\nStatus: 400\nSearch: {self.getSearch()}")
            self.setSearch("")
            raise ValueError("Failed to sanitize the search value.")
        if not match(r"^[a-zA-Z0-9:/.?=]+$", self.getSearch()):
            self.getLogger().error(f"Invalid characters in search term!\nStatus: 400\nSearch: {self.getSearch()}")
            self.setSearch("")
            raise ValueError("Invalid characters in search term")
        if len(self.getSearch()) > 64:
            self.getLogger().error(f"Search term is too long!\nStatus: 400\nSearch: {self.getSearch()}")
            self.setSearch("")
            raise ValueError("The search query is too long.")
        self.setSearch(self.getSearch())
