"""
Implementation of the Logger_Configurator class for configuring logging settings in the Extractio application.
"""
from Environment import Environment
from logging import Logger, getLogger, FileHandler, Formatter, DEBUG, Handler
from typing import List, Optional
from os import makedirs


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
            Configuring the logger with the specified parameters and returns the logger instance.
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
        directory: str = "Logs",
        filename: str = "Extractio.log",
        format: str = "[%(asctime)s] [%(name)s] [%(levelname)s] %(message)s",
        encoding: str = "utf-8",
        file_mode: str = "a",
        handlers: Optional[List[Handler]] = None
    ):
        """
        Initializing the Logger_Configurator with specified or default settings.

        This constructor sets up the configuration used to create and configure logger instances.  It allows customization of the log file's location, name, message format, and other properties.

        If a `directory` is not provided, it defaults to a 'Logs' subdirectory within the application's main directory, as determined by the `Environment` class.  The directory is created if it does not exist.

        Args:
            directory (str): The directory to store the log file.
            filename (str): The name of the log file.
            format (str): The format string for log messages.
            encoding (str): The character encoding for the log file.
            file_mode (str): The file mode for opening the log file.
            handlers (Optional[List[Handler]]): A list of additional logging handlers to add to the logger.
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
        Configuring the logger with the specified parameters and returns the logger instance.

        Args:
            logger_name (str): Name of the logger to be configured.

        Returns:
            Logger: Configured logger instance.
        """
        logger: Logger = getLogger(logger_name)
        logger.setLevel(DEBUG)
        if not logger.handlers:
            file_handler: FileHandler = FileHandler(
                f"{self.getDirectory()}/{self.getFilename()}",
                mode=self.getFileMode(),
                encoding=self.getEncoding()
            )
            formatter: Formatter = Formatter(self.getFormat())
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)
        return logger
