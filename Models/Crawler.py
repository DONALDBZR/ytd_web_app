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
    __data: list[dict]
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

    def __init__(self, port: str) -> None:
        """
        Initializing the crawler to scrape the data needed.

        Parameters:
            port: string:   port of the server for the application.
        """
        self.setDriver(webdriver.Chrome())
        self.__server(port)

    def getDriver(self) -> WebDriver:
        return self.__driver

    def setDriver(self, driver: WebDriver) -> None:
        self.__driver = driver

    def getData(self) -> list[dict]:
        return self.__data

    def setData(self, data: list[dict]) -> None:
        self.__data = data

    def getDirectory(self) -> str:
        return self.__directory

    def setDirectory(self, directory: str) -> None:
        self.__directory = directory

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
