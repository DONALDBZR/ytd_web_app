# Importing the requirements for the application
from flask import Flask, Response, render_template, jsonify, request, session
from datetime import date
from SessionManagementSystem import Session_Manager
from ObjectRelationalMapper import Object_Relational_Mapper
from Media import Media


# Instantiating the application
Application = Flask(__name__)
# Instantiating the object relational mapper
ObjectRelationalMapper = Object_Relational_Mapper()
# Configuring the application for using sessions
Application.secret_key = ObjectRelationalMapper.get_table_records(parameters=[date.today(
)], table_name="Session", filter_condition="date_created = %s", sort_condition="date_created DESC")[1]
Application.config["SESSION_TYPE"] = 'filesystem'


@Application.route('/')
def homepage() -> str:
    """
    Rendering the template needed which will import the web-worker

    Returns: string
    """
    return render_template('page.html')


@Application.route('/Session')
def getSession() -> Response:
    """
    Sending the session data in the form of JSON

    Returns: Response
    """
    SessionManager = Session_Manager()
    session_data = {
        "Client": {
            "timestamp": session["Client"]["timestamp"],
            "color_scheme": session["Client"]["color_scheme"]
        }
    }
    headers = {
        "Content-Type": "application/json",
    }
    return jsonify(session_data), 200, headers


@Application.route('/Session/Post', methods=['POST'])
def setSession() -> Response:
    """
    Allowing the Session Manager to update the session

    Returns: Response
    """
    SessionManager = Session_Manager()
    get_data = request.json
    SessionManager.updateSession(get_data)
    session_data = {
        "Client": {
            "timestamp": session["Client"]["timestamp"],
            "color_scheme": session["Client"]["color_scheme"]
        }
    }
    headers = {
        "Content-Type": "application/json",
    }
    return jsonify(session_data), 200, headers


@Application.route('/Search')
def searchPage() -> str:
    """
    Rendering the template needed which will import the
    web-worker

    Returns: string
    """
    return render_template('page.html')


@Application.route("/Media/Search", methods=["POST"])
def search() -> (str | None):
    """
    Searching for the media by the uniform resouce locator that has been retrieved from the client.

    Returns: Response
    """
    data = request.json
    media = Media(data["Media"]["search"], None, data["Media"]["platform"])
    return_data = media.verifyPlatform()
    return return_data


@Application.route('/Search/<string:identifier>')
def searchPageWithMedia(identifier: str) -> (str | None):
    """
    Rendering the template needed which will import the web-worker

    Returns: (string | void)
    """
    if 'identifier' in session["Media"]["YouTube"] and identifier == session["Media"]["YouTube"]["identifier"]:
        return render_template('page.html')


@Application.route('/Media')
def getMedia() -> Response:
    """
    Sending the data for the media that has been searched in the form of JSON

    Returns: Response
    """
    SessionManager = Session_Manager()
    media_data = {
        "Media": {
            "YouTube": {
                "uniform_resource_locator": session["Media"]["YouTube"]["uniform_resource_locator"],
                "title": session["Media"]["YouTube"]["title"],
                "author": session["Media"]["YouTube"]["author"],
                "author_channel": session["Media"]["YouTube"]["author_channel"],
                "views": session["Media"]["YouTube"]["views"],
                "published_at": session["Media"]["YouTube"]["published_at"],
                "thumbnail": session["Media"]["YouTube"]["thumbnail"],
                "duration": session["Media"]["YouTube"]["duration"]
            }
        }
    }
    headers = {
        "Content-Type": "application/json",
    }
    return jsonify(media_data), 200, headers


@Application.route('/Media/Download')
def retrieveMedia():
    """
    Retrieving the media needed from the uniform resource locator and stores it in the server while allowing the user to download it.
    """
    SessionManager = Session_Manager()
    referer = request.referrer
    data = request.json
    if 'Search' in referer:
        media = Media(data["Media"]["uniform_resource_locator"],
                      referer, data["media"]["platform"])
        headers = {
            "Content-Type": "application/json",
        }
