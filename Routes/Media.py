from flask import Blueprint, Response, request
from Models.Media import Media
from io import TextIOWrapper
from typing import Dict, Union, List
import json
import os

Media_Portal = Blueprint("Media", __name__)
"""
The Routing for all the Media.

Type: Blueprint
"""


def getDirectory() -> str:
    """
    Retrieving the directory of the application which depends on
    the server that is used.

    Returns:
        string
    """
    if request.environ.get("SERVER_PORT") == '80' or request.environ.get("SERVER_PORT") == '443' or request.environ.get("SERVER_PORT") == '591':
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


@Media_Portal.route("/Search", methods=["GET"])
def search() -> Response:
    """
    Searching for the media by the uniform resource locator that
    has been retrieved from the client.

    Returns:
        Response
    """
    platform: str = str(request.args.get("platform"))
    search: str = str(request.args.get("search"))
    user_request: Dict[str, Union[None, str]] = {
        "referer": None,
        "search": search,
        "platform": platform,
        "ip_address": str(request.environ.get("REMOTE_ADDR")),
        "port": str(request.environ.get("SERVER_PORT"))
    }
    mime_type: str = "application/json"
    media: Media = Media(user_request)
    response: Dict[
        str,
        Union[
            int,
            Dict[
                str, Union[str, int, Dict[str, Union[str, int, None]], None]
            ]
        ]
    ] = media.verifyPlatform()
    status: int = int(response["data"]["status"])  # type: ignore
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
    system_request: dict[str, str | None] = {
        "referer": None,
        "search": "",
        "platform": "",
        "ip_address": "127.0.0.1",
        "port": str(request.environ.get("SERVER_PORT"))
    }
    media = Media(system_request)
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
    response: dict[str, int | dict[str, str | int | None]] | str
    # Ensuring that the payload is from the search page
    if "Search" in request.referrer:
        media = Media(user_request)  # type: ignore
        response = media.verifyPlatform()  # type: ignore
    mime_type = "application/json"
    status = int(response["data"]["status"])  # type: ignore
    response = json.dumps(response, indent=4)  # type: ignore
    return Response(response, status, mimetype=mime_type)

@Media_Portal.route('/RelatedContents/<string:identifier>', methods=["GET"])
def getRelatedContents(identifier: str) -> Response:
    """
    Retrieving the related contents of the media content that
    has been downloaded from the application.

    Parameters:
        identifier: string: The identifier of the content

    Returns:
        Response
    """
    mime_type: str = "application/json"
    system_request: Dict[str, Union[str, None]] = {
        "referer": None,
        "search": "",
        "platform": "",
        "ip_address": "127.0.0.1",
        "port": str(request.environ.get("SERVER_PORT"))
    }
    media: Media = Media(system_request)
    model_response: Dict[str, Union[int, List[Dict[str, str]]]] = media.getRelatedContents(identifier)
    status: int = int(model_response["status"]) # type: ignore
    response = json.dumps(model_response["data"], indent=4)  # type: ignore
    return Response(response, status, mimetype=mime_type) # type: ignore