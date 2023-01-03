from abc import ABC, abstractmethod
import re
import os.path


class Cinema(ABC):
    """ Abstract Cinema class to be superseded by concrete objects. """

    # Required attributes
    _oldDirectory: str  # c:\directory\[directory]\file.ext
    _newDirectory: str
    _oldDirectoryPath: str  # [c:\directory\directory]\file.ext
    _newDirectoryPath: str
    _oldAbsolutePath: str  # [c:\directory\directory\file.ext]
    _oldFileName: str  # c:\directory\directory\[file].ext
    _newFileName: str
    _fileExtension: str  # .ext
    _backupName: str  # newParentDirectory.file.ext
    _isMovie: bool = False
    _isShow: bool = False
    _needsIntegration: bool = True

    _title: str
    _resolution: str or None  # 1080p
    _encoding: str or None  # 265
    # _error: str or None = None

    def __init__(self, filePath: str):
        self._oldAbsolutePath = filePath
        self._oldDirectoryPath = os.path.dirname(filePath)
        self._oldDirectory = os.path.split(self._oldDirectoryPath)[1]

        tmp = os.path.splitext(os.path.basename(filePath))
        self._oldFileName = tmp[0]
        self._fileExtension = tmp[1]

    ##########
    # CHECKS #
    ##########

    # def hasError(self) -> bool:
    #     return self._error is not None

    def hasCorrectFileName(self) -> bool:
        return self._oldFileName == self._newFileName
    
    def hasCorrectDirectoryName(self) -> bool:
        return self._oldDirectory == self._newDirectory
    
    def needsIntegration(self) -> bool:
        return self._needsIntegration

    def isMovie(self) -> bool:
        return self._isMovie
    
    def isShow(self) -> bool:
        return self._isShow

    ###########
    # SETTERS #
    ###########

    # def setError(self, msg: str) -> None:
    #     self._error = msg

    @abstractmethod
    def updateFileName(self, passed: str) -> None:
        """ Changes the new file name, but also changes the backup name. """

    def updateFileNameSimple(self, passed: str) -> None:
        self.updateFileName(f"{passed}{self._getTags()}")

    def setBackupName(self, passed: str) -> None:
        self._backupName = passed

    def setNewDirectoryPath(self, passed: str) -> None:
        self._newDirectoryPath = passed

    def setIntegrationFalse(self) -> None:
        self._needsIntegration = False

    def _setTitle(self, passed: str) -> None:
        """ Set the title of the Cinema object. """

        # self._title = passed[:-1]  # remove the trailing space that is always attached to the title group
        self._title = self._capitalize(passed)

    def _setResolution(self, match: re.Match or None) -> None:
        """ Set the resolution of the Cinema object (e.g., 1080p). """

        if match is None:
            self._resolution = None
        else:
            self._resolution = match.group("resolution")

    def _setEncoding(self, match: re.Match or None) -> None:
        """ Set the encoding of the Cinema object (e.g., H.265). """

        if match is None:
            self._encoding = None
        else:
            self._encoding = match.group("encoding")

    ###########
    # GETTERS #
    ###########

    # def getError(self) -> str:
    #     return self._error

    def getOldDirectory(self) -> str:  # c:\\[folder]\\name.ext
        return self._oldDirectory

    @abstractmethod    
    def getNewDirectory(self) -> str:
        pass

    def getOldDirectoryPath(self) -> str:  # [c:\\folder]\\name.ext
        return self._oldDirectoryPath

    def getNewDirectoryPath(self) -> str:
        return self._newDirectoryPath

    def getOldAbsolutePath(self) -> str:  # [c:\\folder\\name.ext]
        return self._oldAbsolutePath

    def getNewAbsolutePath(self) -> str:
        return f"{self._oldDirectoryPath}\\{self._newFileName}{self._fileExtension}"

    def getOldFileName(self) -> str:
        return self._oldFileName

    def getNewFileName(self) -> str:
        return self._newFileName
    
    @abstractmethod
    def getNewFileNameSimple(self) -> str:
        pass

    def getBackupName(self) -> str:  # c:\\[folder.name.ext]
        return self._backupName

    def getFileExtension(self) -> str:
        return self._fileExtension

    def _getTitle(self) -> str:
        return self._title

    def _getResolution(self) -> str:
        return self._resolution

    def _getEncoding(self) -> str:
        return self._encoding

    def _getTags(self) -> str:
        tags = ""

        if self._resolution:
            tags += f" [{self._resolution}]"
        
        if self._encoding:
            tags += f" [x{self._encoding}]"

        return tags

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

    @staticmethod
    def _capitalize(title: str) -> str:

        def uppercaseFirstAndLastWordsInTitle() -> None:
            if numberOfWords > 0:
                titleWordList[0] = titleWordList[0][:1].upper() + titleWordList[0][1:]
                titleWordList[-1] = titleWordList[-1][:1].upper() + titleWordList[-1][1:]

        def lowercaseOrUppercaseRelevantWordsInTitle() -> None:
            i = 1  # skip the first word in the title
            if numberOfWords > 2:
                for _ in range(numberOfWords - 2):  # skip the last word in the title
                    if titleWordList[i].lower() in lowercaseList:
                        titleWordList[i] = titleWordList[i].lower()
                    else:
                        titleWordList[i] = titleWordList[i][:1].upper() + titleWordList[i][1:]
                    i += 1

        articles = ["a", "an", "the"]
        coordConjunctions = ["for", "and", "but", "yet", "or", "nor", "if", "vs"]
        prepositions = ["as", "at", "by", "of", "to", "on", "off", "with", "without", "in", "per", "via"]
        lowercaseList = articles + coordConjunctions + prepositions

        titleWordList = title.split()
        numberOfWords = len(titleWordList)

        uppercaseFirstAndLastWordsInTitle()
        lowercaseOrUppercaseRelevantWordsInTitle()

        return " ".join(titleWordList)
