from Course import *
from ScheduleInput import *

IN_FILE_NAME = "input.txt"
OUT_FILE_NAME = "plaintext_parser_output.txt"

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

def main():
	print(fileInputCourses(IN_FILE_NAME))
	outputCourseDataToFile(*fileInputCourses(IN_FILE_NAME))

if __name__ == '__main__':
	main()