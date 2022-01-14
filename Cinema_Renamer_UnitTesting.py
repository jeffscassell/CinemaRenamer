import os
import unittest
# from unittest.mock import patch

from cinemaParser import Parser
from cinema import Cinema
from movie import Movie
from show import Show
from unknown import Unknown
from databasePickle import DatabasePickle
from handler import Handler

invalidDir = "testing\\invalidDir"
validDir = "testing"  # 4 validly-named files within (invalid types tho), plus 1 invalid file
uncorrectedFileDir = f"{validDir}\\uncorrectedFile"
correctedFileDir = f"{validDir}\\correctedFile"


class CinemaParserTestCase(unittest.TestCase):

    showPath = "testing\\tv shows"
    moviePath = "testing\\movies"

    simpleShow = f"{showPath}\\Legion 01x06.txt"
    easyShow = f"{showPath}\\Rick.and.Morty.S05E05.720p.WEBRip.x264-BAE.txt"
    mediumShow = f"{showPath}\\Ghost.Adventures.S20E00.Curse.of.the.Harrisville.Farmhouse.1080p.WEB.x264-CAFFEiNE.txt"
    hardShow = f"{showPath}\\Shingeki no Kyojin - The Final Season - S04E10 - A Sound Argument.txt"
    namedEpisodeShow = f"{showPath}\\The Office 05x03 Baby Shower.txt"
    specialCharsShow = f"{showPath}\\Konosuba 01x02 An Explosion For This Chuunibyou!.txt"

    simpleMovie = f"{moviePath}\\Amateur Night (2016).txt"
    easyMovie = f"{moviePath}\\Amateur Night (2016) 720p.txt"
    mediumMovie = f"{moviePath}\\Anchorman.The.Legend.of.Ron.Burgundy.2004.1080p.BluRay.H264.AAC-RARBG.txt"
    hardMovie = f"{moviePath}\\American.History.X.1998.1080p.BluRay.x264.anoXmous_.txt"
    uniqueCharsMovie = f"{moviePath}\\As.Above,.So.Below.2014.1080p.BluRay.x264.YIFY.txt"

    sampleNonsense = "testing\\something something test case.txt"

    validFileList = [easyShow, simpleMovie, hardShow, hardMovie]
    validMixedList = validFileList + [validDir]
    invalidMixedList = validFileList + [invalidDir]

    parser = Parser()

    def testRecognizeSimpleShow(self):
        show = self.parser.getCinemaList(self.simpleShow)
        self.assertIsInstance(show[0], Show)
        self.assertTrue(show[0].hasError())
        self.assertEqual("Legion 01x06", show[0].getNewFileName())

    def testParseEasyShow(self):
        show = self.parser.getCinemaList(self.easyShow)
        self.assertIsInstance(show[0], Show)
        self.assertEqual("Rick and Morty 05x05 [720p] [x264]", show[0].getNewFileName())

    def testParseMediumShow(self):
        show = self.parser.getCinemaList(self.mediumShow)
        self.assertIsInstance(show[0], Show)
        self.assertEqual("Ghost Adventures 20x00 Curse of the Harrisville Farmhouse [1080p] [x264]",
                         show[0].getNewFileName())

    def testParseHardShow(self):
        show = self.parser.getCinemaList(self.hardShow)
        self.assertIsInstance(show[0], Show)
        self.assertEqual("Shingeki No Kyojin 04x10 A Sound Argument", show[0].getNewFileName())

    def testRecognizeSpecialCharsShow(self):
        show = self.parser.getCinemaList(self.specialCharsShow)
        self.assertIsInstance(show[0], Show)
        self.assertEqual("Konosuba 01x02 An Explosion for This Chuunibyou!", show[0].getNewFileName())

    def testRecognizeSimpleMovie(self):
        movie = self.parser.getCinemaList(self.simpleMovie)
        self.assertIsInstance(movie[0], Movie)
        self.assertEqual("Amateur Night (2016)", movie[0].getNewFileName())

    def testParseEasyMovie(self):
        movie = self.parser.getCinemaList(self.easyMovie)
        self.assertIsInstance(movie[0], Movie)
        self.assertEqual("Amateur Night (2016) [720p]", movie[0].getNewFileName())

    def testParseMediumMovie(self):
        movie = self.parser.getCinemaList(self.mediumMovie)
        self.assertIsInstance(movie[0], Movie)
        self.assertIsNone(movie[0].getError())
        self.assertEqual("Anchorman the Legend of Ron Burgundy (2004) [1080p] [x264]", movie[0].getNewFileName())

    def testParseHardMovie(self):
        movie = self.parser.getCinemaList(self.hardMovie)
        self.assertIsInstance(movie[0], Movie)
        self.assertIsNone(movie[0].getError())
        self.assertEqual("American History X (1998) [1080p] [x264]", movie[0].getNewFileName())

    def testParseUniqueCharsMovie(self):
        movie = self.parser.getCinemaList(self.uniqueCharsMovie)
        self.assertIsInstance(movie[0], Movie)
        self.assertIsNone(movie[0].getError())
        self.assertEqual("As Above, So Below (2014) [1080p] [x264]", movie[0].getNewFileName())

    def testCreateUnknown(self):
        unknown = self.parser.getCinemaList(self.sampleNonsense)
        self.assertIsInstance(unknown[0], Unknown)

    def testListOfValidFiles(self):
        cinemaList = self.parser.getCinemaList(self.validFileList)

        for obj in cinemaList:
            self.assertNotIsInstance(obj, Unknown)

    def testValidDir(self):
        dirContents = self.parser.getCinemaList(validDir)
        for obj in dirContents:
            self.assertNotIsInstance(obj, Unknown)
        assert len(dirContents) == 4

    def testInvalidDirectory(self):
        sampleDir = self.parser.getCinemaList(invalidDir)
        self.assertIsInstance(sampleDir[0], Unknown)
        assert len(sampleDir) == 1

    def testListOfFilesPlusValidDirectory(self):
        mixed = self.parser.getCinemaList(self.validMixedList)
        for obj in mixed:
            self.assertNotIsInstance(obj, Unknown)
        assert len(mixed) == 8

    def testListOfFilesPlusInvalidDirectory(self):
        mixed = self.parser.getCinemaList(self.invalidMixedList)
        unknownCount = 0
        for obj in mixed:
            if isinstance(obj, Unknown):
                unknownCount += 1
        assert len(mixed) == 5
        assert unknownCount == 1

    # def testError(self):
    #     pass  # what was i going to test here??? too late to be coding still


