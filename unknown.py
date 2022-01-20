from cinema import Cinema
import re


class Unknown(Cinema):
    """ An unrecognized file that was parsed from Cinema files. Can be treated as a file or directory. """

    __isFile: bool

    def __init__(self, path: str, error: str, isFile: bool):
        super().__init__(path)

        # required params
        self.setError(error)
        self.__isFile = isFile
        self._buildAttributes()

        # optional params
        self._setResolution(None)
        self._setEncoding(None)

        # finalize object
        self._buildNewFileName()
        self._doErrorCheck()

    def parentDir(self) -> str:
        if self.__isFile:
            return self._parentDir
        else:
            return self.getOldAbsPath()

    @staticmethod
    def getPattern() -> re.Pattern:
        pass

    def _buildAttributes(self) -> None:
        pass

    def _buildNewFileName(self):
        self.setNewFileName("INVALID")

    def _doErrorCheck(self) -> None:
        pass
