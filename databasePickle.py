import _pickle

from database import Database
from cinema import Cinema
import pickle
import os


class DatabasePickle(Database):
    """ Concrete Cinema database implementation that uses flat files. """

    PICKLE_PROTOCOL = 4
    DIRECTORY = "Cinema Renamer Backups"
    EXT = ".pkl"

    def __init__(self):
        if not os.path.exists(self.DIRECTORY):
            os.mkdir(self.DIRECTORY)

    def getBackupAbsPath(self) -> str:
        return os.path.join(os.getcwd(), self.DIRECTORY)

    def create(self, record: Cinema) -> None:
        fileName = record.getNewFileName()
        fileNameEnd = ""
        fileExt = record.getFileExt()

        i = 1
        while os.path.exists(f"{self.DIRECTORY}\\{fileName}{fileNameEnd}{fileExt}{self.EXT}"):

            fileNameEnd = f"({i})"
            # record.setNewFileName(fileName)
            i += 1

        with open(f"{self.DIRECTORY}\\{fileName}{fileNameEnd}{fileExt}{self.EXT}", "xb") as outp:
            pickle.dump(record, outp, self.PICKLE_PROTOCOL)

    def read(self, path: str) -> Cinema:  # throws ValueError, FileNotFoundError
        try:
            with open(path, "rb") as inp:  # read bytes
                return pickle.load(inp)  # raise EOFError with empty input, or _pickle.UnpicklingError with false input
        except _pickle.UnpicklingError as e:
            raise ValueError(f"{e}\n"
                             f"Not a valid backup file: {path}")
        except EOFError as e:
            raise ValueError(f"{e}\n"
                             f"Not a valid backup file: {path}")

    def delete(self, record: Cinema) -> None:  # throws FileNotFoundError
        fileName = f"{record.getNewFileName()}{record.getFileExt()}"

        if os.path.exists(f"{self.DIRECTORY}\\{fileName}{self.EXT}"):
            os.remove(f"{self.DIRECTORY}\\{fileName}{self.EXT}")
        else:
            raise FileNotFoundError
