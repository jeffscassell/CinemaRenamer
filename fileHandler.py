import os
from cinema import Cinema
from database import Database
import shutil


class FileHandler:
    """ Interacts with files and an attached database. """

    __database: Database

    def __init__(self, database: Database):
        self.__database = database



    def backup(self, cinema: Cinema) -> None:
        """ Backup a Cinema object. """

        self.__database.create(cinema)

    

    def backupOverwrite(self, obj: Cinema) -> None:
        """ Overwrite an existing database record. """

        self.__database.update(obj)



    def backupAppend(self, obj: Cinema) -> None:
        """ Append to (instead of overwriting) an existing database record. """

        self.__database.createAppend(obj)


    
    def integrateIntoLibrary(self, obj: Cinema, library: str, copyFlag: bool, overwriteFlag: bool) -> None:
        """ Integrate the passed Cinema object into the passed library. Use the copy flag to determine copying or moving a file into the library, and the
            overwrite flag to determine overwriting or skipping an existing file. """

        def renameFileInLibraryDir() -> None:   
            os.replace(f"{libraryPathAndNewDirectory}\\{oldFileName}{extension}", newAbsolutePathInLibrary)

        def renameInLibraryDir() -> None:
            if not obj.hasCorrectFileName:  # In case just the directory needs renaming, skip file renaming
                if os.path.exists(newAbsolutePathInLibrary):  # File conflict exists
                    if overwriteFlag:
                        renameFileInLibraryDir()
                    else:
                        raise FileExistsError("OVERWRITE NECESSARY")
                else:
                    renameFileInLibraryDir()

        # TODO REFACTOR THIS WHOLE FUNCTION. NEEDS TO BE SPLIT INTO SEPARATE FUNCTIONS RATHER THAN USE FLAGS

        oldFileName = obj.getOldFileName()
        newFileName = obj.getNewFileName()
        extension = obj.getFileExtension()
        libraryPathAndOldDirectory = f"{library}\\{obj.getOldDirectory()}"
        libraryPathAndNewDirectory = f"{library}\\{obj.getNewFileNameSimple()()}"
        oldAbsolutePath = obj.getOldAbsolutePath()
        newAbsolutePathInLibrary = f"{library}\\{obj.getNewFileNameSimple()()}\\{newFileName}{extension}"
        oldDirectoryExistsInLibrary = os.path.exists(libraryPathAndOldDirectory)  # and obj.getOldDirectory() == obj.getNewDirectory()
        newDirectoryExistsInLibrary = os.path.exists(libraryPathAndNewDirectory)

        # Case insensitive windows sometimes gets it wrong when determining if a directory already exists in a library, due to the names being the same but the case being different. This double checks.
        sameDirectoryNamesDifferentCase = obj.getOldDirectory() != obj.getNewFileNameSimple()()

        # Regardless of the copy flag, files will only be moved if they are NOT already in the library structure
        # os.mkdir(path) (can throw a FileExistsError, or a FileNotFoundError if a file in the parent directory in the path does not exist)
        # os.replace(src, dst) will work with directories, but they have to be empty. also works cross-platform, whereas os.rename does not

        if oldDirectoryExistsInLibrary:  # If the object is already in the library, but the directory is misnamed
            if not newDirectoryExistsInLibrary:
                os.replace(libraryPathAndOldDirectory, libraryPathAndNewDirectory)  # Rename directory
                renameInLibraryDir()
            else:  # Old and new directory names exist at the same time, UNLESS Windows can't detect a difference due to case insensitivity
                if sameDirectoryNamesDifferentCase:
                    os.replace(libraryPathAndOldDirectory, libraryPathAndNewDirectory)  # Rename directory
                    renameInLibraryDir()
                else:
                    raise FileExistsError("OLD AND NEW DIRECTORIES BOTH EXIST")

            obj.setNewDirectoryAbsolutePath(libraryPathAndNewDirectory)
            self.backupOverwrite(obj)

        elif newDirectoryExistsInLibrary:
            if not obj.hasCorrectFileName():
                if os.path.exists(newAbsolutePathInLibrary):  # File conflict exists
                    if overwriteFlag:
                        renameFileInLibraryDir()
                    else:
                        raise FileExistsError("OVERWRITE NECESSARY")
                else:
                    if copyFlag:
                        shutil.copy(oldAbsolutePath, newAbsolutePathInLibrary)
                    else:
                        shutil.move(oldAbsolutePath, newAbsolutePathInLibrary)

            obj.setNewDirectoryAbsolutePath(libraryPathAndNewDirectory)
            self.backupOverwrite(obj)

        else:  # The object is not in the library and the directory doesn't exist
            os.mkdir(libraryPathAndNewDirectory)

            if copyFlag:
                if os.path.exists(newAbsolutePathInLibrary):
                    if overwriteFlag:
                        os.replace(oldAbsolutePath, newAbsolutePathInLibrary)
                    else:
                        raise FileExistsError("OVERWRITE NECESSARY")
                else:
                    shutil.copy(oldAbsolutePath, newAbsolutePathInLibrary)
            else:
                if os.path.exists(newAbsolutePathInLibrary):
                    if overwriteFlag:
                        shutil.move(oldAbsolutePath, newAbsolutePathInLibrary)  # Will only overwrite if its on the same filesystem
                    else:
                        raise FileExistsError("OVERWRITE NECESSARY")
                else:
                    shutil.move(oldAbsolutePath, newAbsolutePathInLibrary)

            obj.setNewDirectoryAbsolutePath(libraryPathAndNewDirectory)
            self.backupOverwrite(obj)




    def deleteBackup(self, cinema: Cinema) -> None:
        self.__database.delete(cinema)
    


    def rename(self, cinema: Cinema) -> None:
        """ The Cinema object's file is not being integrated into a library and just needs renaming in the OS. """

        cinema.setNewDirectoryAbsolutePath(cinema.getOldDirectory())
        os.replace(cinema.getOldAbsolutePath(), cinema.getNewAbsolutePath())  # what exceptions does this possibly throw? FileNotFoundError?
        self.backupOverwrite(cinema)



    def readObjFromBackup(self, path: str) -> Cinema:  # throws ValueError, FileNotFoundError
        """ Attempt to retrieve the provided path as a backed up Cinema object. """

        return self.__database.read(path)



    def restoreBackupObj(self, cinema: Cinema) -> None:
        """ Restore a Cinema object's file name. """

        os.replace(cinema.getNewAbsolutePath(), f"{cinema.getNewDirectoryAbsolutePath()}\\{cinema.getOldFileName()}{cinema.getFileExtension()}")
        self.__database.delete(cinema)



    # def restoreBackupObj(self, obj: Cinema) -> None:  # throws ValueError, FileNotFoundError
    #     """ Restore a Cinema file from a backup file path. """

    #     os.replace(obj.getNewAbsolutePath(), obj.getOldAbsolutePath())

    #     self.__database.delete(obj)
