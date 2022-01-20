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

        self.__validateInput(model)

        if self.controller.hasValidatedCinemaArgs():
            self.__processCinema(self.controller.getCinemaArgs())
        if self.controller.hasValidatedBackupArgs():
            self.__processRestore(self.controller.getBackupArgs())

        print("\nEXITING.\n")
        os.system("pause")
        exit()

    def __validateInput(self, model: list[str]) -> None:

        def printErrors() -> None:
            errorsDict = self.controller.getValidationErrorDict()
            for error, errorPathList in errorsDict.items():
                for path in errorPathList:
                    print(f"{error}: {path}")

        print("VALIDATING INPUT... ", end="")

        try:
            self.controller.validate(model)
        except ValueError as e:
            print("[FAIL]\n")
            print(f"{e}\n"
                  "At least a single absolute path for a file or directory is required for processing.\n\n"
                  "Files:       Can be cinema files or backups.\n"
                  "Directories: Can be cinema directories (no recursive searches performed).\n\n"
                  "Exiting.\n")

            os.system("pause")
            exit(1)

        if self.controller.hasValidationErrors():
            print(f"[{self.controller.getValidationErrorNum()} ERROR(S)]\n")
            printErrors()
        else:
            print("[OK]\n")

    def __processCinema(self, model: list[str]) -> None:

        def processUnknownList() -> None:
            self.__printHeader(f"removed {len(unknownList)} unrecognized file(s)")
            for obj in unknownList:
                print(f"    -> {obj.getOldAbsPath()}")
            print()

        def processErrorList() -> None:
            self.__printHeader(f"removed {len(errorList)} detected error(s)")
            self.__printCinemaTree(errorList)

        self.__printHeader(f"processing {len(model)} cinema file(s)")

        self.controller.parseCinemaPaths(model)
        cinemaList = self.controller.getGoodCinemaList()
        unknownList = self.controller.getUnknownCinemaList()
        errorList = self.controller.getErrorCinemaList()

        if len(unknownList) > 0:
            processUnknownList()

        if len(errorList) > 0:
            processErrorList()

        self.__printHeader("cinema file(s) finished processing")

        if len(cinemaList) > 0:
            self.__promptForRenamingAction(cinemaList)

    def __promptForRenamingAction(self, cinemaList: list[Cinema]) -> None:

        def processCorrectionChoices() -> None:

            def newNameHasIllegalChar() -> bool:
                illegal = False
                for char in newName:
                    if char in illegalChars:
                        illegal = True
                return illegal

            for index in choices:
                index = int(index)
                print(f" {index:>4d}: {cinemaList[index].getNewFileName()}")

                illegalChars = ["\\", "/", ":", "*", "\"", "<", ">", "|"]
                newName = ""
                cont = True
                while cont:
                    newName = input("    -> ")

                    if len(newName) > 0:
                        cont = False

                        if newNameHasIllegalChar():
                            cont = True
                            print("       ILLEGAL CHARACTER ENTERED:  \\ / : * \" < > |")

                cinemaList[index].setNewFileName(newName)
                print()

        self.__printCinemaTree(cinemaList)

        correctionChoiceOptions = self.__getListOfIndexOptions(cinemaList)
        choice = ""
        while choice != "y":
            print("TO MAKE MANUAL EDITS, SPECIFY THEIR INDICES SEPARATED BY A SPACE (2 11 0 ...).")

            choice = input("PERFORM RENAME? [Y|n|#]: ") or "y"
            choice = choice.lower()

            if choice == "n":
                return
            else:
                doCorrections = True
                choices = choice.split()
                for i in choices:
                    if i not in correctionChoiceOptions:
                        doCorrections = False
                if doCorrections:
                    print()
                    processCorrectionChoices()
                    self.__printHeader("edited cinema files")
                    self.__printCinemaTree(cinemaList)

        self.__doRename(cinemaList)

    def __doRename(self, cinemaList: list[Cinema]) -> None:

        def attemptRename(numErrors) -> None:  # todo figure out why function can't see local numErrors
            for obj in cinemaList:
                try:
                    self.controller.rename(obj)
                except ValueError or FileNotFoundError as e:
                    numErrors += 1
                    errors.append(f"{str(e)}: {obj.getNewFileName()}{obj.getFileExt()}")
                except FileExistsError:
                    numErrors += 1
                    renameList.append(obj)

        def handleErrors() -> None:
            for error in errors:
                print(error)
            print()

        print(f"\nRENAMING {len(cinemaList)} FILES... ", end="")
        numErrors = 0
        errors = []
        renameList = []

        attemptRename(numErrors)

        if numErrors == 0:
            print("[OK]\n")
        else:
            print(f"[{numErrors} ERROR(S), {len(cinemaList) - numErrors} OK]\n")
            for error in errors:
                print(error)
            print()

        print(f"OPERATION COMPLETE. ORIGINAL FILE NAMES ARE BACKED UP TO DIRECTORY:\n"
              f"{self.controller.getBackupDir()}\n")

    def __processRestore(self, model: list[str]) -> None:
        self.__printHeader("processing backup files")

        cinemaList = []

        for path in model:
            try:
                cinemaList.append(self.controller.readCinemaFromBackup(path))
            except ValueError or FileNotFoundError as e:
                pass

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
                self.controller.restoreFromBackup(path)
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

    @staticmethod
    def __printHeader(inp: str) -> None:
        underlineChar = "+"
        underline = ""
        for _ in range(len(inp)+4):
            underline += underlineChar

        print(f"{underline}\n"
              f"{underlineChar} {inp.upper()} {underlineChar}\n"
              f"{underline}\n")

    @staticmethod
    def __printCinemaTree(cinemaList: list[Cinema]) -> None:

        def printErrorCinema() -> None:
            print(f"    - {obj.getOldFileName()}{obj.getFileExt()}")  # 5 spaces to actual text
            print(f"      [!]     {obj.getError()}")

        def printCinema() -> None:
            print(f" {i:>4d}: {obj.getOldFileName()}{obj.getFileExt()}")  # 6 spaces to actual text
            print(f"    -> {obj.getNewFileName()}{obj.getFileExt()}")

        i = 0
        currentDir = ""

        for obj in cinemaList:
            if currentDir == obj.parentDir():
                if obj.hasError():
                    printErrorCinema()
                else:
                    printCinema()

                print()
            else:
                print()
                currentDir = obj.parentDir()
                print(currentDir)

                if obj.hasError():
                    printErrorCinema()
                else:
                    printCinema()

                print()

            i += 1

        print()

    @staticmethod
    def __getListOfIndexOptions(lst) -> list:
        i = 0
        indexList = []
        for _ in lst:
            indexList.append(str(i))
            i += 1
        return indexList
