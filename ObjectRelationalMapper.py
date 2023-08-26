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
