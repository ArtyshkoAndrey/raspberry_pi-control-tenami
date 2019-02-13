from jsondb.db import Database

def save(db, Smart, System):

	if not Smart.paused:
		dictToReturn = "on"
	else:
		dictToReturn = "off"

	response = {
		'system': dictToReturn,
		'times': System.times,
		'timer': System.Tens.TimeSleep
	}

	db['system'] = response
	print(response)