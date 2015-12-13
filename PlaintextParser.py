from Course import *

FILE_NAME = "ics6b.txt"
COURSE_NAME = FILE_NAME.replace(".txt", "")
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
					new_class.append(line[column_indices[i][0]:column_indices[i][1]].strip())
				new_class.append(line[column_indices[-1][0]:].strip())
				tuples.append(tuple(new_class))

	return tuples

TYPE_INDEX = 1

def isConnected(class_tuples: 'list of tuple') -> bool:
	"""
	Returns if course represented by argument is a connected course.
	"""
	if len(class_tuples) < 2:
		return False
	#else:
	return class_tuples[0][TYPE_INDEX] != class_tuples[1][TYPE_INDEX]
def _isConnectedAssertions():
	lec = ('', 'LEC ', '', '', '', '', '', '', '', '', '', '', '', '', '')
	lab = ('', 'LAB ', '', '', '', '', '', '', '', '', '', '', '', '', '')
	assert not isConnected( () )
	assert not isConnected( (lec, ) )
	assert isConnected( (lec, lab) )
	assert not isConnected( (lec, lec) )
	assert isConnected( (lec, lab, lec) )
	assert not isConnected( (lec, lec, lab, lec) )
_isConnectedAssertions()

def getType1Name(tuples: 'list of tuple') -> str:
	"""
	Returns name of type of first class in course.
	"""
	return tuples[0][TYPE_INDEX]
def getType2Name(tuples: 'list of tuple') -> str:
	"""
	Returns name of second type for connected course.
	Assumes course is connected.
	"""
	type1 = getType1Name(tuples)
	for tup in tuples:
		currType = tup[TYPE_INDEX]
		if currType != type1:
			return currType

def getSubCourses(tuples: 'list of tuple') -> 'list of list of tuple':
	"""
	Splits argument course into multiple sub-courses, where each sub-course
	is made up of the classes of one type.
	"""
	subCourses = []
	prevType = None
	for tup in tuples:
		currType = tup[TYPE_INDEX]
		if currType != prevType:
			subCourses.append([tup])
			prevType = currType
		else:
			subCourses[-1].append(tup)
	return subCourses
def _getSubCoursesAssertions():
	lec = ('', 'LEC ', '', '', '', '', '', '', '', '', '', '', '', '', '')
	lab = ('', 'LAB ', '', '', '', '', '', '', '', '', '', '', '', '', '')
	assert getSubCourses([]) == []
	assert getSubCourses([lec]) == [[lec]]
	assert getSubCourses([lec, lec]) == [[lec, lec]]
	assert getSubCourses([lec, lab]) == [[lec], [lab]]
	assert getSubCourses([lec, lec, lab, lab]) == [[lec, lec], [lab, lab]]
	assert getSubCourses([lec, lab, lec, lab]) == [[lec], [lab], [lec], [lab]]
_getSubCoursesAssertions()

def outputTuplesToFile(tuples: 'list of tuple', courseName) -> None:
	"""
	Outputs argument to file.
	"""
	with open(OUT_FILE_NAME, 'w') as f:
		if isConnected(tuples):
			f.write("{0} {1}_C_{0} {2}\n".format(courseName, getType1Name(tuples), getType2Name(tuples)))
			for tup in tuples:
				f.write(str(tup) + '\n')
		else:
			for subCourse in getSubCourses(tuples):
				f.write("{0} {1}\n".format(courseName, getType1Name(subCourse)))
				for tup in subCourse:
					f.write(str(tup) + '\n')

outputTuplesToFile(readCourseFileToTuples(FILE_NAME), COURSE_NAME)