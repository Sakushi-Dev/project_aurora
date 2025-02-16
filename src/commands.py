import os
import re
import time

from rich.console import Console

from rich.panel import Panel

from prompt_toolkit import prompt
from prompt_toolkit.styles import Style

# History-Manager-Import:
from history_manager import (
    replay_last_interaction
)

from task_organizer import (
    print_latest_messages
)

from data_handler import (
    read_json,
    user_name_path,
    load_history,
    get_slot,
    slot_path,
    save_set,
    slot_content,
    load_slot,
    save_current_emo_score,
    save_slot_cost,
    save_msg_time
)

custom_style = Style.from_dict({
    '': 'fg:#87FF87',
})

# Rich-Console-Objekt:
console = Console(width=120)



def handle_exit():
    console.print("Chat beendet. Tschüss!")
    return "exit"

def handle_again(highlighted):

    # lösche Letze zwei Einträge und gbe die letzte User-Nachricht zurück
    last_user_message = replay_last_interaction()
    if last_user_message:

        # Clear Screen
        os.system('cls' if os.name == 'nt' else 'clear')

        # Alte Usernachricht anzeigen
        user_input = last_user_message["content"]

        data= read_json(user_name_path)
        user = data["user_name"]

        slot = get_slot()

        # History laden und anzeigen
        history, list_msg = load_history(slot)
        print_latest_messages(list_msg, highlighted=highlighted)

        # User-Nachricht anzeigen
        highlighted_text = re.sub(
            r"\*\s*(.*?)\*",
            r"[orange1]\1[/orange1]",
            user_input,
            flags=re.DOTALL
        )
        console.print(
            Panel(
                highlighted_text,
                title=f"[bold]{user}[/bold]",
                expand=True,
                border_style="white"
                )
            )
        print()
        
    return history, user_input

def handle_slot():
    os.system('cls' if os.name == 'nt' else 'clear')
    
    slot_content_list = None
    slot_content_list = slot_content()

    proven_slots = []
    for content in slot_content_list:
        for key, value in content.items():
            key = key.replace("slot_", "")
            key = int(key)
            key = key + 1
            #prüfen ob NONE wete in der liste sind
            val = value[0]
            if val is not None:
                proven_slots.append(key)
                console.print(
                    Panel(
                    f"Charakter: {value[0]}\nErstellt: {value[1]}\nDialog-Länge: {value[2]}",
                    title=f"[bold green]Slot: {key}[/bold green]",
                    width=60,
                    expand=True,
                    border_style="white"
                    )
                )
                console.print(f"[black]{'─' * 120}[/black]")
            else:
                console.print(
                    Panel(
                    "Dieser Slot ist leer.\n\n",
                    title=f"[bold green]Slot: {key}[/bold green]",
                    width=60,
                    expand=True,
                    border_style="white"
                    )
                )
                console.print(f"[black]{'─' * 120}[/black]")

    
    
    console.print("[green]Du kannst einen Chatverlauf auswählen oder einen neuen Chat starten.[/green]\n")
    slot_choice = int(console.input("Wähle einen Slot aus: "))

    os.system('cls' if os.name == 'nt' else 'clear')
    
    if not slot_choice in proven_slots:
        save_set(slot=True, data=slot_choice)

        chars = {1: "Mia", 2: "Yu-jun"}

        console.print(
            f"\nName: {chars[1]}\n"
            f"Scenario: Autonom Simulation\n"
            "Description:\n\n"
            f"{chars[1]} ist ein Autonome KI, der Kern des Projekts Aurora. Sie ist darauf programmiert\n"
            "Autonomes Verhalten zu Simulieren und mit dem User zu interagieren.\n"
            "Behandeslst du sie gut, wird sie dir vertrauen und dich mögen.\n"
            "Behandelst du sie schlecht, wird sie dich ignorieren und dir nicht vertrauen.\n"
            "Es gibt noch eine Besonderheit, die du später erfahren wirst.\n"
        )

        console.print(f"[black]{'─' * 120}[/black]\n")
        console.print(
            f"Name: {chars[2]}\n"
            f"Scenario: Roleplay\n"
            "Description:\n\n"
            "Du befindest dich in Südkorea, in der Stadt Seoul. Als Tochter einer mittelständischen Familie\n"
            "findest du dich in einer situtaion wieder, in der deine Eltern eine arrangierte Ehe für dich\n"
            "mit Yu-jun geplant haben. Yu-jun ist ein erfolgreiches Idol, aber bekannt für seine kalte\n"
            "und selbstsüchtige Art.\n"         
        )
        console.print(f"[black]{'─' * 120}[/black]\n")

        while True:
            # wählbaren Charakter anzeigen
            console.print("Wähle einen Charakter aus (1:Mia/2:Yu-jun)\n")
            choice = int(prompt("Wähle mit 1 oder 2: ", style=custom_style))
            print()
            if choice in range(1, 3):
                char = chars[choice]
                save_set(char=True, data=char)
                return "slot"
            else:
                print("Ungültige Eingabe!\n")
                continue
    else:
        save_set(slot=True, data=slot_choice)
        char,_,_ = load_slot(slot_choice)
        save_set(char=True, data=char)
        console.print(f"Chat mit [green]{char.title()}[/green] wird fortgesetzt.")
        return "slot"


