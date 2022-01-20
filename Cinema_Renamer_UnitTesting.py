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
validDir = "testing\\validDir"  # 4 validly-named files within (invalid types tho), plus 1 invalid file
uncorrectedFileDir = f"testing\\uncorrectedFile"
correctedFileDir = f"testing\\correctedFile"


class CinemaParserTestCase(unittest.TestCase):

    parser = Parser()

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

    sampleNonsense = "testing\\validDir\\something something test case.txt"

    validFileList = [easyShow, simpleMovie, hardShow, hardMovie]
    validMixedList = validFileList + [validDir]
    invalidMixedList = validFileList + [invalidDir]

    def testRecognizeSimpleShow(self):
        self.parser.parseCinemaPaths(self.simpleShow)
        show = self.parser.getUnprocessedCinemaList()
        self.assertIsInstance(show[0], Show)
        self.assertTrue(show[0].hasError())
        self.assertEqual("Legion 01x06", show[0].getNewFileName())

    def testParseEasyShow(self):
        self.parser.parseCinemaPaths(self.easyShow)
        show = self.parser.getUnprocessedCinemaList()
        self.assertIsInstance(show[0], Show)
        self.assertEqual("Rick and Morty 05x05 [720p] [x264]", show[0].getNewFileName())

    def testParseMediumShow(self):
        self.parser.parseCinemaPaths(self.mediumShow)
        show = self.parser.getUnprocessedCinemaList()
        self.assertIsInstance(show[0], Show)
        self.assertEqual("Ghost Adventures 20x00 Curse of the Harrisville Farmhouse [1080p] [x264]",
                         show[0].getNewFileName())

    def testParseHardShow(self):
        self.parser.parseCinemaPaths(self.hardShow)
        show = self.parser.getUnprocessedCinemaList()
        self.assertIsInstance(show[0], Show)
        self.assertEqual("Shingeki No Kyojin 04x10 A Sound Argument", show[0].getNewFileName())

    def testRecognizeSpecialCharsShow(self):
        self.parser.parseCinemaPaths(self.specialCharsShow)
        show = self.parser.getUnprocessedCinemaList()
        self.assertIsInstance(show[0], Show)
        self.assertEqual("Konosuba 01x02 An Explosion for This Chuunibyou!", show[0].getNewFileName())

    def testRecognizeSimpleMovie(self):
        self.parser.parseCinemaPaths(self.simpleMovie)
        movie = self.parser.getUnprocessedCinemaList()
        self.assertIsInstance(movie[0], Movie)
        self.assertEqual("Amateur Night (2016)", movie[0].getNewFileName())

    def testParseEasyMovie(self):
        self.parser.parseCinemaPaths(self.easyMovie)
        movie = self.parser.getUnprocessedCinemaList()
        self.assertIsInstance(movie[0], Movie)
        self.assertEqual("Amateur Night (2016) [720p]", movie[0].getNewFileName())

    def testParseMediumMovie(self):
        self.parser.parseCinemaPaths(self.mediumMovie)
        movie = self.parser.getUnprocessedCinemaList()
        self.assertIsInstance(movie[0], Movie)
        self.assertIsNone(movie[0].getError())
        self.assertEqual("Anchorman the Legend of Ron Burgundy (2004) [1080p] [x264]", movie[0].getNewFileName())

    def testParseHardMovie(self):
        self.parser.parseCinemaPaths(self.hardMovie)
        movie = self.parser.getUnprocessedCinemaList()
        self.assertIsInstance(movie[0], Movie)
        self.assertIsNone(movie[0].getError())
        self.assertEqual("American History X (1998) [1080p] [x264]", movie[0].getNewFileName())

    def testParseUniqueCharsMovie(self):
        self.parser.parseCinemaPaths(self.uniqueCharsMovie)
        movie = self.parser.getUnprocessedCinemaList()
        self.assertIsInstance(movie[0], Movie)
        self.assertIsNone(movie[0].getError())
        self.assertEqual("As Above, So Below (2014) [1080p] [x264]", movie[0].getNewFileName())

    def testCreateUnknown(self):
        self.parser.parseCinemaPaths(self.sampleNonsense)
        unknown = self.parser.getUnprocessedCinemaList()
        self.assertIsInstance(unknown[0], Unknown)

    def testListOfValidFiles(self):
        self.parser.parseCinemaPaths(self.validFileList)
        cinemaList = self.parser.getUnprocessedCinemaList()

        for obj in cinemaList:
            self.assertNotIsInstance(obj, Unknown)

    def testValidDir(self):
        self.parser.parseCinemaPaths(validDir)
        dirContents = self.parser.getUnprocessedCinemaList()
        for obj in dirContents:
            self.assertNotIsInstance(obj, Unknown)
        assert len(dirContents) == 4

    def testInvalidDirectory(self):
        self.parser.parseCinemaPaths(invalidDir)
        sampleDir = self.parser.getUnprocessedCinemaList()
        self.assertIsInstance(sampleDir[0], Unknown)
        assert len(sampleDir) == 1

    def testListOfFilesPlusValidDirectory(self):
        self.parser.parseCinemaPaths(self.validMixedList)
        mixed = self.parser.getUnprocessedCinemaList()
        for obj in mixed:
            self.assertNotIsInstance(obj, Unknown)
        assert len(mixed) == 8

    def testListOfFilesPlusInvalidDirectory(self):
        self.parser.parseCinemaPaths(self.invalidMixedList)
        mixed = self.parser.getUnprocessedCinemaList()
        unknownCount = 0
        for obj in mixed:
            if isinstance(obj, Unknown):
                unknownCount += 1
        assert len(mixed) == 5
        assert unknownCount == 1


