"""
The module that has the routing for the analytics.
"""
from flask import Blueprint, Response, request
from typing import Dict


Track_Portal = Blueprint("Track", __name__)
"""
The Routing for all the analytics.

Type: Blueprint
"""

@Track_Portal.route('/', methods=['POST'])
def postEvent():
    """
    Processing the event and sending it to the relational
    database server.

    Returns:
        Response
    """
    mime_type: str = "application/json"
    status: int = 503
    response: Dict[str, str] = {
        "message": "Service Unavailable"
    }
    return Response(response, status, mimetype=mime_type)
