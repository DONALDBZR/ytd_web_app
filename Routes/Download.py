from flask import Blueprint, Response, render_template, request, send_file
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
    template = render_template('page.html', google_analytics_key=ENV.getGoogleAnalyticsKey())
    mime_type = "text/html"
    status = 200
    return Response(template, status, mimetype=mime_type)


@Download_Portal.route('/', methods=['POST'])
def downloadFile() -> Response:
    """
    Downloading the file from the file location that is sent
    from the view.

    Returns: Response
    """
    request_json = request.json
    file_path = request_json['file']  # type: ignore
    file_name = request_json['file_name']  # type: ignore
    mime_type = ""
    if "Audio" in file_path:
        mime_type = "audio/mp3"
    elif "Video" in file_path:
        mime_type = "video/mp4"
    return send_file(path_or_file=file_path, mimetype=mime_type, as_attachment=True, download_name=file_name)
