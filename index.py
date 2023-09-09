# Importing the requirements for the application
from flask import Flask, render_template, request, session, send_file, Response
from datetime import date
from SessionManagementSystem import Session_Manager
from DatabaseHandler import Database_Handler
from Media import Media
import json
from SecurityManagementSystem import Security_Management_System

Application = Flask(__name__)
"""
The flask object implements a WSGI application and acts as
the central object.  It is passed the name of the module or
package of the application.  Once it is created it will act
as a central registry for the view functions, the URL rules,
template configuration and much more.

Type: Flask
"""
host = f"{request.environ.get('SERVER_NAME')}:{request.environ.get('SERVER_PORT')}"
"""
The server on which the application is being hosted on which
it will be either Apache HTTPD or Werkzeug.
"""
DatabaseHandler = Database_Handler(host)
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


def debug(mime_type: str = None, status: int = 500, response: str = None) -> None:  # type: ignore
    """
    Debugging the application.

    Parameters:
        mime_type:  string|null:    The MIME type of the application.
        status:     int:            The status of the response
        response:   string|null:    The response data

    Returns: void
    """
    directory = "/var/www/html/ytd_web_app/Access.log"
    file = open(directory, "a")
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
    mime_type = ""
    status = 404
    # Verifying that the template is returned
    if type(template) is str:
        mime_type = "text/html"
        status = 200
    debug(status=status, mime_type=mime_type)
    return Response(template, status, mimetype=mime_type)


@Application.route('/Session', methods=['GET'])
def getSession() -> Response:
    """
    Sending the session data in the form of JSON.

    Returns: Response
    """
    mime_type = ""
    status = 500
    user_request = {
        "ip_address": str(request.environ.get('REMOTE_ADDR')),
        "http_client_ip_address": str(request.environ.get("HTTP_CLIENT_IP")),
        "proxy_ip_address": str(request.environ.get("HTTP_X_FORWARDED_FOR"))
    }
    SessionManager = Session_Manager(user_request, session)
    session_data = {
        "Client": {
            "timestamp": SessionManager.getSession()["Client"]["timestamp"],
            "color_scheme": SessionManager.getSession()["Client"]["color_scheme"]
        }
    }
    response = json.dumps(session_data, indent=4)
    mime_type = "application/json"
    status = 200
    debug(mime_type=mime_type, status=status, response=response)
    return Response(response, status, mimetype=mime_type)


@Application.route('/Session/Post', methods=['POST'])
def setSession() -> Response:
    """
    Allowing the Session Manager to update the session.

    Returns: Response
    """
    payload = request.json
    mime_type = ""
    status = 500
    user_request = {
        "ip_address": str(request.environ.get('REMOTE_ADDR')),
        "http_client_ip_address": str(request.environ.get("HTTP_CLIENT_IP")),
        "proxy_ip_address": str(request.environ.get("HTTP_X_FORWARDED_FOR"))
    }
    SessionManager = Session_Manager(user_request, session)
    SessionManager.updateSession(payload)
    mime_type = "application/json"
    status = 201
    session_data = {
        "Client": {
            "timestamp": SessionManager.getSession()["Client"]["timestamp"],
            "color_scheme": SessionManager.getSession()["Client"]["color_scheme"]
        }
    }
    response = json.dumps(session_data, indent=4)
    debug(
        mime_type=mime_type, status=status, response=response)
    return Response(response, status, mimetype=mime_type)


@Application.route('/Search')
def searchPage() -> Response:
    """
    Rendering the template needed which will import the
    web-worker.

    Returns: Response
    """
    template = render_template('page.html')
    mime_type = ""
    status = 404
    # Verifying that the template is returned
    if type(template) is str:
        mime_type = "text/html"
        status = 200
    debug(status=status, mime_type=mime_type)
    return Response(template, status, mimetype=mime_type)


@Application.route("/Media/Search", methods=["POST"])
def search() -> Response:
    """
    Searching for the media by the uniform resouce locator that
    has been retrieved from the client.

    Returns: Response
    """
    payload = request.json
    mime_type = ""
    status = 500
    user_request = {
        "referer": None,
        "search": str(payload["Media"]["search"]),  # type: ignore
        "platform": str(payload["Media"]["platform"]),  # type: ignore
        "ip_address": str(request.environ.get("REMOTE_ADDR"))
    }
    media = Media(user_request)
    response = json.dumps(media.verifyPlatform(), indent=4)
    status = int(media.verifyPlatform()["data"]["status"])
    mime_type = "application/json"
    debug(
        mime_type=mime_type, status=status, response=response)
    return Response(response, status, mimetype=mime_type)


@Application.route('/Search/<string:identifier>', methods=['GET'])
def searchPageWithMedia(identifier: str) -> Response:
    """
    Rendering the template needed which will import the
    web-worker.

    Parameters:
        identifier: string: Identifier of the media conetent to be searched.

    Returns: Response
    """
    template = render_template('page.html')
    mime_type = ""
    status = 404
    # Verifying that the template is returned
    if type(template) is str:
        mime_type = "text/html"
        status = 200
    debug(status=status, mime_type=mime_type)
    return Response(template, status, mimetype=mime_type)


@Application.route('/Media', methods=["GET"])
def getMedia() -> Response:
    """
    Sending the data for the media that has been searched in the
    form of JSON.

    Returns: Response
    """
    mime_type = ""
    status = 404
    file_name = f"/var/www/html/ytd_web_app/Cache/Media/{request.environ.get('REMOTE_ADDR')}.json"
    file = open(file_name)
    response = file.read()
    mime_type = "application/json"
    status = 200
    debug(status=status, mime_type=mime_type, response=response)
    return Response(response, status, mimetype=mime_type)


@Application.route('/Media/Download', methods=['POST'])
def retrieveMedia() -> Response:
    """
    Retrieving the media needed from the uniform resource
    locator and stores it in the server while allowing the user
    to download it.

    Returns: string
    """
    mime_type = ""
    status = 500
    payload = request.json
    data = payload["Media"]  # type: ignore
    user_request = {
        "referer": request.referrer,
        "search": str(data["uniform_resource_locator"]),  # type: ignore
        "platform": str(data["platform"]),  # type: ignore
        "ip_address": str(request.environ.get("REMOTE_ADDR"))
    }
    response = {}
    # Ensuring that the payload is from the search page
    if "Search" in request.referrer:
        media = Media(user_request)
        response = media.verifyPlatform()
    mime_type = "application/json"
    status = response["data"]["status"]
    response = json.dumps(response, indent=4)
    debug(status=status, mime_type=mime_type, response=response)
    return Response(response, status, mimetype=mime_type)


@Application.route('/Download/YouTube/<string:identifier>', methods=['GET'])
def downloadPage(identifier: str) -> Response:
    """
    Rendering the template needed which will import the
    web-worker.

    Parameters:
        identifier: string: Identifier of the media conetent to be searched.

    Returns: Response
    """
    template = render_template('page.html')
    mime_type = ""
    status = 404
    # Verifying that the template is returned
    if type(template) is str:
        mime_type = "text/html"
        status = 200
    debug(status=status, mime_type=mime_type)
    return Response(template, status, mimetype=mime_type)


@Application.route('/Download', methods=['POST'])
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
