"""
The module that will contain the model of the Videos.

Authors:
    Darkness4869
"""
from Environment import Environment
from Models.Logger import Extractio_Logger
from Models.DatabaseHandler import Database_Handler, Relational_Database_Error
from os.path import exists
from typing import Tuple
from os import remove
from Models.MediaFileModel import Media_File


class Video:
    """
    It will handle any I/O operations that are related with the
    video contents as well as the databases operations.
    """
    __identifier: str
    """
    The identifier of the video
    """
    __directory: str
    """
    The directory of the content
    """
    __logger: Extractio_Logger
    """
    The logger that will all the action of the application.
    """
    __database_handler: Database_Handler
    """
    The database handler that will communicate with the database
    server.
    """
    __table_name: str
    """
    The table to be affected by the management system.
    """
    ok: int = 200
    """
    The status of a success read
    """
    accepted: int = 202
    """
    The status of a success write
    """
    not_found: int = 404
    """
    The status for not-found
    """
    service_unavailable: int = 503
    """
    The status of a service that is unavailable
    """

    def __init__(self, identifier: str):
        """
        Initializing the management system as well as all of its
        dependencies.

        Parameters:
            identifier: string: The identifier of the video.
        """
        ENV: Environment = Environment()
        self.setLogger(Extractio_Logger(__name__))
        self.setDatabaseHandler(Database_Handler())
        self.setDirectory(f"{ENV.getDirectory()}/Public/Video")
        self.setTableName("MediaFile")
        self.setIdentifier(identifier)
        self.getLogger().inform("The Video Management System has been successfully initialized!")

    def getTableName(self) -> str:
        return self.__table_name

    def setTableName(self, table_name: str) -> None:
        self.__table_name = table_name

    def getDatabaseHandler(self) -> Database_Handler:
        return self.__database_handler

    def setDatabaseHandler(self, database_handler: Database_Handler) -> None:
        self.__database_handler = database_handler

    def getLogger(self) -> Extractio_Logger:
        return self.__logger

    def setLogger(self, logger: Extractio_Logger) -> None:
        self.__logger = logger

    def getDirectory(self) -> str:
        return self.__directory

    def setDirectory(self, directory: str) -> None:
        self.__directory = directory

    def getIdentifier(self) -> str:
        return self.__identifier

    def setIdentifier(self, identifier: str) -> None:
        self.__identifier = identifier

    def serveFile(self, is_shorts: bool = False) -> int:
        """
        Serving the file needed by the user-interface.

        Args:
            is_shorts (bool): The flag for checking the type of the video.

        Returns:
            int
        """
        file_path: str = f"{self.getDirectory()}/shorts/{self.getIdentifier()}.mp4" if is_shorts else f"{self.getDirectory()}/{self.getIdentifier()}.mp4"
        status: int = self.ok if exists(file_path) else self.not_found
        if status != self.ok:
            self.getLogger().error(f"The file {self.getIdentifier()}.mp4 does not exist!  It will be removed from the relational database server. - Identifier: {self.getIdentifier()}")
            relational_database_status: int = self.removeIdentifierRelationalDatabaseServer(is_shorts)
            file_server_status: int = self.removeDataFileServer(is_shorts)
            status = self.not_found if relational_database_status == self.accepted and file_server_status == self.accepted else self.service_unavailable
            return status
        self.getLogger().inform(f"The file {self.getIdentifier()}.mp4 has been served! - Status: {status}")
        return status

    def removeDataFileServer(self, is_shorts: bool) -> int:
        """
        Removing all of the data from the file servers which are linked to a specific identifier.

        Args:
            is_shorts (bool): The flag for checking the type of the video.

        Returns:
            int
        """
        try:
            audio_file: str = f"{self.getDirectory()}/../Audio/shorts/{self.getIdentifier()}.mp3" if is_shorts else f"{self.getDirectory()}/../Audio/{self.getIdentifier()}.mp3"
            cache_file: str = f"{self.getDirectory()}/../../Cache/Media/shorts/{self.getIdentifier()}.json" if is_shorts else f"{self.getDirectory()}/../../Cache/Media/{self.getIdentifier()}.json"
            remove(audio_file)
            remove(cache_file)
            self.getLogger().inform(f"The files related have been deleted from the file servers. - Identifier: {self.getIdentifier()} - Status: {self.accepted}")
            return self.accepted
        except Exception as error:
            self.getLogger().error(f"There is an error between the model and the file servers. - Error: {error} - Status: {self.service_unavailable}")
            return self.service_unavailable

    def removeIdentifierRelationalDatabaseServer(self, is_shorts: bool) -> int:
        """
        Removing the specified identifier from the relational database server.

        This method constructs the identifier based on whether it represents a short video, then attempts to delete the corresponding records from the database using the `deleteByYouTube` method of the `Media_File` class.  It logs an informative message if the deletion is successful or an error message if it fails.

        Args:
            is_shorts (bool): A flag indicating if the identifier is for a short video.

        Returns:
            int: HTTP-like status code indicating success (202) or failure (503).

        Raises:
            Relational_Database_Error: If there is an issue communicating with the database.
        """
        identifier: str = f"shorts/{self.getIdentifier()}" if is_shorts else self.getIdentifier()
        try:
            response: bool = Media_File.deleteByYouTube(self.getDatabaseHandler(), identifier)
            status: int = self.accepted if response else self.service_unavailable
            message: str = "The files related have been deleted from the relational database server." if response else "There is an error between the model and the relational database server."
            if response:
                self.getLogger().inform(f"{message} - Identifier: {self.getIdentifier()} - Status: {status}")
            else:
                self.getLogger().error(f"{message} - Identifier: {self.getIdentifier()} - Status: {status}")
            return status
        except Relational_Database_Error as error:
            self.getLogger().error(f"There is an error between the model and the relational database server. - Error: {error} - Status: {self.service_unavailable}")
            return self.service_unavailable
