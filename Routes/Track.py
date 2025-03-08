"""
The module that has the routing for the analytics.
"""
from flask import Blueprint, Response, request
from Models.AnalyticalManagementSystem import AnalyticalManagementSystem, Dict, Union, Extractio_Logger, List
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
        if data is None:
            Logger.error("The payload in the request data is empty.")
            return Response(
                response=None,
                status=400,
                mimetype=mime_type
            )
        data["ip_address"] = request.environ.get('REMOTE_ADDR', request.remote_addr)
        system: AnalyticalManagementSystem = AnalyticalManagementSystem()
        status: int = system.processEvent(data)
        return Response(
            response=None,
            status=status,
            mimetype=mime_type
        )
    except JSONDecodeError as error:
        Logger.error(f"The payload in the request data is invalid.\nError: {error}")
        return Response(
            response=None,
            status=400,
            mimetype=mime_type
        )
