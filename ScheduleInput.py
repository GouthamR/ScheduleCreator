from Course import *

#Removes newline from end of inputStr if necessary and returns it.
#Does NOT modify inputStr
def removeNewline(inputStr):
    inputStr = inputStr.replace('\xa0', ' ')
    if inputStr.endswith("\n"):
        return inputStr[:-1] #remove newline
    #else:
    return inputStr

#Returns next line, removing newline from end if necessary
def readNextLine(file):
    return removeNewline(file.readline())

def fileInputClasses(file, course):
    currInput = "_flag_"
    while currInput != "":
        currInput = readNextLine(file)
        if(currInput != ""):
            course.addClass(Class(currInput))

CONNECTED_COURSE_INDICATOR = "_C_"

def readStandardCourses(file, courses, currInput):
    courses.append(Course(currInput))
    fileInputClasses(file, courses[-1])

def readConnectedCourses(file, courses, connectedClassDict, firstLine):
    lectureCourse, labCourse = (Course(i) for i in firstLine.split(CONNECTED_COURSE_INDICATOR))

    isLecture = False
    lastType = None
    currLine = "_flag_"
    key = None

    while currLine != "":
        currLine = readNextLine(file)
        if currLine != "":
            currClass = Class(currLine)
            if currClass.type != lastType:
                isLecture = not isLecture
            if isLecture:
                lectureCourse.addClass(currClass)
                key = currClass.code
                connectedClassDict[key] = []
            else:
                labCourse.addClass(currClass)
                connectedClassDict[key].append(currClass)
            lastType = currClass.type
    
    courses.append(lectureCourse)
    courses.append(labCourse)

def fileInputCourses(fileName):
    courses = []
    connectedClassDict = {}
    with open(fileName, 'r') as file:
        currInput = "_flag_"
        while currInput != "":
            currInput = readNextLine(file)
            if(currInput != ""):
                if CONNECTED_COURSE_INDICATOR in currInput:
                    readConnectedCourses(file, courses, connectedClassDict, currInput)
                else:
                    readStandardCourses(file, courses, currInput)
    return courses, connectedClassDict

def fileInputRedZones(fileName):
    redZones = []
    with open(fileName, 'r') as file:
        for line in file:
            redZones.append(ClassTime(removeNewline(line)))
    return redZones

def fileInputMinutesBetween(fileName):
    minutesBetween = None
    with open(fileName, 'r') as file:
        minutesBetween = int(readNextLine(file))
    return minutesBetween
