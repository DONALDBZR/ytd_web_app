from collections import defaultdict, deque
from threading import Lock
from time import monotonic
from datetime import datetime
from typing import Deque, Optional, List
from Models.Streaming.ChannelManager import Channel
from urllib.parse import urlparse
from flask import Blueprint, Response, redirect, request, send_from_directory, url_for
from Models.Logger import Extractio_Logger
from Models.Streaming.ChannelManager import ChannelConfigurationError, Channel_Manager
from Models.Streaming.StreamManager import ResolutionBusy, Stream_Manager
from Models.Streaming.YouTubeLiveStream import StreamUnavailable, YouTubeLiveStream, Resolved_Stream
from Models.Streaming.RemuxManager import Remux_Manager, RemuxUnavailable
from os import environ, geteuid
from tempfile import gettempdir
from ipaddress import ip_network, ip_address
from json import dumps
from re import sub
from pathlib import Path
from Environment import Environment


Streaming_Portal: Blueprint = Blueprint("Streaming", __name__)
logger: Extractio_Logger = Extractio_Logger(__name__)
ENV: Environment = Environment()

def _integer_setting(
    name: str,
    default: int,
    minimum: int,
    maximum: int
) -> int:
    """
    Retrieving an integer setting from the environment variables, ensuring it falls within the specified range.

    Procedures:
        1. Retrieve the value of the environment variable with the given name.
        2. Convert the value to an integer.
        3. Ensure the value falls within the specified minimum and maximum range.
        4. Return the validated integer value.

    Parameters:
        name: str: The name of the environment variable.
        default: int: The default value to use if the environment variable is not set.
        minimum: int: The minimum allowed value.
        maximum: int: The maximum allowed value.

    Returns:
        int: The validated integer value.
    """
    try:
        value = int(environ.get(name, str(default)))
    except ValueError as error:
        message = "The value of the environment variable is invalid."
        logger.error(f"{message} - Name: {name} - Error: {error}")
        raise RuntimeError(message)
    if not minimum <= value <= maximum:
        message = "The value of the environment variable is outside of its allowed range."
        logger.error(f"{message} - Name: {name} - Value: {value}")
        raise RuntimeError(message)
    return value

try:
    file_path: str = f"{ENV.getDirectory()}/Cache/StreamingChannels.json"
    channel_configuration: Path = Path(file_path)
    channels: Channel_Manager = Channel_Manager.fromJson(channel_configuration.read_text(encoding="utf-8"))
    _timeout = _integer_setting(
        "STREAMING_RESOLUTION_TIMEOUT",
        15,
        1,
        60
    )
    _cache_ttl = _integer_setting(
        "STREAMING_CACHE_TTL",
        20,
        0,
        120
    )
    _max_sessions = _integer_setting(
        "STREAMING_MAX_CONCURRENT_SESSIONS",
        2,
        1,
        8
    )
    _networks = [ip_network(value.strip()) for value in environ.get("STREAMING_ALLOWED_NETWORKS", "127.0.0.0/8,::1/128").split(",") if value.strip()]
except (ChannelConfigurationError, ValueError, RuntimeError) as error:
    message = "The streaming configuration is invalid."
    logger.error(f"{message} - Error: {error}")
    raise RuntimeError(message)
manager: Stream_Manager = Stream_Manager(
    channels,
    YouTubeLiveStream(_timeout),
    _cache_ttl,
    _max_sessions
)
remux_manager: Remux_Manager = Remux_Manager(
    Path(gettempdir()) / f"extractio-streaming-remux-{geteuid()}",
    max_sessions=_max_sessions
)
_hits = defaultdict(deque)
_hits_lock = Lock()

def _network_allowed() -> bool:
    """
    Checking if the request's IP address is allowed based on the configured networks.

    Returns:
        bool: True if the network is allowed, False otherwise.
    """
    try:
        address = ip_address(request.remote_addr or "")
    except ValueError:
        logger.error(f"The IP address is invalid. - Address: {request.remote_addr or 'Not Applicable'}")
        return False
    return any(address in network for network in _networks)

