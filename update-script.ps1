# Aurora Project Update Script (Git Version)
# This script updates the Aurora project via git pull while preserving user-specific data
# Version: 0.1.1
# Author: Sakushi-Dev

# Configuration
$backupDir = ".\update_backup"
$updateVersion = "0.1.1" # Change this to match your update version

# Files and directories to preserve
$preservePaths = @(
    "API\api_key.env",
    "data\costs",
    "data\history",
    "data\last_msg_time",
    "data\set",
    "data\mood\emotion_score.json",
    "prompts\user_spec"
)

# Create directories
function EnsureDirExists($path) {
    if (!(Test-Path -Path $path)) {
        New-Item -ItemType Directory -Path $path -Force | Out-Null
        Write-Host "Created directory: $path" -ForegroundColor Green
    }
}

# Display banner
function ShowBanner {
    Write-Host "`n`n=============================================" -ForegroundColor Cyan
    Write-Host "        AURORA PROJECT UPDATER v$updateVersion" -ForegroundColor Cyan
    Write-Host "=============================================" -ForegroundColor Cyan
    Write-Host "This script will update Aurora via Git while preserving your personal data.`n" -ForegroundColor White
}

# Check if Git is installed
function CheckGitInstalled {
    try {
        $gitVersion = git --version
        Write-Host "Git detected: $gitVersion" -ForegroundColor Green
        return $true
    } catch {
        Write-Host "Git is not installed or not in PATH. Please install Git to use this updater." -ForegroundColor Red
        return $false
    }
}

# Check if directory is a git repository
function IsGitRepository {
    if (Test-Path -Path ".git") {
        return $true
    } else {
        Write-Host "This directory is not a Git repository. You need to clone the repository first." -ForegroundColor Red
        return $false
    }
}

# Backup important user data
function BackupUserData {
    Write-Host "Backing up user data..." -ForegroundColor Yellow
    
    EnsureDirExists $backupDir
    
    foreach ($path in $preservePaths) {
        $fullPath = (Resolve-Path -Path ".\$path" -ErrorAction SilentlyContinue).Path
        
        if (Test-Path -Path ".\$path") {
            $destPath = Join-Path -Path $backupDir -ChildPath $path
            $destDir = Split-Path -Path $destPath -Parent
            
            # Create destination directory if it doesn't exist
            EnsureDirExists $destDir
            
            # Copy files or directories
            if (Test-Path -Path ".\$path" -PathType Container) {
                Copy-Item -Path ".\$path" -Destination $destDir -Recurse -Force
                Write-Host "  Backed up directory: $path" -ForegroundColor Green
            } else {
                Copy-Item -Path ".\$path" -Destination $destPath -Force
                Write-Host "  Backed up file: $path" -ForegroundColor Green
            }
        } else {
            Write-Host "  Skipping (not found): $path" -ForegroundColor Yellow
        }
    }
    
    Write-Host "Backup completed successfully." -ForegroundColor Green
}

# Pull latest changes from git
function GitPull {
    Write-Host "`nUpdating via Git pull..." -ForegroundColor Yellow
    
    try {
        # Stash any local changes first
        git stash
        Write-Host "Local changes stashed." -ForegroundColor Green
        
        # Pull the latest changes
        $pullResult = git pull
        
        if ($pullResult -match "Already up to date") {
            Write-Host "Repository is already up to date. No update needed." -ForegroundColor Green
            return $false
        } else {
            Write-Host "Update pulled successfully." -ForegroundColor Green
            return $true
        }
    } catch {
        Write-Host "Error during git pull: $_" -ForegroundColor Red
        return $false
    }
}

# Restore user data from backup
function RestoreUserData {
    Write-Host "`nRestoring user data..." -ForegroundColor Yellow
    
    foreach ($path in $preservePaths) {
        $backupPath = Join-Path -Path $backupDir -ChildPath $path
        
        if (Test-Path -Path $backupPath) {
            # Ensure target directory exists
            $targetDir = Split-Path -Path ".\$path" -Parent
            EnsureDirExists $targetDir
            
            # Copy back files or directories
            if (Test-Path -Path $backupPath -PathType Container) {
                Copy-Item -Path $backupPath -Destination $targetDir -Recurse -Force
                Write-Host "  Restored directory: $path" -ForegroundColor Green
            } else {
                Copy-Item -Path $backupPath -Destination ".\$path" -Force
                Write-Host "  Restored file: $path" -ForegroundColor Green
            }
        } else {
            Write-Host "  Skipping restoration (not found in backup): $path" -ForegroundColor Yellow
        }
    }
    
    Write-Host "User data restored successfully." -ForegroundColor Green
}

# Clean up temporary files
function CleanUp {
    Write-Host "`nCleaning up temporary files..." -ForegroundColor Yellow
    
    # Ask user if they want to keep the backup
    $keepBackup = Read-Host "Do you want to keep the backup? (Y/N)"
    
    if ($keepBackup -ne "Y" -and $keepBackup -ne "y") {
        Remove-Item -Path $backupDir -Recurse -Force -ErrorAction SilentlyContinue
        Write-Host "Backup directory removed." -ForegroundColor Green
    } else {
        Write-Host "Backup directory preserved at: $backupDir" -ForegroundColor Green
    }
}

# Run the update process
function RunUpdate {
    ShowBanner
    
    # Check prerequisites
    if (-not (CheckGitInstalled)) {
        return
    }
    
    if (-not (IsGitRepository)) {
        return
    }
    
    # Ask for confirmation
    $confirmation = Read-Host "Do you want to proceed with the update? (Y/N)"
    if ($confirmation -ne "Y" -and $confirmation -ne "y") {
        Write-Host "Update cancelled." -ForegroundColor Yellow
        return
    }
    
    # Check if the Aurora is running
    $auroraProcess = Get-Process -Name "python" -ErrorAction SilentlyContinue | Where-Object { $_.CommandLine -like "*aurora.py*" }
    if ($auroraProcess) {
        Write-Host "Aurora is currently running. Please close it before updating." -ForegroundColor Red
        $closeConfirmation = Read-Host "Attempt to close Aurora automatically? (Y/N)"
        if ($closeConfirmation -eq "Y" -or $closeConfirmation -eq "y") {
            $auroraProcess | Stop-Process -Force
            Write-Host "Aurora has been closed." -ForegroundColor Green
            Start-Sleep -Seconds 2  # Give it time to fully shut down
        } else {
            Write-Host "Please close Aurora manually and run this script again." -ForegroundColor Yellow
            return
        }
    }
    
    # Run update steps
    BackupUserData
    $updateApplied = GitPull
    
    if ($updateApplied) {
        RestoreUserData
        CleanUp
        
        Write-Host "`n=============================================" -ForegroundColor Cyan
        Write-Host "           UPDATE COMPLETED SUCCESSFULLY" -ForegroundColor Cyan
        Write-Host "=============================================" -ForegroundColor Cyan
        
        # Ask if user wants to start Aurora
        $startAurora = Read-Host "Do you want to start Aurora now? (Y/N)"
        if ($startAurora -eq "Y" -or $startAurora -eq "y") {
            Write-Host "Starting Aurora..." -ForegroundColor Green
            Start-Process -FilePath "powershell" -ArgumentList "-Command", ".\start.bat"
        }
    } else {
        Write-Host "`nNo updates were applied." -ForegroundColor Yellow
    }
}

# Run the update
RunUpdate
