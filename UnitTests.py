import unittest
from Course import *
from CourseDataParser import *
from Schedule import *
from ScheduleInput import *
from ScheduleInput import _isInt, _isConnected, _convertToClassesByType
from WebsiteInput import *
from WebsiteInput import _getFileName, Term, _getTerm, _getDept, _getCourseName, _getCourseCodes, _parseCoursesParamsFromConfigFile
class ClassTests(unittest.TestCase):

    def setUp(self):
        self._classRawTuple1 = ("36610", "LAB", "1", "0", "STAFF", "MWF   8:00- 9:50", "ICS 189", "", "44", "10/15", "n/a", "9", "0","A&N", "OPEN")

    def test_class_name(self):
        """
        Class should correctly store name argument.
        """
        name = "ClassName"
        class1 = ClassDataParser.toClass(name, self._classRawTuple1)
        self.assertEqual(class1.name, name)

    def test_class_parse(self):
        """
        ClassDataParser should correctly parse tuples.
        """
        class1 = ClassDataParser.toClass("", self._classRawTuple1)
        self.assertEqual(class1.code, 36610)
        self.assertEqual(class1.days.days, [0, 2, 4])
        self.assertEqual(class1.classTime.start, TimeDataParser.toTime("8:00"))
        self.assertEqual(class1.classTime.end, TimeDataParser.toTime("9:50"))
        self.assertEqual(class1.type, "LAB")

class TimeTests(unittest.TestCase):

    def test_time_hour_parse(self):
        """
        TimeDataParser should correctly interpret hour from input.
        """
        self.assertEqual(TimeDataParser.toTime("11:00").hour, 11)
        self.assertEqual(TimeDataParser.toTime("12:00p").hour, 12)
        self.assertEqual(TimeDataParser.toTime("3:00p").hour, 15)
        self.assertEqual(TimeDataParser.toTime("12:00").hour, 0)

    def test_time_comparison(self):
        """
        Time should correctly compare with other Times.
        """
        time1 = Time(8, 0)
        time2 = Time(9, 0)
        time3 = Time(21, 0)
        time4 = Time(22, 0)
        self.assertTrue(time1 < time2)
        self.assertTrue(time1 < time3)
        self.assertTrue(time2 < time3)
        self.assertTrue(time3 < time4)
        self.assertTrue(time1 <= time1)
        self.assertTrue(time1 >= time1)
        self.assertTrue(time2 <= time3)
        self.assertTrue(time4 >= time3)
        self.assertTrue(time1 == time1)
        self.assertFalse(time2 == time3)

