import pathlib

from course import *
import coursedataparser

# Note: sub-course is all the classes of a single type within a course. E.g. sub-course of ICS31 is ICS31 Lec.

_HEADER_START = "CCode"

def _isInt(input: str) -> int:
    """ Checks if input str contains an integer. """
    try:
        int(input)
        return True
    except Exception:
        return False

def _isTableHeader(line: str) -> bool:
    """
    Returns True if line is in format of course table header.
    """
    return line.strip().startswith(_HEADER_START)

def _isClassFormat(line: str) -> bool:
    """
    Returns True if line is in format of class fields.
    """
    return _isInt(line.strip()[0:5])

def _getColumnIndices(line: str) -> 'list of (tuple of int)':
    """
    Returns list representing position of each column in line.
    Each element is a tuple of form (start index, end index), except for
    last element which is of form (start index, None).
    """
    column_indices = []
    column_names = line.split()
    for i in range(len(column_names) - 1):
        column_indices.append( (line.index(column_names[i]), line.index(column_names[i+1])) )
    column_indices.append( (line.index(column_names[-1]), None) )
    return column_indices

def _getClassTuple(line: str, column_indices: 'list of (tuple of int)') -> 'tuple of str':
    """
    Returns tuple of class fields corresponding to input line,
    using table format based on column_indices.
    """
    new_class = []
    for i in range(len(column_indices) - 1):
        new_class.append(line[column_indices[i][0]:column_indices[i][1]].strip())
    new_class.append(line[column_indices[-1][0]:].strip())
    return tuple(new_class)

def readCourseFileToTuples(courseFile: pathlib.Path) -> 'list of (tuple of str)':
    """
    Reads file for a course and returns list of tuples, with each tuple
    corresponding to each class in file.
    """
    tuples = []
    curr_column_indices = None
    with courseFile.open('r') as f:
        for line in f:
            if _isTableHeader(line):
                curr_column_indices = _getColumnIndices(line)
            elif _isClassFormat(line):
                tuples.append(_getClassTuple(line, curr_column_indices))
    return tuples

def _isConnected(splitClasses: 'list of list of Class') -> bool:
    """
    Returns if course represented by argument is a connected course.
    If not valid connected course with two-sub-courses, raises ValueError.
    """
    numSubCourses = len(splitClasses)
    if numSubCourses < 2 or len(splitClasses[0]) != 1 or numSubCourses % 2 != 0:
        return False
    # else, number of sub-courses is even and at least 2, and first sub-course has one class.
    # Now, check for valid sub-course connection:
    firstType = splitClasses[0][0].type
    for i in range(2, len(splitClasses), 2):
        currSubCourse = splitClasses[i]
        if len(currSubCourse) != 1 or currSubCourse[0].type != firstType:
            raise ValueError("Invalid connected courses.")
    # if here, no exception raised:
    return True

def _convertToClassesByType(courseName: str, tuples: 'list of tuple') -> 'list of list of Class':
    """
    Converts argument list of class-tuples into multiple lists of Class, where
    each list is made up of the classes of one type in sequence.
    E.g. For [lec, lec, lab, lec], returns [[lec, lec], [lab], [lec]].
    """
    classes = []
    prevType = None
    for tup in tuples:
        try:
            currClass = coursedataparser.toClass(courseName, tup)
        except ValueError:
            print("SKIPPING INVALID CLASS: {}".format(tup))
        else:
            currType = currClass.type
            if currType != prevType:
                classes.append([currClass])
                prevType = currType
            else:
                classes[-1].append(currClass)
    return classes

def _convertConnectedSplitClassesToCourseData(splitClasses: 'list of list of Class',
                                                courseName: str) -> ('list of Course', 'dict of (courseNum:list of Class)'):
    """
    For connected course data split classes, returns sub-course objects and
    dict of connected class data.
    Assumes only two sub-courses for connected courses.
    """
    course1Classes = []
    course2Classes = []
    connectedClassDict = {}
    for i in range(0, len(splitClasses), 2):
        currCourse1Class = splitClasses[i][0]
        course1Classes.append(currCourse1Class)
        key = currCourse1Class.code
        connectedClassDict[key] = []
        for currCourse2Class in splitClasses[i + 1]:
            course2Classes.append(currCourse2Class)
            connectedClassDict[key].append(currCourse2Class)
    course1 = Course(courseName, course1Classes)
    course2 = Course(courseName, course2Classes)
    return [course1, course2], connectedClassDict

def readCourseFileToCourseData(courseFile: pathlib.Path) -> ([Course], 'dict of (courseNum:list of Class) OR None'):
    """
    Reads course data from argument file.
    If course is connected, returns sub-courses and dict of connected class data.
    If course is not connected, returns sub-courses and None.
    Assumes only two sub-courses for connected courses.
    """
    print("courseFileType is: ")
    courseName = courseFile.stem
    tuples = readCourseFileToTuples(courseFile)
    splitClasses = _convertToClassesByType(courseName, tuples)
    if _isConnected(splitClasses):
        return _convertConnectedSplitClassesToCourseData(splitClasses, courseName)
    else:
        subCourses = [Course(courseName, subCourseClasses) for subCourseClasses in splitClasses]
        return subCourses, None

def fileInputCourses(files: [pathlib.Path]) -> ([Course], 'dict of (courseNum:list of Class) OR None'):
    """
    Reads course data from argument course files.
    Returns sub-courses and dict of connected class data.
    If no connected courses, returns sub-courses and None.
    """
    subCourses = []
    connectedClassDict = None
    for i in range(len(files)):
        currSubCourses, currDict = readCourseFileToCourseData(files[i])
        subCourses.extend(currSubCourses)
        if currDict != None:
            if connectedClassDict == None:
                connectedClassDict = {}
            connectedClassDict.update(currDict)
    return subCourses, connectedClassDict