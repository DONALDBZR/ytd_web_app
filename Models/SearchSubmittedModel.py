from Models.TableModel import Table_Model, Database_Handler, List, RowType, Tuple


class Search_Submitted(Table_Model):
    def __init__(
        self,
        database_handler: Database_Handler,
        **kwargs
    ):
        """
        Initializing a Search Submitted model instance with the specified database handler.

        Parameters:
            database_handler (Database_Handler): The handler for interacting with the database.
            **kwargs: Additional keyword arguments passed to the parent class.

        Inherits:
            Initializing the base model with the table name set to "Search_Submitted".
        """
        super().__init__(
            database_handler,
            table_name="SearchSubmitted",
            **kwargs
        )

    @classmethod
    def getBySearchTerm(cls, database_handler: Database_Handler, search_term: str) -> List["Search_Submitted"]:
        """
        Retrieving all rows from the `Search_Submitted` table that match the provided search term.

        Parameters:
            database_handler (Database_Handler): The database handler to execute queries.
            search_term (str): The search term to filter records by.

        Returns:
            List[Search_Submitted]: A list of matching Search_Submitted instances. Returns an empty list if no matches are found.
        """
        temporary_instance: "Search_Submitted" = cls(database_handler)
        query: str = f"SELECT * FROM {temporary_instance.getTableName()} WHERE search_term = %s"
        parameters: Tuple[str] = (search_term,)
        response: List[RowType] = temporary_instance.getDatabaseHandler().getData(query, parameters)
        if not response:
            return []
        return [cls(database_handler, **row) for row in response] # type: ignore
