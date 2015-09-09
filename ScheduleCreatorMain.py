##Goutham Rajeev
##Started 7/29/15
##ScheduleCreator
##Generates schedules.

from Course import *
from Schedule import *
from ScheduleInput import *
from UnitTests import *
from ScheduleGUI import *

def main():
    courses, connectedClassDict = fileInputCourses("actual_input_3.txt")
    schedules = generatePossibleSchedules(courses, connectedClassDict)
    redZones = fileInputRedZones("red_zones.txt")
    minutesBetweenClasses = 30
    #print([schedule.getClassCodes() for schedule in schedules])
    print("Number of schedules = " + str(len(schedules)))
    preferenceParams = (redZones, 2, minutesBetweenClasses, 1)
    print("\n".join([str(i.getClassCodes()) + str(i.calculatePreferenceScore(*preferenceParams)) for i in schedules]))
    schedules.sort(key=lambda sched: sched.calculatePreferenceScore(*preferenceParams), reverse=True)
    print("done sorting")
    print("\n".join([str(i.getClassCodes()) + str(i.calculatePreferenceScore(*preferenceParams)) for i in schedules]))
    ScheduleGUI(schedules)

unitTests()
main()
