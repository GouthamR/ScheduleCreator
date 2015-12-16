import unittest
from Course import *
from Schedule import *
from ScheduleInput import *

class ClassConstruction(unittest.TestCase):
    """
    Tests Class constructor.
    """

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

if __name__ == "__main__":
    unittest.main()