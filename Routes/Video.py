from flask import Blueprint, Response

Video_Portal = Blueprint("Video", __name__, "../Public/Video/")
"""
The Routing for all the videos.

Type: Blueprint
"""


@Video_Portal.route("/<string:title>")
def serveVideo(title: str) -> Response:
    """
    Sending the static file from the server.

    Returns: Response
    """
    return Video_Portal.send_static_file(title)
