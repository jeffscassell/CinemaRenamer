from cinema import Cinema
from view import View
from cinemaParser import CinemaParser
from configparser import ConfigParser
from fileHandler import FileHandler
from databasePickle import DatabasePickle
from inputValidator import InputValidator
import os
from settingsHandler import SettingsHandler
from cinemaDirectory import CinemaDirectory


# TODO make into package(s)


class Controller:
    """ The controller in the MVC architecture. """

    __parser = CinemaParser()
    __database = DatabasePickle()
    __fileHandler = FileHandler(__database)
    __validator = InputValidator()
    settingsHandler = SettingsHandler()

    def __init__(self, model: list, view: View):
        self.__model = model
        self.__view = view
        self.settingsHandler.loadSettingsFile()
        # self.__fileHandler.loadDatabase()

    def start(self) -> None:
        self.__view.start(self.__model, self)

    ##########
    # PARSER #
    ##########

    def parseCinemaPathsList(self, model: list[str] or str) -> None:
        self.__parser.parseCinemaPathsList(model)

    def getProcessedCinemaList(self) -> list[Cinema]:
        return self.__parser.getProcessedCinemaList()

    def getUnknownCinemaList(self) -> list[Cinema]:
        return self.__parser.getUnknownCinemaList()

    def getAlreadyCorrectCinemaList(self) -> list[Cinema]:
        return self.__parser.getAlreadyCorrectCinemaList()

    # def getErrorCinemaList(self) -> list[Cinema]:
    #     return self.__parser.getErrorCinemaList()

    ############
    # HANDLERS #
    ############

    # FILE #

    def checkDirectoryExistsInLibrary(self, cinemaDirectory: CinemaDirectory) -> bool:
        pass

    def getBackupsDirectory(self) -> str:
        return self.__database.getBackupsAbsPath()

    def backup(self, obj: Cinema) -> None:  # throws ValueError if name is unchanged
        """ Create database record of Cinema object. """

        self.__fileHandler.backup(obj)

    def backupOverwrite(self, obj: Cinema) -> None:
        self.__fileHandler.backupOverwrite(obj)

    def backupAppend(self, obj: Cinema) -> None:
        self.__fileHandler.backupAppend(obj)

    def deleteBackup(self, obj: Cinema) -> None:
        self.__fileHandler.deleteBackup(obj)

    def renameCinema(self, obj: Cinema) -> None:
        """ Rename the Cinema object's file. """
        
        self.__fileHandler.renameCinema(obj)
    
    def integrateIntoLibrary(self, obj: Cinema, library: str, copyFlag: bool, overwriteFlag: bool) -> None:
        """ The object file is integrated into the provided library directory. The copy flag indicates if the file is meant to be copied from the original directory into the new one, or moved.
            The overwrite flag indicates if the file is to be overwritten when a conflict exists, or skipped. """

        self.__fileHandler.integrateIntoLibrary(obj, library, copyFlag, overwriteFlag)

    def readObjFromBackup(self, path: str) -> Cinema:
        return self.__fileHandler.readObjFromBackup(path)

    def restoreBackupObj(self, obj: str) -> None:
        self.__fileHandler.restoreBackupObj(obj)

    def buildLibraries(self) -> None:
        pass

    # DATABASE

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
