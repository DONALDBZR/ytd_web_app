"""
The main entrypoint of the application.

Link:
    https://omnitechbros.ddns.net:591/
    http://omnitechbros.ddns.net:5000/
"""


from flask import Flask, render_template, request, Response, send_from_directory
from flask_compress import Compress
from Models.DatabaseHandler import Database_Handler
from Models.SecurityManagementSystem import Security_Management_System
from Routes.Session import Session_Portal
from Routes.Search import Search_Portal
from Routes.Media import Media_Portal
from Routes.Download import Download_Portal
from Routes.Video import Video_Portal
from Routes.Trend import Trend_Portal
from Environment import Environment


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
key = str(data[0]["hash"]) # type: ignore
"""
Encryption key of the application
"""
ENV = Environment()
"""
ENV File of the application
"""
Application.secret_key = key
Application.config["SESSION_TYPE"] = 'filesystem'
Application.config["COMPRESS_ALGORITHM"] = "gzip"
Application.config["COMPRESS_LEVEL"] = 6
Application.config["COMPRESS_MIN_SIZE"] = 500
Application.config["COMPRESS_MIMETYPES"] = ["text/html", "text/css", "text/javascript", "application/json", "text/babel"]
Application.register_blueprint(Session_Portal, url_prefix="/Session")
Application.register_blueprint(Search_Portal, url_prefix="/Search")
Application.register_blueprint(Media_Portal, url_prefix="/Media")
Application.register_blueprint(Download_Portal, url_prefix="/Download")
Application.register_blueprint(Video_Portal, url_prefix="/Public/Video")
Application.register_blueprint(Trend_Portal, url_prefix="/Trend")
Compress(Application)


def debug(mime_type: str = None, status: int = 500, response: str = None) -> None:  # type: ignore
    """
    Debugging the application.

    Parameters:
        mime_type:  string|null:    The MIME type of the application.
        status:     int:            The status of the response
        response:   string|null:    The response data

    Returns:
        void
    """
    directory = ""
    if request.environ.get("SERVER_PORT") == '80' or request.environ.get("SERVER_PORT") == '591':
        directory = "/var/www/html/ytd_web_app"
    else:
        directory = "/home/darkness4869/Documents/extractio"
    log = f"{directory}/Access.log"
    file = open(log, "a")
    if mime_type.find("html") != -1:
        file.write(
            f"Request Method: {request.environ.get('REQUEST_METHOD')}\nRoute: {request.environ.get('REQUEST_URI')}\nMIME type: {mime_type}\nResponse Status: HTTP/{status}\n")  # type: ignore
    else:
        if mime_type.find("json") != -1 and request.environ.get("POST"):
            file.write(
                f"Request Method: {request.environ.get('REQUEST_METHOD')}\nRoute: {request.environ.get('REQUEST_URI')}\nMIME type: {mime_type}\nResponse Status: HTTP/{status}\nRequest: {request.json}\nResponse: {response}\n")  # type: ignore
        else:
            file.write(
                f"Request Method: {request.environ.get('REQUEST_METHOD')}\nRoute: {request.environ.get('REQUEST_URI')}\nMIME type: {mime_type}\nResponse Status: HTTP/{status}\nResponse: {response}\n")  # type: ignore
    file.close()


@Application.route('/', methods=['GET'])
def homepage() -> Response:
    """
    Rendering the template needed which will import the
    web-worker.

    Returns:
        Response
    """
    template = render_template('Homepage.html', google_analytics_key=ENV.getGoogleAnalyticsKey())
    mime_type = "text/html"
    status = 200
    response = Response(template, status, mimetype=mime_type)
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
def serveJS(file: str) -> Response:
    """
    Serving the JavaScript files.

    Parameters:
        file: string: The name of the file.

    Returns:
        Response
    """
    response = send_from_directory('static/scripts/js', file)
    response.cache_control.max_age = 604800
    response.cache_control.no_cache = False
    response.cache_control.public = True
    return response