from urllib import parse, request

class Term:
	FALL   = "92"
	WINTER = "03"
	SPRING = "14"

def getWebsiteData(term: 'constant from Term', year: int, dept: str, courseName: str, courseCodes: str) -> str:
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

def writeCourseWebDataToFile(term: 'constant from Term', year: int, dept: str,
								courseName: str, courseCodes: str, fileName: str) -> None:
	"""
	Writes website data for the classes specified by arguments to a file with fileName.
	"""
	with open(fileName, 'w') as f:
		f.write(getWebsiteData(term, year, dept, courseName, courseCodes))

def _getFileName(courseName: str) -> str:
	"""
	Returns file name corresponding to courseName.
	File name is the lowercased course name without spaces, with a .txt extension.
	"""
	return courseName.lower().replace(" ", "") + ".txt"

def writeCoursesWebDataToFiles(term: 'constant from Term', year: int, depts: 'list of str',
								courseNames: 'list of str', courseCodes: 'list of str') -> None:
	"""
	Writes website data for the courses specified by arguments to files corresponding to course names.
	The files will be text files with the name corresponding to the lowercased course name without spaces.
	All list arguments should have same length and have corresponding elements.
	Assumes all courses in same term and year.
	"""
	fileNames = [_getFileName(name) for name in courseNames]
	for i in range(len(depts)):
		writeCourseWebDataToFile(term, year, depts[i], courseNames[i], courseCodes[i], fileNames[i])

def _getTerm(term_str: str) -> 'constant from Term':
	"""
	For argument string from file input, returns corresponding Term constant.
	If invalid term_str, raises ValueError.
	"""
	term_str_processed = term_str.strip().lower()
	if term_str_processed == 'fall':
		return Term.FALL
	elif term_str_processed == 'winter':
		return Term.WINTER
	elif term_str_processed == 'spring':
		return Term.SPRING
	else:
		raise ValueError("Invalid term string.")

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

def main():
	term = Term.WINTER
	year = 2016
	depts = ["I&C SCI", "HUMAN", "I&C SCI"]
	courseNames = ["ICS 32", "HUMAN 1B", "ICS 6B"]
	courseCodes = ["36600-36623", "28100-28126", ""]
	writeCoursesWebDataToFiles(term, year, depts, courseNames, courseCodes)
	getCoursesParamsFromFile("web_input.txt")

if __name__ == '__main__':
	main()