from cinema import Cinema
from view import View
from cinemaParser import CinemaParser
from configparser import ConfigParser
from fileHandler import FileHandler
from databasePickle import DatabasePickle
from inputValidator import InputValidator
import os


# TODO make into package(s)


class Controller:
    """ The controller in the MVC architecture. """

    __parser = CinemaParser()
    __database = DatabasePickle()
    __handler = FileHandler(__database)
    __validator = InputValidator()

    movieLibraryDirectory: str
    showLibraryDirectory: str
    copyFlag: bool
    overwriteFlag: bool

    def __init__(self, model: list, view: View):
        self.__model = model
        self.__view = view
        self.__loadSettings()

    def start(self) -> None:
        self.__view.start(self.__model, self)

    ############
    # SETTINGS #
    ############

    def __loadSettings(self) -> None:

        def tryReadingLibrary(passed: str) -> str:
            try:
                return config.get("libraries", passed, raw=True)  # Raw removes the need to surround the directory in quotes to handle spaces
            except Exception:
                return None
        
        def tryReadingFlag(passed: str) -> bool:
            try:
                return config.getboolean("flags", passed)
            except Exception:
                return None
        
        settingsFile = "cr_config.ini"
        config = ConfigParser()

        if os.path.exists(settingsFile) and os.path.getsize(settingsFile) > 0:  # Config file exists and is not empty. Load settings
            config.read(settingsFile)

            # Libraries
            self.movieLibraryDirectory = tryReadingLibrary("movies")
            self.showLibraryDirectory = tryReadingLibrary("shows")

            # Flags
            self.copyFlag = tryReadingFlag("copy")
            self.overwriteFlag = tryReadingFlag("overwrite")
        else:  # Create empty config file
            config.add_section("libraries")
            config.set("libraries", "shows", "")
            config.set("libraries", "movies", "")
            config.add_section("flags")
            config.set("flags", "copy", "true")
            config.set("flags", "overwrite", "true")
            with open(settingsFile, "w") as outp:
                config.write(outp)

    ##########
    # PARSER #
    ##########

    def parseCinemaPaths(self, model: list[str] or str) -> None:
        self.__parser.parseCinemaPaths(model)

    def getProcessedCinemaList(self) -> list[Cinema]:
        return self.__parser.getProcessedCinemaList()

    def getUnknownCinemaList(self) -> list[Cinema]:
        return self.__parser.getUnknownCinemaList()

    def getAlreadyCorrectCinemaList(self) -> list[Cinema]:
        return self.__parser.getAlreadyCorrectCinemaList()

    # def getErrorCinemaList(self) -> list[Cinema]:
    #     return self.__parser.getErrorCinemaList()

    ###########
    # HANDLER #
    ###########

    def getBackupsDir(self) -> str:
        return self.__database.getBackupsAbsPath()

    def backup(self, obj: Cinema) -> None:  # throws ValueError if name is unchanged
        """ Create database record of Cinema object. """

        self.__handler.backup(obj)

    def backupOverwrite(self, obj: Cinema) -> None:
        self.__handler.backupOverwrite(obj)

    def backupAppend(self, obj: Cinema) -> None:
        self.__handler.backupAppend(obj)

    def deleteBackup(self, obj: Cinema) -> None:
        self.__handler.deleteBackup(obj)

    def rename(self, obj: Cinema) -> None:
        """ Rename the Cinema object's file. """
        
        self.__handler.rename(obj)
    
    def integrateIntoLibrary(self, obj: Cinema, library: str, copyFlag: bool, overwriteFlag: bool) -> None:
        """ The object file is integrated into the provided library directory. The copy flag indicates if the file is meant to be copied from the original directory into the new one, or moved.
            The overwrite flag indicates if the file is to be overwritten when a conflict exists, or skipped. """

        self.__handler.integrateIntoLibrary(obj, library, copyFlag, overwriteFlag)

    def readObjFromBackup(self, path: str) -> Cinema:
        return self.__handler.readObjFromBackup(path)

    def restoreBackupObj(self, obj: str) -> None:
        self.__handler.restoreBackupObj(obj)

    def buildLibraries(self) -> None:
        pass

    #############
    # VALIDATOR #
    #############

    def validate(self, model) -> None:
        self.__validator.doValidation(model)

    # def getNumberOfValidationErrors(self) -> int:
    #     return self.__validator.getNumErrors()

    def getValidationErrorsDictionary(self) -> dict[str, list[str]]:
        return self.__validator.getValidationErrorsDictionary()

    def hasValidatedCinemaArgs(self) -> bool:
        return self.__validator.hasCinema()

    def hasValidatedBackupArgs(self) -> bool:
        return self.__validator.hasBackup()

    def getCinemaArguments(self) -> list[str]:
        return self.__validator.getCinemaArguments()

    def getBackupArguments(self) -> list[str]:
        return self.__validator.getBackupArguments()
