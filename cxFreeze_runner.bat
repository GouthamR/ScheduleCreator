rmdir /s /q dist
python cxFreezeSetup.py build
robocopy config\ dist\config /s /e