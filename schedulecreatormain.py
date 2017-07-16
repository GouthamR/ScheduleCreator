##Copyright 2017 Goutham R.  All rights reserved.
##Goutham R
##Started 7/29/15
##ScheduleCreator
##Generates schedules.

import pathlib
import tkinter as tk
import functools

import scheduleinput
from schedulegui import ScheduleGUI
from websiteinput import WebsiteInput
import configfileinput
import schedule

INPUT_FILE = pathlib.Path("config/web_input.txt")
REDZONE_FILE = pathlib.Path("config/red_zones.txt")
MINUTESBETWEEN_FILE = pathlib.Path("config/minutes_between_classes.txt")
COURSEFILES_DIR = pathlib.Path("coursefiles/")

def _initSchedules(scheduleGUI: ScheduleGUI):
    websiteInput = WebsiteInput(COURSEFILES_DIR)
    if websiteInput.savedFilesExist():
        print("Loading from saved course file...")
    else:
        print("Loading from website...")
        websiteInput.scrapeCoursesDataFromWebsiteAndSaveToFiles(*configfileinput.fileInputCourseParams(INPUT_FILE))
    
    courseFiles = websiteInput.getSavedCourseFiles()
    courses, connectedClassDict = scheduleinput.fileInputCourses(courseFiles)
    print("Starting schedule generation...")
    schedules = schedule.generatePossibleSchedules(courses, connectedClassDict)
    redZones = configfileinput.fileInputRedZones(REDZONE_FILE)
    minutesBetweenClasses = configfileinput.fileInputMinutesBetween(MINUTESBETWEEN_FILE)
    print("Number of schedules = " + str(len(schedules)))
    preferenceParams = (redZones, 2, minutesBetweenClasses, 1)
    schedules.sort(key=lambda sched: sched.calculatePreferenceScore(*preferenceParams), reverse=True)
    print("Done sorting")
    #print("\n".join([str(i.getClassCodes()) + " = " + str(i.calculatePreferenceScore(*preferenceParams)) for i in schedules]))
    for i in range(len(schedules)):
        curr_schedule = schedules[i]
        print("%s: %s = %s" % (i, curr_schedule.getClassCodes(), curr_schedule.calculatePreferenceScore(*preferenceParams)))

    scheduleGUI.initSchedules(schedules)

def _runProgram():
    print("CREATED BY GOUTHAM RAJEEV")
    print("Copyright 2016 Goutham Rajeev.  All rights reserved.")
    
    root = tk.Tk()
    root.protocol('WM_DELETE_WINDOW', root.destroy)
    root.title("Schedule Creator - Schedule Viewer. By Goutham Rajeev")
    scheduleGUI = ScheduleGUI(root)
    root.after(0, _initSchedules, scheduleGUI) # execute concurrently with tkinter main loop
    tk.mainloop()

def _main():
    try:
        _runProgram()
    except Exception as e:
        stars = "*" * 80
        print("\n{0}\nEXCEPTION. Check config files. Details follow:\n{0}\n".format(stars))
        raise

if __name__ == '__main__':
    _main()
