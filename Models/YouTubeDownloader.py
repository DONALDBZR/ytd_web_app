from Models.DatabaseHandler import Database_Handler
from datetime import datetime
from Models.Logger import Extractio_Logger
from Environment import Environment
from mysql.connector.types import RowType
from urllib.error import HTTPError
from yt_dlp import YoutubeDL
from typing import Dict, Union, List, Tuple
from time import strftime, gmtime
from os.path import isfile, exists
from os import makedirs


class YouTube_Downloader:
    """
    It will handle every operations related to YouTube.
    """
    __uniform_resource_locator: str
    """
    The uniform resource locator to be searched.
    """
    __video: YoutubeDL
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
    __streams: List[Dict[str, Union[str, int, float, List[Dict[str, Union[str, float]]], None, Dict[str, str]]]]
    """
    The list of the streams
    """
    __stream: Dict[str, Union[str, int, float, List[Dict[str, Union[str, float]]], None, Dict[str, str]]]
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
        ENV: Environment = Environment()
        self.setDirectory(f"{ENV.getDirectory()}/Public")
        self.setLogger(Extractio_Logger(__name__))
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

    def getVideo(self) -> YoutubeDL:
        return self.__video

    def setVideo(self, video: YoutubeDL) -> None:
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

    def getStreams(self) -> List[Dict[str, Union[str, int, float, List[Dict[str, Union[str, float]]], None, Dict[str, str]]]]:
        return self.__streams

    def setStreams(self, streams: List[Dict[str, Union[str, int, float, List[Dict[str, Union[str, float]]], None, Dict[str, str]]]]) -> None:
        self.__streams = streams

    def getStream(self) -> Dict[str, Union[str, int, float, List[Dict[str, Union[str, float]]], None, Dict[str, str]]]:
        return self.__stream

    def setStream(self, stream: Dict[str, Union[str, int, float, List[Dict[str, Union[str, float]]], None, Dict[str, str]]]) -> None:
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

    def retrieveIdentifier(self, identifier: str) -> str:
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
            {uniform_resource_locator: string, author: string, title: string, identifier: string, author_channel: string, views: int, published_at: string, thumbnail: string, duration: string, audio_file: string|null, video_file: string|null}
        """
        options: Dict[str, bool] = {
            "quiet": True,
            "skip_download": True
        }
        self.setVideo(YoutubeDL(options))
        self.setIdentifier(self.getUniformResourceLocator())
        identifier: str = self.retrieveIdentifier(self.getIdentifier().replace("https://www.youtube.com/watch?v=", "")) if "youtube" in self.getUniformResourceLocator() else self.retrieveIdentifier(self.getIdentifier().replace("https://youtu.be/", "").rsplit("?")[0])
        self.setIdentifier(identifier)
        youtube = self.getVideo().extract_info(self.getUniformResourceLocator(), download=False)
        meta_data: Dict[str, Union[int, List[RowType], str]] = self.getYouTube()
        self.setLength(int(meta_data["data"][0]["length"]) if meta_data["status"] == 200 else int(youtube["duration"])) # type: ignore
        published_date: str = youtube["upload_date"] # type: ignore
        published_at: str = str(meta_data["data"][0]["published_at"]) if meta_data["status"] == 200 else f"{published_date[:4]}-{published_date[4:6]}-{published_date[6:]}" # type: ignore
        self.setPublishedAt(published_at)
        self.setAuthor(str(meta_data["data"][0]["author"]) if meta_data["status"] == 200 else str(youtube["uploader"])) # type: ignore
        self.setTitle(str(meta_data["data"][0]["title"]) if meta_data["status"] == 200 else str(youtube["title"])) # type: ignore
        self.setDuration(strftime("%H:%M:%S", gmtime(self.getLength())))
        file_locations: Dict[str, Union[str, None]] = self._getFileLocations(list(meta_data["data"])) if meta_data["status"] == 200 else {} # type: ignore
        audio_file: Union[str, None] = file_locations["audio_file"] if meta_data["status"] == 200 else None
        video_file: Union[str, None] = file_locations["video_file"] if meta_data["status"] == 200 else None
        if meta_data["status"] != 200:
            self.postYouTube()
        return {
            "uniform_resource_locator": self.getUniformResourceLocator(),
            "author": self.getAuthor(),
            "title": self.getTitle(),
            "identifier": self.getIdentifier(),
            "author_channel": str(youtube["uploader_url"]),  # type: ignore
            "views": int(youtube["view_count"]),  # type: ignore
            "published_at": self.getPublishedAt(),  # type: ignore
            "thumbnail": str(youtube["thumbnail"]),  # type: ignore
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

    def getYouTube(self) -> Dict[str, Union[int, List[RowType], str]]:
        """
        Retrieving the metadata from the YouTube table.

        Returns:
            {status: int, data: [{author: string, title: string, identifier: string, published_at: string, length: int, location: string|null}, timestamp: string]}
        """
        filter_parameters: Tuple[str] = (self.getIdentifier(),)
        media: List[RowType] = self.getDatabaseHandler().getData(
            parameters=filter_parameters, # type: ignore
            table_name="YouTube",
            join_condition="MediaFile ON MediaFile.YouTube = YouTube.identifier",
            filter_condition="YouTube.identifier = %s",
            column_names="author, title, YouTube.identifier, published_at, length, location",
            sort_condition="MediaFile.identifier ASC",
            limit_condition=2
        )
        self.setTimestamp(datetime.now().strftime("%Y-%m-%d - %H:%M:%S"))
        status: int = 200 if len(media) != 0 else 204
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
        self.getDatabaseHandler().postData(
            table="YouTube",
            columns="identifier, length, published_at, author, title, Media",
            values="%s, %s, %s, %s, %s, %s",
            parameters=data # type: ignore
        )

    def mediaDirectory(self) -> None:
        """
        Creating the directories for storing the media files.

        Return:
            void
        """
        if not exists(f"{self.getDirectory()}/Video"):
            makedirs(f"{self.getDirectory()}/Video")
        if not exists(f"{self.getDirectory()}/Audio"):
            makedirs(f"{self.getDirectory()}/Audio")

    def retrievingStreams(self) -> Dict[str, Union[str, int, None]]:
        """
        Downloading the contents of the media from the platform to
        save on the server.

        Return:
            {uniform_resource_locator: string, author: string, title: string, identifier: string, author_channel: string, views: int, published_at: string, thumbnail: string, duration: string, audio: string|null, video: string|null}
        """
        metadata: Dict[str, Union[str, int, None]] = self.search()
        self.setIdentifier(str(metadata["identifier"]))
        audio_file_location: str = f"{self.getDirectory()}/Audio/{self.getIdentifier()}.mp3"
        video_file_location: str = f"{self.getDirectory()}/Video/{self.getIdentifier()}.mp4"
        options: Dict[str, bool] = {
            "quiet": True,
            "listformats": True
        }
        if isfile(audio_file_location) == False and isfile(video_file_location) == False:
            self.setVideo(YoutubeDL(options))
            self.getDatabaseHandler()._execute()
            info = self.getVideo().extract_info(self.getUniformResourceLocator(), download=False)
            self.setStreams(info["formats"]) # type: ignore
            audio_file_location = self.getAudioFile()
            video_file_location = self.getVideoFile()
        self.getLogger().inform(f"The media content has been downloaded!\nAudio: {audio_file_location}\nVideo: {video_file_location}")
        return {
            "uniform_resource_locator": self.getUniformResourceLocator(),
            "author": self.getAuthor(),
            "title": self.getTitle(),
            "identifier": self.getIdentifier(),
            "author_channel": str(metadata["author_channel"]),
            "views": int(metadata["views"]),  # type: ignore
            "published_at": self.getPublishedAt(),  # type: ignore
            "thumbnail": str(metadata["thumbnail"]),  # type: ignore
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
        audio_streams: List[Dict[str, Union[str, int, float, List[Dict[str, Union[str, float]]], None, Dict[str, str]]]] = [stream for stream in self.getStreams() if stream["abr"] != None and stream["abr"] != 0 and "mp4a" in stream["acodec"]] # type: ignore
        adaptive_bitrate: float = float(max(audio_streams, key=lambda stream: stream["abr"])["abr"]) # type: ignore
        self.setStream([stream for stream in audio_streams if stream["abr"] == adaptive_bitrate][0])
        self.setMimeType("audio/mp3")
        response: str = self.__downloadAudio() if self.getStream() != None else ""
        return response

    def getVideoFile(self) -> str:
        """
        Retrieving the video file and saving it on the server as
        well as adding its meta data in the database.

        Returns:
            string
        """
        self.setMimeType("video/mp4")
        return self.__downloadVideo()

    def __downloadVideo(self) -> str:
        """
        Recursively downloading the video data from YouTube's main
        data center.

        Returns:
            string
        """
        response: str = ""
        audio_streams: List[Dict[str, Union[str, int, float, List[Dict[str, Union[str, float]]], None, Dict[str, str]]]] = [stream for stream in self.getStreams() if (stream.get("abr") is not None and stream.get("abr") != 0.00) and "mp4a" in str(stream.get("acodec"))]
        if len(audio_streams) == 0:
            self.getLogger().error(f"There is not valid audio stream available.\nStatus: 503")
            return response
        adaptive_bitrate: float = float(max(audio_streams, key=lambda stream: stream["abr"])["abr"]) # type: ignore
        self.setStream([stream for stream in audio_streams if stream["abr"] == adaptive_bitrate][0])
        audio_stream: Dict[str, Union[str, int, float, List[Dict[str, Union[str, float]]], None, Dict[str, str]]] = self.getStream()
        video_streams: List[Dict[str, Union[str, int, float, List[Dict[str, Union[str, float]]], None, Dict[str, str]]]] = [stream for stream in self.getStreams() if stream.get("vbr") is not None and stream.get("vbr") != 0.00]
        if len(video_streams) == 0:
            self.getLogger().error(f"There is not valid video stream available.\nStatus: 503")
            return response
        height: int = int(max(video_streams, key=lambda stream: stream["height"])["height"]) # type: ignore
        width: int = int(max(video_streams, key=lambda stream: stream["width"])["width"]) # type: ignore
        video_streams = [stream for stream in video_streams if stream.get("height") == height and stream.get("width") == width and "avc" in str(stream.get("vcodec")) and "filesize" in stream]
        if not video_streams:
            self.getLogger().error(f"There is not valid video stream available.\nStatus: 503")
            return response
        file_size: int = int(max(video_streams, key=lambda stream: stream["filesize"])["filesize"]) # type: ignore
        self.setStream([stream for stream in video_streams if stream.get("filesize") == file_size][0])
        video_stream: Dict[str, Union[str, int, float, List[Dict[str, Union[str, float]]], None, Dict[str, str]]] = self.getStream()
        file_name: str = f"{self.getIdentifier()}.mp4"
        file_path: str = f"{self.getDirectory()}/Video/{file_name}"
        options: Dict[str, str] = {
            "format": f"{video_stream['format_id']}+{audio_stream['format_id']}",
            "merge_output_format": "mp4",
            "outtmpl": file_path
        }
        self.setVideo(YoutubeDL(options))
        self.getVideo().download([self.getUniformResourceLocator()])
        data: Tuple[str, str, str, str] = (self.getMimeType(), self.getTimestamp(), file_path, self.getIdentifier())
        self.getDatabaseHandler().postData(
            table="MediaFile",
            columns="type, date_downloaded, location, YouTube",
            values="%s, %s, %s, %s",
            parameters=data # type: ignore
        )
        return file_path

    def handleHttpError(self, error: HTTPError, file_path: str) -> str:
        """
        Handling the HTTP Errors accordingly as it must be noted
        that HTTP/403 is being caused as the application could not
        keep track of the file path which gets lost where the back
        end which acts the front-end of YouTube's datacenter,
        generates the HTTP/403 which in turn generate the HTTP/500
        into the application's front-end.

        Parameters:
            error: HTTPError: Raised when HTTP error occurs, but also acts like non-error return
            file_path: string: The path of the file.

        Returns:
            string
        """
        if "403" in str(error):
            return file_path
        else:
            return ""

    def __downloadAudio(self) -> str:
        """
        Recursively downloading the audio data from YouTube's main
        data center.

        Returns:
            string
        """
        file_name: str = f"{self.getIdentifier()}.mp3"
        file_path: str = f"{self.getDirectory()}/Audio/{file_name}"
        options: Dict[str, str] = {
            "format": str(self.getStream()["format_id"]),
            "outtmpl": file_path
        }
        self.setVideo(YoutubeDL(options))
        self.getVideo().download([self.getUniformResourceLocator()])
        data: Tuple[str, str, str, str] = (self.getMimeType(), self.getTimestamp(), file_path, self.getIdentifier())
        self.getDatabaseHandler().postData(
            table="MediaFile",
            columns="type, date_downloaded, location, YouTube",
            values="%s, %s, %s, %s",
            parameters=data # type: ignore
        )
        return file_path
