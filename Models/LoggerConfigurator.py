"""
It is the configuration module for the Extractio application logging system.

Authors:
    Darkness4869
"""
from Environment import Environment
from logging import Logger, getLogger, FileHandler, Formatter, DEBUG, Handler
from typing import List, Optional
from os import makedirs
from os.path import join


class Logger_Configurator:
    """
    A class to configure logging settings for the Extractio application.

    This class allows customization of log file location, name, format, encoding, file mode, and supports additional handlers.

    Attributes:
        directory (str): Directory where log files are stored.
        filename (str): Name of the log file.
        log_format (str): Format string for log messages.
        encoding (str): Encoding for the log file.
        file_mode (str): File mode for opening the log file.
        handlers (List[Handler]): List of additional logging handlers to be added to the logger.

    Methods:
        configure(logger_name: str) -> Logger:
            Configuring and retrieving a logger instance based on the stored settings.
    """
    __directory: str
    """
    Directory where log files are stored.
    """
    __filename: str
    """
    Name of the log file.
    """
    __format: str
    """
    Format of the log messages.
    """
    __encoding: str
    """
    Encoding used for the log file.
    """
    __file_mode: str
    """
    Mode in which the log file is opened.
    """
    __handlers: List[Handler]
    """
    List of additional logging handlers to be added to the logger.
    """

    def __init__(
        self,
        directory: str = "",
        filename: str = "Extractio.log",
        format: str = "[%(asctime)s] [%(name)s] [%(levelname)s] %(message)s",
        encoding: str = "utf-8",
        file_mode: str = "a",
        handlers: Optional[List[Handler]] = None
    ):
        """
        Initializing the Logger_Configurator instance.

        It sets up the logging configuration with the provided parameters and creates the log directory if it does not exist.

        Parameters:
            directory (str): Directory where log files are stored. (default: "")
            filename (str): Name of the log file. (default: "Extractio.log")
            format (str): Format string for log messages. (default: "[%(asctime)s] [%(name)s] [%(levelname)s] %(message)s")
            encoding (str): Encoding used for the log file. (default: "utf-8")
            file_mode (str): Mode in which the log file is opened. (default: "a")
            handlers (List[Handler]): List of additional logging handlers to be added to the logger. (default: None)
        """
        env: Environment = Environment()
        self.setDirectory(directory if directory else f"{env.getDirectory()}/Logs")
        self.setFilename(filename)
        self.setFormat(format)
        self.setEncoding(encoding)
        self.setFileMode(file_mode)
        self.setHandlers(handlers or [])
        makedirs(self.getDirectory(), exist_ok=True)

    def getDirectory(self) -> str:
        return self.__directory

    def setDirectory(self, directory: str) -> None:
        self.__directory = directory

    def getFilename(self) -> str:
        return self.__filename

    def setFilename(self, filename: str) -> None:
        self.__filename = filename

    def getFormat(self) -> str:
        return self.__format

    def setFormat(self, format: str) -> None:
        self.__format = format

    def getEncoding(self) -> str:
        return self.__encoding

    def setEncoding(self, encoding: str) -> None:
        self.__encoding = encoding

    def getFileMode(self) -> str:
        return self.__file_mode

    def setFileMode(self, file_mode: str) -> None:
        self.__file_mode = file_mode

    def getHandlers(self) -> List[Handler]:
        return self.__handlers

    def setHandlers(self, handlers: List[Handler]) -> None:
        self.__handlers = handlers

    def configure(self, logger_name: str) -> Logger:
        """
        Configuring and retrieving a logger instance based on the stored settings.

        This method gets a logger by its name.  If the logger has already been configured with handlers, it is returned immediately to prevent duplicate handler attachment.

        Otherwise, it creates a new `FileHandler` using the path, mode, and encoding specified in this configurator instance.  It also attaches any additional handlers provided during initialization.

        Args:
            logger_name (str): The name of the logger to configure, typically the `__name__` of the calling module.

        Returns:
            Logger: The configured logger instance, ready for use.
        """
        logger: Logger = getLogger(logger_name)
        logger.setLevel(DEBUG)
        if logger.hasHandlers():
            return logger
        file_handler: FileHandler = FileHandler(
            join(
                self.getDirectory(),
                self.getFilename()
            ),
            mode=self.getFileMode(),
            encoding=self.getEncoding()
        )
        formatter: Formatter = Formatter(self.getFormat())
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        for handler in self.getHandlers():
            logger.addHandler(handler)
        return logger