class ClassTimeTests(unittest.TestCase):

    def test_overlap(self):
        """
        ClassTime should correctly check overlap with other ClassTimes.
        """
        classTimeRawStr1 = "8:00- 8:50" #overlaps with self
        classTimeRawStr2 = "8:30- 9:00" #overlaps with end of 1
        classTimeRawStr3 = "7:30- 8:30" #overlaps with beginning of 1
        classTimeRawStr4 = "7:30- 7:50" #does not overlap with 1 - before beginning
        classTimeRawStr5 = "9:00- 9:30" #does not overlap with 1 - after end
        self.assertTrue(ClassTimeDataParser.toClassTime(classTimeRawStr1).overlapsWith(ClassTimeDataParser.toClassTime(classTimeRawStr1)))
        self.assertTrue(ClassTimeDataParser.toClassTime(classTimeRawStr1).overlapsWith(ClassTimeDataParser.toClassTime(classTimeRawStr2)))
        self.assertTrue(ClassTimeDataParser.toClassTime(classTimeRawStr1).overlapsWith(ClassTimeDataParser.toClassTime(classTimeRawStr3)))
        self.assertFalse(ClassTimeDataParser.toClassTime(classTimeRawStr1).overlapsWith(ClassTimeDataParser.toClassTime(classTimeRawStr4)))
        self.assertFalse(ClassTimeDataParser.toClassTime(classTimeRawStr1).overlapsWith(ClassTimeDataParser.toClassTime(classTimeRawStr5)))

    def test_isWithin(self):
        """
        ClassTime should correctly check isWithin with other ClassTimes.
        """
        self.assertTrue(ClassTimeDataParser.toClassTime("8:00- 8:50").isWithin(ClassTimeDataParser.toClassTime("7:50- 9:00")))
        self.assertFalse(ClassTimeDataParser.toClassTime("8:00- 8:50").isWithin(ClassTimeDataParser.toClassTime("8:10- 8:40")))
        self.assertFalse(ClassTimeDataParser.toClassTime("8:00- 8:50").isWithin(ClassTimeDataParser.toClassTime("7:50- 8:40")))
        self.assertFalse(ClassTimeDataParser.toClassTime("8:00- 8:50").isWithin(ClassTimeDataParser.toClassTime("8:10- 9:00")))

    def test_ampm_construction(self):
        """
        ClassTimeDataParser should correctly infer am/pm from constructor argument,
        or raise RuntimeError if invalid argument.
        """
        # Remember that 12:00p is noon, not midnight
        raw1 = "10:00- 11:59a"
        raw2 = "10:00- 12:59p"
        raw3 = "12:01- 12:59p"
        raw4 = "12:01- 1:00p"
        raw5 = "1:00- 10:00p"
        raw6 = "10:00- 11:59p"
        raw7 = "10:00- 12:01"
        raw8 = "10:00- 1:01"

        self.assertEqual(ClassTimeDataParser.toClassTime(raw1).start, TimeDataParser.toTime("10:00"))
        self.assertEqual(ClassTimeDataParser.toClassTime(raw1).end, TimeDataParser.toTime("11:59"))
        self.assertEqual(ClassTimeDataParser.toClassTime(raw2).start, TimeDataParser.toTime("10:00"))
        self.assertEqual(ClassTimeDataParser.toClassTime(raw2).end, TimeDataParser.toTime("12:59p"))
        self.assertEqual(ClassTimeDataParser.toClassTime(raw3).start, TimeDataParser.toTime("12:01p"))
        self.assertEqual(ClassTimeDataParser.toClassTime(raw3).end, TimeDataParser.toTime("12:59p"))
        self.assertEqual(ClassTimeDataParser.toClassTime(raw4).start, TimeDataParser.toTime("12:01p"))
        self.assertEqual(ClassTimeDataParser.toClassTime(raw4).end, TimeDataParser.toTime("1:00p"))
        self.assertEqual(ClassTimeDataParser.toClassTime(raw5).start, TimeDataParser.toTime("1:00p"))
        self.assertEqual(ClassTimeDataParser.toClassTime(raw5).end, TimeDataParser.toTime("10:00p"))
        self.assertEqual(ClassTimeDataParser.toClassTime(raw6).start, TimeDataParser.toTime("10:00p"))
        self.assertEqual(ClassTimeDataParser.toClassTime(raw6).end, TimeDataParser.toTime("11:59p"))
        self.assertRaises(RuntimeError, ClassTimeDataParser.toClassTime, raw7)
        self.assertRaises(RuntimeError, ClassTimeDataParser.toClassTime, raw8)

class CourseTests(unittest.TestCase):

    NAME = "CourseName"

    def test_course_name(self):
        """
        Course should correctly store name argument.
        """
        c1 = Course(self.NAME, [])
        self.assertEqual(c1.name, self.NAME)

    def test_course_classes(self):
        """
        Course should correctly store classes argument.
        """
        classRawTuple1 = ("10000", "LEC", "1", "0", "STAFF", "MWF   8:00- 9:50", "ICS 189", "", "44", "10/15", "n/a", "9", "0","A&N", "OPEN")
        classRawTuple2 = ("20000", "LEC", "2", "0", "STAFF", "MWF   1:00- 2:50p", "ICS 180", "", "44", "10/15", "n/a", "9", "0","A&N", "OPEN")
        classes = [ClassDataParser.toClass(self.NAME, classRawTuple1), ClassDataParser.toClass(self.NAME, classRawTuple2)]
        c1 = Course(self.NAME, classes)
        self.assertEqual(c1.classes, classes)

