import logging
from logging.__init__ import Logger


class ExtractioLogger:
    """
    The logger that will all the action of the application.
    """
    __logger: Logger
    """
    It is responsible for logging all of the actions done by the
    application.
    
    Type: Logger
    visibility: private
    """

    def __init__(self) -> None:
        """
        Instantiating the Logger which will keep track of everything
        that the application does.
        """
        logging.basicConfig(
            filename="../Logs/Extractio.log", encoding="utf-8", filemode="w", format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        self.setLogger(logging.getLogger(__name__))

    def getLogger(self) -> Logger:
        return self.__logger

    def setLogger(self, logger: Logger) -> None:
        self.__logger = logger
