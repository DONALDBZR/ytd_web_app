from Environment import Environment
from logging import Logger, getLogger, FileHandler, Formatter, DEBUG


class Logger_Configurator:
    """
    A class to configure logging settings for the Extractio application.

    This class allows customization of the log file's location, name, message format, encoding and file mode.
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

    def __init__(
        self,
        directory: str = "Logs",
        filename: str = "Extractio.log",
        format: str = "[%(asctime)s] [%(name)s] [%(levelname)s] %(message)s",
        encoding: str = "utf-8",
        file_mode: str = "a"
    ):
        """
        Initializing the Logger_Configurator with specified or default settings.

        This constructor sets up the configuration that will be used to create and configure logger instances.  It allows customization of the log file's location, name, message format, and other properties.  If a directory is not explicitly provided, it defaults to a 'Logs' subdirectory within the application's main directory, as determined by the `Environment` class.

        Args:
            directory (str, optional): The path to the directory where the log file will be stored.
            filename (str, optional): The name of the log file.
            format (str, optional): The format string for log messages.
            encoding (str, optional): The character encoding for the log file.
            file_mode (str, optional): The file mode for opening the log file.
        """
        env: Environment = Environment()
        self.setDirectory(directory if directory else f"{env.getDirectory()}/Logs")
        self.setFilename(filename)
        self.setFormat(format)
        self.setEncoding(encoding)
        self.setFileMode(file_mode)

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
