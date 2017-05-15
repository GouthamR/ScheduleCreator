# Note: created my own Time and ClassTime classes for the learning experience.

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

class TimeDataParser:
    """
    Parses raw input data to initialize Time objects.
    """
    @staticmethod
    def _getHourFromInput(rawHour: str, isPm: bool) -> int:
        """
        Returns hour corresponding to rawHour and if isPm as integer on [0, 24).
        """
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
    @staticmethod
    def toTime(rawData: str) -> Time:
        """
        rawData is raw input time string.
        """
        rawHour, rawMinute = rawData.split(":")
        hour = TimeDataParser._getHourFromInput(rawHour, rawMinute.endswith("p"))
        minute = int(rawMinute[:2]) #cuts off p if necessary
        return Time(hour, minute)

class Days:
    def __init__(self, rawData: str) -> None:
        self.days = DaysDataParser(rawData).days
    def overlapsWith(self, otherDays):
        for day in self.days:
            for otherDay in otherDays.days:
                if day == otherDay:
                    return True
        return False
    def __str__(self):
        return "Days: %s" % (self.days)

class DaysDataParser:
    """
    Parses raw input data for a Days class and stores corresponding Days
    data as field.
    """

    TUESDAY_REPLACEMENT = 't'
    THURSDAY_REPLACEMENT = 'T'
    DAYS_MAP = { 'M': 0,
                TUESDAY_REPLACEMENT: 1,
                'W': 2,
                THURSDAY_REPLACEMENT : 3,
                'F': 4 }

    def __init__(self, rawData: str) -> None:
        """
        Initializes fields.
        """
        #Removes spaces, then converts Tuesday and Thursday to corresponding one-character strings to correspond with DAYS_MAP:
        replaced_raw_data = rawData.replace(" ", "") \
                                    .replace("Tu", DaysDataParser.TUESDAY_REPLACEMENT) \
                                    .replace("Th", DaysDataParser.THURSDAY_REPLACEMENT)
        self.days = [ DaysDataParser.DAYS_MAP[char] for char in replaced_raw_data ]

class ClassTime:
    def __init__(self, rawData: str):
        data = ClassTimeDataParser(rawData)
        self.start, self.end = data.start, data.end
    def __str__(self):
        return "ClassTime: %s, %s" % (self.start, self.end)
    def overlapsWith(self, otherTime):
        return ((self.start >= otherTime.start and self.start <= otherTime.end) or #self begins during other
                (self.end >= otherTime.start and self.end <= otherTime.end) or #self ends during other
                (self.start <= otherTime.start and self.end >= otherTime.end)) #self begins before other and ends after other. i.e. encompassing other
                #other encompassing self is included in first two cases above
    def isWithin(self, other):
        return (self.start >= other.start and self.end <= other.end)

class ClassTimeDataParser:
    """
    Parses raw input data for a ClassTime class and stores corresponding ClassTime
    data (start, end, etc.) as fields.
    """

    END_OF_DAY_ERROR_MESSAGE = "ClassTime crosses end of day"

    def _getDayCrossErrorMessage(rawSplit: 'list of str') -> str:
        """
        Returns error message mentioning rawSplit data.
        """
        return "%s: %s" % (ClassTimeDataParser.END_OF_DAY_ERROR_MESSAGE, rawSplit)

    def _calculateTimes(rawSplit: 'list of str', endIsPM: bool) -> (Time, Time):
        """
        Returns start and end times corresponding to parameters.
        Raises error if times are invalid.
        """
        end = TimeDataParser.toTime(rawSplit[1])
        timeArgStrs = (rawSplit[0] + "p", rawSplit[0])

        start = TimeDataParser.toTime(timeArgStrs[0]) if endIsPM else TimeDataParser.toTime(timeArgStrs[1])
        if start > end:
            start = TimeDataParser.toTime(timeArgStrs[1]) if endIsPM else TimeDataParser.toTime(timeArgStrs[0])
            if start > end:
                raise RuntimeError(ClassTimeDataParser._getDayCrossErrorMessage(rawSplit))

        return start, end

    def __init__(self, rawData: str) -> None:
        """
        Initializes fields based on rawData.
        """
        rawSplit = rawData.replace(" ", "").split("-") # remove spaces, then split
        endIsPM = rawSplit[1].endswith('p')
        self.start, self.end = ClassTimeDataParser._calculateTimes(rawSplit, endIsPM)

class Class:
    """
    Note: name = name of course, e.g. ICS 31. Does NOT include course type.
    """
    def __init__(self, name: str, rawData: 'tuple of str') -> None:
        self.name = name
        parsed = ClassDataParser(rawData)
        self.code, self.days, self.classTime, self.type = \
            parsed.code, parsed.days, parsed.classTime, parsed.type
    def getFullName(self) -> str:
        """
        Returns full name of class, i.e. name and type.
        """
        return "{} {}".format(self.name, self.type.title())
    def __str__(self):
        return "Class: %s, %s" % (self.days, self.classTime)

class ClassDataParser:
    """
    Parses raw input data for a Class class and stores corresponding Class
    data (days, name, etc.) as fields.
    """

    CODE_INDEX = 0
    TYPE_INDEX = 1
    DAY_TIME_INDEX = 5

    def __init__(self, data: 'tuple of str') -> None:
        """
        Initializes fields based on rawData.
        """
        self.code = int(data[ClassDataParser.CODE_INDEX])
        self.type = data[ClassDataParser.TYPE_INDEX]
        day_time = data[ClassDataParser.DAY_TIME_INDEX]
        day_end_index = day_time.index(' ')
        self.days = Days(day_time[0:day_end_index])
        self.classTime = ClassTime(day_time[day_end_index:])

class Course:
    def __init__(self, name: str, classes: 'list of Class') -> None:
        """
        name:       the name of the course.
        classes:    this Course's classes.
        """
        self.name = name
        self.classes = classes
    def __str__(self):
        return "%s: [%s]" % (self.name, ", ".join(map(str, self.classes)))
