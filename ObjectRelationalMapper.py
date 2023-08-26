from DatabaseHandler import Database_Handler


class Object_Relational_Mapper(Database_Handler):
    """
    It is the object relational mapper that will be used to
    simplify the process to entering queries.
    """

    def __init__(self):
        """
        Connecting the database as well as initializing the ORM.
        """
        super().__init__()
        self.setParameters(None)

    def _get_filter(self, condition: str, parameters: tuple | None) -> None:
        """
        Building the query needed for retrieving specific data.

        Parameters:
            condition:  string:     The WHERE statement that will be used.
            parameters: array|null: Parameters to be used to filter the data.

        Returns: void
        """
        if condition == "":
            query = self.getQuery()
            self.setParameters(None)
        else:
            query = f"{self.getQuery()} WHERE {condition}"
            self.setParameters(parameters)
        self.setQuery(query)

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

    def post_data(self, table: str, columns: str, values: str, parameters: tuple) -> None:
        """
        Creating records to store data into the database server.

        Parameters:
            table:      string: Table Name
            columns:    string: Column names
            values:     string: Data to be inserted

        Returns: void
        """
        query = f"INSERT INTO {table}({columns}) VALUES ({values})"
        self.setQuery(query)
        self.setParameters(parameters)
        self.query(self.getQuery(), self.getParameters())
        self.execute()

    def update_data(self, table: str, values: str, parameters: tuple | None, condition: str = "") -> None:
        """
        Updating a specific table in the database.

        Parameters:
            table:      string: Table
            values:     string: Columns to be modified and data to be put within
            condition:  string: Condition for the data to be modified
            parameters: array:  Data to be used for data manipulation.

        Returns: void
        """
        query = f"UPDATE {table} SET {values}"
        self.setQuery(query)
        self._get_filter(condition, parameters)
        self.query(self.getQuery(), self.getParameters())
        self.execute()

    def delete_records(self, table: str, parameters: tuple | None, condition: str = "") -> None:
        """
        Deleting data from the database.

        Parameters:
            table:      string: Table
            parameters: array:  Data to be used for data manipulation.
            condition:  string: Specification

        Returns: void
        """
        query = f"DELETE FROM {table}"
        self.setQuery(query)
        self._get_filter(condition, parameters)
        self.query(self.getQuery(), self.getParameters())
        self.execute()

    def _get_limit(self, condition: str) -> None:
        """
        Building the query needed to be used to limit the amount of
        data from the result set.

        Parameters:
            condition:  string: The ORDER BY statement that will be used.

        Returns: void
        """
        if condition == "":
            query = self.getQuery()
        else:
            query = f"{self.getQuery()} LIMIT {condition}"
        self.setQuery(query)
