from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from Classes.Media import Media
from mysql.connector.types import RowType
import inspect
import time
import json
import logging
import datetime
import sys
import os


sys.path.append(os.getcwd())
from Models.DatabaseHandler import Database_Handler
from Models.Logger import Extractio_Logger
from Environment import Environment


class Crawler:
    """
    It is a web-scrapper meant to scrape analytical data to be
    process later on.
    """
    __driver: WebDriver
    """
    Controls the ChromeDriver and allows you to drive the
    browser.
    """
    __data: list[dict[str, str | int | None]]
    """
    The data from the cache data.
    """
    __directory: str
    """
    The directory of the metadata files.
    """
    __files: list[str]
    """
    The files that are inside of the directory.
    """
    __html_tags: list[WebElement]
    """
    A list of HTML tags which are pieces of markup language
    used to indicate the beginning and end of an HTML element in
    an HTML document.
    """
    __html_tag: WebElement
    """
    An HTML tag which is pieces of markup language used to
    indicate the beginning and end of an HTML element in an HTML
    document.
    """
    __services: Service
    """
    It is responsible for controlling of chromedriver.
    """
    __options: Options
    """
    It is responsible for setting the options for the webdriver.
    """
    __database_handler: Database_Handler
    """
    The database handler that will communicate with the database
    server.
    """
    __Media: Media
    """
    It allows the application to manage the media.
    """
    __logger: Extractio_Logger
    """
    The logger that will all the action of the application.
    """

    def __init__(self) -> None:
        """
        Initializing the crawler to scrape the data needed.
        """
        ENV = Environment()
        self.setLogger(Extractio_Logger())
        self.getLogger().setLogger(logging.getLogger(__name__))
        self.getLogger().getLogger().setLevel(logging.DEBUG)
        self.__setServices()
        self.__setOptions()
        self.setDriver(webdriver.Chrome(self.getOption(), self.getService()))
        self.setDirectory(
            f"{ENV.getDirectory()}/Cache/Trend/"
        )
        self.setDatabaseHandler(Database_Handler())
        self.setData([])
        self.setUpData()

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

    def getMedia(self) -> Media:
        return self.__Media

    def setMedia(self, media: Media) -> None:
        self.__Media = media

    def getLogger(self) -> Extractio_Logger:
        return self.__logger

    def setLogger(self, logger: Extractio_Logger) -> None:
        self.__logger = logger

    def __setServices(self) -> None:
        """
        Setting the services for the ChromeDriver.

        Return:
            (void)
        """
        self.setService(Service(ChromeDriverManager().install()))
        self.getLogger().inform("The Crawler's Service has been installed!")

    def __setOptions(self) -> None:
        """
        Setting the options for the ChromeDriver.

        Return:
            (void)
        """
        self.setOption(Options())
        self.getOption().add_argument('--headless')
        self.getOption().add_argument('--no-sandbox')
        self.getOption().add_argument('--disable-dev-shm-usage')
        self.getLogger().inform("The Crawler has been configured!")

    def setUpData(self) -> None:
        """
        Setting up the data to be used to be used by the web
        crawler.

        Return:
            (void)
        """
        identifiers = self.getDatabaseHandler().getData(
            parameters=None,
            table_name="MediaFile",
            filter_condition="date_downloaded >= NOW() - INTERVAL 1 WEEK",
            column_names="DISTINCT YouTube"
        )
        dataset = self.getData()
        referrer = inspect.stack()[1][3]
        if referrer == "__init__" and self.prepareFirstRun(identifiers) > 0:
            self.getLogger().inform(
                f"Data has been successfully retrieved from the database server.\nWeekly Content Downloaded Amount: {self.prepareFirstRun(identifiers)}\n"
            )
            self.firstRun()
        elif referrer == "firstRun" and self.prepareSecondRun(dataset) > 0:
            self.getLogger().inform(
                f"Latest Content to be displayed on the application.\nNew Content Amount: {self.prepareSecondRun(dataset)}"
            )
            self.secondRun()
        else:
            self.getLogger().inform(
                f"No new data has been found for the last seven days.\nWeekly Content Downloaded Amount: {len(identifiers)}"
            )
            exit()

    def prepareSecondRun(self, dataset: list[dict[str, str | int | None]]) -> int:
        """
        Preparing for the second run of crawling based on the data
        in the cache.

        Return:
            (void)
        """
        new_dataset: list[str] = []
        data: dict[str, str | None] = {}
        self.setData([])
        for index in range(0, len(dataset), 1):
            new_dataset.append(str(dataset[index]["author_channel"]))
        new_dataset = list(set(new_dataset))
        for index in range(0, len(new_dataset), 1):
            data = {
                "author_channel": new_dataset[index],
                "latest_content": None
            }
            self.getData().append(data)  # type: ignore
        return len(self.getData())

    def secondRun(self):
        """
        The second run for the web-crawler to seek for the data
        needed from the targets.

        Return:
            (void)
        """
        delay: float = 0.0
        total: int = 0
        for index in range(0, len(self.getData()), 1):
            total += len(str(self.getData()[index]["author_channel"]))
        delay = ((total / len(self.getData())) / (40 * 5)) * 60
        self.getLogger().debug(
            f"The delay has been calculated!\nDelay: {delay} s"
        )
        for index in range(0, len(self.getData()), 1):
            self.enterTarget(
                str(self.getData()[index]["author_channel"]),
                delay,
                index
            )
        self.buildData()

    def buildData(self) -> None:
        """
        Building the data to be displayed to the user.

        Return:
            (void)
        """
        new_data: list[dict[str, str | int | None]] = []
        data: dict[str, str | int | None]
        for index in range(0, len(self.getData()), 1):
            self.getLogger().inform(
                f"The latest content from YouTube has been retrieved according the usage of the users!\nLatest Content: {self.getData()[index]['latest_content']}"
            )
            self.setMedia(
                Media(
                    str(self.getData()[index]["latest_content"]),
                    "youtube"
                )
            )
            response = self.getMedia().verifyPlatform()
            data = response["data"]["data"]  # type: ignore
            new_data.append(data)
        self.setData(new_data)
        self.save()

    def save(self) -> None:
        """
        Saving the data.

        Return:
            void
        """
        timestamp = int(time.time())
        file_name = f"{self.getDirectory()}{timestamp}.json"
        file = open(file_name, "w")
        file.write(json.dumps(self.getData(), indent=4))
        file.close()
        self.getLogger().inform(
            f"The latest content has been saved!\nFile Name: {file_name}"
        )
        self.getDriver().quit()

    def prepareFirstRun(self, identifiers: list[RowType]) -> int:
        """
        Setting up the data for the first run.

        Parameters:
            identifiers:    (array):    The result set of the identifiers for the last weeks.

        Return:
            (int)
        """
        self.setData([])
        for index in range(0, len(identifiers), 1):
            data = self.getDatabaseHandler().get_data(
                parameters=identifiers[index],
                table_name="YouTube",
                join_condition="Media ON YouTube.Media = Media.identifier",
                filter_condition="YouTube.identifier = %s",
                column_names="YouTube.identifier AS identifier, YouTube.author AS author, Media.value AS platform"
            )[0]
            uniform_resource_locator = self.verifyPlatform(data)
            metadata: dict[str, str | int | None] = {
                "identifier": str(data[0]),
                "author": str(data[1]),
                "uniform_resource_locator": uniform_resource_locator,
                "author_channel": None
            }
            self.getData().append(metadata)
        return len(self.getData())

    def verifyPlatform(self, data: RowType) -> str:
        """
        Veryfing the platform of the metadata to be able to generate
        its correct uniform resource locator.

        Parameters:
            data:   (array):    The record of a metadata.

        Return:
            (string)
        """
        response: str
        if data[2] == "youtube" or data[2] == "youtu.be":
            response = f"https://www.youtube.com/watch?v={data[0]}"
        else:
            response = ""
        return response

    def firstRun(self) -> None:
        """
        Preparing for the first run of crawling based on the data in
        the cache.

        Return:
            (void)
        """
        delay: float = 0.0
        total: int = 0
        for index in range(0, len(self.getData()), 1):
            total += len(
                str(self.getData()[index]["uniform_resource_locator"])
            )
        delay = ((total / len(self.getData())) / (40 * 5)) * 60
        self.getLogger().inform(
            f"The delay has been calculated for the Crawler to process the data.\nDelay: {delay} s"
        )
        for index in range(0, len(self.getData()), 1):
            self.enterTarget(
                str(self.getData()[index]["uniform_resource_locator"]),
                delay,
                index
            )
        self.setUpData()

    def enterTarget(self, target: str, delay: float, index: int = 0) -> None:
        """
        Entering the targeted page.

        Parameters:
            target: (string):   The uniform resource locator of the targeted page.
            delay:  (float):    The amount of time that the Crawler will wait which is based on the average typing speed of a person
            index:  (int):      The identifier of the data.

        Return:
            (void)
        """
        referrer = inspect.stack()[1][3]
        if referrer == "firstRun":
            self.getLogger().inform(
                f"Entering the target!\nTarget: {target}"
            )
            self.getDriver().get(target)
            time.sleep(delay)
        elif referrer == "secondRun":
            self.getLogger().inform(
                f"Entering the target!\nTarget: {target}/videos"
            )
            self.getDriver().get(f"{target}/videos")
            time.sleep(delay)
        self.retrieveData(referrer, index)

    def retrieveData(self, referrer: str, index: int = 0) -> None:
        """
        Retrieving the data needed from the target page.

        Parameters:
            referrer:   (string):   Referrer of the function.
            index:      (int):      The identifier of the data.

        Return:
            (void )
        """
        if referrer == "firstRun":
            self.getData()[index]["author_channel"] = self.getDriver().find_element(
                By.XPATH,
                '//*[@id="text"]/a').get_attribute("href")
        elif referrer == "secondRun":
            self.setHtmlTags(
                self.getDriver().find_elements(
                    By.XPATH,
                    '//a[@id="thumbnail"]'
                )
            )
            self.getData()[index]["latest_content"] = str(
                self.getHtmlTags()[2].get_attribute("href")
            )
