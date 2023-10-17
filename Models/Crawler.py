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
        print(self.getData())
        # self.__buildData()

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
