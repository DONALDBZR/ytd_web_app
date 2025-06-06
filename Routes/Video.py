from flask import Blueprint, Response
from Models.Video import Video


Video_Portal: Blueprint = Blueprint("Video", __name__, "../Public/Video/")
"""
The Routing for all the videos.
"""


@Video_Portal.route("/<string:name>", methods=['GET'])
def serveVideo(name: str) -> Response:
    """
    Sending the static file from the server.

    Parameters:
        name: string: The name of the video

    Returns:
        Response
    """
    ok: int = 200
    identifier: str = name.replace(".mp4", "")
    video_management_system: Video = Video(identifier)
    status: int = video_management_system.serveFile(False)
    return Video_Portal.send_static_file(name) if status == ok else Response({}, status, mimetype="application/json")

@Video_Portal.route("/Shorts/<string:name>", methods=['GET'])
def serveShortsVideo(name: str) -> Response:
    """
    Sending the static file from the server.

    Parameters:
        name: string: The name of the video

    Returns:
        Response
    """
    ok: int = 200
    identifier: str = name.replace(".mp4", "")
    video_management_system: Video = Video(identifier)
    status: int = video_management_system.serveFile(True)
    return Video_Portal.send_static_file(name) if status == ok else Response({}, status, mimetype="application/json")
