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
        self._backupName = f"{self._newDirectory}.{passed + self._fileExtension}"
        # self._newDirectory = self.get

    def _setEpisodeTitle(self, passed: str) -> None:
        # if len(passed) > 0:
        #     if passed[-1] == " ":
        #         self._episodeTitle = passed[:-1]
        #     else:
        #         self._episodeTitle = passed
        # else:
        #     self._episodeTitle = passed
        self._episodeTitle = self._capitalizeAsTitle(passed)

    def _setEpisode(self, passed: str) -> None:
        self._episode = passed

    def _setSeason(self, passed: str) -> None:
        self._season = passed

    ###########
    # GETTERS #
    ###########
    
    def getNewDirectoryName(self) -> str:
        return self._title
    
    def getNewFileNameWithoutTags(self) -> str:
        name = f"{self._title} {self._season}x{self._episode}"

        if not self._episodeTitle == "":
            name += f" {self._episodeTitle}"
        
        return name

    @staticmethod
    def getPattern() -> re.Pattern:
        """ Returns a Pattern object to be used in identifying a Show object. """

        return re.compile(r"^(?P<title>([!0-9a-zA-Z.',_-]+ )+)(- |- (\w+ )+(- )?|)(\(?(?P<date>\d{4})\)? |)"
                          r"(- |- (\w+ )+(- )?|)(|[sS](eason)? ?|)(?P<season>\d{1,2}) ?(x|[eE](pisode)?|) ?"
                          r"(?P<episode>\d{1,2})( |- |$)(?P<episodeTitle>([!0-9a-zA-Z.',_-]+ ?)+)($|[[(]?(\d{3,4}p)?)")
        
        # Old
        # r"^(?P<title>([!0-9a-zA-Z.',_\-]+ )+?)(- (\w+ )+- |- (\w+ )+|- )?([sS]eason|[sS])? ?"
        #                   r"(?P<season>\d{1,2})(x|[eE]pisode|[eE]) ?(?P<episode>\d{1,2})( \[?\d{3,4}p.*| - | |$)"
        #                   r"(?P<episodeTitle>([!0-9a-zA-Z.',_\-]+( |$))+?|$)([[(]?\d{3,4}p|\[|$)")
        # TODO fix shows with dates (1999) registering as movies instead of shows

    #########
    # OTHER #
    #########

    def _buildAttributes(self, match: re.Match) -> None:
        self._setTitle(match.group("title"))
        self._setSeason = match.group("season")
        self._setEpisode = match.group("episode")
        self._setEpisodeTitle(match.group("episodeTitle"))
        self._newDirectory = self._title

    def _buildNewFileName(self) -> None:
        title = self._title
        season = self._season
        episode = self._episode
        episodeTitle = self._episodeTitle

        newName = f"{title} {season}x{episode}"

        if not episodeTitle == "":
            newName += f" {episodeTitle}"

        self._newFileName = newName + self._getTags()
        self._backupName = f"{self._newDirectory}.{newName + self._fileExtension}"
