"""
The module provides a base class for database table models, allowing interaction with the database through methods for CRUD operations.

Author:
    Darkness4869
"""
from Models.DatabaseHandler import Database_Handler, List, RowType, Tuple, Any, Optional
from typing import Dict, Type


class Table_Model:
    """
    A base class for database table models, providing methods to interact with the database.

    Attributes:
        __table_name (str): The name of the table.
        __database_handler (Database_Handler): The database handler instance to interact with the database.
        __fields (List[str]): A list of fields in the table.
        __mysql_field_types (Dict[str, type]): A dictionary mapping field names to their MySQL types.
        __field_types (Dict[str, str]): A dictionary mapping field names to their types, used for validation and sanitization.
        __primary_field (str): The field that is the primary key of the table.

    Methods:
        _getFields() -> Tuple[List[str], Dict[str, str]]: Fetches the column names and types for the table from the database.
        setModelAttributes(kwargs: Dict[str, Any]) -> None: Sets the model attributes based on the provided keyword arguments.
        mySqlTypeToPython(mysql_type: str) -> type: Converts a MySQL type to its corresponding Python type.
        getById(database_handler: Database_Handler, primary_key: Any) -> Optional["TableModel"]: Retrieves a model instance by its primary key.
        getAll(database_handler: Database_Handler) -> List["TableModel"]: Retrieves all model instances from the table.
        save() -> bool: Saves the model instance to the database.
        update() -> bool: Updates the model instance in the database.
        delete() -> bool: Deletes the model instance from the database.
        createModelClass(table_name: str, database_handler: Database_Handler) -> Type["TableModel"]: Dynamically creates a model class for a given table name.
        getLastRowIdentifier(database_handler: Database_Handler) -> int: Retrieves the last inserted row identifier from the database.
    """
    __table_name: str
    """
    The name of the table.
    """
    __database_handler: Database_Handler
    """
    The database handler instance to interact with the database.
    """
    __fields: List[str]
    """
    A list of fields in the table.
    """
    __mysql_field_types: Dict[str, type]
    """
    A dictionary mapping field names to their MySQL types.
    """
    __field_types: Dict[str, str]
    """
    A dictionary mapping field names to their types, used for validation and sanitization.
    """
    __primary_field: str
    """
    The field that is the primary key of the table.
    """

    def __init__(
        self,
        database_handler: Database_Handler,
        table_name: str = "",
        **kwargs
    ):
        """
        Initializing the TableModel with a database handler and optional table name and fields.

        Args:
            database_handler (Database_Handler): The database handler instance to interact with the database.
            table_name (str, optional): The name of the table. If not provided, it will be set later.
            **kwargs: Optional keyword arguments for table name and fields.
        """
        self.setDatabaseHandler(database_handler)
        self.setTableName(table_name)
        if self.getTableName():
            model_class: Type["Table_Model"] = self.createModelClass(self.getTableName(), self.getDatabaseHandler())
            self.__class__ = model_class # type: ignore
        fields, field_types, primary_field = self._getFields()
        self.setFields(fields)
        self.setFieldTypes(field_types)
        self.setPrimaryField(primary_field)
        self.setMySqlFieldTypes({
            "int": int,
            "bigint": int,
            "smallint": int,
            "tinyint": int,
            "mediumint": int,
            "float": float,
            "double": float,
            "decimal": float,
            "char": str,
            "varchar": str,
            "text": str,
            "mediumtext": str,
            "longtext": str,
            "date": str,
            "datetime": str,
            "timestamp": str,
            "time": str,
            "enum": str,
            "set": str,
            "blob": bytes,
            "binary": bytes,
            "varbinary": bytes
        })
        self.setModelAttributes(kwargs)

    def getTableName(self) -> str:
        return self.__table_name

    def setTableName(self, table_name: str) -> None:
        self.__table_name = table_name

    def getDatabaseHandler(self) -> Database_Handler:
        return self.__database_handler

    def setDatabaseHandler(self, database_handler: Database_Handler) -> None:
        self.__database_handler = database_handler

    def getFields(self) -> List[str]:
        return self.__fields

    def setFields(self, fields: List[str]) -> None:
        self.__fields = fields

    def getFieldTypes(self) -> Dict[str, str]:
        return self.__field_types

    def setFieldTypes(self, field_types: Dict[str, str]) -> None:
        self.__field_types = field_types

    def getMySqlFieldTypes(self) -> Dict[str, type]:
        return self.__mysql_field_types

    def setMySqlFieldTypes(self, mysql_field_types: Dict[str, type]) -> None:
        self.__mysql_field_types = mysql_field_types

    def getPrimaryField(self) -> str:
        return self.__primary_field

    def setPrimaryField(self, primary_field: str) -> None:
        self.__primary_field = primary_field

    def _getFields(self) -> Tuple[List[str], Dict[str, str], str]:
        """
        Fetching the column names and types for the table from the database.

        Returns:
            Tuple[List[str], Dict[str, str], str]: A tuple containing a list of field names and a dictionary mapping field names to their MySQL types.
        """
        database_response: List[RowType] = self.getDatabaseHandler().getData(f"SHOW COLUMNS FROM {self.getTableName()}")
        fields: List[str] = [str(column["Field"]) for column in database_response] # type: ignore
        field_types: Dict[str, str] = {str(column["Field"]): str(column["Type"]) for column in database_response} # type: ignore
        primary_field: str = next((str(column["Field"]) for column in database_response if str(column["Key"]) == "PRI"), "identifier") # type: ignore
        return fields, field_types, primary_field

    def setModelAttributes(self, kwargs: Dict[str, Any]) -> None:
        """
        Setting the model attributes based on the provided keyword arguments.

        Args:
            kwargs (Dict[str, Any]): Keyword arguments containing the attributes to set.
        """
        for field in self.getFields():
            setattr(self, field, kwargs.get(field))

    def mySqlTypeToPython(self, mysql_type: str) -> type:
        print(f"{mysql_type=}")
        base: str = mysql_type.split("(")[0].lower()
        print(f"{base=}")
        return self.getMySqlFieldTypes().get(base, type)

    @classmethod
    def getById(cls, database_handler: Database_Handler, primary_key: Any) -> Optional["Table_Model"]:
        """
        Retrieving a model instance by its primary key.

        Args:
            database_handler (Database_Handler): The database handler instance to interact with the database.
            primary_key (Any): The primary key value to search for.

        Returns:
            Optional[TableModel]: The model instance if found, otherwise None.
        """
        query: str = f"SELECT * FROM {cls.__table_name} WHERE {cls.__primary_field} = %s"
        response: List[RowType] = database_handler.getData(query, (primary_key,))
        if not response:
            return None
        return cls(database_handler, **response[0]) # type: ignore
    
    @classmethod
    def getAll(cls, database_handler: Database_Handler) -> List["Table_Model"]:
        """
        Retrieving all model instances from the table.

        Args:
            database_handler (Database_Handler): The database handler instance to interact with the database.

        Returns:
            List[Table_Model]: A list of model instances.
        """
        temporary_instance: "Table_Model" = cls(database_handler)
        query: str = f"SELECT * FROM {temporary_instance.getPrimaryField()}"
        response: List[RowType] = database_handler.getData(query)
        return [cls(database_handler, **row) for row in response] # type: ignore

    def save(self) -> bool:
        """
        Saving the model instance to the database.

        Returns:
            bool: True if the save operation was successful, otherwise False.
        """
        fields: List[str] = [field for field in self.getFields() if field != self.getPrimaryField()]
        values: Tuple[Any, ...] = tuple(getattr(self, field) for field in fields)
        placeholders: str = ", ".join(["%s"] * len(fields))
        query: str = f"INSERT INTO {self.getTableName()} ({', '.join(fields)}) VALUES ({placeholders})"
        return self.getDatabaseHandler().postData(query, values)

    def update(self) -> bool:
        """
        Updating the model instance in the database.

        Returns:
            bool: True if the update operation was successful, otherwise False.
        """
        fields: List[str] = [field for field in self.getFields() if field != self.getPrimaryField()]
        values: Tuple[Any, ...] = tuple(getattr(self, field) for field in fields)
        set_clause: str = ", ".join([f"{field} = %s" for field in fields])
        query: str = f"UPDATE {self.getTableName()} SET {set_clause} WHERE {self.getPrimaryField()} = %s"
        return self.getDatabaseHandler().updateData(query, values + (getattr(self, self.getPrimaryField()),))

    def delete(self) -> bool:
        """
        Deleting the model instance from the database.

        Returns:
            bool: True if the delete operation was successful, otherwise False.
        """
        query: str = f"DELETE FROM {self.getTableName()} WHERE {self.getPrimaryField()} = %s"
        return self.getDatabaseHandler().deleteData(query, (getattr(self, self.getPrimaryField()),))

    @classmethod
    def createModelClass(cls, table_name: str, database_handler: Database_Handler) -> Type["Table_Model"]:
        """
        Dynamically creating a model class for interacting with a database table.

        This method constructs a new class with attributes and methods specific to the given table name.  It retrieves the columns from the specified table and maps their types to Python types.  The resulting class can be used to instantiate objects that represent rows in the table.

        Args:
            table_name (str): The name of the table for which to create the model class.
            database_handler (Database_Handler): The database handler instance to interact with the database.

        Returns:
            Type[Table_Model]: A dynamically created subclass of `Table_Model` representing the specified table.
        """
        temporary_instance: "Table_Model" = cls(database_handler, table_name)
        columns: List[RowType] = temporary_instance.getDatabaseHandler().getData(f"SHOW COLUMNS FROM {temporary_instance.getTableName()}")
        annotations: Dict[str, type] = {}
        primary_field: str = next((str(column["Field"]) for column in columns if str(column["Key"]) == "PRI"), "identifier") # type: ignore
        for column in columns:
            class_type: type = temporary_instance.mySqlTypeToPython(str(column["Type"])) # type: ignore
            annotations[str(column["Field"])] = class_type # type: ignore

        def __init__(self, **kwargs):
            """
            Initializing a `TableModel` instance with a database handler, table name, fields, field types, primary key, and keyword arguments.

            Parameters:
                **kwargs: Additional keyword arguments to set the model's fields.

            Attributes:
                __database_handler (Database_Handler): The database handler instance to interact with the database.
                __table_name (str): The name of the table.
                __fields (List[str]): The names of the fields in the table.
                __field_types (Dict[str, type]): A mapping of field names to their corresponding types.
                __primary_key (str): The name of the primary key field.
            """
            self.__database_handler = database_handler
            self.__table_name = table_name
            self.__fields = list(annotations.keys())
            self.__field_types = annotations
            self.__primary_key = primary_field
            for field in self.__fields:
                setattr(self, field, kwargs.get(field))

        attributes: Dict[str, Any] = {
            "__table_name": table_name,
            "__database_handler": database_handler,
            "__fields": list(annotations.keys()),
            "__field_types": annotations,
            "__primary_field": primary_field,
            "__init__": __init__,
            "__annotations__": annotations
        }
        return type(table_name.capitalize(), (cls,), attributes)

    @classmethod
    def getLastRowIdentifier(cls, database_handler: Database_Handler) -> int:
        """
        Retrieving the last inserted row identifier from the database.

        Parameters:
            database_handler (Database_Handler): The database handler used to execute the query.

        Returns:
            int: The last inserted identifier if available, or 0 if the query fails or no ID is present.
        """
        query: str = "SELECT LAST_INSERT_ID() AS last_identifier"
        response: List[RowType] = database_handler.getData(query)
        if not response or "last_identifier" not in response[0]:
            database_handler.getLogger().warn("Could not retrieve last inserted identifier.")
            return 0
        last_identifier: Any = response[0]["last_identifier"] # type: ignore
        if not isinstance(last_identifier, int):
            database_handler.getLogger().warn(f"The identifier is invalid. - Type: {type(last_identifier)}")
            return 0
        return last_identifier
