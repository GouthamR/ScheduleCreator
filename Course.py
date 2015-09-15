class Time:
    def getHourFromInput(rawHour, isPm):
        rawHourInt = int(rawHour)
        if isPm:
            if rawHourInt == 12:
                return 12
            else:
                return (rawHourInt + 12)
        else:
            if rawHourInt == 12:
                return 0
            else:
                return rawHourInt
    def __init__(self, rawData):
        rawHour, rawMinute = rawData.split(":")
        self.hour = Time.getHourFromInput(rawHour, rawMinute.endswith("p"))
        self.minute = int(rawMinute[:2]) #cuts off p if necessary
    def getTotalMinutes(self):
        return (self.hour * 60 + self.minute)
    def getFormatted(self):
        hour_12 = None
        if self.hour <= 12:
            hour_12 = self.hour
        else:
            hour_12 = self.hour - 12
        return "%d:%02d" % (hour_12, self.minute)
    def __str__(self):
        return "Time: %s:%s" % (self.hour, self.minute)
    def __lt__(self, other):
        return (((self.hour == other.hour) and (self.minute < other.minute)) #same hour, different minute
            or self.hour < other.hour) #(different hour and same minute) OR (different hour and different minute)
    def __gt__(self, other):
        return (not (self == other) and not (self < other))
    def __eq__(self, other):
        return self.hour == other.hour and self.minute == other.minute
    def __le__(self, other):
        return (self < other or self == other)
    def __ge__(self, other):
        return (self > other or self == other)

class Days:
    def __init__(self, rawData):
        self.days = []
        daysDict = { 'M': 0, 't': 1, 'W': 2, 'T' : 3, 'F': 4} #move outside function for performance
        for c in rawData.replace(" ", "").replace("Th","T").replace("Tu","t"): #Removes spaces, then converts Tuesday and Thursday to one character strings, to correspond with above dict
            self.days.append(daysDict[c])
    def overlapsWith(self, otherDays):
        for day in self.days:
            for otherDay in otherDays.days:
                if day == otherDay:
                    return True
        return False
    def __str__(self):
        return "Days: %s" % (self.days)

class ClassTime:
    END_OF_DAY_ERROR_MESSAGE = "ClassTime crosses end of day"
    def calculateTimes(rawSplit, endIsPM):
        end = Time(rawSplit[1])
        start = None
        if endIsPM:
            start = Time(rawSplit[0] + "p")
            if start > end:
                start = Time(rawSplit[0])
                if start > end:
                    raise RuntimeError("%s: %s" % (ClassTime.END_OF_DAY_ERROR_MESSAGE, rawSplit))
        else:
            start = Time(rawSplit[0])
            if start > end:
                start = Time(rawSplit[0] + "p")
                if start > end:
                    raise RuntimeError("%s: %s" % (ClassTime.END_OF_DAY_ERROR_MESSAGE, rawSplit))
        return start, end
    def __init__(self, rawData):
        rawSplit = rawData.replace(" ", "").split("-") #remove spaces, then split
        endIsPM = rawSplit[1].endswith('p')
        self.start, self.end = ClassTime.calculateTimes(rawSplit, endIsPM)
    def __str__(self):
        return "ClassTime: %s, %s" % (self.start, self.end)
    def overlapsWith(self, otherTime):
        return ((self.start >= otherTime.start and self.start <= otherTime.end) or #self begins during other
                (self.end >= otherTime.start and self.end <= otherTime.end) or #self ends during other
                (self.start <= otherTime.start and self.end >= otherTime.end)) #self begins before other and ends after other. i.e. encompassing other
                #other encompassing self is included in first two cases above
    def isWithin(self, other):
        return (self.start >= other.start and self.end <= other.end)

class Class:
    DATA_TIMINGS_INDEX = 5
    DATA_TYPE_INDEX = 1
    def __init__(self, rawData):
        self.rawData = rawData
        rawSplit = rawData.split("\t")
        self.code = int(rawSplit[0])
        timingsList = rawSplit[Class.DATA_TIMINGS_INDEX].split("   ")
        self.days = Days(timingsList[0])
        self.classTime = ClassTime(timingsList[1])
        self.type = rawSplit[Class.DATA_TYPE_INDEX]
        self.name = "No Name"
    def setName(self, name):
        self.name = name
    def __str__(self):
        return "Class: %s, %s" % (self.days, self.classTime)

class Course:
    def __init__(self, name):
        self.name = name
        self.classes = []
    def addClass(self, newClass):
        self.classes.append(newClass)
        newClass.setName(self.name)
    def __str__(self):
        return "%s: [%s]" % (self.name, ", ".join(map(str, self.classes)))
