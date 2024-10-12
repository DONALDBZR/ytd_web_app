"""
The Endpoint for the Media Management System.
"""

from flask import Blueprint, Response, request
from Models.Media import Media
from typing import Dict, Union, List
from json import dumps, loads
from os.path import isfile
import json
import os


Media_Portal: Blueprint = Blueprint("Media", __name__)
"""
The Routing for all the Media.
"""

def loadFile(file_name: str) -> Union[str, None]:
    """
    Loading the file needed.

    Parameters:
        file_name:  string: Name of the file.

    Returns:
        string|null
    """
    try:
        file = open(file_name, "r")
        return file.read().strip()
    except FileNotFoundError:
        return None


def getMetaData(file_name: str) -> Union[Dict[str, Dict[str, Dict[str, Union[str, int]]]], Dict[str, Union[str, int, None]], Dict[str, Union[str, int]]]:
    """
    Retrieving the metadata.

    Parameters:
        file_name:  string: Name of the file.

    Returns:
        {Media: {YouTube: {uniform_resource_locator: string, author: string, title: string, identifier: string, author_channel: string, views: number, published_at: string, thumbnail: string, duration: string, audio: string, video: string}}}
    """
    if isfile(file_name):
        content: str = loadFile(file_name)
        return loads(content)
    else:
        directory: str = "/var/www/html/ytd_web_app" if request.environ.get("SERVER_PORT") == '80' or request.environ.get("SERVER_PORT") == '443' or request.environ.get("SERVER_PORT") == '591' else "/home/darkness4869/Documents/extractio"
        identifier: str = file_name.replace(f"{directory}/Cache/Media/", "").replace(".json", "")
        user_request: Dict[str, Union[None, str]] = {
            "referer": None,
            "search": f"https://www.youtube.com/watch?v={identifier}",
            "platform": "youtube",
            "ip_address": str(request.environ.get("REMOTE_ADDR")),
            "port": str(request.environ.get("SERVER_PORT"))
        }
        media: Media = Media(user_request)
        model_response: Dict[str, int | Dict[str, str | int | None] | Dict[str, str | int]] = media.verifyPlatform()
        return model_response["data"] # type: ignore


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
    response: Dict[str, Union[int, Dict[str, Union[str, int, None]], Dict[str, Union[str, int]]]] = media.verifyPlatform()
    status: int = int(response["status"])  # type: ignore
    return Response(dumps(response, indent=4), status, mimetype=mime_type)


@Media_Portal.route('/<string:identifier>', methods=["GET"])
def getMedia(identifier: str) -> Response:
    """
    Sending the data for the media that has been searched in the
    form of JSON.

    Parameters:
        identifier: string: Identifier of the content.

    Returns:
        Response
    """
    directory: str = "/var/www/html/ytd_web_app" if request.environ.get("SERVER_PORT") == '80' or request.environ.get("SERVER_PORT") == '443' or request.environ.get("SERVER_PORT") == '591' else "/home/darkness4869/Documents/extractio"
    file_name: str = f"{directory}/Cache/Media/{identifier}.json"
    response: Union[Dict[str, Dict[str, Dict[str, Union[str, int]]]], Dict[str, Union[str, int, None]], Dict[str, Union[str, int]]] = getMetaData(file_name)
    mime_type: str = "application/json"
    status: int = 200
    return Response(dumps(response, indent=4), status, mimetype=mime_type)


@Media_Portal.route('/Download', methods=['POST'])
def retrieveMedia() -> Response:
    """
    Retrieving the media needed from the uniform resource
    locator and stores it in the server while allowing the user
    to download it.

    Returns:
        Response
    """
    response: Union[Dict[str, Union[int, Dict[str, Union[str, int, None]]]], str]
    payload: Dict[str, Dict[str, str]] = request.json  # type: ignore
    data: Dict[str, str] = payload["Media"]
    status: int
    mime_type: str = "application/json"
    user_request: Dict[str, str] = {
        "referer": request.referrer,
        "search": data["uniform_resource_locator"],
        "platform": data["platform"],
        "ip_address": str(request.environ.get("REMOTE_ADDR")),
        "port": str(request.environ.get("SERVER_PORT"))
    }
    if "Search" in request.referrer:
        media: Media = Media(user_request) # type: ignore
        model_response: Dict[str, Union[int, Dict[str, Union[str, int, None]], Dict[str, Union[str, int]]]] = media.verifyPlatform()
        status = int(model_response["data"]["status"])  # type: ignore
        response = dumps(model_response["data"]["data"], indent=4) # type: ignore
    else:
        status = 403
        response = dumps({}, indent=4)
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
    status: int = int(model_response["status"])  # type: ignore
    response = json.dumps(model_response["data"], indent=4)  # type: ignore
    return Response(response, status, mimetype=mime_type)  # type: ignore
