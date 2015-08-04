##Goutham Rajeev
##Started 7/29/15
##ScheduleCreator
##Generates schedules.

class Time:
    def __init__(self, rawData):
        rawHour, rawMinute = rawData.split(":")
        self.hour = int(rawHour)
        if(rawMinute.endswith("p")):
            self.hour += 12
        self.minute = int(rawMinute[:2]) #cuts off p if necessary
    def __str__(self):
        return "Time: %s:%s" % (self.hour, self.minute)
    def __eq__(self, other):
        return self.hour == other.hour and self.minute == other.minute
    def __le__(self, other):
        return (self == other #same hour and same minute
            or ((self.hour == other.hour) and (self.minute < other.minute)) #same hour, different minute
            or self.hour < other.hour) #(different hour and same minute) OR (different hour and different minute)
    def __ge__(self, other):
        return ((self == other) or (not (self <= other)))
    def isPM(self):
        return self.hour > 12

class Days:
    def __init__(self, rawData):
        self.days = []
        daysDict = { 'M': 0, 't': 1, 'W': 2, 'T' : 3, 'F': 4} #move outside function for performance
        for c in rawData.replace(" ", "").replace("Th","T").replace("Tu","t"): #Removes spaces, then converts Tuesday and Thursday to one character strings, to correspond with above dict
            self.days.append(daysDict[c])
    def __str__(self):
        return "Days: %s" % (self.days)

class ClassTime:
    def __init__(self, rawData):
        timeStrList = rawData.replace(" ", "").split("-") #remove spaces, then split
        self.end = Time(timeStrList[1])
        if self.end.isPM():
            timeStrList[0] += "p" #if the end time is pm, odds are high that the start time is pm.
        self.start = Time(timeStrList[0])
    def __str__(self):
        return "ClassTime: %s, %s" % (self.start, self.end)
    def overlapsWith(self, otherTime):
        return ((self.start >= otherTime.start and self.start <= otherTime.end) or #self begins during other
                (self.end >= otherTime.start and self.end <= otherTime.end) or #self ends during other
                (self.start <= otherTime.start and self.end >= otherTime.end)) #self begins before other and ends after other. i.e. encompassing other
                #other encompassing self is included in first two cases above

class Class:
    DATA_TIMINGS_INDEX = 5
    def __init__(self, rawData):
        self.rawData = rawData
        rawSplit = rawData.split("\t")
        timingsList = rawSplit[Class.DATA_TIMINGS_INDEX].split("   ")
        self.days = Days(timingsList[0])
        self.classTime = ClassTime(timingsList[1])
    def __str__(self):
        return "Class: %s, %s" % (self.days, self.classTime)

class Course:
    def __init__(self, name):
        self.name = name
        self.classes = []
    def addClass(self, newClass):
        self.classes.append(newClass)
    def __str__(self):
        return "%s: [%s]" % (self.name, ", ".join(map(str, self.classes)))

def printUnitTest(testName, *testResults): #testResult = True is success, False is failure
    print("%s: %s" % (testName, testResults))

def unitTests():
    classRawStr = "44215	Lec	A	4	STAFF	MWF   8:00- 8:50	DBH 1100	Sat, Dec 5, 1:30-3:30pm	221	34	0	51	111	A and N	Bookstore	 	OPEN"
    classRawStr2 = "44225	Dis	11	0	STAFF	TuTh   3:00- 3:50p	HICF 100M	 	45	2	0	1	23	 	Bookstore	 	OPEN"
    printUnitTest("Class parse test", str(Class(classRawStr)) == "Class: Days: [0, 2, 4], ClassTime: Time: 8:0, Time: 8:50",
                                      str(Class(classRawStr2)) == "Class: Days: [1, 3], ClassTime: Time: 15:0, Time: 15:50")
    time1 = Time("8:00")
    time2 = Time("9:00")
    time3 = Time("9:00p")
    time4 = Time("10:00p")
    printUnitTest("Time comparison tests", time1 <= time2, time1 <= time3, time2 <= time3, time3 <= time4)
    classTimeRawStr1 = "8:00- 8:50" #overlaps with self
    classTimeRawStr2 = "8:30- 9:00" #overlaps with end of 1
    classTimeRawStr3 = "7:30- 8:30" #overlaps with beginning of 1
    classTimeRawStr4 = "7:30- 7:50" #does not overlap with 1 - before beginning
    classTimeRawStr5 = "9:00- 9:30" #does not overlap with 1 - after end
    printUnitTest("ClassTime overlap tests", ClassTime(classTimeRawStr1).overlapsWith(ClassTime(classTimeRawStr1)),
                  ClassTime(classTimeRawStr1).overlapsWith(ClassTime(classTimeRawStr2)),
                  ClassTime(classTimeRawStr1).overlapsWith(ClassTime(classTimeRawStr3)),
                  not ClassTime(classTimeRawStr1).overlapsWith(ClassTime(classTimeRawStr4)),
                  not ClassTime(classTimeRawStr1).overlapsWith(ClassTime(classTimeRawStr5)))
    course1 = Course("TestCourse 1A")
    course1.addClass(Class(classRawStr))
    course1.addClass(Class(classRawStr2))
    printUnitTest("Course unit test", str(course1) == "TestCourse 1A: [Class: Days: [0, 2, 4], ClassTime: Time: 8:0, Time: 8:50, Class: Days: [1, 3], ClassTime: Time: 15:0, Time: 15:50]")
    print("End unit tests.")

def inputClasses(course):
    print ("Type in classes. Press enter when finished.")
    currInput = "_flag_"
    while currInput != "":
        currInput = input("Class -> ")
        if(currInput != ""):
            course.addClass(Class(currInput))

def main():
    courses = []
    print ("Type in names of courses. Press enter when finished.")
    currInput = "_flag_"
    while currInput != "":
        currInput = input("Course -> ")
        if(currInput != ""):
            courses.append(Course())
            inputClasses(courses[0])
    print ("%s" % "\n".join(map(str, courses)))

unitTests()
#main()
