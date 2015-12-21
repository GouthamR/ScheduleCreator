from urllib import parse, request

class Term:
	FALL = "92"
	WINTER = "03"
	SPRING = "14"

term = Term.WINTER
year = 2016
dept_str = "I&C SCI"
course_num_str = "ICS 32"
course_codes = ""

YEAR_TERM_FORMAT = "{}-{}"
term_param = YEAR_TERM_FORMAT.format(year, term)

URL = "https://www.reg.uci.edu/perl/WebSoc"
PARAMS = { "Breadth":"ANY",
			"CancelledCourses":"Exclude",
			"ClassType":"ALL",
			"CourseNum":course_num_str,
			"CourseCodes":course_codes,
			"Dept":dept_str,
			"Division":"ANY",
			"FontSize":"200",
			"FullCourses":"ANY",
			"ShowComments":"off",
			"ShowFinals":"off",
			"Submit":"Display Text Results",
			"YearTerm": term_param}

headers = { }
params = parse.urlencode(PARAMS)
req = request.Request(URL, params.encode('ascii'), headers)
response = request.urlopen(req)
print(response.status, response.reason)
data = response.read().decode(response.headers.get_content_charset())

with open('output.txt', 'w') as f:
	f.write(data)