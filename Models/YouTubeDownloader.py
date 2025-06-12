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
from yt_dlp.utils import DownloadError, ExtractorError


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
            self.setBaseUniformResourceLocator("https://www.youtube.com")
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
        Retrieves the identifier from a given string by removing any query parameters after the last "&" symbol.  If the string does not contain the "&" symbol, it returns the original identifier.

        This method splits the identifier string at the last occurrence of the "&" symbol and returns the portion before it, effectively removing any query parameters.

        Parameters:
            identifier (string): The identifier string, which may contain query parameters.

        Returns:
            str
        """
        return identifier.rsplit("&", 1)[0] if "&" in identifier else identifier

    def sanitizeYouTubeIdentifier(self) -> str:
        """
        Extracting and sanitizing the unique YouTube video identifier from various uniform resource locator formats.

        This method handles multiple YouTube uniform resource locator patterns and extracts only the video identifier by:
        - Stripping the base uniform resource locator for standard YouTube video links.
        - Handling YouTube Shorts links by removing the "/shorts/" path segment.
        - Supporting shortened YouTube uniform resource locators, removing query parameters if present.

        Returns:
            str: The sanitized YouTube video identifier.
        """
        sanitized_identifier: str
        if "/shorts/" in self.getUniformResourceLocator():
            sanitized_identifier = f"shorts/{self.getUniformResourceLocator().replace(self.getBaseUniformResourceLocator(), '').replace('/shorts/', '')}"
        elif "youtube" in self.getUniformResourceLocator():
            sanitized_identifier = self.getUniformResourceLocator().replace(self.getBaseUniformResourceLocator(), "").replace("/watch?v=", "")
        else:
            sanitized_identifier = self.getUniformResourceLocator().replace("https://youtu.be/", "").rsplit("?")[0]
        return self.retrieveIdentifier(sanitized_identifier)

    def __isRawYouTube(self, raw_youtube: Dict[str, Any]) -> None:
        """
        Validating the presence of a raw YouTube response dictionary.

        This method checks whether the provided dictionary-like object `raw_youtube` is not empty or None. If it is empty or falsy, a ValueError is raised to indicate an invalid response.

        Args:
            raw_youtube (Dict[str, Any]): The raw response dictionary expected from YouTube data.

        Raises:
            ValueError: If `raw_youtube` is None or empty.
        """
        if raw_youtube:
            return
        self.getLogger().error(f"The response is invalid")
        raise ValueError("Invalid Response")

    def __presentGetYouTube(self, status: int) -> None:
        """
        Handling the presentation logic after attempting to retrieve YouTube data.

        If the HTTP status code indicates success (200 OK), the method simply returns. Otherwise, it calls `postYouTube()` to perform a fallback or alternative action.

        Args:
            status (int): The HTTP status code returned from a YouTube GET request.

        Returns:
            None

        Side Effects:
            May trigger the `postYouTube()` method if the status code is not 200.
        """
        if status == 200:
            return
        self.postYouTube()

    def search(self) -> Dict[str, Union[str, int, None]]:
        """
        Extracting metadata for a YouTube video using `yt-dlp` and returning relevant information.

        This method attempts to retrieve video metadata either from YouTube directly or from a local/internal cache.  The retrieved data includes title, author, view count, publish date, thumbnail, duration, and file locations.

        Key Features:
            - Uses yt-dlp to extract video metadata without downloading.
            - Attempts to use internal database metadata if available.
            - Constructs and returns a clean dictionary of metadata for front-end consumption.
            - Handles unexpected errors gracefully and logs details.

        Returns:
            Dict[str, Union[str, int, None]]: A dictionary containing video metadata, including:
                - 'uniform_resource_locator': str — Original URL
                - 'author': str — Author/uploader name
                - 'title': str — Video title
                - 'identifier': str — Sanitized video ID
                - 'author_channel': str — URL to the author's channel
                - 'views': int — Number of views
                - 'published_at': str — ISO date string of publication
                - 'thumbnail': str — URL to the thumbnail
                - 'duration': str — Video duration in HH:MM:SS
                - 'audio_file': Optional[str] — Path to stored audio file (if found)
                - 'video_file': Optional[str] — Path to stored video file (if found)

        Raises:
            ValueError: If the video metadata cannot be parsed correctly.
            Exception: For any other unexpected errors.
        """
        options: Dict[str, bool] = {
            "quiet": True,
            "skip_download": True,
            "nocheckcertificate": True,
            "force_generic_extractor": False,
            "extract_flat": False
        }
        self.setVideo(YoutubeDL(options))
        self.setIdentifier(self.sanitizeYouTubeIdentifier())
        try:
            raw_youtube: Dict[str, Any] = self.getVideo().extract_info(
                url=self.getUniformResourceLocator(),
                download=False
            ) # type: ignore
            self.__isRawYouTube(raw_youtube)
            youtube: Dict[str, Any] = {
                key: escape(value) if isinstance(value, str) else value for key, value in raw_youtube.items() # type: ignore
            }
            meta_data: Dict[str, Union[int, List[RowType], str]] = self.getYouTube()
            has_metadata: bool = meta_data["status"] == 200
            self.setLength(int(meta_data["data"][0]["length"]) if has_metadata else int(youtube["duration"])) # type: ignore
            self.setPublishedAt(str(meta_data["data"][0]["published_at"]) if has_metadata else f"{youtube['upload_date'][:4]}-{youtube['upload_date'][4:6]}-{youtube['upload_date'][6:]}") # type: ignore
            self.setAuthor(str(meta_data["data"][0]["author"]) if has_metadata else str(youtube["uploader"])) # type: ignore
            self.setTitle(str(meta_data["data"][0]["title"]) if has_metadata else str(youtube["title"])) # type: ignore
            self.setDuration(strftime("%H:%M:%S", gmtime(self.getLength())))
            file_locations: Dict[str, Union[str, None]] = self._getFileLocations(list(meta_data["data"])) if has_metadata else {} # type: ignore
            audio_file: Union[str, None] = escape(str(file_locations["audio_file"])) if has_metadata else None
            video_file: Union[str, None] = escape(str(file_locations["video_file"])) if has_metadata else None
            self.__presentGetYouTube(int(str(meta_data["status"])))
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
        Retrieving the available media streams (audio and video) for a given resource and provides metadata such as author, title, views, and publication date.  If the audio and video files are not already downloaded, they will be downloaded using YoutubeDL.

        This method performs the following tasks:
            1. Searches for the metadata of the media.
            2. Retrieves and stores the audio and video file paths.
            3. Downloads the media streams if the files do not exist.
            4. Returns a dictionary containing the following metadata:
                - uniform_resource_locator: The URL of the media.
                - author: The author of the media.
                - title: The title of the media.
                - identifier: A unique identifier for the media.
                - author_channel: The author's channel name or identifier.
                - views: The number of views the media has received.
                - published_at: The publication date of the media.
                - thumbnail: The URL of the media's thumbnail image.
                - duration: The duration of the media.
                - audio: The file path to the downloaded audio.
                - video: The file path to the downloaded video.

        Returns:
            Dict[string, Union[string, int, None]]

        Raises:
            NotFoundError: If the media resource cannot be found.
            DownloadError: If there is an error while downloading the media.
            Relational_Database_Error: If there is a database-related error.
        """
        try:
            metadata: Dict[str, Union[str, int, None]] = self.search()
            self.setIdentifier(str(metadata["identifier"]))
            audio_file_location: str = f"{self.getDirectory()}/Audio/{self.getIdentifier()}.mp3"
            video_file_location: str = f"{self.getDirectory()}/Video/{self.getIdentifier()}.mp4"
            options: Dict[str, bool] = {
                "quiet": True,
                "listformats": True
            }
            files: Dict[str, str] = self.__getFiles(audio_file_location, video_file_location, options)
            self.getLogger().inform(f"The media content has been downloaded!\nAudio: {audio_file_location}\nVideo: {video_file_location}")
            audio_file_location = files["audio"]
            video_file_location = files["video"]
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
        except (NotFoundError, DownloadError, Relational_Database_Error, ExtractorError) as error:
            self.getLogger().error(f"There is an error while retrieving the streams.\nError: {error}")
            return {}

    def __getFiles(self, audio: str, video: str, options: Dict[str, bool]) -> Dict[str, str]:
        """
        Retrieving the audio and video files for a given resource.  If the audio and video files already exist, it returns their file paths. Otherwise, it downloads the streams using YoutubeDL and returns the downloaded file paths.

        This method performs the following tasks:
            1. Checks if the audio and video files exist.
            2. If the files exist, it returns their file paths.
            3. If the files do not exist, it downloads the audio and video streams using YoutubeDL.
            4. Returns a dictionary containing the paths to the audio and video files.

        Parameters:
            audio (string): The file path of the audio file.
            video (string): The file path of the video file.
            options (Dict[string, bool]): A dictionary of options to configure the YoutubeDL download process.

        Returns:
            Dict[string, string]

        Raises:
            NotFoundError: If the media resource cannot be found.
            DownloadError: If there is an error while downloading the media.
            Relational_Database_Error: If there is a database-related error.
        """
        if isfile(audio) and isfile(video):
            return {
                "audio": audio,
                "video": video
            }
        try:
            self.setVideo(YoutubeDL(options))
            info = self.getVideo().extract_info(
                url=self.getUniformResourceLocator(),
                download=False
            )
            self.setStreams(info["formats"]) # type: ignore
            return {
                "audio": self.getAudioFile(),
                "video": self.getVideoFile()
            }
        except (NotFoundError, DownloadError, Relational_Database_Error, ExtractorError) as error:
            self.getLogger().error(f"There is an error while retrieving the streams.\nError: {error}")
            raise error

    def getAudioFile(self) -> str:
        """
        Retrieving the highest-quality audio stream from available streams.

        This method filters the available streams to extract only valid audio streams, selects the one with the highest adaptive bitrate, and sets it as the current stream.  It also sets the MIME type to "audio/mp3" before initiating the download.

        Returns:
            str

        Raises:
            NotFoundError: If no valid audio stream is available.
        """
        streams: List[Dict[str, Union[str, int, float, List[Dict[str, Union[str, float]]], None, Dict[str, str]]]] = []
        for stream in self.getStreams():
            is_audio_only: bool = stream.get("vcodec") == "none"
            adaptive_bitrate: float = stream.get("abr") or stream.get("tbr") or 0 # type: ignore
            audio_codec: str = stream.get("acodec", "Unknown") # type: ignore
            if is_audio_only and adaptive_bitrate > 0 and isinstance(audio_codec, str):
                streams.append(stream)
        if not streams:
            self.getLogger().error("There is no audio stream with the codec needed.")
            raise NotFoundError("There is no audio stream with the codec needed.")
        preferred_streams: List[Dict[str, Union[str, int, float, List[Dict[str, Union[str, float]]], None, Dict[str, str]]]] = [stream for stream in streams if self.getAudioCodec() in str(stream.get("acodec"))]
        stream: Dict[str, Union[str, int, float, List[Dict[str, Union[str, float]]], None, Dict[str, str]]] = max(preferred_streams or streams, key=lambda stream: stream.get("abr", 0.00)) # type: ignore
        self.setStream(stream)
        self.setMimeType("audio/mp3")
        return self.__downloadAudio(self.getStream())

    def _getAudioStreams(self) -> List[Dict[str, Union[str, int, float, List[Dict[str, Union[str, float]]], None, Dict[str, str]]]]:
        """
        Retrieving the audio streams from all of the possible streams.

        Returns:
            List[Dict[str, Union[str, int, float, List[Dict[str, Union[str, float]]], None, Dict[str, str]]]]: A list of audio streams.
        """
        streams: List[Dict[str, Union[str, int, float, List[Dict[str, Union[str, float]]], None, Dict[str, str]]]] = []
        for stream in self.getStreams():
            is_audio_only: bool = stream.get("vcodec") == "none"
            adaptive_bitrate: float = stream.get("abr") or stream.get("tbr") or 0 # type: ignore
            audio_codec: str = stream.get("acodec", "Unknown") # type: ignore
            streams = self.__getAudioStreams(streams, stream, is_audio_only, adaptive_bitrate, audio_codec)
        return streams

    def __getAudioStreams(self, streams: List[Dict[str, Union[str, int, float, List[Dict[str, Union[str, float]]], None, Dict[str, str]]]], stream: Dict[str, Union[str, int, float, List[Dict[str, Union[str, float]]], None, Dict[str, str]]], is_audio_only: bool, adaptive_bitrate: float, audio_codec: str) -> List[Dict[str, Union[str, int, float, List[Dict[str, Union[str, float]]], None, Dict[str, str]]]]:
        """
        Verifying that the stream is an audio stream to add it to the list of streams.

        Args:
            streams (List[Dict[str, Union[str, int, float, List[Dict[str, Union[str, float]]], None, Dict[str, str]]]]): The list of streams to be returned.
            stream (Dict[str, Union[str, int, float, List[Dict[str, Union[str, float]]], None, Dict[str, str]]]): The stream to be verified.
            is_audio_only (bool): Whether the stream is audio-only.
            adaptive_bitrate (float): The adaptive bitrate of the stream.
            audio_codec (str): The audio codec of the stream.

        Returns:
            List[Dict[str, Union[str, int, float, List[Dict[str, Union[str, float]]], None, Dict[str, str]]]]: The updated list of streams.
        """
        if is_audio_only and adaptive_bitrate > 0 and isinstance(audio_codec, str):
            streams.append(stream)
        return streams

    def getVideoFile(self) -> str:
        """
        Retrieving the highest-quality video and audio streams and downloads the video file.

        This method filters available streams to select the best audio and video quality, ensuring the video resolution does not exceed 1080p (1920x1080).  It then combines the selected audio and video streams and initiates the video download.

        Returns:
            string

        Raises:
            NotFoundError: If no valid audio or video stream is available.
        """
        maximum_height: int = 1080 if "shorts/" not in self.getIdentifier() else 1920
        maximum_width: int = 1920 if "shorts/" not in self.getIdentifier() else 1080
        audio_streams: List[Dict[str, Union[str, int, float, List[Dict[str, Union[str, float]]], None, Dict[str, str]]]] = [stream for stream in self.getStreams() if (stream.get("abr") is not None and stream.get("abr") != 0.00) and self.getAudioCodec() in str(stream.get("acodec"))]
        self.getLogger().debug(f"Function: getVideoFile()\nStreams: {audio_streams}")
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
        video_streams = [stream for stream in video_streams if stream.get("height") == height and stream.get("width") == width and self.getVideoCodec() in str(stream.get("vcodec")) and "filesize" in stream]
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

    def handleHttpError(self, error: HTTPError) -> None:
        """
        Handling HTTP errors that occur during requests.

        Parameters:
            error (HTTPError): The HTTP error encountered.

        Raises:
            HTTPError: If the error is not a 403 Forbidden error.
        """
        self.getLogger().error(f"An HTTP error occurred.\nError: {error}")
        if "403" not in str(error):
            raise error

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
