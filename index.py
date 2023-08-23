# Importing the requirements for the application
from flask import Flask, Response, render_template, jsonify, request, session
from datetime import date
import time
import os
import json
from pytube import YouTube
from SessionManagementSystem import Session_Manager
from ObjectRelationalMapper import Object_Relational_Mapper
from Media import Media


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
