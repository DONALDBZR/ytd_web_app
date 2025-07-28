from Models.TableModel import Table_Model, Database_Handler, RowType, List


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
        query: str = f"SELECT YouTube FROM {temporary_instance.getTableName()} WHERE date_downloaded >= NOW() - INTERVAL 2 WEEK"
        database_response: List[RowType] = temporary_instance.getDatabaseHandler().getData(query)
        if not database_response:
            return []
        return [cls(database_handler, **row) for row in database_response] # type: ignore

