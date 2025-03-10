@echo off
chcp 65001 >nul
echo Aurora Project Updater (Git Version)

:: Check for PowerShell
powershell -Command "Write-Host 'PowerShell is available'" >nul 2>&1
if %errorlevel% neq 0 (
    echo PowerShell is required to run the updater but was not found.
    echo Please install PowerShell and try again.
    pause
    exit /b 1
)

:: Check for Git
git --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Git is required to run the updater but was not found.
    echo Please install Git from https://git-scm.com/ and try again.
    pause
    exit /b 1
)

:: Check if the script exists
if not exist update-script.ps1 (
    echo Cannot find update.ps1 script. Please make sure it exists in the current directory.
    pause
    exit /b 1
)

echo Launching Git-based updater...
powershell -ExecutionPolicy Bypass -File .\update-script.ps1

:: No need for pause at the end as the PowerShell script already waits for input
