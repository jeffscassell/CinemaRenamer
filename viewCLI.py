import os

from view import View
from cinema import Cinema
from unknown import Unknown
from controller import Controller


class ViewCLI(View):
    """ The terminal interface for Cinema Renamer. """

    # isCinema = False
    controller: Controller

    def start(self, model: list, controller: Controller) -> None:
        print()
        self.controller = controller

        self.__doValidation(model)

        if self.controller.hasCinemaArgs() and self.controller.hasBackupArgs():
            self.__printHeader("cinema and backup files recognized. processing cinema first.")
            self.__processCinema(self.controller.getCinemaArgs())
            self.__processRestore(self.controller.getBackupArgs())
        elif self.controller.hasCinemaArgs():
            self.__processCinema(self.controller.getCinemaArgs())
        else:
            self.__processRestore(self.controller.getBackupArgs())

        print("\nEXITING.\n")
        os.system("pause")
        exit()

    def __doValidation(self, model: list[str]) -> None:

        def printErrors(errorsDict: dict[str, list[str]]) -> None:
            for error, errorPaths in errorsDict.items():
                for path in errorPaths:
                    print(f"{error}: {path}")

        print("VALIDATING INPUT... ", end="")

        try:
            self.controller.doValidation(model)
        except ValueError as e:
            print("[FAIL]\n")
            print(f"{e}\n"
                  "At least a single absolute path for a file or directory is required for processing.\n\n"
                  "Files:       Can be cinema files or backups.\n"
                  "Directories: Can be cinema directories (no recursive searches performed).\n\n"
                  "Exiting.\n")

            os.system("pause")
            exit(1)

        if self.controller.checkForValidationErrors():
            print(f"[{self.controller.getValidationErrorNum()} ERROR(S)]\n")

            printErrors(self.controller.getValidationErrorDict())
        else:
            print("[OK]\n")

    def __processCinema(self, model: list[str]) -> None:

        def getUnknownCinema(inpList: list[Cinema]) -> list[Cinema]:
            returnList = []
            for obj in inpList:
                if isinstance(obj, Unknown):
                    unknownList.append(obj)
            return returnList

        def getErrorCinema(inpList: list[Cinema]) -> list[Cinema]:
            returnList = []
            for obj in inpList:
                if obj.hasError():
                    returnList.append(obj)
            return returnList

        self.__printHeader("processing cinema files")

        cinemaList = self.controller.getParsedCinemaObjs(model)

        unknownList = getUnknownCinema(cinemaList)

        if len(unknownList) > 0:
            self.__printHeader("removing unrecognized files")
            for obj in unknownList:
                cinemaList.remove(obj)
                print(f"    -> {obj.getOldAbsPath()}")
            print()

        errorList = getErrorCinema(cinemaList)

        if len(errorList) > 0:
            for obj in errorList:
                cinemaList.remove(obj)
            self.__printHeader("removing detected errors")
            self.__printCinemaTree(errorList)

        self.__printHeader("cinema files finished processing")

        if len(cinemaList) > 0:
            self.__printCinemaTree(cinemaList)
        else:
            return

        choiceOptions = self.__getListOfIndexOptions(cinemaList)
        choice = ""
        while choice != "y":
            print("TO MAKE MANUAL EDITS, SPECIFY THEIR INDICES SEPARATED BY A SPACE (2 11 0 ...).")

            choice = input("PERFORM RENAME? [Y|n|#]: ") or "y"
            choice = choice.lower()

            if choice == "n":
                return
            else:
                valid = True
                choices = choice.split()
                for arg in choices:
                    if arg not in choiceOptions:
                        valid = False
                if valid:
                    print()
                    self.__doCorrections(cinemaList, choices)

        self.__doRename(cinemaList)

    def __doCorrections(self, model: list[Cinema], choices: list[str]) -> None:

        def hasIllegalChar(inp: str) -> bool:
            illegal = False
            for char in inp:
                if char in illegalChars:
                    illegal = True
            return illegal

        for choice in choices:
            choice = int(choice)
            print(f" {choice:>4d}: {model[choice].getNewFileName()}")

            # loop here based on input validation
            illegalChars = ["\\", "/", ":", "*", "\"", "<", ">", "|"]
            newName = ""
            cont = True
            while cont:
                newName = input("    -> ")

                if len(newName) > 0:
                    cont = False

                    if hasIllegalChar(newName):
                        cont = True
                        print("       ILLEGAL CHARACTER ENTERED:  \\ / : * \" < > |")

            model[choice].setNewFileName(newName)
            print()

        self.__printHeader("edited cinema files")
        self.__printCinemaTree(model)

    def __doRename(self, model: list[Cinema]) -> None:
        print("\nRENAMING FILES... ", end="")
        numErrors = 0
        errors = []

        # attempt to rename files and handle/count errors
        for obj in model:
            try:
                self.controller.rename(obj)
            except ValueError as e:
                numErrors += 1
                errors.append(f"{str(e)}: {obj.getNewFileName()}{obj.getFileExt()}")

        if numErrors == 0:
            print("[OK]\n")
        else:
            print(f"[{numErrors} ERROR(S)]\n")
            for error in errors:
                print(error)
            print()

        print(f"OPERATION COMPLETE. ORIGINAL FILE NAMES ARE BACKED UP TO DIRECTORY:\n"
              f"{self.controller.getBackupDir()}\n")

    def __processRestore(self, model: list[str]) -> None:
        self.__printHeader("processing backup files")

        cinemaList = []
        # display passed files
        for path in model:
            cinemaList.append(self.controller.getCinemaObjFromBackup(path))

        i = 1
        for obj in cinemaList:
            print(f" {i:>3d}: {obj.getNewFileName()}{obj.getFileExt()}\n"
                  f"   -> {obj.getOldFileName()}{obj.getFileExt()}\n")
            i += 1

        print()

        # prompt for continuation
        cont = ""
        while cont.lower() not in ["y", "n"]:
            cont = input("PERFORM RESTORATION? [Y|n]: ") or "y"

        print()

        if cont == "y":
            self.__doRestore(model)

    def __doRestore(self, model: list[str]) -> None:
        print("RESTORING FILES...", end="")

        numErrors = 0

        for path in model:
            try:
                self.controller.restore(path)
            except Exception as e:
                numErrors += 1
                print(e)

        if numErrors == 0:
            print("[OK]\n")
            print(f"OPERATION COMPLETE.\n")
        else:
            print(f"[{numErrors} ERROR(S)]\n")

            # todo identify specific errors during restoration and handle them

            print(f"OPERATION COMPLETE. ORIGINAL FILE NAMES ARE BACKED UP TO:\n"
                  f"{self.controller.getBackupDir()}\n")

    def __printHeader(self, inp: str) -> None:
        underlineChar = "+"
        underline = ""
        for _ in range(len(inp)+4):
            underline += underlineChar

        print(f"{underline}\n"
              f"{underlineChar} {inp.upper()} {underlineChar}\n"
              f"{underline}\n")

    def __printCinemaTree(self, cinemaList: list[Cinema]) -> None:
        i = 0
        currentDir = ""

        for obj in cinemaList:
            if currentDir == obj.getParentDir():
                if obj.hasError():
                    self.__printErrorCinema(obj)
                else:
                    self.__printCinema(obj, i)

                print()
            else:
                print()
                currentDir = obj.getParentDir()
                print(currentDir)

                if obj.hasError():
                    self.__printErrorCinema(obj)
                else:
                    self.__printCinema(obj, i)

                print()

            i += 1

        print()

    def __printErrorCinema(self, cinema: Cinema) -> None:
        print(f"    - {cinema.getOldFileName()}{cinema.getFileExt()}")  # 5 spaces to actual text
        print(f"      [!]     {cinema.getError()}")

    def __printCinema(self, cinema: Cinema, i: int) -> None:
        print(f" {i:>4d}: {cinema.getOldFileName()}{cinema.getFileExt()}")  # 6 spaces to actual text
        print(f"    -> {cinema.getNewFileName()}{cinema.getFileExt()}")

    def __getListOfIndexOptions(self, lst) -> list:
        i = 0
        count = []
        for _ in lst:
            count.append(str(i))
            i += 1
        return count

    # def __printRestoreCinema(self, restoreList: list[Cinema]) -> None:
    #     i = 1
    #     for obj in restoreList:
    #         print(f" {i:>3d}: {obj.getNewFileName()}{obj.getFileExt()}\n"
    #               f"   -> {obj.getOldFileName()}{obj.getFileExt()}\n")
    #         i += 1

    # def __displayCinema(self, model: list[Cinema], rename: bool) -> None:
    #     i = 0
    #     currentDir = ""
    #
    #     for cinema in model:
    #         if currentDir == cinema.getParentDir():
    #             self.__printErrorCinema(cinema, i)
    #         else:
    #             print()
    #             currentDir = cinema.getParentDir()
    #             print(currentDir)
    #             self.__printErrorCinema(cinema, i)
    #
    #         i += 1
