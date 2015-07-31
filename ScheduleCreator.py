##Goutham Rajeev
##Started 7/29/15
##ScheduleCreator
##Generates schedules.

class Time:
    def __init__(self, rawData):
        rawHour, rawMinute = rawData.split(":")
        self.hour = int(rawHour)
        if(rawMinute.endswith("p")):
            self.hour += 12
        self.minute = int(rawMinute[:2]) #cuts off p if necessary
    def __str__(self):
        return "Time: %s:%s" % (self.hour, self.minute)

class Days:
    def __init__(self, rawData):
        self.days = []
        daysDict = { 'M': 0, 't': 1, 'W': 2, 'T' : 3, 'F': 4} #move outside function for performance
        for c in rawData.replace(" ", "").replace("Th","T").replace("Tu","t"): #Removes spaces, then converts Tuesday and Thursday to one character strings, to correspond with above dict
            self.days.append(daysDict[c])
    def __str__(self):
        return "Days: %s" % (self.days)

class ClassTime:
    def __init__(self, rawData):
        timeStrList = rawData.replace(" ", "").split("-") #remove spaces, then split
        self.start = Time(timeStrList[0])
        self.end = Time(timeStrList[1])
    def __str__(self):
        return "ClassTime: %s, %s" % (self.start, self.end)
    def overlapsWith(otherTime):
        return self.start < otherTime.end or self.end > otherTime.start

class Class:
    DATA_TIMINGS_INDEX = 5
    def __init__(self, rawData):
        self.rawData = rawData
        rawSplit = rawData.split("\t")
        timingsList = rawSplit[Class.DATA_TIMINGS_INDEX].split("   ")
        self.days = Days(timingsList[0])
        self.classTime = ClassTime(timingsList[1])
    def __str__(self):
        return "Class: %s, %s" % (self.days, self.classTime)

def unitTests():
    classRawStr = "44215	Lec	A	4	STAFF	MWF   8:00- 8:50	DBH 1100	Sat, Dec 5, 1:30-3:30pm	221	34	0	51	111	A and N	Bookstore	 	OPEN"
    print("Class parse test: %s" % (str(Class(classRawStr)) == "Class: Days: [0, 2, 4], ClassTime: Time: 8:0, Time: 8:50"))
    print("End unit tests.")

def main():
    classes = []
    currInput = "_flag_"

    print ("Type in classes. Press enter when finished.")
    while currInput != "":
        currInput = input(" -> ")
        if(currInput != ""):
            classes.append(Class(currInput))

    print ("%s" % "\n".join(map(str, classes)))

unitTests()
main()