def handle_delete():
    # Löscht im aktiven slot den aktuellen Chatverlauf
    global slot_path
    delete = console.input("[red]Sind Sie sicher, dass Sie den Chatverlauf löschen möchten? (Y/N): [/red]")
    if delete.lower() == "y":
        # Screen leeren
        os.system('cls' if os.name == 'nt' else 'clear')

        slot= get_slot()
        path = slot_path + f"/slot_{slot-1}.json"

        console.print("[red]Löschvorgang darf nicht unterbrochen werden![/red]")

        # File-Backup löschen
        with open(path, "w") as file:
            file.write("")
        print(f"Dialog in Slot {slot} gelöscht.")
        time.sleep(0.2)

        # costs.py löschen
        save_slot_cost(0.0, 0.0)
        print("Kosten-Datei gelöscht.")
        time.sleep(0.2)

        # emotion_score.json löschen
        score = {
            "Angry_Level": 0,
            "Sad_Level": 0,
            "Affection_Level": 0,
            "Arousal_Level": 0,
            "Trust_Level": 0
            }
        save_current_emo_score(score)
        print("Emotion-Datei gelöscht.")
        time.sleep(0.2)

        # current_time.txt löschen
        save_msg_time("")
        print("Zeit-Datei gelöscht.")
        time.sleep(0.2)

        # Fragen ob Neuer chat gestartet werden soll mit aktuellem Charakter oder anderem Charakter
        new_chat = console.input("[green]Neuen Chat starten mit aktuellem Charakter? (Y/N): [/green]")
        if new_chat.lower() == "y":
            return "delete"
        else:
            while True:
                dialog_choice= console.input("[green]Bereits vorhandenen Dialog wählen? (Y/N): [/green]")
            
                if dialog_choice.lower() == "y":
                    # Slot-Content anzeigen
                    slot_content_list = None
                    slot_content_list = slot_content()
                    os.system('cls' if os.name == 'nt' else 'clear')

                    proven_slots = []
                    for content in slot_content_list:
                        for key, value in content.items():
                            key = key.replace("slot_", "")
                            key = int(key)
                            key = key + 1
                            #prüfen ob NONE wete in der liste sind
                            val = value[0]
                            if val is not None:
                                proven_slots.append(key)
                                console.print(
                                    Panel(
                                    f"Charakter: {value[0]}\nErstellt: {value[1]}\nDialog-Länge: {value[2]}",
                                    title=f"[bold green]Slot: {key}[/bold green]",
                                    width=60,
                                    expand=True,
                                    border_style="white"
                                    )
                                )
                                console.print(f"[black]{'─' * 120}[/black]")
                            else:
                                console.print(
                                    Panel(
                                    "Dieser Slot ist leer.\n\n",
                                    title=f"[bold green]Slot: {key}[/bold green]",
                                    width=60,
                                    expand=True,
                                    border_style="white"
                                    )
                                )
                                console.print(f"[black]{'─' * 120}[/black]")
                    if proven_slots:
                        while True:
                            slot_choice = int(console.input("[green]Wähle einen leeren Slot aus: [/green]"))
                            if slot_choice in proven_slots:
                                save_set(slot=True, data=slot_choice)
                                console.print(f"[green]Chat wird fortgesetzt.[/green]")
                                break 
                            else:
                                print("Ungültige Eingabe!")
                                continue
                        return "delete"
                    else:
                        console.print("Keine Chatverläufe vorhanden.")
                        save_set(slot=True, data=1)
                        continue
     
                else:
            
                    while True:
                        # wählbaren Charakter anzeigen
                        console.print("Wähle einen Charakter aus (1:Mia/2:Yu-jun)\n")
                        while True:
                            choice = int(prompt("Wähle mit 1 oder 2: ", style=custom_style))
                            print()
                            if choice in range(1, 3):
                                break
                            else:
                                print("Ungültige Eingabe!\n")
                                continue

                        chars = {1: "Mia", 2: "Yu-jun"}
                        
                        if choice == 1:
                            char = chars[1]
                            save_set(char=True, data=char)
                        else:
                            char = chars[2]
                            save_set(char=True, data=char)
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

