import json
import os
from flask import Blueprint, Response, request
from Media import Media
from io import TextIOWrapper

Media_Portal = Blueprint("Media", __name__)
"""
The Routing for all the Media.

Type: Blueprint
"""


def getDirectory() -> str:
    """
    Retrieving the directory of the application which depends on
    the server that is used.

    Returns: string
    """
    # Verifying that the port is for either Apache HTTPD or Werkzeug
    if request.environ.get("SERVER_PORT") == '80':
        return "/var/www/html/ytd_web_app"
    else:
        return "/home/darkness4869/Documents/extractio"


def getMetaData(file_name: str) -> TextIOWrapper:
    """
    Retrieving the metadata.

    Parameters:
        file_name:  string: Name of the file.

    Returns: TextIOWrapper
    """
    if os.path.isfile(file_name):
        return open(file_name)
    else:
        directory = getDirectory()
        identifier = file_name.replace(
            f"{directory}/Cache/Media/", "").replace(".json", "")
        user_request = {
            "referer": None,
            "search": f"https://www.youtube.com/watch?v={identifier}",
            "platform": "youtube",
            "ip_address": str(request.environ.get("REMOTE_ADDR")),
            "port": str(request.environ.get("SERVER_PORT"))
        }
        media = Media(user_request)
        response = json.dumps(media.verifyPlatform(), indent=4)
        return open(file_name)


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
        "port": str(request.environ.get("SERVER_PORT"))  # type: ignore
    }
    media = Media(user_request)
    response = media.verifyPlatform()
    status = int(response["data"]["status"])  # type: ignore
    mime_type = "application/json"
    return Response(json.dumps(response, indent=4), status, mimetype=mime_type)


@Media_Portal.route('/<string:identifier>', methods=["GET"])
def getMedia(identifier: str) -> Response:
    """
    Sending the data for the media that has been searched in the
    form of JSON.

    Parameters:
        identifier: string: Identifier of the content.

    Returns: Response
    """
    directory = getDirectory()
    file_name = f"{directory}/Cache/Media/{identifier}.json"
    file = getMetaData(file_name)
    response = file.read()
    mime_type = "application/json"
    status = 200
    return Response(response, status, mimetype=mime_type)


@Media_Portal.route('/Download', methods=['POST'])
def retrieveMedia() -> Response:
    """
    Retrieving the media needed from the uniform resource
    locator and stores it in the server while allowing the user
    to download it.

    Returns: string
    """
    payload = request.json
    data = payload["Media"]  # type: ignore
    user_request = {
        "referer": request.referrer,
        "search": str(data["uniform_resource_locator"]),  # type: ignore
        "platform": str(data["platform"]),  # type: ignore
        "ip_address": str(request.environ.get("REMOTE_ADDR")),
        "port": str(request.environ.get("SERVER_PORT"))  # type: ignore
    }
    response = {}
    # Ensuring that the payload is from the search page
    if "Search" in request.referrer:
        media = Media(user_request)
        response = media.verifyPlatform()
    mime_type = "application/json"
    status = response["data"]["status"]
    response = json.dumps(response, indent=4)
    return Response(response, status, mimetype=mime_type)
