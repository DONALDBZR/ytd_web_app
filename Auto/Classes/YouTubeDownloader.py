from pytube import YouTube
from datetime import datetime
from mysql.connector.types import RowType
from typing import Dict, List, Tuple, Union
from time import strftime, gmtime
import sys
import os


sys.path.append(os.getcwd())
from Models.DatabaseHandler import Database_Handler
from Models.Logger import Extractio_Logger



class YouTube_Downloader:
    """
    It will handle every operations related to YouTube.
    """
    __uniform_resource_locator: str
    """
    The uniform resource locator to be searched.
    """
    __video: YouTube
    """
    Core developer interface for pytube.
    """
    __title: str
    """
    The title of the video.
    """
    __identifier: str
    """
    The identifier of the video.
    """
    __length: int
    """
    The length of the video in seconds.
    """
    __duration: str
    """
    The duration of the video in the format of HH:mm:ss.
    """
    __published_at: Union[str, datetime, None]
    """
    The date at which the video has been published.
    """
    __database_handler: Database_Handler
    """
    It is the object relational mapper that will be used to
    simplify the process to entering queries.
    """
    __author: str
    """
    The author of the video/music.
    """
    __media_identifier: int
    """
    The media type for the system.
    """
    __timestamp: str
    """
    The timestamp at which the session has been created.
    """
    __directory: str
    """
    The directory of the media files.
    """
    __logger: Extractio_Logger
    """
    The logger that will all the action of the application.
    """

    def __init__(self, uniform_resource_locator: str, media_identifier: int):
        """
        Instantiating the class and launching the operations needed.

        Parameters:
            uniform_resource_locator:   (string):   The uniform resource locator to be searched.
            media_identifier:           (int):      The media type for the system.
        """
        self.setLogger(Extractio_Logger(__name__))
        self.setDatabaseHandler(Database_Handler())
        self.setUniformResourceLocator(uniform_resource_locator)
        self.setMediaIdentifier(media_identifier)
        self.getLogger().inform("The Downloader has been initialized")

    def getUniformResourceLocator(self) -> str:
        return self.__uniform_resource_locator

    def setUniformResourceLocator(self, uniform_resource_locator: str) -> None:
        self.__uniform_resource_locator = uniform_resource_locator

    def getVideo(self) -> YouTube:
        return self.__video

    def setVideo(self, video: YouTube) -> None:
        self.__video = video

    def getTitle(self) -> str:
        return self.__title

    def setTitle(self, title: str) -> None:
        self.__title = title

    def getIdentifier(self) -> str:
        return self.__identifier

    def setIdentifier(self, identifier: str) -> None:
        self.__identifier = identifier

    def getLength(self) -> int:
        return self.__length

    def setLength(self, length: int) -> None:
        self.__length = length

    def getDuration(self) -> str:
        return self.__duration

    def setDuration(self, duration: str) -> None:
        self.__duration = duration

    def getPublishedAt(self) -> Union[str, datetime, None]:
        return self.__published_at

    def setPublishedAt(self, published_at: Union[str, datetime, None]) -> None:
        self.__published_at = str(published_at)

    def getDatabaseHandler(self) -> Database_Handler:
        return self.__database_handler

    def setDatabaseHandler(self, database_handler: Database_Handler) -> None:
        self.__database_handler = database_handler

    def getAuthor(self) -> str:
        return self.__author

    def setAuthor(self, author: str) -> None:
        self.__author = author

    def getMediaIdentifier(self) -> int:
        return self.__media_identifier

    def setMediaIdentifier(self, media_identifier: int) -> None:
        self.__media_identifier = media_identifier

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

    def retrieveIdentifier(self, identifier: str) -> str:
        """
        Retrieving the identifier of the content in the condition
        that it is in a playlist.

        Parameters:
            identifier: string: The ID of the content.

        Returns:
            string
        """
        return identifier.rsplit("&", 1)[0] if "&" in identifier else identifier

    def search(self) -> Dict[str, Union[str, int, None]]:
        """
        Searching for the video in YouTube.

        Returns:
            {uniform_resource_locator: string, author: string, title: string, identifier: string, author_channel: string, views: int, published_at: string, thumbnail: string, duration: string, audio_file: string|null, video_file: string|null}
        """
        self.setVideo(YouTube(self.getUniformResourceLocator()))
        self.setIdentifier(self.getUniformResourceLocator())
        self.setIdentifier(self.retrieveIdentifier(self.getIdentifier().replace("https://www.youtube.com/watch?v=", ""))) if "youtube" in self.getUniformResourceLocator() else self.setIdentifier(self.getIdentifier().replace("https://youtu.be/", "").rsplit("?")[0])
        meta_data: Dict[str, Union[int, List[RowType], str]] = self.getYouTube()
        self.setLength(int(meta_data["data"][0]["length"])) if meta_data["status"] == 200 else self.setLength(self.getVideo().length) # type: ignore
        self.setPublishedAt(str(meta_data["data"][0]["published_at"])) if meta_data["status"] == 200 else self.setPublishedAt(self.getVideo().publish_date) # type: ignore
        self.setAuthor(str(meta_data["data"][0]["author"])) if meta_data["status"] == 200 else self.setAuthor(self.getVideo().author) # type: ignore
        self.setTitle(str(meta_data["data"][0]["title"])) if meta_data["status"] == 200 else self.setTitle(self.getVideo().title) # type: ignore
        self.setDuration(strftime("%H:%M:%S", gmtime(self.getLength()))) if meta_data["status"] == 200 else self.setDuration(strftime("%H:%M:%S", gmtime(self.getLength())))
        File_Location: Union[Dict[str, Union[str, None]], None] = self._getFileLocations(meta_data["data"]) if meta_data["status"] == 200 else None # type: ignore
        audio_file: Union[str, None] = File_Location["audio_file"] if File_Location != None else None
        video_file: Union[str, None] = File_Location["audio_file"] if File_Location != None else None
        if meta_data["status"] != 200:
            self.postYouTube()
        return {
            "uniform_resource_locator": self.getUniformResourceLocator(),
            "author": self.getAuthor(),
            "title": self.getTitle(),
            "identifier": self.getIdentifier(),
            "author_channel": self.getVideo().channel_url,
            "views": self.getVideo().views,
            "published_at": str(self.getPublishedAt()),
            "thumbnail": self.getVideo().thumbnail_url,
            "duration": self.getDuration(),
            "audio_file": audio_file,
            "video_file": video_file
        }

    def _getFileLocations(self, result_set: List[RowType]) -> Dict[str, Union[str, None]]:
        """
        Extracting the file locations on the application's
        directory.

        Parameters:
            result_set: [{author: string, title: string, identifier: string, published_at: string, length: int, location: string}]: The data from the database server.

        Returns:
            {audio_file: string|null, video_file: string|null}
        """
        audio_file: Union[str, None] = str(result_set[0]["location"]) if len(result_set) == 2 else None # type: ignore
        video_file: Union[str, None] = str(result_set[1]["location"]) if len(result_set) == 2 else None # type: ignore
        return {
            "audio_file": audio_file,
            "video_file": video_file
        }

    def getYouTube(self) -> Dict[str, Union[int, List[RowType], str]]:
        """
        Retrieving the metadata from the YouTube table.

        Returns:
            {status: int, data: [{author: string, title: string, identifier: string, published_at: string, length: int, location: string}], timestamp: string}
        """
        filter_parameters: Tuple[str] = (self.getIdentifier(),)
        media: List[RowType] = self.getDatabaseHandler().getData(
            parameters=filter_parameters,
            table_name="YouTube",
            join_condition="MediaFile ON MediaFile.YouTube = YouTube.identifier",
            filter_condition="YouTube.identifier = %s",
            column_names="author, title, YouTube.identifier, published_at, length, location",
            sort_condition="MediaFile.identifier ASC",
            limit_condition=2
        )
        self.setTimestamp(datetime.now().strftime("%Y-%m-%d - %H:%M:%S"))
        self.getLogger().inform(f"The media content has been retrieved from the database server!\nContent Amount: {len(media)}\nCurrent Media: {media}")
        status: int = 404 if len(media) == 0 else 200
        return {
            "status": status,
            "data": media,
            "timestamp": self.getTimestamp()
        }

    def postYouTube(self) -> None:
        """
        Creating a record for the media with its data.

        Returns:
            void
        """
        data: Tuple[str, int, Union[str, datetime, None], str, str, int] = (self.getIdentifier(), self.getLength(), self.getPublishedAt(), self.getAuthor(), self.getTitle(), self.getMediaIdentifier())
        self.getLogger().inform(f"Data to be inserted into the database server.\nIdentifier: {self.getIdentifier()}\nLength: {self.getLength()}\nPublished At: {self.getPublishedAt()}\nAuthor: {self.getAuthor()}\nTitle: {self.getTitle()}\nMedia's Identifier: {self.getMediaIdentifier()}")
        self.getDatabaseHandler().postData(
            table="YouTube",
            columns="identifier, length, published_at, author, title, Media",
            values="%s, %s, %s, %s, %s, %s",
            parameters=data
        )
