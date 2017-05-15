# Note: I created my own Time class for the learning experience.

class Time:
    def __init__(self, hour: int, minute: int):
        """
        hour parameter should be int on interval [0, 23].
        minute parameter should be int on interval [0, 50].
        """
        self.hour = hour
        self.minute = minute
    def getTotalMinutes(self) -> int:
        return (self.hour * 60 + self.minute)
    def getFormatted(self) -> str:
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
    def __init__(self, days: [int]) -> None:
        """
        days is a list of int where each int corresponds to a day as follows:
        Monday: 0, Tuesday: 1, ..., Friday: 4
        """
        self.days = days
    def overlapsWith(self, otherDays) -> bool:
        for day in self.days:
            for otherDay in otherDays.days:
                if day == otherDay:
                    return True
        return False
    def __str__(self):
        return "Days: %s" % (self.days)

class ClassTime:
    def __init__(self, start: Time, end: Time):
        self.start = start
        self.end = end
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
    """
    name: name of course, e.g. ICS 31. Does NOT include course type.
    code: integer class code, e.g. 50713
    type_param: string class type, e.g. "lecture", "discussion"
    """
    def __init__(self, name: str, code: int, days: Days, classTime: ClassTime, type_param: str):
        self.name = name
        self.code = code
        self.days = days
        self.classTime = classTime
        self.type = type_param
    def getFullName(self) -> str:
        """
        Returns full name of class, i.e. name and type.
        """
        return "{} {}".format(self.name, self.type.title())
    def __str__(self):
        return "Class: %s, %s" % (self.days, self.classTime)

class Course:
    def __init__(self, name: str, classes: [Class]) -> None:
        """
        name:       the name of the course.
        classes:    this Course's classes.
        """
        self.name = name
        self.classes = classes
    def __str__(self):
        return "%s: [%s]" % (self.name, ", ".join(map(str, self.classes)))
