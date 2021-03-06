OVERLAP_REMOVAL_ETA = True

class Schedule:
    def __init__(self, classes):
        self.classes = classes
    def hasOverlaps(self):
        for i in (range(len(self.classes) - 1)): # [0, second to last]
            for j in (range(i + 1, len(self.classes))): # [next, last]
                if( self.classes[i].days.overlapsWith(self.classes[j].days) and
                    self.classes[i].classTime.overlapsWith(self.classes[j].classTime)):
                    return True
        return False
    def hasValidConnections(self, connectedClassDict):
        for currClass in self.classes:
            if currClass.code in connectedClassDict:
                validConnection = False
                i = 0
                currConnected = connectedClassDict[currClass.code]
                while ((not validConnection) and (i < len(currConnected))):
                    if currConnected[i] in self.classes:
                        validConnection = True
                    else:
                        i += 1
                if not validConnection:
                    return False
        return True
    def calculatePreferenceScore(self, redZones, redZonePriority, minutesBetweenClasses, minutesBetweenClassesPriority):
        return (self.calculateRedZoneScore(redZones) * redZonePriority + self._calculateBetweenClassScore(minutesBetweenClasses) * minutesBetweenClassesPriority)
    def calculateRedZoneScore(self, redZones):
        score = 0
        for currClass in self.classes:
            currClassTime = currClass.classTime
            for redZone in redZones:
                if currClassTime.isWithin(redZone):
                    score -= 2
                elif currClassTime.overlapsWith(redZone):
                    score -= 1
        return score
    #Prerequisite: second is after first. First and second are both Times.
    def _getMinutesDifference(first, second):
        hourDiff = second.hour - first.hour
        minDiff = second.minute - first.minute
        return (hourDiff * 60 + minDiff)
    #Prerequisite: schedule has no overlaps
    def _calculateBetweenClassScore(self, minutesBetweenClasses):
        score = 0
        classTimes = [currClass.classTime for currClass in self.classes]
        #print([str(classTime) for classTime in classTimes])
        classTimes.sort(key=lambda classTime: classTime.start)
        #print("sorted!")
        #print([str(classTime) for classTime in classTimes])
        for i in range(len(classTimes) - 1): #[0, second to last element]
            if (Schedule._getMinutesDifference(classTimes[i].end, classTimes[i + 1].start) < minutesBetweenClasses):
                score -= 1
            else:
                score += 1
        return score
    def __str__(self):
        return "[%s]" % (", ".join(map(str, self.classes)))
    def getClassCodes(self):
        codes = []
        for currClass in self.classes:
            codes.append(currClass.code)
        return codes

def _overlapRemovalETA(schedules):
    import time

    nonOverlappingSchedules = []

    start = time.clock()
    for i in range(5):
        schedule = schedules[int(len(schedules)/2)]
        if not schedule.hasOverlaps():
            nonOverlappingSchedules.append(schedule)
    end = time.clock()

    eta = (end - start)/5 * len(schedules)
    print("Overlap removal ETA = %s" % (eta))
    #input("Press enter to continue...")

def generatePossibleSchedules(courses, connectedClassDict):
    schedules = [Schedule(subTuple) for subTuple in _generateAllSchedulesHelper(courses, 0)]

    if OVERLAP_REMOVAL_ETA:
        _overlapRemovalETA(schedules)

    return [schedule for schedule in schedules if (not schedule.hasOverlaps() and schedule.hasValidConnections(connectedClassDict))]

def _generateAllSchedulesHelper(courses, index):
    if index == len(courses): #if past last course
        return ((), )
    #else:
    mainList = []
    fnTuple = _generateAllSchedulesHelper(courses, index + 1)
    for currClass in courses[index].classes:
        for subTuple in fnTuple:
            mainList.append((currClass, ) + subTuple)
    return tuple(mainList)
