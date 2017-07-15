from urllib import parse, request
import pathlib
from term import Term
from courseinputinfo import CourseInputInfo

def _getWebsiteData(term: 'constant from Term', year: int, courseInputInfo: CourseInputInfo) -> str:
	"""
	Returns a string of website's data for the classes specified by arguments.
	"""
	URL = "https://www.reg.uci.edu/perl/WebSoc"
	YEAR_TERM_FORMAT = "{}-{}"
	term_param = YEAR_TERM_FORMAT.format(year, term)
	params_dict = { "Breadth":"ANY",
				"CancelledCourses":"Exclude",
				"ClassType":"ALL",
				"CourseNum":courseInputInfo.courseName,
				"CourseCodes":courseInputInfo.courseCodes,
				"Dept":courseInputInfo.dept,
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

def _writeCourseWebDataToFile(term: 'constant from Term', year: int, courseInputInfo: CourseInputInfo,
								courseFile: pathlib.Path) -> None:
	"""
	Writes website data for the classes specified by arguments to courseFile.
	"""
	with courseFile.open('w') as f:
		f.write(_getWebsiteData(term, year, courseInputInfo))

def _getFileName(courseName: str) -> str:
	"""
	Returns file name corresponding to courseName.
	File name is the lowercased course name without spaces, with a .txt extension.
	"""
	return courseName.lower().replace(" ", "") + ".txt"

class WebsiteInput:
	_COURSEFILENAMES_FILE_NAME = "coursefilenames.txt"
	def __init__(self, courseFilesDir: pathlib.Path):
		"""
		inputFile: file specifying which courses to scrape.
		courseFilesDir: directory to store the website input config files.
		"""
		if not courseFilesDir.is_dir():
			raise ValueError("courseFilesDir is not a directory")

		self._courseFilesDir = courseFilesDir
		self._courseFilenamesFile = self._courseFilesDir.joinpath(WebsiteInput._COURSEFILENAMES_FILE_NAME)
	def savedFilesExist(self) -> bool:
		"""
		Returns True if previously-saved course files exist.
		"""
		return self._courseFilenamesFile.exists()
	def getSavedCourseFiles(self) -> [pathlib.Path]:
		"""
		Returns the filenames of files containing course data.
		"""
		if not self.savedFilesExist():
			raise ValueError("No saved course files")

		with self._courseFilenamesFile.open('r') as f:
			return [self._courseFilesDir.joinpath(line.strip()) for line in f]

	def scrapeCoursesDataFromWebsiteAndSaveToFiles(self, term: 'constant from Term', year: int,
													courseInputInfos: [CourseInputInfo]) -> None:
		"""
		Scrapes website data for the courses specified by the arguments.
		Then saves the data for each course to course files directory.
		Assumes all courses in same term and year.
		"""
		with self._courseFilenamesFile.open('w') as f:
			for courseInputInfo in courseInputInfos:
				courseFile = self._courseFilesDir.joinpath(_getFileName(courseInputInfo.courseName))
				_writeCourseWebDataToFile(term, year, courseInputInfo, courseFile)
				f.write(courseFile.name + '\n')

def _main():
	websiteInput = WebsiteInput(pathlib.Path("coursefiles/"))
	print(websiteInput.savedFilesExist())
	print(websiteInput.getSavedCourseFiles())
	websiteInput.scrapeCoursesDataFromWebsiteAndSaveToFiles(Term.FALL, 2017, [CourseInputInfo('COMPSCI', 'COMPSCI 161', '')])

if __name__ == '__main__':
	_main()