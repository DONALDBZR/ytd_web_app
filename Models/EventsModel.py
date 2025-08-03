from Models.TableModel import Table_Model, Database_Handler, List, RowType, Tuple


class Event(Table_Model):
    """
    The class which interacts for all of the database operations for the `Events` table.

    Methods:
        `countConnections()`: Counting the number of event connections for a specific IP address and endpoint within a given time window.
    """
    def __init__(
        self,
        database_handler: Database_Handler,
        **kwargs
    ):
        """
        Initializing an Event model instance with the specified database handler.

        Parameters:
            database_handler (Database_Handler): The handler for interacting with the database.
            **kwargs: Additional keyword arguments passed to the parent class.

        Inherits:
            Base_Model: Initializes the base model with the table name set to "Events".
        """
        super().__init__(
            database_handler,
            table_name="Events",
            **kwargs
        )

    @classmethod
    def countConnections(
        cls,
        database_handler: Database_Handler,
        ip_address: str,
        endpoint: str,
        start_window: int
    ) -> int:
        """
        Counting the number of event connections for a specific IP address and endpoint within a given time window.

        This class method queries the `Events` table, joining with the `NetworkLocation` table, to count the number of records that match the specified IP address, endpoint, and have a timestamp greater than the provided start window.

        Args:
            database_handler (Database_Handler): The handler for executing database queries.
            ip_address (str): The IP address to filter event connections.
            endpoint (str): The endpoint (uniform resource locator) to filter event connections.
            start_window (int): The timestamp representing the start of the time window.

        Returns:
            int: The count of event connections matching the specified criteria.
        """
        temporary_instance: "Event" = cls(database_handler)
        join_table: str = "NetworkLocation"
        query: str = f"SELECT {temporary_instance.getTableName()}.uniform_resource_locator, FROM_UNIXTIME({temporary_instance.getTableName()}.timestamp), NetworkLocation.ip_address FROM {temporary_instance.getTableName()} INNER JOIN {join_table} ON {temporary_instance.getTableName()}.NetworkLocation = {join_table}.identifier WHERE {join_table}.ip_address = %s AND {temporary_instance.getTableName()}.uniform_resource_locator = %s AND {temporary_instance.getTableName()}.timestamp > %s"
        parameters: Tuple[str, str, int] = (ip_address, endpoint, start_window)
        response: List[RowType] = temporary_instance.getDatabaseHandler().getData(query, parameters)
        return len(response)
