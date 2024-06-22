@echo off
setlocal enabledelayedexpansion

echo Searching for .cpg, .cpp, and .dylib files across the entire C:\ drive:
echo --------------------------------------------------------

for /r "C:\" %%F in (*.cpg *.cpp *.dylib) do (
    echo File found: %%F
    echo ------------
    type "%%F"
    echo.
)

pause
