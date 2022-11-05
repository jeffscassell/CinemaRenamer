import re
import os.path
from natsort import natsorted
from cinema import Cinema
from show import Show
from movie import Movie
from unknown import Unknown


class ClassPatternsEmpty(Exception):
    """ If the concrete subclass patterns cannot be created, this error is raised. """
    pass


class Parser:
    """ Parses passed path strings for relevant Cinema objects by matching against Cinema patterns. """

    __patternDict: dict[re.Pattern, object]  # {pattern: class, ...}
    __resolutionPattern: re.Pattern
    __encodingPattern: re.Pattern
    __spacingPattern: re.Pattern
    __doubleSpacesPattern: re.Pattern
    __missingSpacesPattern: re.Pattern
    __beginningTagsPattern: re.Pattern

    __unprocessedList: list[Cinema]
    __unknownList: list[Unknown]
    __alreadyCorrectList: list[Cinema]
    # __errorList: list[Cinema]
    __processedCinemaList: list[Cinema]

    def __init__(self):
        self.__buildPatterns()

    ###########
    # GETTERS #
    ###########

    def getUnprocessedList(self) -> list[Cinema]:
        return self.__unprocessedList

    def getUnknownCinemaList(self) -> list[Unknown]:
        return self.__unknownList

    def getAlreadyCorrectCinemaList(self) -> list[Cinema]:
        return self.__alreadyCorrectList

    # def getErrorCinemaList(self) -> list[Cinema]:
    #     return self.__errorList

    def getProcessedCinemaList(self) -> list[Cinema]:
        return self.__processedCinemaList



    def parseAndGetList(self, pathList: list[str] or str) -> list[Cinema]:
        self.parseCinemaPaths(pathList)
        return self.getUnprocessedList()

    def parseCinemaPaths(self, pathList: list[str] or str) -> None:
        """ Main method for this class. Performs all the processing on a passed list and extracts Unknown, Cinema, and Cinema objects with errors into separate lists. """

        if isinstance(pathList, str):
            pathList = [pathList]

        pathList = natsorted(pathList)  # sort list
        cinemaList: list[Cinema] = []

        for path in pathList:
            cinema = self._getCinema(path)

            if isinstance(cinema, list):
                cinemaList += cinema
            else:
                cinemaList.append(cinema)

        self.__unprocessedList = cinemaList.copy()

        # Extract unknown files from passed list of paths
        unknownList: list[Unknown] = []
        for obj in cinemaList[:]:
            if isinstance(obj, Unknown):
                unknownList.append(obj)
                cinemaList.remove(obj)
        self.__unknownList = unknownList

        # Extract already-correct Cinema files from passed list
        alreadyCorrectList: list[Cinema] = []
        for obj in cinemaList[:]:
            if obj.hasCorrectFileName() and obj.hasCorrectDirName():
                alreadyCorrectList.append(obj)
                cinemaList.remove(obj)
        self.__alreadyCorrectList = alreadyCorrectList

        # Extract Cinema objects that contain errors from passed list
        # errorList: list[Cinema] = []
        # for obj in cinemaList[:]:
        #         if obj.hasError():
        #             errorList.append(obj)
        #             cinemaList.remove(obj)
        # self.__errorList = errorList

        self.__processedCinemaList = cinemaList

    def _getCinema(self, path: str) -> Cinema or list[Cinema]:
        """ Parse a single path in string form and return either a single concrete Cinema object, or a list of them,
        based on file/directory contents. """

        if os.path.isfile(path):
            return self._getCinemaFile(path)
        else:
            return self._getCinemaDir(path)

    def _getCinemaFile(self, passed: str) -> Cinema:
        """ Parse a single file and return a single Cinema object. """

        absPath = os.path.split(passed)
        temp = os.path.splitext(absPath[1])  # file name
        fileName = temp[0]  # file name without extension

        cleaned = self.__getCleanFileName(fileName)

        for pattern, cls in self.__getPatternDict().items():
            specificMatch = pattern.search(cleaned)

            if specificMatch:
                resolutionMatch = self.__getResolutionPattern().search(cleaned)
                encodingMatch = self.__getEncodingPattern().search(cleaned)

                return cls(passed, specificMatch, resolutionMatch, encodingMatch)

        return Unknown(passed, "Not a recognized Cinema file", isFile=True)

    def _getCinemaDir(self, path: str) -> list[Cinema]:
        """ Parse a single directory and return a list of Cinema objects, or a single Unknown object if none exist.
        Does not recurse into subdirectories. """

        dirContents = os.listdir(path)  # returns only the file names (not full paths)
        returnList = []

        for item in dirContents:
            itemPath = os.path.join(path, item)  # convert list items to full paths

            # only process files (no recursion into directory trees)
            if os.path.isfile(itemPath):
                cinema = self._getCinemaFile(itemPath)

                if not isinstance(cinema, Unknown):
                    returnList.append(cinema)

        if len(returnList) == 0:
            return [Unknown(path, "No valid files in directory", isFile=False)]
        else:
            return returnList

    def __getCleanFileName(self, path: str) -> str:
        """ Process the original file name and return a cleaned string for continued processing. """

        # replace . and _ with space
        # .'s that aren't preceded by a capital letter (F.B.I.)
        cleanFileName = re.sub(self.__spacingPattern, " ", path)

        # remove any double spaces (or more)
        cleanFileName = re.sub(self.__doubleSpacesPattern, " ", cleanFileName)

        # add spaces that should be there
        cleanFileName = re.sub(self.__missingSpacesPattern, r"\2 \3", cleanFileName)

        # remove tags at beginning of file name
        cleanFileName = re.sub(self.__beginningTagsPattern, "", cleanFileName)

        return cleanFileName

    def __getPatternDict(self) -> dict:
        return self.__patternDict

    def __getEncodingPattern(self) -> re.Pattern:
        return self.__encodingPattern

    def __getResolutionPattern(self) -> re.Pattern:
        return self.__resolutionPattern

    def __buildPatterns(self) -> None:
        """ Build's the CinemaParser's required Pattern objects from the Cinema base class and its subclasses. """

        self.__buildConcretePatternList()
        self.__buildStandardPatterns()

    def __buildConcretePatternList(self) -> None:
        """ Build the concrete Cinema object pattern list from the Cinema subclasses. """

        patternDict: dict = {}

        for cls in Cinema.__subclasses__():
            pattern = cls.getPattern()
            if pattern:  # account for Unknown class by omitting None pattern returned by Unknown class
                patternDict[pattern] = cls

        if len(patternDict) == 0:
            raise ClassPatternsEmpty

        self.__patternDict = patternDict

    def __buildStandardPatterns(self) -> None:
        """ Build the common patterns from the Cinema base class. """

        self.__resolutionPattern = re.compile(Cinema.getResolutionPattern())
        self.__encodingPattern = re.compile(Cinema.getEncodingPattern())

        self.__spacingPattern = re.compile(r"((?<![A-Z])\.|\.(?=[A-Z][a-z])|\.(?=[0-9])|_)")
        self.__doubleSpacesPattern = re.compile(r" {2,}")
        self.__missingSpacesPattern = re.compile(r"((\w)([([])|([])])(\w))")
        self.__beginningTagsPattern = re.compile(r"^\[.+?] ?")
