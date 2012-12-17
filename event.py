import re
import dateparser
from data import classList
from flask import abort, url_for

def eventMakeObject(event, datechoice):
	event = event.split("\n")
	objArray = []
	eventDict = {}
	for each in event:
		if re.match("(?:DTSTART)(.*?)", each): # Find start time
			dtstart 	= each.replace("DTSTART:", "") # Remove non-relevant info
			startTime 	= dateparser.parseVcsTimeFormat(dtstart) # Parse to datetime
			eventDict['startTime'] 	= startTime
		elif re.match("(?:DTEND)(.*?)", each): # Find end time
			dtend 		= each.replace("DTEND:", "") # Remove non-relevant info
			endTime		= dateparser.parseVcsTimeFormat(dtend) # Parse to datetime
			eventDict['endTime']	= endTime
		elif re.match("(?:SUMMARY)(.*?)", each): # Find the SUMMARY-property
			summary = each.split(":") # Split SUMMARY on each comma
			classProperty = summary[1] # Second part of the summary is the class-property
			classProperty = classProperty.replace(" ", "") # Remove spaces
			classProperty = classProperty.split(",") # Split on comma
			classInsert = []
			for each in classProperty:
				if int(each) in classList():
					classURL = '<a href="' + url_for("class_choice", classchoice=int(each)) + '">' +
					 each + '</a>'
					classInsert.append(classURL)
				else:
					classInsert.append(each)
			eventDict['class']		= ", ".join(classInsert)
			eventDict['teacher']	= summary[2] # 
			eventDict['subject']	= summary[3] # 
			if len(summary) > 4:
				eventDict['subjectID']	= summary[4]
			else:
				eventDict['subjectID']	= None
			if len(summary) > 5:
				eventDict['comment']	= summary[5]
			else:
				eventDict['comment']	= None
		elif re.match("(?:LOCATION)(.*?)", each): # Find the LOCATION-property
			eventDict['location']	= each.replace("LOCATION;ENCODING=QUOTED-PRINTABLE:", "")
	if eventDict['startTime'].date() == datechoice:
		return eventDict
	else:
		return None