def __checkIpAddress(key: str, now: float) -> bool:
    """
    Checking if the request's IP address has exceeded the rate limit.

    Procedures:
        1. Check if the key exists in the _hits dictionary and if the dictionary has reached its maximum size.
        2. Remove stale entries if necessary.
        3. Retrieve the hit history for the key.
        4. Remove hits that are older than 60 seconds.
        5. Check if the number of hits exceeds the limit.
        6. Append the current hit timestamp.
        7. Return True if the request is limited, False otherwise.

    Parameters:
        key (str): The IP address key for the request.
        now (float): The current timestamp.

    Returns:
        bool: True if the request is limited, False otherwise.
    """
    if key not in _hits and len(_hits) >= 1024:
        stale_key = next((address for address, history in _hits.items() if not history or history[-1] <= now - 60), None)
        if stale_key is None:
            return True
        del _hits[stale_key]
    hits: Deque[float] = _hits[key]
    while hits and hits[0] <= now - 60:
        hits.popleft()
    if len(hits) >= 30:
        return True
    hits.append(now)
    return False

def _limited() -> bool:
    """
    Checking if the request's IP address has exceeded the rate limit.

    Returns:
        bool: True if the request is limited, False otherwise.
    """
    now = monotonic()
    key = request.remote_addr or "unknown"
    with _hits_lock:
        return __checkIpAddress(key, now)

@Streaming_Portal.before_request
def authorize_streaming_request() -> Optional[Response]:
    """
    Authorizing streaming requests by checking network restrictions and rate limits.

    Procedures:
        1. Check if the request's IP address is allowed based on network restrictions.
        2. Check if the request has exceeded the rate limit.
        3. Return an appropriate response if the request is not authorized.

    Returns:
        Optional[Response]: The response if the request is not authorized, None otherwise.
    """
    if not _network_allowed():
        message = "Streaming is restricted to allowed networks."
        logger.error(message)
        return Response(
            status=403,
            response=dumps(
                obj={
                    "error": message
                },
                indent=4
            )
        )
    allowed_endpoints: List[str] = [
        "Streaming.health",
        "Streaming.remux_media",
    ]
    if request.endpoint not in allowed_endpoints and _limited():
        message = "The request for the streaming services has exceeded the rate limit."
        logger.error(message)
        return Response(
            status=429,
            response=dumps(
                obj={
                    "error": message
                },
                indent=4
            )
        )
    return None

@Streaming_Portal.route("/Health", methods=["GET"])
def health() -> Response:
    """
    Health check endpoint for the streaming service.

    Returns:
        Response: A JSON response indicating the health status of the service.
    """
    return Response(
        response=dumps(
            obj={
                "status": "ok",
                "application": "available",
                "youtube": "not_checked",
                "configured_channels": len(channels.list(enabled_only=True))
            },
            indent=4
        ),
        status=200,
        mimetype="application/json"
    )

@Streaming_Portal.route("/Channels", methods=["GET"])
def list_channels() -> Response:
    """
    Listing all available streaming channels.

    Returns:
        Response: A JSON response containing the list of channels and their details.
    """
    return Response(
        response=dumps(
            obj={
                "channels": [{
                    "slug": channel.slug,
                    "display_name": channel.display_name,
                    "url": channel.youtube_url,
                    "enabled": channel.enabled,
                    "playback_status": "not_checked",
                } for channel in channels.list()]
            },
            indent=4
        ),
        status=200,
        mimetype="application/json"
    )

@Streaming_Portal.route("/Channels/<string:slug>", methods=["GET"])
def channel_info(slug: str) -> Response:
    """
    Retrieving the information for a specific streaming channel.

    Procedures:
        1. Validate the channel slug format.
        2. Retrieve the channel information from the database.
        3. Return the channel details if found, otherwise return an error.

    Parameters:
        slug (str): The slug identifier of the streaming channel.

    Returns:
        Response: A JSON response containing the details of the requested channel if found, or an error message if not found.
    """
    if not channels.getSlugPattern().fullmatch(slug):
        message = "The channel slug is invalid."
        logger.error(f"{message} - Slug: {slug}")
        return Response(
            response=dumps({
                "error": message
            }),
            status=400,
            mimetype="application/json"
        )
    channel = channels.get(slug)
    if channel is None:
        message = "The channel is not found."
        logger.error(f"{message} - Slug: {slug}")
        return Response(
            response=dumps({
                "error": message
            }),
            status=404,
            mimetype="application/json"
        )
    metadata = {
        "subscriber_count": None,
        "video_count": None,
        "playback_status": "unavailable",
        "metadata_status": "unavailable",
        "checked_at": datetime.now().astimezone().isoformat(),
    }
    if channel.enabled:
        try:
            current = manager.getResolver().getChannelMetadata(channel)
            live_status = current.get("live_status")
            metadata.update({
                "subscriber_count": current.get("subscriber_count"),
                "video_count": current.get("video_count"),
                "playback_status": (
                    "live" if live_status == "is_live"
                    else "offline" if live_status in {"not_live", "was_live", "post_live", "is_upcoming"}
                    else "unknown"
                ),
                "metadata_status": "available",
                "checked_at": datetime.now().astimezone().isoformat(),
            })
        except Exception as error:
            logger.warn(f"Channel metadata lookup failed. - Slug: {slug} - Error type: {type(error).__name__}")
    return Response(
        response=dumps({
            "slug": channel.slug,
            "display_name": channel.display_name,
            "url": channel.youtube_url,
            "enabled": channel.enabled,
            **metadata,
        }),
        status=200,
        mimetype="application/json"
    )

