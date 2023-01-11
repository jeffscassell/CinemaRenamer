from abc import ABC, abstractmethod

class Library:
    __name: str
    __directory: str

    def __init__(self, name, directory):
        self.__name = name
        self.__directory = directory