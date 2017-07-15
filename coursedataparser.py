import course

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

def toTime(rawData: str) -> course.Time:
    """
    rawData is raw input time string.
    """
    rawHour, rawMinute = rawData.split(":")
    hour = _getHourFromInput(rawHour, rawMinute.endswith("p"))
    minute = int(rawMinute[:2]) #cuts off p if necessary
    return course.Time(hour, minute)

def toDays(rawData: str) -> course.Days:
    _TUESDAY_REPLACEMENT = 't'
    _THURSDAY_REPLACEMENT = 'T'
    _DAYS_MAP = { 'M': 0,
                _TUESDAY_REPLACEMENT: 1,
                'W': 2,
                _THURSDAY_REPLACEMENT : 3,
                'F': 4 }

    #Removes spaces, then converts Tuesday and Thursday to corresponding one-character strings to correspond with _DAYS_MAP:
    replaced_raw_data = rawData.replace(" ", "") \
                                .replace("Tu", _TUESDAY_REPLACEMENT) \
                                .replace("Th", _THURSDAY_REPLACEMENT)
    days_nums = [ _DAYS_MAP[char] for char in replaced_raw_data ]
    return course.Days(days_nums)


def _getDayCrossErrorMessage(rawSplit: 'list of str') -> str:
    """
    Returns error message mentioning rawSplit data.
    """
    _END_OF_DAY_ERROR_MESSAGE = "course.ClassTime crosses end of day"
    return "%s: %s" % (_END_OF_DAY_ERROR_MESSAGE, rawSplit)

def _calculateTimes(rawSplit: 'list of str', endIsPM: bool) -> (course.Time, course.Time):
    """
    Returns start and end times corresponding to parameters.
    Raises error if times are invalid.
    """
    end = toTime(rawSplit[1])
    timeArgStrs = (rawSplit[0] + "p", rawSplit[0])

    start = toTime(timeArgStrs[0]) if endIsPM else toTime(timeArgStrs[1])
    if start > end:
        start = toTime(timeArgStrs[1]) if endIsPM else toTime(timeArgStrs[0])
        if start > end:
            raise RuntimeError(_getDayCrossErrorMessage(rawSplit))

    return start, end

def toClassTime(rawData: str) -> course.ClassTime:
    rawSplit = rawData.replace(" ", "").split("-") # remove spaces, then split
    endIsPM = rawSplit[1].endswith('p')
    start, end = _calculateTimes(rawSplit, endIsPM)
    return course.ClassTime(start, end)

def toClass(name: str, data: 'tuple of str') -> course.Class:
    """
    data: a tuple of raw data string fields
    """
    _CODE_INDEX = 0
    _TYPE_INDEX = 1
    _DAY_TIME_INDEX = 5

    code = int(data[_CODE_INDEX])
    type_param = data[_TYPE_INDEX]
    day_time = data[_DAY_TIME_INDEX]
    day_end_index = day_time.index(' ')
    days = toDays(day_time[0:day_end_index])
    classTime = toClassTime(day_time[day_end_index:])
    
    return course.Class(name, code, days, classTime, type_param)