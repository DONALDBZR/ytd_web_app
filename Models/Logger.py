"""
The Extractio_Logger module provides a logger class for the Extractio application.

Author:
    Darkness4869
"""
from logging.__init__ import Logger
from typing import Optional
from Models.LoggerConfigurator import Logger_Configurator


class Extractio_Logger:
    """
    A class to create and manage a logger instance for the Extractio application.
    
    This class encapsulates a logger instance and provides methods to log messages at different severity levels (debug, info, warning, error).
    """
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

    def debug(self, message: str) -> None:
        """
        Logging a debug message.

        Parameters:
            message (str): The message to log.
        """
        self.getLogger().debug(message)

    def inform(self, message: str) -> None:
        """
        Logging an informational message.

        Parameters:
            message (str): The message to log.
        """
        self.getLogger().info(message)

    def warn(self, message: str) -> None:
        """
        Logging a warning message.

        Parameters:
            message (str): The message to log.
        """
        self.getLogger().warning(message)

    def error(self, message: str) -> None:
        """
        Logging an error message.

        Parameters:
            message (str): The message to log.
        """
        self.getLogger().error(message)
