import re
import os.path
from natsort import natsorted
from cinema import Cinema
from show import Show
from movie import Movie
from unknown import Unknown
from cinemaDirectory import CinemaDirectory


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

    # GETTERS
    #########

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
        self.parseCinemaPathsList(pathsList)
        return self.__unprocessedCinemaList

    def parseCinemaPathAndGetDirectoryObject(self, path: str) -> CinemaDirectory:
        pass

    # UTILITY
    #########

    def parseCinemaPathsList(self, pathsList: list[str] or str) -> None:
        """ Main method for this class. Performs all the processing on a passed list and separates Unknown, Cinema, and Cinema objects with errors into individual lists. """

        def addToDirectoryDictionary(dictionary: dict[str, CinemaDirectory], cinema: Cinema) -> None:
            if cinema.getNewDirectoryName() in dictionary:  # Search through keys to see if directory already exists
                dictionary[cinema.getNewDirectoryName()].append(cinema)
            else:
                dictionary[cinema.getNewDirectoryName()] = CinemaDirectory(cinema)

        if isinstance(pathsList, str):
            pathsList = [pathsList]

        pathsList = natsorted(pathsList)  # Sort list
        unprocessedCinemaDirectoryDictionary: dict[str, CinemaDirectory] = {}

        for path in pathsList:
            if os.path.isfile(path):
                cinema = self._createCinemaObject(path)
                # TODO mixed/missing tags between files of a directory are an issue

                addToDirectoryDictionary(unprocessedCinemaDirectoryDictionary, cinema)
            else:
                cinemaList = self._createCinemaObjectList(path)

                for cinema in cinemaList:
                    addToDirectoryDictionary(unprocessedCinemaDirectoryDictionary, cinema)

            # cinema = self._getCinema(path)

            # if isinstance(cinema, list):
            #     processedCinemaList += cinema
            # else:
            #     processedCinemaList.append(cinema)

        # self.__unprocessedCinemaList = processedCinemaList.copy()

        # Extract unknown files from passed list of paths
        # unknownCinemaList: list[Unknown] = []
        # for obj in processedCinemaList[:]:  # Works with a copy of the original list so that changes can be made to the original on the fly
        #     if isinstance(obj, Unknown):
        #         unknownCinemaList.append(obj)
        #         processedCinemaList.remove(obj)
        # self.__unknownCinemaList = unknownCinemaList

        # # Extract already-correct Cinema files from passed list
        # alreadyCorrectCinemaList: list[Cinema] = []
        # for obj in processedCinemaList[:]:
        #     if obj.hasCorrectFileName() and obj.hasCorrectDirectoryName():
        #         alreadyCorrectCinemaList.append(obj)
        #         processedCinemaList.remove(obj)
        # self.__alreadyCorrectCinemaList = alreadyCorrectCinemaList

        # Extract Cinema objects that contain errors from passed list
        # errorCinemaList: list[Cinema] = []
        # for obj in processedCinemaList[:]:
        #         if obj.hasError():
        #             errorCinemaList.append(obj)
        #             processedCinemaList.remove(obj)
        # self.__errorCinemaList = errorCinemaList

        # self.__processedCinemaList = processedCinemaList



    # def _getCinema(self, path: str) -> Cinema or list[Cinema]:
    #     """ Parse a single path in string form and return either a single concrete Cinema object, or a list of them,
    #     based on file/directory contents. """

    #     if os.path.isfile(path):
    #         return self._createCinemaObject(path)
    #     else:
    #         return self._createCinemaDirectoryObject(path)



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



    def _createCinemaObjectList(self, path: str) -> list[Cinema]:
        """ Parse a single directory and return a list of Cinema objects, or a single Unknown object if none exist.
        Does not recurse into subdirectories. """

        directoryContentsFileNames = os.listdir(path)  # returns only the file names (not full paths)
        cinemaList = []

        for fileName in directoryContentsFileNames:
            fileAbsolutePath = os.path.join(path, fileName)  # convert list items to full paths

            # Only process files (no recursion into directories)
            if os.path.isfile(fileAbsolutePath):
                cinema = self._createCinemaObject(fileAbsolutePath)

                if not isinstance(cinema, Unknown):
                    cinemaList.append(cinema)

        if len(cinemaList) == 0:
            return [Unknown(path, "No valid files in directory", isFile=False)]
        else:
            return cinemaList



    def __getCorrectedFileName(self, path: str) -> str:
        """ Process the original file name and return a cleaned string for continued processing. """

        # Replace . and _ with space
        # .'s that aren't preceded by a capital letter (F.B.I.)
        cleanFileName = re.sub(self.__dotsOrUnderscoresPattern, " ", path)

        # Remove any double (or more) spaces
        cleanFileName = re.sub(self.__doubleSpacesPattern, " ", cleanFileName)

        # Add spaces that should be there
        cleanFileName = re.sub(self.__missingSpacesPattern, r"\2 \3", cleanFileName)

        # Remove tags at beginning of file name
        cleanFileName = re.sub(self.__beginningTagsPattern, "", cleanFileName)

        return cleanFileName

    def __getPatternDictionary(self) -> dict:
        return self.__patternDictionary

    def __buildRecognizedPatterns(self) -> None:
        """ Build's the CinemaParser's required Pattern objects from the Cinema base class and its subclasses. """

        # Build the Cinema objects' concrete patterns list
        patternDictionary: dict = {}

        for subclass in Cinema.__subclasses__():
            pattern = subclass.getPattern()
            if pattern:  # exclude adding the Unknown subclass' pattern by omitting the None pattern returned by the Unknown subclass
                patternDictionary[pattern] = subclass

        if len(patternDictionary) == 0:
            raise ClassPatternsEmpty

        self.__patternDictionary = patternDictionary

        # Build the common patterns
        self.__resolutionPattern = re.compile(Cinema.getResolutionPattern())
        self.__encodingPattern = re.compile(Cinema.getEncodingPattern())

        self.__dotsOrUnderscoresPattern = re.compile(r"((?<![A-Z])\.|\.(?=[A-Z][a-z])|\.(?=[0-9])|_)")
        self.__doubleSpacesPattern = re.compile(r" {2,}")
        self.__missingSpacesPattern = re.compile(r"((\w)([([])|([])])(\w))")
        self.__beginningTagsPattern = re.compile(r"^\[.+?] ?")
        
        