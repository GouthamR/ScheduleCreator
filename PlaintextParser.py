from Course import *

COURSE_NAME = "CourseName"
FILE_NAME = "ics32.txt"
OUT_FILE_NAME = "output.txt"

def isInt(input: str) -> int:
	""" Checks if input str contains an integer. """
	try:
		int(input)
		return True
	except Exception:
		return False
assert isInt('534')
assert isInt('-534')
assert isInt('0')
assert isInt('-0')
assert not isInt('a0')
assert not isInt('0a')
assert not isInt('asdf')

def readCourseFileToTuples(fileName: str) -> 'list of tuple':
	"""
	Reads file for a course and returns list of tuples, with each tuple
	corresponding to each class in file.
	"""
	COLUMN_NAMES = ("CCode", "Typ", "Sec", "Unt", "Instructor", "Time", "Place", "Final", "Max", "Enr", "WL", "Req", "Nor", "Rstr", "Status ")

	tuples = []

	with open(fileName, 'r') as f:
		for line in f:
			if line.strip().startswith("CCode"):
				column_indices = []
				for i in range(len(COLUMN_NAMES) - 1):
					column_indices.append( (line.index(COLUMN_NAMES[i]), line.index(COLUMN_NAMES[i+1])) )
				column_indices.append( (line.index(COLUMN_NAMES[-1]), None) )
				column_indices = tuple(column_indices)
			elif isInt(line.strip()[0:5]):
				new_class = []
				for i in range(len(column_indices) - 1):
					new_class.append(line[column_indices[i][0]:column_indices[i][1]])
				new_class.append(line[column_indices[-1][0]:])
				tuples.append(tuple(new_class))

	return tuples

def outputTuplesToFile(tuples: 'list of tuple') -> None:
	"""
	Outputs argument to file.
	"""
	with open(OUT_FILE_NAME, 'w') as f:
		for tup in tuples:
			f.write(str(tup) + '\n')
			f.write(str(Class(tup)) + '\n')

outputTuplesToFile(readCourseFileToTuples(FILE_NAME))