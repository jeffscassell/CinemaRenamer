from abc import ABC, abstractmethod
from cinema import Cinema


class CinemaDirectory():
    """ Container for Cinema objects. """

    name: str
    library: str
    tags: str
    __cinemaList: list[Cinema]
    # __libraryDirectory: str

    def __init__(self, cinema: Cinema) -> None:
        self.name = cinema.getNewFileNameSimple()
        self.__cinemaList = [cinema]

    def append(self, cinema: Cinema) -> None:
        self.__cinemaList.append(cinema)
    