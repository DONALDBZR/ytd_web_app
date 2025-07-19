from logging.__init__ import Logger
from logging import basicConfig, DEBUG, INFO, WARNING, ERROR
from typing import Callable, Optional
from Models.LoggerConfigurator import Logger_Configurator


class Extractio_Logger:
    __logger: Logger
    """
    The underlying logger instance from Python's logging module.
    """
    __configurator: Logger_Configurator
    """
    The configurator instance that manages the logging settings.
    """

    def __init__(self, name: str, configurator: Optional[Logger_Configurator] = None):
        """
        Initializing the Extractio_Logger instance.

        This constructor creates a logger instance tied to a specific name, typically the `__name__` of the calling module.  It uses a `Logger_Configurator` instance to apply the logging configuration, such as setting up file handlers and formatters.

        If a `configurator` is not provided, a default `Logger_Configurator` is created and used.

        Args:
            name (str): The name to associate with the logger instance.
            configurator (Optional[Logger_Configurator]): The configuration object to use for setting up the logger.
        """
        self.setConfigurator(configurator or Logger_Configurator())
        self.setLogger(self.getConfigurator().configure(name))

    def getLogger(self) -> Logger:
        return self.__logger

    def setLogger(self, logger: Logger) -> None:
        self.__logger = logger

    def getConfigurator(self) -> Logger_Configurator:
        return self.__configurator

    def setConfigurator(self, configurator: Logger_Configurator) -> None:
        self.__configurator = configurator

    def __configureLogging(
        self,
        filepath: str,
        format: str = "[%(asctime)s] [%(name)s] [%(levelname)s] %(message)s",
        encoding: str = "utf-8",
        filemode: str = "a",
        configurator: Callable = basicConfig
    ) -> None:
        """
        Configuring the logging settings.

        Args:
            filepath (str): Path to the log file.
            format (str): Log message format.
            encoding (str): File encoding.
            filemode (str): File open mode.
            configurator (Callable): Function to apply configuration (default: logging.basicConfig)

        Returns:
            None
        """
        configurator(
            filename=filepath,
            encoding=encoding,
            filemode=filemode,
            format=format
        )

    def __log(self, level: int, message: str) -> None:
        """
        Logging a message at the specified logging level.

        Args:
            level (int): The severity level to be used for logging.
            message (str): The message to log.

        Returns:
            None
        """
        if not self.getLogger().isEnabledFor(level):
            return
        self.getLogger().log(level, message)

    def debug(self, message: str) -> None:
        """
        Logging a debug message.

        Parameters:
            message (str): The message to log.
        """
        self.__log(DEBUG, message)

    def inform(self, message: str) -> None:
        """
        Logging an informational message.

        Parameters:
            message (str): The message to log.
        """
        self.__log(INFO, message)

    def warn(self, message: str) -> None:
        """
        Logging a warning message.

        Parameters:
            message (str): The message to log.
        """
        self.__log(WARNING, message)

    def error(self, message: str) -> None:
        """
        Logging an error message.

        Parameters:
            message (str): The message to log.
        """
        self.__log(ERROR, message)
