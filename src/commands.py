import os
import sys
import time

from rich.console import Console

# History-Manager-Import:
from history_manager import (
    replay_last_interaction,
    load_history_from_file,
)

from task_organizer import (
    print_latest_messages
)

# Rich-Console-Objekt:
console = Console(width=84)

# 1) Lokale Datei-History laden
full_history = load_history_from_file()


def handle_exit():
    console.print("Chat beendet. Tschüss!")
    return "exit"

def handle_again(user, old_history, highlighted):

    # Letzte User-Nachricht Speichern und full_history neu laden ohne letzte Nachricht
    full_history, last_user_message = replay_last_interaction(old_history)
    if last_user_message:

        # Clear Screen
        os.system('cls' if os.name == 'nt' else 'clear')

        # Alte Usernachricht anzeigen
        user_input = last_user_message["content"]

        # Analyse-Datei neu laden
        if "history.analytics" in sys.modules:
            del sys.modules["history.analytics"]
        from history.analytics import analytics  # type: ignore

        # Letzten Eintrag aus analytics entfernen
        if analytics:
            analytics.pop()  # KI-Antwort
            analytics.pop()  # User-Eingabe

            full_history = old_history[:-4]

        # History laden und erneut ausgeben
        print_latest_messages(full_history, highlighted=highlighted)
        console.print(f"[{user}]:\n\n{user_input}\n")

        # Löschen in Datei.py
        with open("./src/history/analytics.py", "w") as f:
            f.write("analytics = [\n")
            for msg in analytics:
                f.write(f"{msg},\n")
            f.write("]\n")

        # Analyse-Datei neu laden
        if "history.analytics" in sys.modules:
            del sys.modules["history.analytics"]
        from history.analytics import analytics  # type: ignore
    else:
        console.print("[red]Nichts zum Wiederholen gefunden.[/red]")
    return full_history, user_input

    

def handle_delete():
    delete = console.input("[red]Sind Sie sicher, dass Sie den Chatverlauf löschen möchten? (Y/N): [/red]")
    if delete.lower() == "y":
        # Screen leeren
        os.system('cls' if os.name == 'nt' else 'clear')

        # File-Backup löschen
        file_path = "./src/history/history_backup.py"
        if os.path.exists(file_path):
            os.remove(file_path)
        print("Backup-Datei gelöscht.")
        time.sleep(0.2)
        
        # Analyse-Datei löschen
        file_path = "./src/history/analytics.py"
        if os.path.exists(file_path):
            os.remove(file_path)
        print("Analyse-Datei gelöscht.")
        time.sleep(0.2)

        # costs.py löschen
        file_path = "./src/history/costs.py"
        if os.path.exists(file_path):
            os.remove(file_path)
        print("Kosten-Datei gelöscht.")
        time.sleep(0.2)

        # emotion_score.json löschen
        file_path = "./data/emotion_score.json"
        if os.path.exists(file_path):
            os.remove(file_path)
        print("Emotion-Datei gelöscht.")
        time.sleep(0.2)

        # current_time.txt löschen
        file_path = "./data/current_time.txt"
        if os.path.exists(file_path):
            os.remove(file_path)
        print("Zeit-Datei gelöscht.")
        time.sleep(0.2)

        return "delete"
    else:
        return "cancel"


def handle_restart():
    os.system('cls' if os.name == 'nt' else 'clear')
    
    # Aurora.py neu starten
    os.system('python "./src/aurora.py"')
    # cost_manager.py neu starten
    os.system('python ./src/cost_manager.py')
    return "restart"

def handle_unknown():
    console.print("[red]Befehl nicht erkannt. Gib /help ein, um verfügbare Befehle zu sehen.[/red]")