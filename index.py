# Importing the requirements for the application
from flask import Flask, Response, render_template, url_for, jsonify, request, session, redirect
from datetime import datetime, timedelta
import time
import os
import json
from Environment import Environment
from pytube import YouTube
import mysql.connector


class Session_Manager:
    """
    It allows the application to manage the session.
    """
    __directory: str
    """
    The directory of the session files

    Type: string
    Visibility: private
    """
    __ip_address: str
    """
    The IP Address of the user

    Type: string
    Visibility: private
    """
    __http_client_ip_address: str
    """
    The client's IP Address of the user

    Type: string
    Visibility: private
    """
    __proxy_ip_address: str
    """
    The Proxy's IP Address of the user

    Type: string
    Visibility: private
    """
    __timestamp: str
    """
    The timestamp at which the session has been created

    Type: string
    Visibility: private
    """
    __session_files: list
    """
    The files containing the session of the users

    Type: array
    Visibility: private
    """
    __color_scheme: str
    """
    The color scheme of the application

    Type: string
    Visibility: private
    """
    __length: int
    """
    The amount of session files

    Type: int
    Visibility: private
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

        Returns: void
        """
        session.clear()
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
        file_name = self.getIpAddress() + ".json"
        file_path = self.getDirectory() + file_name
        session_file = open(file_path, 'w')
        session_file.write(session_data)
        session_file.close()

    def verifySession(self) -> None:
        """
        Verifying that the session is not hijacked

        Returns: (void)
        """
        self.setDirectory("./Cache/Session/Users/")
        self.setSessionFiles(os.listdir(self.getDirectory()))
        self.setLength(len(self.getSessionFiles()))
        # Ensuring that there are session files.
        if len(self.getSessionFiles()) > 0:
            # Iterating throughout the session files to find any file that contains the IP Address of the client.
            for index in range(0, len(self.getSessionFiles()), 1):
                # Ensuring that the session files are of JSON file type.
                if self.getSessionFiles()[index].endswith(".json"):
                    file_name = str(self.getDirectory() + "/" +
                                    self.getSessionFiles()[index])
                    file = open(file_name)
                    data = json.load(file)
                    # Verifying the IP Address of the client against the IP Address stored in the cache database as well as ensuring that the session is not expired.
                    if request.environ.get('REMOTE_ADDR') == data['Client']['ip_address']:
                        timestamp = datetime.strptime(
                            data['Client']['timestamp'], "%Y-%m-%d - %H:%M:%S") + timedelta(hours=1)
                        # Verifying that the session has not expired
                        if timestamp > datetime.now():
                            session = data
                        else:
                            self.createSession()
            self.setIpAddress(request.environ.get('REMOTE_ADDR'))
            # Ensuring that the Client data type is not null or else a session will be created.
            if session.get('Client') is not None:
                # Comparing the IP Addresses to either renew the timestamp or to clear the session.
                if session['Client']['ip_address'] == self.getIpAddress() and session["Client"]:
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

        Returns: string
        """
        return json.dumps(session, indent=4)

    def updateSession(self, data) -> None:
        """
        Modifying the session

        Parameters: data: mixed: Data from the view

        Returns: void
        """
        self.setIpAddress(request.environ.get('REMOTE_ADDR'))
        self.setTimestamp(datetime.now().strftime("%Y-%m-%d - %H:%M:%S"))
        self.setColorScheme(data["Client"]["color_scheme"])
        self.setSessionFiles(os.listdir(self.getDirectory()))
        # Iterating throughout the session files to update the session needed.
        for index in range(0, len(self.getSessionFiles()), 1):
            # Ensuring that the session files are of JSON file type.
            if self.getSessionFiles()[index].endswith(".json"):
                file_name = str(self.getDirectory() + "/" +
                                self.getSessionFiles()[index])
                file = open(file_name)
                data = json.load(file)
                # Ensuring that the IP Addresses corresponds in order to update the session.
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
    Visibility: private
    """
    _YouTubeDownloader: None
    """
    It will handle every operations related to YouTube

    Type: YouTube_Downloader
    Visibility: protected
    """
    __referer: str | None
    """
    The http referrer which is the uniform resource locator that is needed to be able to allow the user to download the requried media.

    Type: string|null
    Visibility: private
    """

    def __init__(self, search: str, referer: str | None) -> None:
        """
        Instantiating the media's manager which will search the media.

        Parameters:
            search: string: The uniform resource locator to be searched.
            referer: string | null: The http referrer which is the uniform resource locator that is needed to be able to allow the user to download the requried media.
        """
        self.setSearch(search)
        self.setReferer(referer)

    def getSearch(self) -> str:
        return self.__search

    def setSearch(self, search: str) -> None:
        self.__search = search

    def getReferer(self) -> str | None:
        return self.__referer

    def setReferer(self, referer: str | None) -> None:
        self.__referer = referer

    def verifyUniformResourceLocator(self):
        """
        Verifying the uniform resource locator in order to switch to the correct system as well as select and return the correct response.

        Returns: String | None
        """
        # Verifying that the content is from the specified platform before trigerreing the correct system.
        if "youtube" in self.getSearch() or "youtu.be" in self.getSearch():
            # Verifying that there is no referer.
            if self.getReferer() is None:
                self._YouTube = YouTube_Downloader(self.getSearch())
                return self._YouTube.search()
            else:
                self._YouTube = YouTube_Downloader(self.getSearch())


