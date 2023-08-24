# Importing the requirements for the application
from flask import Flask, render_template, request
from datetime import date
from SessionManagementSystem import Session_Manager
from ObjectRelationalMapper import Object_Relational_Mapper
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
SecurityManagementSystem = Security_Management_System()
"""
It will be a major component that will assure the security
of the data that will be stored across the application.

Type: Security_Management_System
"""
ObjectRelationalMapper = Object_Relational_Mapper()
"""
It is the object relational mapper that will be used to
simplify the process to entering queries.

Type: Object_Relational_Mapper
"""
SessionManager = Session_Manager(request)
"""
It will be a major component that will assure the security
of the data that will be stored across the application.

Type: Session_Manager
"""
"""
SELECT *
FROM `Session`
WHERE date_created = :date_created
ORDER BY date_created DESC;
"""
Application.secret_key = ObjectRelationalMapper.get_table_records(parameters=[date.today(
)], table_name="Session", filter_condition="date_created = %s", sort_condition="identifier ASC")[1]
Application.config["SESSION_TYPE"] = 'filesystem'
"""
It allows the application to manage the session.

Type: Session_Management
"""


@Application.route('/')
def homepage() -> str:
    """
    Rendering the template needed which will import the web-worker

    Returns: string
    """
    return render_template('page.html')


@Application.route('/Session')
def getSession() -> str:
    """
    Sending the session data in the form of JSON.

    Returns: string
    """
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
    media = Media(data["Media"]["search"], None, data["Media"]["platform"])
    return json.dumps(media.verifyPlatform(), indent=4)


@Application.route('/Search/<string:identifier>')
def searchPageWithMedia(identifier: str):
    """
    Rendering the template needed which will import the
    web-worker.

    Parameters:
        identifier: string: Identifier of the media conetent to be searched.

    Returns: (string | void)
    """
    # if 'identifier' in session["Media"]["YouTube"] and identifier == session["Media"]["YouTube"]["identifier"]:
    return render_template('page.html')


# @Application.route('/Media')
# def getMedia():
#     """
#     Sending the data for the media that has been searched in the
#     form of JSON.

#     Returns: string
#     """
#     media_data = {
#         "Media": {
#             "YouTube": {
#                 "uniform_resource_locator": session["Media"]["YouTube"]["uniform_resource_locator"],
#                 "title": session["Media"]["YouTube"]["title"],
#                 "author": session["Media"]["YouTube"]["author"],
#                 "author_channel": session["Media"]["YouTube"]["author_channel"],
#                 "views": session["Media"]["YouTube"]["views"],
#                 "published_at": session["Media"]["YouTube"]["published_at"],
#                 "thumbnail": session["Media"]["YouTube"]["thumbnail"],
#                 "duration": session["Media"]["YouTube"]["duration"]
#             }
#         }
#     }
#     headers = {
#         "Content-Type": "application/json",
#     }
#     return jsonify(media_data), 200, headers


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
