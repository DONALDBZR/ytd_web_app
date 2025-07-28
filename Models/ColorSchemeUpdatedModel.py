from Models.TableModel import Table_Model, Database_Handler, List, RowType, Tuple


class Color_Scheme_Updated(Table_Model):
    def __init__(
        self,
        database_handler: Database_Handler,
        **kwargs
    ):
        """
        Initializing a Color_Scheme_Updated model instance with the specified database handler.

        Parameters:
            database_handler (Database_Handler): The handler for interacting with the database.
            **kwargs: Additional keyword arguments passed to the parent class.

        Inherits:
            Initializing the base model with the table name set to "ColorSchemeUpdated".
        """
        super().__init__(
            database_handler,
            table_name="ColorSchemeUpdated",
            **kwargs
        )
