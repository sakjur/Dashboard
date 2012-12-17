def classList():
	classList = {
		1001: 5248000,
		1002: 5249000,
		1003: 5250000,
		1101: 5580000,
		1102: 5581000,
		1103: 5582000,
		1201: 8325000,
		1202: 8326000,
		1203: 8327000
	}

	return classList

def classID(classchoice):
	# classID(int) takes an integer as argument and finds the associated class in classList()
	# Returns None if classchoice is not in the classList
	# Value is used for TimeEdit-identifiers.
	return classList().get(classchoice, None)