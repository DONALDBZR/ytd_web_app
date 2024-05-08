from flask import Blueprint, Response, render_template
from Environment import Environment


Search_Portal = Blueprint("Search", __name__)
"""
The Routing for all the Searches.

Type: Blueprint
"""
ENV = Environment()
"""
ENV File of the application
"""

@Search_Portal.route('/', methods=['GET'])
def searchPage() -> Response:
    """
    Rendering the template needed which will import the
    web-worker.

    Returns: Response
    """
    template = render_template('page.html', google_analytics_key=ENV.getGoogleAnalyticsKey())
    mime_type = "text/html"
    status = 200
    return Response(template, status, mimetype=mime_type)


@Search_Portal.route('/<string:identifier>', methods=['GET'])
def searchPageWithMedia(identifier: str) -> Response:
    """
    Rendering the template needed which will import the
    web-worker.

    Parameters:
        identifier: string: Identifier of the media conetent to be searched.

    Returns: Response
    """
    template = render_template('page.html', google_analytics_key=ENV.getGoogleAnalyticsKey())
    mime_type = "text/html"
    status = 200
    return Response(template, status, mimetype=mime_type)
