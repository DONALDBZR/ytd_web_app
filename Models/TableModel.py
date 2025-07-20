from Models.DatabaseHandler import Database_Handler, List, RowType, Tuple, Any, Optional
from typing import Dict


class TableModel:
    __table_name: str
    """
    The name of the table.
    """
    __database_handler: Database_Handler
    """
    The database handler instance to interact with the database.
    """
    __fields: List[str]
    """
    A list of fields in the table.
    """
    __mysql_field_types: Dict[str, type]
    """
    A dictionary mapping field names to their MySQL types.
    """
    __field_types: Dict[str, str]
    """
    A dictionary mapping field names to their types, used for validation and sanitization.
    """

    def __init__(
        self,
        database_handler: Database_Handler,
        **kwargs
    ):
        """
        Initializing the TableModel with a database handler and optional table name and fields.

        Args:
            database_handler (Database_Handler): The database handler instance to interact with the database.
            **kwargs: Optional keyword arguments for table name and fields.
        """
        self.setDatabaseHandler(database_handler)
        fields, field_types = self._getFields()
        self.setFields(fields)
        self.setFieldTypes(field_types)
        self.setMySqlFieldTypes({
            "int": int,
            "bigint": int,
            "smallint": int,
            "tinyint": int,
            "mediumint": int,
            "float": float,
            "double": float,
            "decimal": float,
            "char": str,
            "varchar": str,
            "text": str,
            "mediumtext": str,
            "longtext": str,
            "date": str,
            "datetime": str,
            "timestamp": str,
            "time": str,
            "enum": str,
            "set": str,
            "blob": bytes,
            "binary": bytes,
            "varbinary": bytes
        })
        self.setModelAttributes(kwargs)

    def getTableName(self) -> str:
        return self.__table_name

    def setTableName(self, table_name: str) -> None:
        self.__table_name = table_name

    def getDatabaseHandler(self) -> Database_Handler:
        return self.__database_handler

    def setDatabaseHandler(self, database_handler: Database_Handler) -> None:
        self.__database_handler = database_handler

    def getFields(self) -> List[str]:
        return self.__fields

    def setFields(self, fields: List[str]) -> None:
        self.__fields = fields

    def getFieldTypes(self) -> Dict[str, str]:
        return self.__field_types

    def setFieldTypes(self, field_types: Dict[str, str]) -> None:
        self.__field_types = field_types

    def getMySqlFieldTypes(self) -> Dict[str, type]:
        return self.__mysql_field_types

    def setMySqlFieldTypes(self, mysql_field_types: Dict[str, type]) -> None:
        self.__mysql_field_types = mysql_field_types

    def _getFields(self) -> Tuple[List[str], Dict[str, str]]:
        """
        Fetching the column names and types for the table from the database.

        Returns:
            Tuple[List[str], Dict[str, str]]: A tuple containing a list of field names and a dictionary mapping field names to their MySQL types.
        """
        database_response: List[RowType] = self.getDatabaseHandler().getData(f"SHOW COLUMNS FROM {self.getTableName()}")
        fields: List[str] = [str(column["Field"]) for column in database_response] # type: ignore
        field_types: Dict[str, str] = {str(column["Field"]): str(column["Type"]) for column in database_response} # type: ignore
        return fields, field_types

    def setModelAttributes(self, kwargs: Dict[str, Any]) -> None:
        """
        Setting the model attributes based on the provided keyword arguments.

        Args:
            kwargs (Dict[str, Any]): Keyword arguments containing the attributes to set.
        """
        for field in self.getFields():
            setattr(self, field, kwargs.get(field))

    def mySqlTypeToPython(self, mysql_type: str) -> type:
        """
        Converting a MySQL type to its corresponding Python type.

        Args:
            mysql_type (str): The MySQL type as a string.

        Returns:
            type: The corresponding Python type.
        """
        base: str = mysql_type.split("(")[0].lower()
        return self.getMySqlFieldTypes().get(base, type)

    @classmethod
    def getById(cls, database_handler: Database_Handler,primary_key: Any) -> Optional["TableModel"]:
        """
        Retrieving a model instance by its primary key.

        Args:
            database_handler (Database_Handler): The database handler instance to interact with the database.
            primary_key (Any): The primary key value to search for.

        Returns:
            Optional[TableModel]: The model instance if found, otherwise None.
        """
        query: str = f"SELECT * FROM {cls.__table_name} WHERE id = %s"
        response: List[RowType] = database_handler.getData(query, (primary_key,))
        if not response:
            return None
        return cls(database_handler, **response[0])
