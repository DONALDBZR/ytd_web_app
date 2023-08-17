# Importing the requirements
from flask import session, request
from datetime import datetime, timedelta
import os
import json
from flask import sessions
from flask.sessions import SessionMixin


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
    __timestamp: str
    """
    The timestamp at which the session has been created

    Type: string
    Visibility: private
    """
    __session_files: list
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

    def __init__(self) -> None:
        """
        Instantiating the session's manager which will verify the session of the users
        """
        self.setDirectory("./Cache/Session/Users/")
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

    def getTimestamp(self) -> str:
        return self.__timestamp

    def setTimestamp(self, timestamp: str) -> None:
        self.__timestamp = timestamp

    def getSessionFiles(self) -> list:
        return self.__session_files

    def setSessionFiles(self, session_files: list) -> None:
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

    def createSession(self) -> None:
        """
        Creating the session

        Returns: void
        """
        self.getSession().clear()
        self.setIpAddress(str(request.environ.get('REMOTE_ADDR')))
        self.setHttpClientIpAddress(str(request.environ.get('HTTP_CLIENT_IP')))
        self.setProxyIpAddress(
            str(request.environ.get('HTTP_X_FORWARDED_FOR')))
        self.setTimestamp(datetime.now().strftime("%Y-%m-%d - %H:%M:%S"))
        self.setColorScheme("light")
        data = {
            "ip_address": self.getIpAddress(),
            "http_client_ip_address": self.getHttpClientIpAddress(),
            "proxy_ip_address": self.getProxyIpAddress(),
            "timestamp": self.getTimestamp(),
            "color_scheme": self.getColorScheme()
        }
        self.getSession()['Client'] = data
        session_data = self.retrieveSession()
        file_name = self.getIpAddress() + ".json"
        file_path = self.getDirectory() + file_name
        session_file = open(file_path, 'w')
        session_file.write(session_data)
        session_file.close()
        session = self.getSession()

    def verifySession(self) -> None:
        """
        Verifying that the session is not hijacked

        Returns: (void)
        """
        self.setSessionFiles(os.listdir(self.getDirectory()))
        self.setLength(len(self.getSessionFiles()))
        self.setIpAddress(str(request.environ.get('REMOTE_ADDR')))
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

    def updateSession(self, data) -> None:
        """
        Modifying the session

        Parameters: data: mixed: Data from the view

        Returns: void
        """
        self.setIpAddress(request.environ.get('REMOTE_ADDR'))
        self.setTimestamp(datetime.now().strftime("%Y-%m-%d - %H:%M:%S"))
        self.setColorScheme(data["Client"]["color_scheme"])
        self.setSessionFiles(os.listdir(self.getDirectory()))
        # Iterating throughout the session files to update the session needed.
        for index in range(0, len(self.getSessionFiles()), 1):
            # Ensuring that the session files are of JSON file type.
            if self.getSessionFiles()[index].endswith(".json"):
                file_name = str(self.getDirectory() + "/" +
                                self.getSessionFiles()[index])
                file = open(file_name)
                data = json.load(file)
                # Ensuring that the IP Addresses corresponds in order to update the session.
                if self.getIpAddress() == data['Client']['ip_address']:
                    new_data = {
                        "ip_address": self.getIpAddress(),
                        "http_client_ip_address": data["Client"]["http_client_ip_address"],
                        "proxy_ip_address": data["Client"]["proxy_ip_address"],
                        "timestamp": self.getTimestamp(),
                        "color_scheme": self.getColorScheme()
                    }
                    session["Client"] = new_data
                    session_data = self.getSession()
                    file_to_be_updated = open(file_name, "w")
                    file_to_be_updated.write(session_data)
                    file_to_be_updated.close()
                    session["Client"]["timestamp"] = self.getTimestamp()
                    session["Client"]["color_scheme"] = self.getColorScheme()

    def sessionsLoader(self, sessions: list) -> dict:
        """
        Iterating throughout the session files to process them depending on the response from the system.

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

    def handleFile(self, file_name: str) -> dict:
        """
        Ensuring that the file is of type JSON in order to process it further more.

        Parameters:
            file: Any: file to be loaded
        Returns: object
        """
        response = {}
        # Ensuring that the session files are of JSON file type.
        if file_name.endswith(".json"):
            file_path = str(self.getDirectory() + "/" + file_name)
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

    def validateIpAddress(self, data) -> dict:
        """
        Validating the IP Address against the one stored in the cache file.

        Parameters:
            data: object: The data in the file

        Returns: object
        """
        response = {}
        # Verifying the IP Address of the client against the IP Address stored in the cache database as well as ensuring that the session is not expired.
        if self.getIpAddress() == str(data['Client']['ip_address']):
            timestamp = datetime.strptime(
                str(data['Client']['timestamp']), "%Y-%m-%d - %H:%M:%S") + timedelta(hours=1)
            response = {
                "status": self.handleExpiryTime(timestamp)["status"]
            }
        else:
            response = {
                "status": 204
            }
        return response

    def handleExpiryTime(self, expiry_time: datetime) -> dict:
        """
        Handling the expiry time of the session

        Parameters:
            expiry_time: datetime: The expiry time of the session
            data: object: The data in the file

        Returns: object
        """
        response = {}
        # Verifying that the session has not expired
        if expiry_time > datetime.now():
            response = {
                "status": 200
            }
        else:
            response = {
                "status": 205
            }
        return response

    def handleSession(self, status: int, name: str) -> dict:
        """
        Handling the session based on the status retrieved from the system.

        Parameters:
            status: int: HTTP Status Code
            name: string: File Name

        Returns: object
        """
        response = {}
        file_path = str(self.getDirectory() + "/" + name)
        file = open(file_path)
        data = json.load(file)
        if status == 200:
            self.setSession(data)
            session = self.getSession()
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

    def handleSessionData(self, session_data: dict):
        """
        Verifying that the data has not been tampered in order to renew the session.

        Parameters:
            session_data: dict: Session's data

        Returns: void
        """
        # Verifying that the data has been received or created in order to verify it to renew access.
        if session_data["status"] == 200 or session_data == 201:
            self.renew(self.getSession())
        else:
            self.createSession()

    def renew(self, session_data: SessionMixin):
        """
        Verifying that the IP Addresses are the same for renewing the access to their current data

        Parameters:
            session_data: SessionMixin: Session Data
        """
        file_path = str(self.getDirectory() + "/" +
                        self.getIpAddress() + ".json")
        # Comparing the IP Addresses to either renew the timestamp or to clear the session.
        if session_data['Client']['ip_address'] == self.getIpAddress():
            self.setTimestamp(datetime.now().strftime("%Y-%m-%d - %H:%M:%S"))
            session_data['Client']['timestamp'] = self.getTimestamp()
            self.setSession(session_data)
            file = open(file_path, "w")
            file.write(json.dumps(self.getSession()))
            file.close()
            session = self.getSession()
        else:
            self.getSession().clear()
            os.remove(file_path)
            session = self.getSession()
            self.createSession()
