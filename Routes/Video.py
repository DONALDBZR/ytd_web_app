from flask import Blueprint, Response


Video_Portal: Blueprint = Blueprint("Video", __name__, "../Public/Video/")
"""
The Routing for all the videos.
"""


@Video_Portal.route("/<string:identifier>")
def serveVideo(identifier: str) -> Response:
    """
    Sending the static file from the server.

    Parameters:
        identifier: string: Identifier of the video

    Returns: Response
    """
    return Video_Portal.send_static_file(identifier)
