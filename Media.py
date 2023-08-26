from DatabaseHandler import Database_Handler
from datetime import datetime
from flask import request
import json
from YouTubeDownloader import YouTube_Downloader


class Media:
    """
    It allows the application to manage the media.
    """
    __search: str
    """
    The uniform resource locator to be searched.

    Type: string
    Visibility: private
    """
    _YouTubeDownloader: "YouTube_Downloader"
    """
    It will handle every operations related to YouTube.

    Type: YouTube_Downloader
    Visibility: protected
    """
    __referer: str | None
    """
    The http referrer which is the uniform resource locator that
    is needed to be able to allow the user to download the
    required media.

    Type: string|null
    Visibility: private
    """
    __database_handler: "Database_Handler"
    """
    It is the object relational mapper that will be used to
    simplify the process to entering queries.

    Type: Database_Handler
    Visibility: private
    """
    __identifier: int
    """
    The identifier of the required media

    Type: int
    Visibility: private
    """
    __value: str
    """
    The value of the required media which have to correspond to
    the name of the platform from which the media comes from.

    Type: string | null
    Visibility: private
    """
    __timestamp: str
    """
    The timestamp at which the session has been created

    Type: string
    Visibility: private
    """
    __directory: str
    """
    The directory of the JSON files

    Type: string
    Visibility: private
    """
    __ip_address: str
    """
    The IP Address of the user

    Type: string
    Visibility: private
    """

    def __init__(self, search: str, referer: str | None, value: str) -> None:
        """
        Instantiating the media's manager which will interact with
        the media's dataset and do the required processing.

        Parameters:
            search: string: The uniform resource locator to be searched.
            referer: string | null: The http referrer which is the uniform resource locator that is needed to be able to allow the user to download the required media.
            value: string: The value of the required media which have to correspond to the name of the platform from which the media comes from.
        """
        self.setDirectory("./Cache/Media/")
        self.setDatabaseHandler(Database_Handler())
        self.getDatabaseHandler()._query(
            "CREATE TABLE IF NOT EXISTS `Media` (identifier INT PRIMARY KEY AUTO_INCREMENT, `value` VARCHAR(8))", None)
        self.getDatabaseHandler()._execute()
        self.setSearch(search)
        self.setReferer(referer)
        self.setValue(value)

    def getSearch(self) -> str:
        return self.__search

    def setSearch(self, search: str) -> None:
        self.__search = search

    def getReferer(self) -> str | None:
        return self.__referer

    def setReferer(self, referer: str | None) -> None:
        self.__referer = referer

    def getDatabaseHandler(self) -> "Database_Handler":
        return self.__database_handler

    def setDatabaseHandler(self, database_handler: "Database_Handler") -> None:
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

    def verifyPlatform(self) -> dict:
        """
        Verifying the uniform resource locator in order to switch to
        the correct system as well as select and return the correct
        response.

        Returns: object
        """
        response = {}
        media = self.getMedia()
        # Verifying that the media does not exist to create one.
        if media["status"] != 200:
            self.postMedia()
            self.verifyPlatform()
        else:
            self.setIdentifier(media["data"][0][0])
        # Verifying the platform data to redirect to the correct system.
        if "youtube" in self.getValue():
            response = {
                "status": 200,
                "data": self.handleYouTube()
            }
        return response

    def getMedia(self) -> dict:
        """
        Retrieving the Media data from the Media table.

        Returns: object
        """
        media = self.getDatabaseHandler().get_data(
            tuple([self.getValue()]), "Media", filter_condition="value = %s")
        self.setTimestamp(datetime.now().strftime("%Y-%m-%d - %H:%M:%S"))
        response = {}
        if len(media) == 0:
            response = {
                'status': 204,
                'data': media,
                'timestamp': self.getTimestamp()
            }
        else:
            response = {
                'status': 200,
                'data': media,
                'timestamp': self.getTimestamp()
            }
        return response

    def postMedia(self) -> None:
        """
        Creating a record for the media with its data.

        Returns: void
        """
        self.getDatabaseHandler().post_data(
            "Media", "value", "%s", tuple([self.getValue()]))

    def handleYouTube(self) -> dict:
        """
        Handling the data throughout the You Tube Downloader which
        will depend on the referer.

        Returns: object
        """
        self._YouTubeDownloader = YouTube_Downloader(
            self.getSearch(), self.getIdentifier())
        response = {}
        self.setIpAddress(str(request.environ.get("REMOTE_ADDRESS")))
        # Verifying the referer to retrieve to required data
        if self.getReferer() is None:
            media = {
                "YouTube": self._YouTubeDownloader.search()
            }
            filename = self.getDirectory() + self.getIpAddress() + ".json"
            file = open(filename, "w")
            file.write(json.dumps(media, indent=4))
            file.close()
            response = {
                "status": 200,
                "data": self._YouTubeDownloader.search()
            }
        return response
