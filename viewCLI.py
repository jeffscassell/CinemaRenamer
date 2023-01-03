import os

from view import View
from cinema import Cinema
from controller import Controller
from configparser import ConfigParser


class ViewCLI(View):
    """ The terminal interface for Cinema Renamer. """

    controller: Controller
    moviesDir: str = ""
    showsDir: str = ""
    copyFlag: bool = True
    overwriteFlag: bool = True

    def start(self, model: list, controller: Controller) -> None:
        print()
        self.controller = controller

        self.__validateInput(model)
        self.__loadConfigurationSettings()

        if self.controller.hasValidatedCinemaArgs():
            self.__processCinema(self.controller.getCinemaArgs())
        if self.controller.hasValidatedBackupArgs():
            self.__processRestore(self.controller.getBackupArgs())

        print("\nEXITING.\n")
        os.system("pause")
        exit()



    def __validateInput(self, model: list[str]) -> None:

        print("VALIDATING INPUT... ", end="")

        try:
            self.controller.validate(model)
        except ValueError as e:
            print("[FAIL]\n")
            print(f"{e}\n"
                  "At least a single absolute path for a file or directory is required for processing.\n\n"
                  "Files:       Can be cinema files or backups.\n"
                  "Directories: Can be cinema directories (no recursive searches performed).\n\n")

            # TODO prompt to change copy and overwrite flags, and then update config file

            # Prompt to copy or move files that need to be integrated
            # choice = ""
            # print("SHOULD FILES BE COPIED OR MOVED (CUT AND PASTE) TO NEW LIBRARY DIRECTORY, IF NECESSARY?")
            # while choice not in ["c", "m"]:
            #     choice = input("NOTE: FILES WILL ONLY BE MOVED, NOT COPIED, IF THEY ARE ALREADY WITHIN THE LIBRARY STRUCTURE. [C|m]: ") or "c"
            #     choice.lower()
            # print()
            # if choice == "m":
            #     copyFlag = False

            # # Prompt to overwrite or skip files where conflicts exist
            # choice = ""
            # while choice not in ["o", "s"]:
            #     choice = input("SHOULD FILES BE OVERWRITTEN OR SKIPPED, WHERE CONFLICTS EXIST? [O|s]: ") or "o"
            #     choice.lower()
            # print()
            # if choice == "s":
            #     overwriteFlag = False

            os.system("pause")
            exit(1)

        validationErrors = self.controller.getValidationNumErrors()

        if validationErrors > 0:
            print(f"[{validationErrors} ERROR(S)]\n")
            
            # Print validation errors
            errorsDict = self.controller.getValidationErrorDictionary()
            for error, errorPathList in errorsDict.items():
                for path in errorPathList:
                    print(f"{error}: {path}")
            print()
        else:
            print("[OK]\n")
    


    def __loadConfigurationSettings(self) -> None:

        def tryReadingLibrary(passed: str) -> str:
            try:
                return config.get("libraries", passed, raw=True)  # Raw removes the need to surround the directory in quotes to handle spaces
            except Exception:
                pass
        
        def tryReadingFlag(passed: str) -> bool:
            try:
                return config.getboolean("flags", passed)
            except Exception:
                pass
        
        configFile = "cr_config.ini"
        config = ConfigParser()

        if os.path.exists(configFile):
            if os.path.getsize(configFile) > 0:  # Config file exists and is not empty. Load settings
                config.read(configFile)

                # Libraries
                self.moviesDir = tryReadingLibrary("movies")
                self.showsDir = tryReadingLibrary("shows")

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
            with open(configFile, "w") as outp:
                config.write(outp)



    def __processCinema(self, model: list[str]) -> None:

        self.__printHeader(f"processing {len(model)} cinema file(s)")

        self.controller.parseCinemaPaths(model)
        unknownCinemaList = self.controller.getUnknownCinemaList()
        # errorCinemaList = self.controller.getErrorCinemaList()
        alreadyCorrectCinemaList = self.controller.getAlreadyCorrectCinemaList()
        cinemaList = self.controller.getProcessedCinemaList()

        # Process Unknown List
        if len(unknownCinemaList) > 0:
            self.__printHeader(f"removed {len(unknownCinemaList)} unrecognized file(s)")
            for obj in unknownCinemaList:
                print(f"    -> {obj.getOldAbsolutePath()}")
            print()

        # Process Error List
        # if len(errorCinemaList) > 0:
        #     self.__printHeader(f"removed {len(errorCinemaList)} detected error(s)")
        #     self.__printDetailedCinemaTree(errorCinemaList)

        # Process Already-Correct List
        if len(alreadyCorrectCinemaList) > 0:
            # Check for false-positives due to the file having the correct directory name, but not being in the library, and re-add them to cinemaList
            for obj in alreadyCorrectCinemaList[:]:
                alreadyInMovieLib = f"{self.moviesDir}\\{obj.getNewDirectory()}" == obj.getOldDirectoryPath()
                alreadyInShowLib = f"{self.showsDir}\\{obj.getNewDirectory()}" == obj.getOldDirectoryPath()
                if not alreadyInMovieLib and not alreadyInShowLib:
                    alreadyCorrectCinemaList.remove(obj)
                    cinemaList.append(obj)

            if len(alreadyCorrectCinemaList) > 0:
                self.__printHeader(f"removed {len(alreadyCorrectCinemaList)} already correct file(s)")
                self.__printSimpleCinemaTree(alreadyCorrectCinemaList)

        self.__printHeader("cinema file(s) finished processing")

        if len(cinemaList) > 0:
            # Check if objs are already in library and disable integration if so
            for obj in cinemaList:
                alreadyInMovieLib = f"{self.moviesDir}\\{obj.getNewDirectory()}" == obj.getOldDirectoryPath()
                alreadyInShowLib = f"{self.showsDir}\\{obj.getNewDirectory()}" == obj.getOldDirectoryPath()
                if alreadyInMovieLib or alreadyInShowLib:
                    obj.setIntegrationFalse()

            self.__promptForRenamingAction(cinemaList)



    def __promptForRenamingAction(self, cinemaList: list[Cinema]) -> None:
        """ Cinema files were detected that needed renaming and an action is needed to be chosen for them. """

        self.__printDetailedCinemaTree(cinemaList)

        # Compile choice option list to choose from in terminal
        # i = 0 ##################!!!!!!!!!!!!!!!!!!!!!!!!################################
        correctionChoiceOptions = []
        for i, _ in enumerate(cinemaList):
            correctionChoiceOptions.append(str(i))
            # i += 1

        # Prompt for what to do with items that have been processed
        choice = ""
        while choice != "y":
            print("TO MAKE MANUAL EDITS, SPECIFY THEIR INDICES SEPARATED BY A SPACE (2 11 0 ...).")

            # todo make it an option to remove items from renaming

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
                        break
                if doCorrections:
                    print()
                    
                    # Process corrections
                    illegalChars = ["\\", "/", ":", "*", "\"", "<", ">", "|"]

                    for index in choices:
                        index = int(index)
                        print(f" {index:>4d}: {cinemaList[index].getNewFileNameSimple()}")

                        newName = ""
                        cont = True
                        while cont:
                            newName = input("    -> ")

                            if len(newName) == 0:
                                pass  # remove item from list?
                            else:
                                cont = False

                                # Check for illegal characters in new name
                                illegalCharsPresent = False
                                for char in newName:
                                    if char in illegalChars:
                                        illegalCharsPresent = True

                                if illegalCharsPresent:
                                    cont = True
                                    print("       ILLEGAL CHARACTER ENTERED:  \\ / : * \" < > |")
                                
                                # Check that the name is actually changing
                                if newName == cinemaList[index].getNewFileNameSimple():
                                    cont = True
                                    print("       NAME IS UNCHANGED")

                        cinemaList[index].updateFileNameSimple(newName)
                        print()

                    # End processing corrections

                    self.__printHeader("edited cinema files")
                    self.__printDetailedCinemaTree(cinemaList)

        if len(cinemaList) > 0:
            print()
            self.__doBackup(cinemaList)



    def __doBackup(self, cinemaList: list[Cinema]) -> None:

        self.__printHeader(f"backing up file(s)")

        print(f"BACKING UP {len(cinemaList)} FILE(S)...")
        errors = []
        conflictList: list[Cinema] = []
        
        # Try to backup files. Move objs that have a conflict to separate list for resolving.
        for obj in cinemaList[:]:  # Works on a copy of the list, instead of the original, so that objs can be removed in real time
            try:
                if self.overwriteFlag:
                    self.controller.backupOverwrite(obj)
                    self.passed()
                else:
                    self.controller.backup(obj)
                    self.passed()
            except FileExistsError:  # Exception handling (but not throwing) should be done in UI
                self.fail()
                errors.append(f"BACKUP EXISTS: {obj.getBackupName()}")
                cinemaList.remove(obj)
                conflictList.append(obj)
            except Exception as e:
                self.fail()
                errors.append(e)
                cinemaList.remove(obj)
        self.fin()

        if not len(errors) == 0:
            # Display errors
            for error in errors:
                print(error)
            print()

            # Handle naming conflicts
            if len(conflictList) > 0:
                choice = ""
                while choice not in ["o", "a", "s"]:
                    choice = input(f"BACKUP NAMING CONFLICTS EXIST. OVERWRITE, APPEND, OR SKIP? [O|a|s]: ") or "o"
                    choice.lower()
                print()

                # Overwrite
                if choice == "o":
                    for obj in conflictList:
                        self.controller.backupOverwrite(obj)
                        cinemaList.append(obj)
                
                # Append
                if choice == "a":
                    for obj in conflictList:
                        self.controller.backupAppend(obj)
                        cinemaList.append(obj)

        if len(cinemaList) > 0:
            print(f"BACKUP COMPLETE. BACKUP FILE(S) ARE IN DIRECTORY:\n"
                f"{self.controller.getBackupsDir()}\n")
            self.__doRename(cinemaList)



    def __doRename(self, cinemaList: list[Cinema]) -> None:

        print(f"RENAMING AND/OR INTEGRATING {len(cinemaList)} FILE(S)...")

        # for obj in cinemaList:
        #             try:
        #                 self.controller.rename(obj)
        #             except Exception as e:
        #                 errorList += f"{str(e)}: {obj.getNewFileName() + obj.getFileExtension()}"
        #                 self.controller.deleteBackup(obj)

        errorList = []

        if os.path.exists(self.moviesDir) and os.path.isdir(self.moviesDir) and os.path.exists(self.showsDir) and os.path.isdir(self.showsDir):
            for obj in cinemaList[:]:
                if obj.needsIntegration():
                    try:
                        if obj.isMovie():
                            self.controller.integrateIntoLibrary(obj, self.moviesDir, self.copyFlag, self.overwriteFlag)
                            self.passed()
                        elif obj.isShow():
                            self.controller.integrateIntoLibrary(obj, self.showsDir, self.copyFlag, self.overwriteFlag)
                            self.passed()
                        else:
                            raise FileNotFoundError("NO MATCHING LIBRARY FOR CINEMA TYPE")
                    except FileNotFoundError as e:
                        self.fail()
                        errorList += f"{str(e)}: {obj.getNewFileName() + obj.getFileExtension()}"
                        self.controller.deleteBackup(obj)
                    except FileExistsError as e:
                        self.fail()
                        errorList.append(f"{str(e)}: {obj.getNewFileName()}{obj.getFileExtension}")
                        cinemaList.remove(obj)
                        self.controller.deleteBackup(obj)
                    except Exception as e:
                        self.fail()
                        errorList.append(e)
                        self.controller.deleteBackup(obj)
                else:  # If folder is already correctly named
                    try:
                        self.controller.rename(obj)
                        self.controller.backupOverwrite(obj)
                        # renamedList.append(obj)
                        self.passed()
                    except FileExistsError:
                        self.fail()
                        cinemaList.remove(obj)
                        self.controller.deleteBackup(obj)
                    except Exception as e:
                        self.fail()
                        errorList.append(e)
                        self.controller.deleteBackup(obj)
            self.fin()
        else:
            # Print error if missing at least 1 library directory
            print("MOVIES LIBRARY DIRECTORY: ", end="")
            if self.moviesDir:
                print(f"{self.moviesDir}")
            else:
                print("[MISSING]")
            
            print("SHOWS LIBRARY DIRECTORY: ", end="")
            if self.showsDir:
                print(f"{self.showsDir}")
            else:
                print("[MISSING]")
            
            # Prompt for continue or exit
            print()
            choice = ""
            print("WHILE ANY LIBRARY DIRECTORY IS MISSING OR INVALID, MOVING OR COPYING FILES INTO LIBRARY STRUCTURES IS NOT POSSIBLE.")
            while choice not in ["y", "n"]:
                choice = input("ONLY RENAMING WILL BE PERFORMED. CONTINUE? [Y|n]: ") or "y"
                choice.lower()
            print()

            if choice == "y":  # Continue
                for obj in cinemaList[:]:
                    try:
                        self.controller.rename(obj)
                        self.passed()
                    except Exception as e:
                        self.fail()
                        errorList.append(e)
                        self.controller.deleteBackup(obj)
                self.fin()
            else:  # Delete backups before exiting
                print("DELETING BACKUPS...")
                for obj in cinemaList:
                    self.controller.deleteBackup(obj)
                    self.passed()
                self.fin()
        
        # Print any errors
        if not len(errorList) == 0:
            # Display errors
            for error in errorList:
                print(error)
            print()



    def __processRestore(self, model: list[str]) -> None:

        def printCinemaList() -> None:
            i = 1
            for obj in cinemaList:
                print(f" {i:>3d}: {obj.getNewFileName()}{obj.getFileExtension()}\n"
                      f"   -> {obj.getOldFileName()}{obj.getFileExtension()}\n")
                i += 1

            print()

        def printErrors() -> None:
            for error in errors:
                print(error)
            print()

        self.__printHeader(f"processing {len(model)} backup file(s)")

        cinemaList = []
        errors: list[str] = []

        print("READING BACKUP FILE(S)...")

        for path in model:
            try:
                cinemaList.append(self.controller.readObjFromBackup(path))
                self.passed()
            except ValueError as e:  # Not a backup file
                self.fail()
                errors.append(f"NOT A BACKUP: {path}")
            except FileNotFoundError:
                self.fail()
                errors.append(f"DOES NOT EXIST: {path}")
        self.fin()

        if not len(errors) == 0:
            self.__printErrorsTestResult(len(errors), len(cinemaList))
            printErrors()

        self.__printHeader("backup file(s) finished processing")

        if len(cinemaList) > 0:
            printCinemaList()
            cont = ""
            while cont.lower() not in ["y", "n"]:
                cont = input("PERFORM RESTORATION? [Y|n]: ") or "y"
                if cont == "n":
                    return
            
            print()
            self.__doRestore(cinemaList)



    def __doRestore(self, cinemaList: list[Cinema]) -> None:

        print(f"RESTORING {len(cinemaList)} FILE(S)...")

        errorList: list[str] = []

        for obj in cinemaList[:]:
            try:
                self.controller.restoreBackupObj(obj)
                self.passed()
            except Exception as e:
                self.fail()
                errorList.append(e)
        self.fin()

        if not len(errorList) == 0:
            self.__printErrorsTestResult(len(errorList), len(cinemaList))
            for error in errorList:
                print(error)
            print()

        print(f"RESTORATION(S) COMPLETE.\n")



    def passed(self) -> None:
        """ Prints an "iteration success" to the screen when processing lists. """
        print(".", end="")
    
    def fail(self) -> None:
        """ Prints an "iteration failure" to the screen when processing lists. """
        print("x", end="")
    
    def fin(self) -> None:
        print(" [DONE]\n")



    @staticmethod
    def __printHeader(inp: str) -> None:
        fillChar = "+"
        underline = ""
        for _ in range(len(inp) + 4):
            underline += fillChar

        print(f"{underline}\n"
              f"{fillChar} {inp.upper()} {fillChar}\n"
              f"{underline}\n")



    def __printErrorsTestResult(self, numErrors: int, numPassed: int) -> None:
        print(f"[{numErrors} ERROR(S), {numPassed} OK]\n")



    def __printSimpleCinemaTree(self, cinemaList: list[Cinema]) -> None:

        def printCount() -> None:
            print(f"     {fileCount} FILE(S)")

        currentDirPath = ""
        fileCount = 0
        for obj in cinemaList:
            if currentDirPath == obj.getOldDirectoryPath():
                fileCount += 1
            else:
                if fileCount != 0:
                    printCount()

                currentDirPath = obj.getOldDirectoryPath()
                print(currentDirPath)
                fileCount = 1

        printCount()
        print()



    def __printDetailedCinemaTree(self, cinemaList: list[Cinema]) -> None:

        # C:\Some\directory\path
        #     0 - old JackeD up NAME -MILKYWAYGALAXYTAGFTW-.mkv
        #         New Shiny Name.mkv
        #     1 - Already Correct.mp4
        #              ! NEEDS TO BE INTEGRATED INTO LIBRARY

        def printCinema() -> None:
            print(f"  {i:>3d} - {obj.getOldFileName()}{obj.getFileExtension()}")  # 5 spaces to actual text starting, 2 spaces + 2 padding + 1 index start
            if obj.hasCorrectFileName() and not obj.hasCorrectDirectoryName():
                print(f"             ! FILE CORRECT, DIRECTORY WILL BE RENAMED")
            elif obj.hasCorrectFileName() and obj.hasCorrectDirectoryName():
                print(f"             ! NEEDS TO BE INTEGRATED INTO LIBRARY")
            else:
                print(f"        {obj.getNewFileName()}{obj.getFileExtension()}")

        # def printErrorCinema() -> None:
        #     print(f"    - {obj.getOldFileName()}{obj.getFileExtension()}")  # 5 spaces to actual text
        #     print(f"      [!]     {obj.getError()}")

        i = 0
        currentDirPath = ""

        for obj in cinemaList:
            if currentDirPath == obj.getOldDirectoryPath():
                # if obj.hasError():
                #     printErrorCinema()
                # else:
                printCinema()

                # print()
            else:
                print()
                currentDirPath = obj.getOldDirectoryPath()
                print(currentDirPath)

                # if obj.hasError():
                #     printErrorCinema()
                # else:
                printCinema()

                # print()

            i += 1

        print()
