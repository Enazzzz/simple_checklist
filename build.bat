@echo off
echo Building checklist application with PyInstaller...
python -m PyInstaller checklist.spec
echo Build complete! Check the dist/ folder for the executable.
pause 