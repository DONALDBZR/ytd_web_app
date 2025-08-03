"""
The module that has the data model for the `Session`.
"""
from Models.TableModel import Table_Model, Database_Handler, RowType, List


class Session(Table_Model):
    """
    The model that is used as model to interact with the database for the Session Table.

    Methods:
        deleteOtherThanToday() -> bool: Deleting all session records created before the current day.
        getTodaySession(database_handler: Database_Handler) -> Session: Retrieving the earliest session record for the current day.
    """
    def __init__(
        self,
        database_handler: Database_Handler,
        **kwargs
    ):
        """
        Initializing a new Session model instance.

        This constructor passes the database handler and any additional keyword arguments to the parent `Table_Model`, specifically setting the table name to "Session".

        Args:
            database_handler (Database_Handler): The database handler instance to interact with the database.
            **kwargs: Arbitrary keyword arguments that are passed to the parent constructor.  These typically include the model's field values.
        """
        super().__init__(
            database_handler,
            table_name="Session",
            **kwargs
        )

    def deleteOtherThanToday(self) -> bool:
        """
        Deleting all session records created before the current day.

        This method constructs and executes a SQL query to remove all entries from the 'Session' table where the 'date_created' field is earlier than the current date.  This is useful for cleaning up old, expired session records.

        Returns:
            bool: True if the deletion was successful, False otherwise.
        """
        query: str = f"DELETE FROM {self.getTableName()} WHERE date_created < CURDATE()"
        return self.getDatabaseHandler().deleteData(query)

    @classmethod
    def getTodaySession(cls, database_handler: Database_Handler) -> "Session":
        """
        Retrieving the earliest session record for the current day.

        This class method queries the database to find the first session entry created on the current date, ordering by the primary identifier to ensure consistency.  It is useful for retrieving the active session for the day.

        Args:
            database_handler (Database_Handler): The database handler instance used to execute the query.

        Returns:
            Session: An instance of the `Session` class populated with the data for today's session.
        """
        temporary_instance: "Session" = cls(database_handler)
        query: str = f"SELECT * FROM {temporary_instance.getTableName()} WHERE date_created = CURDATE() ORDER BY identifier ASC LIMIT 1"
        database_response: List[RowType] = temporary_instance.getDatabaseHandler().getData(query)
        if not database_response:
            return cls(
                temporary_instance.getDatabaseHandler(),
                table_name=temporary_instance.getTableName()
            )
        return [cls(temporary_instance.getDatabaseHandler(), **row) for row in database_response][0] # type: ignore

    def create(self) -> bool:
        """
        Creating the Session table if it does not already exist.

        This method creates the Session table according to the defined structure.  It is useful for setting up the database schema.

        Returns:
            bool: True if the table creation was successful, False otherwise.
        """
        query: str = f"CREATE TABLE IF NOT EXISTS `{self.getTableName()}` (identifier INT PRIMARY KEY AUTO_INCREMENT, hash VARCHAR(256) NOT NULL, date_created VARCHAR(16), CONSTRAINT unique_constraint_session UNIQUE (hash))"
        return self.getDatabaseHandler().createTable(query, None)
