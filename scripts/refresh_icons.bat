@echo off
echo Refreshing Windows icon cache...

REM Stop Windows Explorer
taskkill /f /im explorer.exe

REM Clear icon cache
del /q "%localappdata%\IconCache.db" 2>nul
del /q "%localappdata%\Microsoft\Windows\Explorer\iconcache*" 2>nul

REM Clear thumbnail cache
del /q "%localappdata%\Microsoft\Windows\Explorer\thumbcache*" 2>nul

REM Restart Windows Explorer
start explorer.exe

echo Icon cache refreshed! Please check your executable icon now.
pause 