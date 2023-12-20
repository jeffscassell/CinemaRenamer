import os
from configparser import ConfigParser

class SettingsHandler():
    """ Creates, loads, and updates the Cinema Renamer configuration file. """


    __SETTINGS_FILE: str = "cr_config.ini"
    __CONFIG = ConfigParser()

    __movieLibraryDirectory: str = ""
    __showLibraryDirectory: str = ""
    __copyFlag: bool = True
    __overwriteFlag: bool = True


    # def __init__(self) -> None:
    #     self.__loadSettings()

    ###########
    # GETTERS #
    ###########

    def getMovieLibraryDirectory(self) -> str:
        return self.__movieLibraryDirectory
    def getShowLibraryDirectory(self) -> str:
        return self.__showLibraryDirectory
    def getCopyFlag(self) -> bool:
        return self.__copyFlag
    def getOverwriteFlag(self) -> bool:
        return self.__overwriteFlag

    ###########
    # SETTERS #
    ###########

    def setMovieLibraryDirectory(self, passed: str) -> None:
        self.__movieLibraryDirectory = passed
    def setShowLibraryDirectory(self, passed: str) -> None:
        self.__showLibraryDirectory = passed
    def setCopyFlag(self, passed: bool) -> None:
        self.__copyFlag = passed
    def setOverwriteFlag(self, passed: bool) -> None:
        self.__overwriteFlag = passed

    ###########
    # UTILITY #
    ###########

    def settingsLoadedSuccessfully(self) -> bool:
        if self.getMovieLibraryDirectory() == "":
            return False
        if self.getShowLibraryDirectory() == "":
            return False
        return True

    def loadSettingsFile(self) -> None:
        """ Read settings from the configuration file. A blank file is created if one does not exist and default settings are loaded. """

        def tryReadingLibrary(passed: str) -> str:
            try:
                return self.__CONFIG.get("libraries", passed, raw=True)  # Raw removes the need to surround the directory in quotes to handle spaces
            except Exception:  # TODO handle a little more robustly
                return ""
        
        def tryReadingFlag(passed: str) -> bool:
            try:
                return self.__CONFIG.getboolean("flags", passed)
            except Exception:
                return True

        if os.path.exists(self.__SETTINGS_FILE) and os.path.getsize(self.__SETTINGS_FILE) > 0:  # Config file exists and is not empty. Load settings
            self.__CONFIG.read(self.__SETTINGS_FILE)

            # Libraries
            self.setMovieLibraryDirectory(tryReadingLibrary("movies"))
            self.setShowLibraryDirectory(tryReadingLibrary("shows"))

            # Flags
            self.setCopyFlag(tryReadingFlag("copy"))
            self.setOverwriteFlag(tryReadingFlag("overwrite"))
        else:  # Create empty config file
            self.__CONFIG.add_section("libraries")
            self.__CONFIG.add_section("flags")

            self.saveSettingsFile()

    def saveSettingsFile(self) -> None:
        self.__CONFIG.set("libraries", "movies", self.getMovieLibraryDirectory())
        self.__CONFIG.set("libraries", "shows", self.getShowLibraryDirectory())
        self.__CONFIG.set("flags", "copy", self.getCopyFlag())
        self.__CONFIG.set("flags", "overwrite", self.getOverwriteFlag())

        with open(self.__SETTINGS_FILE, "w") as outputFile:
            self.__CONFIG.write(outputFile)