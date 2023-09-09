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


@Media_Portal.route('/', methods=["GET"])
def getMedia() -> Response:
    """
    Sending the data for the media that has been searched in the
    form of JSON.

    Returns: Response
    """
    directory = ""
    # Verifying that the port is for either Apache HTTPD or Werkzeug
    if request.environ.get("SERVER_PORT") == 80:
        directory = "/var/www/html/ytd_web_app"
    else:
        directory = "/home/darkness4869/Documents/extractio"
    file_name = f"{directory}/Cache/Media/{request.environ.get('REMOTE_ADDR')}.json"
    file = open(file_name)
    response = file.read()
    mime_type = "application/json"
    status = 200
    return Response(response, status, mimetype=mime_type)
