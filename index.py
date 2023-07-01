# Importing the requirements for the application
from flask import Flask, render_template, url_for
# Instantiating the application
Application = Flask(__name__)


@Application.route('/')
def homepage():
    return render_template('page.html')
