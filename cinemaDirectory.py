from abc import ABC, abstractmethod
from cinema import Cinema


class CinemaDirectory():
    """ Container for Cinema objects. """

    __name: str
    __libraryPath: str
    # __tags: str
    __cinemaList: list[Cinema]
    __cinemaErrorList: list[Cinema] = []

    def __init__(self, cinema: Cinema) -> None:
        self.__name = cinema.getNewDirectoryName()
        self.__cinemaList = [cinema]

    # UTILITY
    #########
    
    def hasError(self) -> bool:
        if len(self.__cinemaErrorList) > 0:
            return True
        else:
            return False

    def append(self, cinema: Cinema) -> None:
        self.__cinemaList.append(cinema)

    def remove(self, cinema: Cinema) -> None:
        self.__cinemaList.remove(cinema)

    def clearCinemaError(self, cinema: Cinema) -> None:
        self.__cinemaList[cinema].clearError()
        self.__cinemaErrorList.remove(cinema)

    def changeDirectoryName(self, passed: str) -> None:
        self.__name = passed

    # GETTERS
    #########
    
    def getName(self) -> str:
        return self.__name

    def getLibraryPath(self) -> str:
        return self.__libraryPath

    def getCinemaList(self) -> list[Cinema]:
        return self.__cinemaList

    def getCinemaErrorList(self) -> list[Cinema]:
        return self.__cinemaList

    def getErrorCount(self) -> int:
        return len(self.__cinemaErrorList)
    
    def getTags(self) -> str:
        return self.__tags

    # SETTERS
    #########

    def setName(self, passed: str) -> None:
        self.__name = passed

    def setCinemaError(self, cinema: Cinema, errorMessage: str) -> None:
        self.__cinemaList[cinema].setError(errorMessage)
        self.__cinemaErrorList.append(cinema)

    def setLibraryPath(self, passed: str) -> None:
        self.__libraryPath = passed
