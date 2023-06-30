from flask import Flask, render_template
Application = Flask(__name__)


@Application.route('/')
def homepage():
    return render_template('page.html')
