"""
The Endpoint for the Media Management System.

Authors:
    Darkness4869
"""

from flask import Blueprint, Response, request
from Models.Media import Media
from typing import Dict, Union, List
from json import dumps, loads, JSONDecodeError
from os.path import isfile
from Environment import Environment


Media_Portal: Blueprint = Blueprint("Media", __name__)
"""
The Routing for all the Media.
"""

def readFile(file_name: str) -> Union[str, None]:
    """
    Reading the file needed.

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

def loadData(contents: Union[str, None]) -> Union[Dict, List, None]:
    """
    Loading the data from the contents.

    Parameters:
        contents:  string|null: Contents to be loaded.

    Returns:
        object|array|null
    """
    if contents is None:
        return None
    try:
        return loads(contents)
    except JSONDecodeError:
        return None

def getMetaData(file_name: str) -> Dict[str, Union[int, Dict[str, Union[str, int, None]]]]:
    """
    Retrieving the metadata.

    Parameters:
        file_name:  string: Name of the file.

    Returns:
        {status: int, data: {Media: {YouTube: {uniform_resource_locator: string, author: string, title: string, identifier: string, author_channel: string, views: number, published_at: string, thumbnail: string, duration: string, audio: string, video: string}}}}
    """
    data: Dict[str, Union[str, int, None]]
    if isfile(file_name):
        file_data: Dict[str, Dict[str, Dict[str, Union[str, int, None]]]] = loadData(readFile(file_name)) # type: ignore
        status: int = 200 if file_data is not None else 503
        data = file_data["Media"]["YouTube"] if status == 200 else {}
        return {
            "status": status,
            "data": data
        }
    ENV: Environment = Environment()
    ENV.__setDirectory(int(str(request.environ.get("SERVER_PORT"))))
    identifier: str = file_name.replace(f"{ENV.getDirectory()}/Cache/Media/", "").replace(".json", "")
    user_request: Dict[str, Union[None, str]] = {
        "referer": None,
        "search": f"https://www.youtube.com/watch?v={identifier}",
        "platform": "youtube",
        "ip_address": str(request.environ.get("REMOTE_ADDR")),
        "port": str(request.environ.get("SERVER_PORT"))
    }
    media: Media = Media(user_request)
    return media.verifyPlatform()

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
    mime_type: str = "application/json"
    user_request: Dict[str, Union[None, str]] = {
        "referer": None,
        "search": search,
        "platform": platform,
        "ip_address": str(request.environ.get("REMOTE_ADDR")),
        "port": str(request.environ.get("SERVER_PORT"))
    }
    media: Media = Media(user_request)
    response: Dict[str, Union[int, Dict[str, Union[str, int, None]]]] = media.verifyPlatform()
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
    ENV: Environment = Environment()
    ENV.__setDirectory(int(str(request.environ.get("SERVER_PORT"))))
    mime_type: str = "application/json"
    file_name: str = f"{ENV.getDirectory()}/Cache/Media/{identifier}.json"
    response: Dict[str, Union[int, Dict[str, Union[str, int, None]]]] = getMetaData(file_name)
    return Response(dumps(response["data"], indent=4), int(str(response["status"])), mimetype=mime_type)

@Media_Portal.route('/Download', methods=['POST'])
def retrieveMedia() -> Response:
    """
    Retrieving the media needed from the uniform resource
    locator and stores it in the server while allowing the user
    to download it.

    Returns:
        Response
    """
    mime_type: str = "application/json"
    if "Search" not in request.referrer:
        return Response(dumps({}, indent=4), 403, mimetype=mime_type)
    payload: Dict[str, Dict[str, str]] = request.json  # type: ignore
    data: Dict[str, str] = payload["Media"]
    user_request: Dict[str, str] = {
        "referer": request.referrer,
        "search": data["uniform_resource_locator"],
        "platform": data["platform"],
        "ip_address": str(request.environ.get("REMOTE_ADDR")),
        "port": str(request.environ.get("SERVER_PORT"))
    }
    media: Media = Media(user_request) # type: ignore
    model_response: Dict[str, Union[int, Dict[str, Union[str, int, None]]]] = media.verifyPlatform()
    return Response(dumps(model_response["data"], indent=4), int(str(model_response["status"])), mimetype=mime_type)

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
    return Response(dumps(model_response["data"], indent=4), int(str(model_response["status"])), mimetype=mime_type)