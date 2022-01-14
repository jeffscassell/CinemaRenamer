from cinema import Cinema
import re


class Movie(Cinema):
    """ A Cinema object specific to movies. """

    __date: str

    def __init__(self, filePath, specificMatch: re.Match, resolutionMatch: re.Match, encodingMatch: re.Match):
        super().__init__(filePath)

        # required params
        self._buildAttributes(specificMatch)

        # optional params
        self._setResolution(resolutionMatch)
        self._setEncoding(encodingMatch)

        # finalize object
        self._buildNewFileName()
        self._doErrorCheck()

    def __setDate(self, passed: str) -> None:
        self.__date = passed

    def __getDate(self) -> str:
        return self.__date

    @staticmethod
    def getPattern() -> re.Pattern:
        """ Returns a Pattern object to be used in identifying a Movie object. """

        return re.compile(r"^(?P<title>([!0-9a-zA-Z.',_\-]+ (- )?)+?)(- (\w+ )+- |(- (\w+ )+)|- )?[([]?"
                          r"(?P<date>\d{4})[]) ]")

    def _buildAttributes(self, match: re.Match) -> None:
        self._setTitle(match.group("title"))
        self.__setDate(match.group("date"))

    def _buildNewFileName(self) -> None:
        title = self._capitalize(self._getTitle())
        date = self.__getDate()
        resolution = self._getResolution()
        encoding = self._getEncoding()

        newName = f"{title} ({date})"

        if resolution:
            newName += f" [{resolution}]"

        if encoding:
            newName += f" [x{encoding}]"

        self.setNewFileName(newName)
