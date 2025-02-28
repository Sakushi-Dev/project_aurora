@echo off
chcp 65001 >nul
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
exit