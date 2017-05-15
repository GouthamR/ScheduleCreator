from Course import *

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

class DaysDataParser:
    """
    Parses raw input data for a Days class and stores corresponding Days
    data as field.
    """

    _TUESDAY_REPLACEMENT = 't'
    _THURSDAY_REPLACEMENT = 'T'
    _DAYS_MAP = { 'M': 0,
                _TUESDAY_REPLACEMENT: 1,
                'W': 2,
                _THURSDAY_REPLACEMENT : 3,
                'F': 4 }

    @staticmethod
    def toDays(rawData: str) -> Days:
        #Removes spaces, then converts Tuesday and Thursday to corresponding one-character strings to correspond with _DAYS_MAP:
        replaced_raw_data = rawData.replace(" ", "") \
                                    .replace("Tu", DaysDataParser._TUESDAY_REPLACEMENT) \
                                    .replace("Th", DaysDataParser._THURSDAY_REPLACEMENT)
        days_nums = [ DaysDataParser._DAYS_MAP[char] for char in replaced_raw_data ]
        return Days(days_nums)

class ClassTimeDataParser:
    """
    Parses raw input data for a ClassTime class and stores corresponding ClassTime
    data (start, end, etc.) as fields.
    """

    _END_OF_DAY_ERROR_MESSAGE = "ClassTime crosses end of day"

    @staticmethod
    def _getDayCrossErrorMessage(rawSplit: 'list of str') -> str:
        """
        Returns error message mentioning rawSplit data.
        """
        return "%s: %s" % (ClassTimeDataParser._END_OF_DAY_ERROR_MESSAGE, rawSplit)

    @staticmethod
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

    @staticmethod
    def toClassTime(rawData: str) -> ClassTime:
        """
        Initializes fields based on rawData.
        """
        rawSplit = rawData.replace(" ", "").split("-") # remove spaces, then split
        endIsPM = rawSplit[1].endswith('p')
        start, end = ClassTimeDataParser._calculateTimes(rawSplit, endIsPM)
        return ClassTime(start, end)

class ClassDataParser:

    _CODE_INDEX = 0
    _TYPE_INDEX = 1
    _DAY_TIME_INDEX = 5

    @staticmethod
    def toClass(name: str, data: 'tuple of str') -> Class:
        """
        data: a tuple of raw data string fields
        """
        code = int(data[ClassDataParser._CODE_INDEX])
        type_param = data[ClassDataParser._TYPE_INDEX]
        day_time = data[ClassDataParser._DAY_TIME_INDEX]
        day_end_index = day_time.index(' ')
        days = DaysDataParser.toDays(day_time[0:day_end_index])
        classTime = ClassTimeDataParser.toClassTime(day_time[day_end_index:])
        return Class(name, code, days, classTime, type_param)