from io import TextIOWrapper
import json
import time
from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver
import os
from selenium.webdriver.common.by import By
import re
import inspect


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

    def getTargets(self) -> list[str]:
        return self.__targets

    def setTargets(self, targets: list[str]) -> None:
        self.__targets = targets

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
        self.setTargets([])
        # Verifying that the data has been set up.
        if inspect.stack()[1][3] == "setUpData":
            # Iterating thoughout the data to retrieve the targets for the first run.
            for index in range(0, len(self.getData()), 1):
                data = {
                    "author": self.getData()[index]["author"],
                    "author_channel": self.getData()[index]["author_channel"],
                    "rating": self.getData()[index]["rating"]
                }
                self.getData()[index] = data
                self.getTargets().append(str(data["author_channel"]))
        print(self.getData())
        self.refineData()
        # self.secondRun()

    def refineData(self) -> None:
        """
        Refining the data when there is duplicate data.

        Returns: void
        """
        new_data: list[dict[str, str | int | float | None]]
        authors = self.extractAuthors(self.getData())
        data: dict[str, str | int | float | None]
        indices: list[int]
        rating: float
        new_data = self.removeDuplicateData(self.extractAuthors(self.getData(
        )), self.calculateAverageRating(self.extractAuthors(self.getData())))

    def removeDuplicateData(self, authors: list[str], dataset: list[dict[str, str | int | float | None]]) -> list[dict[str, str | int | float | None]]:
        """
        Removing the duplicates from the data.

        Parameters:
            authors:    array:  The list of authors that is in the crawler.
            dataset:    array:  The dataset to be used.

        Returns: array
        """
        # Iterating throughout the list of authors to remove the duplicate data.
        for first_index in range(0, len(authors), 1):
            self.verifyDuplicateAuthor(authors, first_index, dataset)
        return dataset

    def verifyDuplicateAuthor(self, authors: list[str], index: int, dataset: list[dict[str, str | int | float | None]]) -> None:
        """
        Verifying that there is a duplicate author to remove it from
        the dataset.

        Parameters:
            authors:    array:  The list of authors that is in the crawler.
            index:      int:    The index of the data.
            dataset     array:  The dataset to be processed.

        Returns: void
        """
        # Ensuring that there is more than one occurence of the author needed.
        if authors.count(authors[index]):
            indices = [
                author_index for author_index,
                item in enumerate(authors)
                if item == authors[index]
            ]
            self.findDuplicateAuthor(indices, dataset)

    def findDuplicateAuthor(self, indices: list[int], dataset: list[dict[str, str | int | float | None]]):
        """
        Finding the duplicate authors.

        Parameters:
            indices:    array:  The identifiers of the duplicate authors.

        Return: None
        """
        # Iterating throughout the list of indices to remove the duplicates
        for index in range(0, len(indices), 1):
            # Removing every occurences after the first one.
            if index != 0:
                dataset.remove(dataset[indices[index]])

    def calculateAverageRating(self, authors: list[str]) -> list[dict[str, str | int | float | None]]:
        """
        Calculating the average rating based on the data that is in
        the crawler.

        Parameters:
            authors:    array:  The list of authors that is in the crawler.

        Returns: array
        """
        new_data: list[dict[str, str | int | float | None]] = []
        # Iterating throughout the data to calculate the rating.
        for first_index in range(0, len(authors), 1):
            data = self.getData()[first_index]
            new_data.append(self.verifyAuthor(first_index, authors, data))
        return new_data

    def verifyAuthor(self, index: int, authors: list[str], data: dict[str, str | int | float | None]) -> dict[str, str | int | float | None]:
        """
        Verifying the amount of occurences for an author to
        calculate their average rating.

        Parameters:
            index:      int:    The index of the data in the array.
            authors:    array:  The list of authors that is in the crawler.
            data:       object: The data to be refined

        Returns: object
        """
        # Ensuring that there are more than one occurence of the authors.
        if authors.count(authors[index]) != 1:
            indices = [
                author_index for author_index,
                item in enumerate(authors)
                if item == authors[index]
            ]
            rating: float = data["rating"]  # type: ignore
            data["rating"] = self.calculateDuplicateAverageRating(
                indices, rating)
        return data

    def calculateDuplicateAverageRating(self, indices: list[int], rating: float) -> float:
        """
        Calculating the average rating of the duplicate data.

        Parameters:
            indices:    array:  The list of indices of the duplicate data.
            rating:     float:  The rating of a media of the author.

        Returns:    float
        """
        # Iterating throughout the indices of the duplicates to calculate the average rating.
        for index in range(0, len(indices), 1):
            new_rating = float(
                self.getData()[indices[index]]["rating"])  # type: ignore
            rating = round(((rating + new_rating) / 2), 4)
        return rating

    def extractAuthors(self, dataset: list[dict[str, str | int | float | None]]) -> list[str]:
        """
        Extracting the authors from the data.

        Returns: array
        """
        authors: list[str] = []
        # Iterating throughout the data to return an array of the authors.
        for index in range(0, len(dataset), 1):
            authors.append(str(dataset[index]["author"]))
        return authors

    def secondRun(self):
        """
        The second run for the web-crawler to seek for the data
        needed from the targets.

        Returns: void
        """
        # Iterating throughout the targets to run throughout them
        for index in range(0, len(self.getTargets()), 1):
            self.enterTarget(self.getTargets()[index])
        # self.buildUpRating()

    def setUpDataSecondRun(self) -> int:
        """
        Setting up the data for the second run.

        Returns: int
        """
        # Iterating throughout the files to append their data to the array to be processed.
        for index in range(0, len(self.getFiles()), 1):
            file = open(f"{self.getDirectory()}/{self.getFiles()[index]}")
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
            file = open(f"{self.getDirectory()}/{self.getFiles()[index]}")
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
        self.setTargets([])
        # Verifying that the data has been set up.
        if inspect.stack()[1][3] == "setUpData":
            # Iterating thoughout the data to retrieve the targets for the first run.
            for index in range(0, len(self.getData()), 1):
                self.getTargets().append(
                    str(self.getData()[index]["uniform_resource_locator"]))
        elif inspect.stack()[1][3] == "consolidateData":
            # Iterating thoughout the data to retrieve the targets for the first run.
            for index in range(0, len(self.getUnprocessedData()), 1):
                self.getTargets().append(
                    str(self.getUnprocessedData()[index]["uniform_resource_locator"]))
        self.firstRun()

    def enterTarget(self, target: str) -> None:
        """
        Entering the targeted page.

        Parameters:
            target: string: The uniform resource locator of the targeted page.

        Returns: void
        """
        referrer = inspect.stack()[1][3]
        # Verifying the run of the crawler
        if referrer == "firstRun":
            self.getDriver().get(target)
            time.sleep(2.34375)
        elif referrer == "secondRun":
            self.getDriver().get(f"{target}/videos")
            time.sleep(117.1875)
        self.retrieveData(referrer)

    def retrieveData(self, referrer: str):
        """
        Retrieving the data needed from the target page.

        Parameters:
            referrer:   string: Referrer of the function

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
            videos_tab = self.getDriver().find_element(
                By.XPATH, '//*[@id="tabsContent"]/tp-yt-paper-tab[2]').click()

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

    def firstRun(self):
        """
        The first run for the web-crawler to seek for the data
        needed from the targets.

        Returns: void
        """
        # Iterating throughout the targets to run throughout them
        for index in range(0, len(self.getTargets()), 1):
            self.enterTarget(self.getTargets()[index])
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
            rating = round(int(data["Media"]["YouTube"]["likes"]) /  # type: ignore
                           int(data["Media"]["YouTube"]["views"]), 4)  # type: ignore
            data["Media"]["YouTube"]["rating"] = rating
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
