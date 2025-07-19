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

    def __init__(
        self,
        name: str,
        log_configurator: Callable,
        env: Environment,
        logger_provider: Callable[[str], Logger]
    ):
        """
        Initializing the ExtractioLogger using injected dependencies for configuration and environment.

        Args:
            name (str): Name of the logger.
            log_configurator (Callable): A function to configure logging.
            env (Environment): Environment instance to retrieve directories.
            logger_provider (Callable): A function that returns a logger given a name.
        """
        log_file: str = f"{env.getDirectory()}/Logs/Extractio.log"
        log_configurator(log_file)
        self.setLogger(logger_provider(name))

    def getLogger(self) -> Logger:
        return self.__logger

    def setLogger(self, logger: Logger) -> None:
        self.__logger = logger

    def debug(self, message: str) -> None:
        """
        Logging a debug message.

        This method logs a message at the DEBUG level after sanitizing it.  It also prints the message to the console.

        Parameters:
            message (str): The message to log.
        """
        self.getLogger().setLevel(DEBUG)
        self.getLogger().debug(message)

    def inform(self, message: str) -> None:
        """
        Logging an informational message.

        This method logs a message at the INFO level after sanitizing it.  It also prints the message to the console.

        Parameters:
            message (str): The message to log.
        """
        self.getLogger().setLevel(INFO)
        self.getLogger().info(message)

    def warn(self, message: str) -> None:
        """
        Logging a warning message.

        This method logs a message at the WARNING level after sanitizing it.  It also prints the message to the console.

        Parameters:
            message (str): The message to log.
        """
        self.getLogger().setLevel(WARNING)
        self.getLogger().warning(message)

    def error(self, message: str) -> None:
        """
        Logging an error message.

        This method logs a message at the ERROR level after sanitizing it.  It also prints the message to the console.

        Parameters:
            message (str): The message to log.
        """
        self.getLogger().setLevel(ERROR)
        self.getLogger().error(message)
