from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from Classes.Media import Media
from mysql.connector.types import RowType
from os import getcwd
from typing import List, Dict, Union, Tuple, cast
from logging import DEBUG
from inspect import stack
from time import time, sleep
from json import dumps
from sys import path
from bleach import clean
from urllib.parse import ParseResult, urlparse
from random import randint


path.append(getcwd())
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
    __data: List[Dict[str, Union[str, int, None]]]
    """
    The data from the cache data.
    """
    __directory: str
    """
    The directory of the metadata files.
    """
    __files: List[str]
    """
    The files that are inside of the directory.
    """
    __html_tags: List[WebElement]
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
        ENV: Environment = Environment()
        self.setLogger(Extractio_Logger(__name__))
        self.__setServices()
        self.__setOptions()
        self.setDriver(webdriver.Chrome(self.getOption(), self.getService()))
        self.setDirectory(f"{ENV.getDirectory()}/Cache/Trend/")
        self.setDatabaseHandler(Database_Handler())
        self.setData([])
        self.setUpData()

    def getDriver(self) -> WebDriver:
        return self.__driver

    def setDriver(self, driver: WebDriver) -> None:
        self.__driver = driver

    def getData(self) -> List[Dict[str, Union[str, int, None]]]:
        return self.__data

    def setData(self, data: List[Dict[str, Union[str, int, None]]]) -> None:
        self.__data = data

    def getDirectory(self) -> str:
        return self.__directory

    def setDirectory(self, directory: str) -> None:
        self.__directory = directory

    def getFiles(self) -> List[str]:
        return self.__files

    def setFiles(self, files: List[str]) -> None:
        self.__files = files

    def getHtmlTags(self) -> List[WebElement]:
        return self.__html_tags

    def setHtmlTags(self, html_tags: List[WebElement]) -> None:
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

        Returns:
            void
        """
        self.setService(Service(ChromeDriverManager().install()))
        self.getLogger().inform("The Crawler's Service has been installed!")

    def __setOptions(self) -> None:
        """
        Setting the options for the ChromeDriver.

        Returns:
            void
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

        Returns:
            void
        """
        identifiers: List[RowType] = self.getDatabaseHandler().getData(
            parameters=None,
            table_name="MediaFile",
            filter_condition="date_downloaded >= NOW() - INTERVAL 2 WEEK",
            column_names="YouTube",
            group_condition="YouTube"
        )
        dataset: List[Dict[str, Union[str, int, None]]] = self.getData()
        referrer: str = stack()[1][3]
        if referrer == "__init__":
            self.prepareFirstRun(identifiers)
        if referrer == "firstRun":
            self.prepareSecondRun(dataset)
        if referrer == "__init__" and len(self.getData()) > 0:
            self.getLogger().inform(f"Data has been successfully retrieved from the database server.\nWeekly Content Downloaded Amount: {len(self.getData())}\n")
            self.firstRun()
        if referrer == "firstRun" and len(self.getData()) > 0:
            self.getLogger().inform(f"Latest Content to be displayed on the application.\nNew Content Amount: {len(self.getData())}")
            self.secondRun()
        self.getLogger().inform(f"No new data has been found.\nWeekly Content Downloaded Amount: {len(identifiers)}")
        exit()

    def prepareSecondRun(self, dataset: list[dict[str, str | int | None]]) -> None:
        """
        Preparing for the second run of crawling based on the data
        in the cache.

        Returns:
            void
        """
        new_dataset: List[Dict[str, Union[str, None]]] = [{"author_channel": author_channel, "latest_content": None} for author_channel in list(set([str(media_metadata["author_channel"]) for media_metadata in dataset]))]
        self.setData(cast(List[Dict[str, Union[str, int, None]]], new_dataset))

    def secondRun(self) -> None:
        """
        Executing the second phase of the data retrieval process by
        iterating through stored data and processing each entry with
        an appropriate delay.

        Returns:
            void
        """
        for index in range(0, len(self.getData()), 1):
            delay: float = self.getDelay(str(self.getData()[index]["author_channel"]))
            self.getLogger().debug(f"The delay has been calculated for Crawler to process the data.\nDelay: {delay} s\nUniform Resource Locator: {str(self.getData()[index]['author_channel'])}")
            sleep(delay)
            self.enterTarget(str(self.getData()[index]["author_channel"]), delay, index)
        self.buildData()

    def buildData(self) -> None:
        """
        Building the data to be displayed to the user.

        Returns:
            void
        """
        new_data: List[Dict[str, Union[str, int, None]]] = []
        data: Dict[str, Union[str, int, None]]
        for index in range(0, len(self.getData()), 1):
            self.getLogger().inform(f"The latest content from YouTube has been retrieved according the usage of the users!\nLatest Content: {self.getData()[index]['latest_content']}")
            self.setMedia(Media(str(self.getData()[index]["latest_content"]), "youtube"))
            response: Union[Dict[str, Union[int, Dict[str, Union[int, Dict[str, Union[str, int, None]]]]]], Dict[str, Union[int, str]]] = self.getMedia().verifyPlatform()
            data: Dict[str, Union[str, int, None]] = response["data"]["data"]  # type: ignore
            new_data.append(data)
        self.setData(new_data)
        self.save()

    def save(self) -> None:
        """
        Saving the data.

        Returns:
            void
        """
        timestamp: int = int(time())
        file_name: str = f"{self.getDirectory()}{timestamp}.json"
        file = open(file_name, "w")
        file.write(dumps(self.getData(), indent=4))
        file.close()
        self.getLogger().inform(f"The latest content has been saved!\nFile Name: {file_name}")
        self.getDriver().quit()

    def prepareFirstRun(self, identifiers: Union[List[RowType], List[Dict[str, str]]]) -> None:
        """
        Setting up the data for the first run.

        Parameters:
            identifiers: [{YouTube: string}]: The result set of the identifiers for the last weeks.

        Returns:
            void
        """
        dataset: List[Dict[str, Union[str, int, None]]] = []
        for index in range(0, len(identifiers), 1):
            parameters: Tuple[str] = (str(identifiers[index]["YouTube"]),) # type: ignore
            data: Union[RowType, Dict[str, str]] = self.getDatabaseHandler().getData(
                parameters=parameters,
                table_name="YouTube",
                join_condition="Media ON YouTube.Media = Media.identifier",
                filter_condition="YouTube.identifier = %s",
                column_names="YouTube.identifier AS identifier, YouTube.author AS author, Media.value AS platform"
            )[0]
            uniform_resource_locator: str = f"https://www.youtube.com/watch?v={data['identifier']}" if str(data["platform"]) == "youtube" or str(data["platform"]) == "youtu.be" else "" # type: ignore
            metadata: Dict[str, Union[str, int, None]] = {
                "identifier": str(data["identifier"]), # type: ignore
                "author": str(data["author"]), # type: ignore
                "uniform_resource_locator": uniform_resource_locator,
                "author_channel": None
            }
            dataset.append(metadata)
        self.setData(dataset)

    def firstRun(self) -> None:
        """
        Executing the first run of the data processing workflow.

        Returns:
            void
        """
        for index in range(0, len(self.getData()), 1):
            delay: float = self.getDelay(str(self.getData()[index]["uniform_resource_locator"]))
            self.getLogger().inform(f"The delay has been calculated for the Crawler to process the data.\nDelay: {delay} s\nUniform Resource Locator: {str(self.getData()[index]['uniform_resource_locator'])}")
            sleep(delay)
            self.enterTarget(str(self.getData()[index]["uniform_resource_locator"]), delay, index)
        self.setUpData()

    def getDelay(self, uniform_resource_locator: str) -> float:
        """
        Calculating a randomized delay based on the length of the
        uniform resource locator and ensuring the delay falls within
        a specific range.

        Parameters:
            uniform_resource_locator (string): The uniform resource locator for which the delay is calculated.

        Returns:
            float
        """
        iteration: int = randint(0, 10)
        delay: float = (len(uniform_resource_locator) / (200 * (1.1 ** iteration))) * 60
        return delay if delay >= 10.00 and delay < 15.00 else 12.50

    def enterTarget(self, target: str, delay: float, index: int = 0) -> None:
        """
        Navigating to the specified target uniform resource locator
        and processes data based on the referrer.

        Parameters:
            target (string): The uniform resource locator to be visited.
            delay (float): The waiting time before proceeding.
            index (int): The index of the data entry being processed.

        Returns:
            void
        """
        referrer: str = stack()[1][3]
        if referrer == "firstRun":
            self.getLogger().inform(f"Entering the target!\nTarget: {target}")
            self.getDriver().get(target)
            sleep(delay)
        if referrer == "secondRun":
            self.getLogger().inform(f"Entering the target!\nTarget: {target}/videos")
            self.getDriver().get(f"{target}/videos")
            sleep(delay)
        self.retrieveData(referrer, index)

    def retrieveData(self, referrer: str, index: int = 0) -> None:
        """
        Retrieving the data needed from the target page.

        Parameters:
            referrer: string: Referrer of the function.
            index: int: The identifier of the data.

        Returns:
            void
        """
        try:
            self.__getDataFirstRun(referrer, index)
            self.__getDataSecondRun(referrer, index)
        except Exception as error:
            self.getLogger().error(f"An error occurred while retrieving data!\nError: {error}")

    def __getDataSecondRun(self, referrer: str, index: int) -> None:
        """
        Retrieving the latest content uniform resource locator
        during the second run and updates the data structure.

        Parameters:
            referrer (string): The source of the function call. Should be "secondRun" to proceed.
            index (int): The index in the data structure where the latest content uniform resource locator should be stored.

        Returns:
            void
        """
        if referrer != "secondRun":
            return
        try:
            self.setHtmlTags(self.getDriver().find_elements(By.XPATH, '//a[@id="thumbnail"]'))
            if len(self.getHtmlTags()) < 2:
                self.getLogger().warn("The thumbnail element is not found!")
                return
            self.setHtmlTag(self.getHtmlTags()[2])
            latest_content_uniform_resource_locator: str = str(self.getHtmlTag().get_attribute("href"))
            self.getData()[index]["latest_content"] = self.sanitizeUniformResourceLocator(latest_content_uniform_resource_locator)
        except Exception as error:
            self.getLogger().error(f"An error occurred while retrieving data for the second run!\nError: {error}")
            self.getData()[index]["latest_content"] = ""

    def __getDataFirstRun(self, referrer: str, index: int) -> None:
        """
        Retrieves the author's channel uniform resource locator
        during the first run and updates the data structure.

        Parameters:
            referrer (string): The source of the function call.  Should be "firstRun" to proceed.
            index (int): The index in the data structure where the author's channel uniform resource locator should be stored.

        Returns:
            void
        """
        if referrer != "firstRun":
            return
        try:
            self.setHtmlTag(self.getDriver().find_element(By.XPATH, '//*[@id="text]/a'))
            author_channel_uniform_resource_locator: str = str(self.getHtmlTag().get_attribute("href"))
            self.getData()[index]["author_channel"] = self.sanitizeUniformResourceLocator(author_channel_uniform_resource_locator)
        except Exception as error:
            self.getLogger().error(f"An error occurred while retrieving data for the first run!\nError: {error}")
            self.getData()[index]["author_channel"] = ""

    def sanitizeHtml(self, html: str) -> str:
        """
        Sanitizing the given HTML string by removing all tags and
        attributes.

        Parameters:
            html (string): The HTML content to be sanitized.

        Returns:
            string
        """
        allowed_tags: List[str] = ["a"]
        allowed_attributes: Dict[str, List[str]] = {
            "a": ["href", "title", "target", "rel"]
        }
        return clean(
            text=html,
            tags=allowed_tags,
            attributes=allowed_attributes,
            strip=True
        )

    def sanitizeUniformResourceLocator(self, uniform_resource_locator: str) -> str:
        """
        Sanitizing the given uniform resource locator by ensuring it
        belongs to an allowed domain.

        Parameters:
            uniform_resource_locator (string): The uniform resource locator to be sanitized.

        Returns:
            string
        """
        allowed_domains: List[str] = ["youtube.com", "youtu.be"]
        try:
            parsed_uniform_resource_locator: ParseResult = urlparse(uniform_resource_locator)
            return uniform_resource_locator if parsed_uniform_resource_locator.netloc in allowed_domains else ""
        except Exception as error:
            self.getLogger().error(f"Error occurred while sanitizing the Uniform Resource Locator!\nError: {error}\nUniform Resource Locator: {uniform_resource_locator}")
            return ""

