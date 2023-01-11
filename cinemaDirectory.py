from abc import ABC, abstractmethod
from cinema import Cinema


class CinemaDirectory(ABC):
    """ Container for Cinema objects. """

    __name: str
    __tags: str
    __cinemaList: list[Cinema]
    __libraryName: str
    __libraryDirectory: str