def handle_reset():
    from init_data import spit_path
    from data_handler import (
        set_path,
        slot_path,
        emo_score_path,
        cost_path,
        last_msg_time_path,
        user_path
    )

    # Formatiere zu relativen Order-Pfaden um alle Dateien innerhalb des Ordners zu löschen
    costs_p, _ = spit_path(cost_path)
    last_p, _ = spit_path(last_msg_time_path)

    # Nur diese Datei wird zum Löschen benötigt
    emo_p = emo_score_path

    # Relativer Pfad zu den Set-Dateien
    set_p = set_path

    # Relativer Pfad zu den User-Dateien
    user_p = user_path

    # Relativer Pfad zu den Slot-Dateien
    slot_p = slot_path

    os.system('cls' if os.name == 'nt' else 'clear')
    
    console.print(
        "[red]Achtung! Willst du wirklich [orange1]Aurora[/orange1] zurücksetzen?[/red]\n"
        "[orange1]Info:[/orange1] Alle Dialoge und Einstellungen werden gelöscht.\n"
        "API-Key bleibt erhalten, kann aber auch auf Wunsch gelöscht werden.\n"
        )
    reset = ""

    reset = console.input("[red]Willst du einen Reset durchführen? (Y/N): [/red]")
    if reset.lower() == "y":

        # Sicherheitsabfrage
        reset = console.input("[red]Bist du dir sicher? (Y/N): [/red]")
        if reset.lower() == "y":

            # Screen leeren
            os.system('cls' if os.name == 'nt' else 'clear')


            route_map = {
                "Kosten der Dialoge": costs_p, 
                "Zeiten für 'Impatience'": last_p,
                "Emotions-Score Daten": emo_p,
                "Settings": set_p,
                "User-Data": user_p,
                "Chat-Verläufe": slot_p
            }
            
            # Löschen der Dateien
            for key, value in route_map.items():
                try:

                    if os.path.isdir(value):
                        for root, dirs, files in os.walk(value, topdown=False):
                            for name in files:
                                os.remove(os.path.join(root, name))
                            for name in dirs:
                                os.rmdir(os.path.join(root, name))
                        os.rmdir(value)
                    elif os.path.isfile(value):
                        os.remove(value)

                    console.print(f"\n[orange1]Lösche der {key} wird durchgeführt[/orange1]", end="")
                    for i in range(0, 3):
                        console.print(f"[red].[/red]", end="")
                        time.sleep(0.7)
                    console.print(f"\n[green]{key} gelöscht.[/green]")
                except FileNotFoundError:
                    console.print(f"\n[red]{key} nicht gefunden.[/red]")

            # Löschen von '__pycache__'
            try:
                os.system("rm -r ./src/__pycache__")
                console.print("\n[green]__pycache__ gelöscht.[/green]")
            except FileNotFoundError:
                console.print("\n[red]__pycache__ nicht gefunden.[/red]")
                pass

            console.print("[orange]Löschvorgang abgeschlossen.[/orange]")
            
            #==================================================================================================

            # Fragen ob API-Key gelöscht werden soll

            api_key = console.input("[red]Willst du den API-Key löschen? (Y/N): [/red]")
            if api_key.lower() == "y":
                # API-Key löschen file
                os.remove("./API/api_key.env")
                os.rmdir("./API")

                console.print("[orange]API-Key gelöscht.[/orange]")

            else:
                console.print("[green]API-Key bleibt erhalten.[/green]")
                
            
            os.system('cls' if os.name == 'nt' else 'clear')

            while True:
                choice = console.input(
                    "[green]Gebe [orange1]1[/orange1] ein, um Aurora neu zu starten"
                    "\nWenn du beenden möchtest, gebe [orange1]2[/orange1] ein: [/green]"
                    )
                if choice == "1":
                    return "reset"
                elif choice == "2":
                    os._exit(0)
                else:
                    console.print("[red]Ungültige Eingabe![/red]")
                    continue
        else:
            return "cancel"
    else:
        return "cancel"

