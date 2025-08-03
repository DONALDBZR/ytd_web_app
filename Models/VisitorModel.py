from Models.TableModel import Table_Model, Database_Handler, RowType, List


class Visitor(Table_Model):
    """
    The model to be used for interacting with the `Visitors` table in the database.

    Methods:
        `create()`: Creating the Visitor table in the database if it does not already exist.
    """
    def __init__(
        self,
        database_handler: Database_Handler,
        **kwargs
    ):
        """
        Initializing a Visitor model instance with the specified database handler.

        Parameters:
            database_handler (Database_Handler): The handler for interacting with the database.
            **kwargs: Additional keyword arguments passed to the parent class.

        Inherits:
            Initializing the base model with the table name set to "Visitor".
        """
        super().__init__(
            database_handler,
            table_name="Visitor",
            **kwargs
        )

    def create(self) -> bool:
        """
        Creating the Visitor table in the database if it does not already exist.

        This method constructs a SQL query to create the Visitor table with fields for identifier, timestamp, and client.  It then executes the query using the database handler.

        Returns:
            bool: True if the table was created successfully, False otherwise.
        """
        query: str = f"CREATE TABLE IF NOT EXISTS `{self.getTableName()}` (identifier INT PRIMARY KEY AUTO_INCREMENT, `timestamp` INT, client VARCHAR(16))"
        return self.getDatabaseHandler().createTable(query, None)
