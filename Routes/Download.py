from flask import Blueprint, Response, render_template

Download_Portal = Blueprint("Download", __name__)
"""
The Routing for all the Downloads.

Type: Blueprint
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
    template = render_template('page.html')
    mime_type = "text/html"
    status = 200
    return Response(template, status, mimetype=mime_type)
