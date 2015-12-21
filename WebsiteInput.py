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

def writeWebsiteDataToFile(term: 'constant from Term', year: int, dept: str, courseName: str, courseCodes: str, fileName: str) -> None:
	"""
	Writes website data for the classes specified by arguments to a file with fileName.
	"""
	with open(fileName, 'w') as f:
		f.write(getWebsiteData(term, year, dept, courseName, courseCodes))

term = Term.WINTER
year = 2016
dept = "I&C SCI"
courseName = "ICS 32"
courseCodes = ""
fileName = "out.txt"
writeWebsiteDataToFile(term, year, dept, courseName, courseCodes, fileName)