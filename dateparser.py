import datetime, re

now = datetime.datetime.now()

def parseDate(datechoice):
	if datechoice == None or datechoice == "today":
		return now.date()
	elif datechoice == "tomorrow":
		return now.date() + datetime.timedelta(days=1)
	elif len(datechoice) == 6 and type(datechoice) == int:
		year = int("20" + datechoice[:2])
		month = int(datechoice[2:4])
		day = int(datechoice[4:6])
		return datetime.date(year, month, day)
	elif len(datechoice) == 8 and type(datechoice) == int:
		year = int(datechoice[:4])
		month = int(datechoice[4:6])
		day = int(datechoice[6:8])
		return datetime.date(year, month, day)
	else:
		return now.date()

def isToday(datechoice):
	if parseDate(datechoice) == now.date():
		return True
	else:
		return False

def parseVcsTimeFormat(timestring):
	"""
	Usage: parseVcsTimeFormat(str(timestring)) -> datetime(year, month, day, \
		hour, minutes, seconds)
	Sample Input: str("20121213T071000Z")
	Sample Output: datetime(2012, 12, 13, 07, 10, 00)
	Function: Returns a datetime-object from a VCS-type inputed date-string.
	"""
	if type(timestring) != str:
		raise TypeError("Wrong type on input. Should be string")
		return False
	elif re.match('[0-9]{8}T[0-9]{6}Z', timestring):
		year 		= int(timestring[:4]) # (2012)
		month		= int(timestring[4:6]) # (12)
		day			= int(timestring[6:8]) # (13)
		hour		= int(timestring[9:11]) # (07)
		minutes		= int(timestring[11:13]) # (10)
		seconds 	= int(timestring[13:15]) #  (00)
		finalDt	= datetime.datetime(year, month, day, hour, minutes, seconds)
		return finalDt
	elif re.match('^$', timestring):
		raise ValueError("Empty string.")
		return False
	elif re.match('[0-9]{8}Z[0-9]{6}T', timestring):
		raise ValueError("Swapped place of Z and T" + timestring)
		return False
	else:
		raise Exception("Wrong format. Unknown error.")
		return False

def diffFromUtc(datetimestring):
	if type(datetimestring) != datetime.datetime:
		raise Exception
	else:
		raise Exception

def teDate(datechoice):
	"""
	Usage: teDate(datetime(datechoice)) -> str(rv)
	Function: Parsing dates in the TimeEdit-request form (ie the last two digits
		of the year and the weeknumber)
	Input: Any valid datetime
	Output Range: "0001" - "9953"
	"""

	rv = str(datechoice.year)[2:].zfill(2) 
	rv += str(datechoice.isocalendar()[1]).zfill(2)

	if (int(rv) < 1 or int(rv) > 9953) and len(rv) != 4:
		raise ValueError

	return rv