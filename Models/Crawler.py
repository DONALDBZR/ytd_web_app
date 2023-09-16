from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver


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
    __data: list[str]
    """
    The data from the cache data.

    Type: array
    """

    def __init__(self) -> None:
        self.setDriver(webdriver.Chrome())

    def getDriver(self) -> WebDriver:
        return self.__driver

    def setDriver(self, driver: WebDriver) -> None:
        self.__driver = driver

    def getData(self) -> list[str]:
        return self.__data

    def setData(self, data: list[str]) -> None:
        self.__data = data
