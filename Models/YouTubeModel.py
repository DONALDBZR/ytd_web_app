from Models.TableModel import Table_Model, Database_Handler, RowType, List, Tuple, Any


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

