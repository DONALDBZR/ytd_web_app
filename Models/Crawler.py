from datetime import datetime
from io import TextIOWrapper
from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from mysql.connector.pooling import PooledMySQLConnection
from mysql.connector.connection import MySQLConnection
from mysql.connector.cursor import MySQLCursor
from pytube import YouTube, StreamQuery, Stream
import shutil
import inspect
import re
import os
import time
import json
import mysql.connector
import sys

root_directory = f"{os.getcwd()}"
sys.path.insert(0, root_directory)

from Environment import Environment


class Database_Handler:
    """
    The database handler that will communicate with the database
    server.
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
    The password that allows the required user to connect to the
    database.

    Type: string
    visibility: private
    """
    __database_handler: "PooledMySQLConnection | MySQLConnection"
    """
    The database handler needed to execute the queries needed

    Type: PooledMySQLConnection | MySQLConnection
    visibility: private
    """
    __statement: "MySQLCursor"
    """
    The statement to be used to execute all of the requests to
    the database server

    Type: MySQLCursor
    visibility: private
    """
    __query: str
    """
    The query to be used to be sent to the database server to
    either get, post, update or delete data.

    Type: string
    Visibility: private
    """
    __parameters: tuple | None
    """
    Parameters that the will be used to sanitize the query which
    is either  get, post, update or delete.

    Type: array|null
    Visibility: private
    """

    def __init__(self):
        """
        Instantiating the class which will try to connect to the
        database.
        """
        self.__setHost(Environment.HOST)
        self.__setDatabase(Environment.DATABASE)
        self.__setUsername(Environment.USERNAME)
        self.__setPassword(Environment.PASSWORD)
        try:
            self.__setDatabaseHandler(mysql.connector.connect(host=self.__getHost(
            ), database=self.__getDatabase(), username=self.__getUsername(), password=self.__getPassword()))
        except mysql.connector.Error as error:
            print("Connection Failed: " + str(error))

    def __getHost(self) -> str:
        return self.__host

    def __setHost(self, host: str) -> None:
        self.__host = host

    def __getDatabase(self) -> str:
        return self.__database

    def __setDatabase(self, database: str) -> None:
        self.__database = database

    def __getUsername(self) -> str:
        return self.__username

    def __setUsername(self, username: str) -> None:
        self.__username = username

    def __getPassword(self) -> str:
        return self.__password

    def __setPassword(self, password: str) -> None:
        self.__password = password

    def __getDatabaseHandler(self) -> "PooledMySQLConnection | MySQLConnection":
        return self.__database_handler

    def __setDatabaseHandler(self, database_handler: "PooledMySQLConnection | MySQLConnection") -> None:
        self.__database_handler = database_handler

    def __getStatement(self) -> "MySQLCursor":
        return self.__statement

    def __setStatement(self, statement: "MySQLCursor") -> None:
        self.__statement = statement

    def getQuery(self) -> str:
        return self.__query

    def setQuery(self, query: str) -> None:
        self.__query = query

    def getParameters(self) -> tuple | None:
        return self.__parameters

    def setParameters(self, parameters: tuple | None) -> None:
        self.__parameters = parameters

    def _query(self, query: str, parameters: None | tuple):
        """
        Preparing the SQL query that is going to be handled by the
        database handler.

        Returns: Generator[MySQLCursor, None, None] | None
        """
        self.__setStatement(self.__getDatabaseHandler().cursor(prepared=True))
        self.__getStatement().execute(query, parameters)

    def _execute(self) -> None:
        """
        Executing the SQL query which will send a command to the
        database server

        Returns: None
        """
        self.__getDatabaseHandler().commit()

    def _resultSet(self) -> list:
        """
        Fetching all the data that is requested from the command that
        was sent to the database server

        Returns: array
        """
        result_set = self.__getStatement().fetchall()
        self.__getStatement().close()
        return result_set

    def get_data(self, parameters: tuple | None, table_name: str, join_condition: str = "", filter_condition: str = "", column_names: str = "*", sort_condition: str = "", limit_condition: int = 0) -> list[tuple]:
        """
        Retrieving data from the database.

        Parameters:
            parameters:         array|null: The parameters to be passed into the query.
            table_name:         string:     The name of the table.
            column_names:       string:     The name of the columns.
            join_condition      string:     Joining table condition.
            filter_condition    string:     Items to be filtered with.
            sort_condition      string:     The items to be sorted.
            limit_condition     int:     The amount of items to be returned

        Returns: array
        """
        query = f"SELECT {column_names} FROM {table_name}"
        self.setQuery(query)
        self.setParameters(parameters)
        self._get_join(join_condition)
        self._get_filter(filter_condition)
        self._get_sort(sort_condition)
        self._get_limit(limit_condition)
        self._query(self.getQuery(), self.getParameters())
        return self._resultSet()

    def _get_join(self, condition: str) -> None:
        """
        Building the query needed for retrieving data that is in at
        least two tables.

        Parameters:
            condition:  string: The JOIN statement that is used.

        Returns: void
        """
        if condition == "":
            query = self.getQuery()
        else:
            query = f"{self.getQuery()} LEFT JOIN {condition}"
        self.setQuery(query)

    def _get_filter(self, condition: str) -> None:
        """
        Building the query needed for retrieving specific data.

        Parameters:
            condition:  string: The WHERE statement that will be used.

        Returns: void
        """
        if condition == "":
            query = self.getQuery()
        else:
            query = f"{self.getQuery()} WHERE {condition}"
        self.setQuery(query)

    def _get_sort(self, condition: str) -> None:
        """
        Building the query needed to be used to sort the result set.

        Parameters:
            condition:  string: The ORDER BY statement that will be used.

        Returns: void
        """
        if condition == "":
            query = self.getQuery()
        else:
            query = f"{self.getQuery()} ORDER BY {condition}"
        self.setQuery(query)

    def _get_limit(self, limit: int) -> None:
        """
        Building the query needed to be used to limit the amount of
        data from the result set.

        Parameters:
            limit:  int: The ORDER BY statement that will be used.

        Returns: void
        """
        if limit > 0:
            query = f"{self.getQuery()} LIMIT {limit}"
        else:
            query = self.getQuery()
        self.setQuery(query)

    def post_data(self, table: str, columns: str, values: str, parameters: tuple) -> None:
        """
        Creating records to store data into the database server.

        Parameters:
            table:      string: Table Name
            columns:    string: Column names
            values:     string: Data to be inserted

        Returns: void
        """
        query = f"INSERT INTO {table}({columns}) VALUES ({values})"
        self.setQuery(query)
        self.setParameters(parameters)
        self._query(self.getQuery(), self.getParameters())
        self._execute()

    def update_data(self, table: str, values: str, parameters: tuple | None, condition: str = "") -> None:
        """
        Updating a specific table in the database.

        Parameters:
            table:      string: Table
            values:     string: Columns to be modified and data to be put within
            condition:  string: Condition for the data to be modified
            parameters: array:  Data to be used for data manipulation.

        Returns: void
        """
        query = f"UPDATE {table} SET {values}"
        self.setQuery(query)
        self.setParameters(parameters)
        self._get_filter(condition)
        self._query(self.getQuery(), self.getParameters())
        self._execute()

    def delete_data(self, table: str, parameters: tuple | None, condition: str = "") -> None:
        """
        Deleting data from the database.

        Parameters:
            table:      string: Table
            parameters: array:  Data to be used for data manipulation.
            condition:  string: Specification

        Returns: void
        """
        query = f"DELETE FROM {table}"
        self.setQuery(query)
        self.setParameters(parameters)
        self._get_filter(condition)
        self._query(self.getQuery(), self.getParameters())
        self._execute()

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
    _YouTubeDownloader: "YouTube_Downloader"
    """
    It will handle every operations related to YouTube.

    Type: YouTube_Downloader
    Visibility: protected
    """
    __database_handler: "Database_Handler"
    """
    It is the object relational mapper that will be used to
    simplify the process to entering queries.

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
    The value of the required media which have to correspond to
    the name of the platform from which the media comes from.

    Type: string | null
    Visibility: private
    """
    __timestamp: str
    """
    The timestamp at which the session has been created

    Type: string
    Visibility: private
    """
    __directory: str
    """
    The directory of the JSON files

    Type: string
    Visibility: private
    """
    __metadata_media_files: list[str]
    """
    The metadata of the media content that is stored in the
    document database.

    Type: array
    Visibility: private
    """
    __media_files: list[str]
    """
    The media content that is stored in the document database.

    Type: array
    Visibility: private
    """

    def __init__(self, search: str, value: str) -> None:
        """
        Instantiating the media's manager which will interact with
        the media's dataset and do the required processing.

        Parameters:
            search: string: The uniform resource locator to be searched.
            value:  string: The value of the required media which have to correspond to the name of the platform from which the media comes from.

        Returns:    void
        """
        self.__server()
        self.setDirectory(f"{self.getDirectory()}/Cache/Media")
        self.setDatabaseHandler(Database_Handler())
        self.getDatabaseHandler()._query("CREATE TABLE IF NOT EXISTS `Media` (identifier INT PRIMARY KEY AUTO_INCREMENT, `value` VARCHAR(8))", None)
        self.getDatabaseHandler()._execute()
        self.__maintain()
        self.setSearch(search)
        self.setValue(value)

    def getSearch(self) -> str:
        return self.__search

    def setSearch(self, search: str) -> None:
        self.__search = search

    def getDatabaseHandler(self) -> "Database_Handler":
        return self.__database_handler

    def setDatabaseHandler(self, database_handler: "Database_Handler") -> None:
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

    def getDirectory(self) -> str:
        return self.__directory

    def setDirectory(self, directory: str) -> None:
        self.__directory = directory

    def getMetadataMediaFiles(self) -> list[str]:
        return self.__metadata_media_files

    def setMetadataMediaFiles(self, metadata_media_files: list[str]) -> None:
        self.__metadata_media_files = metadata_media_files

    def getMediaFiles(self) -> list[str]:
        return self.__media_files

    def setMediaFiles(self, media_files: list[str]) -> None:
        self.__media_files = media_files

    def __server(self) -> None:
        """
        Setting the directory for the application.

        Returns: void
        """
        self.setDirectory(os.getcwd())

    def __maintain(self) -> None:
        """
        Maintaining the document database by doing some regular
        checks on the the metadata and media files.

        Returns: void
        """
        self.setMetadataMediaFiles(os.listdir(self.getDirectory()))
        audio_media_files_directory = f"{self.getDirectory()}/../../Public/Audio"
        video_media_files_directory = f"{self.getDirectory()}/../../Public/Video"
        audio_media_files = os.listdir(audio_media_files_directory)
        video_media_files = os.listdir(video_media_files_directory)
        destination_directory = f"{self.getDirectory()}/../../Public/{int(time.time())}"
        self.optimizeDirectory(audio_media_files, audio_media_files_directory, destination_directory)
        self.optimizeDirectory(video_media_files, video_media_files_directory, destination_directory)
        self.deleteMetadata()

    def deleteMetadata(self) -> None:
        """
        Iterate throughout the metadata to delete them from the
        cache database.

        Returns: void
        """
        # Iterating throughout the metadata to check that the metadata is old enough to remove from the cache.
        for index in range(0, len(self.getMetadataMediaFiles()), 1):
            file_name = f"{self.getDirectory()}/{self.getMetadataMediaFiles()[index]}"
            age = int(time.time()) - int(os.path.getctime(file_name))
            self.deleteOldMetadata(age, file_name)

    def deleteOldMetadata(self, age: int, file_name: str) -> None:
        """
        Deleting the metadata in the condition that the metadata is
        at least three days old.

        Parameters:
            age:        int:    The age of the metadata.
            file_name:  string: The name of the file.

        Returns: void
        """
        # Ensuring that the metadata file is at least three days old to be removed from the database.
        if age > 259200:
            os.remove(file_name)

    def optimizeDirectory(self, media_files: list[str], original_directory: str, new_directory: str) -> None:
        """
        Optimizing the directory by iterating throughout the media
        files that are in the directory to remove them from the
        application to be backed up else where.

        Parameters:
            media_files:        array:  The media files in the original directory.
            original_directory: string: The directory where the media files are hosted.
            new_directory:      string: The directory where the media files will be moved.

        Returns: void
        """
        # Iterating throughout the audio media files to restructure all the media files from the original directory.
        for index in range(0, len(media_files), 1):
            original_file = f"{original_directory}/{media_files[index]}"
            age = int(time.time()) - int(os.path.getctime(original_file))
            self.removeOldFile(original_file, media_files[index], new_directory, age)

    def removeOldFile(self, original_file: str, media_file: str, destination_directory: str, age: int) -> None:
        """
        Removing the file that is three days old.

        Parameters:
            original_file:          string: The path of the original file.
            media_file:             string: The media file.
            destination_directory:  string: The directory where the mediafile will be moved.
            age:                    int:    Age of the media file.

        Returns: void
        """
        # Ensuring that the audio file is at most three days old to make a backup of it from the server.
        if age > 259200:
            os.mkdir(destination_directory)
            new_file = f"{destination_directory}/{self.setNewFile(media_file)}"
            self.removeFile(original_file, new_file)

    def setNewFile(self, media_file: str) -> str:
        """
        Setting the new path for the media file.

        Parameters:
            media_file: string: The media file.

        Returns: string
        """
        # Verifying that the file type of the media file.
        if ".mp3" in media_file:
            identifier: str = media_file.replace(".mp3", "")
            parameters = tuple([identifier])
            metadata = self.getDatabaseHandler().get_data(table_name="YouTube", filter_condition="identifier = %s", parameters=parameters)[0]
            new_file = f"{metadata[4]}.mp3"
        else:
            identifier: str = media_file.replace(".mp4", "")
            parameters = tuple([identifier])
            metadata = self.getDatabaseHandler().get_data(table_name="YouTube", filter_condition="identifier = %s",parameters=parameters)[0]
            new_file = f"{metadata[4]}.mp4"
        return new_file

    def removeFile(self, original_file: str, new_file: str) -> None:
        """
        Removing the file from the hosting directory.

        Parameters:
            original_file:  string: The path of the original file.
            new_file:       string: The path of the new file.

        Returns: void
        """
        # Ensuring that the file does not exist to copy it
        if os.path.exists(new_file) == False:
            shutil.copyfile(original_file, new_file)
            os.remove(original_file)

    def verifyPlatform(self) -> dict[str, int | dict[str, str | int | None]]:
        """
        Verifying the uniform resource locator in order to switch to
        the correct system as well as select and return the correct
        response.

        Returns: object
        """
        response: dict[str, int | dict[str, str | int | None]]
        media = self.getMedia()
        # Verifying that the media does not exist to create one.
        if media["status"] != 200:
            self.postMedia()
            self.verifyPlatform()
        else:
            self.setIdentifier(media["data"][0][0])
        # Verifying the platform data to redirect to the correct system.
        if "youtube" in self.getValue() or "youtu.be" in self.getValue():
            response = {
                "status": 200,
                "data": self.handleYouTube()
            }
        return response  # type: ignore

    def getMedia(self) -> dict:
        """
        Retrieving the Media data from the Media table.

        Returns: object
        """
        media = self.getDatabaseHandler().get_data(tuple([self.getValue()]), "Media", filter_condition="value = %s")
        self.setTimestamp(datetime.now().strftime("%Y-%m-%d - %H:%M:%S"))
        response = {}
        if len(media) == 0:
            response = {
                'status': 404,
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

    def handleYouTube(self) -> dict[str, str | int | None]:
        """
        Handling the data throughout the You Tube Downloader which
        will depend on the referer.

        Returns: object
        """
        response: dict[str, str | int | None]
        identifier: str
        self._YouTubeDownloader = YouTube_Downloader(self.getSearch(), self.getIdentifier())
        youtube = self._YouTubeDownloader.search()
        media = {
            "Media": {
                "YouTube": youtube
            }
        }
        if "youtube" in self.getSearch():
            identifier = self.getSearch().replace("https://www.youtube.com/watch?v=", "")
        else:
            identifier = self.getSearch().replace("https://youtu.be/", "").rsplit("?")[0]
        filename = f"{self.getDirectory()}/{identifier}.json"
        file = open(filename, "w")
        file.write(json.dumps(media, indent=4))
        file.close()
        response = {
            "status": 200,
            "data": youtube # type: ignore
        }
        return response

    def metadataDirectory(self):
        """
        Creating the metadata directory

        Returns: void
        """
        if not os.path.exists(self.getDirectory()):
            os.makedirs(self.getDirectory())


class YouTube_Downloader:
    """
    It will handle every operations related to YouTube.
    """
    __uniform_resource_locator: str
    """
    The uniform resource locator to be searched.

    Type: string
    Visibility: private
    """
    __video: "YouTube"
    """
    Core developer interface for pytube.

    Type: YouTube
    Visibility: private
    """
    __title: str
    """
    The title of the video.

    Type: string
    Visibility: private
    """
    __identifier: str
    """
    The identifier of the video.

    Type: string
    Visibility: private
    """
    __length: int
    """
    The length of the video in seconds.

    Type: int
    Visibility: private
    """
    __duration: str
    """
    The duration of the video in the format of HH:mm:ss.

    Type: string
    Visibility: private
    """
    __published_at: str | datetime | None
    """
    The date at which the video has been published.

    Type: string
    Visibility: private
    """
    __database_handler: "Database_Handler"
    """
    It is the object relational mapper that will be used to
    simplify the process to entering queries.

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
    __directory: str
    """
    The directory of the media files.

    Type: string
    Visibility: private
    """

    def __init__(self, uniform_resource_locator: str, media_identifier: int):
        """
        Instantiating the class and launching the operations needed.

        Parameters:
            uniform_resource_locator:   string: The uniform resource locator to be searched.
            media_identifier:           int:    The media type for the system.
        """
        self.setDatabaseHandler(Database_Handler())
        self.getDatabaseHandler()._query("CREATE TABLE IF NOT EXISTS `YouTube` (identifier VARCHAR(16) PRIMARY KEY, `length` INT, published_at VARCHAR(32), author VARCHAR(64), title VARCHAR(128), `Media` INT, CONSTRAINT fk_Media_type FOREIGN KEY (`Media`) REFERENCES `Media` (identifier))", None)
        self.getDatabaseHandler()._execute()
        self.setUniformResourceLocator(uniform_resource_locator)
        self.setMediaIdentifier(media_identifier)

    def getUniformResourceLocator(self) -> str:
        return self.__uniform_resource_locator

    def setUniformResourceLocator(self, uniform_resource_locator: str) -> None:
        self.__uniform_resource_locator = uniform_resource_locator

    def getVideo(self) -> "YouTube":
        return self.__video

    def setVideo(self, video: "YouTube") -> None:
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

    def getPublishedAt(self) -> str | datetime | None:
        return self.__published_at

    def setPublishedAt(self, published_at: str | datetime | None) -> None:
        self.__published_at = str(published_at)

    def getDatabaseHandler(self) -> "Database_Handler":
        return self.__database_handler

    def setDatabaseHandler(self, database_handler: "Database_Handler") -> None:
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

    def getDirectory(self) -> str:
        return self.__directory

    def setDirectory(self, directory: str) -> None:
        self.__directory = directory

    def search(self) -> dict[str, str | int | None]:
        """
        Searching for the video in YouTube.

        Returns: object
        """
        self.setVideo(YouTube(self.getUniformResourceLocator()))
        self.setIdentifier(self.getUniformResourceLocator())
        if "youtube" in self.getUniformResourceLocator():
            self.setIdentifier(self.getIdentifier().replace("https://www.youtube.com/watch?v=", ""))
        else:
            self.setIdentifier(self.getIdentifier().replace("https://youtu.be/", "").rsplit("?")[0])
        response: dict[str, str | int | None]
        meta_data = self.getYouTube()
        audio_file: str | None
        video_file: str | None
        # Verifying the response of the metadata to retrieve the needed response
        if meta_data["status"] == 200:
            self.setLength(int(meta_data["data"][0][4]))  # type: ignore
            self.setPublishedAt(str(meta_data["data"][0][3]))  # type: ignore
            self.setAuthor(str(meta_data["data"][0][0]))  # type: ignore
            self.setTitle(str(meta_data["data"][0][1]))  # type: ignore
            self.setDuration(time.strftime("%H:%M:%S", time.gmtime(self.getLength())))
            # Verifying base on the length to set the file location
            if len(list(meta_data["data"])) == 2:  # type: ignore
                audio_file = str(meta_data["data"][0][5])  # type: ignore
                video_file = str(meta_data["data"][1][5])  # type: ignore
            else:
                audio_file = None
                video_file = None
        else:
            self.setLength(self.getVideo().length)
            self.setPublishedAt(self.getVideo().publish_date)
            self.setAuthor(self.getVideo().author)
            self.setTitle(self.getVideo().title)
            self.setDuration(time.strftime("%H:%M:%S", time.gmtime(self.getLength())))
            audio_file = None
            video_file = None
            self.postYouTube()
        response = {
            "uniform_resource_locator": self.getUniformResourceLocator(),
            "author": self.getAuthor(),
            "title": self.getTitle(),
            "identifier": self.getIdentifier(),
            "author_channel": self.getVideo().channel_url,
            "views": self.getVideo().views,
            "published_at": self.getPublishedAt(),  # type: ignore
            "thumbnail": self.getVideo().thumbnail_url,
            "duration": self.getDuration(),
            "audio_file": audio_file,
            "video_file": video_file
        }
        return response

    def getYouTube(self) -> dict[str, int | list[str | int] | str]:
        """
        Retrieving the metadata from the YouTube table.

        Returns: object
        """
        media = self.getDatabaseHandler().get_data(tuple([self.getIdentifier()]), "YouTube", "MediaFile ON MediaFile.YouTube = YouTube.identifier", "YouTube.identifier = %s", "author, title, YouTube.identifier, published_at, length, location", "MediaFile.identifier ASC", 2)
        self.setTimestamp(datetime.now().strftime("%Y-%m-%d - %H:%M:%S"))
        response: dict[str, int | list[str | int] | str]
        if len(media) == 0:
            response = {
                'status': 404,
                'data': media, # type: ignore
                'timestamp': self.getTimestamp()
            }
        else:
            response = {
                'status': 200,
                'data': media, # type: ignore
                'timestamp': self.getTimestamp()
            }
        return response

    def postYouTube(self) -> None:
        """
        Creating a record for the media with its data.

        Returns: void
        """
        self.getDatabaseHandler().post_data("YouTube", "identifier, length, published_at, author, title, Media", "%s, %s, %s, %s, %s, %s", (self.getIdentifier(), self.getLength(), self.getPublishedAt(), self.getAuthor(), self.getTitle(), self.getMediaIdentifier()))


class Crawler:
    """
    It is a web-scrapper meant to scrape analytical data to be
    process later on.
    """
    __driver: WebDriver
    """
    Controls the ChromeDriver and allows you to drive the
    browser.

    Type: WebDriver
    """
    __data: list[dict[str, str | int | None]]
    """
    The data from the cache data.

    Type: array
    """
    __directory: str
    """
    The directory of the metadata files.

    Type: string
    Visibility: private
    """
    __files: list[str]
    """
    The files that are inside of the directory.

    Type: array
    Visibility: private
    """
    __html_tags: list[WebElement]
    """
    A list of HTML tags which are pieces of markup language
    used to indicate the beginning and end of an HTML element in
    an HTML document.

    Type: array
    Visibility: private
    """
    __html_tag: WebElement
    """
    An HTML tag which is pieces of markup language used to
    indicate the beginning and end of an HTML element in an HTML
    document.

    Type: array
    Visibility: private
    """
    __services: Service
    """
    It is responsible for controlling of chromedriver.

    Type: Service
    Visibility: private
    """
    __options: Options
    """
    It is responsible for setting the options for the webdriver.

    Type: Options
    Visibility: private
    """
    __database_handler: Database_Handler
    """
    The database handler that will communicate with the database
    server.

    Type: Database_Handler
    Visibility: private
    """

    def __init__(self) -> None:
        """
        Initializing the crawler to scrape the data needed.

        Parameters:
            request:    object: The request data from the view.
        """
        self.__setServices()
        self.__setOptions()
        self.setDriver(webdriver.Chrome(self.getOption(), self.getService()))
        self.__server()
        self.setDirectory(f"{self.getDirectory()}/Cache/Media/")
        self.setDatabaseHandler(Database_Handler())
        self.setData([])
        self.__schedule()

    def getDriver(self) -> WebDriver:
        return self.__driver

    def setDriver(self, driver: WebDriver) -> None:
        self.__driver = driver

    def getData(self) -> list[dict[str, str | int | None]]:
        return self.__data

    def setData(self, data: list[dict[str, str | int | None]]) -> None:
        self.__data = data

    def getDirectory(self) -> str:
        return self.__directory

    def setDirectory(self, directory: str) -> None:
        self.__directory = directory

    def getFiles(self) -> list[str]:
        return self.__files

    def setFiles(self, files: list[str]) -> None:
        self.__files = files

    def getHtmlTags(self) -> list[WebElement]:
        return self.__html_tags

    def setHtmlTags(self, html_tags: list[WebElement]) -> None:
        self.__html_tags = html_tags

    def getHtmlTag(self) -> WebElement:
        return self.__html_tag

    def setHtmlTag(self, html_tag: WebElement) -> None:
        self.__html_tag = html_tag

    def getService(self) -> Service:
        return self.__services

    def setService(self, services: Service) -> None:
        self.__services = services

    def getOption(self) -> Options:
        return self.__options

    def setOption(self, options: Options) -> None:
        self.__options = options

    def getDatabaseHandler(self) -> Database_Handler:
        return self.__database_handler

    def setDatabaseHandler(self, database_handler: Database_Handler) -> None:
        self.__database_handler = database_handler

    def __server(self) -> None:
        """
        Setting the directory for the application.

        Returns: void
        """
        self.setDirectory(os.getcwd())

    def __setServices(self) -> None:
        """
        Setting the services for the ChromeDriver.

        Returns: void
        """
        self.setService(Service(ChromeDriverManager().install()))

    def __setOptions(self) -> None:
        """
        Setting the options for the ChromeDriver.

        Returns: void
        """
        self.setOption(Options())
        self.getOption().add_argument('--headless')
        self.getOption().add_argument('--no-sandbox')
        self.getOption().add_argument('--disable-dev-shm-usage')

    def __schedule(self) -> None:
        """
        Automating the web scrapper.

        Returns: void
        """
        trend_dataset: list[str] = os.listdir(f"{self.getDirectory()}../Trend")
        filename: int
        current_time: int = int(time.time())
        # Verifying that there is data.
        if len(trend_dataset) > 0:
            filename = int(trend_dataset[-1].replace(".json", ""))
            age = current_time - filename
            self.__verifyTrendAge(age)
        else:
            self.setUpData()

    def __verifyTrendAge(self, age: int) -> None:
        """
        Verifying the age of the trend.

        Parameters:
            age:    int:    The age of the trend

        Returns: void
        """
        # Ensuring the file is older than a week.
        if age > 604800:
            self.setUpData()

    def setUpData(self) -> None:
        """
        Setting up the data to be used to be used by the web
        crawler.

        Returns: void
        """
        identifiers: list[tuple[str]] = self.getDatabaseHandler().get_data(parameters=None, table_name="MediaFile", filter_condition="date_downloaded >= NOW() - INTERVAL 1 WEEK", column_names="DISTINCT YouTube") # type: ignore
        dataset: list[dict[str, str | int | None]] = self.getData() # type: ignore
        referrer = inspect.stack()[1][3]
        # Verifying the referrer to be able to select the action required.
        if referrer == "__schedule" and self.prepareFirstRun(identifiers) > 0:
            self.firstRun()
        elif referrer == "firstRun" and self.prepareSecondRun(dataset) > 0:
            self.secondRun()

    def prepareSecondRun(self, dataset: list[dict[str, str | int | None]]) -> int:
        """
        Preparing for the second run of crawling based on the data
        in the cache.

        Returns: void
        """
        new_dataset: list[str] = []
        data: dict[str, str | None] = {}
        self.setData([])
        # Iterating throughout the dataset to retrieve the author's channel's uniform resource locator.
        for index in range(0, len(dataset), 1):
            new_dataset.append(str(dataset[index]["author_channel"]))
        new_dataset = list(set(new_dataset))
        # Iterating throughout the dataset to set the latest content
        for index in range(0, len(new_dataset), 1):
            data = {
                "author_channel": new_dataset[index],
                "latest_content": None
            }
            self.getData().append(data) # type: ignore
        return len(self.getData());

    def refineData(self) -> None:
        """
        Refining the data when there is duplicate data.

        Returns: void
        """
        new_data: list[dict[str, str | int | float | None]] = []
        data: dict[str, str | int | float | None]
        crude_data = self.refineAndExtract()
        # Iterating throughout the artists, ratings and author channels to build the new data.
        for index in range(0, len(crude_data["authors"]), 1):
            data = {
                "author": crude_data["authors"][index],  # type: ignore
                "rating": crude_data["ratings"][
                    crude_data["authors"][index]],  # type: ignore
                "author_channel": crude_data["author_channels"][
                    crude_data["authors"][index]]  # type: ignore
            }
            new_data.append(data)
        self.setData(new_data)

    def refineAndExtract(self) -> dict[str, list[str] | dict[str, float] | dict[str, str]]:
        """
        Refining the rating and extracting the channels of the
        authors.

        Returns: object
        """
        ratings: dict[str, float] = {}
        author_channels: dict[str, str] = {}
        authors: list[str] = []
        # Iterating throughout the data to refine the rating and extract the channels of the authors
        for index in range(0, len(self.getData()), 1):
            author = str(self.getData()[index]["author"])  # type: ignore
            rating = float(self.getData()[index]["rating"])  # type: ignore
            # Verifying that the ratings and the author's channels are declared
            if author in ratings and author in author_channels:
                rating = (ratings[author] +
                          float(self.getData()[index]["rating"])) / 2  # type: ignore
            else:
                rating = float(self.getData()[index]["rating"])  # type: ignore
                author_channels[author] = str(
                    self.getData()[index]["author_channel"])
            ratings[author] = rating
            authors.append(author)
        authors = list(set(authors))
        return {
            "authors": authors,
            "author_channels": author_channels,
            "ratings": ratings
        }

    def secondRun(self):
        """
        The second run for the web-crawler to seek for the data
        needed from the targets.

        Returns: void
        """
        delay: float = 0.0
        total: int = 0
        # Iterating throughout the dataset to calculate delay between each run
        for index in range(0, len(self.getData()), 1):
            total += len(str(self.getData()[index]["author_channel"]))
        delay = ((total / len(self.getData())) / (40 * 5)) * 60
        # Iterating throughout the targets to run throughout them
        for index in range(0, len(self.getData()), 1):
            self.enterTarget(str(self.getData()[index]["author_channel"]), delay, index)
        # self.buildData()

    def __buildData(self) -> None:
        """
        Building the data to be displayed to the user.

        Returns: void
        """
        new_data: list[dict[str, str | int | None]] = []
        data: dict[str, str | int | None]
        request: dict[str, str | None]
        # Iterating throughout the data to get metadata.
        for index in range(0, len(self.getData()), 1):
            request = {
                "referer": None,
                "search": str(self.getData()[index]["latest_content"]),
                "platform": "youtube",
                "ip_address": "127.0.0.1",
                "port": self.getRequest()["port"]
            }
            self.setRequest(request)
            self.setMedia(Media(self.getRequest()))
            response = self.getMedia().verifyPlatform()
            data = response["data"]["data"]  # type: ignore
            new_data.append(data)
        self.setData(new_data)  # type: ignore
        self.save()

    def save(self) -> None:
        """
        Saving the data.

        Returns: void
        """
        timestamp = int(time.time())
        filename = f"{self.getDirectory()}../Trend/{timestamp}.json"
        file = open(filename, "w")
        file.write(json.dumps(self.getData(), indent=4))
        file.close()
        self.getDriver().quit()

    def prepareFirstRun(self, identifiers: list[tuple[str]]) -> int:
        """
        Setting up the data for the first run.

        Parameters:
            identifiers:    array:  The result set of the identifiers for the last weeks.

        Returns: int
        """
        self.setData([])
        # Iterating throughout the result set of the identifiers to retrieve the metadata needed
        for index in range(0, len(identifiers), 1):
            data: tuple[str, str, str] = self.getDatabaseHandler().get_data(parameters=identifiers[index], table_name="YouTube", join_condition="Media ON YouTube.Media = Media.identifier", filter_condition="YouTube.identifier = %s", column_names="YouTube.identifier AS identifier, YouTube.author AS author, Media.value AS platform")[0] # type: ignore
            uniform_resource_locator: str = self.verifyPlatform(data)
            metadata: dict[str, str | int | None] = {
                "identifier": data[0],
                "author": data[1],
                "uniform_resource_locator": uniform_resource_locator,
                "author_channel": None
            }
            self.getData().append(metadata)
        return len(self.getData())
    
    def verifyPlatform(self, data: tuple[str, str, str]) -> str: # type: ignore
        """
        Veryfing the platform of the metadata to be able to generate
        its correct uniform resource locator.

        Parameters:
            data:   array:  The record of a metadata.

        Returns:    string
        """
        if data[2] == "youtube" or data[2] == "youtu.be":
            return f"https://www.youtube.com/watch?v={data[0]}"

    def firstRun(self) -> None:
        """
        Preparing for the first run of crawling based on the data in
        the cache.

        Returns: void
        """
        delay: float = 0.0
        total: int = 0
        # Iterating throughout the dataset to calculate delay between each run
        for index in range(0, len(self.getData()), 1):
            total += len(str(self.getData()[index]["uniform_resource_locator"])) # type: ignore
        delay = ((total / len(self.getData())) / (40 * 5)) * 60
        # Iterating throughout the targets to run throughout them
        for index in range(0, len(self.getData()), 1):
            self.enterTarget(str(self.getData()[index]["uniform_resource_locator"]), delay, index) # type: ignore
        self.setUpData()

    def enterTarget(self, target: str, delay: float, index: int = 0) -> None:
        """
        Entering the targeted page.

        Parameters:
            target: string: The uniform resource locator of the targeted page.
            delay:  float:  The amount of time that the Crawler will wait which is based on the average typing speed of a [erspm/]
            index:  int:    The identifier of the data.

        Returns: void
        """
        referrer = inspect.stack()[1][3]
        # Verifying the run of the crawler
        if referrer == "firstRun":
            self.getDriver().get(target)
            time.sleep(delay)
        elif referrer == "secondRun":
            self.getDriver().get(f"{target}/videos")
            time.sleep(delay)
        self.retrieveData(referrer, index)

    def retrieveData(self, referrer: str, index: int = 0) -> None:
        """
        Retrieving the data needed from the target page.

        Parameters:
            referrer:   string: Referrer of the function.
            index:      int:    The identifier of the data.

        Returns: void 
        """
        author_channel: str = ""
        if referrer == "firstRun":
            self.getData()[index]["author_channel"] = self.getDriver().find_element(By.XPATH, '//*[@id="text"]/a').get_attribute("href") # type: ignore
        elif referrer == "secondRun":
            self.setHtmlTags(self.getDriver().find_elements(By.XPATH, '//a[@id="thumbnail"]'))
            self.getData()[index]["latest_content"] = str(self.getHtmlTags()[1].get_attribute("href"))
