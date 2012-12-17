import datetime, re

now = datetime.datetime.now()

def parseDate(datechoice):
	if datechoice == None:
		return now.date()
	elif len(datechoice) == 6:
		year = int("20" + datechoice[:2])
		month = int(datechoice[2:4])
		day = int(datechoice[4:6])
		return datetime.date(year, month, day)
	elif len(datechoice) == 8:
		year = int(datechoice[:4])
		month = int(datechoice[4:6])
		day = int(datechoice[6:8])
		return datetime.date(year, month, day)
	elif len(datechoice) == 12:
		#TODO - Support for multiple dates
		yearfrom = int("20" + str(datechoice[:2]))
		monthfrom = int(str(datechoice[2:4]))
		dayfrom = int(str(datechoice[4:6]))
		yearto = int("20" + str(datechoice[:2]))
		monthto = int(str(datechoice[2:4]))
		dayto = int(str(datechoice[4:6]))
		return [datetime.date(yearfrom, monthfrom, dayfrom), datetime.date(yearto, monthto, dayto)]
	else:
		return now.date()

def parseVcsTimeFormat(timestring):
	# Incoming time format will look like 20121213T071000Z (which is a UTC time)
	if re.match('[0-9]{8}T[0-9]{6}Z', timestring):
		year 		= int(timestring[:4]) # (2012)
		month		= int(timestring[4:6]) # (12)
		day			= int(timestring[6:8]) # (13)
		hour		= int(timestring[9:11]) # (07)
		minutes		= int(timestring[11:13]) # (10)
		seconds 	= int(timestring[13:15]) #  (00)
		finalDt	= datetime.datetime(year, month, day, hour, minutes, seconds)
		return finalDt
	else:
		return None