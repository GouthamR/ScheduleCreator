rmdir /s /q dist
py -m py2exe.build_exe ScheduleCreatorMain.py
robocopy config\ dist\config /s /e
robocopy coursefiles\ dist\coursefiles /s /e