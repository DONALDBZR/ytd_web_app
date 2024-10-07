"""
The module which has the Session Management System of the
application.
"""


from flask.sessions import SessionMixin
from Models.DatabaseHandler import Database_Handler
from Models.Logger import Extractio_Logger
from Environment import Environment
from typing import List, Dict, Union, Tuple
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
    __session_files: List[str]
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

    def __init__(self, request: Dict[str, str], session: SessionMixin) -> None:
        """
        Instantiating the session's manager which will verify the
        session of the users.

        Parameters:
            request: {ip_address: string, http_client_ip_address: string, proxy_ip_address: string, port: string}: The request from the application.
            session: SessionMixin: The session of the user.
        """
        ENV = Environment()
        self.setDirectory(f"{ENV.getDirectory()}/Cache/Session/Users/")
        self.setLogger(Extractio_Logger())
        self.getLogger().setLogger(logging.getLogger(__name__))
        self.setPort(str(request["port"]))
        self.setDatabaseHandler(Database_Handler())
        self.setIpAddress(str(request["ip_address"]))
        self.setHttpClientIpAddress(str(request["http_client_ip_address"]))
        self.setProxyIpAddress(str(request["proxy_ip_address"]))
        self.__maintain()
        self.setSession(session)
        self.getLogger().inform("The Session Management System has been successfully been initialized!")
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

    def getSessionFiles(self) -> List[str]:
        return self.__session_files

    def setSessionFiles(self, session_files: List[str]) -> None:
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

        Returns:
            void
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

        Returns:
            void
        """
        age: int
        data: Union[Dict[str, Dict[str, Union[str, int]]], None]
        for index in range(0, self.getLength(), 1):
            file_name: str = f"{self.getDirectory()}{self.getSessionFiles()[index]}"
            file = open(file_name, "r")
            content: Union[str, None] = file.read().strip()
            file.close()
            if (content is not None or content != "") and len(content) != 0:
                data: Union[Dict[str, Dict[str, Union[str, int]]], None] = self._verifyExistingSessionsGetSessionData(content)
                age = int(time.time()) - int(data["Client"]["timestamp"]) if data is not None else int(time.time()) - 3601
                self.verifyInactiveSession(age, data, file_name)

    def _verifyExistingSessionsGetSessionData(self, content: Union[str, None]) -> Union[Dict[str, Dict[str, Union[str, int]]], None]:
        """
        Retrieving the session data that will be used to verify
        existing sessions.

        Parameters:
            content: string|null: The content of the file that is in a string form.

        Returns:
            {Client: {ip_address: string, http_client_ip_address: string, proxy_ip_address: string, timestamp: int, color_scheme: string}}|null
        """
        try:
            return json.loads(str(content))
        except json.JSONDecodeError:
            return None

    def verifyInactiveSession(self, age: int, session: Union[Dict[str, Dict[str, Union[str, int]]], None], file_name: str) -> None:
        """
        Verifying that the session is inactive to remove it from the
        document database and to store it in the relational
        database.

        Parameters:
            age: int: Age of the session.
            session: {Client: {ip_address: string, http_client_ip_address: string, proxy_ip_address: string, timestamp: int, color_scheme: string}}|null: The data of the session.
            file_name: string: The name of the file.

        Returns:
            void
        """
        if age > 3600 and session is not None:
            expired_sessions: Tuple[int, str] = (int(session["Client"]["timestamp"]), str(session["Client"]["ip_address"]))
            self.getDatabaseHandler().postData(
                table="Visitors",
                columns="timestamp, client",
                values="%s, %s",
                parameters=expired_sessions
            )
            os.remove(file_name)

    def createSession(self) -> SessionMixin:
        """
        Creating the session.

        Returns:
            SessionMixin
        """
        self.getSession().clear()
        self.setTimestamp(int(time.time()))
        self.setColorScheme("light")
        data: Dict[str, Union[str, int]] = {
            "ip_address": self.getIpAddress(),
            "http_client_ip_address": self.getHttpClientIpAddress(),
            "proxy_ip_address": self.getProxyIpAddress(),
            "timestamp": self.getTimestamp(),
            "color_scheme": self.getColorScheme()
        }
        self.getSession()['Client'] = data
        session_data = self.retrieveSession()
        self.getLogger().debug(f"Status: Created\nSession Data: {session_data}")
        file_path = f"{self.getDirectory()}{self.getIpAddress()}.json"
        session_file = open(file_path, 'w')
        session_file.write(session_data)
        session_file.close()
        self.getLogger().inform("The session has been successfully created!")
        return self.getSession()

    def verifySession(self) -> None:
        """
        Verifying that the session is not hijacked

        Returns:
            void
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

        Returns:
            string
        """
        return json.dumps(self.getSession(), indent=4)

    def updateSession(self, data: Dict[str, Dict[str, str]]) -> SessionMixin:
        """
        Modifying the session.

        Parameters:
            data: {Client: {color_scheme: string}}: Data from the view

        Returns:
            SessionMixin
        """
        self.setTimestamp(int(time.time()))
        self.setColorScheme(str(data["Client"]["color_scheme"]))
        file_name: str = f"{self.getDirectory()}{self.getIpAddress()}.json"
        try:
            file = open(file_name, "r")
        except FileNotFoundError:
            self.getLogger().error(f"No such file!\n{file_name=}")
            exit()
        content: Union[str, None] = file.read().strip()
        file.close()
        data = json.loads(content)
        if self.getIpAddress() == data['Client']['ip_address']:
            new_data: Dict[str, Union[str, int]] = {
                "ip_address": self.getIpAddress(),
                "http_client_ip_address": self.getHttpClientIpAddress(),
                "proxy_ip_address": self.getProxyIpAddress(),
                "timestamp": self.getTimestamp(),
                "color_scheme": self.getColorScheme()
            }
            file = open(file_name, "w")
            self.getSession()["Client"] = new_data
            self.getLogger().debug(f"Status: Updated\nSession Data: {self.retrieveSession()}")
            file.write(self.retrieveSession())
            file.close()
            self.getLogger().inform("The session has been successfully updated!")
            return self.getSession()
        else:
            return self.createSession()

    def sessionsLoader(self, sessions: List[str]) -> Dict[str, int]:
        """
        Iterating throughout the session files to process them
        depending on the response from the system.

        Parameters:
            sessions: [string]: List of session files

        Returns:
            {status: int}
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

    def _handleFile(self, file_name: str) -> Dict[str, int]:
        """
        Verifying that the file is not empty to return the correct
        response.

        Parameters:
            file_name: string: The path of the file.

        Returns:
            {status: int}
        """
        file_path: str = f"{self.getDirectory()}{file_name}"
        content: Union[str, None]
        try:
            file = open(file_path, "r", encoding="utf-8")
            content = file.read().strip()
        except FileNotFoundError:
            content = None
        if not content:
            return {
                "status": 204
            }
        else:
            try:
                data = json.loads(content)
                return {
                    "status": self.handleSession(self.validateIpAddress(data)["status"], file_name)["status"]
                }
            except json.JSONDecodeError:
                data = None
                return {
                    "status": self.handleSession(205, file_name)["status"]
                }

    def handleFile(self, file_name: str) -> Dict[str, int]:
        """
        Ensuring that the file is of type JSON in order to process
        it further more.

        Parameters:
            file_name: string: File to be loaded

        Return:
            {status: int}
        """
        response = {}
        if file_name.endswith(".json") and os.path.isfile(f"{self.getDirectory()}{file_name}"):
            response = self._handleFile(file_name)
        else:
            response = {
                "status": 204
            }
        return response

    def validateIpAddress(self, data: Dict[str, Dict[str, Union[str, int]]]) -> Dict[str, int]:
        """
        Validating the IP Address against the one stored in the
        cache file.

        Parameters:
            data: {Client: {ip_address: string, http_client_ip_address: string, proxy_ip_address: string, timestamp: int, color_scheme: string}}: The data in the file

        Returns:
            {status: int}
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

    def handleExpiryTime(self, expiry_time: int) -> Dict[str, int]:
        """
        Handling the expiry time of the session.

        Parameters:
            expiry_time: int: The expiry time of the session

        Returns:
            {status: int}
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
        content: Union[str, None]
        file_path: str = f"{self.getDirectory()}{name}"
        if not os.path.isfile(file_path):
            return {
                "status": 204
            }
        try:
            file = open(file_path, "r")
            content = file.read().strip()
        except FileNotFoundError:
            content = None
        if status == 200 and content is not None and content != "":
            data = json.loads(content)
            self.setSession(data)
            return {
                "status": status
            }
        if status == 204:
            return {
                "status": status
            }
        if status == 205:
            self.getSession().clear()
            try:
                os.remove(file_path)
            except FileNotFoundError:
                pass
            return {
                "status": 202
            }
        try:
            os.remove(file_path)
        except FileNotFoundError:
            pass
        return {
            "status": 204
        }

    def handleSessionData(self, session_data: Dict[str, int]) -> None:
        """
        Verifying that the data has not been tampered in order to
        renew the session.

        Parameters:
            session_data: {Client: {ip_address: string, http_client_ip_address: string, proxy_ip_address: string, timestamp: int, color_scheme: string}}: Session's data

        Returns:
            void
        """
        if "status" in session_data and (session_data["status"] == 200 or session_data["status"] == 201):
            self.renew(self.getSession())
        else:
            self.createSession()

    def renew(self, session_data: SessionMixin) -> Union[SessionMixin, None]:
        """
        Verifying that the IP Addresses are the same for renewing
        the access to their current data

        Parameters:
            session_data: SessionMixin: Session Data

        Returns:
            SessionMixin|void
        """
        file_path: str = f"{self.getDirectory()}{self.getIpAddress()}.json"
        if session_data['Client']['ip_address'] == self.getIpAddress():
            self.setTimestamp(int(time.time()))
            session_data['Client']['timestamp'] = self.getTimestamp()
            self.setSession(session_data)
            file = open(file_path, "w")
            file.write(json.dumps(self.getSession(), indent=4))
            file.close()
            self.getLogger().inform("The session has been successfully renewed!")
            return self.getSession()
        else:
            self.getSession().clear()
            os.remove(file_path)
            self.createSession()
