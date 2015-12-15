from Course import *

# Note: sub-course is all the classes of a single type within a course. E.g. sub-course of ICS31 is ICS31 Lec.

COLUMN_NAMES = ("CCode", "Typ", "Sec", "Unt", "Instructor", "Time", "Place", "Final", "Max", "Enr", "WL", "Req", "Nor", "Rstr", "Status ")

IN_FILE_NAME = "input.txt"
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

def _getClassTuple(line: str, column_indices: 'list of (tuple of int)') -> 'tuple of str':
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
				tuples.append(_getClassTuple(line, curr_column_indices))
	return tuples

def _isConnected(splitClasses: 'list of list of Class') -> bool:
	"""
	Returns if course represented by argument is a connected course.
	If not valid connected course with two-sub-courses, raises ValueError.
	"""
	numSubCourses = len(splitClasses)
	if numSubCourses < 2 or len(splitClasses[0]) != 1 or numSubCourses % 2 != 0:
		return False
	# else, number of sub-courses is even and at least 2, and first sub-course has one class.
	# Now, check for valid sub-course connection:
	firstType = splitClasses[0][0].type
	for i in range(2, len(splitClasses), 2):
		currSubCourse = splitClasses[i]
		if len(currSubCourse) != 1 or currSubCourse[0].type != firstType:
			raise ValueError("Invalid connected courses.")
	# if here, no exception raised:
	return True

def _isConnectedAssertions():
	lecType = "LEC"
	labType = "LAB"
	lecTup = ("28100", lecType, "HA",  "4",   "STAFF", "MWF   9:00- 9:50",  "BS3 1200", "Wed, Mar 16, 8:00-10:00am", "64", "53", "n/a", "57", "0","", "OPEN")
	labTup = ("28100", labType, "HA",  "4",   "STAFF", "MWF   9:00- 9:50",  "BS3 1200", "Wed, Mar 16, 8:00-10:00am", "64", "53", "n/a", "57", "0","", "OPEN")
	lec = Class(lecType, lecTup)
	lab = Class(labType, labTup)
	assert not _isConnected( [] )
	assert not _isConnected( [ [lec] ] )
	assert _isConnected( [[lec], [lab]] )
	assert not _isConnected( [[lec, lec]] )
	assert not _isConnected( [[lec], [lab], [lec]] )
	assert not _isConnected( [[lec, lec], [lab], [lec]] )
_isConnectedAssertions()

def _convertToClassesByType(courseName: str, tuples: 'list of tuple') -> 'list of list of Class':
	"""
	Converts argument list of class-tuples into multiple lists of Class, where
	each list is made up of the classes of one type in sequence.
	E.g. For [lec, lec, lab, lec], returns [[lec, lec], [lab], [lec]].
	"""
	classes = []
	prevType = None
	for tup in tuples:
		currClass = Class(courseName, tup)
		currType = currClass.type
		if currType != prevType:
			classes.append([currClass])
			prevType = currType
		else:
			classes[-1].append(currClass)
	return classes
def _convertToClassesByTypeAssertions():
	lecType = "LEC"
	labType = "LAB"
	lecTup = ("28100", lecType, "HA",  "4",   "STAFF", "MWF   9:00- 9:50",  "BS3 1200", "Wed, Mar 16, 8:00-10:00am", "64", "53", "n/a", "57", "0","", "OPEN")
	labTup = ("28100", labType, "HA",  "4",   "STAFF", "MWF   9:00- 9:50",  "BS3 1200", "Wed, Mar 16, 8:00-10:00am", "64", "53", "n/a", "57", "0","", "OPEN")
	NAME = "Human"

	def convertToTypeList(classes: 'list of list of Class') -> 'list of list of str':
		result = []
		for i in classes:
			newL = []
			for j in i:
				newL.append(j.type)
			result.append(newL)
		return result

	assert convertToTypeList(_convertToClassesByType(NAME, [])) == []
	assert convertToTypeList(_convertToClassesByType(NAME, [lecTup])) == [[lecType]]
	assert convertToTypeList(_convertToClassesByType(NAME, [lecTup, lecTup])) == [[lecType, lecType]]
	assert convertToTypeList(_convertToClassesByType(NAME, [lecTup, labTup])) == [[lecType], [labType]]
	assert convertToTypeList(_convertToClassesByType(NAME, [lecTup, lecTup, labTup, labTup])) == [[lecType, lecType], [labType, labType]]
	assert convertToTypeList(_convertToClassesByType(NAME, [lecTup, labTup, lecTup, labTup])) == [[lecType], [labType], [lecType], [labType]]
