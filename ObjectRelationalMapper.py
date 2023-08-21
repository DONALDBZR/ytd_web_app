from DatabaseHandler import Database_Handler


class Object_Relational_Mapper(Database_Handler):
    """
    It is the relational mapper that will be used to simplify the process to entering queries.
    """
    __query: str
    """
    The query to be used to be sent to the database server to either get, post, update or delete data.

    Type: string
    Visibility: private
    """

    def __init__(self):
        """
        Connecting the database as well as initializing the ORM.
        """
        super().__init__()

    def get_query(self) -> str:
        return self.__query

    def set_query(self, query: str) -> None:
        self.__query = query

    def get_table_records(self, parameters: dict | None, table_name: str, column_names: str = "*", join_condition: str = "", is_joined: bool = False, filtered: bool = False, filter_condition: str = "", is_sorted: bool = False, sort_condition: str) -> list:
        """
        Retrieving data from the database.  (SELECT)

        Parameters:
            parameters:         object|null:    The parameters to be passed into the query.
            table_name:         string:         The name of the table.
            column_names:       string:         The name of the columns.
            join_condition      string:         Joining table condition.
            is_joined           boolean:        The condition to run a JOIN query
            filtered            boolean:        The condition to filter the result set.
            filter_condition    string:         Items to be filtered with.
            is_sorted           boolean:        The condition to sort the result set.
            sort_condition      string:         The items to be sorted.

        Returns:
            array: The list of data retrieved.
        """
        query = f"SELECT {column_names} FROM {table_name}{is_joined}{join_condition}{filtered}{filter_condition}{is_sorted}{sort_condition}"
        super().query(query, parameters)
        super().execute()
        return super().resultSet()
