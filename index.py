# Importing the requirements for the application
from flask import Flask, render_template, url_for
from flask_session import Session
from Session import SessionManager
# Instantiating the application
Application = Flask(__name__)
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
