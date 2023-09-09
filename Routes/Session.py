import json
from flask import Blueprint, Response, request, session
from SessionManagementSystem import Session_Manager

Session_Portal = Blueprint("Session", __name__)
"""
The Routing for all the Sessions.

Type: Blueprint
"""


@Session_Portal.route('/Session', methods=['GET'])
def getSession() -> Response:
    """
    Sending the session data in the form of JSON.

    Returns: Response
    """
    user_request = {
        "ip_address": str(request.environ.get('REMOTE_ADDR')),
        "http_client_ip_address": str(request.environ.get("HTTP_CLIENT_IP")),
        "proxy_ip_address": str(request.environ.get("HTTP_X_FORWARDED_FOR")),
        "port": int(request.environ.get("SERVER_PORT"))  # type: ignore
    }
    SessionManager = Session_Manager(user_request, session)
    session_data = {
        "Client": {
            "timestamp": SessionManager.getSession()["Client"]["timestamp"],
            "color_scheme": SessionManager.getSession()["Client"]["color_scheme"]
        }
    }
    response = json.dumps(session_data, indent=4)
    mime_type = "application/json"
    status = 200
    return Response(response, status, mimetype=mime_type)
