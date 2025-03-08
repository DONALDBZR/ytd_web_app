from flask import Blueprint, Response, request, session
from Models.SessionManagementSystem import Session_Manager, Extractio_Logger, Dict, Union
from json import dumps


Session_Portal: Blueprint = Blueprint("Session", __name__)
"""
The Routing for all the Sessions.
"""
Logger: Extractio_Logger = Extractio_Logger(__name__)
"""
The logger that will all the action of the application.
"""


@Session_Portal.route('/', methods=['GET'])
def getSession() -> Response:
    """
    Sending the session data in the form of JSON.

    Returns:
        Response
    """
    mime_type: str = "application/json"
    status: int = 200
    try:
        user_request: Dict[str, str] = {
            "ip_address": str(request.environ.get('REMOTE_ADDR')),
            "http_client_ip_address": str(request.environ.get("HTTP_CLIENT_IP")),
            "proxy_ip_address": str(request.environ.get("HTTP_X_FORWARDED_FOR")),
            "port": str(request.environ.get("SERVER_PORT"))
        }
        SessionManager: Session_Manager = Session_Manager(user_request, session)
        session_data: Dict[str, Dict[str, Union[int, str]]] = {
            "Client": {
                "timestamp": int(SessionManager.getSession()["Client"]["timestamp"]),
                "color_scheme": str(SessionManager.getSession()["Client"]["color_scheme"])
            }
        }
        Logger.inform(f"The session data has been retrieved.\nStatus: {status}")
        return Response(
            response=dumps(
                obj=session_data,
                indent=4
            ),
            status=status,
            mimetype=mime_type
        )
    except Exception as error:
        Logger.error(f"An unexpected error has occurred and the service is currently unavailable.\nError: {error}")
        data: Dict[str, str] = {
            "error": "Service Unavailble"
        }
        return Response(
            response=dumps(
                obj=data,
                indent=4
            ),
            status=503,
            mimetype=mime_type
        )

@Session_Portal.route('/', methods=['PUT'])
def setSession() -> Response:
    """
    Allowing the Session Manager to update the session.

    Returns:
        Response
    """
    mime_type: str = "application/json"
    status: int = 202
    payload: Dict[str, Dict[str, str]] = request.json # type: ignore
    user_request: Dict[str, str] = {
        "ip_address": str(request.environ.get('REMOTE_ADDR')),
        "http_client_ip_address": str(request.environ.get("HTTP_CLIENT_IP")),
        "proxy_ip_address": str(request.environ.get("HTTP_X_FORWARDED_FOR")),
        "port": str(request.environ.get("SERVER_PORT"))
    }
    SessionManager: Session_Manager = Session_Manager(user_request, session)
    SessionManager.updateSession(payload)  # type: ignore
    session_data: Dict[str, Dict[str, Union[int, str]]] = {
        "Client": {
            "timestamp": int(SessionManager.getSession()["Client"]["timestamp"]),
            "color_scheme": str(SessionManager.getSession()["Client"]["color_scheme"])
        }
    }
    response: str = dumps(session_data, indent=4)
    return Response(response, status, mimetype=mime_type)
