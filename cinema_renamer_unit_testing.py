from genericpath import exists
import os
import unittest
# from unittest.mock import patch

from cinemaParser import CinemaParser
from cinema import Cinema
from movie import Movie
from show import Show
from unknown import Unknown
from databasePickle import DatabasePickle
from fileHandler import FileHandler

testDir = "C:\\Users\\Jeff C\\Documents\\Programming\\Python\\CinemaRenamer\\testing"
invalidDir = f"{testDir}\\invalidDir"
validDir = f"{testDir}\\validDir"  # 4 validly-named files within (invalid types tho), plus 1 invalid file
uncorrectedFileDir = f"{testDir}\\uncorrectedFileDir"
correctedFileDir = f"{testDir}\\Corrected (1999) [720p]"


class CinemaParserTestCase(unittest.TestCase):

    parser = CinemaParser()

    def testShowRecognition(self):
        pass

    # showPath = f"{testDir}\\tv shows"
    # moviePath = f"{testDir}\\movies"

    # simpleShow = f"{showPath}\\Legion 01x06.txt"
    # easyShow = f"{showPath}\\Rick.and.Morty.S05E05.720p.WEBRip.x264-BAE.txt"
    # mediumShow = f"{showPath}\\Ghost.Adventures.S20E00.Curse.of.the.Harrisville.Farmhouse.1080p.WEB.x264-CAFFEiNE.txt"
    # hardShow = f"{showPath}\\Shingeki no Kyojin - The Final Season - S04E10 - A Sound Argument.txt"
    # namedEpisodeShow = f"{showPath}\\The Office 05x03 Baby Shower.txt"
    # specialCharsShow = f"{showPath}\\Konosuba 01x02 An Explosion For This Chuunibyou!.txt"

    # simpleMovie = f"{moviePath}\\Amateur Night (2016).txt"
    # easyMovie = f"{moviePath}\\Amateur Night (2016) 720p.txt"
    # mediumMovie = f"{moviePath}\\Anchorman.The.Legend.of.Ron.Burgundy.2004.1080p.BluRay.H264.AAC-RARBG.txt"
    # hardMovie = f"{moviePath}\\American.History.X.1998.1080p.BluRay.x264.anoXmous_.txt"
    # uniqueCharsMovie = f"{moviePath}\\As.Above,.So.Below.2014.1080p.BluRay.x264.YIFY.txt"

    # sampleNonsense = f"{validDir}\\something something test case.txt"

    # validFileList = [easyShow, simpleMovie, hardShow, hardMovie]
    # validMixedList = validFileList + [validDir]
    # invalidMixedList = validFileList + [invalidDir]

    # def testRecognizeSimpleShow(self):
    #     self.parser.parseCinemaPathsList(self.simpleShow)
    #     show = self.parser.getUnprocessedCinemaList()[0]
    #     self.assertIsInstance(show, Show)
    #     self.assertTrue(show.hasCorrectFileName())
    #     self.assertEqual("Legion 01x06", show.getNewFileName())

    # def testParseEasyShow(self):
    #     self.parser.parseCinemaPathsList(self.easyShow)
    #     show = self.parser.getUnprocessedCinemaList()[0]
    #     self.assertIsInstance(show, Show)
    #     self.assertEqual("Rick and Morty 05x05 [720p] [x264]", show.getNewFileName())

    # def testParseMediumShow(self):
    #     self.parser.parseCinemaPathsList(self.mediumShow)
    #     show = self.parser.getUnprocessedCinemaList()[0]
    #     self.assertIsInstance(show, Show)
    #     self.assertEqual("Ghost Adventures 20x00 Curse of the Harrisville Farmhouse [1080p] [x264]",
    #                      show.getNewFileName())

    # def testParseHardShow(self):
    #     self.parser.parseCinemaPathsList(self.hardShow)
    #     show = self.parser.getUnprocessedCinemaList()[0]
    #     self.assertIsInstance(show, Show)
    #     self.assertEqual("Shingeki No Kyojin 04x10 A Sound Argument", show.getNewFileName())

    # def testRecognizeSpecialCharsShow(self):
    #     self.parser.parseCinemaPathsList(self.specialCharsShow)
    #     show = self.parser.getUnprocessedCinemaList()[0]
    #     self.assertIsInstance(show, Show)
    #     self.assertEqual("Konosuba 01x02 An Explosion for This Chuunibyou!", show.getNewFileName())

    # def testRecognizeSimpleMovie(self):
    #     self.parser.parseCinemaPathsList(self.simpleMovie)
    #     movie = self.parser.getUnprocessedCinemaList()[0]
    #     self.assertIsInstance(movie, Movie)
    #     self.assertEqual("Amateur Night (2016)", movie.getNewFileName())

    # def testParseEasyMovie(self):
    #     self.parser.parseCinemaPathsList(self.easyMovie)
    #     movie = self.parser.getUnprocessedCinemaList()[0]
    #     self.assertIsInstance(movie, Movie)
    #     self.assertEqual("Amateur Night (2016) [720p]", movie.getNewFileName())

    # def testParseMediumMovie(self):
    #     self.parser.parseCinemaPathsList(self.mediumMovie)
    #     movie = self.parser.getUnprocessedCinemaList()[0]
    #     self.assertIsInstance(movie, Movie)
    #     self.assertIsNone(movie.getError())
    #     self.assertEqual("Anchorman the Legend of Ron Burgundy (2004) [1080p] [x264]", movie.getNewFileName())

    # def testParseHardMovie(self):
    #     self.parser.parseCinemaPathsList(self.hardMovie)
    #     movie = self.parser.getUnprocessedCinemaList()[0]
    #     self.assertIsInstance(movie, Movie)
    #     self.assertIsNone(movie.getError())
    #     self.assertEqual("American History X (1998) [1080p] [x264]", movie.getNewFileName())

    # def testParseUniqueCharsMovie(self):
    #     self.parser.parseCinemaPathsList(self.uniqueCharsMovie)
    #     movie = self.parser.getUnprocessedCinemaList()[0]
    #     self.assertIsInstance(movie, Movie)
    #     self.assertIsNone(movie.getError())
    #     self.assertEqual("As Above, So Below (2014) [1080p] [x264]", movie.getNewFileName())

    # def testCreateUnknown(self):
    #     self.parser.parseCinemaPathsList(self.sampleNonsense)
    #     unknown = self.parser.getUnprocessedCinemaList()[0]
    #     self.assertIsInstance(unknown, Unknown)

    # def testListOfValidFiles(self):
    #     self.parser.parseCinemaPathsList(self.validFileList)
    #     cinemaList = self.parser.getUnprocessedCinemaList()

    #     for obj in cinemaList:
    #         self.assertNotIsInstance(obj, Unknown)

    # def testValidDir(self):
    #     self.parser.parseCinemaPathsList(validDir)
    #     dirContents = self.parser.getUnprocessedCinemaList()
    #     for obj in dirContents:
    #         self.assertNotIsInstance(obj, Unknown)
    #     assert len(dirContents) == 4

    # def testInvalidDirectory(self):
    #     self.parser.parseCinemaPathsList(invalidDir)
    #     sampleDir = self.parser.getUnprocessedCinemaList()
    #     self.assertIsInstance(sampleDir[0], Unknown)
    #     assert len(sampleDir) == 1

    # def testListOfFilesPlusValidDirectory(self):
    #     self.parser.parseCinemaPathsList(self.validMixedList)
    #     mixed = self.parser.getUnprocessedCinemaList()
    #     for obj in mixed:
    #         self.assertNotIsInstance(obj, Unknown)
    #     assert len(mixed) == 8

    # def testListOfFilesPlusInvalidDirectory(self):
    #     self.parser.parseCinemaPathsList(self.invalidMixedList)
    #     mixed = self.parser.getUnprocessedCinemaList()
    #     unknownCount = 0
    #     for obj in mixed:
    #         if isinstance(obj, Unknown):
    #             unknownCount += 1
    #     assert len(mixed) == 5
    #     assert unknownCount == 1


