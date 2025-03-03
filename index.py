"""
The main entrypoint of the application.

Link:
    https://omnitechbros.ddns.net:591/
    http://omnitechbros.ddns.net:5000/
"""


from flask import Flask, render_template, request, Response, send_from_directory
from flask_compress import Compress
from flask_cors import CORS
from Models.DatabaseHandler import Database_Handler
from Models.SecurityManagementSystem import Security_Management_System
from Routes.Session import Session_Portal
from Routes.Search import Search_Portal
from Routes.Media import Media_Portal
from Routes.Download import Download_Portal
from Routes.Video import Video_Portal
from Routes.Trend import Trend_Portal
from Routes.Track import Track_Portal
from Environment import Environment
from re import match


Application: Flask = Flask(__name__)
"""
The flask object implements a WSGI application and acts as
the central object.  It is passed the name of the module or
package of the application.  Once it is created it will act
as a central registry for the view functions, the URL rules,
template configuration and much more.
"""
DatabaseHandler: Database_Handler = Database_Handler()
"""
The database handler that will communicate with the database
server.
"""
SecurityManagementSystem: Security_Management_System = Security_Management_System()
"""
It will be a major component that will assure the security
of the data that will be stored across the application.
"""
data = DatabaseHandler.getData(
    parameters=None,
    table_name="Session",
    filter_condition="date_created = CURDATE()",
    column_names="hash",
    sort_condition="identifier ASC",
    limit_condition=1
)
key: str = str(data[0]["hash"])  # type: ignore
"""
Encryption key of the application
"""
ENV: Environment = Environment()
"""
ENV File of the application
"""
Application.secret_key = key
Application.config["SESSION_TYPE"] = 'filesystem'
Application.config["COMPRESS_ALGORITHM"] = "gzip"
Application.config["COMPRESS_LEVEL"] = 6
Application.config["COMPRESS_MIN_SIZE"] = 500
Application.config["COMPRESS_MIMETYPES"] = ["text/html", "text/css", "text/javascript", "application/json", "text/babel"]
Application.config["MAX_CONTENT_LENGTH"] = 256 * 1024 * 1024
Application.register_blueprint(Session_Portal, url_prefix="/Session")
Application.register_blueprint(Search_Portal, url_prefix="/Search")
Application.register_blueprint(Media_Portal, url_prefix="/Media")
Application.register_blueprint(Download_Portal, url_prefix="/Download")
Application.register_blueprint(Video_Portal, url_prefix="/Public/Video")
Application.register_blueprint(Trend_Portal, url_prefix="/Trend")
Application.register_blueprint(Track_Portal, url_prefix="/Track")
Compress(Application)
CORS(Application)


@Application.route('/', methods=['GET'])
def homepage() -> Response:
    """
    Rendering the template needed which will import the
    web-worker.

    Returns:
        Response
    """
    template: str = render_template(
        'Homepage.html',
        google_analytics_key=ENV.getGoogleAnalyticsKey()
    )
    mime_type: str = "text/html"
    status: int = 200
    response: Response = Response(template, status, mimetype=mime_type)
    response.headers["Cache-Control"] = "public, max-age=604800"
    return response


@Application.route('/Sitemap.xml', methods=['GET'])
def getSiteMap() -> Response:
    """
    Sending the sitemap needed for Google Search Console.

    Returns:
        Response
    """
    return Application.send_static_file("Sitemap.xml")


@Application.route('/manifest.json', methods=['GET'])
def getManifest() -> Response:
    """
    Sending the manifest of the application.

    Returns:
        Response
    """
    return Application.send_static_file("manifest.json")


@Application.route('/static/scripts/js/<string:file>', methods=['GET'])
def serveScripts(file: str) -> Response:
    """
    Serving the JavaScript files.

    Parameters:
        file: string: The name of the file.

    Returns:
        Response
    """
    response = send_from_directory('static/scripts/js', file)
    response.cache_control.max_age = 604800
    response.cache_control.no_cache = False # type: ignore
    response.cache_control.public = True
    return response


@Application.route('/static/scripts/views/<path:file>', methods=['GET'])
def serveViews(file: str) -> Response:
    """
    Serving the React Components.

    Parameters:
        file: string: The name of the file.

    Returns:
        Response
    """
    response = send_from_directory('static/scripts/views', file)
    response.cache_control.max_age = 604800
    response.cache_control.no_cache = False # type: ignore
    response.cache_control.public = True
    return response


@Application.route('/static/stylesheets/<string:file>', methods=['GET'])
def serveStylesheets(file: str) -> Response:
    """
    Serving the stylesheets.

    Parameters:
        file: string: The name of the file.

    Returns:
        Response
    """
    response = send_from_directory('static/stylesheets', file)
    response.cache_control.max_age = 604800
    response.cache_control.no_cache = False # type: ignore
    response.cache_control.public = True
    return response

def validateFileName(file_name: str) -> bool:
    """
    Validating the file name based on the characters that are
    allowed.

    Parameters:
        file_name: string: The name of the file.

    Returns:
        boolean
    """
    allowed_characters: str = r"^[a-zA-Z0-9-_.]+$"
    return False if not match(allowed_characters, file_name) else True
