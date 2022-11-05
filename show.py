from cinema import Cinema
import re


class Show(Cinema):
    """ A Cinema object specific to television show episodes. """

    _season: str
    _episode: str
    _episodeTitle: str
    _isShow = True

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

    def _setEpisodeTitle(self, passed: str) -> None:
        # if len(passed) > 0:
        #     if passed[-1] == " ":
        #         self._episodeTitle = passed[:-1]
        #     else:
        #         self._episodeTitle = passed
        # else:
        #     self._episodeTitle = passed
        self._episodeTitle = self._capitalize(passed)

    def _setEpisode(self, passed: str) -> None:
        self._episode = passed

    ###########
    # GETTERS #
    ###########
    
    def getNewDir(self) -> str:
        return self._title
    
    def getNewFileNameSimple(self) -> str:
        name = f"{self._title} {self._season}x{self._episode}"

        if not self._episodeTitle == "":
            name += f" {self._episodeTitle}"
        
        return name

    @staticmethod
    def getPattern() -> re.Pattern:
        """ Returns a Pattern object to be used in identifying a Show object. """

        # matches: Title of a Show; (optional) - More to the Title; S01; E02; (optional) Title of the Episode
        return re.compile(r"^(?P<title>([!0-9a-zA-Z.',_\-]+ )+?)(- (\w+ )+- |- (\w+ )+|- )?([sS]eason|[sS])? ?"
                          r"(?P<season>\d{1,2})(x|[eE]pisode|[eE]) ?(?P<episode>\d{1,2})( \[?\d{3,4}p.*| - | |$)"
                          r"(?P<episodeTitle>([!0-9a-zA-Z.',_\-]+( |$))+?|$)(\[?\d{3,4}p|\[|$)")

    #########
    # OTHER #
    #########

    def _buildAttributes(self, match: re.Match) -> None:
        self._setTitle(match.group("title"))
        self._season = match.group("season")
        self._episode = match.group("episode")
        self._setEpisodeTitle(match.group("episodeTitle"))
        self._newDir = self._title

    def _buildNewFileName(self) -> None:
        title = self._title
        season = self._season
        episode = self._episode
        episodeTitle = self._episodeTitle

        newName = f"{title} {season}x{episode}"

        if not episodeTitle == "":
            newName += f" {episodeTitle}"

        self._newFileName = newName + self._getTags()
        self._backupName = f"{self._newDir}.{newName + self._fileExt}"
