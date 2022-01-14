from abc import ABC, abstractmethod
import re
import os.path


class Cinema(ABC):
    """ Abstract Cinema class to be superseded by concrete objects. """

    # common attributes
    _parentDir: str
    __oldAbsPath: str
    __oldFileName: str
    __newFileName: str
    __fileExt: str
    __title: str
    __resolution: str or None
    __encoding: str or None
    __error: str or None = None

    def __init__(self, filePath: str):
        self.__oldAbsPath = filePath
        temp = os.path.split(filePath)
        self._parentDir = temp[0]

        tmp = os.path.splitext(temp[1])
        self.__oldFileName = tmp[0]
        self.__fileExt = tmp[1]

    ##########
    # CHECKS #
    ##########

    def __isChanged(self) -> bool:
        return self.getOldFileName() != self.getNewFileName()

    def hasError(self) -> bool:
        return self.__error is not None

    ###########
    # SETTERS #
    ###########

    def setError(self, msg: str) -> None:
        self.__error = msg

    # def __setAbsPath(self, passed: tuple) -> None:
    #     self.__absPath = passed

    def setNewFileName(self, passed: str) -> None:
        self.__newFileName = passed

    def _setTitle(self, passed: str) -> None:
        """ Set the title of the Cinema object. """

        # self.__title = passed[:-1]  # remove the trailing space that is always attached to the title group
        self.__title = self._capitalize(passed)

    def _setResolution(self, match: re.Match or None) -> None:
        """ Set the resolution of the Cinema object (e.g., 1080p). """

        if match is None:
            self.__resolution = None
        else:
            self.__resolution = match.group("resolution")

    def _setEncoding(self, match: re.Match or None) -> None:
        """ Set the encoding of the Cinema object (e.g., H.265). """

        if match is None:
            self.__encoding = None
        else:
            self.__encoding = match.group("encoding")

    ###########
    # GETTERS #
    ###########

    def getError(self) -> str:
        return self.__error

    def getParentDir(self):
        return self._parentDir

    def getOldAbsPath(self) -> str:
        return self.__oldAbsPath

    def getNewAbsPath(self) -> str:
        return f"{self.getParentDir()}\\{self.getNewFileName()}{self.getFileExt()}"

    def getOldFileName(self) -> str:
        return self.__oldFileName

    def getNewFileName(self) -> str:
        return self.__newFileName

    def getFileExt(self) -> str:
        return self.__fileExt

    def _getTitle(self) -> str:
        return self.__title

    def _getResolution(self) -> str:
        return self.__resolution

    def _getEncoding(self) -> str:
        return self.__encoding

    @staticmethod
    def getResolutionPattern() -> re.Pattern:
        """ Returns the Pattern object relating to resolution. """

        return re.compile(r"(?P<resolution>(480p|720p|1080p))")

    @staticmethod
    def getEncodingPattern() -> re.Pattern:
        """ Returns the Pattern object relating to encoding. """

        return re.compile(r"([xhH][ .]?)?(?P<encoding>26[45])")

    @staticmethod
    @abstractmethod
    def getPattern() -> re.Pattern:
        """ Returns a Pattern object to be used in identifying concrete subclass objects. """

    #########
    # OTHER #
    #########

    @abstractmethod
    def _buildAttributes(self, specificMatch: re.Match) -> None:
        """ Fill out a concrete class' attributes using a Match object specific to that class. """

    @abstractmethod
    def _buildNewFileName(self) -> None:
        """ Build a new file name based on the filled attributes. """

    def _doErrorCheck(self) -> None:
        if not self.__isChanged():
            self.setError("File is already correctly formatted.")

    def _capitalize(self, title: str) -> str:
        articles = ["a", "an", "the"]
        coordConjunctions = ["for", "and", "nor", "but", "yet"]
        prepositions = ["at", "by", "of", "to", "on", "with", "without"]
        lowerList = articles + coordConjunctions + prepositions

        wordList = title.split()
        numWords = len(wordList)
        if numWords > 0:
            wordList[0] = wordList[0][:1].upper() + wordList[0][1:]
            wordList[-1] = wordList[-1][:1].upper() + wordList[-1][1:]

        i = 1
        if numWords > 1:
            for _ in range(numWords - 1):
                if wordList[i].lower() in lowerList:
                    wordList[i] = wordList[i].lower()
                else:
                    wordList[i] = wordList[i][:1].upper() + wordList[i][1:]
                i += 1

        return " ".join(wordList)
