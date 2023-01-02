import os


class InputValidator:
    """ Performs simple input validation on passed arguments. Must be an absolute path and exist.
    Valid files with extension '.pkl', valid files/directories, and all invalid inputs are stored in separate lists. """

    __errorsDictionary: dict[str, list[str]]
    __cinemaArgs: list[str] = []
    __backupArgs: list[str] = []
    # __copyFlag: bool = True
    # __overwriteFlag: bool = True

    def hasCinema(self) -> bool:
        return len(self.__cinemaArgs) > 0

    def hasBackup(self) -> bool:
        return len(self.__backupArgs) > 0

    def doValidation(self, model: list[str]) -> None:
        """ Validate input by checking the paths to ensure they are both absolute and exist. """

        if len(model) == 0:
            raise ValueError("NO PASSED ARGUMENTS")

        backupList = []
        cinemaList = []
        pathsNotAbsolute = []
        pathsNonexistent = []

        for path in model:
            if os.path.isabs(path):
                if os.path.exists(path):  # valid inputs
                    if os.path.isfile(path):
                        if os.path.splitext(path)[1] == ".pkl":
                            backupList.append(path)
                        else:
                            cinemaList.append(path)
                    else:  # valid directories
                        cinemaList.append(path)
                else:  # invalid inputs
                    pathsNonexistent.append(path)
            else:
                pathsNotAbsolute.append(path)

        if len(cinemaList) == 0 and len(backupList) == 0:
            raise ValueError("NO PASSED ARGUMENTS WERE VALID")

        if len(cinemaList) > 0:
            self.__cinemaArgs = cinemaList

        if len(backupList) > 0:
            self.__backupArgs = backupList

        errorsDictionary: dict[str, list[str]] = {}

        if len(pathsNotAbsolute) > 0:
            errorsDictionary["Not Absolute"] = pathsNotAbsolute

        if len(pathsNonexistent) > 0:
            errorsDictionary["Does Not Exist"] = pathsNonexistent

        self.__errorsDictionary = errorsDictionary

    def getNumErrors(self) -> int:
        return len(self.__errorsDictionary)

    def getErrorsDict(self) -> dict[str, list[str]]:
        return self.__errorsDictionary

    def getCinemaArgs(self) -> list[str]:
        """ Return the processed cinema paths list. """

        return self.__cinemaArgs

    def getBackupArgs(self) -> list[str]:
        """ Return the processed backup paths list. """

        return self.__backupArgs
