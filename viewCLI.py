import os

from view import View
from cinema import Cinema
from controller import Controller
# from configparser import ConfigParser


class ViewCLI(View):
    """ The terminal interface for Cinema Renamer. """

    controller: Controller

    # Controller variables that are used by ViewCLI
    movieLibraryDirectory: str
    showLibraryDirectory: str
    copyFlag: bool
    overwriteFlag: bool

    hasLimitedFunctionality: bool = False

    def start(self, model: list, controller: Controller) -> None:
        print()
        self.controller = controller

        self.__validateInput(model)
        self.__checkSettings()

        if self.controller.hasValidatedCinemaArgs():
            if self.hasLimitedFunctionality:
                self.__processCinemaLimited(self.controller.getCinemaArguments())
            else:
                self.__processCinema(self.controller.getCinemaArguments())

        if self.controller.hasValidatedBackupArgs():
            if self.hasLimitedFunctionality:
                self.__processRestoreLimited(self.controller.getBackupArguments())
            else:
                self.__processRestore(self.controller.getBackupArguments())

        print("\nEXITING.\n")
        os.system("pause")
        exit()



    def __validateInput(self, model: list[str]) -> None:
        """ Validate inputs that are passed to Cinema Renamer to ensure that they exist and are full file paths. Lack of input will show Cinema Renamer's usage and cease operation. """

        try:
            self.controller.validate(model)
        except ValueError:
            print(f"Usage: python cinema_renamer.py \"full file path 1\" \"full file path 2\" ...\n\n\
                \
                Cinema Renamer is intended to be used by dragging files or folders onto the main Python script (cinema_renamer.py).\n\
                It can be used to identify movies and TV shows, correct any naming discrepancies (see example below),\n\
                create backups of the rename so that it can be undone if an error occurs,\n\
                and automatically integrate the renamed file into its appropriate media library location on disk.\n\n\
                \
                ### EXAMPLE ###\n\
                fight.club.1999.1080p.H.265.(tPB).mkv\n\
                ->\n\
                Fight Club (1999) [1080p] [x265].mkv\n\n\
                \
                ### SETTING LIBRARIES ###\n\
                To set the location for the movie and TV show libraries, add their full paths (C:\\example\\example\\movies) to the configuration file (cr_config.ini),\n\
                which should be located in the same directory as the main Python script. Spaces are acceptable. If the file is missing,\n\
                running the main script will generate a blank one.\n\n\
                \
                ### RESTORING BACKUPS ###\n\
                To restore a file from backup, simply drag the backup file (Fight Club (1999) [1080p] [x265].backup) onto the main script.\n\n")

            os.system("pause")
            exit(0)

        validationErrorsDictionary = self.controller.getValidationErrorsDictionary()

        if len(validationErrorsDictionary) > 0:
            print(f"[{len(validationErrorsDictionary)} ERROR(S)]\n")
            
            # Print validation errors
            for error, errorPathList in validationErrorsDictionary.items():
                for path in errorPathList:
                    print(f"{error}: {path}")
            print()
    


    def __checkSettings(self) -> None:
        """ Check that settings were loaded successfully into the Controller. Notify user if settings were not loaded and limit functionality. """

        if self.controller.movieLibraryDirectory is None or self.controller.showLibraryDirectory is None:
            self.hasLimitedFunctionality = True

            # Issue limited functionality warning
            if self.controller.movieLibraryDirectory is None:
                print(f"MOVIE LIBRARY DIRECTORY IS MISSING")

            if self.controller.showLibraryDirectory is None:
                print("SHOW LIBRARY DIRECTORY IS MISSING")

            print("\nWITH LIBRARIES MISSING, FUNCTIONALITY IS LIMITED TO RENAMING ONLY. FILES CANNOT BE MOVED OR COPIED INTO LIBRARIES.\n")
        else:  # Both libraries exist
            self.movieLibraryDirectory = self.controller.movieLibraryDirectory
            self.showLibraryDirectory = self.controller.showLibraryDirectory

            if self.controller.copyFlag is None or self.controller.overwriteFlag is None:

                if self.controller.copyFlag is None:
                    print("COPY FLAG SETTING IS MISSING FROM CONFIGURATION FILE.")

                    # Prompt to copy or move files that need to be integrated
                    choice = ""
                    print("NOTE: FILES WILL ONLY BE MOVED, NOT COPIED, IF THEY ARE ALREADY WITHIN THE LIBRARY STRUCTURE.")
                    while choice not in ["c", "m"]:
                        choice = input("SHOULD FILES BE COPIED, OR MOVED (CUT AND PASTE), TO NEW LIBRARY DIRECTORY IF NECESSARY? [C|m]: ") or "c"
                        choice.lower()
                    print()

                    if choice == "c":
                        self.copyFlag = True
                    else:
                        self.copyFlag = False
                else:
                    self.copyFlag = self.controller.copyFlag

                if self.controller.overwriteFlag is None:
                    print("OVERWRITE FLAG SETTING IS MISSING FROM CONFIGURATION FILE.")

                    # Prompt to overwrite or skip files where conflicts exist
                    choice = ""
                    while choice not in ["o", "s"]:
                        choice = input("SHOULD FILES BE OVERWRITTEN OR SKIPPED, WHERE CONFLICTS EXIST? [O|s]: ") or "o"
                        choice.lower()
                    print()

                    if choice == "o":
                        self.overwriteFlag = True
                    else:
                        self.overwriteFlag = False
            else:
                self.overwriteFlag = self.controller.overwriteFlag



    def __processCinemaLimited(self, pathList: list[str]) -> None:
        self.__printHeader(f"processing {len(pathList)} cinema file(s)")

        self.controller.parseCinemaPaths(pathList)
        unknownCinemaList: list[Cinema] = self.controller.getUnknownCinemaList()
        alreadyCorrectCinemaList: list[Cinema] = self.controller.getAlreadyCorrectCinemaList()
        cinemaList: list[Cinema] = self.controller.getProcessedCinemaList()
        
        if len(unknownCinemaList) > 0:
            self.__printHeader(f"removed {len(unknownCinemaList)} unrecognized file(s)")
            for cinema in unknownCinemaList:
                print(f"    -> {cinema.getOldAbsolutePath()}")
            print()

        # Process Error List
        # if len(errorCinemaList) > 0:
        #     self.__printHeader(f"removed {len(errorCinemaList)} detected error(s)")
        #     self.__printDetailedCinemaTree(errorCinemaList)
    

    
    def __processCinema(self, pathList: list[str]) -> None:
        self.__printHeader(f"processing {len(pathList)} file(s)")

        self.controller.parseCinemaPaths(pathList)
        unknownCinemaList = self.controller.getUnknownCinemaList()
        # errorCinemaList = self.controller.getErrorCinemaList()
        alreadyCorrectCinemaList = self.controller.getAlreadyCorrectCinemaList()
        cinemaList: list[Cinema] = self.controller.getProcessedCinemaList()

        # Process Unknown List
        if len(unknownCinemaList) > 0:
            self.__printHeader(f"removed {len(unknownCinemaList)} unrecognized file(s)")
            for cinema in unknownCinemaList:
                print(f"    -> {cinema.getOldAbsolutePath()}")
            print()

        # Process Error List
        # if len(errorCinemaList) > 0:
        #     self.__printHeader(f"removed {len(errorCinemaList)} detected error(s)")
        #     self.__printDetailedCinemaTree(errorCinemaList)

        # Process Already-Correct List
        if len(alreadyCorrectCinemaList) > 0:

            # Check for false-positives due to the file having the correct directory name, but not being in the library, and re-add them to cinemaList
            for cinema in alreadyCorrectCinemaList[:]:
                alreadyInMovieLib = f"{self.movieLibraryDirectory}\\{cinema.getNewFileNameSimple()()}" == cinema.getOldDirectoryAbsolutePath()
                alreadyInShowLib = f"{self.showLibraryDirectory}\\{cinema.getNewFileNameSimple()()}" == cinema.getOldDirectoryAbsolutePath()
                if not alreadyInMovieLib and not alreadyInShowLib:
                    alreadyCorrectCinemaList.remove(cinema)
                    cinemaList.append(cinema)

            if len(alreadyCorrectCinemaList) > 0:
                self.__printHeader(f"removed {len(alreadyCorrectCinemaList)} already correct file(s)")
                self.__printSimpleCinemaTree(alreadyCorrectCinemaList)

        self.__printHeader("cinema file(s) finished processing")

        # Check if Cinema objects are already in library and disable integration if so
        if len(cinemaList) > 0:
            for cinema in cinemaList:
                alreadyInMovieLib = f"{self.movieLibraryDirectory}\\{cinema.getNewFileNameSimple()()}" == cinema.getOldDirectoryAbsolutePath()
                alreadyInShowLib = f"{self.showLibraryDirectory}\\{cinema.getNewFileNameSimple()()}" == cinema.getOldDirectoryAbsolutePath()
                if alreadyInMovieLib or alreadyInShowLib:
                    cinema.setIntegrationFalse()

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
        for obj in cinemaList[:]:  # Works on a copy of the list, instead of the original, so that objects can be removed in real time
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

        if os.path.exists(self.movieLibraryDirectory) and os.path.isdir(self.movieLibraryDirectory) and os.path.exists(self.showLibraryDirectory) and os.path.isdir(self.showLibraryDirectory):
            for obj in cinemaList[:]:
                if obj.needsIntegration():
                    try:
                        if obj.isMovie():
                            self.controller.integrateIntoLibrary(obj, self.movieLibraryDirectory, self.copyFlag, self.overwriteFlag)
                            self.passed()
                        elif obj.isShow():
                            self.controller.integrateIntoLibrary(obj, self.showLibraryDirectory, self.copyFlag, self.overwriteFlag)
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
            if self.movieLibraryDirectory:
                print(f"{self.movieLibraryDirectory}")
            else:
                print("[MISSING]")
            
            print("SHOWS LIBRARY DIRECTORY: ", end="")
            if self.showLibraryDirectory:
                print(f"{self.showLibraryDirectory}")
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
            if currentDirPath == obj.getOldDirectoryAbsolutePath():
                fileCount += 1
            else:
                if fileCount != 0:
                    printCount()

                currentDirPath = obj.getOldDirectoryAbsolutePath()
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
            if currentDirPath == obj.getOldDirectoryAbsolutePath():
                # if obj.hasError():
                #     printErrorCinema()
                # else:
                printCinema()

                # print()
            else:
                print()
                currentDirPath = obj.getOldDirectoryAbsolutePath()
                print(currentDirPath)

                # if obj.hasError():
                #     printErrorCinema()
                # else:
                printCinema()

                # print()

            i += 1

        print()
