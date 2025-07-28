from Models.TableModel import Table_Model, Database_Handler


class Click(Table_Model):
    def __init__(
        self,
        database_handler: Database_Handler,
        **kwargs
    ):
        """
        Initializing a Click model instance with the specified database handler.

        Parameters:
            database_handler (Database_Handler): The handler for interacting with the database.
            **kwargs: Additional keyword arguments passed to the parent class.

        Inherits:
            Initializing the base model with the table name set to "Click".
        """
        super().__init__(
            database_handler,
            table_name="Click",
            **kwargs
        )
