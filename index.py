# Importing the requirements for the application
from flask import Flask, render_template, request, session
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


@Application.route('/', methods=['GET'])
def homepage() -> str:
    """
    Rendering the template needed which will import the web-worker

    Returns: string
    """
    return render_template('page.html')


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
        "search": str(data["Media"]["search"]),
        "platform": str(data["Media"]["platform"]),
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
    file_name = f"./Cache/Media/{request.environ.get('REMOTE_ADDR')}.json"
    file = open(file_name)
    media_data = file.read()
    return media_data


# @Application.route('/Media/Download')
# def retrieveMedia():
#     """
#     Retrieving the media needed from the uniform resource locator and stores it in the server while allowing the user to download it.
#     """
#     SessionManager = Session_Manager()
#     referer = request.referrer
#     data = request.json
#     if 'Search' in referer:
#         media = Media(data["Media"]["uniform_resource_locator"],
#                       referer, data["media"]["platform"])
#         headers = {
#             "Content-Type": "application/json",
#         }
