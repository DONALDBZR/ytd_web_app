from Models.TableModel import Table_Model, Database_Handler, List, RowType, Tuple


class Event_Types(Table_Model):
    """
    The model which will interact exclusively with the EventTypes table.

    Methods:
        `getByName(cls, database_handler: Database_Handler, name: str) -> List["Event_Types"]`: Fetching event type records from the database by their name.
    """
    def __init__(
        self,
        database_handler: Database_Handler,
        **kwargs
    ):
        """
        Initializing a Event_Types model instance with the specified database handler.

        Parameters:
            database_handler (Database_Handler): The handler for interacting with the database.
            **kwargs: Additional keyword arguments passed to the parent class.

        Inherits:
            Base_Model: Initializes the base model with the table name set to "EventTypes".
        """
        super().__init__(
            database_handler,
            table_name="EventTypes",
            **kwargs
        )

    @classmethod
    def getByName(cls, database_handler: Database_Handler, name: str) -> List["Event_Types"]:
        """
        Fetching event type records from the database by their name.

        Args:
            database_handler (Database_Handler): The database handler used to execute the query.
            name (str): The name of the event type to retrieve.

        Returns:
            List[Event_Types]: A list of Event_Types instances that match the given name.
        """
        temporary_instance: "Event_Types" = cls(database_handler)
        query: str = f"SELECT * FROM {temporary_instance.getTableName()} WHERE name = %s"
        parameters: Tuple[str] = (name,)
        response: List[RowType] = temporary_instance.getDatabaseHandler().getData(query, parameters)
        if not response:
            return []
        return [cls(database_handler, **row) for row in response] # type: ignore
