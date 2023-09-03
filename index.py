# Importing the requirements for the application
from flask import Flask, render_template, request, session, send_file, Response
from datetime import date
from SessionManagementSystem import Session_Manager
from DatabaseHandler import Database_Handler
from Media import Media
import json
from SecurityManagementSystem import Security_Management_System
import os
import logging

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


def debug(mime_type: str, status: int) -> None:
    """
    Debugging the application.

    Parameters:
        mime_type:  string: The MIME type of the application.
        status:     int:    The status of the response

    Returns: void
    """
    directory = "/var/www/html/ytd_web_app/Access.log"
    file = open(directory, "a")
    file.write(
        f"Request Method: {request.environ.get('REQUEST_METHOD')}\nRoute: {request.environ.get('REQUEST_URI')}\nMIME type: {mime_type}\nResponse Status: HTTP/{status}\n")  # type: ignore
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
    debug(mime_type, status)
    return Response(template, 200, mimetype=mime_type)


@Application.route('/Session', methods=['GET'])
def getSession() -> str:
    """
    Sending the session data in the form of JSON.

    Returns: string
    """
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
    return json.dumps(session_data, indent=4)


@Application.route('/Session/Post', methods=['POST'])
def setSession() -> str:
    """
    Allowing the Session Manager to update the session.

    Returns: string
    """
    get_data = request.json
    user_request = {
        "ip_address": str(request.environ.get('REMOTE_ADDR')),
        "http_client_ip_address": str(request.environ.get("HTTP_CLIENT_IP")),
        "proxy_ip_address": str(request.environ.get("HTTP_X_FORWARDED_FOR"))
    }
    SessionManager = Session_Manager(user_request, session)
    SessionManager.updateSession(get_data)
    session_data = {
        "Client": {
            "timestamp": SessionManager.getSession()["Client"]["timestamp"],
            "color_scheme": SessionManager.getSession()["Client"]["color_scheme"]
        }
    }
    return json.dumps(session_data, indent=4)


@Application.route('/Search')
def searchPage() -> str:
    """
    Rendering the template needed which will import the
    web-worker.

    Returns: string
    """
    return render_template('page.html')


@Application.route("/Media/Search", methods=["POST"])
def search() -> str:
    """
    Searching for the media by the uniform resouce locator that
    has been retrieved from the client.

    Returns: string
    """
    data = request.json
    user_request = {
        "referer": None,
        "search": str(data["Media"]["search"]),  # type: ignore
        "platform": str(data["Media"]["platform"]),  # type: ignore
        "ip_address": str(request.environ.get("REMOTE_ADDR"))
    }
    media = Media(user_request)
    return json.dumps(media.verifyPlatform(), indent=4)


@Application.route('/Search/<string:identifier>', methods=['GET'])
def searchPageWithMedia(identifier: str) -> str:
    """
    Rendering the template needed which will import the
    web-worker.

    Parameters:
        identifier: string: Identifier of the media conetent to be searched.

    Returns: string
    """
    return render_template('page.html')


@Application.route('/Media', methods=["GET"])
def getMedia() -> str:
    """
    Sending the data for the media that has been searched in the
    form of JSON.

    Returns: string
    """
    file_name = f"/var/www/html/ytd_web_app/Cache/Media/{request.environ.get('REMOTE_ADDR')}.json"
    file = open(file_name)
    media_data = file.read()
    return media_data


@Application.route('/Media/Download', methods=['POST'])
def retrieveMedia() -> str:
    """
    Retrieving the media needed from the uniform resource
    locator and stores it in the server while allowing the user
    to download it.

    Returns: string
    """
    request_json = request.json
    data = request_json["Media"]  # type: ignore
    user_request = {
        "referer": request.referrer,
        "search": str(data["uniform_resource_locator"]),  # type: ignore
        "platform": str(data["platform"]),  # type: ignore
        "ip_address": str(request.environ.get("REMOTE_ADDR"))
    }
    if "Search" in request.referrer:
        media = Media(user_request)
    print(f"Media Data: {media.verifyPlatform()}")
    return media.verifyPlatform()
    # return json.dumps(media.verifyPlatform(), indent=4)  # type: ignore


@Application.route('/Download/YouTube/<string:identifier>', methods=['GET'])
def downloadPage(identifier: str) -> str:
    """
    Rendering the template needed which will import the
    web-worker.

    Parameters:
        identifier: string: Identifier of the media conetent to be searched.

    Returns: string
    """
    return render_template('page.html')


@Application.route('/Download', methods=['POST'])
def downloadFile() -> Response:
    """
    Downloading the file from the file location that is sent
    from the view.

    Returns: Response
    """
    request_json = request.json
    file_path = f"./{request_json['file']}"  # type: ignore
    file_name = request_json['file_name']  # type: ignore
    mime_type = ""
    if "Audio" in file_path:
        mime_type = "audio/mp4"
    elif "Video" in file_path:
        mime_type = "video/mp4"
    return send_file(path_or_file=file_path, mimetype=mime_type, as_attachment=True, download_name=file_name)
