import os
from cinema import Cinema
from database import Database


class Handler:
    """ Accepts a list of Cinema objects and performs renaming on the objects. Also restores renamed files. """

    def __init__(self, database: Database):
        self.database = database

    def createBackupAndRename(self, cinema: Cinema) -> None:  # throws ValueError, FileNotFoundError
        """ Backup and rename a Cinema file. """

        self.database.create(cinema)
        os.rename(cinema.getOldAbsPath(), cinema.getNewAbsPath())

    def renameBackupAndRename(self, cinema: Cinema) -> None:
        self.database.renameAndCreate(cinema)
        os.rename(cinema.getOldAbsPath(), cinema.getNewAbsPath())

    def readCinemaFromBackup(self, path: str) -> Cinema:  # throws ValueError, FileNotFoundError
        """ Attempt to retrieve the provided path as a backup Cinema object. """

        return self.database.read(path)

    def restoreFromBackup(self, restorePath: str) -> None:  # throws ValueError, FileNotFoundError
        """ Restore a Cinema file from a backup file path. """

        cinema = self.database.read(restorePath)

        os.rename(cinema.getNewAbsPath(), cinema.getOldAbsPath())

        self.database.delete(cinema)
