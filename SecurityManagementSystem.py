from ObjectRelationalMapper import Object_Relational_Mapper
from Environment import Environment


class Security_Management_System:
    """
    It will be a major component that will assure the security
    of the data that will be stored across the application.
    """
    __Object_Relational_Mapper: "Object_Relational_Mapper"
    """
    It is the object relational mapper that will be used to
    simplify the process to entering queries.

    Type: Object_Relational_Mapper
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

    def __init__(self) -> None:
        """
        Instantiating the system which will allow the application to
        encrypt and decrypt the data that moves around in the
        application.
        """
        self.setApplicationName(Environment.APPLICATION_NAME)

    def getObjectRelationalMapper(self) -> "Object_Relational_Mapper":
        return self.__Object_Relational_Mapper

    def setObjectRelationalMapper(self, object_relational_mapper: "Object_Relational_Mapper") -> None:
        self.__Object_Relational_Mapper = object_relational_mapper

    def getApplicationName(self) -> str:
        return self.__application_name

    def setApplicationName(self, application_name: str) -> None:
        self.__application_name = application_name

    def getDatestamp(self) -> int:
        return self.__datestamp

    def setDatestamp(self, datestamp: int) -> None:
        self.__datestamp = datestamp
