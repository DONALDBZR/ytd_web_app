"""
The Endpoint for the Media Management System.

Authors:
    Darkness4869
"""
from flask import Blueprint, Response, request
from Models.Media import Media, Extractio_Logger, Environment, Dict, Union, List, dumps
from json import loads
from os.path import join, realpath
from html import escape
from index import limiter
from re import fullmatch
from typing import Any


Media_Portal: Blueprint = Blueprint("Media", __name__)
"""
The Routing for all the Media.
"""
Routing_Logger: Extractio_Logger = Extractio_Logger(__name__)
"""
The logger that will all the action of the application.
"""
ENV: Environment = Environment()
"""
ENV File of the application.
"""
def getMetaData(file_name: str) -> Dict[str, Union[int, Dict[str, Union[str, int, None]]]]:
    """
    Retrieving metadata from a JSON file while ensuring security measures.

    This function checks the validity of the file name, prevents path traversal, and attempts to read metadata from the specified JSON file.  If the file is missing, it attempts to fetch data using the `Media` class.

    Parameters:
        file_name (string): The name of the metadata file (expected to be a JSON file).

    Returns:
        Dict[string, Union[int, Dict[string, Union[string, int, None]]]]
    """
    allowed_directory: str = f"{ENV.getDirectory()}/Cache/Media/shorts" if "shorts/" in file_name else f"{ENV.getDirectory()}/Cache/Media"
    file_name = file_name.replace("shorts/", "") if "shorts/" in file_name else file_name
    identifier: str = r"^[a-zA-Z0-9\-_]+$"
    file_name = escape(file_name)
    if not fullmatch(identifier, file_name.replace(".json", "").replace(f"{allowed_directory}/", "")):
        Routing_Logger.error(f"The file name is invalid.\nFile Name: {file_name}")
        return {
            "status": 400,
            "data": {}
        }
    file_name = join(allowed_directory, file_name)
    file_path: str = realpath(file_name)
    if not file_path.startswith(realpath(allowed_directory)):
        Routing_Logger.error(f"Path traversal has been detected.\nFile Name: {file_name}")
        return {
            "status": 403,
            "data": {}
        }
    try:
        file = open(file_name, "r")
        contents: str = file.read().strip()
        file_data: Dict[str, Dict[str, Dict[str, Union[str, int, None]]]] = loads(contents)
        status: int = 200
        data = sanitizeStringData(file_data["Media"]["YouTube"])
        return {
            "status": status,
            "data": data
        }
    except FileNotFoundError as error:
        Routing_Logger.error(f"The file is not found.\nFile Name: {file_name}\nError: {error}")
        identifier: str = file_name.replace(f"{ENV.getDirectory()}/Cache/Media/", "").replace(".json", "")
        user_request: Dict[str, Union[str, None]] = {
            "referer": None,
            "search": f"https://www.youtube.com/watch?v={identifier}",
            "platform": "youtube",
            "ip_address": str(request.environ.get("REMOTE_ADDR")),
            "port": str(request.environ.get("SERVER_PORT"))
        }
        media: Media = Media(user_request)
        model_response: Dict[str, Union[int, Dict[str, Union[str, int, None]]]] = media.verifyPlatform()
        return {
            "status": int(str(model_response["status"])),
            "data": model_response["data"]
        }
    except Exception as error:
        Routing_Logger.error(f"The metadata cannot be retrieved.\nFile Name: {file_name}\nError: {error}")
        return {
            "status": 503,
            "data": {}
        }

def sanitizeStringData(data: Dict[str, Any]):
    """
    Sanitizing string values in a dictionary by escaping HTML characters.

    This function iterates through the dictionary and applies HTML escaping to any string values, preventing potential HTML or JavaScript injection.

    Parameters:
        data (Dict[str, Any]): A dictionary containing key-value pairs, where some values may be strings.

    Returns:
        Dict[str, Any]
    """
    for key, value in data.items():
        data[key] = escape(value) if isinstance(value, str) else value
    return data

