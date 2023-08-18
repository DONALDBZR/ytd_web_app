# Importing the requirements for the application
from flask import Flask, Response, render_template, url_for, jsonify, request, session, redirect
from datetime import datetime, timedelta
import time
import os
import json
from Environment import Environment
from pytube import YouTube
import mysql.connector
from Session_Management_System import Session_Manager


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
    The http referrer which is the uniform resource locator that is needed to be able to allow the user to download the required media.

    Type: string|null
    Visibility: private
    """
    __database_handler: None
    """
    The database handler that will communicate with the database server.

    Type: Database_Handler
    Visibility: private
    """
    __identifier: int
    """
    The identifier of the required media

    Type: int
    Visibility: private
    """
    __value: str
    """
    The value of the required media which have to correspond to the name of the platform from which the media comes from.

    Type: string | null
    Visibility: private
    """
    __timestamp: str
    """
    The timestamp at which the session has been created

    Type: string
    Visibility: private
    """

    def __init__(self, search: str, referer: str | None, value: str) -> None:
        """
        Instantiating the media's manager which will interact with the media's dataset and do the required processing.

        Parameters:
            search: string: The uniform resource locator to be searched.
            referer: string | null: The http referrer which is the uniform resource locator that is needed to be able to allow the user to download the required media.
            value: string: The value of the required media which have to correspond to the name of the platform from which the media comes from.
        """
        self.setDatabaseHandler(Database_Handler())
        self.getDatabaseHandler().query(
            "CREATE TABLE IF NOT EXISTS `Media` (identifier INT PRIMARY KEY AUTO_INCREMENT, `value` VARCHAR(8))", None)
        self.getDatabaseHandler().execute()
        self.setSearch(search)
        self.setReferer(referer)
        self.setValue(value)

    def getSearch(self) -> str:
        return self.__search

    def setSearch(self, search: str) -> None:
        self.__search = search

    def getReferer(self) -> str | None:
        return self.__referer

    def setReferer(self, referer: str | None) -> None:
        self.__referer = referer

    def getDatabaseHandler(self):
        return self.__database_handler

    def setDatabaseHandler(self, database_handler) -> None:
        self.__database_handler = database_handler

    def getIdentifier(self) -> int:
        return self.__identifier

    def setIdentifier(self, identifier: int) -> None:
        self.__identifier = identifier

    def getValue(self) -> str:
        return self.__value

    def setValue(self, value: str) -> None:
        self.__value = value

    def getTimestamp(self) -> str:
        return self.__timestamp

    def setTimestamp(self, timestamp: str) -> None:
        self.__timestamp = timestamp

    def verifyPlatform(self) -> dict:
        """
        Verifying the uniform resource locator in order to switch to the correct system as well as select and return the correct response.

        Returns: object
        """
        response = {}
        media = self.getMedia()
        # Verifying that the media does not exist to create one.
        if media["status"] != 200:
            self.postMedia()
            self.verifyPlatform()
        else:
            self.setIdentifier(media["data"][0][0])
        # Verifying the platform data to redirecto to the correct system.
        if "youtube" in self.getValue():
            response = {
                "status": 200,
                "data": self.handleYouTube()
            }
        return response

    def getMedia(self) -> dict:
        """
        Retrieving the Media data from the Media table.

        Returns: object
        """
        self.getDatabaseHandler().query(
            "SELECT * FROM `Media` WHERE value = %s", (self.getValue(),))
        media = self.getDatabaseHandler().resultSet()
        self.setTimestamp(datetime.now().strftime("%Y-%m-%d - %H:%M:%S"))
        response = {}
        if len(media) == 0:
            response = {
                'status': 204,
                'data': media,
                'timestamp': self.getTimestamp()
            }
        else:
            response = {
                'status': 200,
                'data': media,
                'timestamp': self.getTimestamp()
            }
        return response

    def postMedia(self) -> None:
        """
        Creating a record for the media with its data.

        Returns: void
        """
        self.getDatabaseHandler().query(
            "INSERT INTO `Media` (`value`) VALUES (%s)", (self.getValue(),))
        self.getDatabaseHandler().execute()

    def handleYouTube(self) -> dict:
        """
        Handling the data throughout the You Tube Downloader which will depend on the referer.

        Returns: object
        """
        self._YouTubeDownloader = YouTube_Downloader(
            self.getSearch(), self.getIdentifier())
        response = {}
        # Verifying the referer to retrieve to required data
        if self.getReferer() is None:
            session["Media"] = {}
            session["Media"]["YouTube"] = self._YouTubeDownloader.search()
            filename = "./Cache/Session/Users/" + \
                session["Client"]["ip_address"] + ".json"
            file = open(filename, "w")
            file.write(json.dumps(session, indent=4))
            file.close()
            response = {
                "status": 200,
                "data": self._YouTubeDownloader.search()
            }
        return response


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
    __database_handler: None
    """
    The database handler that will communicate with the database server.

    Type: Database_Handler
    Visibility: private
    """
    __author: str
    """
    The author of the video/music.

    Type: string
    Visibility: private
    """
    __media_identifier: int
    """
    The media type for the system.

    Type: int
    Visibility: private
    """
    __timestamp: str
    """
    The timestamp at which the session has been created.

    Type: string
    Visibility: private
    """

    def __init__(self, uniform_resource_locator: str, media_identifier: int):
        """
        Instantiating the class and launching the operations needed

        Parameters:
            uniform_resource_locator: string: The uniform resource locator to be searched.
            media_identifier: int: The media type for the system. 
        """
        self.setDatabaseHandler(Database_Handler())
        self.getDatabaseHandler().query("CREATE TABLE IF NOT EXISTS `YouTube` (identifier VARCHAR(16) PRIMARY KEY, `length` INT, published_at VARCHAR(32), author VARCHAR(64), title VARCHAR(128), `Media` INT, CONSTRAINT fk_Media_type FOREIGN KEY (`Media`) REFERENCES `Media` (identifier))", None)
        self.getDatabaseHandler().execute()
        self.setUniformResourceLocator(uniform_resource_locator)
        self.setMediaIdentifier(media_identifier)

    def getUniformResourceLocator(self) -> str:
        return self.__uniform_resource_locator

    def setUniformResourceLocator(self, uniform_resource_locator: str) -> None:
        self.__uniform_resource_locator = uniform_resource_locator

    def getVideo(self) -> YouTube:
        return self.__video

    def setVideo(self, video: YouTube) -> None:
        self.__video = video

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

    def getDatabaseHandler(self):
        return self.__database_handler

    def setDatabaseHandler(self, database_handler) -> None:
        self.__database_handler = database_handler

    def getAuthor(self) -> str:
        return self.__author

    def setAuthor(self, author: str) -> None:
        self.__author = author

    def getMediaIdentifier(self) -> int:
        return self.__media_identifier

    def setMediaIdentifier(self, media_identifier: int) -> None:
        self.__media_identifier = media_identifier

    def getTimestamp(self) -> str:
        return self.__timestamp

    def setTimestamp(self, timestamp: str) -> None:
        self.__timestamp = timestamp

    def search(self) -> dict:
        """
        Searching for the video in YouTube.

        Returns: object
        """
        self.setVideo(YouTube(self.getUniformResourceLocator()))
        self.setIdentifier(self.getUniformResourceLocator())
        self.setIdentifier(self.getIdentifier().replace(
            "https://www.youtube.com/watch?v=", ""))
        meta_data = self.getYouTube()
        response = {}
        # Verifying the response of the metadata to retrieve the needed response
        if meta_data["status"] == 200:
            self.setLength(meta_data["data"][0][1])
            self.setPublishedAt(meta_data["data"][0][2])
            self.setAuthor(meta_data["data"][0][3])
            self.setTitle(meta_data["data"][0][4])
            self.setDuration(time.strftime(
                "%H:%M:%S", time.gmtime(self.getLength())))
        else:
            self.setLength(self.getVideo().length)
            self.setPublishedAt(self.getVideo().publish_date)
            self.setAuthor(self.getVideo().author)
            self.setTitle(self.getVideo().title)
            self.setDuration(time.strftime(
                "%H:%M:%S", time.gmtime(self.getLength())))
            self.postYouTube()
        response = {
            "uniform_resource_locator": self.getUniformResourceLocator(),
            "author": self.getAuthor(),
            "title": self.getTitle(),
            "identifier": self.getIdentifier(),
            "author_channel": self.getVideo().channel_url,
            "views": self.getVideo().views,
            "published_at": self.getPublishedAt(),
            "thumbnail": self.getVideo().thumbnail_url,
            "duration": self.getDuration()
        }
        return response

    def getYouTube(self) -> dict:
        """
        Retrieving the metadata from the YouTube table.

        Returns: object
        """
        self.getDatabaseHandler().query(
            "SELECT * FROM `YouTube` WHERE identifier = %s", (self.getIdentifier(),))
        media = self.getDatabaseHandler().resultSet()
        self.setTimestamp(datetime.now().strftime("%Y-%m-%d - %H:%M:%S"))
        response = {}
        if len(media) == 0:
            response = {
                'status': 204,
                'data': media,
                'timestamp': self.getTimestamp()
            }
        else:
            response = {
                'status': 200,
                'data': media,
                'timestamp': self.getTimestamp()
            }
        return response

    def postYouTube(self) -> None:
        """
        Creating a record for the media with its data.

        Returns: void
        """
        data = (self.getIdentifier(), self.getLength(), self.getPublishedAt(
        ), self.getAuthor(), self.getTitle(), self.getMediaIdentifier())
        self.getDatabaseHandler().query(
            "INSERT INTO `YouTube` (identifier, `length`, published_at, author, title, `Media`) VALUES (%s, %s, %s, %s, %s, %s)", data)
        self.getDatabaseHandler().execute()


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

        Returns: Generator[MySQLCursor, None, None] | None
        """
        self.setStatement(self.getDatabaseHandler().cursor(prepared=True))
        self.getStatement().execute(query, parameters)

    def execute(self) -> None:
        """
        Executing the SQL query which will send a command to the database server

        Returns: None
        """
        self.getDatabaseHandler().commit()

    def resultSet(self):
        """
        Fetching all the data that is requested from the command that was sent to the database server

        Returns: (Any | List[RowType])
        """
        return self.getStatement().fetchall()


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
