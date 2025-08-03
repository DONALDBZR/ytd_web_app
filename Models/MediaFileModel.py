from Models.TableModel import Table_Model, Database_Handler, RowType, List, Tuple


class Media_File(Table_Model):
    def __init__(
        self,
        database_handler: Database_Handler,
        **kwargs
    ):
        """
        Initializing a new Media File model instance.

        This constructor passes the database handler and any additional keyword arguments to the parent `Table_Model`, specifically setting the table name to "MediaFile".

        Args:
            database_handler (Database_Handler): The database handler instance to interact with the database.
            **kwargs: Arbitrary keyword arguments that are passed to the parent constructor.  These typically include the model's field values.
        """
        super().__init__(
            database_handler,
            table_name="MediaFile",
            **kwargs
        )

    @classmethod
    def getRecentFiles(cls, database_handler: Database_Handler) -> List["Media_File"]:
        """
        Retrieving media file entries downloaded within the last 2 weeks.

        Args:
            database_handler (Database_Handler): The database handler instance used to run the query.

        Returns:
            List[Media_File]: A list of Media_File objects matching the time filter.
        """
        temporary_instance: "Media_File" = cls(database_handler)
        query: str = f"SELECT YouTube FROM {temporary_instance.getTableName()} WHERE date_downloaded >= NOW() - INTERVAL 2 WEEK GROUP BY YouTube"
        database_response: List[RowType] = temporary_instance.getDatabaseHandler().getData(query)
        if not database_response:
            return []
        return [cls(database_handler, **row) for row in database_response] # type: ignore

    @classmethod
    def deleteByYouTube(cls, database_handler: Database_Handler, identifier: str) -> bool:
        """
        Deleting a media file record by its YouTube identifier.

        Args:
            database_handler (Database_Handler): The database handler instance used to delete the record.
            identifier (str): The YouTube identifier to search for in the database.

        Returns:
            bool: True if the deletion was successful, False otherwise.
        """
        temporary_instance: "Media_File" = cls(database_handler)
        query: str = f"DELETE FROM {temporary_instance.getTableName()} WHERE YouTube = %s"
        parameters: Tuple[str] = (identifier,)
        return temporary_instance.getDatabaseHandler().deleteData(query, parameters)

    def create(self) -> bool:
        """
        Creating the MediaFile table in the database if it does not already exist.

        This method constructs and executes a SQL query to create the `MediaFile` table with columns for identifier, type, downloaded date, deleted date, location, and a foreign key reference to the `YouTube` table.

        Returns:
            bool: True if the table was created or already exists, False otherwise.
        """
        query: str = f"CREATE TABLE IF NOT EXISTS `{self.getTableName()}` (identifier INT PRIMARY KEY AUTO_INCREMENT, `type` VARCHAR(64), date_downloaded VARCHAR(32), date_deleted VARCHAR(32) NULL, location VARCHAR(128), `YouTube` VARCHAR(16), CONSTRAINT fk_source FOREIGN KEY (`YouTube`) REFERENCES `YouTube` (identifier))"
        return self.getDatabaseHandler().createTable(query)
