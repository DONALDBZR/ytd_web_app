from Models.TableModel import Table_Model, Database_Handler, List, RowType, Tuple, Any


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

    def save(self) -> bool:
        """
        Inserting the current network location instance into the database.

        This method constructs an SQL INSERT query using the instance's fields, excluding the primary key.  It then executes the query with the appropriate parameters to save the network location data into the `NetworkLocation` table, including geographic coordinates as a spatial point.

        Returns:
            bool: True if the data was successfully inserted, False otherwise.
        """
        fields: List[str] = [field for field in self.getFields() if field != self.getPrimaryField()]
        parameters: Tuple[str, str, float, float, str, str, str, str, float, float] = (self.ip_address, self.hostname, self.latitude, self.longitude, self.city, self.region, self.country, self.timezone, self.latitude, self.longitude) # type: ignore
        query: str = f"INSERT INTO {self.getTableName()} ({', '.join(fields)}) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, ST_SRID(ST_GeomFromText(CONCAT('POINT(', %s, ' ', %s, ')')), 4326))"
        return self.getDatabaseHandler().postData(query, parameters)

    @classmethod
    def getByHostname(cls, database_handler: Database_Handler, hostname: str) -> List[str]:
        """
        Retrieving a list of IP addresses associated with a hostname from the database based on activity within the last 24 hours.

        This class method queries the `NetworkLocation` table, joining with the `Events` table, to fetch a list of IP addresses associated with a given hostname.  The query includes a filter for timestamps within the last 24 hours and groups the results by IP address.

        Args:
            database_handler (Database_Handler): The handler for executing database queries.
            hostname (str): The hostname to filter network locations.

        Returns:
            List[str]: A list of IP addresses associated with the given hostname.
        """
        temporary_instance: "Network_Location" = cls(database_handler)
        indexed_table: str = "Events"
        query: str = f"SELECT {temporary_instance.getTableName()}.ip_address FROM {temporary_instance.getTableName()} INNER JOIN {indexed_table} ON {temporary_instance.getTableName()}.identifier = {indexed_table}.NetworkLocation AND {indexed_table}.timestamp >=UNIX_TIMESTAMP(DATE_SUB(NOW(), INTERVAL 1 DAY)) WHERE {temporary_instance.getTableName()}.hostname = %s GROUP BY {temporary_instance.getTableName()}.ip_address"
        parameters: Tuple[str] = (hostname,)
        database_response: List[RowType] = temporary_instance.getDatabaseHandler().getData(query, parameters)
        if not database_response:
            return []
        response: List["Network_Location"] = [cls(database_handler, **row) for row in database_response] # type: ignore
        if not response:
            return []
        return [row.ip_address for row in response] # type: ignore

    @classmethod
    def getLocationDataByIpAddress(cls, database_handler: Database_Handler, ip_address: str) -> List["Network_Location"]:
        """
        Retrieving location data records from the database that match the given IP address and were active within the last 24 hours.

        This class method queries the `NetworkLocation` table, joining with the `Events` table, to fetch a list of location data associated with a given IP address.  The query includes a filter for timestamps within the last 24 hours and groups the results by IP address.

        Args:
            database_handler (Database_Handler): The handler for executing database queries.
            ip_address (str): The IP address to filter network locations.

        Returns:
            List[Network_Location]: A list of Network_Location instances containing location data matching the given IP address.
        """
        temporary_instance: "Network_Location" = cls(database_handler)
        indexed_table: str = "Events"
        query: str = f"SELECT {temporary_instance.getTableName()}.latitude, {temporary_instance.getTableName()}.longitude, {temporary_instance.getTableName()}.city, {temporary_instance.getTableName()}.region, {temporary_instance.getTableName()}.country FROM {temporary_instance.getTableName()} INNER JOIN {indexed_table} ON {temporary_instance.getTableName()}.identifier = {indexed_table}.NetworkLocation AND {indexed_table}.timestamp >= UNIX_TIMESTAMP(DATE_SUB(NOW(), INTERVAL 1 DAY)) WHERE {temporary_instance.getTableName()}.ip_address = %s ORDER BY {indexed_table}.timestamp ASC"
        parameters: Tuple[str] = (ip_address,)
        response: List[RowType] = temporary_instance.getDatabaseHandler().getData(query, parameters)
        if not response:
            return []
        return [cls(database_handler, **row) for row in response] # type: ignore
