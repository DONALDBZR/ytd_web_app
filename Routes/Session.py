from flask import Blueprint, Response, request, session
from Models.SessionManagementSystem import Session_Manager
from typing import Dict, Union
from json import dumps


Session_Portal: Blueprint = Blueprint("Session", __name__)
"""
The Routing for all the Sessions.

Type: Blueprint
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
    response: str = dumps(session_data, indent=4)
    return Response(response, status, mimetype=mime_type)


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
        "port": str(request.environ.get("SERVER_PORT"))  # type: ignore
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
