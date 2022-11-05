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
        """ Append to (instead of overwriting) an existing record. """

        self.__database.createAppend(obj)


    
    def integrateIntoLibrary(self, obj: Cinema, library: str, copyFlag: bool, overwriteFlag: bool) -> None:
        """ Integrate the passed Cinema object into the passed library. Use the copy flag to determine copying or moving a file into the library, and the
            overwrite flag to determine overwriting or skipping an existing file. """

        def renameFileInLibraryDir() -> None:   
            os.replace(f"{libPathWithNewDir}\\{oldFile}{ext}", newAbsPathInLibrary)

        def renameInLibraryDir() -> None:
            if not obj.hasCorrectFileName:  # In case just the directory needs renaming, skip file renaming
                if os.path.exists(newAbsPathInLibrary):  # File conflict exists
                    if overwriteFlag:
                        renameFileInLibraryDir()
                    else:
                        raise FileExistsError("OVERWRITE NECESSARY")
                else:
                    renameFileInLibraryDir()

        oldFile = obj.getOldFileName()
        newFile = obj.getNewFileName()
        ext = obj.getFileExt()
        libPathWithOldDir = f"{library}\\{obj.getOldDir()}"
        libPathWithNewDir = f"{library}\\{obj.getNewDir()}"
        oldAbsPath = obj.getOldAbsPath()
        newAbsPathInLibrary = f"{library}\\{obj.getNewDir()}\\{newFile}{ext}"
        oldDirExistsInLibrary = os.path.exists(libPathWithOldDir)
        newDirExistsInLibrary = os.path.exists(libPathWithNewDir)

        # Case insensitive windows doesn't work well sometimes
        sameDirNamesDiffCase = obj.getOldDir() != obj.getNewDir()

        # Regardless of the copy flag, files will only be moved if they are NOT already in the library structure
        # os.mkdir(path) (can throw a FileExistsError, or a FileNotFoundError if a file in the parent directory in the path does not exist)
        # os.replace(src, dst) will work with directories, but they have to be empty. also works cross-platform, whereas os.rename does not

        if oldDirExistsInLibrary:  # If the object is already in the library, but the directory is misnamed
            if not newDirExistsInLibrary:
                os.replace(libPathWithOldDir, libPathWithNewDir)  # Rename directory
                renameInLibraryDir()
            else:  # Old and new directory names exist at the same time, UNLESS Windows can't detect a difference due to case insensitivity
                if sameDirNamesDiffCase:
                    os.replace(libPathWithOldDir, libPathWithNewDir)  # Rename directory
                    renameInLibraryDir()
                else:
                    raise FileExistsError("OLD AND NEW DIRECTORIES BOTH EXIST")

            obj.setNewDirPath(libPathWithNewDir)
            self.backupOverwrite(obj)

        elif newDirExistsInLibrary:
            if not obj.hasCorrectFileName():
                if os.path.exists(newAbsPathInLibrary):  # File conflict exists
                    if overwriteFlag:
                        renameFileInLibraryDir()
                    else:
                        raise FileExistsError("OVERWRITE NECESSARY")
                else:
                    if copyFlag:
                        shutil.copy(oldAbsPath, newAbsPathInLibrary)
                    else:
                        shutil.move(oldAbsPath, newAbsPathInLibrary)

            obj.setNewDirPath(libPathWithNewDir)
            self.backupOverwrite(obj)

        else:  # The object is not in the library and the directory doesn't exist
            os.mkdir(libPathWithNewDir)

            if copyFlag:
                if os.path.exists(newAbsPathInLibrary):
                    if overwriteFlag:
                        os.replace(oldAbsPath, newAbsPathInLibrary)
                    else:
                        raise FileExistsError("OVERWRITE NECESSARY")
                else:
                    shutil.copy(oldAbsPath, newAbsPathInLibrary)
            else:
                if os.path.exists(newAbsPathInLibrary):
                    if overwriteFlag:
                        shutil.move(oldAbsPath, newAbsPathInLibrary)  # Will only overwrite if its on the same filesystem
                    else:
                        raise FileExistsError("OVERWRITE NECESSARY")
                else:
                    shutil.move(oldAbsPath, newAbsPathInLibrary)

            obj.setNewDirPath(libPathWithNewDir)
            self.backupOverwrite(obj)




    def deleteBackup(self, cinema: Cinema) -> None:
        self.__database.delete(cinema)
    


    def rename(self, cinema: Cinema) -> None:
        """ The Cinema object's file is not being integrated into a library and just needs renaming in the OS. """

        cinema.setNewDirPath(cinema.getOldDir())
        os.replace(cinema.getOldAbsPath(), cinema.getNewAbsPath())  # what exceptions does this possibly throw? FileNotFoundError?
        self.backupOverwrite(cinema)



    def readObjFromBackup(self, path: str) -> Cinema:  # throws ValueError, FileNotFoundError
        """ Attempt to retrieve the provided path as a backed up Cinema object. """

        return self.__database.read(path)



    def restoreBackupObj(self, cinema: Cinema) -> None:
        """ Restore a Cinema object's file name. """

        os.replace(cinema.getNewAbsPath(), f"{cinema.getNewDirPath()}\\{cinema.getOldFileName()}{cinema.getFileExt()}")
        self.__database.delete(cinema)



    # def restoreBackupObj(self, obj: Cinema) -> None:  # throws ValueError, FileNotFoundError
    #     """ Restore a Cinema file from a backup file path. """

    #     os.replace(obj.getNewAbsPath(), obj.getOldAbsPath())

    #     self.__database.delete(obj)