@Streaming_Portal.route("/Channels/<string:slug>/live", methods=["GET"])
def play_live(slug: str) -> Response:
    """
    Playing the live stream of a specific channel.

    Procedures:
        1. Validate the channel slug format.
        2. Retrieve the channel information from the database.
        3. Check if the channel is enabled.
        4. Resolve the live stream URL.
        5. Redirect to the live stream if available, otherwise return an error.

    Parameters:
        slug (str): The slug identifier of the streaming channel.

    Returns:
        Response: A redirect response to the live stream if available, or a JSON response containing an error message if not available.
    """
    if not channels.getSlugPattern().fullmatch(slug):
        message = "The channel slug is invalid."
        logger.error(f"{message} - Slug: {slug}")
        return Response(
            response=dumps({
                "error": message
            }),
            status=400,
            mimetype="application/json"
        )
    channel = channels.get(slug)
    if channel is None:
        message = "The channel is not found."
        logger.error(f"{message} - Slug: {slug}")
        return Response(
            response=dumps({
                "error": message
            }),
            status=404,
            mimetype="application/json"
        )
    if not channel.enabled:
        message = "The channel is disabled."
        logger.error(f"{message} - Slug: {slug}")
        return Response(
            response=dumps({
                "error": message
            }),
            status=404,
            mimetype="application/json"
        )
    try:
        stream: Resolved_Stream = manager.resolve(channel)
        if stream.requires_remux:
            session_id = remux_manager.startOrReuse(channel.slug, stream)
            response = redirect(
                url_for(
                    "Streaming.remux_media",
                    slug=channel.slug,
                    session_id=session_id,
                    filename="index.m3u8",
                ),
                code=302,
            )
            response.headers["Cache-Control"] = "no-store"
            return response # type: ignore
        if not stream.url or not manager.getResolver().allowedMediaUniformResourceLocator(stream.url):
            message = "The resolved stream uniform resource locator is not allowed."
            logger.error(f"{message} - Slug: {slug}")
            return Response(
                response=dumps({
                    "error": message
                }),
                status=502,
                mimetype="application/json"
            )
        response = redirect(stream.url, code=302)
        response.headers["Cache-Control"] = "no-store"
        return response # type: ignore
    except StreamUnavailable as error:
        message = "The channel is not playable."
        logger.warn(f"{message} - Slug: {slug} - Error: {error}")
        return Response(
            response=dumps({
                "error": str(error),
            }),
            status=503,
            mimetype="application/json"
        )
    except ResolutionBusy as error:
        message = "The resolver is busy.  Please retry later."
        logger.warn(f"{message} - Slug: {slug} - Error: {error}")
        return Response(
            response=dumps({
                "error": message
            }),
            status=503,
            mimetype="application/json"
        )
    except RemuxUnavailable as error:
        message = "The live stream could not be remuxed."
        logger.warn(f"{message} - Slug: {slug} - Error: {error}")
        return Response(
            response=dumps({
                "error": str(error)
            }),
            status=503,
            mimetype="application/json"
        )
    except Exception as error:
        message = "The stream resolution failed."
        logger.error(f"{message} - Slug: {slug} - Error: {error}")
        return Response(
            response=dumps({
                "error": message,
                "channel": slug
            }),
            status=502,
            mimetype="application/json"
        )

