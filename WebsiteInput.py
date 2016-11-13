from urllib import parse, request
import os.path

_COURSENAMES_SAVEFILE_NAME = "config/coursefilenames.txt"

class Term:
	FALL   = "92"
	WINTER = "03"
	SPRING = "14"

def _getWebsiteData(term: 'constant from Term', year: int, dept: str, courseName: str, courseCodes: str) -> str:
	"""
	Returns a string of website's data for the classes specified by arguments.
	"""
	URL = "https://www.reg.uci.edu/perl/WebSoc"
	YEAR_TERM_FORMAT = "{}-{}"
	term_param = YEAR_TERM_FORMAT.format(year, term)
	params_dict = { "Breadth":"ANY",
				"CancelledCourses":"Exclude",
				"ClassType":"ALL",
				"CourseNum":courseName,
				"CourseCodes":courseCodes,
				"Dept":dept,
				"Division":"ANY",
				"FontSize":"200",
				"FullCourses":"ANY",
				"ShowComments":"off",
				"ShowFinals":"off",
				"Submit":"Display Text Results",
				"YearTerm": term_param}
	headers = { }
	params = parse.urlencode(params_dict)
	req = request.Request(URL, params.encode('ascii'), headers)
	response = request.urlopen(req)
	print(response.status, response.reason)
	data = response.read().decode(response.headers.get_content_charset())
	return data

def _writeCourseWebDataToFile(term: 'constant from Term', year: int, dept: str,
								courseName: str, courseCodes: str, fileName: str) -> None:
	"""
	Writes website data for the classes specified by arguments to a file with fileName.
	"""
	with open(fileName, 'w') as f:
		f.write(_getWebsiteData(term, year, dept, courseName, courseCodes))

def _getFileName(courseName: str) -> str:
	"""
	Returns file name corresponding to courseName.
	File name is the lowercased course name without spaces, with a .txt extension.
	"""
	return 'config/' + courseName.lower().replace(" ", "") + ".txt"

def writeCoursesWebDataToFiles(term: 'constant from Term', year: int, depts: 'list of str',
								courseNames: 'list of str', courseCodes: 'list of str') -> None:
	"""
	Writes website data for the courses specified by arguments to files corresponding to course names.
	Also writes course file names to save file specified by _COURSENAMES_SAVEFILE_NAME.
	The course files will be text files with the name corresponding to the lowercased course name without spaces.
	All list arguments should have same length and have corresponding elements.
	Assumes all courses in same term and year.
	"""
	fileNames = [_getFileName(name) for name in courseNames]
	for i in range(len(depts)):
		_writeCourseWebDataToFile(term, year, depts[i], courseNames[i], courseCodes[i], fileNames[i])
	with open(_COURSENAMES_SAVEFILE_NAME, 'w') as f:
		for name in fileNames:
			f.write(name + '\n')

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

def getCoursesParamsFromFile(fileName: str) -> ('term = constant from Term', 'year = int', 'depts = list of str',
													'courseNames = list of str', 'courseCodes = list of str'):
	"""
	Parses argument file for and then returns course parameters.

	Assumes argument file is in the following format:
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
	with open(fileName, 'r') as f:
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

def readSavedCourseFileNames() -> "list of str":
	"""
	Reads and returns course file names from save file, _COURSENAMES_SAVEFILE_NAME.
	"""
	with open(_COURSENAMES_SAVEFILE_NAME, 'r') as f:
		return [line.strip() for line in f]

def savedCourseFileExists() -> bool:
	"""
	Returns True if course names save file, _COURSENAMES_SAVEFILE_NAME, exists.
	"""
	return os.path.isfile(_COURSENAMES_SAVEFILE_NAME)

def main():
	print(savedCourseFileExists())
	writeCoursesWebDataToFiles(*getCoursesParamsFromFile("config/web_input.txt"))
	print(readSavedCourseFileNames())

if __name__ == '__main__':
	main()