class CinemaDatabasePickleTestCase(unittest.TestCase):

    parser = CinemaParser()
    parser.parseCinemaPathsList(uncorrectedFileDir)
    correctedFile = parser.getUnprocessedCinemaList()[0]
    database = DatabasePickle()
    correctedFileBackupPath = f"{database.BACKUP_PATH}\\{correctedFile.getBackupName()}{database.BACKUP_EXTENSION}"

    def testCreateAndDeleteRecord(self):
        self.assertFalse(os.path.exists(self.correctedFileBackupPath))
        self.database.create(self.correctedFile)
        self.assertTrue(os.path.exists(self.correctedFileBackupPath))
        self.database.delete(self.correctedFile)
        self.assertFalse(os.path.exists(self.correctedFileBackupPath))

    def testReadRecord(self):
        self.assertFalse(os.path.exists(self.correctedFileBackupPath))
        self.database.create(self.correctedFile)
        cinema = self.database.read(self.correctedFileBackupPath)
        self.assertIsInstance(cinema, Cinema)
        self.database.delete(cinema)
        self.assertFalse(os.path.exists(self.correctedFileBackupPath))

    def testReadFalseEmptyRecord(self):
        self.assertRaises(EOFError, self.database.read,
                          f"{testDir}\\fakeEmpty.pkl")

    def testReadFalseNonEmptyRecord(self):
        self.assertRaises(ValueError, self.database.read,
                          f"{testDir}\\fakeNonEmpty.pkl")

    def testCreateDuplicateRecord(self):
        self.assertFalse(os.path.exists(self.correctedFileBackupPath))
        self.database.create(self.correctedFile)
        self.assertRaises(FileExistsError, self.database.create, self.correctedFile)
        self.assertTrue(os.path.exists(self.correctedFileBackupPath))
        self.database.delete(self.correctedFile)
        self.assertFalse(os.path.exists(self.correctedFileBackupPath))

    def testOverwriteRecord(self):
        self.assertFalse(os.path.exists(self.correctedFileBackupPath))
        self.database.create(self.correctedFile)
        self.assertTrue(os.path.exists(self.correctedFileBackupPath))
        self.database.update(self.correctedFile)  # would have to check write times between creation and updating to verify update occurred
        self.database.delete(self.correctedFile)
        self.assertFalse(os.path.exists(self.correctedFileBackupPath))

    def testAppendRecord(self):
        self.assertFalse(os.path.exists(self.correctedFileBackupPath))
        self.database.create(self.correctedFile)
        self.assertTrue(os.path.exists(self.correctedFileBackupPath))
        
        origBackupName = self.correctedFile.getBackupName()
        appendAbs = f"{self.database.BACKUP_PATH}\\{self.correctedFile.getBackupName()}(1){self.database.BACKUP_EXTENSION}"
        self.database.createAppend(self.correctedFile)
        self.assertTrue(os.path.exists(appendAbs))
        self.database.delete(self.correctedFile)
        self.assertFalse(os.path.exists(appendAbs))

        self.correctedFile.setBackupName(origBackupName)
        self.database.delete(self.correctedFile)
        self.assertFalse(os.path.exists(self.correctedFileBackupPath))

    # def testRestoreBackupObj(self):