@Media_Portal.route("/Search", methods=["GET"])
@limiter.limit("100 per day", error_message="Rate Limit Exceeded")
def search() -> Response:
    """
    Handling GET requests to the /Search endpoint for retrieving media metadata.

    This endpoint validates the incoming query parameters and constructs a media search request.  If validation passes, it delegates to the media verification system and returns a structured JSON response.

    Route:
        - GET /Search

    Query Parameters:
        - platform (str): The name of the platform to search on.
        - type (str): The type of media to search for.
        - identifier (str): The identifier of the media.

    Response Codes:
        - 200: Successful response with search results.
        - 400: Bad request due to missing or invalid parameters.
        - 429: Rate limit exceeded.

    Returns:
        Response
    """
    platform: str = escape(str(request.args.get("platform")))
    type: str = escape(str(request.args.get("type")))
    identifier: str = escape(str(request.args.get("identifier")))
    mime_type: str = "application/json"
    if not platform or not type or not identifier:
        Routing_Logger.error("The parameters are missing.")
        return Response(
            response=dumps(
                obj={
                    "error": "The parameters are missing."
                },
                indent=4
            ),
            status=400,
            mimetype=mime_type
        )
    if len(identifier) > 16:
        Routing_Logger.error("The identifier is too long.")
        return Response(
            response=dumps(
                obj={
                    "error": "The identifier is too long."
                },
                indent=4
            ),
            status=400,
            mimetype=mime_type
        )
    if type not in ENV.getAllowedYoutubeContents():
        Routing_Logger.error(f"The type is invalid.\nType: {type}")
        return Response(
            response=dumps(
                obj={
                    "error": "The type is invalid."
                },
                indent=4
            ),
            status=400,
            mimetype=mime_type
        )
    search: str = f"{ENV.getYouTubeVideoUniformResourceLocator()}{identifier}" if type == "Video" else f"{ENV.getYouTubeShortsUniformResourceLocator()}{identifier}"
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
    Routing_Logger.inform(f"The response has been sent.\nStatus: {status}\nData: {response['data']}")
    return Response(
        response=dumps(
            obj=response,
            indent=4
        ),
        status=status,
        mimetype=mime_type
    )

@Media_Portal.route('/<string:identifier>', methods=["GET"])
@limiter.limit("100 per day", error_message="Rate Limit Exceeded")
def getMedia(identifier: str) -> Response:
    """
    Retrieving media metadata based on a unique identifier.

    This function processes a GET request to fetch metadata for a specific media entry.  It verifies the identifier format, ensuring it contains only alphanumeric characters, dashes, or underscores. If valid, it retrieves metadata from a JSON file.

    Routes:
        - GET /

    Parameters:
        identifier (string): A unique media identifier consisting of letters, numbers, dashes, or underscores.

    Response Codes:
        - 200: Successful response with media metadata.
        - 400: Bad request due to invalid identifier format.
        - 404: Not found if the media metadata is not found.
        - 429: Rate limit exceeded.

    Returns:
        Response
    """
    mime_type: str = "application/json"
    identifier_regex: str = r"^[a-zA-Z0-9\-_]+$"
    if not fullmatch(identifier_regex, identifier):
        Routing_Logger.error(f"The identifier is invalid.\nIdentifier: {identifier}")
        data: Dict[str, str] = {
            "error": "The identifier is invalid."
        }
        return Response(
            response=dumps(
                obj=data,
                indent=4
            ),
            status=400,
            mimetype=mime_type
        )
    file_name: str = f"{identifier}.json"
    response: Dict[str, Union[int, Dict[str, Union[str, int, None]]]] = getMetaData(file_name)
    return Response(
        response=dumps(
            obj=response["data"],
            indent=4
        ),
        status=int(str(response["status"])),
        mimetype=mime_type
    )

