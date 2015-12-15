from Course import *

def fileInputRedZones(fileName):
    redZones = []
    with open(fileName, 'r') as f:
        for line in f:
            redZones.append(ClassTime(line.strip()))
    return redZones

def fileInputMinutesBetween(fileName):
    minutesBetween = None
    with open(fileName, 'r') as f:
        minutesBetween = int(f.read().strip())
    return minutesBetween

def fileInputRunUnitTests(fileName):
    INVALID_INPUT_ERROR_MESSAGE = "Invalid run_unit_tests file input"
    with open(fileName, 'r') as f:
        runTestsStr = f.read().strip()
        if runTestsStr == "True":
            return True
        elif runTestsStr == "False":
            return False
    #else:
    raise RuntimeError("%s: %s" % (INVALID_INPUT_ERROR_MESSAGE, runTestsStr))
