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

    @classmethod
    def getByDeviceType(
        cls,
        database_handler: Database_Handler,
        user_agent: str,
        screen_resolution: str
    ) -> List["Device"]:
        """
        Fetching device records from the database that match the given user agent and screen resolution.

        Args:
            database_handler (Database_Handler): The database handler to use for the query.
            user_agent (str): The user agent string to match.
            screen_resolution (str): The screen resolution to match.

        Returns:
            List[Device]: A list of Device instances that match the given criteria.
        """
        temporary_instance: "Device" = cls(database_handler)
        query: str = f"SELECT * FROM {temporary_instance.getTableName()} WHERE user_agent = %s AND screen_resolution = %s"
        parameters: Tuple[str, str] = (user_agent, screen_resolution)
        response: List[RowType] = temporary_instance.getDatabaseHandler().getData(query, parameters)
        if not response:
            return []
        return [cls(database_handler, **row) for row in response] # type: ignore