_convertToClassesByTypeAssertions()

def _convertConnectedSplitClassesToCourseData(splitClasses: 'list of list of Class',
												courseName: str) -> ('list of Course', 'dict of (courseNum:list of Class)'):
	"""
	For connected course data split classes, returns sub-course objects and
	dict of connected class data.
	Assumes only two sub-courses for connected courses.
	"""
	course1Classes = []
	course2Classes = []
	connectedClassDict = {}
	for i in range(0, len(splitClasses), 2):
		currCourse1Class = splitClasses[i][0]
		course1Classes.append(currCourse1Class)
		key = currCourse1Class.code
		connectedClassDict[key] = []
		for currCourse2Class in splitClasses[i + 1]:
			course2Classes.append(currCourse2Class)
			connectedClassDict[key].append(currCourse2Class)
	course1 = Course(courseName, course1Classes)
	course2 = Course(courseName, course2Classes)
	return [course1, course2], connectedClassDict

def readCourseFileToCourseData(fileName: str, courseName: str) -> ('list of Course', 'dict of (courseNum:list of Class) OR None'):
	"""
	Reads course data from file.
	If course is connected, returns sub-courses and dict of connected class data.
	If course is not connected, returns sub-courses and None.
	Assumes only two sub-courses for connected courses.
	"""
	tuples = readCourseFileToTuples(fileName)
	splitClasses = _convertToClassesByType(courseName, tuples)
	if _isConnected(splitClasses):
		return _convertConnectedSplitClassesToCourseData(splitClasses, courseName)
	else:
		subCourses = [Course(courseName, subCourseClasses) for subCourseClasses in splitClasses]
		return subCourses, None

def readCourseFilesToCourseData(fileNames: 'list of str', courseNames: 'list of str') -> ('list of Course', 'dict of (courseNum:list of Class) OR None'):
	"""
	Reads course data from multiple course files.
	Returns sub-courses and dict of connected class data.
	If no connected courses, returns sub-courses and None.
	courseNames must correspond to fileNames.
	Assumes only two sub-courses for connected courses.
	"""
	subCourses = []
	connectedClassDict = None
	for i in range(len(fileNames)):
		currSubCourses, currDict = readCourseFileToCourseData(fileNames[i], courseNames[i])
		subCourses.extend(currSubCourses)
		if currDict != None:
			if connectedClassDict == None:
				connectedClassDict = {}
			connectedClassDict.update(currDict)
	return subCourses, connectedClassDict

def outputCourseDataToFile(subCourses, connectedDict):
	with open(OUT_FILE_NAME, 'w') as f:
		for c in subCourses:
			f.write("{}\n".format(c))
		f.write('\n')
		if connectedDict == None:
			f.write("Not connected.")
		else:
			for key in connectedDict:
				f.write("{}:\n".format(key))
				for currClass in connectedDict[key]:
					f.write("\t{}\n".format(currClass))
				f.write('\n')

def fileInputCourses(inFile: str) -> ('list of Course', 'dict of (courseNum:list of Class) OR None'):
	"""
	Reads course data from multiple course files as specified in inFile.
	Returns sub-courses and dict of connected class data.
	If no connected courses, returns sub-courses and None.
	"""
	fileNames = []
	with open(inFile, 'r') as f:
		for line in f:
			fileNames.append(line.strip())
	courseNames = [fName.replace(".txt", "") for fName in fileNames]
	return readCourseFilesToCourseData(fileNames, courseNames)

def main():
	print(fileInputCourses(IN_FILE_NAME))
	outputCourseDataToFile(*fileInputCourses(IN_FILE_NAME))

if __name__ == '__main__':
	main()