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


class CinemaParser:
    """ Parses passed path strings for relevant Cinema objects by matching against Cinema patterns. """

    # Concrete objects patterns
    __patternDictionary: dict[re.Pattern, object]  # {pattern: class, ...}

    # Common patterns
    __resolutionPattern: re.Pattern
    __encodingPattern: re.Pattern

    # Corrected file name patterns
    __dotsOrUnderscoresPattern: re.Pattern
    __doubleSpacesPattern: re.Pattern
    __missingSpacesPattern: re.Pattern
    __beginningTagsPattern: re.Pattern

    # Outputted Lists
    __unprocessedCinemaList: list[Cinema]
    __unprocessedCinemaDirectoryList: list[CinemaDirectory]
    __unknownCinemaList: list[Unknown]
    __alreadyCorrectCinemaList: list[Cinema]
    # __errorCinemaList: list[Cinema]
    __processedCinemaList: list[Cinema]

    def __init__(self):
        self.__buildRecognizedPatterns()

    ###########
    # GETTERS #
    ###########

    def getUnprocessedCinemaList(self) -> list[Cinema]:
        return self.__unprocessedCinemaList

    def getUnknownCinemaList(self) -> list[Unknown]:
        return self.__unknownCinemaList

    def getAlreadyCorrectCinemaList(self) -> list[Cinema]:
        return self.__alreadyCorrectCinemaList

    # def getErrorCinemaList(self) -> list[Cinema]:
    #     return self.__errorCinemaList

    def getProcessedCinemaList(self) -> list[Cinema]:
        return self.__processedCinemaList

    def parseAndGetUnprocessedCinemaList(self, pathsList: list[str] or str) -> list[Cinema]:
        self.parseCinemaPaths(pathsList)
        return self.__unprocessedCinemaList

    def parseCinemaPaths(self, pathsList: list[str] or str) -> None:
        """ Main method for this class. Performs all the processing on a passed list and extracts Unknown, Cinema, and Cinema objects with errors into separate lists. """

        if isinstance(pathsList, str):
            pathsList = [pathsList]

        pathsList = natsorted(pathsList)  # sort list
        processedCinemaList: list[Cinema] = []

        for path in pathsList:
            cinema = self._getCinema(path)

            if isinstance(cinema, list):
                processedCinemaList += cinema
            else:
                processedCinemaList.append(cinema)

        self.__unprocessedCinemaList = processedCinemaList.copy()

        # Extract unknown files from passed list of paths
        unknownCinemaList: list[Unknown] = []
        for obj in processedCinemaList[:]:  # Works with a copy of the original list so that changes can be made to the original on the fly
            if isinstance(obj, Unknown):
                unknownCinemaList.append(obj)
                processedCinemaList.remove(obj)
        self.__unknownCinemaList = unknownCinemaList

        # Extract already-correct Cinema files from passed list
        alreadyCorrectCinemaList: list[Cinema] = []
        for obj in processedCinemaList[:]:
            if obj.hasCorrectFileName() and obj.hasCorrectDirectoryName():
                alreadyCorrectCinemaList.append(obj)
                processedCinemaList.remove(obj)
        self.__alreadyCorrectCinemaList = alreadyCorrectCinemaList

        # Extract Cinema objects that contain errors from passed list
        # errorCinemaList: list[Cinema] = []
        # for obj in processedCinemaList[:]:
        #         if obj.hasError():
        #             errorCinemaList.append(obj)
        #             processedCinemaList.remove(obj)
        # self.__errorCinemaList = errorCinemaList

        self.__processedCinemaList = processedCinemaList

    def _getCinema(self, path: str) -> Cinema or list[Cinema]:
        """ Parse a single path in string form and return either a single concrete Cinema object, or a list of them,
        based on file/directory contents. """

        if os.path.isfile(path):
            return self._createCinemaObject(path)
        else:
            return self._getCinemaDir(path)

    def _createCinemaObject(self, passed: str) -> Cinema:
        """ Parse a single file path and return a single Cinema object. """

        passedAbsolutePathPlusFile = os.path.split(passed)
        fileNamePlusExtension = os.path.splitext(passedAbsolutePathPlusFile[1])  # extracting the file name plus extension
        fileName = fileNamePlusExtension[0]  # file name without extension

        correctedFileName = self.__getCorrectedFileName(fileName)

        for pattern, subclass in self.__getPatternDictionary().items():
            patternMatchFound = pattern.search(correctedFileName)  # Unknown Cinema has no Pattern and will return no match for a search

            if patternMatchFound:
                resolutionMatch = self.__resolutionPattern.search(correctedFileName)
                encodingMatch = self.__encodingPattern.search(correctedFileName)

                return subclass(passed, patternMatchFound, resolutionMatch, encodingMatch)

        return Unknown(passed, "Not a recognized Cinema file", isFile=True)

    def _getCinemaDir(self, path: str) -> list[Cinema]:
        """ Parse a single directory and return a list of Cinema objects, or a single Unknown object if none exist.
        Does not recurse into subdirectories. """

        directoryContentsFileNames = os.listdir(path)  # returns only the file names (not full paths)
        returnList = []

        for fileName in directoryContentsFileNames:
            itemPath = os.path.join(path, fileName)  # convert list items to full paths

            # only process files (no recursion into directory trees)
            if os.path.isfile(itemPath):
                cinema = self._createCinemaObject(itemPath)

                if not isinstance(cinema, Unknown):
                    returnList.append(cinema)

        if len(returnList) == 0:
            return [Unknown(path, "No valid files in directory", isFile=False)]
        else:
            return returnList

    def __getCorrectedFileName(self, path: str) -> str:
        """ Process the original file name and return a cleaned string for continued processing. """

        # replace . and _ with space
        # .'s that aren't preceded by a capital letter (F.B.I.)
        cleanFileName = re.sub(self.__dotsOrUnderscoresPattern, " ", path)

        # remove any double spaces (or more)
        cleanFileName = re.sub(self.__doubleSpacesPattern, " ", cleanFileName)

        # add spaces that should be there
        cleanFileName = re.sub(self.__missingSpacesPattern, r"\2 \3", cleanFileName)

        # remove tags at beginning of file name
        cleanFileName = re.sub(self.__beginningTagsPattern, "", cleanFileName)

        return cleanFileName

    def __getPatternDictionary(self) -> dict:
        return self.__patternDictionary

    def __buildRecognizedPatterns(self) -> None:
        """ Build's the CinemaParser's required Pattern objects from the Cinema base class and its subclasses. """

        self.__buildConcretePatternList()
        self.__buildCommonPatterns()

    def __buildConcretePatternList(self) -> None:
        """ Build the concrete Cinema object pattern list from the Cinema subclasses. """

        patternDictionary: dict = {}

        for subclass in Cinema.__subclasses__():
            pattern = subclass.getPattern()
            if pattern:  # exclude adding the Unknown subclass' pattern by omitting the None pattern returned by the Unknown subclass
                patternDictionary[pattern] = subclass

        if len(patternDictionary) == 0:
            raise ClassPatternsEmpty

        self.__patternDictionary = patternDictionary

    def __buildCommonPatterns(self) -> None:
        """ Build the common patterns from the Cinema base class. """

        self.__resolutionPattern = re.compile(Cinema.getResolutionPattern())
        self.__encodingPattern = re.compile(Cinema.getEncodingPattern())

        self.__dotsOrUnderscoresPattern = re.compile(r"((?<![A-Z])\.|\.(?=[A-Z][a-z])|\.(?=[0-9])|_)")
        self.__doubleSpacesPattern = re.compile(r" {2,}")
        self.__missingSpacesPattern = re.compile(r"((\w)([([])|([])])(\w))")
        self.__beginningTagsPattern = re.compile(r"^\[.+?] ?")
