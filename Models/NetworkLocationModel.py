from Models.TableModel import Table_Model, Database_Handler, List, RowType, Tuple


class Network_Location(Table_Model):
    def __init__(
        self,
        database_handler: Database_Handler,
        **kwargs
    ):
        """
        Initializing a Network_Location model instance with the specified database handler.

        Parameters:
            database_handler (Database_Handler): The handler for interacting with the database.
            **kwargs: Additional keyword arguments passed to the parent class.

        Inherits:
            Base_Model: Initializes the base model with the table name set to "NetworkLocation".
        """
        super().__init__(
            database_handler,
            table_name="NetworkLocation",
            **kwargs
        )

    @classmethod
    def getByIpAndLocation(
        cls,
        database_handler: Database_Handler,
        ip_address: str,
        location: List[float]
    ) -> List["Network_Location"]:
        """
        Retrieving all network location records that match a given IP address and geographical location.

        Args:
            database_handler (Database_Handler): Instance for interacting with the database.
            ip_address (str): The IP address to query.
            location (List[float]): A list containing the latitude and longitude [latitude, longitude].

        Returns:
            List[Network_Location]: A list of Network_Location instances matching the given criteria.
        """
        temporary_instance: "Network_Location" = cls(database_handler)
        query: str = f"SELECT * FROM {temporary_instance.getTableName()} WHERE ip_address = %s AND latitude = %s AND longitude = %s"
        parameters: Tuple[str, float, float] = (ip_address, location[0], location[1])
        response: List[RowType] = temporary_instance.getDatabaseHandler().getData(query, parameters)
        if not response:
            return []
        return [cls(database_handler, **row) for row in response] # type: ignore