class ScheduleTests(unittest.TestCase):

    def test_getClassCodes(self):
        """
        Schedule should return correct class codes.
        """
        classRawTuple1 = ("10000", "LEC", "1", "0", "STAFF", "MWF   8:00- 9:50", "ICS 189", "", "44", "10/15", "n/a", "9", "0","A&N", "OPEN")
        classRawTuple2 = ("20000", "LEC", "2", "0", "STAFF", "MWF   1:00- 2:50p", "ICS 180", "", "44", "10/15", "n/a", "9", "0","A&N", "OPEN")
        sched = Schedule([ClassDataParser.toClass("", classRawTuple1), ClassDataParser.toClass("", classRawTuple2)])
        self.assertEqual(sched.getClassCodes(), [10000, 20000])

    def test_generatePossibleSchedules(self):
        """
        generatePossibleSchedules should return correct values.
        """

        class_2_1 = ClassDataParser.toClass("", ("21000", "LEC", "1", "0", "STAFF", "MWF   3:00- 3:50", "ICS 189", "", "44", "10/15", "n/a", "9", "0","A&N", "OPEN"))
        class_2_2 = ClassDataParser.toClass("", ("22000", "LEC", "1", "0", "STAFF", "MWF   4:00- 5:00", "ICS 189", "", "44", "10/15", "n/a", "9", "0","A&N", "OPEN"))
        course2 = Course("", [class_2_1, class_2_2])
        class_3_1 = ClassDataParser.toClass("", ("31000", "LEC", "1", "0", "STAFF", "TuTh   7:00- 8:00", "ICS 189", "", "44", "10/15", "n/a", "9", "0","A&N", "OPEN"))
        class_3_2 = ClassDataParser.toClass("", ("32000", "LEC", "1", "0", "STAFF", "MW   7:00- 8:00", "ICS 189", "", "44", "10/15", "n/a", "9", "0","A&N", "OPEN"))
        course3 = Course("", [class_3_1, class_3_2])
        class_4_1 = ClassDataParser.toClass("", ("41000", "LEC", "1", "0", "STAFF", "TuTh   10:00- 11:00", "ICS 189", "", "44", "10/15", "n/a", "9", "0","A&N", "OPEN"))
        course4 = Course("", [class_4_1])
        class_5_1 = ClassDataParser.toClass("", ("51000", "LEC", "1", "0", "STAFF", "TuTh   10:00- 10:50", "ICS 189", "", "44", "10/15", "n/a", "9", "0","A&N", "OPEN"))
        course5 = Course("", [class_5_1])

        scheds_1 = generatePossibleSchedules([course2], {})
        scheds_2 = generatePossibleSchedules([course2, course4], {})
        scheds_3 = generatePossibleSchedules([course2, course3], {})
        scheds_4 = generatePossibleSchedules([course4, course5], {})

        self.assertEqual([s.classes for s in scheds_1], [(class_2_1, ), (class_2_2, )])
        self.assertEqual([s.classes for s in scheds_2], [(class_2_1, class_4_1), (class_2_2, class_4_1)])
        self.assertEqual([s.classes for s in scheds_3], [(class_2_1, class_3_1), (class_2_1, class_3_2), (class_2_2, class_3_1), (class_2_2, class_3_2)])
        self.assertEqual([s.classes for s in scheds_4], [])

    def test_hasValidConnections(self):
        """
        hasValidConnections should return correct value.
        """
        c1_class1 = ClassDataParser.toClass("", ("52111", "LEC", "1", "0", "STAFF", "MWF   3:00- 3:50", "ICS 189", "", "44", "10/15", "n/a", "9", "0","A&N", "OPEN"))
        c2_class1 = ClassDataParser.toClass("", ("10010", "LEC", "1", "0", "STAFF", "MWF   3:00- 3:50", "ICS 189", "", "44", "10/15", "n/a", "9", "0","A&N", "OPEN"))
        c2_class2 = ClassDataParser.toClass("", ("20010", "LEC", "1", "0", "STAFF", "MWF   3:00- 3:50", "ICS 189", "", "44", "10/15", "n/a", "9", "0","A&N", "OPEN"))
        c2_class3 = ClassDataParser.toClass("", ("30010", "LEC", "1", "0", "STAFF", "MWF   3:00- 3:50", "ICS 189", "", "44", "10/15", "n/a", "9", "0","A&N", "OPEN"))
        c3_class1 = ClassDataParser.toClass("", ("11111", "LAB", "1", "0", "STAFF", "MWF   3:00- 3:50", "ICS 189", "", "44", "10/15", "n/a", "9", "0","A&N", "OPEN"))
        c3_class2 = ClassDataParser.toClass("", ("11112", "LAB", "1", "0", "STAFF", "MWF   3:00- 3:50", "ICS 189", "", "44", "10/15", "n/a", "9", "0","A&N", "OPEN"))
        c3_class3 = ClassDataParser.toClass("", ("21111", "LAB", "1", "0", "STAFF", "MWF   3:00- 3:50", "ICS 189", "", "44", "10/15", "n/a", "9", "0","A&N", "OPEN"))
        c3_class4 = ClassDataParser.toClass("", ("21112", "LAB", "1", "0", "STAFF", "MWF   3:00- 3:50", "ICS 189", "", "44", "10/15", "n/a", "9", "0","A&N", "OPEN"))
        c3_class5 = ClassDataParser.toClass("", ("21113", "LAB", "1", "0", "STAFF", "MWF   3:00- 3:50", "ICS 189", "", "44", "10/15", "n/a", "9", "0","A&N", "OPEN"))
        c3_class6 = ClassDataParser.toClass("", ("31111", "LAB", "1", "0", "STAFF", "MWF   3:00- 3:50", "ICS 189", "", "44", "10/15", "n/a", "9", "0","A&N", "OPEN"))
        c4_class1 = ClassDataParser.toClass("", ("42111", "LAB", "1", "0", "STAFF", "MWF   3:00- 3:50", "ICS 189", "", "44", "10/15", "n/a", "9", "0","A&N", "OPEN"))
        connectedClassDict = { 10010:[c3_class1, c3_class2], 20010:[c3_class3, c3_class4, c3_class5], 30010:[c3_class6] }

        self.assertTrue(Schedule([c2_class1, c3_class1, c1_class1]).hasValidConnections(connectedClassDict))
        self.assertFalse(Schedule([c2_class1, c3_class3]).hasValidConnections(connectedClassDict))
        self.assertTrue(Schedule([c2_class3, c3_class6]).hasValidConnections(connectedClassDict))
        self.assertFalse(Schedule([c2_class3, c3_class5]).hasValidConnections(connectedClassDict))
        self.assertTrue(Schedule([c1_class1, c4_class1]).hasValidConnections(connectedClassDict))
        self.assertTrue(Schedule([c3_class1, c3_class5]).hasValidConnections(connectedClassDict)) # True because connection is one-way, lec to lab

    def test_calculateRedZoneScore(self):
        """
        calculateRedZoneScore should return correct value.
        """
        c1_1 = ClassDataParser.toClass("", ("52111", "RedIn", "1", "0", "STAFF", "TuTh   6:10- 7:00", "ICS 189", "", "44", "10/15", "n/a", "9", "0","A&N", "OPEN"))
        c1_2 = ClassDataParser.toClass("", ("10010", "OK", "1", "0", "STAFF", "MWF   9:10- 10:00", "ICS 189", "", "44", "10/15", "n/a", "9", "0","A&N", "OPEN"))
        c1_3 = ClassDataParser.toClass("", ("11112", "RedIn", "1", "0", "STAFF", "MWF   3:10- 4:00p", "ICS 189", "", "44", "10/15", "n/a", "9", "0","A&N", "OPEN"))
        c1_4 = ClassDataParser.toClass("", ("20010", "RedOv", "1", "0", "STAFF", "MWF   4:10- 5:10p", "ICS 189", "", "44", "10/15", "n/a", "9", "0","A&N", "OPEN"))
        c1_5 = ClassDataParser.toClass("", ("42111", "RedOv", "1", "0", "STAFF", "TuTh   9:10- 10:30p", "ICS 189", "", "44", "10/15", "n/a", "9", "0","A&N", "OPEN"))
        c2_1 = ClassDataParser.toClass("", ("52111", "OK", "1", "0", "STAFF", "TuTh   10:10- 11:00", "ICS 189", "", "44", "10/15", "n/a", "9", "0","A&N", "OPEN"))
        c2_2 = ClassDataParser.toClass("", ("10010", "OK", "1", "0", "STAFF", "MWF   9:10- 10:00", "ICS 189", "", "44", "10/15", "n/a", "9", "0","A&N", "OPEN"))
        c2_3 = ClassDataParser.toClass("", ("11112", "RedIn", "1", "0", "STAFF", "MWF   3:10- 4:00p", "ICS 189", "", "44", "10/15", "n/a", "9", "0","A&N", "OPEN"))
        c2_4 = ClassDataParser.toClass("", ("20010", "RedOv", "1", "0", "STAFF", "MWF   4:10- 5:10p", "ICS 189", "", "44", "10/15", "n/a", "9", "0","A&N", "OPEN"))
        c2_5 = ClassDataParser.toClass("", ("42111", "RedOv", "1", "0", "STAFF", "TuTh   9:10- 10:30p", "ICS 189", "", "44", "10/15", "n/a", "9", "0","A&N", "OPEN"))
        schedule1 = Schedule([c1_1, c1_2, c1_3, c1_4, c1_5])
        schedule2 = Schedule([c2_1, c2_2, c2_3, c2_4, c2_5])
        schedules = [schedule1, schedule2]
        redZones = [ClassTimeDataParser.toClassTime("1:00- 9:00"), ClassTimeDataParser.toClassTime("3:00- 5:00p"), ClassTimeDataParser.toClassTime("10:00- 11:00p")]

        self.assertEqual(schedule1.calculateRedZoneScore(redZones), -6)
        self.assertEqual(schedule2.calculateRedZoneScore(redZones), -4)

