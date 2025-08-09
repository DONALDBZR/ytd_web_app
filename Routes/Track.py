"""
The module that has the routing for the analytics.
"""
from flask import Blueprint, Response, request
from Models.AnalyticalManagementSystem import AnalyticalManagementSystem, Dict, Union, Extractio_Logger, Database_Handler
from json import JSONDecodeError
from index import DatabaseHandler


Track_Portal: Blueprint = Blueprint("Track", __name__)
"""
The Routing for all the analytics.

Type: Blueprint
"""
Logger: Extractio_Logger = Extractio_Logger(__name__)
"""
The logger that will all the action of the application.
"""
database_handler: Database_Handler = DatabaseHandler
"""
A class to handle database operations such as connecting, executing queries, and managing transactions.
"""

def closeDatabase():
    """
    Closing the database connection.

    This function is called when the application is being torn down, such as when the server is being shut down.  It closes the database connection and cursor to ensure that resources are released properly.
    """
    if database_handler.getCursor() is not None:
        database_handler.closeCursor()
    if database_handler.getConnection() is not None and database_handler.getConnection().is_connected():
        database_handler.closeConnection()

@Track_Portal.route('/', methods=['POST'])
def postEvent() -> Response:
    """
    This endpoint is used to track any event that happens on the application.  Any incoming request to this endpoint will be processed and the event will be saved in the database.  The event name and timestamp are required for the event to be saved.  The event name should be one of the following: `page_view`, `search_submitted`, `color_scheme_updated`, or `click`.

    The endpoint will return a JSON response with the HTTP status code indicating the result of the operation.  If the request is successful, the HTTP status code will be `201` and the response will be an empty JSON object.  If the request is not valid, the HTTP status code will be `400` and the response will contain the error message.

    Parameters:
        data (Dict[str, Union[str, float]]): The request data as a JSON object.

    Returns:
        Response: A JSON response with the result of the operation.
    """
    mime_type: str = "application/json"
    try:
        data: Dict[str, Union[str, float]] = request.get_json()
        isEmpty(data)
        data["ip_address"] = request.environ.get('REMOTE_ADDR', request.remote_addr)
        system: AnalyticalManagementSystem = AnalyticalManagementSystem(database_handler)
        status: int = system.processEvent(data)
        closeDatabase()
        Logger.inform(f"The event has been stored in the database. - Status: {status}")
        return Response(
            response=None,
            status=status,
            mimetype=mime_type
        )
    except (JSONDecodeError, ValueError) as error:
        closeDatabase()
        Logger.error(f"The payload in the request data is invalid. - Error: {error}")
        return Response(
            response=None,
            status=400,
            mimetype=mime_type
        )

def isEmpty(data: Union[Dict[str, Union[str, float]], None]) -> None:
    """
    Checking if the provided data is empty and logs an error if so.

    This function:
    - Verifies whether `data` is `None`.
    - If `data` is `None`, logs an error and raises a `ValueError`.
    - Otherwise, the function simply returns without performing any action.

    Parameters:
        data (Union[Dict[str, Union[str, float]], None]): The data to be checked. It can be either a dictionary containing string/float values or `None`.

    Raises:
        ValueError: If `data` is `None`, an error is logged, and an exception is raised.
    """
    if data is not None:
        return
    Logger.error("The payload in the request data is empty.")
    raise ValueError("The payload in the request data is empty.")
