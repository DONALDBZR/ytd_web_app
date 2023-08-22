from ObjectRelationalMapper import Object_Relational_Mapper


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

    def getObjectRelationalMapper(self) -> "Object_Relational_Mapper":
        return self.__Object_Relational_Mapper

    def setObjectRelationalMapper(self, object_relational_mapper: "Object_Relational_Mapper") -> None:
        self.__Object_Relational_Mapper = object_relational_mapper
