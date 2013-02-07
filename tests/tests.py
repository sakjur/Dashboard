import unittest, os, sys, datetime

path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if not path in sys.path:
    sys.path.insert(1, path)
del path

import dateparser

class TestSequenceVCS2JSON(unittest.TestCase):
    """docstring for TestSequenceCSV2JSON"""
    
    def setUp(self):
        pass

    def test_confirm_vcs(self):
        self.assertTrue(True)

    def test_vcs_conversion(self):
        """
        Test for testing the VCS timeformat conversion.

        This tests passes if the valid string 20121213T071000Z is equal to the expected
        datetime format when parsed through the parseVcsTimeFormat-function.
        """
        testDataVcs = "20121213T071000Z"
        testDataTime = datetime.datetime(2012, 12, 13, 7, 10, 0, 0)

        test = dateparser.parseVcsTimeFormat(testDataVcs)    
        self.assertEqual(test, testDataTime)

    def test_vcs_wrong_format(self):
        """
        Test for the VCS timeformat conversion.

        This test passes if all of the invalid inputs  raises the expected
        exception when parsed to parseVcsTimeFormat.
        """

        with self.assertRaisesRegexp(ValueError, 'Empty'):
            # Tries if empty strings raises the empty-exception.
            dateparser.parseVcsTimeFormat("")

        with self.assertRaisesRegexp(TypeError, 'Wrong type'):
            # Tests if non-strings raises the wrong type-exception.
            dateparser.parseVcsTimeFormat(["12", "12", "13", "07", "10"])
            dateparser.parseVcsTimeFormat(15)

        with self.assertRaisesRegexp(ValueError, 'Swapped'):
            # Swapped place of Z and T
            dateparser.parseVcsTimeFormat("20121213Z071000T") # Z and T swapped

        with self.assertRaises(Exception):
            # Tests if a few other inputs raises the Unknown error-exception.
            dateparser.parseVcsTimeFormat("19940226 15:00") # Wrong datetime

    def test_vcs_datetime(self):
        """
        This is basically testing the datetime.datetime() function that is
        called from parseVcsTimeFormat()
        """

        with self.assertRaises(ValueError):
            # Checks if datetime.datetime() raises a value error on not a date
            dateparser.parseVcsTimeFormat("20121313T071000Z") # Not a date

        with self.assertRaises(TypeError):
            # Checks if datetime.datetime() raises a type error on wrong type
            datetime.datetime(2012, "test", 13, 7, 10, 0, 0)

    def test_teDate(self):
        """
        Testing if conversion to TimeEdit-format is done correctly
        """
        testDataTime = datetime.datetime(2012, 12, 13, 7, 10, 0, 0)

        test = dateparser.teDate(testDataTime)    
        self.assertEqual(test, "1250")


    def tearDown(self):
        pass


if __name__ == '__main__':
    unittest.main()