import _pickle

from database import Database
from cinema import Cinema
import pickle
import os


class DatabasePickle(Database):
    """ Concrete Cinema database implementation that uses flat files. """

    PICKLE_PROTOCOL = 4
    __filePath = os.path.dirname(os.path.abspath(__file__))
    BACKUP_PATH = f"{__filePath}\\Cinema Renamer Backups"
    EXT = ".pkl"



    def __init__(self):
        if not os.path.exists(self.BACKUP_PATH):
            os.mkdir(self.BACKUP_PATH)



    def getBackupsAbsPath(self) -> str:
        return os.path.join(os.getcwd(), self.BACKUP_PATH)



    def create(self, record: Cinema) -> None:
        """ Create new record. If record already exists, an appendment is made to the record name. """

        with open(f"{self.BACKUP_PATH}\\{record.getBackupName()}{self.EXT}", "xb") as outp:  # folder.file.ext.pkl | xb, exclusive creation (no overwrite) in binary mode
            pickle.dump(record, outp, self.PICKLE_PROTOCOL)



    def update(self, record: Cinema) -> None:
        """ Overwrite an existing record. """

        with open(f"{self.BACKUP_PATH}\\{record.getBackupName()}{self.EXT}", "wb") as outp:
            pickle.dump(record, outp, self.PICKLE_PROTOCOL)
            


    def createAppend(self, record: Cinema) -> None:
        backupName = record.getBackupName()
        append = ""
        i = 1

        while os.path.exists(f"{self.BACKUP_PATH}\\{backupName}{append}{self.EXT}"):  # folder.file.ext(1).pkl
            append = f"({i})"
            i += 1
        
        # If the record was appended, update the obj's attribute
        if append != "":
            backupName = backupName + append
            record.setBackupName(backupName)
        
        self.create(record)



    def read(self, path: str) -> Cinema:
        try:
            with open(path, "rb") as inp:  # read bytes
                return pickle.load(inp)  # raise EOFError with empty input, or _pickle.UnpicklingError with non-pickle input
        except _pickle.UnpicklingError:
            raise ValueError()



    def delete(self, record: Cinema) -> None:  # throws FileNotFoundError
        """ Delete backup file from Cinema object. """

        os.remove(f"{self.BACKUP_PATH}\\{record.getBackupName()}{self.EXT}")
