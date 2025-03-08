from flask import Blueprint, Response, request, session
from Models.SessionManagementSystem import Session_Manager, Extractio_Logger, Dict, Union
from json import JSONDecodeError, dumps
from jsonschema import validate
from typing import Any
from jsonschema.exceptions import ValidationError


Session_Portal: Blueprint = Blueprint("Session", __name__)
"""
The Routing for all the Sessions.
"""
Logger: Extractio_Logger = Extractio_Logger(__name__)
"""
The logger that will all the action of the application.
"""
session_payload_schema: Dict[str, Any] = {
    "type": "object",
    "properties": {
        "Client": {
            "type": "object",
            "properties": {
                "color_scheme": {
                    "type": "string",
                    "enum": ["light", "dark"]
                }
            },
            "required": ["color_scheme"]
        }
    },
    "required": ["Client"]
}

@Session_Portal.route('/', methods=['GET'])
def getSession() -> Response:
    """
    Retrieving session data for the client.

    This function gathers information about the client's request, including IP addresses and port number.  It then initializes a `Session_Manager` instance to retrieve session-related data such as timestamp and color scheme.  If the session is successfully retrieved, the function returns a JSON response containing the session data.  Otherwise, it handles exceptions and returns a 503 Service Unavailable response.

    Returns:
        Response

    Raises:
        Exception: If an unexpected error occurs during session retrieval.
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
    Updating the session data for the client.

    This function receives a JSON payload, validates it, and updates the session data using `Session_Manager`.  If the payload is invalid, it returns a 400 Bad Request response.  If the session update is successful, it returns the updated session data with a 202 Accepted status.  If an unexpected error occurs, it returns a 503 Service Unavailable response.

    Returns:
        Response: A Flask response object containing updated session data in JSON format, or an error message if the request fails.
    
    Raises:
        ValueError: If the payload is empty or invalid.
        Exception: If an unexpected error occurs during session update.
    """
    mime_type: str = "application/json"
    status: int = 202
    try:
        payload: Dict[str, Dict[str, str]] = request.json # type: ignore
        isPayloadEmpty(payload)
        validate(
            instance=payload,
            schema=session_payload_schema
        )
        user_request: Dict[str, str] = {
            "ip_address": str(request.environ.get('REMOTE_ADDR')),
            "http_client_ip_address": str(request.environ.get("HTTP_CLIENT_IP")),
            "proxy_ip_address": str(request.environ.get("HTTP_X_FORWARDED_FOR")),
            "port": str(request.environ.get("SERVER_PORT"))
        }
        SessionManager: Session_Manager = Session_Manager(user_request, session)
        SessionManager.updateSession(payload)
        session_data: Dict[str, Dict[str, Union[int, str]]] = {
            "Client": {
                "timestamp": int(SessionManager.getSession()["Client"]["timestamp"]),
                "color_scheme": str(SessionManager.getSession()["Client"]["color_scheme"])
            }
        }
        response: str = dumps(
            obj=session_data,
            indent=4
        )
        return Response(
            response=response,
            status=status,
            mimetype=mime_type
        )
    except ValidationError as error:
        Logger.error(f"An invalid JSON has been received as payload.\nError: {error}")
        return Response(
            response=dumps(
                obj={
                    "error": "Invalid JSON Structure"
                },
                indent=4
            ),
            status=400,
            mimetype=mime_type
        )
    except JSONDecodeError as error:
        Logger.error(f"An invalid JSON has been received as payload.\nError: {error}")
        return Response(
            response=dumps(
                obj={
                    "error": str(error)
                },
                indent=4
            ),
            status=400,
            mimetype=mime_type
        )
    except Exception as error:
        Logger.error(f"An unexpected error has occured.\nError: {error}")
        return Response(
            response=dumps(
                obj={
                    "error": "Service Unavailable"
                },
                indent=4
            ),
            status=503,
            mimetype=mime_type
        )

def isPayloadEmpty(payload: Dict[str, Dict[str, str]]) -> None:
    """
    Checking if the provided payload is empty.

    This function verifies whether the given payload dictionary contains data.  If the payload is empty, it logs an error message and raises a `ValueError`.

    Parameters:
        payload (Dict[str, Dict[str, str]]): The JSON payload to be checked.
    
    Raises:
        ValueError: If the payload is empty or invalid.
    """
    if payload:
        return
    Logger.error("An invalid JSON has been received as payload.")
    raise ValueError("Invalid JSON")
