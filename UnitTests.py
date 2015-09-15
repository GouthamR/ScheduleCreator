from Course import *
from Schedule import *
from ScheduleInput import *

def printUnitTest(testName, *testResults): #testResult = True is success, False is failure
    for i in testResults:
        if i == False:
            print("%s: %s" % (testName, testResults))
            return
    #if not returned before here, all tests pass:
    print("%s: success!" % (testName))

def redZoneUnitTests():
    courses = fileInputCourses("sample_input_3.txt")[0]
    schedule1 = Schedule(courses[0].classes)
    schedule2 = Schedule(courses[1].classes)
    schedules = [schedule1, schedule2]
    redZones = fileInputRedZones("sample_red_zones.txt")
    schedules.sort(key=lambda sched: sched.calculateRedZoneScore(redZones), reverse=True)
    printUnitTest("Red zone unit tests",
                  schedule1.calculateRedZoneScore(redZones) == -6,
                  schedule2.calculateRedZoneScore(redZones) == -4,
                  schedules == [schedule2, schedule1])

def connectedCourseUnitTests():
    courses, connectedClassDict = fileInputCourses("sample_input_2.txt")
    printUnitTest("Connected course input unit tests",
                  [i.code for i in courses[0].classes] == [52111],
                  [i.code for i in courses[1].classes] == [10010, 20010, 30010],
                  [i.code for i in courses[2].classes] == [11111, 11112, 21111, 21112, 21113, 31111],
                  [i.code for i in courses[3].classes] == [42111],
                  [i.code for i in connectedClassDict[10010]] == [11111, 11112],
                  [i.code for i in connectedClassDict[20010]] == [21111, 21112, 21113],
                  [i.code for i in connectedClassDict[30010]] == [31111])
    printUnitTest("Connected course validation unit tests",
                  Schedule([courses[1].classes[0], courses[2].classes[0], courses[0].classes[0]]).hasValidConnections(connectedClassDict) == True,
                  Schedule([courses[1].classes[0], courses[2].classes[2]]).hasValidConnections(connectedClassDict) == False,
                  Schedule([courses[1].classes[2], courses[2].classes[5]]).hasValidConnections(connectedClassDict) == True,
                  Schedule([courses[1].classes[2], courses[2].classes[4]]).hasValidConnections(connectedClassDict) == False)

def generateScheduleUnitTests():
    course2 = Course("TestCourse 2A")
    course2.addClass(Class("21000	test	test	test	test	MWF   3:00- 3:50	testinga	test	test	test	test	test	test	test	test"))
    course2.addClass(Class("22000	test	test	test	test	MWF   4:00- 5:00	testinga	test	test	test	test	test	test	test	test"))
    course3 = Course("TestCourse 3A")
    course3.addClass(Class("31000	test	test	test	test	TuTh   7:00- 8:00	testinga	test	test	test	test	test	test	test	test"))
    course3.addClass(Class("32000	test	test	test	test	MW   7:00- 8:00	testinga	test	test	test	test	test	test	test	test"))
    course4 = Course("TestCourse 4A")
    course4.addClass(Class("41000	test	test	test	test	TuTh   10:00- 11:00	testinga	test	test	test	test	test	test	test	test"))
    course5 = Course("TestCourse 5A")
    course5.addClass(Class("51000	test	test	test	test	TuTh   10:00- 10:50	testinga	test	test	test	test	test	test	test	test"))
    printUnitTest("Generate schedule unit tests", [i.getClassCodes() for i in generatePossibleSchedules([course2], {})] == [[21000], [22000]],
                  [i.getClassCodes() for i in generatePossibleSchedules([course2, course4], {})] == [[21000, 41000], [22000, 41000]],
                  [i.getClassCodes() for i in generatePossibleSchedules([course2, course3], {})] == [[21000, 31000], [21000, 32000], [22000, 31000], [22000, 32000]],
                  len(generatePossibleSchedules([course4, course5], {})) == 0)

