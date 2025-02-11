@echo off
chcp 65001 >nul
REM --- Pakete aus requirements.txt installieren ---

echo Starte Installation der Pakete aus requirements.txt ...
pip freeze > installed.txt

for /f "tokens=*" %%i in (requirements.txt) do (
    findstr /c:"%%i" installed.txt >nul
    if errorlevel 1 (
        echo Installing %%i ...
        pip install %%i
    ) else (
        echo %%i ist bereits installiert.
    )
)

del installed.txt
echo.
xcopy "%~dp0Aurora.lnk" "%~dp0..\.." /Y
echo Installation abgeschlossen.
echo.

REM --- Abfrage: Verknüpfung erstellen? ---

:ASK_LINK
set /p CREATE_SHORTCUT="Soll eine Verknüpfung (Aurora.lnk) auf dem Desktop erstellt werden? (J/N): "

if /I "%CREATE_SHORTCUT%"=="J" goto CREATE
if /I "%CREATE_SHORTCUT%"=="N" goto NOPE
echo Bitte J oder N eingeben.
goto ASK_LINK

:CREATE
echo Erstelle Verknüpfung auf dem Desktop ...
xcopy "%~dp0Aurora.lnk" "%USERPROFILE%\Desktop" /Y

echo Verknüpfung wurde erstellt.
echo.
goto END

:NOPE
echo OK, es wird keine Verknüpfung erstellt.

:END
echo.
pause
exit
