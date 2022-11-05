from cinema import Cinema
from view import View
from parser import Parser
from fileHandler import FileHandler
from databasePickle import DatabasePickle
from inputValidator import InputValidator


# todo make into package(s)


class Controller:
    """ The controller in the MVC architecture. """

    __parser = Parser()
    __database = DatabasePickle()
    __handler = FileHandler(__database)
    __validator = InputValidator()

    def __init__(self, model: list, view: View):
        self.__model = model
        self.__view = view

    def start(self) -> None:
        self.__view.start(self.__model, self)

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

    #############
    # VALIDATOR #
    #############

    def validate(self, model) -> None:
        self.__validator.doValidation(model)

    def getValidationNumErrors(self) -> int:
        return self.__validator.getNumErrors()

    def getValidationErrorDict(self) -> dict[str, list[str]]:
        return self.__validator.getErrorsDict()

    def hasValidatedCinemaArgs(self) -> bool:
        return self.__validator.hasCinema()

    def hasValidatedBackupArgs(self) -> bool:
        return self.__validator.hasBackup()

    def getCinemaArgs(self) -> list[str]:
        return self.__validator.getCinemaArgs()

    def getBackupArgs(self) -> list[str]:
        return self.__validator.getBackupArgs()
