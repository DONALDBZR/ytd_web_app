from flask import Blueprint, Response, request, Request
from Models.Logger import Extractio_Logger, Environment
from Errors.ExtractioErrors import ForgedRequestError, NotFoundError
from typing import List
from os import listdir
from re import match


Trend_Portal: Blueprint = Blueprint("Trend", __name__, "../Cache/Trend/")
"""
The Routing for all the trends.

Type: Blueprint
"""
ENV: Environment = Environment()
"""
ENV File of the application
"""
Logger: Extractio_Logger = Extractio_Logger(__name__)
"""
The logger that will all the action of the application.
"""

@Trend_Portal.route('/', methods=['GET'])
def getTrend():
    """
    Handling the request to retrieve the trend data from the server.

    This function:
    - Verifies if the request is correctly parameterized.
    - Retrieves the latest JSON file from the "Trend" directory.
    - Validates the filename to prevent malicious access.
    - Returns the content of the latest file as a JSON response.

    Returns:
        Response

    Raises:
        ForgedRequestError: If the request is forged or has invalid parameters.
        NotFoundError: If the directory is empty or the file cannot be found.
        ValueError: If the file name is invalid or does not match the expected format.
    """
    mime_type: str = "application/json"
    try:
        isRequestParametized(request)
        files: List[str] = listdir(Trend_Portal.static_folder)
        isEmptyFiles(files)
        file_name: str = max(files)
        isValidFileName(file_name)
        file_path: str = f"{ENV.getDirectory()}/Cache/Trend/{file_name}"
        file = open(file_path, "r")
        response: str = file.read()
        return Response(
            response=response,
            status=200,
            mimetype=mime_type
        )
    except ForgedRequestError as error:
        Logger.error(f"An attack attempt was attempted on this route.\nError: {error}\nIP Address: {request.remote_addr}")
        return Response(
            response={},
            status=403,
            mimetype=mime_type
        )
    except NotFoundError as error:
        Logger.error(f"There is an unexpected error on the API.\nError: {error}")
        return Response(
            response={},
            status=503,
            mimetype=mime_type
        )
    except ValueError as error:
        Logger.error(f"There is an unexpected error on the API's cache data.\nError: {error}\nFile Name: {file_name}")
        return Response(
            response={},
            status=503,
            mimetype=mime_type
        )

def isValidFileName(file_name: str) -> None:
    """
    Validating the file name to prevent malicious file access.

    This function:
    - Ensures the file name ends with ".json".
    - Checks that the file name consists only of digits.
    - Verifies that the file name doesn't contain any path traversal characters.
    - Raises appropriate errors if the file name is invalid or attempts a path traversal attack.

    Parameters:
        file_name (string): The name of the file to validate.

    Returns:
        None

    Raises:
        ValueError: If the file name is not valid or ends with an invalid extension.
        ForgedRequestError: If the file name contains malicious path traversal characters.
    """
    allowed_characters: str = r"^[0-9]+$"
    if not file_name.endswith(".json"):
        raise ValueError("The request has been forged.")
    file_name = file_name.replace(".json", "")
    if not match(allowed_characters, file_name):
        raise ValueError("Invalid file name.")
    if ".." in file_name or "\'" in file_name or "/" in file_name:
        raise ForgedRequestError("Path Transversal Attack is detected")
    if file_name.startswith("/") or file_name.startswith("\'"):
        raise ForgedRequestError("Path Transversal Attack is detected")
    return

def isRequestParametized(request: Request) -> None:
    """
    Checking if the request contains any data. If it does, raises a ForgedRequestError.

    This function is used to ensure that the request does not contain any unexpected parameters or data.

    Parameters:
        request (Request): The incoming Flask request object.

    Returns:
        None

    Raises:
        ForgedRequestError: If the request contains data when it shouldn't.
    """
    if not request.data:
        return
    raise ForgedRequestError("The request has been forged.")

def isEmptyFiles(files: List[str]) -> None:
    """
    Checking if the list of files is empty.

    This function ensures that there are files in the `"Trend"` directory.  If no files are found, raises a NotFoundError.

    Args:
        files (List[str]): A list of filenames in the `"Trend"` directory.

    Returns:
        None

    Raises:
        NotFoundError: If no files are found in the directory.
    """
    if files:
        return
    raise NotFoundError("The directory is empty.")
