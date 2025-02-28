@echo off
chcp 65001 >nul
setlocal

:: Überprüfen, ob Python installiert ist
python --version >nul 2>&1
if %errorlevel% == 0 (
    echo Python ist bereits installiert.
    echo Drücke Enter, um das Skript zu beenden...
    pause >nul
    exit
)

:: Falls Python nicht installiert ist, nach Installation fragen
echo Python wurde nicht gefunden.
set /p install="Möchtest du Python 3.12 installieren? (ja/nein): "

if /I "%install%"=="ja" (
    echo Starte die Installation von Python 3.12...
    
    :: Installationsdatei herunterladen
    bitsadmin /transfer "PythonDownload" ^
        https://www.python.org/ftp/python/3.12.1/python-3.12.1-amd64.exe ^
        "%temp%\python-3.12.1-amd64.exe"

    :: Installation starten (Silent Mode mit PATH-Option)
    "%temp%\python-3.12.1-amd64.exe" /quiet InstallAllUsers=1 PrependPath=1
    
    echo Installation abgeschlossen.
    echo Drücke Enter, um das Skript zu beenden...
    pause >nul
    exit
) else (
    echo Installation abgebrochen.
    echo Drücke Enter, um das Skript zu beenden...
    pause >nul
    exit
)

endlocal