class FileInputTests(unittest.TestCase):

    def test_connected_course_input(self):
        """
        Connected courses should be read in properly by readCourseFileToCourseData.
        """
        courses, connectedClassDict = readCourseFileToCourseData("unit_test_files/unit_test_input_2.txt", "")

        self.assertEqual(len(courses), 2)
        self.assertEqual([i.code for i in courses[0].classes], [10010, 20010, 30010])
        self.assertEqual([i.code for i in courses[1].classes], [11111, 11112, 21111, 21112, 21113, 31111])
        keyList = sorted(list(connectedClassDict.keys()))
        self.assertEqual(keyList, [10010, 20010, 30010])
        self.assertEqual([i.code for i in connectedClassDict[10010]], [11111, 11112])
        self.assertEqual([i.code for i in connectedClassDict[20010]], [21111, 21112, 21113])
        self.assertEqual([i.code for i in connectedClassDict[30010]], [31111])

    def test_nonconnected_course_input(self):
        """
        Non-connected courses should be read in properly by readCourseFileToCourseData.
        """
        courses, connectedClassDict = readCourseFileToCourseData("unit_test_files/unit_test_input_4.txt", "")

        self.assertEqual(len(courses), 2)
        self.assertEqual([i.code for i in courses[0].classes], [10010, 20010])
        self.assertEqual([i.code for i in courses[1].classes], [11111, 11112, 21111])
        self.assertEqual(connectedClassDict, None)

    def test_fileInputRedZones(self):
        """
        fileInputRedZones should return correct values.
        """
        zones = fileInputRedZones("unit_test_files/unit_test_red_zones.txt")
        self.assertEqual(len(zones), 3)
        self.assertEqual(zones[0].start, TimeDataParser.toTime("1:00"))
        self.assertEqual(zones[0].end, TimeDataParser.toTime("9:00"))
        self.assertEqual(zones[1].start, TimeDataParser.toTime("3:00p"))
        self.assertEqual(zones[1].end, TimeDataParser.toTime("5:00p"))
        self.assertEqual(zones[2].start, TimeDataParser.toTime("10:00p"))
        self.assertEqual(zones[2].end, TimeDataParser.toTime("11:00p"))

