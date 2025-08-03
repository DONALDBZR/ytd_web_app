from time import time
from typing import Optional
from Models.DatabaseHandler import Database_Handler


class Rate_Limiter:
    """
    It will handle any rate limiting needed for the application.
    """
    __database_handler: Database_Handler
    """
    A class to handle database operations such as connecting, executing queries, and managing transactions.
    """

    def getDatabaseHandler(self) -> Database_Handler:
        return self.__database_handler

    def setDatabaseHandler(self, database_handler: Database_Handler) -> None:
        self.__database_handler = database_handler
