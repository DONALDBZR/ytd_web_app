"""
The module that has the data model for the `Session`.
"""
from Models.TableModel import Table_Model, Database_Handler


class Session(Table_Model):
    """
    The model that is used as model to interact with the database for the Session Table.
    """
    def __init__(
        self,
        database_handler: Database_Handler,
        **kwargs
    ):
        """
        Initializing a new Session model instance.

        This constructor passes the database handler and any additional keyword arguments to the parent `Table_Model`, specifically setting the table name to "Session".

        Args:
            database_handler (Database_Handler): The database handler instance to interact with the database.
            **kwargs: Arbitrary keyword arguments that are passed to the parent constructor.  These typically include the model's field values.
        """
        super().__init__(
            database_handler,
            table_name="Session",
            **kwargs
        )