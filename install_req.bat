@echo off
chcp 65001 >nul
setlocal

:: --- Prüfen, ob Python installiert ist ---
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python ist nicht installiert. Installation wird gestartet...

    :: Python-Installer herunterladen (neueste Version - ggf. URL anpassen)
    echo Lade Python herunter...
    curl -o python_installer.exe https://www.python.org/ftp/python/3.12.1/python-3.12.1-amd64.exe

    :: Python installieren (Silent Mode)
    echo Installiere Python...
    start /wait python_installer.exe /quiet InstallAllUsers=1 PrependPath=1

    :: Überprüfe erneut, ob Python nun installiert ist
    python --version >nul 2>&1
    if %errorlevel% neq 0 (
        echo Fehler: Python konnte nicht installiert werden!
        exit /b 1
    ) else (
        echo Python wurde erfolgreich installiert.
    )
) else (
    echo Python ist bereits installiert.
)

:: --- Prüfen, ob pip funktioniert ---
pip --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Fehler: pip wurde nicht gefunden. Versuche, es zu reparieren...
    python -m ensurepip --default-pip
    python -m pip install --upgrade pip
)

:: --- Pakete aus requirements.txt installieren ---
echo.
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
echo Installation abgeschlossen.
echo.
exit /b 0
