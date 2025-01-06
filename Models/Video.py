"""
The module that will contain the model of the Videos.

Authors:
    Darkness4869
"""
class Video:
    """
    It will handle any I/O operations that are related with the
    video contents as well as the databases operations.
    """
    __identifier: str
    """
    The identifier of the video
    """

    def getIdentifier(self) -> str:
        return self.__identifier

    def setIdentifier(self, identifier: str) -> None:
        self.__identifier = identifier