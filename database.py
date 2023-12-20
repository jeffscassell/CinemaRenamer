from abc import ABC, abstractmethod
from cinema import Cinema


class Database(ABC):
    """ An abstract database interface to be used with Cinema objects. """

    BACKUP_PATH: str

    @abstractmethod
    def create(self, record: Cinema):
        """ Add a new record to the database. """

    @abstractmethod
    def read(self, record: str) -> Cinema:
        """ Read a record from the database. """

    # @abstractmethod
    # def createAppend(self, record: Cinema):
    #     """ Append to an existing in the database record. """

    @abstractmethod
    def update(self, record: Cinema):
        """ Update a record in the database. """

    @abstractmethod
    def delete(self, record: Cinema):
        """ Delete a record from the database. """

    # @abstractmethod
    # def getBackupsAbsPath(self) -> str:
    #     """ Return the absolute path of the backup directory. """
