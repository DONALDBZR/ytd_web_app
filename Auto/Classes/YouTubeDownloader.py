from pytube import YouTube
from datetime import datetime
import time
import logging
import sys
import os


sys.path.append(os.getcwd())
from Models.DatabaseHandler import Database_Handler
from Models.Logger import Extractio_Logger
from Environment import Environment



class YouTube_Downloader:
    """
    It will handle every operations related to YouTube.
    """
    __uniform_resource_locator: str
    """
    The uniform resource locator to be searched.

    Type: string
    Visibility: private
    """
    __video: "YouTube"
    """
    Core developer interface for pytube.

    Type: YouTube
    Visibility: private
    """
    __title: str
    """
    The title of the video.

    Type: string
    Visibility: private
    """
    __identifier: str
    """
    The identifier of the video.

    Type: string
    Visibility: private
    """
    __length: int
    """
    The length of the video in seconds.

    Type: int
    Visibility: private
    """
    __duration: str
    """
    The duration of the video in the format of HH:mm:ss.

    Type: string
    Visibility: private
    """
    __published_at: str | datetime | None
    """
    The date at which the video has been published.

    Type: string
    Visibility: private
    """
    __database_handler: "Database_Handler"
    """
    It is the object relational mapper that will be used to
    simplify the process to entering queries.

    Type: Database_Handler
    Visibility: private
    """
    __author: str
    """
    The author of the video/music.

    Type: string
    Visibility: private
    """
    __media_identifier: int
    """
    The media type for the system.

    Type: int
    Visibility: private
    """
    __timestamp: str
    """
    The timestamp at which the session has been created.

    Type: string
    Visibility: private
    """
    __directory: str
    """
    The directory of the media files.

    Type: string
    Visibility: private
    """
    __logger: Extractio_Logger
    """
    The logger that will all the action of the application.

    Type: Extractio_Logger
    Visibility: private
    """

    def __init__(self, uniform_resource_locator: str, media_identifier: int):
        """
        Instantiating the class and launching the operations needed.

        Parameters:
            uniform_resource_locator:   string: The uniform resource locator to be searched.
            media_identifier:           int:    The media type for the system.
        """
        self.setLogger(Extractio_Logger())
        self.getLogger().setLogger(logging.getLogger("pytube"))
        self.setDatabaseHandler(Database_Handler())
        self.setUniformResourceLocator(uniform_resource_locator)
        self.setMediaIdentifier(media_identifier)
        self.getLogger().inform(
            f"Message: The Downloader has been initialized\nCurrent Time: {datetime.now()}"
        )

    def getUniformResourceLocator(self) -> str:
        return self.__uniform_resource_locator

    def setUniformResourceLocator(self, uniform_resource_locator: str) -> None:
        self.__uniform_resource_locator = uniform_resource_locator

    def getVideo(self) -> "YouTube":
        return self.__video

    def setVideo(self, video: "YouTube") -> None:
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

    def getPublishedAt(self) -> str | datetime | None:
        return self.__published_at

    def setPublishedAt(self, published_at: str | datetime | None) -> None:
        self.__published_at = str(published_at)

    def getDatabaseHandler(self) -> "Database_Handler":
        return self.__database_handler

    def setDatabaseHandler(self, database_handler: "Database_Handler") -> None:
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

        Returns: string
        """
        if "&" in identifier:
            return identifier.rsplit("&", 1)[0]
        else:
            return identifier

    def search(self) -> dict[str, str | int | None]:
        """
        Searching for the video in YouTube.

        Returns: object
        """
        self.setVideo(YouTube(self.getUniformResourceLocator()))
        self.setIdentifier(self.getUniformResourceLocator())
        if "youtube" in self.getUniformResourceLocator():
            self.setIdentifier(
                self.retrieveIdentifier(
                    self.getIdentifier().replace(
                        "https://www.youtube.com/watch?v=",
                        ""
                    )
                )
            )
        else:
            self.setIdentifier(
                self.getIdentifier().replace(
                    "https://youtu.be/",
                    ""
                ).rsplit("?")[0]
            )
        response: dict[str, str | int | None]
        meta_data = self.getYouTube()
        audio_file: str | None
        video_file: str | None
        # Verifying the response of the metadata to retrieve the needed response
        if meta_data["status"] == 200:
            self.setLength(int(meta_data["data"][0][4]))  # type: ignore
            self.setPublishedAt(str(meta_data["data"][0][3]))  # type: ignore
            self.setAuthor(str(meta_data["data"][0][0]))  # type: ignore
            self.setTitle(str(meta_data["data"][0][1]))  # type: ignore
            self.setDuration(
                time.strftime("%H:%M:%S", time.gmtime(self.getLength()))
            )
            # Verifying base on the length to set the file location
            if len(list(meta_data["data"])) == 2:  # type: ignore
                audio_file = str(meta_data["data"][0][5])  # type: ignore
                video_file = str(meta_data["data"][1][5])  # type: ignore
            else:
                audio_file = None
                video_file = None
        else:
            self.setLength(self.getVideo().length)
            self.setPublishedAt(self.getVideo().publish_date)
            self.setAuthor(self.getVideo().author)
            self.setTitle(self.getVideo().title)
            self.setDuration(
                time.strftime("%H:%M:%S", time.gmtime(self.getLength()))
            )
            audio_file = None
            video_file = None
            self.postYouTube()
        response = {
            "uniform_resource_locator": self.getUniformResourceLocator(),
            "author": self.getAuthor(),
            "title": self.getTitle(),
            "identifier": self.getIdentifier(),
            "author_channel": self.getVideo().channel_url,
            "views": self.getVideo().views,
            "published_at": self.getPublishedAt(),  # type: ignore
            "thumbnail": self.getVideo().thumbnail_url,
            "duration": self.getDuration(),
            "audio_file": audio_file,
            "video_file": video_file
        }
        return response

    def getYouTube(self) -> dict[str, int | list[tuple[str, str, str, str, int, str | None]] | str]:
        """
        Retrieving the metadata from the YouTube table.

        Returns: object
        """
        media = self.getDatabaseHandler().get_data(
            tuple([self.getIdentifier()]),
            "YouTube",
            "MediaFile ON MediaFile.YouTube = YouTube.identifier",
            "YouTube.identifier = %s",
            "author, title, YouTube.identifier, published_at, length, location",
            "MediaFile.identifier ASC",
            2
        )
        self.setTimestamp(datetime.now().strftime("%Y-%m-%d - %H:%M:%S"))
        response: dict[
            str, int | list[tuple[str, str, str, str, int, str | None]] | str
        ]
        self.getLogger().inform(
            f"Content Amount: {len(media)}\nCurrent Media: {datetime.now()}"
        )
        if len(media) == 0:
            response = {
                'status': 404,
                'data': media,  # type: ignore
                'timestamp': self.getTimestamp()
            }
        else:
            response = {
                'status': 200,
                'data': media,  # type: ignore
                'timestamp': self.getTimestamp()
            }
        return response

    def postYouTube(self) -> None:
        """
        Creating a record for the media with its data.

        Returns: void
        """
        self.getLogger().inform(
            f"Message: Data to be inserted into the database server.\nIdentifier: {self.getIdentifier()}\nLength: {self.getLength()}\nPublished At: {self.getPublishedAt()}\nAuthor: {self.getAuthor()}\nTitle: {self.getTitle()}\nMedia's Identifier: {self.getMediaIdentifier()}\nCurrent time: {datetime.now()}"
        )
        self.getDatabaseHandler().post_data(
            "YouTube",
            "identifier, length, published_at, author, title, Media",
            "%s, %s, %s, %s, %s, %s",
            (
                self.getIdentifier(),
                self.getLength(),
                self.getPublishedAt(),
                self.getAuthor(),
                self.getTitle(),
                self.getMediaIdentifier()
            )
        )
