from flask import Blueprint, Response, request
import os

Trend_Portal = Blueprint("Trend", __name__, "../Cache/Trend/")
"""
The Routing for all the trends.

Type: Blueprint
"""


def getDirectory() -> str:
    """
    Retrieving the directory of the application which depends on
    the server that is used.

    Returns: string
    """
    # Verifying that the port is for either Apache HTTPD or Werkzeug
    if request.environ.get("SERVER_PORT") == '80' or request.environ.get("SERVER_PORT") == '443':
        return "/var/www/html/ytd_web_app"
    else:
        return "/home/darkness4869/Documents/extractio"


@Trend_Portal.route('/', methods=['GET'])
def getTrend():
    """
    Sending the current trend in the form of JSON.

    Returns: Response
    """
    files = os.listdir(Trend_Portal.static_folder)
    file_name = f"{getDirectory()}/Cache/Trend/{files[-1]}"
    file = open(file_name, "r")
    response = file.read()
    mime_type = "application/json"
    status = 200
    return Response(response, status, mimetype=mime_type)
