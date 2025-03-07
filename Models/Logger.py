"""
The module that has the logger of the application.

Authors:
    Darkness4869
"""


from logging.__init__ import Logger
from logging import basicConfig, getLogger as get_logger, DEBUG, INFO, WARNING, ERROR
from Environment import Environment
from re import sub


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
            format="Current Time: %(asctime)s\nModule: %(name)s\nLogging Level: %(levelname)s\nMessage: %(message)s"
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
        self.getLogger().debug(self.sanitize(message))

    def inform(self, message: str) -> None:
        """
        Logging informational data.

        Parameters:
            message: string: The action done.

        Returns:
            void
        """
        self.getLogger().setLevel(INFO)
        self.getLogger().info(self.sanitize(message))

    def warn(self, message: str) -> None:
        """
        Logging the data for a warning.

        Parameters:
            message: string: The action done.

        Returns:
            void
        """
        self.getLogger().setLevel(WARNING)
        self.getLogger().warning(self.sanitize(message))

    def error(self, message: str) -> None:
        """
        Logging the data for an error.

        Parameters:
            message: string: The action done.

        Returns:
            void
        """
        self.getLogger().setLevel(ERROR)
        self.getLogger().error(self.sanitize(message))

    def sanitize(self, message: str) -> str:
        """
        Removing control characters from the given message.

        This method ensures that the input string does not contain any non-printable ASCII control characters.  These characters can cause issues in logging, databases, or user interfaces.

        Parameters:
            message (string): The input string to be sanitized.

        Returns:
            string
        """
        return sub(r"[\x00-\x1F\x7F-\x9F]", "", message)
