"""
The module that has the routing for the analytics.
"""
from flask import Blueprint, Response, request
from Models.AnalyticalManagementSystem import AnalyticalManagementSystem, Dict, Union, Extractio_Logger
from json import JSONDecodeError


Track_Portal: Blueprint = Blueprint("Track", __name__)
"""
The Routing for all the analytics.

Type: Blueprint
"""
Logger: Extractio_Logger = Extractio_Logger(__name__)
"""
The logger that will all the action of the application.
"""

@Track_Portal.route('/', methods=['POST'])
def postEvent() -> Response:
    """
    Handling an incoming HTTP POST request to process an event.

    This function:
    - Extracts JSON data from the request body.
    - Logs an error and returns a `400 Bad Request` response if the payload is empty.
    - Adds the client's IP address to the extracted data.
    - Processes the event using an `AnalyticalManagementSystem` instance.
    - Returns an HTTP response with the appropriate status.

    Returns:
        Response

    Raises:
        JSONDecodeError: If the request data is not valid JSON.
    """
    mime_type: str = "application/json"
    try:
        data: Dict[str, Union[str, float]] = request.get_json()
        isEmpty(data)
        data["ip_address"] = request.environ.get('REMOTE_ADDR', request.remote_addr)
        system: AnalyticalManagementSystem = AnalyticalManagementSystem()
        status: int = system.processEvent(data)
        return Response(
            response=None,
            status=status,
            mimetype=mime_type
        )
    except (JSONDecodeError, ValueError) as error:
        Logger.error(f"The payload in the request data is invalid.\nError: {error}")
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
