"""
The module that has the logger of the application.

Authors:
    Darkness4869
"""

from logging.__init__ import Logger
from logging import basicConfig, getLogger as get_logger, DEBUG, INFO, WARNING, ERROR
from Environment import Environment


class Extractio_Logger:
    """
    The logger that will all the action of the application.
    """
    __logger: Logger
    """
    It is responsible for logging all of the actions done by the
    application.
    """

    def __init__(self, name: str):
        """
        Instantiating the Logger which will keep track of everything
        that the application does.

        Parameters:
            name: string: The name of the logger.
        """
        ENV = Environment()
        basicConfig(
            filename=f"{ENV.getDirectory()}/Logs/Extractio.log",
            encoding="utf-8",
            filemode="a",
            format="----------\nCurrent Time: %(asctime)s\nModule: %(name)s\nLogging Level: %(levelname)s\nMessage: %(message)s"
        )
        self.setLogger(get_logger(name))

    def getLogger(self) -> Logger:
        return self.__logger

    def setLogger(self, logger: Logger) -> None:
        self.__logger = logger

    def debug(self, message: str) -> None:
        """
        Logging the data for debugging

        Parameters:
            message: string: The action done.

        Returns:
            void
        """
        self.getLogger().setLevel(DEBUG)
        self.getLogger().debug(message)

    def inform(self, message: str) -> None:
        """
        Logging informational data.

        Parameters:
            message: string: The action done.

        Returns:
            void
        """
        self.getLogger().setLevel(INFO)
        self.getLogger().info(message)

    def warn(self, message: str) -> None:
        """
        Logging the data for a warning.

        Parameters:
            message: string: The action done.

        Returns:
            void
        """
        self.getLogger().setLevel(WARNING)
        self.getLogger().warning(message)

    def error(self, message: str) -> None:
        """
        Logging the data for an error.

        Parameters:
            message: string: The action done.

        Returns:
            void
        """
        self.getLogger().setLevel(ERROR)
        self.getLogger().error(message)
