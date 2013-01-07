# Datetest

import os, sys, datetime, re

path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if not path in sys.path:
    sys.path.insert(1, path)
del path

import dateparser

print("==========================")
print("Testing the date-functions")
print("==========================\n")

def parseVcsTimeFormatTest():

	tests = {
	"passWorking": 		"20121213T071000Z",
	"failTypo":			"20121213Z071000T",
	"failWrongFormat":	"19940226 15:00",
	"failNotDate":		"20121312T251000",
	"failNotString":	["20121213T071000Z"]
	}

	testRun(tests, dateparser.parseVcsTimeFormat)

def diffFromUtcTest():

	tests = {
	"passWorking": 	datetime.datetime(2012, 12, 18, 11, 9, 6, 861000),
	"failString":	"THISWILLFAIL"
	}

	testRun(tests, dateparser.diffFromUtc)

def testRun(tests, func):

	output = []

	for test, value in tests.iteritems():
		try:
			func(value)
			if test[:4] == "pass":
				output.append(test[4:] + " Working Correctly")
			else:
				output.append("ERROR: " + test[4:] + " Working Incorrectly")
		except:
			if test[:4] == "fail":
				output.append(test[4:] + " Failed Successfully")
			else:
				output.append("ERROR: " + test[4:] + " Failed Falsely")

	testPrint(output, func.__name__)

def testPrint(input, testname, loud=False):
	errors = 0
	for counter, each in enumerate(input):
		if each[:5] == "ERROR":
			print(each)
			errors += 1

	print("Testing " + testname)
	print("Out of " + str(counter+1) + " tests " + str(errors) + " failed")

parseVcsTimeFormatTest()
diffFromUtcTest()