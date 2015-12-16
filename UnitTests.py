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

if __name__ == "__main__":
    unittest.main()