from Models.TableModel import Table_Model, Database_Handler, RowType, List, Tuple, Any, Optional


class YouTube(Table_Model):
    def __init__(
        self,
        database_handler: Database_Handler,
        **kwargs
    ):
        """
        Initializing a new YouTube model instance.

        This constructor passes the database handler and any additional keyword arguments to the parent `Table_Model`, specifically setting the table name to "YouTube".

        Args:
            database_handler (Database_Handler): The database handler instance to interact with the database.
            **kwargs: Arbitrary keyword arguments that are passed to the parent constructor.  These typically include the model's field values.
        """
        super().__init__(
            database_handler,
            table_name="YouTube",
            **kwargs
        )

    @classmethod
    def getMetadata(
        cls,
        database_handler: Database_Handler,
        join_table: str,
        parameters: Tuple[Any, ...]
    ) -> List["YouTube"]:
        """
        Retrieving metadata records for a given media identifier by joining the media table with a provided platform/value table.

        Args:
            database_handler (Database_Handler): The database handler instance to run the query.
            join_table (str): The name of the table to join for additional metadata.
            parameters (Tuple[Any, ...]): Parameters for the SQL WHERE clause (e.g., identifier tuple).

        Returns:
            List[YouTube]: A list of YouTube instances containing the fetched metadata.
        """
        temporary_instance: "YouTube" = cls(database_handler)
        base_table: str = temporary_instance.getTableName()
        query: str = f"SELECT {base_table}.identifier AS identifier, {base_table}.author AS author, {join_table}.value AS platform FROM {base_table} LEFT JOIN {join_table} ON {base_table}.Media = {join_table}.identifier WHERE {base_table}.identifier = %s"
        database_response: List[RowType] = temporary_instance.getDatabaseHandler().getData(query, parameters)
        if not database_response:
            return []
        return [cls(database_handler, **row) for row in database_response] # type: ignore

    @classmethod
    def getByTitle(cls, database_handler: Database_Handler, title: str) -> List["YouTube"]:
        """
        Retrieving YouTube video records from the database based on a title.

        This method queries the YouTube table to find videos whose titles match the given pattern.  It returns a list of YouTube instances, each containing metadata such as identifier, duration, author, title, and a URL to the video.

        Args:
            database_handler (Database_Handler): The database handler instance for executing the query.
            title (str): The title pattern to search for in the database.

        Returns:
            List[YouTube]: A list of YouTube instances with metadata matching the given title pattern.
        """
        temporary_instance: "YouTube" = cls(database_handler)
        query: str = f"SELECT identifier, CONCAT(LPAD(FLOOR(length / 3600), 2, '0'), ':', LPAD(FLOOR(length / 60), 2, '0'), ':', LPAD(length % 60, 2, '0')) AS duration, author AS channel, title, CONCAT('https://www.youtube.com/watch?v=', identifier) AS uniform_resource_locator, Media AS media_identifier FROM {temporary_instance.getTableName()} WHERE title LIKE %s"
        parameters: Tuple[str] = (title,)
        response: List[RowType] = temporary_instance.getDatabaseHandler().getData(query, parameters)
        if not response:
            return []
        return [cls(database_handler, **row) for row in response] # type: ignore

    @classmethod
    def getByChannel(cls, database_handler: Database_Handler, channel: str) -> List["YouTube"]:
        """
        Retrieving YouTube video records from the database based on a channel name.

        This method queries the YouTube table to find videos whose authors match the given channel name.  It returns a list of YouTube instances, each containing metadata such as identifier, duration, author, title, and a URL to the video.

        Args:
            database_handler (Database_Handler): The database handler instance for executing the query.
            channel (str): The channel name to search for in the database.

        Returns:
            List[YouTube]: A list of YouTube instances with metadata matching the given channel name.
        """
        temporary_instance: "YouTube" = cls(database_handler)
        query: str = f"SELECT identifier, CONCAT(LPAD(FLOOR(length / 3600), 2, '0'), ':', LPAD(FLOOR(length / 60), 2, '0'), ':', LPAD(length % 60, 2, '0')) AS duration, author AS channel, title, CASE WHEN identifier LIKE 'shorts/%' THEN CONCAT('https://www.youtube.com/', identifier) ELSE CONCAT('https://www.youtube.com/watch?v=', identifier) END AS uniform_resource_locator, Media AS media_identifier FROM {temporary_instance.getTableName()} WHERE author = %s"
        parameters: Tuple[str] = (channel,)
        response: List[RowType] = temporary_instance.getDatabaseHandler().getData(query, parameters)
        if not response:
            return []
        return [cls(database_handler, **row) for row in response] # type: ignore

    @classmethod
    def getByIdentifier(cls, database_handler: Database_Handler, identifier: str) -> Optional["YouTube"]:
        """
        Retrieving a YouTube video record from the database by its identifier.

        This method queries the YouTube table to find a video with the given identifier.  It returns a YouTube instance, containing metadata such as author, title, and a URL to the video.

        Args:
            database_handler (Database_Handler): The database handler instance for executing the query.
            identifier (str): The unique identifier of the video to retrieve.

        Returns:
            Optional[YouTube]: A YouTube instance with metadata matching the given identifier, or None if no record is found.
        """
        temporary_instance: "YouTube" = cls(database_handler)
        query: str = f"SELECT author, title FROM {temporary_instance.getTableName()} WHERE identifier = %s LIMIT 1"
        parameters: Tuple[str] = (identifier,)
        response: List[RowType] = temporary_instance.getDatabaseHandler().getData(query, parameters)
        if not response:
            return None
        return [cls(database_handler, **row) for row in response][0] # type: ignore