class CinemaDatabasePickleTestCase(unittest.TestCase):

    parser = Parser()
    fileList = parser.getCinemaList(validDir)
    singleFile = parser.getCinemaList(uncorrectedFileDir)
    database = DatabasePickle()

    def testCreateAndDeleteRecord(self):
        self.database.create(self.singleFile[0])
        self.assertTrue(os.path.exists(f"{self.database.DIRECTORY}\\"
                                       f"{self.singleFile[0].getNewFileName()}{self.singleFile[0].getFileExt()}"
                                       f"{self.database.EXT}"))
        self.database.delete(self.singleFile[0])
        self.assertFalse(os.path.exists(f"{self.database.DIRECTORY}\\"
                                        f"{self.singleFile[0].getNewFileName()}{self.singleFile[0].getFileExt()}"
                                        f"{self.database.EXT}"))

    def testReadRecord(self):
        self.database.create(self.singleFile[0])
        cinema = self.database.read(f"{self.database.DIRECTORY}\\"
                                    f"{self.singleFile[0].getNewFileName()}{self.singleFile[0].getFileExt()}"
                                    f"{self.database.EXT}")
        self.assertIsInstance(cinema, Cinema)
        self.database.delete(self.singleFile[0])
        self.assertFalse(os.path.exists(f"{self.database.DIRECTORY}\\"
                                        f"{self.singleFile[0].getNewFileName()}{self.singleFile[0].getFileExt()}"
                                        f"{self.database.EXT}"))

    def testReadFalseEmptyRecord(self):
        self.assertRaises(ValueError, self.database.read,
                          r"C:\Users\Jeff\PycharmProjects\CinemaRenamer\testing\fakeEmpty.pkl")

    def testReadFalseNonEmptyRecord(self):
        self.assertRaises(ValueError, self.database.read,
                          r"C:\Users\Jeff\PycharmProjects\CinemaRenamer\testing\fakeNonEmpty.pkl")

    def testCreateDuplicate(self):
        self.database.create(self.singleFile[0])
        self.database.create(self.singleFile[0])
        self.assertTrue(os.path.exists(f"{self.database.DIRECTORY}\\"
                                       f"{self.singleFile[0].getNewFileName()}{self.singleFile[0].getFileExt()}"
                                       f"{self.database.EXT}"))
        self.assertTrue(os.path.exists(f"{self.database.DIRECTORY}\\"
                                       f"{self.singleFile[0].getNewFileName()}(1){self.singleFile[0].getFileExt()}"
                                       f"{self.database.EXT}"))

    # def testOverwriteRecord(self):
    #     pass


class CinemaHandlerTestCase(unittest.TestCase):
    parser = Parser()
    database = DatabasePickle()
    handler = Handler(database)

    uncorrectedFile = parser.getCinemaList(uncorrectedFileDir)
    uncorrectedPath = f"{database.DIRECTORY}\\" \
                      f"{uncorrectedFile[0].getNewFileName()}{uncorrectedFile[0].getFileExt()}{database.EXT}"
    correctedFile = parser.getCinemaList(correctedFileDir)
    fileList = parser.getCinemaList(validDir)
    picklePaths = []
    for obj in fileList:
        if not obj.getError():
            picklePaths.append(f"{database.DIRECTORY}\\{obj.getNewFileName()}{obj.getFileExt()}{database.EXT}")

    def testRenameCorrectedFile(self):
        self.assertRaises(ValueError, self.handler.rename, self.correctedFile[0])
        self.assertTrue(self.correctedFile[0].getError())
        self.assertTrue(os.path.exists(f"{self.correctedFile[0].getOldAbsPath()}"))

    def testRenameAndRestoreUncorrectedFile(self):
        self.handler.rename(self.uncorrectedFile[0])
        self.assertTrue(os.path.exists(f"{self.uncorrectedFile[0].getNewAbsPath()}"))
        self.assertFalse(os.path.exists(f"{self.uncorrectedFile[0].getOldAbsPath()}"))

        self.handler.restore(self.uncorrectedPath)
        self.assertFalse(os.path.exists(f"{self.uncorrectedFile[0].getNewAbsPath()}"))
        self.assertTrue(os.path.exists(f"{self.uncorrectedFile[0].getOldAbsPath()}"))

    def testRenameAndRestoreMultipleFiles(self):
        for obj in self.fileList:
            self.handler.rename(obj)

        for obj in self.fileList:
            if not obj.getError():
                self.assertTrue(os.path.exists(f"{obj.getNewAbsPath()}"))

        for path in self.picklePaths:
            self.handler.restore(path)

        for obj in self.fileList:
            if not obj.getError():
                self.assertFalse(os.path.exists(obj.getNewAbsPath()))

    # def testHandleDuplicate(self):
    #     pass


if __name__ == "__main__":
    unittest.main()
