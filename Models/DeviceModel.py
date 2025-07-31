from Models.TableModel import Table_Model, Database_Handler, List, RowType, Tuple


class Device(Table_Model):
    def __init__(
        self,
        database_handler: Database_Handler,
        **kwargs
    ):
        """
        Initializing a Device model instance with the specified database handler.

        Parameters:
            database_handler (Database_Handler): The handler for interacting with the database.
            **kwargs: Additional keyword arguments passed to the parent class.

        Inherits:
            Base_Model: Initializes the base model with the table name set to "Devices".
        """
        super().__init__(
            database_handler,
            table_name="Devices",
            **kwargs
        )
