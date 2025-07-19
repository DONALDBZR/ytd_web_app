"""
The module for the custom logger of the application.

Authors:
    Darkness4869
"""
from logging.__init__ import Logger
from logging import basicConfig, getLogger as get_logger, DEBUG, INFO, WARNING, ERROR
from Environment import Environment
from typing import Callable


class Extractio_Logger:
    """
    A custom logger class for the Extractio application.

    This class provides methods for logging messages at different levels and sanitizes log messages to remove control characters.  It utilizes Python's built-in logging module and is configured to write log messages to a file specified in the application's environment.
    """
    __logger: Logger
    """
    The underlying logger instance from Python's logging module.
    """

    def __init__(self, name: str):
        """
        Initializing the ExtractioLogger.

        This method functions as follows:
            - It configures the logger to used the directory provided by the environment.
            - It sets the logger instance.

        Args:
            name (str): Name of the logger.
        """
        env = Environment()
        log_filepath: str = f"{env.getDirectory()}/Logs/Extractio.log"
        self.__configureLogging(log_filepath)
        self.setLogger(get_logger(name))

    def getLogger(self) -> Logger:
        return self.__logger

    def setLogger(self, logger: Logger) -> None:
        self.__logger = logger

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

        This method logs a message at the ERROR level after sanitizing it.  It also prints the message to the console.

        Parameters:
            message (str): The message to log.
        """
        self.getLogger().setLevel(ERROR)
        self.getLogger().error(message)
