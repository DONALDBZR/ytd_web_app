"""
It is the module for the shared rotating file handler used in the Extractio application.

Authors:
    Darkness4869
"""
from logging.handlers import RotatingFileHandler
from os import chmod, remove
from shutil import copyfileobj
from gzip import open as gzip_open
from io import TextIOWrapper


class Shared_Rotating_File_Handler(RotatingFileHandler):
    """
    Rotating file handler that gzips old files and keeps the log writable by both the web server and the crawler user.
    """

    def __init__(self, *arguments, **keywords) -> None:
        super().__init__(*arguments, **keywords)
        self.namer = lambda name: f"{name}.gz"
        self.rotator = self.__compress

    @staticmethod
    def __compress(source: str, destination: str) -> None:
        """
        Compressing the source file into the destination file using gzip and then removing the source file.

        Parameters:
            source (str): Path to the source file to be compressed.
            destination (str): Path to the destination compressed file.

        Returns:
            None
        """
        with open(source, "rb") as source_file, gzip_open(destination, "wb") as destination_file:
            copyfileobj(source_file, destination_file)
        remove(source)

    def _open(self) -> TextIOWrapper:
        """
        Open the log file and set its permissions to be writable by both the web server and the crawler user.

        Returns:
            The opened log file stream.
        """
        stream = super()._open()
        try:
            chmod(self.baseFilename, 0o666)
        except OSError:
            pass
        return stream