# Importing the requirements
from flask.sessions import SessionMixin
import os
import json
import time


class Session_Manager:
    """
    It allows the application to manage the session.
    """
    __directory: str
    """
    The directory of the session files

    Type: string
    Visibility: private
    """
    __ip_address: str
    """
    The IP Address of the user

    Type: string
    Visibility: private
    """
    __http_client_ip_address: str
    """
    The client's IP Address of the user

    Type: string
    Visibility: private
    """
    __proxy_ip_address: str
    """
    The Proxy's IP Address of the user

    Type: string
    Visibility: private
    """
    __timestamp: int
    """
    The timestamp at which the session has been created

    Type: int
    Visibility: private
    """
    __session_files: list[str]
    """
    The files containing the session of the users

    Type: array
    Visibility: private
    """
    __color_scheme: str
    """
    The color scheme of the application

    Type: string
    Visibility: private
    """
    __length: int
    """
    The amount of session files

    Type: int
    Visibility: private
    """
    __session: SessionMixin
    """
    The session of the user.

    Type: SessionMixin
    Visibility: private
    """
    __port: str
    """
    The port of the application

    Type: int
    Visibility: private
    """

    def __init__(self, request: dict[str, str], session: "SessionMixin") -> None:
        """
        Instantiating the session's manager which will verify the
        session of the users.

        Parameters:
            request:    object:         The request from the application.
            session:    SessionMixin:   The session of the user.
        """
        self.setPort(request["port"])  # type: ignore
        self.__server()
        self.setDirectory(f"{self.getDirectory()}/Cache/Session/Users/")
        self.setIpAddress(request["ip_address"])  # type: ignore
        self.setHttpClientIpAddress(
            request["http_client_ip_address"])  # type: ignore
        self.setProxyIpAddress(request["proxy_ip_address"])  # type: ignore
        self.setSession(session)
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

    def getSession(self) -> "SessionMixin":
        return self.__session

    def setSession(self, session: "SessionMixin") -> None:
        self.__session = session

    def getPort(self) -> str:
        return self.__port

    def setPort(self, port: str) -> None:
        self.__port = port

    def __server(self) -> None:
        """
        Setting the directory for the application.

        Returns: void
        """
        # Verifying that the port is for either Apache HTTPD or Werkzeug
        if self.getPort() == '80' or self.getPort() == '443':
            self.setDirectory("/var/www/html/ytd_web_app")
        else:
            self.setDirectory("/home/darkness4869/Documents/extractio")

    def createSession(self) -> "SessionMixin":
        """
        Creating the session

        Returns: SessionMixin
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
        return self.getSession()

    def verifySession(self) -> None:
        """
        Verifying that the session is not hijacked

        Returns: void
        """
        self.setSessionFiles(os.listdir(self.getDirectory()))
        self.setLength(len(self.getSessionFiles()))
        # Ensuring that there are session files.
        if len(self.getSessionFiles()) > 0:
            self.handleSessionData(self.sessionsLoader(self.getSessionFiles()))
        else:
            self.createSession()

    def retrieveSession(self) -> str:
        """
        Returning a stringified form of the session

        Returns: string
        """
        return json.dumps(self.getSession(), indent=4)

    def updateSession(self, data: dict[str, dict[str, str | int]]) -> SessionMixin | None:
        """
        Modifying the session.

        Parameters:
            data:   object: Data from the view

        Returns: SessionMixin | void
        """
        self.setTimestamp(int(time.time()))
        self.setColorScheme(str(data["Client"]["color_scheme"]))
        file_name = f"{self.getDirectory()}/{self.getIpAddress()}.json"
        data = json.load(open(file_name))
        # Ensuring that the IP Addresses corresponds in order to update the session.
        if self.getIpAddress() == data['Client']['ip_address']:
            new_data = {
                "ip_address": self.getIpAddress(),
                "http_client_ip_address": data["Client"]["http_client_ip_address"],
                "proxy_ip_address": data["Client"]["proxy_ip_address"],
                "timestamp": self.getTimestamp(),
                "color_scheme": self.getColorScheme()
            }
            file = open(file_name, "w")
            self.getSession()["Client"] = new_data
            file.write(self.retrieveSession())
            file.close()
            return self.getSession()

    def sessionsLoader(self, sessions: list[str]) -> dict[str, int]:
        """
        Iterating throughout the session files to process them
        depending on the response from the system.

        Parameters:
            sessions: array: List of session files

        Returns: object
        """
        response = {}
        # Iterating throughout the session files to find any file that contains the IP Address of the client.
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
            file: Any: file to be loaded
        Returns: object
        """
        response = {}
        # Ensuring that the session files are of JSON file type.
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
            data: object: The data in the file

        Returns: object
        """
        response = {}
        # Verifying the IP Address of the client against the IP Address stored in the cache database as well as ensuring that the session is not expired.
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
        Handling the expiry time of the session

        Parameters:
            expiry_time: datetime: The expiry time of the session

        Returns: object
        """
        response = {}
        # Verifying that the session has not expired
        if expiry_time < 3600:
            response = {
                "status": 200
            }
        else:
            response = {
                "status": 205
            }
        return response

    def handleSession(self, status: int, name: str) -> dict[str, int]:
        """
        Handling the session based on the status retrieved from the
        system.

        Parameters:
            status: int: HTTP Status Code
            name: string: File Name

        Returns: object
        """
        response = {}
        file_path = f"{self.getDirectory()}/{name}"
        file = open(file_path)
        data = json.load(file)
        if status == 200:
            self.setSession(data)
            response = {
                "status": status
            }
        elif status == 204:
            response = {
                "status": status
            }
        elif status == 205:
            self.getSession().clear()
            os.remove(file_path)
            response = {
                "status": 202
            }
        return response

    def handleSessionData(self, session_data: dict[str, int]) -> None:
        """
        Verifying that the data has not been tampered in order to
        renew the session.

        Parameters:
            session_data: dict: Session's data

        Returns: void
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
            session_data: SessionMixin: Session Data

        Returns: SessionMixin | void
        """
        file_path = f"{self.getDirectory()}/{self.getIpAddress()}.json"
        # Comparing the IP Addresses to either renew the timestamp or to clear the session.
        if session_data['Client']['ip_address'] == self.getIpAddress():
            self.setTimestamp(int(time.time()))
            session_data['Client']['timestamp'] = self.getTimestamp()
            self.setSession(session_data)
            file = open(file_path, "w")
            file.write(json.dumps(self.getSession()))
            file.close()
            return self.getSession()
        else:
            self.getSession().clear()
            os.remove(file_path)
            self.createSession()

    def sessionDirectory(self) -> None:
        """
        Creating the Session Directory.

        Returns: void
        """
        if not os.path.exists(self.getDirectory()):
            os.makedirs(self.getDirectory(), 777)
