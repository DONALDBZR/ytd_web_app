from Models.TableModel import Table_Model, Database_Handler


class Media(Table_Model):
    """
    It inherits from `Table_Model` and is used to interact with a `Media` table in a database.

    Methods:
        `create()`: Creating the Media table in the database if it does not already exist.
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
