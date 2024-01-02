from abc import ABC, abstractmethod
from sys import argv
import os


class Entertainment(ABC):
    @abstractmethod
    def __init__(self, originalTitle, resolution=None, encoding=None):
        pass

    @abstractmethod
    def setNewTitle(self, newTitle):
        pass

    @abstractmethod
    def getTitle(self):
        pass


class Movie(Entertainment):
    def __init__(self, title, releaseDate, resolution=None, encoding=None):
        self.title = title
        self.releaseDate = releaseDate

        if resolution is not None:
            self.resolution = resolution

        if encoding is not None:
            self.encoding = encoding

    def setNewTitle(self, newTitle):
        self.title = newTitle

    def getTitle(self):
        return self.title

    def getReleaseDate(self):
        return self.releaseDate


class Show(Entertainment):
    def __init__(self, title, resolution=None, encoding=None):
        self.title = title

        if resolution is not None:
            self.resolution = resolution

        if encoding is not None:
            self.encoding = encoding

    def setNewTitle(self, newTitle):
        self.title = newTitle

    def getTitle(self):
        return self.title


def main():
    if argv[1] is None:
        print(f"\nPass a domain to process.")
        exit(1)

    # do something with this
    if argv[2] is not None:
        pass

# check for file input. prompt if none provided.

# capture file names and attach to objects

# differentiate movies and tv shows

# gather movie/show data from TMDB API

# tentatively rename input file objects

# display potential changes

# prompt for modifying any proposed changes

# save new files
