import datetime

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