def handle_unknown():
    console.print("[red]Befehl nicht erkannt. Gib /help ein, um verfügbare Befehle zu sehen.[/red]")

def handle_mood():
    from tabulate import tabulate
    from data_handler import load_current_emo_score

    score = load_current_emo_score()

    angry_value = score["Angry_Level"]
    sad_value = score["Sad_Level"]
    affection_value = score["Affection_Level"]
    arousal_value = score["Arousal_Level"]
    trust_value = score["Trust_Level"]

    show_mood = [["Emotionen", "Score"],
                ["Wut", f"{angry_value}"],
                ["Trauer", f"{sad_value}"],
                ["Zuneigung", f"{affection_value}"],
                ["Erregung", f"{arousal_value}"],
                ["Vertrauen", f"{trust_value}"]
                ]

    console.print(tabulate(show_mood, headers="firstrow", tablefmt="grid"), "\n")

def command_dispatcher(user_input: str, highlighted:str, history_len:int):
    # Settings-Import:
    from settings import set_config
    from history_manager import (
    get_history_length,
    organize_chat_and_char
    )
    
    commands = {
    "/exit": handle_exit,
    "/config": set_config,
    "/again": handle_again,
    "/delete": handle_delete,
    "/slot": handle_slot,
    "/reset": handle_reset,
    "/mood": handle_mood,
    }

    command = user_input.lower().split()[0]
    if command in commands:
        if command == "/again"and history_len > 2:
            sub_user_input = None
            history, sub_user_input = commands[command](highlighted)
            history_len = get_history_length(history)
            return [sub_user_input, history, history_len]
        else:
            result = commands[command]()
    
    if command in ["/exit", "/delete", "/slot", "/reset"] and result in ["exit", "delete", "slot", "reset"] or command == "/restart":
        console.print(f"Aurora.py wird in neu gestartet", end="")
        for _ in range(5, 0, -1):
            console.print(f"[red].[/red]", end="")
            time.sleep(1)
        handle_restart()
    elif command == "/config" and result == "exit":
        os.system('cls' if os.name == 'nt' else 'clear')
        history, list_msg = organize_chat_and_char()
        print_latest_messages(list_msg, highlighted=highlighted)
        return None # Falls config beendet wird, soll der Chat-Loop von vorne starten
    elif command == "/mood":
        return None # Chat-Loop startet von vorne
    elif user_input.startswith("/"):
        handle_unknown()
        return None # Chat-Loop startet von vorne
    else:
        return True # Damit der Chat-Loop weiter läuft