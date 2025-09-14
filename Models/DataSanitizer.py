"""
The module provides a class for sanitizing user input data to prevent SQL injection attacks and ensure safe string usage.

Author:
    Darkness4869
"""
from typing import List, Any, Optional
from re import match


class Data_Sanitizer:
    """
    A class to sanitize user input data to prevent SQL injection attacks and ensure safe string usage.

    Attributes:
        __structured_query_language_keywords (List[str]): A list of SQL keywords that should not be used in user input to prevent SQL injection attacks.
        __safe_string (str): A regex pattern that allows alphanumeric characters, spaces, and some special characters.

    Methods:
        sanitize(data: Any) -> Any: Sanitizes the input data by checking if it matches
    """
    __structured_query_language_keywords: List[str]
    """
    A list of SQL keywords that should not be used in user input to prevent SQL injection attacks.
    """
    __safe_string: str
    """
    A regex pattern that allows alphanumeric characters, spaces, and some special characters.
    """

    def __init__(
        self,
        structured_query_language_keywords: Optional[List[str]] = None,
        safe_string: str = r"^[a-zA-Z0-9\s\-$_.,:|;/\[\]?=<>#&!’%+\(\)\"']*$"
    ) -> None:
        """
        Initializing a `Data_Sanitizer` instance with optional SQL keywords and a regex pattern for safe strings.

        Args:
            structured_query_language_keywords (Optional[List[str]]): A list of SQL keywords to check against user input.
            safe_string (str): A regex pattern defining allowed characters in user input. Defaults to a pattern allowing alphanumeric characters, spaces, and some special characters.
        """
        self.setSqlKeywords(structured_query_language_keywords or ["ALTER", "DROP", "TRUNCATE", "RENAME", "INSERT", "UPDATE", "DELETE", "MERGE", "SELECT", "GRANT", "REVOKE", "COMMIT", "ROLLBACK", "SAVEPOINT", "RELEASE SAVEPOINT"])
        self.setSafeString(safe_string)

    def getSqlKeywords(self) -> List[str]:
        return self.__structured_query_language_keywords

    def setSqlKeywords(self, structured_query_language_keywords: List[str]) -> None:
        self.__structured_query_language_keywords = structured_query_language_keywords

    def getSafeString(self) -> str:
        return self.__safe_string

    def setSafeString(self, safe_string: str) -> None:
        self.__safe_string = safe_string

    def sanitize(self, data: Any) -> Any:
        """
        Sanitizing the input data by checking if it matches the allowed regex pattern and does not contain any restricted SQL keywords.

        Args:
            data (Any): The data to be sanitized.

        Returns:
            Any: The sanitized data.

        Raises:
            ValueError: If the data is invalid or contains restricted SQL keywords.
        """
        if data is None:
            return None
        if not isinstance(data, str):
            return data
        if not match(self.getSafeString(), data):
            raise ValueError(f"The provided data is invalid. - Data: {data}")
        unchecked_data: str = str(data).upper()
        if any(f" {keyword} " in f" {unchecked_data} " for keyword in self.getSqlKeywords()):
            raise ValueError(f"The provided data contains restricted SQL keywords. - Data: {unchecked_data}")
        return data