@Media_Portal.route('/Download', methods=['POST'])
@limiter.limit("20 per 7 days", error_message="Rate Limit Exceeded")
def retrieveMedia() -> Response:
    """
    Handling media retrieval requests.

    This function processes a POST request to download media.  It expects a JSON payload containing media information, verifies the request parameters, and checks if the specified platform is supported.

    Routes:
        - POST /Download

    Response Codes:
        - 201: Successful response with file downloaded on the server.
        - 400: Bad request due to missing or invalid parameters.
        - 503: Service unavailable due to platform verification failure.
        - 429: Rate limit exceeded.

    Returns:
        Response
    """
    mime_type: str = "application/json"
    payload: Dict[str, Dict[str, str]] = request.json  # type: ignore
    data: Dict[str, str] = payload["Media"]
    if data.get("uniform_resource_locator") is None or data.get("platform") is None:
        Routing_Logger.error(f"The parameters are invalid.\nData: {data}")
        data: Dict[str, str] = {
            "error": "The parameters are invalid."
        }
        return Response(
            response=dumps(
                obj=data,
                indent=4
            ),
            status=400,
            mimetype=mime_type
        )
    uniform_resource_locator: str = escape(data["uniform_resource_locator"])
    platform: str = escape(data["platform"])
    user_request: Dict[str, str] = {
        "referer": request.referrer,
        "search": uniform_resource_locator,
        "platform": platform,
        "ip_address": str(request.environ.get("REMOTE_ADDR")),
        "port": str(request.environ.get("SERVER_PORT"))
    }
    media: Media = Media(user_request) # type: ignore
    model_response: Dict[str, Union[int, Dict[str, Union[str, int, None]]]] = media.verifyPlatform()
    status: int = 201 if int(str(model_response["status"])) >= 200 and int(str(model_response["status"])) <= 299 else 503
    return Response(
        response=dumps(
            obj=model_response["data"],
            indent=4
        ),
        status=status,
        mimetype=mime_type
    )

@Media_Portal.route('/RelatedContents/<string:identifier>', methods=["GET"])
@limiter.limit("100 per day", error_message="Rate Limit Exceeded")
def getRelatedContents(identifier: str) -> Response:
    """
    Retrieving the related contents of the media content that has been downloaded from the application.

    Parameters:
        identifier (string): The identifier of the content

    Returns:
        Response
    """
    mime_type: str = "application/json"
    identifier_regex: str = r"^[a-zA-Z0-9\-_]+$"
    if not fullmatch(identifier_regex, identifier):
        Routing_Logger.error(f"The format for the identifier is invalid identifier.\nIdentifier: {identifier}\nStatus: 400")
        data: Dict[str, str] = {
            "error": "The format for the identifier is invalid."
        }
        return Response(
            response=dumps(
                obj=data,
                indent=4
            ),
            status=400,
            mimetype=mime_type
        )
    system_request: Dict[str, Union[str, None]] = {
        "referer": None,
        "search": "",
        "platform": "",
        "ip_address": "127.0.0.1",
        "port": str(request.environ.get("SERVER_PORT"))
    }
    media: Media = Media(system_request)
    model_response: Dict[str, Union[int, List[Dict[str, str]]]] = media.getRelatedContents(identifier)
    return Response(
        response=dumps(
            obj=model_response["data"],
            indent=4
        ),
        status=int(str(model_response["status"])),
        mimetype=mime_type
    )

@Media_Portal.after_request
def securityHeaders(response: Response) -> Response:
    """
    Adds security-related HTTP headers to the response to
    enhance security.  This function sets various security
    headers to mitigate risks such as  clickjacking, MIME-type
    sniffing, and improper content embedding.

    Parameters:
        response (Response): The Flask response object.

    Returns:
        Response
    """
    content_security_policy: str = "; ".join([
        "default-src 'none'",
        "connect-src 'self'",
        "frame-src 'none'",
        "object-src 'none'",
        "base-uri 'none'",
        "form-action 'none'"
    ])
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    response.headers["Content-Security-Policy"] = content_security_policy
    return response

@Media_Portal.errorhandler(429)
def rateLimited(error: Exception) -> Response:
    """
    Handles HTTP 429 Too Many Requests errors for the `Media_Portal` Blueprint.

    This function is triggered when a client exceeds the request rate limit.  It returns a JSON response containing the error message.

    Parameters:
        error (Exception): The exception object representing the 429 error.

    Returns:
        Response
    """
    data: Dict[str, str] = {
        "error": str(error)
    }
    return Response(
        response=dumps(
            obj=data,
            indent=4
        ),
        status=429
    )

