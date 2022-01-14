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

    def getParsedCinemaObjs(self, model: list[str]) -> list[Cinema]:
        return self.__parser.getCinemaList(model)

    ###########
    # HANDLER #
    ###########

    def getBackupDir(self) -> str:
        return self.__database.getBackupAbsPath()

    def rename(self, obj: Cinema) -> None:
        self.__handler.rename(obj)

    def getCinemaObjFromBackup(self, path: str) -> Cinema:
        return self.__handler.getCinemaObjFromBackup(path)

    def restore(self, path: str) -> None:
        self.__handler.restore(path)

    #############
    # VALIDATOR #
    #############

    def doValidation(self, model) -> None:
        self.__validator.doValidation(model)

    def checkForValidationErrors(self) -> bool:
        return self.__validator.hasErrors()

    def getValidationErrorNum(self) -> int:
        return self.__validator.getNumErrors()

    def getValidationErrorDict(self) -> dict[str, list[str]]:
        return self.__validator.getErrorsDict()

    def hasCinemaArgs(self) -> bool:
        return self.__validator.hasCinema()

    def hasBackupArgs(self) -> bool:
        return self.__validator.hasBackup()

    def getCinemaArgs(self) -> list[str]:
        return self.__validator.getCinemaArgs()

    def getBackupArgs(self) -> list[str]:
        return self.__validator.getBackupArgs()
