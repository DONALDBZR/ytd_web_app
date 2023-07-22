# Importing the requirements for the application
from flask import Flask, Response, render_template, url_for, jsonify, request, session
from datetime import datetime
import os
import json
from Environment import Environment
from pytube import YouTube


class SessionManager:
    """
    It allows the application to manage the session.
    """
    __directory: str
    """
    The directory of the session files

    Type: string
    """
    __ip_address: str
    """
    The IP Address of the user

    Type: string
    """
    __http_client_ip_address: str
    """
    The client's IP Address of the user

    Type: string
    """
    __proxy_ip_address: str
    """
    The Proxy's IP Address of the user

    Type: string
    """
    __timestamp: str
    """
    The timestamp at which the session has been created

    Type: string
    """
    __session_files: list
    """
    The files containing the session of the users

    Type: array
    """
    __color_scheme: str
    """
    The color scheme of the application

    Type: string
    """
    __length: int
    """
    The amount of session files

    Type: int
    """

    def __init__(self) -> None:
        """
        Instantiating the session's manager which will verify the session of the users
        """
        self.verifySession()

    def getDirectory(self) -> str:
        return self.__directory

    def setDirectory(self, directory: str) -> None:
        self.__directory = directory

    def getIpAddress(self) -> str:
        return self.__ip_address

    def setIpAddress(self, ip_address: str) -> None:
        self.__ip_address = ip_address

    def getHttpClientIpAddress(self) -> str:
        return self.__http_client_ip_address

    def setHttpClientIpAddress(self, http_client_ip_address: str) -> None:
        self.__http_client_ip_address = http_client_ip_address

    def getProxyIpAddress(self) -> str:
        return self.__proxy_ip_address

    def setProxyIpAddress(self, proxy_ip_address: str) -> None:
        self.__proxy_ip_address = proxy_ip_address

    def getTimestamp(self) -> str:
        return self.__timestamp

    def setTimestamp(self, timestamp: str) -> None:
        self.__timestamp = timestamp

    def getSessionFiles(self) -> list:
        return self.__session_files

    def setSessionFiles(self, session_files: list) -> None:
        self.__session_files = session_files

    def getColorScheme(self) -> str:
        return self.__color_scheme

    def setColorScheme(self, color_scheme: str) -> None:
        self.__color_scheme = color_scheme

    def getLength(self) -> int:
        return self.__length

    def setLength(self, length: int) -> None:
        self.__length = length

    def createSession(self) -> None:
        """
        Creating the session

        Returns: (void): The session is created
        """

        self.setIpAddress(request.environ.get('REMOTE_ADDR'))
        self.setHttpClientIpAddress(request.environ.get('HTTP_CLIENT_IP'))
        self.setProxyIpAddress(request.environ.get('HTTP_X_FORWARDED_FOR'))
        self.setTimestamp(datetime.now().strftime("%Y-%m-%d - %H:%M:%S"))
        self.setColorScheme("light")
        data = {
            "ip_address": self.getIpAddress(),
            "http_client_ip_address": self.getHttpClientIpAddress(),
            "proxy_ip_address": self.getProxyIpAddress(),
            "timestamp": self.getTimestamp(),
            "color_scheme": self.getColorScheme()
        }
        session['Client'] = data
        session_data = self.getSession()
        new_length = self.getLength() + 1
        file_name = "User_" + str(new_length) + ".json"
        file_path = self.getDirectory() + file_name
        session_file = open(file_path, 'w')
        session_file.write(session_data)
        session_file.close()

    def verifySession(self) -> None:
        """
        Verifying that the session is not hijacked

        Returns: (void): Either the session has been updated, the session has been destroyed or the session will be created
        """
        self.setDirectory("./Cache/Session/Users/")
        self.setSessionFiles(os.listdir(self.getDirectory()))
        self.setLength(len(self.getSessionFiles()))
        # Ensuring that there are session files.
        if len(self.getSessionFiles()) > 0:
            """
            Iterating throughout the session files to find any file that
            contains the IP Address of the client.
            """
            for index in range(0, len(self.getSessionFiles()), 1):
                # Ensuring that the session files are of JSON file type.
                if self.getSessionFiles()[index].endswith(".json"):
                    file_name = str(self.getDirectory() + "/" +
                                    self.getSessionFiles()[index])
                    file = open(file_name)
                    data = json.load(file)
                    """
                    Verifying the IP Address of the client against the IP
                    Address stored in the cache database.
                    """
                    if request.environ.get('REMOTE_ADDR') == data['Client']['ip_address']:
                        session = data
            self.setIpAddress(request.environ.get('REMOTE_ADDR'))
            """
            Ensuring that the Client data type is not null or else a
            session will be created.
            """
            if session.get('Client') is not None:
                """
                Comparing the IP Addresses to either renew the timestamp or
                to clear the session.
                """
                if session['Client']['ip_address'] == self.getIpAddress():
                    self.setTimestamp(
                        datetime.now().strftime("%Y-%m-%d - %H:%M:%S"))
                    session['Client']['timestamp'] = self.getTimestamp()
                else:
                    session.clear()
            else:
                self.createSession()
        else:
            self.createSession()

    def getSession(self) -> str:
        """
        Returning a stringified form of the session

        Returns: (str): A JSON stringified form of the session
        """
        return json.dumps(session, indent=4)

    def updateSession(self, data) -> None:
        """
        Modifying the session

        Parameters:
            data: (Any): Data from the view

        Returns: (void): The session has been updated
        """
        self.setIpAddress(request.environ.get('REMOTE_ADDR'))
        self.setTimestamp(datetime.now().strftime("%Y-%m-%d - %H:%M:%S"))
        self.setColorScheme(data["Client"]["color_scheme"])
        self.setSessionFiles(os.listdir(self.getDirectory()))
        """
        Iterating throughout the session files to update the session
        needed.
        """
        for index in range(0, len(self.getSessionFiles()), 1):
            # Ensuring that the session files are of JSON file type.
            if self.getSessionFiles()[index].endswith(".json"):
                file_name = str(self.getDirectory() + "/" +
                                self.getSessionFiles()[index])
                file = open(file_name)
                data = json.load(file)
                """
                Ensuring that the IP Addresses corresponds in order to
                update the session.
                """
                if self.getIpAddress() == data['Client']['ip_address']:
                    new_data = {
                        "ip_address": self.getIpAddress(),
                        "http_client_ip_address": data["Client"]["http_client_ip_address"],
                        "proxy_ip_address": data["Client"]["proxy_ip_address"],
                        "timestamp": self.getTimestamp(),
                        "color_scheme": self.getColorScheme()
                    }
                    session["Client"] = new_data
                    session_data = self.getSession()
                    file_to_be_updated = open(file_name, "w")
                    file_to_be_updated.write(session_data)
                    file_to_be_updated.close()
                    session["Client"]["timestamp"] = self.getTimestamp()
                    session["Client"]["color_scheme"] = self.getColorScheme()