class CinemaHandlerTestCase(unittest.TestCase):
    parser = CinemaParser()
    database = DatabasePickle()
    handler = FileHandler(database)

    parser.parseCinemaPathsList(uncorrectedFileDir)
    uncorrectedFile = parser.getUnprocessedCinemaList()[0]
    uncorrectedPath = f"{database.BACKUP_PATH}\\" \
                      f"{uncorrectedFile.getBackupName()}{database.BACKUP_EXTENSION}"
    # correctedFile = parser.getUnprocessedCinemaList()
    # fileList = parser.getUnprocessedCinemaList()
    # picklePaths = []
    # for obj in fileList:
    #     if not obj.getError():
    #         picklePaths.append(f"{database.BACKUP_PATH}\\{obj.getNewFileName()}{obj.getFileExtension()}{database.EXT}")
    movieDir = r"C:\Users\Jeff C\Documents\Programming\Python\CinemaRenamer\testing\movies"
    showDir = r"C:\Users\Jeff C\Documents\Programming\Python\CinemaRenamer\testing\tv shows"

    # TODO write test cases from handler's new integration method

    # def testCopyToNewDirectory(self):

    # def testRenameAndRestoreUncorrectedFile(self):

    # def testRenameAndRestoreMultipleFiles(self):

    # def testHandleDuplicate(self):
    #     pass


if __name__ == "__main__":
    unittest.main()
