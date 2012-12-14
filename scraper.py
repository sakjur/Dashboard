import urllib2
import re
import math
import datetime
from flask import abort, url_for

now = datetime.datetime.now()

def classList():
	classList = {
		1001: 5248000,
		1003: 5250000,
		1101: 5580000,
		1103: 5582000
	}

	return classList 

def getClassSchedule(classchoice, datechoice):

	if datechoice == None:
		# Currently non-functional
		datechoice = now.date()
	elif len(datechoice) == 6:
		year = int("20" + datechoice[:2])
		month = int(datechoice[2:4])
		day = int(datechoice[4:6])
		datechoice = datetime.datetime(year, month, day)
	elif len(datechoice) == 8:
		year = int(datechoice[:4])
		month = int(datechoice[4:6])
		day = int(datechoice[6:8])
		datechoice = datetime.datetime(year, month, day)
	elif len(datechoice) == 12:
		#TODO
		yearfrom = int("20" + str(datechoice[:2]))
		monthfrom = int(str(datechoice[2:4]))
		dayfrom = int(str(datechoice[4:6]))
		yearto = int("20" + str(datechoice[:2]))
		monthto = int(str(datechoice[2:4]))
		dayto = int(str(datechoice[4:6]))
		datechoice = [datetime.datetime(yearfrom, monthfrom, dayfrom), datetime.datetime(yearto, monthto, dayto)]
	else:
		datechoice = now.date()

	# Find associated classIdentifier using the classchoice the function has been invoked with.
	classIdentifier = classID(classchoice)

	if classIdentifier == None:
		# Abort operation if no class with name classchoice can be found.
		abort(404)
	
	schedule = cleanVcsFile("http://schema.abbindustrigymnasium.se:8080/" +
		"4DACTION/iCal_downloadReservations/timeedit.vcs?from=1250&to=1250&id1=" + str(classIdentifier))

	scheduleFormatted = []
	for each in schedule:
		if re.match("^\n(?:DTSTART)", each): # Only include event-filled rows
			event = eventMakeObject(each, datechoice)
			if event != None:
				scheduleFormatted.append(event)

	return scheduleFormatted

def classID(classchoice):
	# classID(int) takes an integer as argument and returns the value that is associated with that integer.
	# Returns None if classchoice is not in the classList
	# Value is used for TimeEdit-identifiers.
	return classList().get(classchoice, None)

def eventMakeObject(event, datechoice):
	event = event.split("\n")
	objArray = []
	eventDict = {}
	for each in event:
		if re.match("(?:DTSTART)(.*?)", each): # Find start time
			dtstart 	= each.replace("DTSTART:", "") # Remove non-relevant info
			startTime 	= parseVcsTimeFormat(dtstart) # Parse the "VCS time format" to datetime
			eventDict['startTime'] 	= startTime
		elif re.match("(?:DTEND)(.*?)", each): # Find end time
			dtend 		= each.replace("DTEND:", "") # Remove non-relevant info
			endTime		= parseVcsTimeFormat(dtend) # Parse the "VCS time format" to datetime
			eventDict['endTime']	= endTime
		elif re.match("(?:SUMMARY)(.*?)", each): # Find the SUMMARY-property
			summary = each.split(":") # Split SUMMARY on each comma
			classProperty = summary[1] # Second part of the summary is the class-property
			classProperty = classProperty.replace(" ", "") # Remove spaces
			classProperty = classProperty.split(",") # Split on comma
			classInsert = []
			for each in classProperty:
				if int(each) in classList():
					classURL = '<a href="' + url_for("class_choice", classchoice=int(each)) + '">' + each + '</a>'
					classInsert.append(classURL)
				else:
					classInsert.append(each)
			eventDict['class']		= ", ".join(classInsert)
			eventDict['teacher']	= summary[2] # Third part of the summary is the teacher-property
			eventDict['subject']	= summary[3] # Fourth part of the summary is the subject-property
			if len(summary) > 4:
				eventDict['subjectID']	= summary[4]
			else:
				eventDict['subjectID']	= None
			if len(summary) > 5:
				eventDict['comment']	= summary[5]
			else:
				eventDict['comment']	= None
		elif re.match("(?:LOCATION)(.*?)", each): # Find the LOCATION-property
			eventDict['location']	= each.replace("LOCATION;ENCODING=QUOTED-PRINTABLE:", "") # Remove non-relevant info
	if eventDict['startTime'].date() == datechoice:
		return eventDict
	else:
		return None

def parseVcsTimeFormat(timestring):
	# Incoming time format will look like 20121213T071000Z (which is a UTC time)
	year 		= int(timestring[:4]) # (2012)
	month		= int(timestring[4:6]) # (12)
	day			= int(timestring[6:8]) # (13)
	hour		= int(timestring[9:11]) # (07)
	minutes		= int(timestring[11:13]) # (10)
	seconds 	= int(timestring[13:15]) #  (00)
	finalDt	= datetime.datetime(year, month, day, hour, minutes, seconds)
	return finalDt

def cleanVcsFile(url):
	fetchVcsUrl = urllib2.urlopen(url) # Fetch the VCS-file
	urlRaw = fetchVcsUrl.read() # Get the raw-text VCS

	# Regular expression that finds everything between "BEGIN:VEVENT" and
	# the "END:VEVENT" keywords
	regex = re.compile("(?:BEGIN\:VEVENT)(.*?)(?:END\:VEVENT)", re.DOTALL)

	# Tidying up the VCS-file
	urlRaw = urlRaw.replace("\r\n", "\n") # Fuck Windows
	urlRaw = urlRaw.replace("=\n", "") # srsly Timeedit?
	urlRaw = urlRaw.replace("=0D=0A", ":")

	# Following: Fixes for Swedish characters
	urlRaw = urlRaw.replace("=D6", "&Ouml;")
	urlRaw = urlRaw.replace("=F6", "&ouml;")
	urlRaw = urlRaw.replace("=E4", "&auml;")
	urlRaw = urlRaw.replace("=C5", "&Aring;")
	urlRaw = urlRaw.replace("=E5", "&aring;")
	return regex.split(urlRaw)