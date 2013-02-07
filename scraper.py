import urllib2, re, math, datetime
from event import eventMakeObject
from data import classList, classID
from flask import abort, url_for
from dateparser import teDate, parseDate

def getClassSchedule(classchoice, rawdate):
	classIdentifier = classID(classchoice)

	datechoice = parseDate(rawdate) 

	if classIdentifier == None:
		# Abort operation if no class with name classchoice can be found.
		abort(404)

	url = "http://schema.abbindustrigymnasium.se:8080/" +\
		"4DACTION/iCal_downloadReservations/timeedit.vcs?"
	url += "from=" + teDate(datechoice) + "&"
	url += "to=" + teDate(datechoice) + "&"
	url += "id1=" + classIdentifier
	
	fetchVcsUrl = urllib2.urlopen(url) # Fetch the VCS-file
	urlData = fetchVcsUrl.read() # Get the raw-text VCS
	schedule = cleanVcsFile(urlData)

	return formatVcs(schedule, datechoice)

def formatVcs(schedule, datechoice):
	scheduleFormatted = []
	for each in schedule:
		if re.match("^\n(?:DTSTART)", each): # Only include event-filled rows
			e = eventMakeObject(each, datechoice)
			if e != None:
				scheduleFormatted.append(e)

	return scheduleFormatted


def cleanVcsFile(data):
	# Regular expression that finds everything between "BEGIN:VEVENT" and
	# the "END:VEVENT" keywords
	regex = re.compile("(?:BEGIN\:VEVENT)(.*?)(?:END\:VEVENT)", re.DOTALL)

	# Tidying up the VCS-file
	data = data.replace("\r\n", "\n") # Fuck Windows
	data = data.replace("=\n", "") # srsly Timeedit?
	data = data.replace("=0D=0A", ":")

	# Following: Fixes for Swedish characters
	data = data.replace("=D6", "&Ouml;")
	data = data.replace("=F6", "&ouml;")
	data = data.replace("=E4", "&auml;")
	data = data.replace("=C5", "&Aring;")
	data = data.replace("=E5", "&aring;")
	return regex.split(data)