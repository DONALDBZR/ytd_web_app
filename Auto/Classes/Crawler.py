from selenium.webdriver import Chrome
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
from inspect import stack
from time import time, sleep
from json import dumps
from sys import path
from urllib.parse import ParseResult, urlparse
from random import randint, uniform
from urllib.robotparser import RobotFileParser
from selenium.common.exceptions import TimeoutException, WebDriverException, NoSuchElementException
from re import search
from html import escape


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
    __robot_parsers: Dict[str, RobotFileParser]
    """
    The robot parsers.
    """
    __environment: Environment
    """
    ENV File of the application
    """
    __user_agents: List[str]
    """
    The list of user agents.
    """

    def __init__(self) -> None:
        """
        Initializing the crawler to scrape the required data.  This
        method sets up the necessary components for the crawler,
        including the logger, services, options, web driver, data
        storage, and database handler.  It also sets the directory
        for caching and initializes the data structures required for
        the crawler.

        Raises:
            Exception: If an error occurs during the initialization process.
        """
        try:
            self.setEnvironment(Environment())
        except Exception as error:
            self.getLogger().error(f"An error occurred while setting the environment.\nError: {error}")
            raise error
        try:
            self.setLogger(Extractio_Logger(__name__))
        except Exception as error:
            self.getLogger().error(f"An error occurred while setting the logger.\nError: {error}")
            raise error
        self.__setUserAgents()
        self.__setServices()
        self.__setOptions()
        self.setDriver(Chrome(self.getOption(), self.getService()))
        self.setDirectory(f"{self.getEnvironment().getDirectory()}/Cache/Trend/")
        try:
            self.setDatabaseHandler(Database_Handler())
        except Exception as error:
            self.getLogger().error(f"An error occurred while setting the database handler.\nError: {error}")
            raise error
        self.setData([])
        self.setRobotParsers({})
        self.setUpData()

    def __setUserAgents(self) -> None:
        """
        Loading and set user agents from a file.  This method reads
        user agent strings from a file named `user_agents.txt`
        located in the environment's directory. The user agents are
        then stored using `setUserAgents`.  If an error occurs while
        reading the file, an error message is logged, and the
        exception is raised.

        Raises:
            Exception: If the file cannot be read or processed.

        Returns:
            void
        """
        try:
            file_name: str = f"{self.getEnvironment().getDirectory()}/user_agents.txt"
            file = open(file_name, "r")
            self.setUserAgents([line.strip() for line in file.readlines()])
            file.close()
        except Exception as error:
            self.getLogger().error(f"An error occurred while setting up the user agents.\nError: {error}")
            raise error

    def getUserAgents(self) -> List[str]:
        return self.__user_agents

    def setUserAgents(self, user_agents: List[str]) -> None:
        self.__user_agents = user_agents

    def getEnvironment(self) -> Environment:
        return self.__environment

    def setEnvironment(self, environment: Environment) -> None:
        self.__environment = environment

    def getRobotParsers(self) -> Dict[str, RobotFileParser]:
        return self.__robot_parsers

    def setRobotParsers(self, robot_parsers: Dict[str, RobotFileParser]) -> None:
        self.__robot_parsers = robot_parsers

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

        Raises:
            Exception: If an error occurs while setting the service.
        """
        try:
            self.setService(Service(ChromeDriverManager().install()))
            self.getLogger().inform("The Crawler's Service has been installed!")
        except Exception as error:
            self.getLogger().error(f"An error occurred while setting the service.\nError: {error}")
            raise error

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
        Setting up the data to be used by the web crawler.  This
        method retrieves the relevant data from the database
        (with a filter for content downloaded in the past 2 weeks),
        prepares the data for the crawling process, and invokes
        different crawling procedures based on the state of the
        system.  The referrer is checked to determine which phase
        the crawler is in (first run or second run), and the
        appropriate methods for the first and second runs are
        invoked.  If no new data is found, a log message is
        generated indicating no content was downloaded.  If there is
        an error during any step, it is logged for further
        investigation.

        Returns:
            void

        Raises:
            Exception: If an error occurs while setting up the data.
        """
        try:
            identifiers: List[RowType] = self.getDatabaseHandler().getData(
                parameters=None,
                table_name="MediaFile",
                filter_condition="date_downloaded >= NOW() - INTERVAL 2 WEEK",
                column_names="YouTube",
                group_condition="YouTube"
            )
            dataset: List[Dict[str, Union[str, int, None]]] = self.getData()
            referrer: str = stack()[1][3]
            self.__setUpFirstRun(referrer, identifiers)
            self.__setUpSecondRun(referrer, dataset)
            self.__initializeFirstRun(referrer)
            self.__initializeSecondRun(referrer)
            self.getLogger().inform(f"No new data has been found.\nWeekly Content Downloaded Amount: {len(identifiers)}") if len(identifiers) == 0 else exit()
        except Exception as error:
            self.getLogger().error(f"An error occurred while setting up the data.\nError: {str(error)}")
            raise error

    def __initializeSecondRun(self, referrer: str) -> None:
        """
        Initializing the second run process by checking if the
        system is in the `'firstRun'` state and contains data to
        process.  If the conditions are met, it logs the new content
        amount and proceeds with the second run.

        Parameters:
            referrer (string): The referrer string indicating the state of the system.

        Returns:
            void
        """
        if referrer != "firstRun" or len(self.getData()) == 0:
            return
        self.getLogger().inform(f"Latest Content to be displayed on the application.\nNew Content Amount: {len(self.getData())}")
        self.secondRun()

    def __initializeFirstRun(self, referrer: str) -> None:
        """
        Initializing the first run of the crawler if the conditions
        are met.  This method checks if the referrer is "__init__"
        and if data has been successfully retrieved.  If these
        conditions are satisfied, it logs the successful retrieval
        of the data and initiates the first run of the crawler.

        Parameters:
            referrer (string): The referrer string that indicates the state of the system.

        Returns:
            void
        """
        if referrer != "__init__" or len(self.getData()) == 0:
            return
        self.getLogger().inform(f"Data has been successfully retrieved from the database server.\nWeekly Content Downloaded Amount: {len(self.getData())}\n")
        self.firstRun()

    def __setUpSecondRun(self, referrer: str, dataset: List[Dict[str, Union[str, int, None]]]) -> None:
        """
        Preparing the system for the second run by initializing the
        data.  This method checks if the referrer is `"firstRun"`,
        indicating that the system is in the second run phase.  If
        this condition is met, it proceeds to prepare the system for
        the second run by calling `prepareSecondRun` with the
        provided dataset.

        Parameters:
            referrer (string): The referrer string that indicates the state of the system.
            dataset (List[Dict[string, Union[string, int, None]]]): The data that needs to be processed for the second run.

        Returns:
            None
        """
        if referrer != "firstRun":
            return
        self.prepareSecondRun(dataset)

    def __setUpFirstRun(self, referrer: str, dataset: List[RowType]) -> None:
        """
        Preparing the system for the first run by initializing the
        data.  This method checks if the referrer is `"__init__"`,
        indicating that the system is in the initialization phase.
        If this condition is met, it proceeds to prepare the system
        for the first run by calling `prepareFirstRun` with the
        provided dataset.

        Parameters:
            referrer (string): The referrer string that indicates the state of the system.
            dataset (List[RowType]): The data that needs to be processed for the first run.

        Returns:
            void
        """
        if referrer != "__init__":
            return
        self.prepareFirstRun(dataset)

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
            delay: float = self.getDelay()
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
        try:
            for index in range(0, len(self.getData()), 1):
                self.getLogger().inform(f"The latest content from YouTube has been retrieved according the usage of the users!\nLatest Content: {self.getData()[index]['latest_content']}")
                self.setMedia(Media(str(self.getData()[index]["latest_content"]), "youtube"))
                response: Union[Dict[str, Union[int, Dict[str, Union[int, Dict[str, Union[str, int, None]]]]]], Dict[str, Union[int, str]]] = self.getMedia().verifyPlatform()
                data: Dict[str, Union[str, int, None]] = response["data"]["data"] # type: ignore
                new_data.append(data)
            self.setData(new_data)
        except Exception as error:
            self.getLogger().error(f"An error occurred while building the data!\nError: {error}")
            raise error

    def save(self) -> None:
        """
        Saving the data.

        Returns:
            void

        Raises:
            Exception: If an error occurs while saving the data.
        """
        timestamp: int = int(time())
        file_name: str = f"{self.getDirectory()}{timestamp}.json"
        try:
            file = open(file_name, "w")
            file.write(dumps(self.getData(), indent=4))
            file.close()
        except Exception as error:
            self.getLogger().error(f"An error occurred while saving the data!\nError: {error}\nFile name: {file_name}")
        self.getLogger().inform(f"The latest content has been saved!\nFile Name: {file_name}")
        self.getDriver().quit()

    def prepareFirstRun(self, identifiers: List[RowType]) -> None:
        """
        Preparing the data for the first run by fetching and
        processing YouTube data.  This method processes the
        identifiers, retrieves YouTube data from the database, and
        updates the dataset.  It then sets the processed dataset to
        be used later in the web crawler.

        Parameters:
            identifiers (List[RowType]): A list of identifiers used to fetch YouTube data from the database.

        Returns:
            void

        Raises:
            Exception: If there is an error while retrieving data from the database or processing it.
        """
        allowed_platforms: List[str] = ["youtube", "youtu.be"]
        dataset: List[Dict[str, Union[str, int, None]]] = []
        try:
            dataset = self.__getYoutubeData(dataset, identifiers, allowed_platforms)
            self.setData(dataset)
        except Exception as error:
            self.getLogger().error(f"An error occured while retrieving data from the database server.\nError: {error}")
            raise error

    def __getYoutubeData(self, dataset: List[Dict[str, Union[str, int, None]]], identifiers: List[RowType], allowed_platforms: List[str]) -> List[Dict[str, Union[str, int, None]]]:
        """
        Retrieving and process YouTube data based on provided
        identifiers.

        This method fetches YouTube data from the relational database server using provided identifiers, validates them, and appends the results to the dataset.

        Parameters:
            dataset (List[Dict[string, Union[string, int, None]]]): The dataset where YouTube data will be stored.
            identifiers (List[RowType]): List of identifiers containing YouTube video references.
            allowed_platforms (List[string]): A list of allowed platforms.

        Returns:
            List[Dict[string, Union[string, int, None]]]

        Raises:
            ValueError: If identifiers are not a list, contain non-object values, or lack the 'YouTube' key.
        """
        if not isinstance(identifiers, list):
            self.getLogger().error(f"Invalid data from the relational database server.\nIdentifiers: {identifiers}")
            raise ValueError("Invalid data from the relational database server.")
        if not all(isinstance(data, dict) for data in identifiers):
            self.getLogger().error(f"The dataset contains non-object values!\nIdentifiers: {identifiers}")
            raise ValueError("The identifiers contains non-object values!")
        if not identifiers:
            self.getLogger().debug("No identifiers provided.")
            return dataset
        if "YouTube" not in identifiers[0]:
            self.getLogger().error(f"Missing key YouTube in identifier.\nIdentifiers: {identifiers[0]}")
            raise ValueError("Missing key YouTube in identifier.")
        for index in range(0, len(identifiers), 1):
            parameters: Tuple[str] = (identifiers[index]["YouTube"],) # type: ignore
            youtube_data: List[RowType] = self.getDatabaseHandler().getData(
                parameters=parameters,
                table_name="YouTube",
                join_condition="Media ON YouTube.Media = Media.identifier",
                filter_condition="YouTube.identifier = %s",
                column_names="YouTube.identifier AS identifier, YouTube.author AS author, Media.value AS platform"
            )
            dataset = self.__processYouTubeData(youtube_data, allowed_platforms, dataset)
        return dataset

    def __processYouTubeData(self, youtube: List[RowType], allowed_platforms: List[str], dataset: List[Dict[str, Union[str, int, None]]]) -> List[Dict[str, Union[str, int, None]]]:
        """
        Processing YouTube data and append valid entries to the
        dataset.

        This method verifies and processes YouTube data retrieved from a relational database.  It ensures that:
        - The YouTube data is a list of dictionaries.
        - The dataset consists of valid objects.
        - Each entry in the YouTube data has a valid identifier, platform, and metadata.

        If the data is valid, a properly formatted dictionary containing the YouTube video's identifier, author, uniform resource locator, and author channel is added to the dataset.

        Parameters:
            youtube (List[Dict[string, Union[string, int, None]]]): The list of YouTube video data.
            allowed_platforms (List[string]): A list of allowed platforms.
            dataset (List[Dict[string, Union[string, int, None]]]): The dataset where valid video entries will be added.

        Returns:
            List[Dict[string, Union[string, int, None]]]

        Raises:
            ValueError: If the YouTube data, dataset, or platform format is invalid.
        """
        if not isinstance(youtube, list):
            self.getLogger().error(f"Invalid data from the relational database server.\nYouTube: {youtube}")
            raise ValueError("Invalid data from the relational database server.")
        if not all(isinstance(data, dict) for data in dataset):
            self.getLogger().error(f"The dataset contains non-object values!\nDataset: {dataset}")
            raise ValueError("The dataset contains non-object values!")
        if not all(isinstance(data, dict) for data in youtube):
            self.getLogger().error(f"The YouTube data contains non-object values!\nYouTube: {youtube}")
            raise ValueError("The YouTube data contains non-object values!")
        if not youtube:
            self.getLogger().debug("No YouTube data found.")
            return dataset
        if not youtube[0]:
            self.getLogger().error("The youtube list is empty!\nyoutube: {youtube}")
            raise ValueError("The youtube list is empty!")
        video: Dict[str, str] = youtube[0] # type: ignore
        if bool(search(r"^[a-zA-Z0-9_-]$", video["identifier"])) != False:
            self.getLogger().error(f"Invalid identifier format!\nIdentifier: {video['identifier']}")
            raise ValueError("Invalid identifier format!")
        if video["platform"] not in allowed_platforms:
            self.getLogger().error(f"Invalid platform!\nPlatform: {video['platform']}")
            raise ValueError("Invalid platform!")
        uniform_resource_locator: str = f"{self.getEnvironment().getYouTubeVideoUniformResourceLocator()}{video['identifier']}"
        author: str = escape(video["author"])
        dataset.append({
            "identifier": video["identifier"],
            "author": author,
            "uniform_resource_locator": uniform_resource_locator,
            "author_channel": None
        })
        return dataset

    def firstRun(self) -> None:
        """
        Executing the first run of the data processing workflow.

        Returns:
            void
        """
        for index in range(0, len(self.getData()), 1):
            delay: float = self.getDelay()
            self.getLogger().inform(f"The delay has been calculated for the Crawler to process the data.\nDelay: {delay} s\nUniform Resource Locator: {str(self.getData()[index]['uniform_resource_locator'])}")
            sleep(delay)
            self.enterTarget(str(self.getData()[index]["uniform_resource_locator"]), delay, index)
        self.setUpData()

    def getDelay(self) -> float:
        """
        Calculating a randomized delay, ensuring it falls within a
        specific range. The calculation of the delay does not take
        in consideration external data.

        Returns:
            float: A delay between 10 and 15 seconds.
        """
        return uniform(10.0, 15.0)

    def enterTarget(self, target: str, delay: float, index: int = 0) -> None:
        """
        Navigating to the specified target uniform resource locator
        and processes data based on the referrer.  Checks the
        `robots.txt` file to determine if the crawler is allowed to
        access the target.  If allowed, it navigates to the target
        uniform resource locator.  The behavior differs depending on
        whether the function is called from the "firstRun" or
        "secondRun".

        Parameters:
            target (string): The uniform resource locator to be visited.
            delay (float): The delay between requests.
            index (int): The index of the data entry being processed.

        Returns:
            void
        """
        referrer: str = stack()[1][3]
        retries: int = 3
        user_agent: str = self.getUserAgents()[randint(0, len(self.getUserAgents()))]
        self.getOption().add_argument(f"user-agent={user_agent}")
        try:
            for attempt in range(0, retries, 1):
                self.setDriver(Chrome(self.getOption(), self.getService()))
                self.getLogger().debug(f"Attempting to enter the target!\nAttempt: {attempt + 1}\nUniform Resource Locator: {target}")
                parsed_uniform_resource_locator: ParseResult = urlparse(target)
                base_uniform_resource_locator: str = f"{parsed_uniform_resource_locator.scheme}://{parsed_uniform_resource_locator.netloc}"
                if self.__attemptNavigation(target, base_uniform_resource_locator, referrer, index, attempt, retries, user_agent):
                    return
                sleep(delay)
                delay *= 2
        except Exception as error:
            self.getLogger().error(f"An error occurred while trying to enter the target.\nError: {error}\nUniform Resource Locator: {target}")
        finally:
            self.getDriver().close()

    def __attemptNavigation(self, target: str, base_uniform_resource_locator: str, referrer: str, index: int, attempt: int, retries: int, user_agent: str) -> bool:
        """
        Attempting to navigate to a given target uniform resource
        locator, handling crawling restrictions, and retrieving
        data.  This method checks the `robots.txt` file to ensure
        that crawling is allowed, navigates to the target based on
        the referrer, and retrieves data if successful.

        Parameters:
            target (string): The uniform resource locator to be visited.
            base_uniform_resource_locator (string): The base uniform resource locator extracted from the target.
            referrer (string): The function or context that initiated the navigation.
            index (int): The index of the data entry being processed.
            attempt (int): The current attempt number for crawling.
            retries (int): The total number of allowed retry attempts.
            user_agent (string): The user agent string used for the request.

        Returns:
            bool

        Raises:
            TimeoutException: If the request times out.
            WebDriverException: If an issue occurs with the web driver.
            NoSuchElementException: If the target element is not found.
            Exception: If an unexpected error occurs.
        """
        try:
            parser: Union[RobotFileParser, None] = self.__checkRobotsParser(base_uniform_resource_locator)
            self.__robotTxtNotParsed(parser, target)
            self.__notAllowedCrawl(parser, target, user_agent)
            self.__enterTargetFirstRun(referrer, target)
            self.__enterTargetSecondRun(referrer, target)
            self.retrieveData(referrer, index)
            return True
        except (TimeoutException, WebDriverException, NoSuchElementException) as error:
            self.getLogger().error(f"The current attempt on crawling has failed.\nError: {error}\nAttempt: {attempt + 1}")
            if attempt >= retries - 1:
                self.getLogger().error(f"Failing to navigate the current target!\nError: {error}\nAttempts: {retries}\nUniform Resource Locator: {target}")
            return False
        except Exception as error:
            self.getLogger().error(f"An unexpected error occurred!\nError: {error}\nUniform Resource Locator: {target}")
            return False

    def __robotTxtNotParsed(self, parser: Union[RobotFileParser, None], target: str) -> None:
        """
        Checking whether the `robots.txt` file has been parsed.  If
        it has not, logs an error and removes the target uniform
        resource locator from the data list at the given index.

        Parameters:
            parser (Union[RobotFileParser, None]): The parser object for the `robots.txt` file.  If None, the `robots.txt` file is considered not parsed.
            target (string): The Uniform Resource Locator that is being checked.

        Returns:
            None

        Raises:
            Exception: If the `robots.txt` file has not been parsed.
        """
        if parser:
            return
        self.getLogger().error(f"The robots.txt file has not been parsed!\nUniform Resource Locator: {target}")
        raise Exception("The robots.txt file has not been parsed!")

    def __notAllowedCrawl(self, parser: Union[RobotFileParser, None], target: str, user_agent: str) -> None:
        """
        Checking if the crawler is allowed to access a specific
        target based on the `robots.txt` file.  If not allowed, logs
        a warning and removes the target uniform resource locator
        from the data list at the given index.

        Parameters:
            parser (Union[RobotFileParser, None]): The parser object for the `robots.txt` file.  It should be able to check whether crawling is allowed.
            target (string): The Uniform Resource Locator that is being checked for crawling permission.
            user_agent (string): The user agent value that is being used to access the target.

        Returns:
            None

        Raises:
            Exception: If the crawler is not allowed to access the target.
        """
        if parser.can_fetch(user_agent, target): # type: ignore
            return
        self.getLogger().error(f"The crawler is not allowed to accessed the target.\nUniform Resource Locator: {target}")
        raise Exception(f"The crawler is not allowed to accessed the target!\nUniform Resource Locator: {target}")

    def __enterTargetFirstRun(self, referrer: str, target: str) -> None:
        """
        Entering the target URL if the referrer is `"firstRun"`.
        Logs an informational message and directs the web driver to
        the target URL.

        Parameters:
            referrer (string): The referrer value that should be `"firstRun"` to trigger the target entry.
            target (string): The Uniform Resource Locator (URL) to which the web driver should navigate.

        Returns:
            None

        Raises:
            Exception: If an error occurs while entering the first target.
        """
        if referrer != "firstRun":
            return
        try:
            self.getLogger().inform(f"Entering the target!\nTarget: {target}")
            self.getDriver().get(target)
        except Exception as error:
            self.getLogger().error(f"An error occurred while entering the first target!\nError: {error}\nTarget: {target}")
            raise error


    def __enterTargetSecondRun(self, referrer: str, target: str) -> None:
        """
        Entering the target uniform resource locator with a `"/videos"` suffix if the referrer is `"secondRun"`.  Logs an informational message and directs the web driver to the target uniform resource locator with the `"/videos"` path.

        Parameters:
            referrer (string): The referrer value that should be `"secondRun"` to trigger the target entry.
            target (string): The Uniform Resource Locator (URL) to which the web driver should navigate, with `"/videos"` appended.

        Returns:
            None

        Raises:
            Exception: If an error occurs while entering the second target.
        """
        if referrer != "secondRun":
            return
        try:
            self.getLogger().inform(f"Entering the target!\nTarget: {target}/videos")
            self.getDriver().get(f"{target}/videos")
        except Exception as error:
            self.getLogger().error(f"An error occurred while entering the second target!\nError: {error}\nTarget: {target}")
            raise error

    def __checkRobotsParser(self, uniform_resource_locator: str) -> Union[RobotFileParser, None]:
        """
        Checking and retrieving the robots.txt parser for a given
        uniform resource locator.  This method verifies if the
        `robots.txt` file for the specified uniform resource locator
        has already been parsed and stored.  If not, it fetches the
        `robots.txt` file, parses it, and stores it for future use.
        The parser is then returned for further checking of crawling
        permissions.

        Parameters:
            uniform_resource_locator (string): The uniform resource locator for which the robots.txt file is being checked.

        Returns:
            Union[RobotFileParser, None]
        """
        self.getLogger().debug(f"Checking robots parser.\nUniform Resource Locator: {uniform_resource_locator}")
        if uniform_resource_locator not in self.getRobotParsers():
            robots_uniform_resource_locator: str = f"{uniform_resource_locator}/robots.txt"
            parser: RobotFileParser = RobotFileParser()
            parser.set_url(robots_uniform_resource_locator)
            self.__readRobotTxt(parser, uniform_resource_locator)
        return self.getRobotParsers().get(uniform_resource_locator)

    def __readRobotTxt(self, parser: RobotFileParser, uniform_resource_locator: str) -> None:
        """
        Reading the `robots.txt` file for the specified Uniform
        Resource Locator and updating the internal robot parsers.
        This method attempts to read the `robots.txt` file using the
        provided parser.  If an error occurs during the reading
        process, it logs the error and removes the corresponding
        entry from the internal robot parsers dictionary.  The
        result is stored in the internal robot parsers dictionary
        with the uniform resource locator as the key.

        Parameters:
            parser (RobotFileParser): The parser instance used to read the `robots.txt` file.
            uniform_resource_locator (string): The uniform resource locator for which the `robots.txt` file is being read.

        Returns:
            None

        Raises:
            Exception: If an error occurs while reading the `robots.txt` file.
        """
        try:
            parser.read()
            self.getRobotParsers()[uniform_resource_locator] = parser
        except Exception as error:
            self.getLogger().error(f"An error occured while reading the robots.txt file.\nError: {error}\nUniform Resource Locator: {uniform_resource_locator}")
            if uniform_resource_locator in self.getRobotParsers():
                del self.getRobotParsers()[uniform_resource_locator]
            raise error

    def retrieveData(self, referrer: str, index: int = 0) -> None:
        """
        Retrieving the data needed from the target page.

        Parameters:
            referrer: string: Referrer of the function.
            index: int: The identifier of the data.

        Returns:
            void

        Raises:
            Exception: If an error occurs while retrieving data.
        """
        try:
            self.__getDataFirstRun(referrer, index)
            self.__getDataSecondRun(referrer, index)
        except Exception as error:
            self.getLogger().error(f"An error occurred while retrieving data!\nError: {error}")
            raise error

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
            raise error

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
            raise error

    def sanitizeUniformResourceLocator(self, uniform_resource_locator: str) -> str:
        """
        Sanitizing the given uniform resource locator by ensuring it
        belongs to an allowed domain.  This function parses the
        uniform resource locator and validates its components such
        as scheme, domain, port, user info, and fragment.  Only
        HTTPS uniform resource locators belonging to allowed domains
        are considered valid.

        Parameters:
            uniform_resource_locator (string): The uniform resource locator to be sanitized.

        Returns:
            string

        Raises:
            ValueError: If the uniform resource locator is invalid.
        """
        allowed_domains: List[str] = ["youtube.com", "youtu.be"]
        try:
            parsed_uniform_resource_locator: ParseResult = urlparse(uniform_resource_locator)
            return self.validateUniformResourceLocator(parsed_uniform_resource_locator, allowed_domains, uniform_resource_locator)
        except (ValueError, Exception) as error:
            self.getLogger().error(f"Error occurred while sanitizing the Uniform Resource Locator!\nError: {error}\nUniform Resource Locator: {uniform_resource_locator}")
            raise error

    def validateUniformResourceLocator(self, parsed_uniform_resource_locator: ParseResult, allowed_domains: List[str], uniform_resource_locator: str) -> str:
        """
        Validating the parsed uniform resource locator against
        security constraints.  This function checks if the scheme is
        HTTPS, the domain is in the allowed list, and ensures that
        ports, user info, and fragments are not present.

        Parameters:
            parsed_uniform_resource_locator (ParseResult): The parsed uniform resource locator object.
            allowed_domains (List[str]): List of allowed domain names.
            uniform_resource_locator (string): The original uniform resource locator string.

        Returns:
            string

        Raises:
            ValueError: If the uniform resource locator is invalid.
        """
        if parsed_uniform_resource_locator.scheme != "https":
            self.getLogger().error(f"Invalid scheme in URL. Only HTTPS is allowed.\nUniform Resource Locator: {uniform_resource_locator}")
            raise ValueError("Invalid scheme in URL. Only HTTPS is allowed.")
        if parsed_uniform_resource_locator.netloc not in allowed_domains:
            self.getLogger().error(f"Invalid domain in URL. Domain is not allowed.\nUniform Resource Locator: {uniform_resource_locator}")
            raise ValueError("Invalid domain in URL. Domain is not allowed.")
        if parsed_uniform_resource_locator.port is not None:
            self.getLogger().error(f"Port number is not allowed in URL.\nUniform Resource Locator: {uniform_resource_locator}")
            raise ValueError("Port number is not allowed in URL.")
        if parsed_uniform_resource_locator.username or parsed_uniform_resource_locator.password:
            self.getLogger().error(f"User information is not allowed in URL.\nUniform Resource Locator: {uniform_resource_locator}")
            raise ValueError("User information is not allowed in URL.")
        if parsed_uniform_resource_locator.fragment:
            self.getLogger().error(f"Fragment is not allowed in URL.\nUniform Resource Locator: {uniform_resource_locator}")
            raise ValueError("Fragment is not allowed in URL.")
        return uniform_resource_locator
