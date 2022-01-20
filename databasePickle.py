import _pickle

from database import Database
from cinema import Cinema
import pickle
import os


class DatabasePickle(Database):
    """ Concrete Cinema database implementation that uses flat files. """

    PICKLE_PROTOCOL = 4
    __filePath = os.path.dirname(os.path.abspath(__file__))
    DIRECTORY = f"{__filePath}\\Cinema Renamer Backups"
    EXT = ".pkl"

    def __init__(self):
        if not os.path.exists(self.DIRECTORY):
            os.mkdir(self.DIRECTORY)

    def getBackupAbsPath(self) -> str:
        return os.path.join(os.getcwd(), self.DIRECTORY)

    def create(self, record: Cinema) -> None:
        if record.hasError():
            raise ValueError(record.getError())

        fileName = record.getNewFileName()
        fileExt = record.getFileExt()

        with open(f"{self.DIRECTORY}\\{fileName + fileExt}{self.EXT}", "xb") as outp:
            pickle.dump(record, outp, self.PICKLE_PROTOCOL)

    def read(self, path: str) -> Cinema:  # throws ValueError, FileNotFoundError
        try:
            with open(path, "rb") as inp:  # read bytes
                return pickle.load(inp)  # raise EOFError with empty input, or _pickle.UnpicklingError with false input
        except _pickle.UnpicklingError or EOFError:
            raise ValueError(f"INVALID BACKUP")

    def renameAndCreate(self, record: Cinema) -> None:
        fileName = record.getNewFileName()
        fileNameAppend = ""
        fileExt = record.getFileExt()

        i = 1
        while os.path.exists(f"{self.DIRECTORY}\\{fileName + fileNameAppend + fileExt}{self.EXT}"):

            fileNameAppend = f"({i})"
            record.setNewFileName(fileName + fileNameAppend)
            i += 1

        self.create(record)

    # def update(self, record: Cinema) -> None:
    #     pass

    def delete(self, record: Cinema) -> None:  # throws FileNotFoundError
        fileName = record.getNewFileName() + record.getFileExt()

        os.remove(f"{self.DIRECTORY}\\{fileName}{self.EXT}")