class Media:
    """
    It allows the application to manage the media.
    """
    __search: str
    """
    The uniform resource locator to be searched.

    Type: string
    """
    _YouTube: None
    """
    It will handle every operations related to YouTube

    Type: YouTubeDownloader
    """

    def __init__(self, search: str) -> None:
        """
        Instantiating the media's manager which will search the media.
        """
        self.setSearch(search)

    def getSearch(self) -> str:
        return self.__search

    def setSearch(self, search: str) -> None:
        self.__search = search

    def verifyUniformResourceLocator(self) -> (dict | None):
        """
        Verifying the uniform resource locator in order to switch to
        the correct system.

        Returns: dict | None
        """
        if "youtube" in self.getSearch() or "youtu.be" in self.getSearch():
            self._YouTube = YouTubeDownloader(self.getSearch())
            return self._YouTube.search()


class YouTubeDownloader:
    """
    It will handle every operations related to YouTube
    """
    __uniform_resource_locator: str
    """
    The uniform resource locator to be searched.

    Type: string
    """
    __video: YouTube
    """
    The video from YouTube

    Type: YouTube
    """
    __artist: str
    """
    The artist of the video

    Type: string
    """
    __title: str
    """
    The title of the video

    Type: string
    """

    def __init__(self, uniform_resource_locator: str):
        """
        Instantiating the class and launching the operations needed
        """
        self.setUniformResourceLocator(uniform_resource_locator)

    def getUniformResourceLocator(self) -> str:
        return self.__uniform_resource_locator

    def setUniformResourceLocator(self, uniform_resource_locator: str) -> None:
        self.__uniform_resource_locator = uniform_resource_locator

    def getVideo(self) -> YouTube:
        return self.__video

    def setVideo(self, video: YouTube) -> None:
        self.__video = video

    def getArtist(self) -> str:
        return self.__artist

    def setArtist(self, artist: str) -> None:
        self.__artist = artist

    def getTitle(self) -> str:
        return self.__title

    def setTitle(self, title: str) -> None:
        self.__title = title

    def search(self) -> dict:
        """
        Searching for the video in YouTube.

        Returns: dict
        """
        self.setVideo(YouTube(self.getUniformResourceLocator()))
        self.setArtist(self.getVideo().title.split(" - ")[0])
        self.setTitle(self.getVideo().title.split(" - ")[1])
        data = {
            "uniform_resource_locator": self.getUniformResourceLocator(),
            "artist": self.getArtist(),
            "title": self.getTitle()
        }
        return data


# Instantiating the application
Application = Flask(__name__)
# Configuring the application for using sessions
Application.secret_key = Environment.SESSION_KEY
Application.config["SESSION_TYPE"] = 'filesystem'


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
    Session_Manager = SessionManager()
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

    Returns: (Response): JSON containing the session data
    """
    Session_Manager = SessionManager()
    get_data = request.json
    Session_Manager.updateSession(get_data)
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
    Rendering the template needed which will import the web-worker

    Returns: (str): The template which is stringified version of a HTML file
    """
    return render_template('page.html')


@Application.route("/Media/Search", methods=["POST"])
def search():
    """
    Searching for the media by the uniform resouce locator that
    has been retrieved from the client.
    """
    data = request.json
    media = Media(data["Media"]["search"])
    return "Done"
