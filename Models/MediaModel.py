from Models.TableModel import Table_Model, Database_Handler, List, Tuple, RowType


class Media(Table_Model):
    """
    It inherits from `Table_Model` and is used to interact with a `Media` table in a database.

    Methods:
        `create()`: Creating the Media table in the database if it does not already exist.
        `getByValue()`: Retrieving Media records from the database with a given value.
    """
    def __init__(
        self,
        database_handler: Database_Handler,
        **kwargs
    ):
        """
        Initializing a Media model instance with the specified database handler.

        Parameters:
            database_handler (Database_Handler): The handler for interacting with the database.
            **kwargs: Additional keyword arguments passed to the parent class.

        Inherits:
            Table_Model: Initializes the base model with the table name set to "Media".
        """
        super().__init__(
            database_handler,
            table_name="Media",
            **kwargs
        )

    def create(self) -> bool:
        """
        Creating the Media table in the database if it does not already exist.

        Returns:
            bool: True if the table was created, False otherwise.
        """
        query: str = f"CREATE TABLE IF NOT EXISTS `{self.getTableName()}` (identifier INT PRIMARY KEY AUTO_INCREMENT, `value` VARCHAR(8))"
        return self.getDatabaseHandler().createTable(query, None)

    @classmethod
    def getByValue(cls, database_handler: Database_Handler, value: str) -> List["Media"]:
        """
        Retrieving Media records from the database with a given value.

        Args:
            database_handler (Database_Handler): The database handler instance to interact with the database.
            value (str): The value to search for in the database.

        Returns:
            List[Media]: A list of Media instances matching the given value.
        """
        temporary_instance: "Media" = cls(database_handler)
        query: str = f"SELECT * FROM {temporary_instance.getTableName()} WHERE value = %s"
        parameters: Tuple[str] = (value,)
        response: List[RowType] = temporary_instance.getDatabaseHandler().getData(query, parameters)
        if not response:
            return []
        return [cls(database_handler, **row) for row in response] # type: ignore
