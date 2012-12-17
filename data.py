def classList():
	classList = {
		1001: 5248000,
		1003: 5250000,
		1101: 5580000,
		1103: 5582000
	}

	return classList

def classID(classchoice):
	# classID(int) takes an integer as argument and returns the value that is associated with that integer.
	# Returns None if classchoice is not in the classList
	# Value is used for TimeEdit-identifiers.
	return classList().get(classchoice, None)