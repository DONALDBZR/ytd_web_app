from pytube import YouTube, StreamQuery, Stream
from Models.DatabaseHandler import Database_Handler
from datetime import datetime
from Models.Logger import Extractio_Logger
from Environment import Environment
from mysql.connector.types import RowType
from urllib.error import HTTPError
from typing import Dict, Tuple, Union, List
from os.path import isfile
from time import strftime, gmtime
import os
import logging


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
    __streams: StreamQuery
    """
    Interface for querying the available media streams.
    """
    __stream: Union[Stream, None]
    """
    Container for stream manifest data.
    """
    __itag: int
    """
    YouTube format identifier code
    """
    __mime_type: str
    """
    Two-part identifier for file formats and format contents
    composed of a "type" and a "subtype".
    """
    __logger: Extractio_Logger
    """
    The logger that will all the action of the application.
    """

    def __init__(self, uniform_resource_locator: str, media_identifier: int):
        """
        Instantiating the class and launching the operations needed.

        Parameters:
            uniform_resource_locator: string: The uniform resource locator to be searched.
            media_identifier: int: The media type for the system.
        """
        ENV = Environment()
        self.setDirectory(f"{ENV.getDirectory()}/Public")
        self.setLogger(Extractio_Logger())
        self.getLogger().setLogger(logging.getLogger(__name__))
        self.mediaDirectory()
        self.setDatabaseHandler(Database_Handler())
        self.getDatabaseHandler()._query(
            query="CREATE TABLE IF NOT EXISTS `YouTube` (identifier VARCHAR(16) PRIMARY KEY, `length` INT, published_at VARCHAR(32), author VARCHAR(64), title VARCHAR(128), `Media` INT, CONSTRAINT fk_Media_type FOREIGN KEY (`Media`) REFERENCES `Media` (identifier))",
            parameters=None
        )
        self.getDatabaseHandler()._execute()
        self.getDatabaseHandler()._query(
            query="CREATE TABLE IF NOT EXISTS `MediaFile` (identifier INT PRIMARY KEY AUTO_INCREMENT, `type` VARCHAR(64), date_downloaded VARCHAR(32), date_deleted VARCHAR(32) NULL, location VARCHAR(128), `YouTube` VARCHAR(16), CONSTRAINT fk_source FOREIGN KEY (`YouTube`) REFERENCES `YouTube` (identifier))",
            parameters=None
        )
        self.getDatabaseHandler()._execute()
        self.setUniformResourceLocator(uniform_resource_locator)
        self.setMediaIdentifier(media_identifier)
        self.getLogger().inform("The YouTube Downloader has been successfully been initialized!")

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

    def getStreams(self) -> StreamQuery:
        return self.__streams

    def setStreams(self, streams: StreamQuery) -> None:
        self.__streams = streams

    def getStream(self) -> Union[Stream, None]:
        return self.__stream

    def setStream(self, stream: Union[Stream, None]) -> None:
        self.__stream = stream

    def getITAG(self) -> int:
        return self.__itag

    def setITAG(self, itag: int) -> None:
        self.__itag = itag

    def getMimeType(self) -> str:
        return self.__mime_type

    def setMimeType(self, mime_type: str) -> None:
        self.__mime_type = mime_type

    def getLogger(self) -> Extractio_Logger:
        return self.__logger

    def setLogger(self, logger: Extractio_Logger) -> None:
        self.__logger = logger

    def sanitizeYouTubeIdentifier(self) -> None:
        """
        Sanitizing the identifier of the content from the platform
        YouTube.

        Returns:
            void
        """
        if "youtube" in self.getUniformResourceLocator():
            self.setIdentifier(self.getIdentifier().replace("https://www.youtube.com/watch?v=", "").rsplit("&", 1)[0]) if "&" in self.getIdentifier() else self.setIdentifier(self.getIdentifier().replace("https://www.youtube.com/watch?v=", ""))
        else:
            self.setIdentifier(self.getIdentifier().replace("https://youtu.be/", "").rsplit("?")[0].rsplit("&", 1)[0]) if "&" in self.getIdentifier() else self.getIdentifier().replace("https://youtu.be/", "").rsplit("?")[0]

    def search(self) -> Dict[str, Union[str, int, None]]:
        """
        Searching for the video in YouTube.

        Returns:
            {uniform_resource_locator: string, author: string, title: string, identifier: string, author_channel: string, views: int, published_at: string | Datetime | null, thumbnail: string, duration: string, audio_file: string, video_file: string}
        """
        self.setVideo(YouTube(self.getUniformResourceLocator()))
        self.setIdentifier(self.getUniformResourceLocator())
        self.sanitizeYouTubeIdentifier()
        meta_data: Dict[str, Union[int, List[Dict[str, Union[str, int]]], str]] = self.getYouTube()
        file_locations: Dict[str, Union[str, None]] = self._getFileLocations(list(meta_data["data"])) # type: ignore
        self.setLength(int(meta_data["data"][0]["length"])) if int(str(meta_data["status"])) == 200 else self.setLength(self.getVideo().length) # type: ignore
        self.setPublishedAt(str(meta_data["data"][0]["published_at"])) if int(str(meta_data["status"])) == 200 else self.setPublishedAt(self.getVideo().publish_date) # type: ignore
        self.setAuthor(str(meta_data["data"][0]["author"])) if int(str(meta_data["status"])) == 200 else self.setAuthor(self.getVideo().author) # type: ignore
        self.setTitle(str(meta_data["data"][0]["title"])) if int(str(meta_data["status"])) == 200 else self.setTitle(self.getVideo().title) # type: ignore
        self.setDuration(strftime("%H:%M:%S", gmtime(self.getLength()))) if int(str(meta_data["status"])) == 200 else self.setDuration(strftime("%H:%M:%S", gmtime(self.getLength())))
        audio_file: Union[str, None] = file_locations["audio_file"] if int(str(meta_data["status"])) == 200 else None
        video_file: Union[str, None] = file_locations["video_file"] if int(str(meta_data["status"])) == 200 else None
        if int(meta_data["status"]) != 200: # type: ignore
            self.postYouTube()
        return {
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

    def _getFileLocations(self, result_set: List[Dict[str, Union[str, int]]]) -> Dict[str, Union[str, None]]:
        """
        Extracting the file location of the media content on the
        server.

        Parameters:
            result_set: [{author: string, title: string, identifier: string, published_at: string, length: int, location: string}]: The data from the database server.

        Returns:
            {audio_file: string | null, video_file: string | null}
        """
        if len(result_set) == 2:
            return {
                "audio_file": str(result_set[0]["location"]), # type: ignore
                "video_file": str(result_set[1]["location"]) # type: ignore
            }
        return {
            "audio_file": None,
            "video_file": None
        }

    def getYouTube(self) -> Dict[str, Union[int, List[Dict[str, Union[str, int]]], str]]:
        """
        Retrieving the metadata from the YouTube table.

        Returns:
            {status: int, data: [{author: string, title: string, identifier: string, published_at: string, length: int, location: string}], timestamp: string}
        """
        filter_parameters: Tuple[str] = (self.getIdentifier(),)
        media: Union[List[RowType], List[Dict[str, Union[str, int]]]] = self.getDatabaseHandler().getData(
            parameters=filter_parameters,
            table_name="YouTube",
            join_condition="MediaFile ON MediaFile.YouTube = YouTube.identifier",
            filter_condition="YouTube.identifier = %s",
            column_names="author, title, YouTube.identifier, published_at, length, location",
            sort_condition="MediaFile.identifier ASC",
            limit_condition=2
        )
        self.setTimestamp(datetime.now().strftime("%Y-%m-%d - %H:%M:%S"))
        response: Dict[str, Union[int, List[Dict[str, Union[str, int]]], str]]
        if len(media) == 0:
            response = {
                'status': 204,
                'data': media, # type: ignore
                'timestamp': self.getTimestamp()
            }
        else:
            response = {
                'status': 200,
                'data': media, # type: ignore
                'timestamp': self.getTimestamp()
            }
        return response

    def postYouTube(self) -> None:
        """
        Creating a record for the media with its data.

        Returns:
            void
        """
        data: Tuple[str, int, Union[str, datetime, None], str, str, int] = (self.getIdentifier(), self.getLength(), self.getPublishedAt(), self.getAuthor(), self.getTitle(), self.getMediaIdentifier())
        self.getDatabaseHandler().postData(
            table="YouTube",
            columns="identifier, length, published_at, author, title, Media",
            values="%s, %s, %s, %s, %s, %s",
            parameters=data
        )

    def mediaDirectory(self):
        """
        Creating the directories for storing the media files.

        Return:
            (void)
        """
        if not os.path.exists(f"{self.getDirectory()}/Video"):
            os.makedirs(f"{self.getDirectory()}/Video")
        if not os.path.exists(f"{self.getDirectory()}/Audio"):
            os.makedirs(f"{self.getDirectory()}/Audio")

    def retrievingStreams(self) -> Dict[str, Union[str, int]]:
        """
        Downloading the contents of the media from the platform to
        save on the server.

        Returns:
            {uniform_resource_locator: string, author: string, title: string, identifier: string, author_channel: string, views: int, published_at: string, thumbnail: string, duration: string, audio: string, video: string}
        """
        response: Dict[str, Union[str, int]]
        metadata: Dict[str, Union[str, int, None]] = self.search()
        self.setIdentifier(str(metadata["identifier"]))
        audio_file_location: str = f"{self.getDirectory()}/Audio/{self.getIdentifier()}.mp3"
        video_file_location: str = f"{self.getDirectory()}/Video/{self.getIdentifier()}.mp4"
        if isfile(audio_file_location) == False and isfile(video_file_location) == False:
            self.setVideo(YouTube(self.getUniformResourceLocator()))
            self.getDatabaseHandler()._execute()
            self.setStreams(self.getVideo().streams)
            audio_file_location = self.getAudioFile()
            video_file_location = self.getVideoFile()
        self.getLogger().inform("The media content has been downloaded!")
        return {
            "uniform_resource_locator": self.getUniformResourceLocator(),
            "author": self.getAuthor(),
            "title": self.getTitle(),
            "identifier": self.getIdentifier(),
            "author_channel": self.getVideo().channel_url,
            "views": self.getVideo().views,
            "published_at": self.getPublishedAt(),  # type: ignore
            "thumbnail": self.getVideo().thumbnail_url,
            "duration": self.getDuration(),
            "audio": audio_file_location,
            "video": video_file_location
        }

    def getAudioFile(self) -> str:
        """
        Retrieving the audio file and saving it on the server as
        well as adding its meta data in the database.

        Returns:
            string
        """
        streams: List[Stream] = [stream for stream in self.getStreams().filter(mime_type="audio/mp4", abr="128kbps", audio_codec="mp4a.40.2")]
        if streams:
            self.setITAG(streams[0].itag)
            self.setStream(self.getStreams().get_by_itag(self.getITAG()))
            self.setMimeType("audio/mp3")
            return self.__downloadAudio()
        return ""

    def getVideoFile(self) -> str:
        """
        Retrieving the video file and saving it on the server as
        well as adding its meta data in the database.

        Returns:
            string
        """
        streams: List[Stream] = [stream for stream in self.getStreams().filter(mime_type="video/mp4", audio_codec="mp4a.40.2", resolution="720p")]
        if streams:
            self.setITAG(streams[0].itag)
            self.setStream(self.getStreams().get_by_itag(self.getITAG()))
            self.setMimeType("video/mp4")
            return self.__downloadVideo()
        return ""

    def __downloadVideo(self) -> str:
        """
        Recursively downloading the video data from YouTube's main
        data center.

        Returns:
            string
        """
        file_path: str = f"{self.getDirectory()}/Video/{self.getIdentifier()}.mp4"
        try:
            self.getStream().download( # type: ignore
                output_path=f"{self.getDirectory()}/Video",
                filename=f"{self.getIdentifier()}.mp4"
            )
            self.setTimestamp(datetime.now().strftime("%Y-%m-%d - %H:%M:%S"))
            data: Tuple[str, str, str, str] = (self.getMimeType(), self.getTimestamp(), file_path, self.getIdentifier())
            self.getDatabaseHandler().postData(
                table="MediaFile",
                columns="type, date_downloaded, location, YouTube",
                values="%s, %s, %s, %s",
                parameters=data
            )
            return file_path
        except HTTPError as error:
            self.getLogger().error(f"Error occured while the application was trying to download the media content.  The application will retry to download it.\nError: {error}")
            return file_path if "403" in str(error) else ""

    def __downloadAudio(self) -> str:
        """
        Recursively downloading the audio data from YouTube's main
        data center.

        Returns:
            string
        """
        file_path: str = f"{self.getDirectory()}/Audio/{self.getIdentifier()}.mp3"
        try:
            self.getStream().download(  # type: ignore
                output_path=f"{self.getDirectory()}/Audio",
                filename=f"{self.getIdentifier()}.mp3"
            )
            self.setTimestamp(datetime.now().strftime("%Y-%m-%d - %H:%M:%S"))
            data: Tuple[str, str, str, str] = (self.getMimeType(), self.getTimestamp(), file_path, self.getIdentifier())
            self.getDatabaseHandler().postData(
                table="MediaFile",
                columns="type, date_downloaded, location, YouTube",
                values="%s, %s, %s, %s",
                parameters=data
            )
            return file_path
        except HTTPError as error:
            self.getLogger().error(
                f"Error occured while the application was trying to download the media content.  The application will retry to download it.\nError: {error}"
            )
            return file_path if "403" in str(error) else ""
