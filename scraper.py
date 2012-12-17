import urllib2, re, math, datetime
from event import eventMakeObject
from data import classList, classID
from flask import abort, url_for

def getClassSchedule(classchoice, parsedDate):

	# Find associated classIdentifier using the classchoice the function has been invoked with.
	classIdentifier = classID(classchoice)

	if type(parsedDate) == list:
		datechoice = parsedDate[0]
	else:
		datechoice = parsedDate 

	if classIdentifier == None:
		# Abort operation if no class with name classchoice can be found.
		abort(404)
	
	fromDate = str(datechoice.year)[2:] + str(datechoice.isocalendar()[1])
	toDate = str(datechoice.year)[2:] + str(datechoice.isocalendar()[1])

	schedule = cleanVcsFile("http://schema.abbindustrigymnasium.se:8080/" +
		"4DACTION/iCal_downloadReservations/timeedit.vcs" +
		"?from=" + fromDate + "&to=" + toDate + "&id1=" + str(classIdentifier))

	scheduleFormatted = []
	for each in schedule:
		if re.match("^\n(?:DTSTART)", each): # Only include event-filled rows
			e = eventMakeObject(each, datechoice)
			if e != None:
				scheduleFormatted.append(e)

	return scheduleFormatted


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