@Media_Portal.route('/Shorts/<string:identifier>', methods=["GET"])
@limiter.limit("100 per day", error_message="Rate Limit Exceeded")
def getMediaShorts(identifier: str) -> Response:
    """
    Retrieving metadata for a specific media short by identifier.

    This endpoint handles a GET request to fetch metadata associated with a media short.  It validates the identifier format and returns metadata from a corresponding JSON file if found.

    URL Pattern:
        GET /Shorts/<identifier>

    Parameters:
        identifier (str): A unique identifier for the media short.  Must consist of alphanumeric characters, dashes (`-`), or underscores (`_`).

    Returns:
        Response

    Response Status Codes:
        200 OK: Metadata retrieved successfully.
        400 Bad Request: Invalid identifier format.
        404 Not Found: Metadata file not found.
        429 Too Many Requests: Rate limit exceeded.

    Rate Limiting:
        Maximum 100 requests per day per IP address.
    """
    mime_type: str = "application/json"
    identifier_regex: str = r"^[a-zA-Z0-9\-_]+$"
    if not fullmatch(identifier_regex, identifier):
        Routing_Logger.error(f"The identifier is invalid.\nIdentifier: {identifier}")
        data: Dict[str, str] = {
            "error": "The identifier is invalid."
        }
        return Response(
            response=dumps(
                obj=data,
                indent=4
            ),
            status=400,
            mimetype=mime_type
        )
    file_name: str = f"shorts/{identifier}.json"
    response: Dict[str, Union[int, Dict[str, Union[str, int, None]]]] = getMetaData(file_name)
    return Response(
        response=dumps(
            obj=response["data"],
            indent=4
        ),
        status=int(str(response["status"])),
        mimetype=mime_type
    )

@Media_Portal.route('/RelatedContents/Shorts/<string:identifier>', methods=["GET"])
@limiter.limit("100 per day", error_message="Rate Limit Exceeded")
def getRelatedContentsShorts(identifier: str) -> Response:
    """
    Retrieving related media contents for a specific short video.

    This endpoint handles a GET request to return related content based on a given media identifier.  It validates the identifier format and uses the `Media` model to fetch related items.

    URL Pattern:
        GET /RelatedContents/Shorts/<identifier>

    Parameters:
        identifier (str): A unique media identifier consisting of alphanumeric characters, dashes (`-`), or underscores (`_`).

    Response Status Codes:
        200 OK: Related contents retrieved successfully.
        400 Bad Request: Invalid identifier format.
        404 Not Found: No related contents found.
        429 Too Many Requests: Rate limit exceeded.

    Rate Limiting:
        Maximum 100 requests per day per IP address.

    Returns:
        Response
    """
    mime_type: str = "application/json"
    identifier_regex: str = r"^[a-zA-Z0-9\-_]+$"
    if not fullmatch(identifier_regex, identifier):
        Routing_Logger.error(f"The format for the identifier is invalid identifier.\nIdentifier: {identifier}\nStatus: 400")
        data: Dict[str, str] = {
            "error": "The format for the identifier is invalid."
        }
        return Response(
            response=dumps(
                obj=data,
                indent=4
            ),
            status=400,
            mimetype=mime_type
        )
    system_request: Dict[str, Union[str, None]] = {
        "referer": None,
        "search": "",
        "platform": "",
        "ip_address": "127.0.0.1",
        "port": str(request.environ.get("SERVER_PORT"))
    }
    media: Media = Media(system_request)
    identifier = f"shorts/{identifier}"
    model_response: Dict[str, Union[int, List[Dict[str, str]]]] = media.getRelatedContents(identifier)
    return Response(
        response=dumps(
            obj=model_response["data"],
            indent=4
        ),
        status=int(str(model_response["status"])),
        mimetype=mime_type
    )
