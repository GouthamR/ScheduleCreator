rmdir /s /q dist
python cxFreezeSetup.py build
robocopy config\ dist\config /s /e
robocopy coursefiles\ dist\coursefiles /s /e