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
            self.getLogger().error(f"The file {self.getIdentifier()}.mp4 does not exist!  It will be removed from the relational database server.\nIdentifier: {self.getIdentifier()}")
            relational_database_status: int = self.removeIdentifierRelationalDatabaseServer(is_shorts)
            file_server_status: int = self.removeDataFileServer(is_shorts)
            status = self.not_found if relational_database_status == self.accepted and file_server_status == self.accepted else self.service_unavailable
            return status
        self.getLogger().inform(f"The file {self.getIdentifier()}.mp4 has been served!\nStatus: {status}")
        return status

    def removeDataFileServer(self) -> int:
        """
        Removing all of the data from the file servers which are
        linked to a specific identifier.

        Returns:
            int
        """
        try:
            audio_file: str = f"{self.getDirectory()}/../Audio/{self.getIdentifier()}.mp3"
            cache_file: str = f"{self.getDirectory()}/../../Cache/Media/{self.getIdentifier()}.json"
            remove(audio_file)
            remove(cache_file)
            self.getLogger().inform(f"The files related have been deleted from the file servers.\nIdentifier: {self.getIdentifier()}\nStatus: {self.accepted}")
            return self.accepted
        except Exception as error:
            self.getLogger().error(f"There is an error between the model and the file servers.\nError: {error}\nStatus: {self.service_unavailable}")
            return self.service_unavailable

    def removeIdentifierRelationalDatabaseServer(self, is_shorts: bool) -> int:
        """
        Removing all of the entries of the identifier from the relational database server.

        Args:
            is_shorts (bool): The flag for checking the type of the video.

        Returns:
            int
        """
        identifier: str = f"shorts/{self.getIdentifier()}" if is_shorts else self.getIdentifier()
        parameters: Tuple[str] = (identifier,)
        try:
            self.getDatabaseHandler().deleteData(
                table=self.getTableName(),
                parameters=parameters,
                condition="YouTube = %s"
            )
            self.getLogger().inform(f"The files related have been deleted from the relational database server.\nIdentifier: {self.getIdentifier()}\nStatus: {self.accepted}")
            return self.accepted
        except Relational_Database_Error as error:
            self.getLogger().error(f"There is an error between the model and the relational database server.\nError: {error}\nStatus: {self.service_unavailable}")
            return self.service_unavailable
