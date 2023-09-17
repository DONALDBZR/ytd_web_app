from io import TextIOWrapper
import json
import time
from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver
import os
from selenium.webdriver.common.by import By
import re


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
    __targets: list[str]
    """
    The targets of the web-crawler.

    Type: array
    Visibility: private
    """

    def __init__(self, port: str) -> None:
        """
        Initializing the crawler to scrape the data needed.

        Parameters:
            port: string:   port of the server for the application.
        """
        self.setDriver(webdriver.Chrome())
        self.__server(port)
        self.setDirectory(f"{self.getDirectory()}/Cache/Media/")
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

    def getTargets(self) -> list[str]:
        return self.__targets

    def setTargets(self, targets: list[str]) -> None:
        self.__targets = targets

    def addUnprocessedData(self, key: str, keys: list[str], data: dict[str, str | int | None]) -> None:
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
            self.getData().append(data)

    def setUpData(self) -> None:
        """
        Setting up the data to be used to be used by the web
        crawler.

        Returns: void
        """
        self.setData([])
        self.setFiles(os.listdir(self.getDirectory()))
        # Iterating throughout the files to append their data to the array to be processed.
        for index in range(0, len(self.getFiles()), 1):
            file = open(f"{self.getDirectory()}/{self.getFiles()[index]}")
            data: dict[str, str | int | None] = json.load(file)[
                "Media"]["YouTube"]
            key = "likes"
            keys = list(data.keys())
            self.addUnprocessedData(key, keys, data)
        self.prepareFirstRun()

    def prepareFirstRun(self) -> None:
        """
        Preparing for the first run of crawling based on the data in
        the cache.

        Returns: void
        """
        self.setTargets([])
        # Iterating thoughout the data to retrieve the targets for the first run.
        for index in range(0, len(self.getData()), 1):
            self.getTargets().append(
                str(self.getData()[index]["uniform_resource_locator"]))
        self.firstRun()

    def enterTarget(self, target: str, index: int) -> None:
        """
        Entering the targeted page.

        Parameters:
            target: string: The uniform resource locator of the targeted page.
            index:  int:    The index of the target.

        Returns: void
        """
        self.getDriver().get(target)
        time.sleep(1.25)
        self.retrieveData(index)

    def retrieveData(self, index: int):
        """
        Retrieving the data needed from the target page.

        Parameters:
            index:  int:    The index of the target

        Returns: void
        """
        likes = str(self.getDriver().find_element(
            By.XPATH, '//*[@id="segmented-like-button"]/ytd-toggle-button-renderer/yt-button-shape/button').get_attribute("aria-label"))
        likes = re.sub("[a-zA-Z]", "", likes)
        likes = re.sub("\s", "", likes)
        likes = int(re.sub(",", "", likes))
        self.getData()[index]["likes"] = likes

    def firstRun(self):
        """
        The first run for the web-crawler to seek for the data
        needed from the targets.

        Returns: void
        """
        # Iterating throughout the targets to run throughout them
        for index in range(0, len(self.getTargets()), 1):
            self.enterTarget(self.getTargets()[index], index)
        self.buildUpRating()

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