@Streaming_Portal.route("/Channels/<string:slug>/sessions/<string:session_id>/<path:filename>", methods=["GET"])
def remux_media(slug: str, session_id: str, filename: str) -> Response:
    """
    Serving HLS manifests and segments generated by a validated remux session.

    Procedures:
        1. Validate the channel slug, session ID, and requested filename.
        2. Check if the remux session directory exists.
        3. Serve the requested file with appropriate MIME type and headers.

    Parameters:
        slug (str): The channel slug.
        session_id (str): The remux session ID.
        filename (str): The requested filename (e.g., "index.m3u8", "init.mp4", "segmentXXXXXX.m4s").

    Returns:
        Response: The HTTP response containing the requested file or a 404 status if not found.
    """
    if not channels.getSlugPattern().fullmatch(slug) or not channel_is_enabled(slug):
        return Response(status=404)
    if not session_id.isalnum() or len(session_id) != 32 or any(char not in "0123456789abcdef" for char in session_id):
        return Response(status=404)
    if filename != "index.m3u8" and filename != "init.mp4" and not (filename.startswith("segment") and filename.endswith(".m4s") and filename[7:-4].isdigit() and len(filename[7:-4]) == 6):
        return Response(status=404)
    directory: Path = remux_manager.getSessionDirectory(slug, session_id)
    if not directory.is_dir():
        return Response(status=404)
    mime_type: str = "application/vnd.apple.mpegurl" if filename.endswith(".m3u8") else ("video/mp4" if filename.endswith(".mp4") else "video/iso.segment")
    response: Response = send_from_directory(
        directory,
        filename,
        mimetype=mime_type,
        conditional=True
    )
    response.headers["Cache-Control"] = "no-store"
    response.headers["X-Content-Type-Options"] = "nosniff"
    return response

def channel_is_enabled(slug: str) -> bool:
    """
    Checking if a given channel slug corresponds to an enabled channel.

    Procedures:
        1. Retrieve the channel object based on the slug.
        2. Check if the channel exists and is enabled.

    Parameters:
        slug (str): The channel slug.

    Returns:
        bool: True if the channel exists and is enabled, False otherwise.
    """
    channel: Optional[Channel] = channels.get(slug)
    return channel is not None and channel.enabled

@Streaming_Portal.route("/playlist.m3u", methods=["GET"])
def playlist() -> Response:
    """
    Generating and returning the M3U playlist for all enabled channels.

    Procedures:
        1. Validate the configured base URL for the streaming service.
        2. Generate the M3U playlist for all enabled channels.
        3. Return the playlist as a response with appropriate headers.

    Returns:
        Response: The HTTP response containing the M3U playlist or an error message.
    """
    configured_base = environ.get("STREAMING_PUBLIC_BASE_URL", "").strip()
    if not configured_base:
        message = "The based streaming uniform resource locator is not configured."
        logger.error(message)
        return Response(
            response=dumps({
                "error": message
            }),
            status=503,
            mimetype="application/json"
        )
    parsed = urlparse(configured_base)
    allowed_protocols = {
        "http",
        "https",
    }
    if parsed.scheme not in allowed_protocols or not parsed.netloc or parsed.query or parsed.fragment or parsed.username:
        message = "The streaming uniform resource locator is invalid."
        logger.error(message)
        return Response(
            response=dumps({
                "error": message
            }),
            status=503,
            mimetype="application/json"
        )
    try:
        parsed.port
    except ValueError as error:
        message = "The streaming uniform resource locator configuration is invalid."
        logger.error(f"{message} - Error: {error}")
        return Response(
            response=dumps({
                "error": message
            }),
            status=503,
            mimetype="application/json"
        )
    base = configured_base.rstrip("/")
    lines = ["#EXTM3U"]
    for channel in channels.list(enabled_only=True):
        name = sub(r"[\r\n,\"]+", " ", channel.display_name).strip()
        lines.extend([f"#EXTINF:-1 tvg-id=\"{channel.slug}\" tvg-name=\"{name}\",{name}", f"{base}/Streaming/Channels/{channel.slug}/live"])
    response = "\n".join(lines) + "\n"
    response = Response(response, mimetype="audio/x-mpegurl")
    response.headers["Content-Disposition"] = 'inline; filename="extractio.m3u"'
    response.headers["Cache-Control"] = "no-store"
    return response
