"""
The module that has the Security Management System that will
assure the security of the data that will be stored across
the application.

Authors:
    Darkness4869
"""


from Models.DatabaseHandler import Database_Handler
from Models.Logger import Extractio_Logger
from Environment import Environment
from time import time
from argon2 import PasswordHasher
from datetime import datetime
from typing import Union, Tuple
from base64 import b64encode
from re import search, Match
from binascii import unhexlify


class Security_Management_System:
    """
    It will be a major component that will assure the security
    of the data that will be stored across the application.
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
        Instantiating the system which will allow the application to
        encrypt and decrypt the data that moves around in the
        application.
        """
        ENV: Environment = Environment()
        self.setLogger(Extractio_Logger(__name__))
        self.setDatabaseHandler(Database_Handler())
        self.setApplicationName(ENV.getApplicationName())
        self.setDatestamp(int(time()))
        self.getDatabaseHandler()._query(
            query="CREATE TABLE IF NOT EXISTS `Session` (identifier INT PRIMARY KEY AUTO_INCREMENT, hash VARCHAR(256) NOT NULL, date_created VARCHAR(16), CONSTRAINT unique_constraint_session UNIQUE (hash))",
            parameters=None
        )
        self.getDatabaseHandler()._execute()
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
        It is a one-way encryption function that will generate a
        hash based on the Argon 2 hashing algorithm.

        Returns:
            void
        """
        self.setPasswordHasher(PasswordHasher())
        self.setApplicationName(f"{self.getApplicationName()}{str(self.getDatestamp())}")
        self.setHash(self.getPasswordHasher().hash(self.getApplicationName()))
        self.setDateCreated(datetime.fromtimestamp(self.getDatestamp()).strftime("%Y-%m-%d"))
        data: Tuple[str, str] = (self.getHash(), str(self.getDateCreated()))
        self.getDatabaseHandler().postData(
            table="Session",
            columns="hash, date_created",
            values="%s, %s",
            parameters=data # type: ignore
        )
        self.getLogger().inform("The key has been created!")
        self.getDatabaseHandler().deleteData(
            table="Session",
            parameters=None,
            condition="date_created < CURDATE()"
        )
        self.getLogger().inform("The older keys are deleted!")

    def generateNonce(self) -> None:
        """
        It will generate a random nonce that will be used to
        authenticate the user.

        Returns:
            void
        """
        self.setPasswordHasher(PasswordHasher())
        self.setApplicationName(f"{self.getApplicationName()}{int(time())}")
        self.setHash(self.getPasswordHasher().hash(self.getApplicationName()))
        self.setNonce(b64encode(self.getHashBytes()).decode("utf-8"))

    def getHashBytes(self) -> bytes:
        """
        Retrieving the bytes of the hashed value.

        Returns:
            bytes
        """
        match: Union[Match[str], None] = search(r"\$([0-9a-fA-F]+)$", self.getHash())
        if not match:
            self.getLogger().error("The nonce has not been generated!")
            self.setApplicationName(f"{self.getApplicationName()}{int(time())}")
            self.setHash(self.getPasswordHasher().hash(self.getApplicationName()))
            return self.getHashBytes()
        hash_hexadecimal_value: str = match.group(1)
        try:
            hash_bytes: bytes = unhexlify(hash_hexadecimal_value)
            self.getLogger().inform("The bytes of the hashed has been generated!")
            return hash_bytes
        except ValueError as error:
            self.getLogger().error(f"The error has been raised: {error}")
            self.setApplicationName(f"{self.getApplicationName()}{int(time())}")
            self.setHash(self.getPasswordHasher().hash(self.getApplicationName()))
            return self.getHashBytes()