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

def main():
    courses, connectedClassDict = fileInputCourses(INPUT_FILE_NAME)
    schedules = generatePossibleSchedules(courses, connectedClassDict)
    redZones = fileInputRedZones(REDZONE_FILE_NAME)
    minutesBetweenClasses = 30
    print("Number of schedules = " + str(len(schedules)))
    preferenceParams = (redZones, 2, minutesBetweenClasses, 1)
    print("\n".join([str(i.getClassCodes()) + str(i.calculatePreferenceScore(*preferenceParams)) for i in schedules]))
    schedules.sort(key=lambda sched: sched.calculatePreferenceScore(*preferenceParams), reverse=True)
    print("done sorting")
    print("\n".join([str(i.getClassCodes()) + str(i.calculatePreferenceScore(*preferenceParams)) for i in schedules]))
    ScheduleGUI(schedules)

unitTests()
main()
