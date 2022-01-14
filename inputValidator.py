import os


class InputValidator:

    __numErrors: int = 0
    __errorsDict: dict[str, list[str]]
    __cinemaArgs: list[str] = []
    __backupArgs: list[str] = []

    def hasCinema(self) -> bool:
        return len(self.__cinemaArgs) > 0

    def hasBackup(self) -> bool:
        return len(self.__backupArgs) > 0

    def hasErrors(self) -> bool:
        return self.__numErrors > 0

    def doValidation(self, model: list[str]) -> None:
        """ Validate input by checking the paths to ensure they are both absolute and exist. """

        if len(model) == 0:
            raise ValueError("No passed arguments!")

        numErrors = 0
        backupList = []
        cinemaList = []
        pathsNotAbsolute = []
        pathsNotExist = []

        for path in model:
            if os.path.isabs(path):
                if os.path.exists(path):  # valid inputs
                    if os.path.isfile(path):
                        if os.path.splitext(path)[1] == ".pkl":
                            backupList.append(path)
                        else:
                            cinemaList.append(path)
                    else:
                        cinemaList.append(path)
                else:  # invalid inputs
                    numErrors += 1
                    pathsNotExist.append(path)
            else:
                numErrors += 1
                pathsNotAbsolute.append(path)

        if len(cinemaList) == 0 and len(backupList) == 0:
            raise ValueError("No passed arguments were valid!")

        if len(cinemaList) > 0:
            self.__cinemaArgs = cinemaList

        if len(backupList) > 0:
            self.__backupArgs = backupList

        self.__numErrors = numErrors

        errorsDict: dict[str, list[str]] = {}

        if len(pathsNotAbsolute) > 0:
            errorsDict["Not Absolute"] = pathsNotAbsolute

        if len(pathsNotExist) > 0:
            errorsDict["Not Exist"] = pathsNotExist

        self.__errorsDict = errorsDict

    def getNumErrors(self) -> int:
        return self.__numErrors

    def getErrorsDict(self) -> dict[str, list[str]]:
        return self.__errorsDict

    def getCinemaArgs(self) -> list[str]:
        """ Return the processed cinema paths list. """

        return self.__cinemaArgs

    def getBackupArgs(self) -> list[str]:
        """ Return the processed backup paths list. """

        return self.__backupArgs