class ScheduleInputFunctionTests(unittest.TestCase):

    def test_isInt(self):
        """
        _isInt should return correct values.
        """
        self.assertTrue(_isInt('534'))
        self.assertTrue(_isInt('-534'))
        self.assertTrue(_isInt('0'))
        self.assertTrue(_isInt('-0'))
        self.assertFalse(_isInt('a0'))
        self.assertFalse(_isInt('0a'))
        self.assertFalse(_isInt('asdf'))

    def test_isConnected(self):
        """
        _isConnected should return correct values and raise exceptions if necessary.
        """
        lecType = "LEC"
        labType = "LAB"
        lecTup = ("28100", lecType, "HA",  "4",   "STAFF", "MWF   9:00- 9:50",  "BS3 1200", "Wed, Mar 16, 8:00-10:00am", "64", "53", "n/a", "57", "0","", "OPEN")
        labTup = ("28100", labType, "HA",  "4",   "STAFF", "MWF   9:00- 9:50",  "BS3 1200", "Wed, Mar 16, 8:00-10:00am", "64", "53", "n/a", "57", "0","", "OPEN")
        lec = ClassDataParser.toClass(lecType, lecTup)
        lab = ClassDataParser.toClass(labType, labTup)
        self.assertFalse(_isConnected( [] ))
        self.assertFalse(_isConnected( [ [lec] ] ))
        self.assertFalse(_isConnected( [[lec, lec]] ))
        self.assertFalse(_isConnected( [[lec], [lab], [lec]] ))
        self.assertFalse(_isConnected( [[lec, lec], [lab], [lec]] ))
        self.assertTrue(_isConnected( [[lec], [lab]] ))
        self.assertRaises(ValueError, _isConnected, [[lec], [lab], [lec, lec], [lab]] )
        self.assertRaises(ValueError, _isConnected, [[lec], [lab], [lab, lab], [lab]] )

    def test_convertToClassesByType(self):
        """
        _convertToClassesByType should return correct values.
        """
        lecType = "LEC"
        labType = "LAB"
        lecTup = ("28100", lecType, "HA",  "4",   "STAFF", "MWF   9:00- 9:50",  "BS3 1200", "Wed, Mar 16, 8:00-10:00am", "64", "53", "n/a", "57", "0","", "OPEN")
        labTup = ("28100", labType, "HA",  "4",   "STAFF", "MWF   9:00- 9:50",  "BS3 1200", "Wed, Mar 16, 8:00-10:00am", "64", "53", "n/a", "57", "0","", "OPEN")
        NAME = "Human"

        def convertToTypeList(classes: 'list of list of Class') -> 'list of list of str':
            result = []
            for i in classes:
                newL = []
                for j in i:
                    newL.append(j.type)
                result.append(newL)
            return result

        self.assertEqual(convertToTypeList(_convertToClassesByType(NAME, [])), [])
        self.assertEqual(convertToTypeList(_convertToClassesByType(NAME, [lecTup])), [[lecType]])
        self.assertEqual(convertToTypeList(_convertToClassesByType(NAME, [lecTup, lecTup])), [[lecType, lecType]])
        self.assertEqual(convertToTypeList(_convertToClassesByType(NAME, [lecTup, labTup])), [[lecType], [labType]])
        self.assertEqual(convertToTypeList(_convertToClassesByType(NAME, [lecTup, lecTup, labTup, labTup])), [[lecType, lecType], [labType, labType]])
        self.assertEqual(convertToTypeList(_convertToClassesByType(NAME, [lecTup, labTup, lecTup, labTup])), [[lecType], [labType], [lecType], [labType]])

