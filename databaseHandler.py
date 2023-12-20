import os
from cinema import Cinema
from database import Database


class databaseHandler:
    """ """

    __database: Database

    def __init__(self, database: Database):
        self.__database = database

    