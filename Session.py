# Importing the requirements for the system
from flask import session, request
from flask_session import Session
from datetime import datetime
import os


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

    def __init__(self) -> None:
        """
        Instanting the session's manager which will be set to the directory of the sessions so that it can operate as needed
        """

        self.setDirectory("/Cache/Session/Users")

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

    def createSession(self) -> None:
        """
        Creating the session

        Returns: (void): The session is created
        """

        self.setIpAddress(request.environ('REMOTE_ADDR'))
        self.setHttpClientIpAddress(request.environ('HTTP_CLIENT_IP'))
        self.setProxyIpAddress(request.environ('HTTP_X_FORWARDED_FOR'))
        self.setTimestamp(datetime.now())
        data = {
            "ip_address": self.getIpAddress(),
            "http_client_ip_address": self.getHttpClientIpAddress(),
            "proxy_ip_address": self.getProxyIpAddress(),
            "timestamp": self.getTimestamp()
        }
        session['Client'] = data
