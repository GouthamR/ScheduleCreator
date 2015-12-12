from Course import *

COURSE_NAME = "CourseName"
FILE_NAME = "human.txt"
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

def tupleToFileOutputFormat(tup: tuple) -> str:
	"""
	Converts tuple to string in format for output file.
	"""
	return "".format()

def readCourseFileToTuples() -> 'list of tuple':
	"""
	Reads file for a course and returns list of tuples, with each tuple
	corresponding to each class in file.
	"""
	COLUMN_NAMES = ("CCode", "Typ", "Sec", "Unt", "Instructor", "Time", "Place", "Final", "Max", "Enr", "WL", "Req", "Nor", "Rstr", "Status ")

	tuples = []

	with open(FILE_NAME, 'r') as f:
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
			#f.write(tupleToFileOutputFormat(tup) + '\n')

outputTuplesToFile(readCourseFileToTuples())

'''
TYPE_INDEX = 1

if len(tuples) >= 2:
	connected = tuples[0][TYPE_INDEX] != tuples[1][TYPE_INDEX]
else: # len = 0 or 1
	connected = False

with open(OUT_FILE_NAME, 'w') as f:
	if connected:
		type_1 = tuples[0][TYPE_INDEX]
		type_2 = tuples[1][TYPE_INDEX]
		f.write("{0} {1}_C_{0} {2}\n".format(COURSE_NAME, type_1, type_2))
		for t in tuples:
			print("{}\n".format())
	else:
		f.write("{}\n".format(COURSE_NAME))
	for tup in tuples:
		f.write("{}\n".format(tup))
'''