class CinemaDatabasePickleTestCase(unittest.TestCase):

    parser = Parser()
    parser.parseCinemaPaths(uncorrectedFileDir)
    singleFile = parser.getUnprocessedCinemaList()
    database = DatabasePickle()

    def testCreateAndDeleteRecord(self):
        self.database.create(self.singleFile[0])
        self.assertTrue(os.path.exists(f"{self.database.DIRECTORY}\\"
                                       f"{self.singleFile[0].getNewFileName() + self.singleFile[0].getFileExt()}"
                                       f"{self.database.EXT}"))
        self.database.delete(self.singleFile[0])
        self.assertFalse(os.path.exists(f"{self.database.DIRECTORY}\\"
                                        f"{self.singleFile[0].getNewFileName() + self.singleFile[0].getFileExt()}"
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

    def testCreateDuplicateRecord(self):
        self.database.create(self.singleFile[0])
        self.assertRaises(FileExistsError, self.database.create, self.singleFile[0])
        # self.database.create(self.singleFile[0])
        self.assertTrue(os.path.exists(f"{self.database.DIRECTORY}\\"
                                       f"{self.singleFile[0].getNewFileName() + self.singleFile[0].getFileExt()}"
                                       f"{self.database.EXT}"))
        # self.assertTrue(os.path.exists(f"{self.database.DIRECTORY}\\"
        #                                f"{self.singleFile[0].getNewFileName()}(1){self.singleFile[0].getFileExt()}"
        #                                f"{self.database.EXT}"))
        self.database.delete(self.singleFile[0])

    # def testOverwriteRecord(self):
    #     pass


class CinemaHandlerTestCase(unittest.TestCase):
    parser = Parser()
    database = DatabasePickle()
    handler = Handler(database)

    parser.parseCinemaPaths(uncorrectedFileDir)
    uncorrectedFile = parser.getUnprocessedCinemaList()
    uncorrectedPath = f"{database.DIRECTORY}\\" \
                      f"{uncorrectedFile[0].getNewFileName() + uncorrectedFile[0].getFileExt()}{database.EXT}"
    # correctedFile = parser.getUnprocessedCinemaList()
    # fileList = parser.getUnprocessedCinemaList()
    # picklePaths = []
    # for obj in fileList:
    #     if not obj.getError():
    #         picklePaths.append(f"{database.DIRECTORY}\\{obj.getNewFileName()}{obj.getFileExt()}{database.EXT}")

    def testRenameCorrectedFile(self):
        correctedFile = self.parser.parseAndGetList(correctedFileDir)
        self.assertRaises(ValueError, self.handler.createBackupAndRename, correctedFile[0])
        self.assertTrue(correctedFile[0].getError())
        self.assertTrue(os.path.exists(f"{correctedFile[0].getOldAbsPath()}"))
        errorFile = self.parser.getErrorCinemaList()
        assert len(errorFile) == 1

    def testRenameAndRestoreUncorrectedFile(self):
        self.assertFalse(os.path.exists(f"{self.uncorrectedFile[0].getNewAbsPath()}"))

        self.handler.createBackupAndRename(self.uncorrectedFile[0])
        self.assertTrue(os.path.exists(f"{self.uncorrectedFile[0].getNewAbsPath()}"))
        self.assertFalse(os.path.exists(f"{self.uncorrectedFile[0].getOldAbsPath()}"))

        self.handler.restoreFromBackup(self.uncorrectedPath)
        self.assertFalse(os.path.exists(f"{self.uncorrectedFile[0].getNewAbsPath()}"))
        self.assertTrue(os.path.exists(f"{self.uncorrectedFile[0].getOldAbsPath()}"))

    # def testRenameAndRestoreMultipleFiles(self):
    #     for obj in self.fileList:
    #         self.handler.createBackupAndRename(obj)
    #
    #     for obj in self.fileList:
    #         if not obj.getError():
    #             self.assertTrue(os.path.exists(f"{obj.getNewAbsPath()}"))
    #
    #     for path in self.picklePaths:
    #         self.handler.restoreFromBackup(path)
    #
    #     for obj in self.fileList:
    #         if not obj.getError():
    #             self.assertFalse(os.path.exists(obj.getNewAbsPath()))

    # def testHandleDuplicate(self):
    #     pass


if __name__ == "__main__":
    unittest.main()
