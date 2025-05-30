"""
The module for the custom logger of the application.

Authors:
    Darkness4869
"""
from logging.__init__ import Logger
from logging import basicConfig, getLogger as get_logger, DEBUG, INFO, WARNING, ERROR
from Environment import Environment
from re import sub


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
        Initializing the Extractio_Logger.

        It configures the basic logging settings, including the log file location, encoding, file mode, and log message format.  Retrieves the log file directory from the application's environment.

        Parameters:
            name (str): The name of the logger.
        """
        ENV = Environment()
        basicConfig(
            filename=f"{ENV.getDirectory()}/Logs/Extractio.log",
            encoding="utf-8",
            filemode="a",
            format="Current Time: %(asctime)s\nModule: %(name)s\nLogging Level: %(levelname)s\nMessage: %(message)s"
        )
        self.setLogger(get_logger(name))

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
