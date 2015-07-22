import itertools
import os
import pandas
import sys
import unittest
import data_summary

TESTS_DIR               = 'testcases/'
ACTUAL_XLS_PATH         = 'actual.xls'
EXPECTED_XLS_PATH       = 'test_expected.xls'

class TestDataSummary(unittest.TestCase):
    def __init__(self, testName, dataDir, expectedXlsPath, actualXlsPath, methodName='runTest'):
        super(TestDataSummary, self).__init__(methodName)
        self.longMessage = True

        self.testName = testName
        self.dataDir = dataDir
        self.expectedXlsPath = expectedXlsPath
        self.actualXlsPath = actualXlsPath

    def tearDown(self):
        os.remove(self.actualXlsPath)

    def assertExcelEqual(self, actual, expected):
        # assert actual and expected excel docs have the same # of columns
        self.assertEqual(
            len(actual.columns), 
            len(expected.columns), 
            "test '%s' : column count mismatch" % (self.testName,)
        )

        for actual_column, expected_column in zip(actual.columns, expected.columns):
            # assert that the column names are equal
            self.assertEqual(
                actual_column, 
                expected_column,
                "test '%s' : column name mismatch" % (self.testName,)
            )

            # assert that the column values are equal
            actual_series = [str(i) for i in actual[actual_column]]
            expected_series = [str(i) for i in expected[expected_column]]

            self.assertSequenceEqual(
                actual_series, 
                expected_series, 
                "test '%s' : value mismatch at column '%s'" % (self.testName, expected_column,)
            )

    def runTest(self):
        data_summary.main(self.dataDir, self.actualXlsPath)

        # assert that the actual excel doc was produced
        self.assertTrue(os.path.isfile(self.actualXlsPath))

        expected = pandas.read_excel(self.expectedXlsPath, data_summary.SHEET_NAME)
        actual = pandas.read_excel(self.actualXlsPath, data_summary.SHEET_NAME)

        # assert that the two excel docs are equal
        self.assertExcelEqual(expected, actual)

def tests(testsDir, actualXlsPath, expectedXlsPath):
    for f in os.listdir(testsDir):
        testName = f
        dataDir = os.path.join(testsDir, f)
        _expectedXlsPath = os.path.join(dataDir, expectedXlsPath)

        if os.path.isdir(dataDir) == False:
            continue

        if os.path.isfile(_expectedXlsPath) == False:
            continue

        test = TestDataSummary(testName, dataDir, _expectedXlsPath, actualXlsPath)
        yield test

def main(testsDir, actualXlsPath, expectedXlsPath):
    t = tests(testsDir, actualXlsPath, expectedXlsPath)
    suite = unittest.TestSuite(t)
    unittest.TextTestRunner().run(suite)

if __name__ == '__main__':
    main(TESTS_DIR, ACTUAL_XLS_PATH, EXPECTED_XLS_PATH)
