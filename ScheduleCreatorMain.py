##Copyright 2016 Goutham Rajeev.  All rights reserved.
##Goutham Rajeev
##Started 7/29/15
##ScheduleCreator
##Generates schedules.

import pathlib

from ScheduleInput import *
from ScheduleGUI import *
from WebsiteInput import *
from ConfigFileInput import *

INPUT_FILE = pathlib.Path("config/web_input.txt")
REDZONE_FILE_NAME = "config/red_zones.txt"
MINUTESBETWEEN_FILE_NAME = "config/minutes_between_classes.txt"
COURSEFILES_DIR = pathlib.Path("coursefiles/")

def runProgram():
    print("CREATED BY GOUTHAM RAJEEV")
    print("Copyright 2016 Goutham Rajeev.  All rights reserved.")
    websiteInput = WebsiteInput(COURSEFILES_DIR)
    if websiteInput.savedFilesExist():
        print("Loading from saved course file...")
    else:
        print("Loading from website...")
        websiteInput.scrapeCoursesDataFromWebsiteAndSaveToFiles(*parseCoursesParamsFromConfigFile(INPUT_FILE))
    courseFiles = websiteInput.getSavedCourseFiles()
    courses, connectedClassDict = fileInputCourses(courseFiles)
    print("Starting schedule generation...")
    schedules = generatePossibleSchedules(courses, connectedClassDict)
    redZones = fileInputRedZones(REDZONE_FILE_NAME)
    minutesBetweenClasses = fileInputMinutesBetween(MINUTESBETWEEN_FILE_NAME)
    print("Number of schedules = " + str(len(schedules)))
    preferenceParams = (redZones, 2, minutesBetweenClasses, 1)
    schedules.sort(key=lambda sched: sched.calculatePreferenceScore(*preferenceParams), reverse=True)
    print("Done sorting")
    #print("\n".join([str(i.getClassCodes()) + " = " + str(i.calculatePreferenceScore(*preferenceParams)) for i in schedules]))
    for i in range(len(schedules)):
        schedule = schedules[i]
        print("%s: %s = %s" % (i, schedule.getClassCodes(), schedule.calculatePreferenceScore(*preferenceParams)))
    ScheduleGUI(schedules)

def main():
    try:
        runProgram()
    except Exception as e:
        stars = "*" * 80
        print("\n{0}\nEXCEPTION. Check config files. Details follow:\n{0}\n".format(stars))
        raise

if __name__ == '__main__':
    main()
