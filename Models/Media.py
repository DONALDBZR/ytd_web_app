from Models.DatabaseHandler import Database_Handler
from datetime import datetime
import json
from Models.YouTubeDownloader import YouTube_Downloader
import os


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
    __port: str
    """
    The port of the application

    Type: int
    Visibility: private
    """

    def __init__(self, request: dict[str, str | None]) -> None:
        """
        Instantiating the media's manager which will interact with
        the media's dataset and do the required processing.

        Parameters:
            request:    object: The request from the user.
        """
        self.setPort(request["port"])  # type: ignore
        self.__server()
        self.setDirectory(f"{self.getDirectory()}/Cache/Media")
        # self.metadataDirectory()
        self.setDatabaseHandler(Database_Handler())
        self.getDatabaseHandler()._query(
            "CREATE TABLE IF NOT EXISTS `Media` (identifier INT PRIMARY KEY AUTO_INCREMENT, `value` VARCHAR(8))", None)
        self.getDatabaseHandler()._execute()
        self.setSearch(str(request["search"]))
        self.setReferer(request["referer"])
        self.setValue(str(request["platform"]))
        self.setIpAddress(str(request["ip_address"]))

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

    def getPort(self) -> str:
        return self.__port

    def setPort(self, port: str) -> None:
        self.__port = port

    def __server(self) -> None:
        """
        Setting the directory for the application.

        Returns: void
        """
        # Verifying that the port is for either Apache HTTPD or Werkzeug
        if self.getPort() == '80' or self.getPort() == '443':
            self.setDirectory("/var/www/html/ytd_web_app")
        else:
            self.setDirectory("/home/darkness4869/Documents/extractio")

    def verifyPlatform(self) -> dict[str, int | dict[str, str | int | None]]:
        """
        Verifying the uniform resource locator in order to switch to
        the correct system as well as select and return the correct
        response.

        Returns: object
        """
        response: dict[str, int | dict[str, str | int | None]]
        media = self.getMedia()
        # Verifying that the media does not exist to create one.
        if media["status"] != 200:
            self.postMedia()
            self.verifyPlatform()
        else:
            self.setIdentifier(media["data"][0][0])
        # Verifying the platform data to redirect to the correct system.
        if "youtube" in self.getValue() or "youtu.be" in self.getValue():
            response = {
                "status": 200,
                "data": self.handleYouTube()
            }
        return response  # type: ignore

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
                'status': 404,
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

    def handleYouTube(self) -> dict[str, str | int | None]:
        """
        Handling the data throughout the You Tube Downloader which
        will depend on the referer.

        Returns: object
        """
        response: dict[str, str | int | None]
        identifier: str
        self._YouTubeDownloader = YouTube_Downloader(
            self.getSearch(), self.getIdentifier(), self.getPort())
        # Verifying the referer to retrieve to required data
        if self.getReferer() is None:
            youtube = self._YouTubeDownloader.search()
            media = {
                "Media": {
                    "YouTube": youtube
                }
            }
            if "youtube" in self.getSearch():
                identifier = self.getSearch().replace("https://www.youtube.com/watch?v=", "")
            else:
                identifier = self.getSearch().replace(
                    "https://youtu.be/", "").rsplit("?")[0]
            filename = f"{self.getDirectory()}/{identifier}.json"
            file = open(filename, "w")
            file.write(json.dumps(media, indent=4))
            file.close()
            response = {
                "status": 200,
                "data": youtube  # type: ignore
            }  # type: ignore
        else:
            youtube = self._YouTubeDownloader.retrievingStreams()
            media = {
                "Media": {
                    "YouTube": youtube
                }
            }
            if "youtube" in self.getSearch():
                identifier = self.getSearch().replace("https://www.youtube.com/watch?v=", "")
            else:
                identifier = self.getSearch().replace(
                    "https://youtu.be/", "").rsplit("?")[0]
            filename = f"{self.getDirectory()}/{identifier}.json"
            file = open(filename, "w")
            file.write(json.dumps(media, indent=4))
            file.close()
            response = {
                "status": 200,
                "data": {
                    "url": f"/Download/YouTube/{youtube['identifier']}"
                }  # type: ignore
            }  # type: ignore
        return response

    def metadataDirectory(self):
        """
        Creating the metadata directory

        Returns: void
        """
        if not os.path.exists(self.getDirectory()):
            os.makedirs(self.getDirectory())
