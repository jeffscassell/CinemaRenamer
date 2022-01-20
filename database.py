from abc import ABC, abstractmethod
from cinema import Cinema


class Database(ABC):
    """ An abstract database interface to be used with Cinema objects. """

    @abstractmethod
    def create(self, record: Cinema):
        """ Add a new record to the database. """

    @abstractmethod
    def renameAndCreate(self, record: Cinema):
        """ Rename record before creating to compensate for an existing record conflict. """

    @abstractmethod
    def read(self, record: str) -> Cinema:
        """ Read a record from the database. """

    # @abstractmethod
    # def update(self, record: Cinema):
    #     """ Update a record in the database. """

    @abstractmethod
    def delete(self, record: Cinema):
        """ Delete a record from the database. """

    @abstractmethod
    def getBackupAbsPath(self) -> str:
        """ Return the absolute path of the backup directory. """
