"""
The module that has the routing for the analytics.
"""
from flask import Blueprint, Response, request
from typing import Dict
from Models.AnalyticalManagementSystem import AnalyticalManagementSystem


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
    data: Dict[str, str] = request.get_json()
    data["ip_address"] = request.environ.get('REMOTE_ADDR', request.remote_addr)
    system: AnalyticalManagementSystem = AnalyticalManagementSystem()
    status: int = system.processEvent(data)
    return Response(None, status, mimetype=mime_type)
