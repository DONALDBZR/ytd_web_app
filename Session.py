# Importing the requirements for the system
from flask import session, request
from datetime import datetime
import os
import json


class SessionManager:
    """
    It allows the application to manage the session.
    """
    __directory: str
    """
    The directory of the session files

    Type: string
    """
    __ip_address: str
    """
    The IP Address of the user

    Type: string
    """
    __http_client_ip_address: str
    """
    The client's IP Address of the user

    Type: string
    """
    __proxy_ip_address: str
    """
    The Proxy's IP Address of the user

    Type: string
    """
    __timestamp: str
    """
    The timestamp at which the session has been created

    Type: string
    """
    __session_files: list
    """
    The files containing the session of the users

    Type: array
    """
    __session: dict
    """
    The data of the session

    Type: object
    """
    __color_scheme: str
    """
    The color scheme of the application

    Type: string
    """

    def __init__(self) -> None:
        """
        Instantiating the session's manager which will verify the session of the users
        """

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

    def getSession(self) -> dict:
        return self.__session

    def setSession(self, session: dict) -> None:
        self.__session = session

    def getColorScheme(self) -> str:
        return self.__color_scheme

    def setColorScheme(self, color_scheme: str) -> None:
        self.__color_scheme = color_scheme

    def createSession(self) -> None:
        """
        Creating the session

        Returns: (void): The session is created
        """

        self.setIpAddress(request.environ('REMOTE_ADDR'))
        self.setHttpClientIpAddress(request.environ('HTTP_CLIENT_IP'))
        self.setProxyIpAddress(request.environ('HTTP_X_FORWARDED_FOR'))
        self.setTimestamp(datetime.now())
        self.setColorScheme("light")
        data = {
            "ip_address": self.getIpAddress(),
            "http_client_ip_address": self.getHttpClientIpAddress(),
            "proxy_ip_address": self.getProxyIpAddress(),
            "timestamp": self.getTimestamp(),
            "color_scheme": self.getColorScheme()
        }
        session['Client'] = data
        self.setSession(session)

    def verifySession(self) -> None:
        """
        Verifying that the session is not hijacked

        Returns: (void): Either the session has been updated, the session has been destroyed or the session will be created
        """
        self.setDirectory("/Cache/Session/Users")
        self.setSessionFiles(os.listdir(self.getDirectory()))
        self.setIpAddress(request.environ('REMOTE_ADDR'))
        for index in range(0, len(self.getSessionFiles()), 1):
            if self.getSessionFiles()[index].endswith(".json"):
                file_name = str(self.getDirectory() + "/" +
                                self.getSessionFiles()[index])
                file = open(file_name)
                data = json.load(file)
                if data['Client']['ip_address'] == session['Client']['ip_address']:
                    session = data
                    self.setSession(session)
        if session.get('Client') is not None:
            if session['Client']['ip_address'] == self.getIpAddress():
                self.setTimestamp(datetime.now())
                session['Client']['timestamp'] = self.getTimestamp()
            else:
                session.clear()
        else:
            self.createSession()
