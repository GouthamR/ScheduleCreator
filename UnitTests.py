import unittest
from Course import *
from Schedule import *
from ScheduleInput import *

class ClassTests(unittest.TestCase):

    classRawTuple1 = ("36610", "LAB", "1", "0", "STAFF", "MWF   8:00- 9:50", "ICS 189", "", "44", "10/15", "n/a", "9", "0","A&N", "OPEN")

    def test_class_name(self):
        """
        Class should correctly store name argument.
        """
        name = "ClassName"
        class1 = Class(name, self.classRawTuple1)
        self.assertEqual(class1.name, name)

    def test_class_parse(self):
        """
        Class should correctly parse tuples.
        """
        class1 = Class("", self.classRawTuple1)
        self.assertEqual(class1.code, 36610)
        self.assertEqual(str(class1.days), str(Days("MWF")))
        self.assertEqual(str(class1.classTime), str(ClassTime("8:00- 9:50")))
        self.assertEqual(class1.type, "LAB")

class TimeTests(unittest.TestCase):

    def test_time_hour_construction(self):
        """
        Time should correctly interpret hour from input.
        """
        self.assertEqual(Time("11:00").hour, 11)
        self.assertEqual(Time("12:00p").hour, 12)
        self.assertEqual(Time("3:00p").hour, 15)
        self.assertEqual(Time("12:00").hour, 0)

    def test_time_comparison(self):
        """
        Time should correctly compare with other Times.
        """
        time1 = Time("8:00")
        time2 = Time("9:00")
        time3 = Time("9:00p")
        time4 = Time("10:00p")
        self.assertTrue(time1 < time2)
        self.assertTrue(time1 < time3)
        self.assertTrue(time2 < time3)
        self.assertTrue(time3 < time4)
        self.assertTrue(time1 <= time1)
        self.assertTrue(time1 >= time1)
        self.assertTrue(time2 <= time3)
        self.assertTrue(time4 >= time3)
        self.assertTrue(time1 == time1)

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
        self.assertTrue(ClassTime(classTimeRawStr1).overlapsWith(ClassTime(classTimeRawStr1)))
        self.assertTrue(ClassTime(classTimeRawStr1).overlapsWith(ClassTime(classTimeRawStr2)))
        self.assertTrue(ClassTime(classTimeRawStr1).overlapsWith(ClassTime(classTimeRawStr3)))
        self.assertFalse(ClassTime(classTimeRawStr1).overlapsWith(ClassTime(classTimeRawStr4)))
        self.assertFalse(ClassTime(classTimeRawStr1).overlapsWith(ClassTime(classTimeRawStr5)))

    def test_isWithin(self):
        """
        ClassTime should correctly check isWithin with other ClassTimes.
        """
        self.assertTrue(ClassTime("8:00- 8:50").isWithin(ClassTime("7:50- 9:00")))
        self.assertFalse(ClassTime("8:00- 8:50").isWithin(ClassTime("8:10- 8:40")))
        self.assertFalse(ClassTime("8:00- 8:50").isWithin(ClassTime("7:50- 8:40")))
        self.assertFalse(ClassTime("8:00- 8:50").isWithin(ClassTime("8:10- 9:00")))

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
        classes = [Class(self.NAME, classRawTuple1), Class(self.NAME, classRawTuple2)]
        c1 = Course(self.NAME, classes)
        self.assertEqual(c1.classes, classes)

class ScheduleTests(unittest.TestCase):

    def test_getClassCodes(self):
        """
        Schedule should return correct class codes.
        """
        classRawTuple1 = ("10000", "LEC", "1", "0", "STAFF", "MWF   8:00- 9:50", "ICS 189", "", "44", "10/15", "n/a", "9", "0","A&N", "OPEN")
        classRawTuple2 = ("20000", "LEC", "2", "0", "STAFF", "MWF   1:00- 2:50p", "ICS 180", "", "44", "10/15", "n/a", "9", "0","A&N", "OPEN")
        sched = Schedule([Class("", classRawTuple1), Class("", classRawTuple2)])
        self.assertEqual(sched.getClassCodes(), [10000, 20000])

class GenerateScheduleTests(unittest.TestCase):

    def test_generatePossibleSchedules(self):
        """
        generatePossibleSchedules should return correct values.
        """

        class_2_1 = Class("", ("21000", "LEC", "1", "0", "STAFF", "MWF   3:00- 3:50", "ICS 189", "", "44", "10/15", "n/a", "9", "0","A&N", "OPEN"))
        class_2_2 = Class("", ("22000", "LEC", "1", "0", "STAFF", "MWF   4:00- 5:00", "ICS 189", "", "44", "10/15", "n/a", "9", "0","A&N", "OPEN"))
        course2 = Course("", [class_2_1, class_2_2])
        class_3_1 = Class("", ("31000", "LEC", "1", "0", "STAFF", "TuTh   7:00- 8:00", "ICS 189", "", "44", "10/15", "n/a", "9", "0","A&N", "OPEN"))
        class_3_2 = Class("", ("32000", "LEC", "1", "0", "STAFF", "MW   7:00- 8:00", "ICS 189", "", "44", "10/15", "n/a", "9", "0","A&N", "OPEN"))
        course3 = Course("", [class_3_1, class_3_2])
        class_4_1 = Class("", ("41000", "LEC", "1", "0", "STAFF", "TuTh   10:00- 11:00", "ICS 189", "", "44", "10/15", "n/a", "9", "0","A&N", "OPEN"))
        course4 = Course("", [class_4_1])
        class_5_1 = Class("", ("51000", "LEC", "1", "0", "STAFF", "TuTh   10:00- 10:50", "ICS 189", "", "44", "10/15", "n/a", "9", "0","A&N", "OPEN"))
        course5 = Course("", [class_5_1])

        scheds_1 = generatePossibleSchedules([course2], {})
        scheds_2 = generatePossibleSchedules([course2, course4], {})
        scheds_3 = generatePossibleSchedules([course2, course3], {})
        scheds_4 = generatePossibleSchedules([course4, course5], {})

        self.assertEqual([s.classes for s in scheds_1], [(class_2_1, ), (class_2_2, )])
        self.assertEqual([s.classes for s in scheds_2], [(class_2_1, class_4_1), (class_2_2, class_4_1)])
        self.assertEqual([s.classes for s in scheds_3], [(class_2_1, class_3_1), (class_2_1, class_3_2), (class_2_2, class_3_1), (class_2_2, class_3_2)])
        self.assertEqual([s.classes for s in scheds_4], [])

if __name__ == "__main__":
    unittest.main()