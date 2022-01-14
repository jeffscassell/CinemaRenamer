from cinema import Cinema
import re


class Show(Cinema):
    """ A Cinema object specific to television show episodes. """

    __season: str
    __episode: str
    __episodeTitle: str

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

    def _setSeason(self, passed: str) -> None:
        """ Set the season of the Show object. """

        self.__season = passed

    def _setEpisode(self, passed: str) -> None:
        """ Set the episode of the Show object. """

        self.__episode = passed

    def _setEpisodeTitle(self, passed: str) -> None:
        # if len(passed) > 0:
        #     if passed[-1] == " ":
        #         self.__episodeTitle = passed[:-1]
        #     else:
        #         self.__episodeTitle = passed
        # else:
        #     self.__episodeTitle = passed
        self.__episodeTitle = self._capitalize(passed)

    def _getSeason(self) -> str:
        return self.__season

    def _getEpisode(self) -> str:
        return self.__episode

    def _getEpisodeTitle(self) -> str:
        return self.__episodeTitle

    @staticmethod
    def getPattern() -> re.Pattern:
        """ Returns a Pattern object to be used in identifying a Show object. """

        return re.compile(r"^(?P<title>([!0-9a-zA-Z.',_\-]+ )+?)(- (\w+ )+- |- (\w+ )+|- )?([sS]eason|[sS])? ?"
                          r"(?P<season>\d{1,2})(x|[eE]pisode|[eE]) ?(?P<episode>\d{1,2})( \[?\d{3,4}p.*| - | |$)"
                          r"(?P<episodeTitle>([!0-9a-zA-Z.',_\-]+( |$))+?||$)(\[?\d{3,4}p|\[|$)")

    def _buildAttributes(self, match: re.Match) -> None:
        self._setTitle(match.group("title"))
        self._setSeason(match.group("season"))
        self._setEpisode(match.group("episode"))
        self._setEpisodeTitle(match.group("episodeTitle"))

    def _buildNewFileName(self) -> None:
        title = self._getTitle()
        season = self._getSeason()
        episode = self._getEpisode()
        episodeTitle = self._getEpisodeTitle()
        resolution = self._getResolution()
        encoding = self._getEncoding()

        newName = f"{title} {season}x{episode}"

        if not episodeTitle == "":
            newName += f" {episodeTitle}"

        if resolution:
            newName += f" [{resolution}]"

        if encoding:
            newName += f" [x{encoding}]"

        self.setNewFileName(newName)
