import pathlib
from Term import Term

def _getTerm(term_str: str) -> 'constant from Term':
	"""
	For argument string from file input, returns corresponding Term constant.
	Assumes argument has already been stripped of leading and trailing whitespace.
	If invalid term_str, raises ValueError.
	"""
	term_str_processed = term_str.lower()
	if term_str_processed == 'fall':
		return Term.FALL
	elif term_str_processed == 'winter':
		return Term.WINTER
	elif term_str_processed == 'spring':
		return Term.SPRING
	else:
		raise ValueError("Invalid term string.")

def _getDept(course_str: str) -> str:
	"""
	For argument course string from file input, returns department of course.
	If invalid department or department not found in argument, raises ValueError.
	"""
	splitCourseStr = course_str.split('\n')
	firstElement = splitCourseStr[0].strip() # Note: guaranteed to be at least one element, so no need to check number of elements.
	if firstElement == "":
		raise ValueError("Invalid course string.")
	else:
		return firstElement

def _getCourseName(course_str: str) -> str:
	"""
	For argument course string from file input, returns course name.
	Assumes department is found in argument.
	If invalid course name or course name not found in argument, raises ValueError.
	"""
	splitCourseStr = course_str.split('\n')
	if len(splitCourseStr) < 2 or splitCourseStr[1].strip() == '':
		raise ValueError("Invalid course string.")
	else:
		return splitCourseStr[1].strip()

def _getCourseCodes(course_str: str) -> str:
	"""
	For argument course string from file input, returns course codes if any.
	Assumes department and course name are found in argument.
	If too many course fields in argument, raises ValueError.
	"""
	splitCourseStr = course_str.split('\n')
	numElements = len(splitCourseStr)
	if numElements > 3:
		raise ValueError("Invalid course string.")
	elif numElements == 3:
		return splitCourseStr[-1].strip()
	else: # has 2 elements, assuming numElements >= 2
		return ""

def parseCoursesParamsFromConfigFile(configFile: pathlib.Path) -> ('term = constant from Term', 'year = int', 'depts = list of str',
																	'courseNames = list of str', 'courseCodes = list of str'):
	"""
	Parses and returns course parameters from configFile.

	Assumes configFile is in the following format; courseCodes are optional:
	term
	year

	dept
	courseName
	courseCodes

	dept2
	courseName2
	courseCodes2

	...etc...
	"""
	with configFile.open('r') as f:
		term_str = f.readline().strip()
		year_str = f.readline().strip()
		f.readline() # skip blank line
		course_strs = f.read().split('\n\n')
	term = _getTerm(term_str)
	year = int(year_str)
	depts = []
	courseNames = []
	coursesCodes = []
	for course_str in course_strs:
		depts.append(_getDept(course_str))
		courseNames.append(_getCourseName(course_str))
		coursesCodes.append(_getCourseCodes(course_str))
	return term, year, depts, courseNames, coursesCodes