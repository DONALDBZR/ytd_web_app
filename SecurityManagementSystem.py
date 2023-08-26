from DatabaseHandler import Database_Handler
from Environment import Environment
from time import time
from argon2 import PasswordHasher
from datetime import datetime


class Security_Management_System:
    """
    It will be a major component that will assure the security
    of the data that will be stored across the application.
    """
    __Database_Handler: "Database_Handler"
    """
    It is the object relational mapper that will be used to
    simplify the process to entering queries.

    Type: Database_Handler
    Visibility: Private
    """
    __application_name: str
    """
    The name of the application.

    Type: string
    Visibility: Private
    """
    __datestamp: int
    """
    The date retrieved from UNIX time.

    Type: int
    Visibility: Private
    """
    __hash: str
    """
    The hash that will be stored in the database.

    Type: string
    Visibility: Private
    """
    __password_hasher: "PasswordHasher"
    """
    High level class to hash passwords with sensible defaults.

    Type: Password_Hasher
    Visibility: private
    """
    __date_created: str | int
    """
    The date at which the key has been created.

    Type: string | int
    Visibility: private
    """

    def __init__(self) -> None:
        """
        Instantiating the system which will allow the application to
        encrypt and decrypt the data that moves around in the
        application.
        """
        self.setObjectRelationalMapper(Object_Relational_Mapper())
        self.setApplicationName(Environment.APPLICATION_NAME)
        self.setDatestamp(int(time()))
        self.getObjectRelationalMapper().query("CREATE TABLE IF NOT EXISTS `Session` (identifier INT PRIMARY KEY AUTO_INCREMENT, hash VARCHAR(256) NOT NULL, date_created VARCHAR(16), CONSTRAINT unique_constraint_session UNIQUE (hash))", None)
        self.getObjectRelationalMapper().execute()
        self.hash()

    def getDatabaseHandler(self) -> "Database_Handler":
        return self.__Database_Handler

    def setDatabaseHandler(self, database_handler: "Database_Handler") -> None:
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

    def getPasswordHasher(self) -> "PasswordHasher":
        return self.__password_hasher

    def setPasswordHasher(self, password_hasher: "PasswordHasher") -> None:
        self.__password_hasher = password_hasher

    def getDateCreated(self) -> str | int:
        return self.__date_created

    def setDateCreated(self, date_created: str | int) -> None:
        self.__date_created = date_created

    def hash(self) -> None:
        """
        It is a one-way encryption function that will generate a
        hash based on the Argon 2 hashing algorithm.

        Returns: void
        """
        self.setPasswordHasher(PasswordHasher())
        self.setApplicationName(
            self.getApplicationName() + str(self.getDatestamp()))
        self.setHash(self.getPasswordHasher().hash(self.getApplicationName()))
        self.setDateCreated(datetime.fromtimestamp(
            self.getDatestamp()).strftime("%Y-%m-%d"))
        self.getObjectRelationalMapper().post_data(
            "Session", "hash, date_created", "%s, %s", [self.getHash(), self.getDateCreated()])
