from cinema import Cinema
import re


class Unknown(Cinema):
    """ An unrecognized file that was parsed from Cinema files. Can be treated as a file or directory. """

    __isFile: bool

    def __init__(self, path: str, error: str, isFile: bool):
        super().__init__(path)

        # required params
        self._error = error
        self.__isFile = isFile
        self._buildAttributes()

        # optional params
        self._resolution = None
        self._encoding = None

        # finalize object
        self._buildNewFileName()

    def updateFileName(self, passed: str) -> None:
        pass

    def getNewFileNameSimple(self) -> str:
        pass

    def getNewDir(self) -> None:
        pass

    def getOldDirPath(self) -> str:
        if self.__isFile:
            return self._oldDirPath
        else:
            return self._oldAbsPath

    @staticmethod
    def getPattern() -> re.Pattern:
        pass

    def _buildAttributes(self) -> None:
        pass

    def _buildNewFileName(self):
        self._newFileName = "INVALID"
