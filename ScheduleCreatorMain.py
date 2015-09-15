##Goutham Rajeev
##Started 7/29/15
##ScheduleCreator
##Generates schedules.

from Course import *
from Schedule import *
from ScheduleInput import *
from UnitTests import *
from ScheduleGUI import *

INPUT_FILE_NAME = "input.txt"
REDZONE_FILE_NAME = "red_zones.txt"
MINUTESBETWEEN_FILE_NAME = "minutes_between_classes.txt"
RUNUNITTESTS_FILE_NAME = "run_unit_tests.txt"

def main():
    courses, connectedClassDict = fileInputCourses(INPUT_FILE_NAME)
    print("Starting schedule generation...")
    schedules = generatePossibleSchedules(courses, connectedClassDict)
    redZones = fileInputRedZones(REDZONE_FILE_NAME)
    minutesBetweenClasses = fileInputMinutesBetween(MINUTESBETWEEN_FILE_NAME)
    print("Number of schedules = " + str(len(schedules)))
    preferenceParams = (redZones, 2, minutesBetweenClasses, 1)
    schedules.sort(key=lambda sched: sched.calculatePreferenceScore(*preferenceParams), reverse=True)
    print("Done sorting")
    print("\n".join([str(i.getClassCodes()) + " = " + str(i.calculatePreferenceScore(*preferenceParams)) for i in schedules]))
    ScheduleGUI(schedules)

if fileInputRunUnitTests(RUNUNITTESTS_FILE_NAME):
    unitTests()
main()
