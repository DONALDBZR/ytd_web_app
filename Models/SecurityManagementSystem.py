"""
The module that has the Security Management System that will
assure the security of the data that will be stored across
the application.

Authors:
    Darkness4869
"""


from Models.SessionModel import Database_Handler, Session
from Models.Logger import Extractio_Logger
from Environment import Environment
from time import time
from argon2 import PasswordHasher
from datetime import datetime
from typing import Union
from base64 import b64encode


class Security_Management_System:
    """
    It is a major component that will assure the security of the data that will be stored across the application.

    Attributes:
        __Database_Handler: Database_Handler
        __application_name: str
        __datestamp: int
        __hash: str
        __password_hasher: PasswordHasher
        __date_created: Union[str, int]
        __logger: Extractio_Logger
        __nonce: str

    Methods:
        hash() -> None: Generating, storing, and cleaning up a security hash.
        generateNonce() -> None: Generating a random nonce that will be used to authenticate the user.
    """
    __Database_Handler: Database_Handler
    """
    It is the object relational mapper that will be used to
    simplify the process to entering queries.
    """
    __application_name: str
    """
    The name of the application.
    """
    __datestamp: int
    """
    The date retrieved from UNIX time.
    """
    __hash: str
    """
    The hash that will be stored in the database.
    """
    __password_hasher: PasswordHasher
    """
    High level class to hash passwords with sensible defaults.
    """
    __date_created: Union[str, int]
    """
    The date at which the key has been created.
    """
    __logger: Extractio_Logger
    """
    The logger that will all the action of the application.
    """
    __nonce: str
    """
    It is often a random or pseudo-random number issued in an
    authentication protocol to ensure that old communications
    cannot be reused in replay attacks.
    """

    def __init__(self) -> None:
        """
        Initializing the Security Management System.

        It sets up the core components of the system.  It performs the following actions:
            1.  Loading environment variables.
            2.  Initializing the application logger.
            3.  Establishing a database connection handler.
            4.  Setting the application name and the current timestamp.
            5.  Creating the Session table if it does not exist.

        Raises:
            SystemExit: If the Session table could not be created.
        """
        ENV: Environment = Environment()
        self.setLogger(Extractio_Logger(__name__))
        self.setDatabaseHandler(Database_Handler())
        self.setApplicationName(ENV.getApplicationName())
        self.setDatestamp(int(time()))
        session: Session = Session(self.getDatabaseHandler())
        response: bool = session.create()
        if not response:
            self.getLogger().error("The table cannot be created.")
            exit(503)
        self.getLogger().inform("The Security Management System has been successfully been initialized!")
        self.hash()

    def getNonce(self) -> str:
        return self.__nonce

    def setNonce(self, nonce: str) -> None:
        self.__nonce = nonce

    def getDatabaseHandler(self) -> Database_Handler:
        return self.__Database_Handler

    def setDatabaseHandler(self, database_handler: Database_Handler) -> None:
        self.__Database_Handler = database_handler

    def getApplicationName(self) -> str:
        return self.__application_name

    def setApplicationName(self, application_name: str) -> None:
        self.__application_name = application_name

    def getDatestamp(self) -> int:
        return self.__datestamp

    def setDatestamp(self, datestamp: int) -> None:
        self.__datestamp = datestamp

    def getHash(self) -> str:
        return self.__hash

    def setHash(self, hash: str) -> None:
        self.__hash = hash

    def getPasswordHasher(self) -> PasswordHasher:
        return self.__password_hasher

    def setPasswordHasher(self, password_hasher: PasswordHasher) -> None:
        self.__password_hasher = password_hasher

    def getDateCreated(self) -> Union[str, int]:
        return self.__date_created

    def setDateCreated(self, date_created: Union[str, int]) -> None:
        self.__date_created = date_created

    def getLogger(self) -> Extractio_Logger:
        return self.__logger

    def setLogger(self, logger: Extractio_Logger) -> None:
        self.__logger = logger

    def hash(self) -> None:
        """
        Generating, storing, and cleaning up a security hash.

        This method performs the following sequence of operations:
            1.  Initializing a new `PasswordHasher` instance.
            2.  Creating a unique string by concatenating the application name with the current datestamp.
            3.  Hashing this unique string to generate a secure key.
            4.  Setting the creation date based on the datestamp.
            5.  Creating a new `Session` object with the generated hash and creation date.
            6.  Saving the new session record to the database.
            7.  If the save is successful, it proceeds to delete all session records from previous days to maintain a clean session table.
            8.  Logging the outcome of both the creation and deletion operations.
        """
        self.setPasswordHasher(PasswordHasher())
        self.setApplicationName(f"{self.getApplicationName()}{str(self.getDatestamp())}")
        self.setHash(self.getPasswordHasher().hash(self.getApplicationName()))
        self.setDateCreated(datetime.fromtimestamp(self.getDatestamp()).strftime("%Y-%m-%d"))
        session: Session = Session(
            self.getDatabaseHandler(),
            hash=self.getHash(),
            date_created=self.getDateCreated()
        )
        response: bool = session.save()
        if not response:
            self.getLogger().error("The key cannot be created.")
            return
        self.getLogger().inform("The key has been created.")
        response: bool = session.deleteOtherThanToday()
        if not response:
            self.getLogger().error("The older keys cannot be deleted.")
            return
        self.getLogger().inform("The older keys are deleted.")

    def generateNonce(self) -> None:
        """
        It will generate a random nonce that will be used to authenticate the user.

        Returns:
            void
        """
        self.setPasswordHasher(PasswordHasher())
        self.setApplicationName(f"{self.getApplicationName()}{int(time())}")
        self.setHash(self.getPasswordHasher().hash(self.getApplicationName()))
        self.setNonce(b64encode(self.getHash().encode("utf-8")).decode("utf-8"))
        self.getLogger().inform("The nonce has been generated!")
