import unittest, os, sys, datetime

path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if not path in sys.path:
    sys.path.insert(1, path)
del path

import dateparser

class TestSequenceVcsParse(unittest.TestCase):
    """docstring for TestSequenceCSV2JSON"""
    
    def setUp(self):
        pass

    def test_vcs_conversion(self):
        """
        Test for testing the VCS timeformat conversion.

        This tests passes if the valid string 20121213T071000Z is equal to the 
        expected datetime format when parsed through the 
        parseVcsTimeFormat-function.
        
        Observer - the parse Vcs TimeFormat changes the hour from UTC -> CET
        """
        testDataVcs = "20121213T071000Z"
        testDataTime = datetime.datetime(2012, 12, 13, 8, 10, 0, 0)

        test = dateparser.parseVcsTimeFormat(testDataVcs)    

        testDataVcs2 = "20120913T061000Z"
        testDataTime2 = datetime.datetime(2012, 9, 13, 8, 10, 0, 0)

        test2 = dateparser.parseVcsTimeFormat(testDataVcs2)    

        self.assertEqual(test, testDataTime)
        self.assertEqual(test2, testDataTime2)

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

class TestSequenceUtcConversion(unittest.TestCase):
    def setUp(self):
        pass

    def is_dst(self, year, month, date):
        testDataTime = datetime.date(year, month, date)

        return dateparser.is_dst(testDataTime)

    def test_no_dst(self):
        self.assertFalse(self.is_dst(2012, 12, 13))

    def test_no_dst2(self):
        self.assertFalse(self.is_dst(2013, 11, 13))

    def test_no_dst3(self):
        self.assertFalse(self.is_dst(2013, 10, 28))

    def test_dst(self):
        self.assertTrue(self.is_dst(2013, 04, 13))

    def test_dst2(self):
        self.assertTrue(self.is_dst(2013, 10, 26))

    def test_dst3(self):
        self.assertTrue(self.is_dst(2014, 03, 31))

    def tearDown(self):
        pass


if __name__ == '__main__':
    unittest.main()