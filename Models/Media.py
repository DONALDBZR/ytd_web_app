from Models.DatabaseHandler import Database_Handler
from Models.YouTubeDownloader import YouTube_Downloader
from datetime import datetime
import json
import os
import time
import shutil


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
    __metadata_media_files: list[str]
    """
    The metadata of the media content that is stored in the
    document database.

    Type: array
    Visibility: private
    """
    __media_files: list[str]
    """
    The media content that is stored in the document database.

    Type: array
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
        self.setDatabaseHandler(Database_Handler())
        self.getDatabaseHandler()._query(
            "CREATE TABLE IF NOT EXISTS `Media` (identifier INT PRIMARY KEY AUTO_INCREMENT, `value` VARCHAR(8))", None)
        self.getDatabaseHandler()._execute()
        self.__maintain()
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

    def getMetadataMediaFiles(self) -> list[str]:
        return self.__metadata_media_files

    def setMetadataMediaFiles(self, metadata_media_files: list[str]) -> None:
        self.__metadata_media_files = metadata_media_files

    def getMediaFiles(self) -> list[str]:
        return self.__media_files

    def setMediaFiles(self, media_files: list[str]) -> None:
        self.__media_files = media_files

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

    def __maintain(self) -> None:
        """
        Maintaining the document database by doing some regular
        checks on the the metadata and media files.

        Returns: void
        """
        self.setMetadataMediaFiles(os.listdir(self.getDirectory()))
        audio_media_files_directory = f"{self.getDirectory()}/../../Public/Audio"
        video_media_files_directory = f"{self.getDirectory()}/../../Public/Video"
        audio_media_files = os.listdir(audio_media_files_directory)
        video_media_files = os.listdir(video_media_files_directory)
        destination_directory = f"{self.getDirectory()}/../../Public/{int(time.time())}"
        self.optimizeDirectory(
            audio_media_files, audio_media_files_directory, destination_directory)
        self.optimizeDirectory(
            video_media_files, video_media_files_directory, destination_directory)

    def optimizeDirectory(self, media_files: list[str], original_directory: str, new_directory: str) -> None:
        """
        Optimizing the directory by iterating throughout the media
        files that are in the directory to remove them from the
        application to be backed up else where.

        Parameters:
            media_files:        array:  The media files in the original directory.
            original_directory: string: The directory where the media files are hosted.
            new_directory:      string: The directory where the media files will be moved.

        Returns: void
        """
        # Iterating throughout the audio media files to restructure all the media files from the original directory.
        for index in range(0, len(media_files), 1):
            original_file = f"{original_directory}/{media_files[index]}"
            age = int(time.time()) - int(os.path.getctime(original_file))
            self.removeOldFile(
                original_file, media_files[index], new_directory, age)

    def removeOldFile(self, original_file: str, media_file: str, destination_directory: str, age: int) -> None:
        """
        Removing the file that is three days old.

        Parameters:
            original_file:          string: The path of the original file.
            media_file:             string: The media file.
            destination_directory:  string: The directory where the mediafile will be moved.
            age:                    int:    Age of the media file.

        Returns: void
        """
        # Ensuring that the audio file is at most three days old to make a backup of it from the server.
        if age > 259200:
            os.mkdir(destination_directory)
            new_file = f"{destination_directory}/{self.setNewFile(media_file)}"
            self.removeFile(original_file, new_file)

    def setNewFile(self, media_file: str) -> str:
        """
        Setting the new path for the media file.

        Parameters:
            media_file: string: The media file.

        Returns: string
        """
        # Verifying that the file type of the media file.
        if ".mp3" in media_file:
            identifier: str = media_file.replace(".mp3", "")
            parameters = tuple([identifier])
            metadata = self.getDatabaseHandler().get_data(
                table_name="YouTube",
                filter_condition="identifier = %s",
                parameters=parameters
            )[0]
            new_file = f"{metadata[4]}.mp3"
        else:
            identifier: str = media_file.replace(".mp4", "")
            parameters = tuple([identifier])
            metadata = self.getDatabaseHandler().get_data(
                table_name="YouTube",
                filter_condition="identifier = %s",
                parameters=parameters
            )[0]
            new_file = f"{metadata[4]}.mp4"
        return new_file

    def removeFile(self, original_file: str, new_file: str) -> None:
        """
        Removing the file from the hosting directory.

        Parameters:
            original_file:  string: The path of the original file.
            new_file:       string: The path of the new file.

        Returns: void
        """
        # Ensuring that the file does not exist to copy it
        if os.path.exists(new_file) == False:
            shutil.copyfile(original_file, new_file)
            os.remove(original_file)

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
