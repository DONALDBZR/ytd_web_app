import inspect
import re
import os
import time
import json
from Models.Media import Media
from io import TextIOWrapper
from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options


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
    __data: list[dict[str, str | int | None | float]]
    """
    The data from the cache data.

    Type: array
    """
    __unprocessed_data: list[dict[str, str | int | None | float]]
    """
    The data from the cache data that have been left behind.

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
    __media_management_system: Media
    """
    It allows the application to manage the media.

    Type: Media
    Visibility: private
    """
    __request: dict[str, None | str]
    """
    The request data from the view.

    Type: object
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

    def __init__(self, request: dict[str, None | str]) -> None:
        """
        Initializing the crawler to scrape the data needed.

        Parameters:
            request:    object: The request data from the view.
        """
        self.__setServices()
        self.__setOptions()
        self.setRequest(request)
        self.setDriver(webdriver.Chrome(self.getOption(), self.getService()))
        self.__server(str(self.getRequest()["port"]))
        self.setDirectory(f"{self.getDirectory()}/Cache/Media/")
        self.__schedule()

    def getDriver(self) -> WebDriver:
        return self.__driver

    def setDriver(self, driver: WebDriver) -> None:
        self.__driver = driver

    def getData(self) -> list[dict[str, str | int | None | float]]:
        return self.__data

    def setData(self, data: list[dict[str, str | int | None | float]]) -> None:
        self.__data = data

    def getUnprocessedData(self) -> list[dict[str, str | int | None | float]]:
        return self.__unprocessed_data

    def setUnprocessedData(self, unprocessed_data: list[dict[str, str | int | None | float]]) -> None:
        self.__unprocessed_data = unprocessed_data

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

    def getMedia(self) -> Media:
        return self.__media_management_system

    def setMedia(self, media_management_system: Media) -> None:
        self.__media_management_system = media_management_system

    def getRequest(self) -> dict[str, str | None]:
        return self.__request

    def setRequest(self, request: dict[str, str | None]) -> None:
        self.__request = request

    def getService(self) -> Service:
        return self.__services

    def setService(self, services: Service) -> None:
        self.__services = services

    def getOption(self) -> Options:
        return self.__options

    def setOption(self, options: Options) -> None:
        self.__options = options

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
            # Ensuring the file is older than a week.
            if age > 604800:
                self.setUpData()
        else:
            self.setUpData()

    def addUnprocessedData(self, key: str, keys: list[str], data: dict[str, str | int | None | float]) -> None:
        """
        Verifying that the data is not processed to append them to
        the array to be processed.

        Parameters:
            key:    string: The key to be verified.
            keys:   array:  The list of keys.
            data:   object: Data to be processed.

        Returns: void
        """
        # Verifying that the web-scrawler has processed the data
        if keys.count(key) == 0:
            # Verifying that the data has been set up.
            if inspect.stack()[1][3] == "setUpDataFirstRun":
                self.getData().append(data)
            elif inspect.stack()[1][3] == "consolidateData":
                self.getUnprocessedData().append(data)
        elif keys.count(key) == 1:
            # Verifying that the data has been set up.
            if inspect.stack()[1][3] == "setUpDataSecondRun":
                self.getData().append(data)

    def setUpData(self) -> None:
        """
        Setting up the data to be used to be used by the web
        crawler.

        Returns: void
        """
        self.setData([])
        self.setFiles(os.listdir(self.getDirectory()))
        # Verifying the amount of data to be processed
        if self.setUpDataFirstRun() > 0:
            self.prepareFirstRun()
        elif self.setUpDataSecondRun() > 0:
            self.prepareSecondRun()

    def prepareSecondRun(self) -> None:
        """
        Preparing for the second run of crawling based on the data
        in the cache.

        Returns: void
        """
        self.refineData()
        self.secondRun(inspect.stack()[1][3])

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

    def secondRun(self, referer: str):
        """
        The second run for the web-crawler to seek for the data
        needed from the targets.

        Parameters:
            referer:    string: The function that is calling it.

        Returns: void
        """
        # Verifying that the data has been set up.
        if referer == "setUpData":
            # Iterating throughout the targets to run throughout them
            for index in range(0, len(self.getData()), 1):
                self.enterTarget(
                    str(self.getData()[index]["author_channel"]), index)
        self.__buildData()

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

    def setUpDataSecondRun(self) -> int:
        """
        Setting up the data for the second run.

        Returns: int
        """
        # Iterating throughout the files to append their data to the array to be processed.
        for index in range(0, len(self.getFiles()), 1):
            file = open(f"{self.getDirectory()}/{self.getFiles()[index]}", "r")
            data: dict[str, str | int | None | float] = json.load(file)[
                "Media"]["YouTube"]
            key = "rating"
            keys = list(data.keys())
            self.addUnprocessedData(key, keys, data)
        return len(self.getData())

    def setUpDataFirstRun(self) -> int:
        """
        Setting up the data for the first run.

        Returns: int
        """
        # Iterating throughout the files to append their data to the array to be processed.
        for index in range(0, len(self.getFiles()), 1):
            file = open(f"{self.getDirectory()}/{self.getFiles()[index]}", "r")
            data: dict[str, str | int | None | float] = json.load(file)[
                "Media"]["YouTube"]
            key = "likes"
            keys = list(data.keys())
            self.addUnprocessedData(key, keys, data)
        return len(self.getData())

    def prepareFirstRun(self) -> None:
        """
        Preparing for the first run of crawling based on the data in
        the cache.

        Returns: void
        """
        self.firstRun(inspect.stack()[1][3])

    def enterTarget(self, target: str, index: int = 0) -> None:
        """
        Entering the targeted page.

        Parameters:
            target: string: The uniform resource locator of the targeted page.
            index:  int:    The identifier of the data.

        Returns: void
        """
        referrer = inspect.stack()[1][3]
        # Verifying the run of the crawler
        if referrer == "firstRun":
            self.getDriver().get(target)
            time.sleep(2.34375)
        elif referrer == "secondRun":
            self.getDriver().get(f"{target}/videos")
            time.sleep(1.171875)
        self.retrieveData(referrer, index)

    def retrieveData(self, referrer: str, index: int = 0) -> None | list[str]:
        """
        Retrieving the data needed from the target page.

        Parameters:
            referrer:   string: Referrer of the function.
            index:      int:    The identifier of the data.

        Returns: void
        """
        if referrer == "firstRun":
            likes = str(self.getDriver().find_element(
                By.XPATH, '//*[@id="segmented-like-button"]/ytd-toggle-button-renderer/yt-button-shape/button').get_attribute("aria-label"))
            likes = re.sub("[a-zA-Z]", "", likes)
            likes = re.sub("\s", "", likes)  # type: ignore
            likes = int(re.sub(",", "", likes))
            target = self.getDriver().current_url
            self.addRawData(target, likes)
        elif referrer == "secondRun":
            new_data: list[str] = []
            self.setHtmlTags(self.getDriver().find_elements(
                By.XPATH, '//a[@id="thumbnail"]'))
            self.getData()[index]["latest_content"] = str(
                self.getHtmlTags()[1].get_attribute("href"))

    def addRawData(self, target: str, likes: int) -> None:
        """
        Adding the raw data in its related data object.

        Parameters:
            target: string: Target of the web-crawler.
            likes:  int:    Likes of the content.

        Returns: void
        """
        # Iterating throughout the data to retrieve is related object.
        for index in range(0, len(self.getData()), 1):
            self.setLikes(target, likes, index)

    def setLikes(self, target: str, likes: int, index: int) -> None:
        """
        Adding the data from the content

        Parameters:
            target: string: Target of the web-crawler.
            likes:  int:    Likes of the content.
            index:  int:    Index of the content.

        Returns: void
        """
        # Verifying that the the target exists in the data.
        if self.getData()[index]["uniform_resource_locator"] == target:
            self.getData()[index]["likes"] = likes

    def firstRun(self, referrer: str):
        """
        The first run for the web-crawler to seek for the data
        needed from the targets.

        Parameters:
            referrer:   string: The function that is calling it.

        Returns: void
        """
        # Verifying the referer take the correct target.
        if referrer == "setUpData":
            # Iterating throughout the targets to run throughout them
            for index in range(0, len(self.getData()), 1):
                self.enterTarget(
                    str(self.getData()[index]["uniform_resource_locator"]))
        elif referrer == "buildUpRating":
            # Iterating throughout the targets to run throughout them
            for index in range(0, len(self.getUnprocessedData()), 1):
                self.enterTarget(str(self.getUnprocessedData()[
                                 index]["uniform_resource_locator"]))
        self.buildUpRating()

    def buildUpRating(self) -> None:
        """
        Building up the rating based on the data in the cache.

        Returns: void
        """
        self.setUnprocessedData([])
        self.consolidateData()
        # Verifying that there is no data that have been left behind in the process.
        if len(self.getUnprocessedData()) > 0:
            self.prepareFirstRun()
        else:
            self.calculateRating()

    def calculateRating(self) -> None:
        """
        Calculating the rating of the content.

        Returns: void
        """
        # Iterating throughout the data to calculate the rating
        for index in range(0, len(self.getData()), 1):
            data = {
                "Media": {
                    "YouTube": self.getData()[index]
                }
            }
            data["Media"]["YouTube"]["rating"] = round(int(
                data["Media"]["YouTube"]["likes"]) / int(data["Media"]["YouTube"]["views"]), 4)  # type: ignore
            self.getData()[index] = data  # type: ignore
        self.saveData()

    def saveData(self) -> None:
        """
        Saving the data into the cache after processing it.

        Returns: void
        """
        # Iterating throughout the files to update them.
        for index in range(0, len(self.getFiles()), 1):
            file = open(f"{self.getDirectory()}/{self.getFiles()[index]}", "w")
            file.write(json.dumps(self.getData()[index], indent=4))

    def consolidateData(self) -> None:
        """
        Consolidating the data by not leaving the data that have
        been retrieved behind.

        Returns: void
        """
        # Iterating throughout the data to set up the data that have not been processed.
        for index in range(0, len(self.getData()), 1):
            data = self.getData()[index]
            key = "likes"
            keys = list(data.keys())
            self.addUnprocessedData(key, keys, data)

    def __server(self, port: str) -> None:
        """
        Setting the directory for the application.

        Parameters:
            port:   string: The port of the application

        Returns: void
        """
        # Verifying that the port is for either Apache HTTPD or Werkzeug
        if port == '80' or port == '443':
            self.setDirectory("/var/www/html/ytd_web_app")
        else:
            self.setDirectory("/home/darkness4869/Documents/extractio")
