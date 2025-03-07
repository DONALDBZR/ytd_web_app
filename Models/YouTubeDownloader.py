from Models.DatabaseHandler import Database_Handler, Extractio_Logger, Environment, RowType, Union, List, Tuple, Any, Relational_Database_Error
from datetime import datetime
from urllib.error import HTTPError
from yt_dlp import YoutubeDL
from typing import Dict
from time import strftime, gmtime
from os.path import isfile, exists
from os import makedirs
from html import escape
from Errors.ExtractioErrors import NotFoundError
from yt_dlp.utils import DownloadError


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
    __base_uniform_resouce_locator: str
    """
    The base uniform resource locator.
    """
    __audio_codec: str
    """
    The audio codec of the video.
    """
    __video_codec: str
    """
    The video codec of the video.
    """

    def __init__(self, uniform_resource_locator: str, media_identifier: int):
        """
        Initializing the YouTube Downloader class, setting up directories, logging, database tables, and default configurations.

        Parameters:
            uniform_resource_locator (string): The URL of the YouTube video to be processed.
            media_identifier (int): The identifier for the media type.

        Raises:
            Relational_Database_Error: If an error occurs while setting up the database.
        """
        ENV: Environment = Environment()
        self.setDirectory(f"{ENV.getDirectory()}/Public")
        self.setLogger(Extractio_Logger(__name__))
        self.mediaDirectory()
        try:
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
            self.setBaseUniformResourceLocator("https://www.youtube.com/watch?v=")
            self.setAudioCodec("mp4a")
            self.setVideoCodec("avc")
            self.setUniformResourceLocator(uniform_resource_locator)
            self.setMediaIdentifier(media_identifier)
            self.getLogger().inform("The YouTube Downloader has been successfully been initialized!")
        except Relational_Database_Error as error:
            self.getLogger().error(f"The iniatialization of the model has failed.\nError: {error}")
            raise error

    def getVideoCodec(self) -> str:
        return self.__video_codec

    def setVideoCodec(self, video_codec: str) -> None:
        self.__video_codec = video_codec

    def getAudioCodec(self) -> str:
        return self.__audio_codec

    def setAudioCodec(self, audio_codec: str) -> None:
        self.__audio_codec = audio_codec

    def getBaseUniformResourceLocator(self) -> str:
        return self.__base_uniform_resouce_locator

    def setBaseUniformResourceLocator(self, base_uniform_resouce_locator: str) -> None:
        self.__base_uniform_resouce_locator = base_uniform_resouce_locator

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
        Searching for a video on YouTube and retrieves its metadata.

        This function uses `youtube-dl` to extract information about a YouTube video based on its uniform resource locator.  If metadata exists in the database, it is retrieved; otherwise, new data is extracted and stored.

        Returns:
            {"uniform_resource_locator": string, "author": string, "title": string, "identifier": string, "author_channel": string, "views": int, "published_at": string, "thumbnail": string, "duration": string, "audio_file": string | null, "video_file": string | null}

        Raises:
            Error: If an issue occurs with extracting video metadata or database retrieval.
        """
        options: Dict[str, bool] = {
            "quiet": True,
            "skip_download": True
        }
        self.setVideo(YoutubeDL(options))
        self.setIdentifier(self.retrieveIdentifier(self.getUniformResourceLocator().replace("https://www.youtube.com/watch?v=", "")) if "youtube" in self.getUniformResourceLocator() else self.retrieveIdentifier(self.getIdentifier().replace("https://youtu.be/", "").rsplit("?")[0]))
        try:
            raw_youtube: Dict[str, Any] = self.getVideo().extract_info(self.getUniformResourceLocator(), download=False) # type: ignore
            if not raw_youtube:
                self.getLogger().error(f"The response is invalid")
                raise ValueError("Invalid Response")
            youtube: Dict[str, Any] = {
                key: escape(value) if isinstance(value, str) else value for key, value in raw_youtube.items() # type: ignore
            }
            meta_data: Dict[str, Union[int, List[RowType], str]] = self.getYouTube()
            self.setLength(int(meta_data["data"][0]["length"]) if meta_data["status"] == 200 else int(youtube["duration"])) # type: ignore
            self.setPublishedAt(str(meta_data["data"][0]["published_at"]) if meta_data["status"] == 200 else f"{youtube["upload_date"][:4]}-{youtube["upload_date"][4:6]}-{youtube["upload_date"][6:]}") # type: ignore
            self.setAuthor(str(meta_data["data"][0]["author"]) if meta_data["status"] == 200 else str(youtube["uploader"])) # type: ignore
            self.setTitle(str(meta_data["data"][0]["title"]) if meta_data["status"] == 200 else str(youtube["title"])) # type: ignore
            self.setDuration(strftime("%H:%M:%S", gmtime(self.getLength())))
            file_locations: Dict[str, Union[str, None]] = self._getFileLocations(list(meta_data["data"])) if meta_data["status"] == 200 else {} # type: ignore
            audio_file: Union[str, None] = escape(str(file_locations["audio_file"])) if meta_data["status"] == 200 else None
            video_file: Union[str, None] = escape(str(file_locations["video_file"])) if meta_data["status"] == 200 else None
            if meta_data["status"] != 200:
                self.postYouTube()
            return {
                "uniform_resource_locator": self.getUniformResourceLocator(),
                "author": self.getAuthor(),
                "title": self.getTitle(),
                "identifier": self.getIdentifier(),
                "author_channel": str(youtube["uploader_url"]),
                "views": int(youtube["view_count"]),
                "published_at": self.getPublishedAt(),  # type: ignore
                "thumbnail": str(youtube["thumbnail"]),
                "duration": self.getDuration(),
                "audio_file": audio_file,
                "video_file": video_file
            }
        except Exception as error:
            self.getLogger().error(f"There is an error in the search function.\nError: {error}")
            return {}

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
        Retrieving YouTube video metadata from the database.

        This method queries the relational database to fetch metadata related to a YouTube video based on its identifier.  It performs a join operation with the `MediaFile` table to retrieve associated media files.  The results are sorted in ascending order by the `MediaFile.identifier` column and limited to 2 entries.

        Returns:
            Dict[str, Union[int, List[RowType], str]]: A dictionary containing:
                - `"status"` (int): HTTP-like status code (200 if data exists, 204 if no data).
                - `"data"` (List[RowType]): A list of database rows containing the video metadata.
                - `"timestamp"` (str): The timestamp of when the data retrieval occurred.

        Raises:
            Relational_Database_Error: If there is an issue communicating with the database.
        """
        filter_parameters: Tuple[str] = (self.getIdentifier(),)
        self.setTimestamp(datetime.now().strftime("%Y-%m-%d - %H:%M:%S"))
        try:
            media: List[RowType] = self.getDatabaseHandler().getData(
                parameters=filter_parameters, # type: ignore
                table_name="YouTube",
                join_condition="MediaFile ON MediaFile.YouTube = YouTube.identifier",
                filter_condition="YouTube.identifier = %s",
                column_names="author, title, YouTube.identifier, published_at, length, location",
                sort_condition="MediaFile.identifier ASC",
                limit_condition=2
            )
            status: int = 200 if len(media) != 0 else 204
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

    def postYouTube(self) -> None:
        """
        Inserting YouTube video metadata into the database.

        This method extracts relevant metadata (identifier, length, publication date, author, title, and media identifier) and inserts it into the "YouTube" table in the relational database. If an error occurs during the process, it logs the issue.

        Returns:
            void

        Raises:
            Relational_Database_Error: If there is an issue communicating with the database.
        """
        try:
            data: Tuple[str, int, Union[str, datetime, None], str, str, int] = (self.getIdentifier(), self.getLength(), self.getPublishedAt(), self.getAuthor(), self.getTitle(), self.getMediaIdentifier())
            self.getDatabaseHandler().postData(
                table="YouTube",
                columns="identifier, length, published_at, author, title, Media",
                values="%s, %s, %s, %s, %s, %s",
                parameters=data # type: ignore
            )
        except Relational_Database_Error as error:
            self.getLogger().error(f"There is an error between the model and the relational database server.\nError: {error}")

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
            info = self.getVideo().extract_info(
                url=self.getUniformResourceLocator(),
                download=False
            )
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
        Retrieving the highest-quality audio stream from available streams.

        This method filters the available streams to extract only valid audio streams, selects the one with the highest adaptive bitrate, and sets it as the current stream.  It also sets the MIME type to "audio/mp3" before initiating the download.

        Returns:
            str

        Raises:
            NotFoundError: If no valid audio stream is available.
        """
        codec: str = "mp4a"
        streams: List[Dict[str, Union[str, int, float, List[Dict[str, Union[str, float]]], None, Dict[str, str]]]] = [stream for stream in self.getStreams() if stream["abr"] != None and stream["abr"] != 0 and codec in stream["acodec"]] # type: ignore
        adaptive_bitrate: float = float(max(streams, key=lambda stream: stream["abr"])["abr"]) # type: ignore
        self.setStream([stream for stream in streams if stream["abr"] == adaptive_bitrate][0])
        self.setMimeType("audio/mp3")
        if self.getStream() == None:
            raise NotFoundError("There is not valid audio stream available.")
        return self.__downloadAudio(self.getStream())

    def getVideoFile(self) -> str:
        """
        Retrieving the highest-quality video and audio streams and downloads the video file.

        This method filters available streams to select the best audio and video quality, ensuring the video resolution does not exceed 1080p (1920x1080).  It then combines the selected audio and video streams and initiates the video download.

        Returns:
            string

        Raises:
            NotFoundError: If no valid audio or video stream is available.
        """
        maximum_height: int = 1080
        maximum_width: int = 1920
        audio_codec: str = "mp4a"
        video_codec: str = "avc"
        audio_streams: List[Dict[str, Union[str, int, float, List[Dict[str, Union[str, float]]], None, Dict[str, str]]]] = [stream for stream in self.getStreams() if (stream.get("abr") is not None and stream.get("abr") != 0.00) and audio_codec in str(stream.get("acodec"))]
        adaptive_bitrate: float = float(max(audio_streams, key=lambda stream: stream["abr"])["abr"]) # type: ignore
        self.setStream([stream for stream in audio_streams if stream["abr"] == adaptive_bitrate][0])
        if self.getStream() == None:
            raise NotFoundError("There is not valid audio stream available.")
        audio_stream: Dict[str, Union[str, int, float, List[Dict[str, Union[str, float]]], None, Dict[str, str]]] = self.getStream()
        video_streams: List[Dict[str, Union[str, int, float, List[Dict[str, Union[str, float]]], None, Dict[str, str]]]] = [stream for stream in self.getStreams() if stream.get("vbr") is not None and stream.get("vbr") != 0.00]
        height: int = int(max(video_streams, key=lambda stream: stream["height"])["height"]) # type: ignore
        width: int = int(max(video_streams, key=lambda stream: stream["width"])["width"]) # type: ignore
        height = maximum_height if height >= maximum_height else height
        width = maximum_width if width >= maximum_width else width
        video_streams = [stream for stream in video_streams if stream.get("height") == height and stream.get("width") == width and video_codec in str(stream.get("vcodec")) and "filesize" in stream]
        file_size: int = int(max(video_streams, key=lambda stream: stream["filesize"])["filesize"]) # type: ignore
        self.setStream([stream for stream in video_streams if stream.get("filesize") == file_size][0])
        if self.getStream() == None:
            raise NotFoundError("There is not valid video stream available.")
        video_stream: Dict[str, Union[str, int, float, List[Dict[str, Union[str, float]]], None, Dict[str, str]]] = self.getStream()
        self.setMimeType("video/mp4")
        return self.__downloadVideo(audio_stream, video_stream)

    def __downloadVideo(self, audio: Dict[str, Union[str, int, float, List[Dict[str, Union[str, float]]], None, Dict[str, str]]], video: Dict[str, Union[str, int, float, List[Dict[str, Union[str, float]]], None, Dict[str, str]]]) -> str:
        """
        Downloading a video file with the corresponding audio stream and stores it in the specified directory.

        Parameters:
            audio (Dict[string, Union[string, int, float, List[Dict[string, Union[string, float]]], None, Dict[string, string]]]): A dictionary containing metadata about the audio stream, including format ID.
            video (Dict[string, Union[string, int, float, List[Dict[string, Union[string, float]]], None, Dict[string, string]]]): A dictionary containing metadata about the video stream, including format ID.

        Returns:
            string

        Raises:
            DownloadError: If the video download process fails.
            Relational_Database_Error: If there is an issue inserting data into the relational database.
        """
        file_path: str = f"{self.getDirectory()}/Video/{self.getIdentifier()}.mp4"
        options: Dict[str, str] = {
            "format": f"{video['format_id']}+{audio['format_id']}",
            "merge_output_format": "mp4",
            "outtmpl": file_path
        }
        try:
            self.setVideo(YoutubeDL(options))
            self.getVideo().download([self.getUniformResourceLocator()])
        except DownloadError as error:
            self.getLogger().error(f"The downloading of the video file has failed.\nError: {error}")
            raise error
        data: Tuple[str, str, str, str] = (self.getMimeType(), self.getTimestamp(), file_path, self.getIdentifier())
        try:
            self.getDatabaseHandler().postData(
                table="MediaFile",
                columns="type, date_downloaded, location, YouTube",
                values="%s, %s, %s, %s",
                parameters=data # type: ignore
            )
            return file_path
        except Relational_Database_Error as error:
            self.getLogger().error(f"There is an issue between the relational database server and the API.\nError: {error}")
            raise error

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

    def __downloadAudio(self, stream: Dict[str, Union[str, int, float, List[Dict[str, Union[str, float]]], None, Dict[str, str]]]) -> str:
        """
        Downloading an audio file using the provided stream details and stores it in the specified directory.

        Parameters:
            stream (Dict[string, Union[string, int, float, List[Dict[string, Union[string, float]]], None, Dict[string, string]]]):  A dictionary containing metadata about the audio stream, such as format ID.

        Returns:
            string

        Raises:
            DownloadError: If the audio download process fails.
            Relational_Database_Error: If there is an issue inserting data into the relational database.
        """
        file_path: str = f"{self.getDirectory()}/Audio/{self.getIdentifier()}.mp3"
        options: Dict[str, str] = {
            "format": str(stream["format_id"]),
            "outtmpl": file_path
        }
        try:
            self.setVideo(YoutubeDL(options))
            self.getVideo().download([self.getUniformResourceLocator()])
        except DownloadError as error:
            self.getLogger().error(f"The downloading of the audio file has failed.\nError: {error}")
            raise error
        data: Tuple[str, str, str, str] = (self.getMimeType(), self.getTimestamp(), file_path, self.getIdentifier())
        try:
            self.getDatabaseHandler().postData(
                table="MediaFile",
                columns="type, date_downloaded, location, YouTube",
                values="%s, %s, %s, %s",
                parameters=data # type: ignore
            )
            return file_path
        except Relational_Database_Error as error:
            self.getLogger().error(f"There is an issue between the relational database server and the API.\nError: {error}")
            raise error
