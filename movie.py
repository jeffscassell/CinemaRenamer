from cinema import Cinema
import re


class Movie(Cinema):
    """ A Cinema object specific to movies. """

    _date: str
    _isMovie = True

    def __init__(self, filePath, specificMatch: re.Match, resolutionMatch: re.Match, encodingMatch: re.Match):
        super().__init__(filePath)

        # required params
        self._buildAttributes(specificMatch)

        # optional params
        self._setResolution(resolutionMatch)
        self._setEncoding(encodingMatch)

        # finalize object
        self._buildNewFileName()

    ###########
    # SETTERS #
    ###########

    def updateFileName(self, passed: str) -> None:
        self._newFileName = passed
        self._backupName = f"{self._newDir}.{passed + self._fileExt}"

    ###########
    # GETTERS #
    ###########

    def getNewFileNameSimple(self) -> str:
        return f"{self._title} ({self._date})"

    def getNewDir(self) -> str:
        return self._newFileName

    @staticmethod
    def getPattern() -> re.Pattern:
        """ Returns a Pattern object to be used in identifying a Movie object. """

        # matches: Title of My-movie; (optional) - Part II; 2012 or (2012) or [2012];
        return re.compile(r"^(?P<title>([!0-9a-zA-Z.',_\-]+ (- )?)+?)(- (\w+ )+- |(- (\w+ )+)|- )?[([]?"
                          r"(?P<date>\d{4})[]) ]")

    #########
    # OTHER #
    #########

    def _buildAttributes(self, match: re.Match) -> None:
        self._setTitle(match.group("title"))
        self._date = match.group("date")

    def _buildNewFileName(self) -> None:
        title = self._title
        date = self._date

        newName = f"{title} ({date}){self._getTags()}"

        self._newFileName = newName
        self._newDir = newName
        self._backupName = f"{self._newDir}.{newName + self._fileExt}"
