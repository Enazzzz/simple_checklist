@echo off
echo Installing CSV Checklist Application dependencies...

echo Installing Python packages...
pip install -r requirements.txt

echo.
echo Installation complete!
echo.
echo To run the application:
echo   python checklist.py
echo.
echo To build the executable:
echo   build.bat
echo.
pause 