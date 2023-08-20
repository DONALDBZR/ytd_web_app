from DatabaseHandler import Database_Handler


class Object_Relational_Mapper(Database_Handler):
    """
    It is the relational mapper that will be used to simplify the process to entering queries.
    """

    def __init__(self):
        """
        Connecting the database as well as initializing the ORM.
        """
        super().__init__()

    def get_table_records(self) -> list:
        """
        Retrieving data from the database.  (SELECT)

        Returns:
            array: The list of data retrieved.
        """
        query = "SELECT * FROM table JOIN table1 ON table.id = table1.id WHERE a = b ORDER BY a ASC"
        super().query(query, parameters)
        super().execute()
        return super().resultSet()
