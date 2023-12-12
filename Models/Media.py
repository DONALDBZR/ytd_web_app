from Models.DatabaseHandler import Database_Handler
from Models.YouTubeDownloader import YouTube_Downloader
from Models.Logger import Extractio_Logger
from datetime import datetime
from Environment import Environment
from mysql.connector.types import RowType
import json
import os
import logging


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
    __referer: str | None
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

    def __init__(self, request: dict[str, str | None]) -> None:
        """
        Instantiating the media's manager which will interact with
        the media's dataset and do the required processing.

        Parameters:
            request:    (object): The request from the user.
        """
        ENV = Environment()
        self.setDirectory(
            f"{ENV.getDirectory()}/Cache/Media"
        )
        self.setLogger(Extractio_Logger())
        self.getLogger().setLogger(logging.getLogger(__name__))
        self.setPort(str(request["port"]))
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
        self.getLogger().inform(
            "The Media Management System has been successfully been initialized!"
        )

    def getSearch(self) -> str:
        return self.__search

    def setSearch(self, search: str) -> None:
        self.__search = search

    def getReferer(self) -> str | None:
        return self.__referer

    def setReferer(self, referer: str | None) -> None:
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

    def verifyPlatform(self) -> dict[str, int | dict[str, str | int | dict[str, str | int | None] | None]]:
        """
        Verifying the uniform resource locator in order to switch to
        the correct system as well as select and return the correct
        response.

        Return:
            (object)
        """
        response: dict[
            str,
            int | dict[str, str | int | dict[str, str | int | None] | None]
        ]
        media = self.getMedia()
        if media["status"] != 200:
            self.postMedia()
            self.verifyPlatform()
        else:
            self.setIdentifier(int(media["data"][0][0]))  # type: ignore
        if "youtube" in self.getValue() or "youtu.be" in self.getValue():
            response = {
                "status": 200,
                "data": self.handleYouTube()
            }
        return response  # type: ignore

    def getMedia(self) -> dict[str, int | list[RowType] | str]:
        """
        Retrieving the Media data from the Media table.

        Return:
            (object)
        """
        filter_data = tuple([self.getValue()])
        media = self.getDatabaseHandler().get_data(
            parameters=filter_data,
            table_name="Media",
            filter_condition="value = %s"
        )
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

        Return:
            (void)
        """
        data = tuple([self.getValue()])
        self.getDatabaseHandler().post_data(
            table="Media",
            columns="value",
            values="%s",
            parameters=data
        )

    def handleYouTube(self) -> dict[str, str | int | None | dict[str, str | int | None]]:
        """
        Handling the data throughout the You Tube Downloader which
        will depend on the referer.

        Return:
            (object)
        """
        response: dict[str, str | int | None | dict[str, str | int | None]]
        identifier: str
        self._YouTubeDownloader = YouTube_Downloader(
            self.getSearch(),
            self.getIdentifier()
        )
        if self.getReferer() is None:
            youtube = self._YouTubeDownloader.search()
            media = {
                "Media": {
                    "YouTube": youtube
                }
            }
            identifier = self._getIdentifier()
            filename = f"{self.getDirectory()}/{identifier}.json"
            file = open(filename, "w")
            file.write(json.dumps(media, indent=4))
            file.close()
            response = {
                "status": 200,
                "data": youtube
            }
        else:
            youtube = self._YouTubeDownloader.retrievingStreams()
            media = {
                "Media": {
                    "YouTube": youtube
                }
            }
            identifier = self._getIdentifier()
            filename = f"{self.getDirectory()}/{identifier}.json"
            file = open(filename, "w")
            file.write(json.dumps(media, indent=4))
            file.close()
            response = {
                "status": 200,
                "data": {
                    "url": f"/Download/YouTube/{youtube['identifier']}"
                }
            }
        return response

    def _getIdentifier(self) -> str:
        """
        Extracting the identifier from the uniform resource locator.

        Return:
            (string)
        """
        identifier: str
        if "youtube" in self.getSearch():
            identifier = self.getSearch().replace("https://www.youtube.com/watch?v=", "")
        else:
            identifier = self.getSearch().replace(
                "https://youtu.be/",
                ""
            ).rsplit("?")[0]
        return identifier
