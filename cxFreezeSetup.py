import sys
from cx_Freeze import setup, Executable

build_exe_options = {"build_exe": "dist/"}

setup(name = "ScheduleCreator",
		version = "0.5",
        description = "ScheduleCreator by GouthamR",
        options = {"build_exe": build_exe_options},
        executables = [Executable("ScheduleCreatorMain.py")])