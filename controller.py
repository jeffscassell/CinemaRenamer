from cinema import Cinema
from view import View
from cinemaParser import Parser
from handler import Handler
from databasePickle import DatabasePickle
from inputValidator import InputValidator


# todo make into package(s)


class Controller:
    """ The controller in the MVC architecture. """

    __parser = Parser()
    __database = DatabasePickle()
    __handler = Handler(__database)
    __validator = InputValidator()

    def __init__(self, model: list, view: View):
        self.__model = model
        self.__view = view

    def start(self) -> None:
        self.__view.start(self.__model, self)

    ##########
    # PARSER #
    ##########

    def parseCinemaPaths(self, model: list[str]) -> None:
        self.__parser.parseCinemaPaths(model)

    def getGoodCinemaList(self) -> list[Cinema]:
        return self.__parser.getUnprocessedCinemaList()

    def getUnknownCinemaList(self) -> list[Cinema]:
        return self.__parser.getUnknownCinemaList()

    def getErrorCinemaList(self) -> list[Cinema]:
        return self.__parser.getErrorCinemaList()

    ###########
    # HANDLER #
    ###########

    def getBackupDir(self) -> str:
        return self.__database.getBackupAbsPath()

    def rename(self, obj: Cinema) -> None:
        self.__handler.createBackupAndRename(obj)

    def readCinemaFromBackup(self, path: str) -> Cinema:
        return self.__handler.readCinemaFromBackup(path)

    def restoreFromBackup(self, path: str) -> None:
        self.__handler.restoreFromBackup(path)

    #############
    # VALIDATOR #
    #############

    def validate(self, model) -> None:
        self.__validator.doValidation(model)

    def hasValidationErrors(self) -> bool:
        return self.__validator.hasErrors()

    def getValidationErrorNum(self) -> int:
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
