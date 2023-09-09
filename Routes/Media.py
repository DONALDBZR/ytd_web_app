import json
from flask import Blueprint, Response, request
from Media import Media

Media_Portal = Blueprint("Media", __name__)
"""
The Routing for all the Media.

Type: Blueprint
"""


@Media_Portal.route("/Search", methods=["POST"])
def search() -> Response:
    """
    Searching for the media by the uniform resouce locator that
    has been retrieved from the client.

    Returns: Response
    """
    payload = request.json
    user_request = {
        "referer": None,
        "search": str(payload["Media"]["search"]),  # type: ignore
        "platform": str(payload["Media"]["platform"]),  # type: ignore
        "ip_address": str(request.environ.get("REMOTE_ADDR")),
        "port": int(request.environ.get("SERVER_PORT"))  # type: ignore
    }
    media = Media(user_request)
    response = json.dumps(media.verifyPlatform(), indent=4)
    status = int(media.verifyPlatform()["data"]["status"])
    mime_type = "application/json"
    return Response(response, status, mimetype=mime_type)
