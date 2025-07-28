from Models.TableModel import Table_Model, Database_Handler, List, RowType


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

    @classmethod
    def getLastRowIdentifier(cls, database_handler: Database_Handler) -> "Click":
        """
        Retrieving the last inserted row's identifier for the Click table.

        Parameters:
            database_handler (Database_Handler): The handler used to execute the query.

        Returns:
            Click: An instance of Click initialized with the last inserted ID.

        Raises:
            ValueError: If the database query returns no result.
        """
        temporary_instance: "Click" = cls(database_handler)
        query: str = "SELECT LAST_INSERT_ID() AS last_identifier"
        response: List[RowType] = temporary_instance.getDatabaseHandler().getData(query)
        if not response:
            raise ValueError("No identifier found in database.")
        return cls(temporary_instance.getDatabaseHandler(), **response[0]) # type: ignore