class YouTube_Downloader:
    """
    It will handle every operations related to YouTube
    """
    __uniform_resource_locator: str
    """
    The uniform resource locator to be searched.

    Type: string
    Visibility: private
    """
    __video: YouTube
    """
    The video from YouTube

    Type: YouTube
    Visibility: private
    """
    __artist: str
    """
    The artist of the video

    Type: string
    Visibility: private
    """
    __title: str
    """
    The title of the video

    Type: string
    Visibility: private
    """
    __identifier: str
    """
    The identifier of the video

    Type: string
    Visibility: private
    """
    __length: int
    """
    The length of the video in seconds

    Type: int
    Visibility: private
    """
    __duration: str
    """
    The duration of the video in the format of HH:mm:ss

    Type: string
    Visibility: private
    """
    __published_at: str
    """
    The date at which the video has been published

    Type: string
    Visibility: private
    """

    def __init__(self, uniform_resource_locator: str):
        """
        Instantiating the class and launching the operations needed

        Parameters: uniform_resource_locator: string: The uniform resource locator to be searched.
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

    def getIdentifier(self) -> str:
        return self.__identifier

    def setIdentifier(self, identifier: str) -> None:
        self.__identifier = identifier

    def getLength(self) -> int:
        return self.__length

    def setLength(self, length: int) -> None:
        self.__length = length

    def getDuration(self) -> str:
        return self.__duration

    def setDuration(self, duration: str) -> None:
        self.__duration = duration

    def getPublishedAt(self) -> str:
        return self.__published_at

    def setPublishedAt(self, published_at: datetime) -> None:
        self.__published_at = str(published_at)

    def search(self) -> str:
        """
        Searching for the video in YouTube.

        Returns: String
        """
        self.setVideo(YouTube(self.getUniformResourceLocator()))
        self.setArtist(self.getVideo().title.split(" - ")[0])
        self.setTitle(self.getVideo().title.split(" - ")[1])
        self.setIdentifier(self.getUniformResourceLocator())
        self.setIdentifier(self.getIdentifier().replace(
            "https://www.youtube.com/watch?v=", ""))
        self.setLength(self.getVideo().length)
        self.setDuration(time.strftime(
            "%H:%M:%S", time.gmtime(self.getLength())))
        self.setPublishedAt(self.getVideo().publish_date)
        data = {
            "uniform_resource_locator": self.getUniformResourceLocator(),
            "artist": self.getArtist(),
            "title": self.getTitle(),
            "identifier": self.getIdentifier(),
            "author": self.getVideo().author,
            "author_channel": self.getVideo().channel_url,
            "views": self.getVideo().views,
            "published_at": self.getPublishedAt(),
            "thumbnail": self.getVideo().thumbnail_url,
            "duration": self.getDuration()
        }
        session["Media"] = {}
        session["Media"]["YouTube"] = data
        filename = "./Cache/Session/Users/" + \
            session["Client"]["ip_address"] + ".json"
        file = open(filename, "w")
        file.write(json.dumps(session, indent=4))
        file.close()
        return json.dumps(session["Media"], indent=4)


class Database_Handler:
    """
    The database handler that will communicate with the database server.
    """
    __host: str
    """
    The host of the application

    Type: string
    visibility: private
    """
    __database: str
    """
    The database of the application

    Type: string
    visibility: private
    """
    __username: str
    """
    The user that have access to the database

    Type: string
    visibility: private
    """
    __password: str
    """
    The password that allows the required user to connect to the database.

    Type: string
    visibility: private
    """
    __database_handler: None
    """
    The database handler needed to execute the queries needed

    Type: PooledMySQLConnection | MySQLConnection | Any
    visibility: private
    """
    __statement: None
    """
    The statement to be used to execute all of the requests to the database server

    Type: MySQLCursor
    visibility: private
    """

    def __init__(self):
        """
        Instantiating the class which will try to connect to the database.
        """
        self.setHost(Environment.HOST)
        self.setDatabase(Environment.DATABASE)
        self.setUsername(Environment.USERNAME)
        self.setPassword(Environment.PASSWORD)
        try:
            self.setDatabaseHandler(mysql.connector.connect(host=self.getHost(
            ), database=self.getDatabase(), username=self.getUsername(), password=self.getPassword()))
        except mysql.connector.Error as error:
            print("Connection Failed: " + error)

    def getHost(self) -> str:
        return self.__host

    def setHost(self, host: str) -> None:
        self.__host = host

    def getDatabase(self) -> str:
        return self.__database

    def setDatabase(self, database: str) -> None:
        self.__database = database

    def getUsername(self) -> str:
        return self.__username

    def setUsername(self, username: str) -> None:
        self.__username = username

    def getPassword(self) -> str:
        return self.__password

    def setPassword(self, password: str) -> None:
        self.__password = password

    def getDatabaseHandler(self):
        return self.__database_handler

    def setDatabaseHandler(self, database_handler) -> None:
        self.__database_handler = database_handler

    def getStatement(self):
        return self.__statement

    def setStatement(self, statement) -> None:
        self.__statement = statement

    def query(self, query: str, parameters: None | tuple):
        """
        Preparing the SQL query that is going to be handled by the database handler
        """
        self.setStatement(self.getDatabaseHandler().cursor(prepared=True))


# Instantiating the application
Application = Flask(__name__)
# Configuring the application for using sessions
Application.secret_key = Environment.SESSION_KEY
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
    media = Media(data["Media"]["search"], None)
    return_data = media.verifyUniformResourceLocator()
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
                "artist": session["Media"]["YouTube"]["artist"],
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
        media = Media(data["Media"]["uniform_resource_locator"], referer)
        headers = {
            "Content-Type": "application/json",
        }
