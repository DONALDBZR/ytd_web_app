# Importing the requirements for the application
from flask import Flask, Response, render_template, url_for, jsonify
from flask_session import Session
from Session import SessionManager
# Instantiating the application
Application = Flask(__name__)
Session_Manager = SessionManager()
# Configuring the application for using sessions
Application.config["SESSION_TYPE"] = 'filesystem'
Session(Application)


@Application.route('/')
def homepage() -> str:
    """
    Rendering the template needed which will import the web-worker

    Returns: (str): The template which is stringified version of a HTML file
    """
    return render_template('page.html')


@Application.route('/Session')
def getSession() -> Response:
    """
    Sending the session data in the form of JSON

    Returns: (Response): JSON containing the session data
    """
    return jsonify(Session_Manager.getSession())
