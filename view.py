from abc import ABC, abstractmethod


class View(ABC):
    """ Interface to view and interact with Cinema Renamer. """

    @abstractmethod
    def start(self, model: list, controller) -> None:
        pass
