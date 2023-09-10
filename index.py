# Importing the requirements for the application
from flask import Flask, render_template, request, Response
from DatabaseHandler import Database_Handler
from SecurityManagementSystem import Security_Management_System
from Routes.Session import Session_Portal
from Routes.Search import Search_Portal
from Routes.Media import Media_Portal
from Routes.Download import Download_Portal
from Routes.Video import Video_Portal

Application = Flask(__name__)
"""
The flask object implements a WSGI application and acts as
the central object.  It is passed the name of the module or
package of the application.  Once it is created it will act
as a central registry for the view functions, the URL rules,
template configuration and much more.

Type: Flask
"""
DatabaseHandler = Database_Handler()
"""
The database handler that will communicate with the database
server.

Type: Database_Handler
"""
SecurityManagementSystem = Security_Management_System()
"""
It will be a major component that will assure the security
of the data that will be stored across the application.

Type: Security_Management_System
"""
data = DatabaseHandler.get_data(
    None,
    "Session",
    filter_condition="date_created = CURRENT_DATE()",
    column_names="hash",
    sort_condition="identifier ASC",
    limit_condition=1
)
key: str = data[0][0]
"""
Encryption key of the application

Type: string
"""
Application.secret_key = key
Application.config["SESSION_TYPE"] = 'filesystem'
Application.register_blueprint(Session_Portal, url_prefix="/Session")
Application.register_blueprint(Search_Portal, url_prefix="/Search")
Application.register_blueprint(Media_Portal, url_prefix="/Media")
Application.register_blueprint(Download_Portal, url_prefix="/Download")
Application.register_blueprint(Video_Portal, url_prefix="/Public/Video")


def debug(mime_type: str = None, status: int = 500, response: str = None) -> None:  # type: ignore
    """
    Debugging the application.

    Parameters:
        mime_type:  string|null:    The MIME type of the application.
        status:     int:            The status of the response
        response:   string|null:    The response data

    Returns: void
    """
    directory = ""
    # Verifying that the port is for either Apache HTTPD or Werkzeug
    if request.environ.get("SERVER_PORT") == '80':
        directory = "/var/www/html/ytd_web_app"
    else:
        directory = "/home/darkness4869/Documents/extractio"
    log = f"{directory}/Access.log"
    file = open(log, "a")
    # Verifying the MIME type of the file for the correct logging
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

    Returns: Response
    """
    template = render_template('page.html')
    mime_type = "text/html"
    status = 200
    return Response(template, status, mimetype=mime_type)
