from flask.sessions import SessionMixin
from Models.DatabaseHandler import Database_Handler
from Models.Logger import Extractio_Logger
from Environment import Environment
from typing import Dict, Union
from json import JSONDecodeError, load
from os import remove
import os
import json
import time
import logging


class Session_Manager:
    """
    It allows the application to manage the session.
    """
    __directory: str
    """
    The directory of the session files.
    """
    __ip_address: str
    """
    The IP Address of the user.
    """
    __http_client_ip_address: str
    """
    The client's IP Address of the user
    """
    __proxy_ip_address: str
    """
    The Proxy's IP Address of the user.
    """
    __timestamp: int
    """
    The timestamp at which the session has been created.
    """
    __session_files: list[str]
    """
    The files containing the session of the users.
    """
    __color_scheme: str
    """
    The color scheme of the application.
    """
    __length: int
    """
    The amount of session files.
    """
    __session: SessionMixin
    """
    The session of the user.
    """
    __port: str
    """
    The port of the application.
    """
    __database_handler: Database_Handler
    """
    The database handler that will communicate with the database
    server.
    """
    __logger: Extractio_Logger
    """
    The logger that will all the action of the application.
    """

    def __init__(self, request: dict[str, str], session: SessionMixin) -> None:
        """
        Instantiating the session's manager which will verify the
        session of the users.

        Parameters:
            request:    (object):       The request from the application.
            session:    (SessionMixin): The session of the user.
        """
        ENV = Environment()
        self.setDirectory(
            f"{ENV.getDirectory()}/Cache/Session/Users/"
        )
        self.setLogger(Extractio_Logger())
        self.getLogger().setLogger(logging.getLogger(__name__))
        self.setPort(str(request["port"]))
        self.setDatabaseHandler(Database_Handler())
        self.setIpAddress(str(request["ip_address"]))
        self.setHttpClientIpAddress(
            str(request["http_client_ip_address"])
        )
        self.setProxyIpAddress(
            str(request["proxy_ip_address"])
        )
        self.__maintain()
        self.setSession(session)
        self.getLogger().inform(
            "The Session Management System has been successfully been initialized!"
        )
        self.verifySession()

    def getDirectory(self) -> str:
        return self.__directory

    def setDirectory(self, directory: str) -> None:
        self.__directory = directory

    def getIpAddress(self) -> str:
        return self.__ip_address

    def setIpAddress(self, ip_address: str) -> None:
        self.__ip_address = ip_address

    def getHttpClientIpAddress(self) -> str:
        return self.__http_client_ip_address

    def setHttpClientIpAddress(self, http_client_ip_address: str) -> None:
        self.__http_client_ip_address = http_client_ip_address

    def getProxyIpAddress(self) -> str:
        return self.__proxy_ip_address

    def setProxyIpAddress(self, proxy_ip_address: str) -> None:
        self.__proxy_ip_address = proxy_ip_address

    def getTimestamp(self) -> int:
        return self.__timestamp

    def setTimestamp(self, timestamp: int) -> None:
        self.__timestamp = timestamp

    def getSessionFiles(self) -> list[str]:
        return self.__session_files

    def setSessionFiles(self, session_files: list[str]) -> None:
        self.__session_files = session_files

    def getColorScheme(self) -> str:
        return self.__color_scheme

    def setColorScheme(self, color_scheme: str) -> None:
        self.__color_scheme = color_scheme

    def getLength(self) -> int:
        return self.__length

    def setLength(self, length: int) -> None:
        self.__length = length

    def getSession(self) -> SessionMixin:
        return self.__session

    def setSession(self, session: SessionMixin) -> None:
        self.__session = session

    def getPort(self) -> str:
        return self.__port

    def setPort(self, port: str) -> None:
        self.__port = port

    def getDatabaseHandler(self) -> Database_Handler:
        return self.__database_handler

    def setDatabaseHandler(self, database_handler: Database_Handler) -> None:
        self.__database_handler = database_handler

    def getLogger(self) -> Extractio_Logger:
        return self.__logger

    def setLogger(self, logger: Extractio_Logger) -> None:
        self.__logger = logger

    def __maintain(self) -> None:
        """
        Maintaining the database of the Session Management System by
        doing regular checks to keep only the active sessions and
        store inactive sessions in the database.

        Return:
            (void)
        """
        self.getDatabaseHandler()._query(
            query="CREATE TABLE IF NOT EXISTS `Visitors` (identifier INT PRIMARY KEY AUTO_INCREMENT, `timestamp` INT, client VARCHAR(16))",
            parameters=None
        )
        self.setSessionFiles(os.listdir(self.getDirectory()))
        self.setLength(len(self.getSessionFiles()))
        if self.getLength() > 0:
            self.verifyExistingSessions()

    def verifyExistingSessions(self) -> None:
        """
        Verifying existing sessions to remove expired ones.

        Return:
            (void)
        """
        age: int
        data: dict[str, dict[str, str | int]]
        for index in range(0, self.getLength(), 1):
            file_name = f"{self.getDirectory()}{self.getSessionFiles()[index]}"
            file = open(file_name, "r")
            data = json.load(file)
            age = int(time.time()) - int(data["Client"]["timestamp"])
            file.close()
            self.verifyInactiveSession(age, data, file_name)

    def verifyInactiveSession(self, age: int, session: dict[str, dict[str, str | int]], file_name: str) -> None:
        """
        Verifying that the session is inactive to remove it from the
        document database and to store it in the relational database.

        Parameters:
            age:        (int):      Age of the session.
            session:    (object):   The data of the session.
            file_name:  (string):   The name of the file.

        Return:
            (void)
        """
        if age > 3600:
            expired_sessions = (
                int(session["Client"]["timestamp"]),
                str(session["Client"]["ip_address"])
            )
            self.getDatabaseHandler().post_data(
                table="Visitors",
                columns="timestamp, client",
                values="%s, %s",
                parameters=expired_sessions
            )
            os.remove(file_name)

    def createSession(self) -> SessionMixin:
        """
        Creating the session.

        Return:
            (SessionMixin)
        """
        self.getSession().clear()
        self.setTimestamp(int(time.time()))
        self.setColorScheme("light")
        data: dict[str, str | int] = {
            "ip_address": self.getIpAddress(),
            "http_client_ip_address": self.getHttpClientIpAddress(),
            "proxy_ip_address": self.getProxyIpAddress(),
            "timestamp": self.getTimestamp(),
            "color_scheme": self.getColorScheme()
        }
        self.getSession()['Client'] = data
        session_data = self.retrieveSession()
        file_path = f"{self.getDirectory()}{self.getIpAddress()}.json"
        session_file = open(file_path, 'w')
        session_file.write(session_data)
        session_file.close()
        self.getLogger().inform("The session has been successfully created!")
        return self.getSession()

    def verifySession(self) -> None:
        """
        Verifying that the session is not hijacked

        Return:
            (void)
        """
        self.setSessionFiles(os.listdir(self.getDirectory()))
        self.setLength(len(self.getSessionFiles()))
        if len(self.getSessionFiles()) > 0:
            self.handleSessionData(self.sessionsLoader(self.getSessionFiles()))
        else:
            self.createSession()

    def retrieveSession(self) -> str:
        """
        Returning a stringified form of the session

        Return:
            (string)
        """
        return json.dumps(self.getSession(), indent=4)

    def updateSession(self, data: dict[str, dict[str, str | int]]) -> SessionMixin | None:
        """
        Modifying the session.

        Parameters:
            data:   (object):   Data from the view

        Return:
            (SessionMixin | void)
        """
        self.setTimestamp(int(time.time()))
        self.setColorScheme(str(data["Client"]["color_scheme"]))
        file_name = f"{self.getDirectory()}/{self.getIpAddress()}.json"
        data = json.load(open(file_name))
        if self.getIpAddress() == data['Client']['ip_address']:
            new_data: dict[str, str | int] = {
                "ip_address": self.getIpAddress(),
                "http_client_ip_address": self.getHttpClientIpAddress(),
                "proxy_ip_address": self.getProxyIpAddress(),
                "timestamp": self.getTimestamp(),
                "color_scheme": self.getColorScheme()
            }
            file = open(file_name, "w")
            self.getSession()["Client"] = new_data
            file.write(self.retrieveSession())
            file.close()
            self.getLogger().inform("The session has been successfully updated!")
            return self.getSession()

    def sessionsLoader(self, sessions: list[str]) -> dict[str, int]:
        """
        Iterating throughout the session files to process them
        depending on the response from the system.

        Parameters:
            sessions:   (array):  List of session files

        Return:
            (object)
        """
        response = {}
        for index in range(0, len(sessions), 1):
            if self.handleFile(sessions[index])["status"] == 200:
                response = {
                    "status": self.handleFile(sessions[index])["status"]
                }
                break
            elif self.handleFile(sessions[index])["status"] == 202:
                self.createSession()
                response = {
                    "status": 201
                }
                break
            elif self.handleFile(sessions[index])["status"] == 204:
                response = {
                    "status": self.handleFile(sessions[index])["status"]
                }
                continue
        return response

    def handleFile(self, file_name: str) -> dict[str, int]:
        """
        Ensuring that the file is of type JSON in order to process
        it further more.

        Parameters:
            file_name:  (string):   file to be loaded

        Return:
            (object)
        """
        response = {}
        if file_name.endswith(".json"):
            file_path = f"{self.getDirectory()}/{file_name}"
            file = open(file_path)
            data = json.load(file)
            response = {
                "status": self.handleSession(self.validateIpAddress(data)["status"], file_name)["status"]
            }
        else:
            response = {
                "status": 204
            }
        return response

    def validateIpAddress(self, data) -> dict[str, int]:
        """
        Validating the IP Address against the one stored in the
        cache file.

        Parameters:
            data:   (object):   The data in the file

        Return:
            (object)
        """
        response = {}
        if self.getIpAddress() == str(data['Client']['ip_address']):
            age = int(time.time()) - int(data['Client']['timestamp'])
            response = {
                "status": self.handleExpiryTime(age)["status"]
            }
        else:
            response = {
                "status": 204
            }
        return response

    def handleExpiryTime(self, expiry_time: int) -> dict[str, int]:
        """
        Handling the expiry time of the session.

        Parameters:
            expiry_time:    (int):  The expiry time of the session

        Return:
            (object)
        """
        response = {}
        if expiry_time < 3600:
            response = {
                "status": 200
            }
        else:
            response = {
                "status": 205
            }
        return response

    def getData(self, file_path: str) -> Union[Dict[str, Union[str, int]], None]:
        """
        Retrieving the data that is in the file.

        Parameters:
            file_path: string: The path of the file.

        Returns:
            {Client: {ip_address: string, http_client_ip_address: string, proxy_ip_address: string, timestamp: int, color_scheme: string}} | null
        """
        try:
            file = open(file_path, "r")
            data: Dict[str, Union[str, int]] = load(file)
            file.close()
            self.getLogger().inform(f"The file has been successfully read.\nFile Path: {file_path}")
            return data
        except JSONDecodeError as error:
            self.getLogger().error(f"Failed to decode the JSON file.\nFile Path: {file_path}\nError: {error}")
            return None

    def handleSession(self, status: int, name: str) -> Dict[str, int]:
        """
        Handling the session based on the status retrieved from the
        system.

        Parameters:
            status: int: HTTP Status Code
            name: string: File Name

        Returns:
            {status: int}
        """
        ok: int = 200
        accepted: int = 202
        no_content: int = 204
        reset_content: int = 205
        service_unavailable: int = 503
        file_path: str = f"{self.getDirectory()}/{name}"
        data: Union[Dict[str, Union[str, int]], None] = self.getData(file_path)
        if status == ok:
            self.setSession(data) # type: ignore
            return {
                "status": status
            }
        if status == no_content:
            return {
                "status": status
            }
        if status == reset_content:
            self.getSession().clear()
            remove(file_path)
            return {
                "status": accepted
            }
        return {
            "status": service_unavailable
        }

    def handleSessionData(self, session_data: dict[str, int]) -> None:
        """
        Verifying that the data has not been tampered in order to
        renew the session.

        Parameters:
            session_data:   (object):   Session's data

        Return:
            (void)
        """
        # Verifying that the data has been received or created in order to verify it to renew access.
        if session_data["status"] == 200 or session_data["status"] == 201:
            self.renew(self.getSession())
        else:
            self.createSession()

    def renew(self, session_data: SessionMixin) -> (SessionMixin | None):
        """
        Verifying that the IP Addresses are the same for renewing
        the access to their current data

        Parameters:
            session_data:   (SessionMixin): Session Data

        Return:
            (SessionMixin | void)
        """
        file_path = f"{self.getDirectory()}/{self.getIpAddress()}.json"
        if session_data['Client']['ip_address'] == self.getIpAddress():
            self.setTimestamp(int(time.time()))
            session_data['Client']['timestamp'] = self.getTimestamp()
            self.setSession(session_data)
            file = open(file_path, "w")
            file.write(json.dumps(self.getSession()))
            file.close()
            self.getLogger().inform("The session has been successfully renewed!")
            return self.getSession()
        else:
            self.getSession().clear()
            os.remove(file_path)
            self.createSession()
