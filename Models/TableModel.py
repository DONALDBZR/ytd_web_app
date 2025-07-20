from Models.DatabaseHandler import Database_Handler, List


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
