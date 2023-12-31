from Classes.YouTubeDownloader import YouTube_Downloader
from datetime import datetime
from mysql.connector.types import RowType
import json
import sys
import os
import logging


sys.path.append(os.getcwd())
from Models.DatabaseHandler import Database_Handler
from Models.Logger import Extractio_Logger
from Environment import Environment


class Media:
    """
    It allows the CRON to manage the media.
    """
    __search: str
    """
    The uniform resource locator to be searched.
    """
    _YouTubeDownloader: YouTube_Downloader
    """
    It will handle every operations related to YouTube.
    """
    __database_handler: Database_Handler
    """
    It is the object relational mapper that will be used to
    simplify the process to entering queries.
    """
    __identifier: int
    """
    The identifier of the required media.
    """
    __value: str
    """
    The value of the required media which have to correspond to
    the name of the platform from which the media comes from.
    """
    __timestamp: str
    """
    The timestamp at which the session has been created.
    """
    __directory: str
    """
    The directory of the JSON files.
    """
    __logger: Extractio_Logger
    """
    The logger that will all the action of the application.
    """

    def __init__(self, search: str, value: str) -> None:
        """
        Instantiating the media's manager which will interact with
        the media's dataset and do the required processing.

        Parameters:
            search: (string):   The uniform resource locator to be searched.
            value:  (string):   The value of the required media which have to correspond to the name of the platform from which the media comes from.
        """
        ENV = Environment()
        self.setDirectory(
            f"{ENV.getDirectory()}/Cache/Media"
        )
        self.setLogger(Extractio_Logger())
        self.getLogger().setLogger(logging.getLogger(__name__))
        self.setDatabaseHandler(Database_Handler())
        self.setSearch(search)
        self.setValue(value)
        self.getLogger().inform("The Media Management System has been initialized!")

    def getSearch(self) -> str:
        return self.__search

    def setSearch(self, search: str) -> None:
        self.__search = search

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

    def getLogger(self) -> Extractio_Logger:
        return self.__logger

    def setLogger(self, logger: Extractio_Logger) -> None:
        self.__logger = logger

    def verifyPlatform(self) -> dict[str, int | dict[str, int | dict[str, str | int | None]]] | dict[str, int | str]:
        """
        Verifying the uniform resource locator in order to switch to
        the correct system as well as select and return the correct
        response.

        Return:
            (object)
        """
        response: dict[str, int | dict[str, int | dict[str, str | int | None]]] | dict[str, int | str]
        media = self.getMedia()
        error_message: str
        if media["status"] == 200:
            self.setIdentifier(int(media["data"][0][0]))  # type: ignore
        else:
            error_message = "The content does not come from YouTube!"
            self.getLogger().error(error_message)
            raise Exception(error_message)
        if "youtube" in self.getValue() or "youtu.be" in self.getValue():
            response = {
                "status": 200,
                "data": self.handleYouTube()
            }
            self.getLogger().inform(
                f"The data from YouTube has been handled successfully!\nStatus: {response['status']}"
            )
        else:
            error_message = "This application cannot retrieve content from that application!"
            response = {
                "status": 403,
                "error": error_message
            }
            self.getLogger().error(
                f"{error_message}\nStatus: {response['status']}"
            )
        return response

    def getMedia(self) -> dict[str, int | str | list[RowType]]:
        """
        Retrieving the Media data from the Media table.

        Return:
            (object)
        """
        response: dict[str, int | str | list[RowType]]
        filter_parameters = tuple([self.getValue()])
        media = self.getDatabaseHandler().get_data(
            parameters=filter_parameters,
            table_name="Media",
            filter_condition="value = %s"
        )
        self.setTimestamp(datetime.now().strftime("%Y-%m-%d - %H:%M:%S"))
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

    def retrieveYouTubeIdentifier(self, identifier: str) -> str:
        """
        Retrieving the identifier of the content in the condition
        that it is in a playlist.

        Parameters:
            identifier: (string):   The ID of the content.

        Return:
            (string)
        """
        if "&" in identifier:
            return identifier.rsplit("&", 1)[0]
        else:
            return identifier

    def handleYouTube(self) -> dict[str, int | dict[str, str | int | None]]:
        """
        Handling the data throughout the You Tube Downloader which
        will depend on the referer.

        Return:
            (object)
        """
        response: dict[str, int | dict[str, str | int | None]]
        identifier: str
        self._YouTubeDownloader = YouTube_Downloader(
            self.getSearch(),
            self.getIdentifier()
        )
        youtube = self._YouTubeDownloader.search()
        media = {
            "Media": {
                "YouTube": youtube
            }
        }
        if "youtube" in self.getSearch():
            identifier = self.retrieveYouTubeIdentifier(
                self.getSearch().replace(
                    "https://www.youtube.com/watch?v=",
                    ""
                )
            )
        else:
            identifier = self.getSearch().replace(
                "https://youtu.be/",
                ""
            ).rsplit("?")[0]
        filename = f"{self.getDirectory()}/{identifier}.json"
        file = open(filename, "w")
        file.write(json.dumps(media, indent=4))
        file.close()
        response = {
            "status": 200,
            "data": youtube
        }
        return response
