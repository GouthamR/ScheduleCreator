from Course import *

# Note: sub-course is all the classes of a single type within a course. E.g. sub-course of ICS31 is ICS31 Lec.

TYPE_INDEX = 1
COLUMN_NAMES = ("CCode", "Typ", "Sec", "Unt", "Instructor", "Time", "Place", "Final", "Max", "Enr", "WL", "Req", "Nor", "Rstr", "Status ")

FILE_NAME = "human.txt"
COURSE_NAME = FILE_NAME.replace(".txt", "")
OUT_FILE_NAME = "output.txt"

def _isInt(input: str) -> int:
	""" Checks if input str contains an integer. """
	try:
		int(input)
		return True
	except Exception:
		return False
assert _isInt('534')
assert _isInt('-534')
assert _isInt('0')
assert _isInt('-0')
assert not _isInt('a0')
assert not _isInt('0a')
assert not _isInt('asdf')

def _isTableHeader(line: str) -> bool:
	"""
	Returns True if line is in format of course table header, with column
	names (as in COLUMN_NAMES).
	"""
	return line.strip().startswith(COLUMN_NAMES[0])

def _isClassFormat(line: str) -> bool:
	"""
	Returns True if line is in format of class fields.
	"""
	return _isInt(line.strip()[0:5])

def _getColumnIndices(line: str) -> 'list of (tuple of int)':
	"""
	Returns list representing position of each column, from COLUMN_NAMES, in line.
	Each element is a tuple of form (start index, end index), except for
	last element which is of form (start index, None).
	"""
	column_indices = []
	for i in range(len(COLUMN_NAMES) - 1):
		column_indices.append( (line.index(COLUMN_NAMES[i]), line.index(COLUMN_NAMES[i+1])) )
	column_indices.append( (line.index(COLUMN_NAMES[-1]), None) )
	return column_indices

def _getClass(line: str, column_indices: 'list of (tuple of int)') -> 'tuple of str':
	"""
	Returns tuple of class fields corresponding to input line,
	using table format based on column_indices.
	"""
	new_class = []
	for i in range(len(column_indices) - 1):
		new_class.append(line[column_indices[i][0]:column_indices[i][1]].strip())
	new_class.append(line[column_indices[-1][0]:].strip())
	return tuple(new_class)

def readCourseFileToTuples(fileName: str) -> 'list of (tuple of str)':
	"""
	Reads file for a course and returns list of tuples, with each tuple
	corresponding to each class in file.
	"""
	tuples = []
	curr_column_indices = None
	with open(fileName, 'r') as f:
		for line in f:
			if _isTableHeader(line):
				curr_column_indices = _getColumnIndices(line)
			elif _isClassFormat(line):
				tuples.append(_getClass(line, curr_column_indices))
	return tuples

def _isConnected(class_tuples: 'list of tuple') -> bool:
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
	assert not _isConnected( [] )
	assert not _isConnected( [ lec ] )
	assert _isConnected( [lec, lab] )
	assert not _isConnected( [lec, lec] )
	assert _isConnected( [lec, lab, lec] )
	assert not _isConnected( [lec, lec, lab, lec] )
_isConnectedAssertions()

def _getType1Name(tuples: 'list of tuple') -> str:
	"""
	Returns name of type of first class in course.
	"""
	return tuples[0][TYPE_INDEX]

def _getType2Name(tuples: 'list of tuple') -> str:
	"""
	Returns name of second type for connected course.
	Assumes course is connected.
	"""
	type1 = _getType1Name(tuples)
	for tup in tuples:
		currType = tup[TYPE_INDEX]
		if currType != type1:
			return currType

def _splitClassTuplesByType(tuples: 'list of tuple') -> 'list of list of tuple':
	"""
	Splits argument list of class-tuples into multiple lists, where each
	list is made up of the classes of one type in sequence.
	Returns as list of lists.
	E.g. For [lec, lec, lab, lec], returns [[lec, lec], [lab], [lec]].
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
def _splitClassTuplesByTypeAssertions():
	lec = ('', 'LEC ', '', '', '', '', '', '', '', '', '', '', '', '', '')
	lab = ('', 'LAB ', '', '', '', '', '', '', '', '', '', '', '', '', '')
	assert _splitClassTuplesByType([]) == []
	assert _splitClassTuplesByType([lec]) == [[lec]]
	assert _splitClassTuplesByType([lec, lec]) == [[lec, lec]]
	assert _splitClassTuplesByType([lec, lab]) == [[lec], [lab]]
	assert _splitClassTuplesByType([lec, lec, lab, lab]) == [[lec, lec], [lab, lab]]
	assert _splitClassTuplesByType([lec, lab, lec, lab]) == [[lec], [lab], [lec], [lab]]
_splitClassTuplesByTypeAssertions()

def readCourseFileToCourseData(fileName: str, courseName: str) -> ('list of Course', 'dict of (courseNum:list of Class) OR None'):
	"""
	Reads course data from file.
	If course is connected, returns sub-courses and dict of connected class data.
	If course is not connected, returns sub-courses and None.
	Assumes only two sub-courses for connected courses.
	"""
	tuples = readCourseFileToTuples(fileName)
	splitTuples = _splitClassTuplesByType(tuples)
	if _isConnected(tuples):
		course1Classes = []
		course2Classes = []
		connectedClassDict = {}
		course1Name = "{} {}".format(courseName, _getType1Name(tuples).title())
		course2Name = "{} {}".format(courseName, _getType2Name(tuples).title())
		for i in range(0, len(splitTuples), 2):
			currCourse1Class = Class(course1Name, splitTuples[i][0])
			course1Classes.append(currCourse1Class)
			key = currCourse1Class.code
			connectedClassDict[key] = []
			for currCourse2ClassTuple in splitTuples[i + 1]:
				currCourse2Class = Class(course2Name, currCourse2ClassTuple)
				course2Classes.append(currCourse2Class)
				connectedClassDict[key].append(currCourse2Class)
		course1 = Course(course1Name, course1Classes)
		course2 = Course(course2Name, course2Classes)
		return [course1, course2], connectedClassDict
	else:
		subCourses = []
		for subCourseTuples in _splitClassTuplesByType(tuples):
			currCourse = Course("{} {}".format(courseName, _getType1Name(subCourseTuples).title()), subCourseTuples)
			subCourses.append(currCourse)
		return subCourses, None

def outputCourseDataToFile(subCourses, connectedDict):
	with open(OUT_FILE_NAME, 'w') as f:
		for c in subCourses:
			f.write("{}\n".format(c))
		f.write('\n')
		if connectedDict == None:
			f.write("Not connected.")
		else:
			for key in connectedDict:
				f.write("{}:\n ".format(key))
				for currClass in connectedDict[key]:
					f.write("\t{}\n".format(currClass))
				f.write('\n')

outputCourseDataToFile(*readCourseFileToCourseData(FILE_NAME, COURSE_NAME))