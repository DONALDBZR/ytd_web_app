from pytube import YouTube, StreamQuery, Stream
from DatabaseHandler import Database_Handler
from datetime import datetime
import time
import os


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
    __streams: "StreamQuery"
    """
    Interface for querying the available media streams.

    Type: StreamQuery
    Visibility: private
    """
    __stream: "Stream"
    """
    Container for stream manifest data.

    Type: Stream|null
    Visibility: private
    """
    __itag: int
    """
    YouTube format identifier code

    Type: integer
    Visibility: private
    """
    __mime_type: str
    """
    Two-part identifier for file formats and format contents
    composed of a "type" and a "subtype".

    Type: string
    Visibility: private
    """

    def __init__(self, uniform_resource_locator: str, media_identifier: int):
        """
        Instantiating the class and launching the operations needed.

        Parameters:
            uniform_resource_locator: string: The uniform resource locator to be searched.
            media_identifier: int: The media type for the system. 
        """
        self.setDirectory("/var/www/html/ytd_web_app/Public")
        self.mediaDirectory()
        self.setDatabaseHandler(Database_Handler())
        self.getDatabaseHandler()._query("CREATE TABLE IF NOT EXISTS `YouTube` (identifier VARCHAR(16) PRIMARY KEY, `length` INT, published_at VARCHAR(32), author VARCHAR(64), title VARCHAR(128), `Media` INT, CONSTRAINT fk_Media_type FOREIGN KEY (`Media`) REFERENCES `Media` (identifier))", None)
        self.getDatabaseHandler()._execute()
        self.setUniformResourceLocator(uniform_resource_locator)
        self.setMediaIdentifier(media_identifier)

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

    def getStreams(self) -> "StreamQuery":
        return self.__streams

    def setStreams(self, streams: "StreamQuery") -> None:
        self.__streams = streams

    def getStream(self) -> "Stream":
        return self.__stream

    def setStream(self, stream: "Stream") -> None:
        self.__stream = stream

    def getITAG(self) -> int:
        return self.__itag

    def setITAG(self, itag: int) -> None:
        self.__itag = itag

    def getMimeType(self) -> str:
        return self.__mime_type

    def setMimeType(self, mime_type: str) -> None:
        self.__mime_type = mime_type

    def search(self) -> dict:
        """
        Searching for the video in YouTube.

        Returns: object
        """
        self.setVideo(YouTube(self.getUniformResourceLocator()))
        self.setIdentifier(self.getUniformResourceLocator())
        self.setIdentifier(self.getIdentifier().replace(
            "https://www.youtube.com/watch?v=", ""))
        response = {}
        meta_data = self.getYouTube()
        # Verifying the response of the metadata to retrieve the needed response
        if meta_data["status"] == 200:
            self.setLength(meta_data["data"][0][1])
            self.setPublishedAt(meta_data["data"][0][2])
            self.setAuthor(meta_data["data"][0][3])
            self.setTitle(meta_data["data"][0][4])
            self.setDuration(time.strftime(
                "%H:%M:%S", time.gmtime(self.getLength())))
        else:
            self.setLength(self.getVideo().length)
            self.setPublishedAt(self.getVideo().publish_date)
            self.setAuthor(self.getVideo().author)
            self.setTitle(self.getVideo().title)
            self.setDuration(time.strftime(
                "%H:%M:%S", time.gmtime(self.getLength())))
            self.postYouTube()
        response = {
            "uniform_resource_locator": self.getUniformResourceLocator(),
            "author": self.getAuthor(),
            "title": self.getTitle(),
            "identifier": self.getIdentifier(),
            "author_channel": self.getVideo().channel_url,
            "views": self.getVideo().views,
            "published_at": self.getPublishedAt(),
            "thumbnail": self.getVideo().thumbnail_url,
            "duration": self.getDuration()
        }
        return response

    def getYouTube(self) -> dict:
        """
        Retrieving the metadata from the YouTube table.

        Returns: object
        """
        media = self.getDatabaseHandler().get_data(
            tuple([self.getIdentifier()]), "YouTube", filter_condition="identifier = %s")
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

    def postYouTube(self) -> None:
        """
        Creating a record for the media with its data.

        Returns: void
        """
        self.getDatabaseHandler().post_data("YouTube", "identifier, length, published_at, author, title, Media", "%s, %s, %s, %s, %s, %s",
                                            (self.getIdentifier(), self.getLength(), self.getPublishedAt(), self.getAuthor(), self.getTitle(), self.getMediaIdentifier()))

    def mediaDirectory(self):
        """
        Creating the directories for storing the media files.

        Returns: void
        """
        if not os.path.exists(f"{self.getDirectory()}/Video"):
            os.makedirs(f"{self.getDirectory()}/Video")
        if not os.path.exists(f"{self.getDirectory()}/Audio"):
            os.makedirs(f"{self.getDirectory()}/Audio")

    def retrievingStreams(self) -> dict:
        """
        Downloading the contents of the media from the platform to
        save on the server.

        Returns: object
        """
        response = {}
        metadata = self.search()
        audio_file_location = f"{self.getDirectory()}/Audio/{self.getTitle()}.mp4"
        video_file_location = f"{self.getDirectory()}/Video/{self.getTitle()}.mp4"
        # Verifying that the files exist in the server before downloading them
        if os.path.isfile(audio_file_location) and os.path.isfile(video_file_location):
            audio_file_location = f"{self.getDirectory()}/Audio/{self.getTitle()}.mp4"
            video_file_location = f"{self.getDirectory()}/Video/{self.getTitle()}.mp4"
            self.setIdentifier(self.getUniformResourceLocator())
            self.setIdentifier(self.getIdentifier().replace(
                "https://www.youtube.com/watch?v=", ""))
            audio_file_location = f"{self.getDirectory()}/Audio/{self.getTitle()}.mp4"
            video_file_location = f"{self.getDirectory()}/Video/{self.getTitle()}.mp4"
        else:
            self.setVideo(
                YouTube(self.getUniformResourceLocator()))
            self.getDatabaseHandler()._query("CREATE TABLE IF NOT EXISTS `MediaFile` (identifier INT PRIMARY KEY AUTO_INCREMENT, `type` VARCHAR(64), date_downloaded VARCHAR(32), date_deleted VARCHAR(32) NULL, location VARCHAR(128), `YouTube` VARCHAR(16), CONSTRAINT fk_source FOREIGN KEY (`YouTube`) REFERENCES `YouTube` (identifier))", None)
            self.getDatabaseHandler()._execute()
            self.setIdentifier(self.getUniformResourceLocator())
            self.setIdentifier(self.getIdentifier().replace(
                "https://www.youtube.com/watch?v=", ""))
            self.setStreams(self.getVideo().streams)
            audio_file_location = self.getAudioFile()
            video_file_location = self.getVideoFile()
        response = {
            "uniform_resource_locator": self.getUniformResourceLocator(),
            "author": self.getAuthor(),
            "title": self.getTitle(),
            "identifier": self.getIdentifier(),
            "author_channel": self.getVideo().channel_url,
            "views": self.getVideo().views,
            "published_at": self.getPublishedAt(),
            "thumbnail": self.getVideo().thumbnail_url,
            "duration": self.getDuration(),
            "audio": audio_file_location,
            "video": video_file_location
        }
        return response

    def getAudioFile(self) -> str:
        """
        Retrieving the audio file and saving it on the server as
        well as adding its meta data in the database.

        Returns: string
        """
        response = ""
        # Iterating throughout the streams to set the ITAG needed
        for index in range(0, len(self.getStreams().filter(mime_type="audio/mp4", abr="128kbps", audio_codec="mp4a.40.2")), 1):
            self.setITAG(self.getStreams().filter(
                mime_type="audio/mp4", abr="128kbps", audio_codec="mp4a.40.2")[index].itag)
        self.setStream(self.getStreams().get_by_itag(
            self.getITAG()))  # type: ignore
        self.setMimeType("audio/mp3")
        self.getStream().download(
            output_path=f"{self.getDirectory()}/Audio", filename=f"{self.getTitle()}.mp3")
        file_name = f"{self.getTitle()}.mp3"
        self.setTimestamp(datetime.now().strftime("%Y-%m-%d - %H:%M:%S"))
        self.getDatabaseHandler().post_data("MediaFile", "type, date_downloaded, location, YouTube", "%s, %s, %s, %s",
                                            (self.getMimeType(), self.getTimestamp(), f"{self.getDirectory()}/Audio/{self.getTitle()}.mp3", self.getIdentifier()))
        response = f"{self.getDirectory()}/Audio/{self.getTitle()}.mp3"
        return response

    def getVideoFile(self) -> str:
        """
        Retrieving the video file and saving it on the server as
        well as adding its meta data in the database.

        Returns: string
        """
        response = ""
        # Iterating throughout the streams to set the ITAG needed
        for index in range(0, len(self.getStreams().filter(mime_type="video/mp4", audio_codec="mp4a.40.2", resolution="720p")), 1):
            self.setITAG(self.getStreams().filter(
                mime_type="video/mp4", audio_codec="mp4a.40.2", resolution="720p")[index].itag)
        self.setStream(self.getStreams().get_by_itag(
            self.getITAG()))  # type: ignore
        self.setMimeType(self.getStream().mime_type)
        self.getStream().download(f"{self.getDirectory()}/Video")
        self.setTimestamp(datetime.now().strftime("%Y-%m-%d - %H:%M:%S"))
        self.getDatabaseHandler().post_data("MediaFile", "type, date_downloaded, location, YouTube", "%s, %s, %s, %s",
                                            (self.getMimeType(), self.getTimestamp(), f"{self.getDirectory()}/Video/{self.getTitle()}.mp4", self.getIdentifier()))
        response = f"{self.getDirectory()}/Video/{self.getTitle()}.mp4"
        return response
