from Models.DatabaseHandler import Database_Handler, List, RowType, Tuple, Any
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
    __fields: Tuple[List[str], Dict[str, str]]
    """
    A list of fields in the table.
    """
    __mysql_field_types: Dict[str, Any]
    """
    A dictionary mapping field names to their MySQL types.
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
        self.setFields(self._getFields())
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

    def getFields(self) -> Tuple[List[str], Dict[str, str]]:
        return self.__fields

    def setFields(self, fields: Tuple[List[str], Dict[str, str]]) -> None:
        self.__fields = fields

    def getMySqlFieldTypes(self) -> Dict[str, Any]:
        return self.__mysql_field_types

    def setMySqlFieldTypes(self, mysql_field_types: Dict[str, Any]) -> None:
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
