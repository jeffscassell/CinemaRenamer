import os
from cinema import Cinema
from database import Database


class Handler:
    """ Accepts a list of Cinema objects and performs renaming on the objects. Also restores renamed files. """

    def __init__(self, database: Database):
        self.database = database

    def rename(self, renameObj: Cinema) -> None:  # throws ValueError
        """ Rename a Cinema file. """

        if renameObj.hasError():
            raise ValueError("Attempted to rename an already correctly formatted file")

        # backup
        self.database.create(renameObj)

        # rename
        os.rename(renameObj.getOldAbsPath(), renameObj.getNewAbsPath())

    def getCinemaObjFromBackup(self, path: str) -> Cinema:  # throws ValueError, FileNotFoundError
        """ Attempt to retrieve the provided path as a backup Cinema object. """

        return self.database.read(path)

    def restore(self, restorePath: str) -> None:  # throws ValueError, FileNotFoundError
        """ Restore from Cinema file from a backup file path. """

        cinema = self.database.read(restorePath)

        os.rename(cinema.getNewAbsPath(), cinema.getOldAbsPath())

        self.database.delete(cinema)
