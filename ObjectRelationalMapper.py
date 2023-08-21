from DatabaseHandler import Database_Handler


class Object_Relational_Mapper(Database_Handler):
    """
    It is the relational mapper that will be used to simplify
    the process to entering queries.
    """
    __query: str
    """
    The query to be used to be sent to the database server to
    either get, post, update or delete data.

    Type: string
    Visibility: private
    """
    __parameters: tuple | None
    """
    Parameters that the will be used to sanitize the query which
    is either  get, post, update or delete.

    Type: array|null
    Visibility: private
    """

    def __init__(self):
        """
        Connecting the database as well as initializing the ORM.
        """
        super().__init__()

    def getQuery(self) -> str:
        return self.__query

    def setQuery(self, query: str) -> None:
        self.__query = query

    def getParameters(self) -> tuple | None:
        return self.__parameters

    def setParameters(self, parameters: tuple | None) -> None:
        self.__parameters = parameters

    def get_table_records(self, parameters: list | None, table_name: str, join_condition: str = "", filter_condition: str = "", column_names: str = "*", sort_condition: str = "") -> list:
        """
        Retrieving data from the database.  (SELECT)

        Parameters:
            parameters:         array|null: The parameters to be passed into the query.
            table_name:         string:     The name of the table.
            column_names:       string:     The name of the columns.
            join_condition      string:     Joining table condition.
            filter_condition    string:     Items to be filtered with.
            sort_condition      string:     The items to be sorted.

        Returns: array
        """
        query = f"SELECT {column_names} FROM {table_name}"
        self.setQuery(query)
        self._get_join(join_condition)
        self._get_filter(filter_condition, parameters)
        self._get_sort(sort_condition)
        self.query(self.getQuery(), self.getParameters())
        self.execute()
        return self.resultSet()

    def _get_join(self, condition: str) -> None:
        """
        Building the query needed for retrieving data that is in at
        least two tables.

        Parameters:
            condition:  string: The JOIN statement that is used.

        Returns: void
        """
        if condition == "":
            query = self.getQuery()
        else:
            query = f"{self.getQuery()} JOIN {condition}"
        self.setQuery(query)

    def _get_filter(self, condition: str, parameters: list | None) -> None:
        """
        Building the query needed for retrieving specific data.

        Parameters:
            condition:  string:     The WHERE statement that will be used.
            parameters: array|null: Parameters to be used to filter the data.

        Returns: void
        """
        if condition == "":
            query = self.getQuery()
        else:
            query = f"{self.getQuery()} WHERE {condition}"
            self.__handle_parameters(parameters)
        self.setQuery(query)

    def __handle_parameters(self, parameters: list | None) -> None:
        """
        Building the array to be used as parameters to sanitize the
        query for more security.

        Parameters:
            parameters: array|null: The parameters to be used.

        Returns: void
        """
        if type(parameters) is list:
            self.setParameters(tuple(parameters))
        else:
            self.setParameters(None)

    def _get_sort(self, condition: str) -> None:
        """
        Building the query needed to be used to sort the result set.

        Parameters:
            condition:  string: The ORDER BY statement that will be used.

        Returns: void
        """
        if condition == "":
            query = self.getQuery()
        else:
            query = f"{self.getQuery()} ORDER BY {condition}"
        self.setQuery(query)