class WebsiteInputTests(unittest.TestCase):

    def test_getFileName(self):
        """
        _getFileName should returns correct values.
        """
        self.assertEqual(_getFileName("ICS 32"), "config/ics32.txt")
        self.assertEqual(_getFileName("ICS32"), "config/ics32.txt")
        self.assertEqual(_getFileName("IcS 32"), "config/ics32.txt")
        self.assertEqual(_getFileName("ics32"), "config/ics32.txt")

    def test_getTerm(self):
        """
        _getTerm should return correct value or raise exception for invalid input.
        """
        self.assertEqual(_getTerm("FALL"), Term.FALL)
        self.assertEqual(_getTerm("fall"), Term.FALL)
        self.assertEqual(_getTerm("FaLl"), Term.FALL)
        self.assertRaises(ValueError, _getTerm, "hello")

    def test_getDept(self):
        """
        _getDept should return correct value or raise exception for invalid input.
        """
        self.assertEqual(_getDept("I&C SCI\nICS 32\n36600-36623"), "I&C SCI")
        self.assertEqual(_getDept("I&C SCI\nICS 32"), "I&C SCI")
        self.assertEqual(_getDept("I&C SCI"), "I&C SCI")
        self.assertRaises(ValueError, _getDept, "   \nICS 32")
        self.assertRaises(ValueError, _getDept, "\nICS 32")
        self.assertRaises(ValueError, _getDept, "   \n")
        self.assertRaises(ValueError, _getDept, "   ")
        self.assertRaises(ValueError, _getDept, "")

    def test_getCourseName(self):
        """
        _getCourseName should return correct value or raise exception for invalid input.
        """
        self.assertEqual(_getCourseName("I&C SCI\nICS 32\n36600-36623"), "ICS 32")
        self.assertEqual(_getCourseName("I&C SCI\nICS 32"), "ICS 32")
        self.assertRaises(ValueError, _getCourseName, "I&C SCI")
        self.assertRaises(ValueError, _getCourseName, "I&C SCI\n")
        self.assertRaises(ValueError, _getCourseName, "I&C SCI\n   ")
        self.assertRaises(ValueError, _getCourseName, "")

    def test_getCourseCodes(self):
        """
        _getCourseCodes should return correct value or raise exception for invalid input..
        """
        self.assertEqual(_getCourseCodes("I&C SCI\nICS 32\n36600-36623"), "36600-36623")
        self.assertEqual(_getCourseCodes("I&C SCI\nICS 32\n"), "")
        self.assertEqual(_getCourseCodes("I&C SCI\nICS 32"), "")
        self.assertRaises(ValueError, _getCourseCodes, "I&C SCI\nICS 32\n36600-36623\nasdf")
        self.assertRaises(ValueError, _getCourseCodes, "I&C SCI\nICS 32\n36600-36623\n   ")
        self.assertRaises(ValueError, _getCourseCodes, "I&C SCI\nICS 32\n36600-36623\n")

    def test_parseCoursesParamsFromConfigFile(self):
        """
        _parseCoursesParamsFromConfigFile should return correct values.
        Particularly tests if returns correct course codes.
        """
        firstParams = (Term.WINTER, 2016, ["I&C SCI", "HUMAN", "I&C SCI"], ["ICS 32", "HUMAN 1B", "ICS 6B"])
        self.assertEqual(_parseCoursesParamsFromConfigFile("unit_test_files/unit_test_web_input_1.txt"), firstParams + (["36600-36623", "28100-28126", "49100-49130"], ))
        self.assertEqual(_parseCoursesParamsFromConfigFile("unit_test_files/unit_test_web_input_3.txt"), firstParams + (["", "28100-28126", "49100-49130"], ))
        self.assertEqual(_parseCoursesParamsFromConfigFile("unit_test_files/unit_test_web_input_4.txt"), firstParams + (["", "28100-28126", ""], ))
        self.assertEqual(_parseCoursesParamsFromConfigFile("unit_test_files/unit_test_web_input_5.txt"), firstParams + (["", "28100-28126", ""], ))
        self.assertEqual(_parseCoursesParamsFromConfigFile("unit_test_files/unit_test_web_input_7.txt"), firstParams + (["", "", ""], ))

if __name__ == "__main__":
    unittest.main()