def classTimeAMPMUnitTests():
    raw1 = "10:00- 11:59a"
    raw2 = "10:00- 12:59p"
    raw3 = "12:01- 12:59p"
    raw4 = "12:01- 1:00p"
    raw5 = "1:00- 10:00p"
    raw6 = "10:00- 11:59p"
    raw7 = "10:00- 12:01"
    raw8 = "10:00- 1:01"

    exceptionTestsPass = True
    try:
        ClassTime(raw7)
        exceptionTestsPass = False
    except RuntimeError:
        pass
    try:
        ClassTime(raw8)
        exceptionTestsPass = False
    except RuntimeError:
        pass

    printUnitTest("ClassTime ampm tests",
                  str(ClassTime(raw1)) == "ClassTime: Time: 10:0, Time: 11:59",
                  str(ClassTime(raw2)) == "ClassTime: Time: 10:0, Time: 12:59",
                  str(ClassTime(raw3)) == "ClassTime: Time: 12:1, Time: 12:59",
                  str(ClassTime(raw4)) == "ClassTime: Time: 12:1, Time: 13:0",
                  str(ClassTime(raw5)) == "ClassTime: Time: 13:0, Time: 22:0",
                  str(ClassTime(raw6)) == "ClassTime: Time: 22:0, Time: 23:59",
                  exceptionTestsPass)

def runUnitTestsFileInputTests():
    file1Name = "sample_run_unit_tests_1.txt"
    file2Name = "sample_run_unit_tests_2.txt"
    file3Name = "sample_run_unit_tests_3.txt"

    exceptionTestsPass = True
    try:
        fileInputRunUnitTests(file3Name)
        exceptionTestsPass = False
    except RuntimeError:
        pass

    printUnitTest("Run unit tests file input tests",
                  fileInputRunUnitTests(file1Name) == True,
                  fileInputRunUnitTests(file2Name) == False,
                  exceptionTestsPass)

def unitTests():
    classRawStr = "44215	Lec	A	4	STAFF	MWF   8:00- 8:50	DBH 1100	Sat, Dec 5, 1:30-3:30pm	221	34	0	51	111	A and N	Bookstore	 	OPEN"
    classRawStr2 = "44225	Dis	11	0	STAFF	TuTh   3:00- 3:50p	HICF 100M	 	45	2	0	1	23	 	Bookstore	 	OPEN"
    printUnitTest("Class parse test", str(Class(classRawStr)) == "Class: Days: [0, 2, 4], ClassTime: Time: 8:0, Time: 8:50",
                                      str(Class(classRawStr2)) == "Class: Days: [1, 3], ClassTime: Time: 15:0, Time: 15:50")
    printUnitTest("Class code test", Class(classRawStr).code == 44215)
    printUnitTest("Time hour construction tests", Time("11:00").hour == 11, Time("12:00p").hour == 12, Time("3:00p").hour == 15, Time("12:00").hour == 0)
    time1 = Time("8:00")
    time2 = Time("9:00")
    time3 = Time("9:00p")
    time4 = Time("10:00p")
    printUnitTest("Time comparison tests", time1 < time2, time1 < time3, time2 < time3, time3 < time4,
                  time1 <= time1, time1 >= time1, time2 <= time3, time4 >= time3,
                  time1 == time1)
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
    printUnitTest("ClassTime isWithin test",
                  ClassTime("8:00- 8:50").isWithin(ClassTime("7:50- 9:00")),
                  not ClassTime("8:00- 8:50").isWithin(ClassTime("8:10- 8:40")),
                  not ClassTime("8:00- 8:50").isWithin(ClassTime("7:50- 8:40")),
                  not ClassTime("8:00- 8:50").isWithin(ClassTime("8:10- 9:00")))
    course1 = Course("TestCourse 1A")
    course1.addClass(Class(classRawStr))
    course1.addClass(Class(classRawStr2))
    printUnitTest("Course unit test", str(course1) == "TestCourse 1A: [Class: Days: [0, 2, 4], ClassTime: Time: 8:0, Time: 8:50, Class: Days: [1, 3], ClassTime: Time: 15:0, Time: 15:50]")
    printUnitTest("Schedule class code unit test", Schedule([Class(classRawStr), Class(classRawStr2)]).getClassCodes() == [44215, 44225])
    generateScheduleUnitTests()
    connectedCourseUnitTests()
    redZoneUnitTests()
    classTimeAMPMUnitTests()
    runUnitTestsFileInputTests()
    print("End unit tests.")
