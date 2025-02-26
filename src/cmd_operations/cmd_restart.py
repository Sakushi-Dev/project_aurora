import os

def execute_restart():
    os.system('cls' if os.name == 'nt' else 'clear')  # Bildschirm leeren

    # Skript neu starten (ohne Pfad-Ausgabe in PowerShell)
    os.system('python "./src/aurora.py"')