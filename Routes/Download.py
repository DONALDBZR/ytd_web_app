from flask import Blueprint, Response, render_template, request, send_file
from typing import Dict, Generator, Any
from Environment import Environment

Download_Portal = Blueprint("Download", __name__)
"""
The Routing for all the Downloads.

Type: Blueprint
"""
ENV = Environment()
"""
ENV File of the application
"""

@Download_Portal.route('/YouTube/<string:identifier>', methods=['GET'])
def downloadPage(identifier: str) -> Response:
    """
    Rendering the template needed which will import the
    web-worker.

    Parameters:
        identifier: string: Identifier of the media content to be searched.

    Returns: Response
    """
    template: str = render_template(
        'Download.html',
        google_analytics_key=ENV.getGoogleAnalyticsKey()
    )
    mime_type: str = "text/html"
    status: int = 200
    return Response(template, status, mimetype=mime_type)


@Download_Portal.route('/', methods=['POST'])
def downloadFile() -> Response:
    """
    Downloading the file from the file location that is sent
    from the view.

    Returns:
        Response
    """
    request_json: Dict[str, str] = request.json # type: ignore
    file_path: str = request_json['file']
    file_name: str = request_json['file_name']
    mime_type: str = "audio/mp3" if "Audio" in file_path else ""
    mime_type = "video/mp4" if "Video" in file_path else mime_type
    headers: Dict[str, str] = {
        "Content-Disposition": f"attachment: filename={file_name}"
    }

    def generateFile() -> Generator[bytes, Any, None]:
        with open(file_path, "rb") as file:
            while chunk := file.read(8192):
                yield chunk

    return Response(generateFile(), mimetype=mime_type, headers=headers)
