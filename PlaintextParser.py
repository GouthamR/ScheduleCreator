from Course import *

TYPE_INDEX = 1
COLUMN_NAMES = ("CCode", "Typ", "Sec", "Unt", "Instructor", "Time", "Place", "Final", "Max", "Enr", "WL", "Req", "Nor", "Rstr", "Status ")

FILE_NAME = "ics32.txt"
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

def outputTuplesToFile(tuples: 'list of tuple', courseName: str) -> None:
	"""
	Outputs argument to file.
	"""
	# with open(OUT_FILE_NAME, 'w') as f:
	# 	if _isConnected(tuples):
	# 		f.write("{0} {1}_C_{0} {2}\n".format(courseName, _getType1Name(tuples), _getType2Name(tuples)))
	# 		for tup in tuples:
	# 			f.write(str(tup) + '\n')
	# 	else:
	# 		for subCourse in _splitClassTuplesByType(tuples):
	# 			f.write("{0} {1}\n".format(courseName, _getType1Name(subCourse)))
	# 			for tup in subCourse:
	# 				f.write(str(tup) + '\n')
	with open(OUT_FILE_NAME, 'w') as f:
		if _isConnected(tuples):
			f.write("Connected:\n")
			f.write("{}\n\n".format(Course(courseName, tuples)))
		else:
			f.write("Not Connected:\n")
			for subCourse in _splitClassTuplesByType(tuples):
				f.write("{}\n".format(Course("{0} {1}".format(courseName, _getType1Name(subCourse).title()), subCourse)))
			f.write("\n")

outputTuplesToFile(readCourseFileToTuples(FILE_NAME), COURSE_NAME)