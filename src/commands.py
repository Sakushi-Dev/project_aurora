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
    global slot_path

    os.system('cls' if os.name == 'nt' else 'clear')
    
    console.print(
        "[red]Achtung! Willst du wirklich Aurora.py zurücksetzen?[/red]\n"
        "[orange1]Info:[/orange1] Alle Dialoge und Einstellungen werden gelöscht.\n"
        "API-Key bleibt erhalten, kann aber auch auf Wunsch gelöscht werden.\n"
        )
    reset = ""

    reset = console.input("[red]Willst du einen Reset durchführen? (Y/N): [/red]")
    if reset.lower() == "y":
        reset = console.input("[red]Bist du dir sicher? (Y/N): [/red]")
        if reset.lower() == "y":
            # Screen leeren
            os.system('cls' if os.name == 'nt' else 'clear')

            # Slot-Content Löschen

            route_map = (
                "slot_0.json",
                "slot_1.json",
                "slot_2.json",
                "slot_3.json",
                "slot_4.json"
            )
            for route in route_map:
                path = slot_path + f"/{route}"
                with open(path, "w") as file:
                    file.write("")
            
            console.print("[orange]Lösche alle Dialoge[/orange]", end="")
            
            for i in range(1, 4):
                time.sleep(0.3)
                console.print("[red].[/red]", end="")
            
            console.print("\n[green]Alle Dialoge gelöscht.[/green]")

            #==================================================================================================

            # Kosten-Datei löschen
            for i in range(1, 6):
                save_set(slot=True, data=i)
                time.sleep(0.1)
                save_slot_cost(0.0, 0.0)

            console.print("[orange]Lösche alle Kosten-Dateien[/orange]", end="")

            for i in range(1, 4):
                time.sleep(0.3)
                console.print("[red].[/red]", end="")

            console.print("\n[green]Alle Kosten-Dateien gelöscht.[/green]")

            #==================================================================================================

            # Emotion-Datei löschen

            score = {
                "Angry_Level": 0,
                "Sad_Level": 0,
                "Affection_Level": 0,
                "Arousal_Level": 0,
                "Trust_Level": 0
            }

            for i in range(1, 6):
                save_set(slot=True, data=i)
                time.sleep(0.1)
                save_current_emo_score(score)
            
            console.print("[orange]Lösche alle Emotion-Dateien[/orange]", end="")

            for i in range(1, 4):
                time.sleep(0.3)
                console.print("[red].[/red]", end="")

            console.print("\n[green]Alle Emotion-Dateien gelöscht.[/green]")

            #==================================================================================================

            # Zeit-Datei löschen

            for i in range(1, 6):
                save_set(slot=True, data=i)
                time.sleep(0.1)
                save_msg_time("")
            
            console.print("[orange]Lösche alle Zeit-Dateien[/orange]", end="")

            for i in range(1, 4):
                time.sleep(0.3)
                console.print("[red].[/red]", end="")

            console.print("\n[green]Alle Zeit-Dateien gelöscht.[/green]")

            #==================================================================================================

            # User-Name-Datei löschen

            with open(user_name_path, "w") as file:
                file.write("")

            console.print("[orange]Lösche User-Name-Datei[/orange]", end="")
            
            for i in range(1, 4):
                time.sleep(0.3)
                console.print("[red].[/red]", end="")

            console.print("\n[green]User-Name-Datei gelöscht.[/green]")

            #==================================================================================================

            # Einstellungen-Datei auf Standard setzen

            settings = {
                "char": "Mia",
                "slot": 1,
                "max_t": 4096,
                "freq": 2,
                "imp": "off",
                "time_sense": False,
                "color": ""
            }

            for key, value in settings.items():
                save_set(**{key:True}, data=value)

            console.print("[orange]Setze Einstellungen zurück[/orange]", end="")

            for i in range(1, 4):
                time.sleep(0.3)
                console.print("[red].[/red]", end="")

            console.print("\n[green]Einstellungen zurückgesetzt.[/green]")

            #==================================================================================================

            # Fragen ob API-Key gelöscht werden soll

            api_key = console.input("[red]Willst du den API-Key löschen? (Y/N): [/red]")
            if api_key.lower() == "y":
                api_path = "./API/api_key.env"
                # API-Key löschen file
                os.remove(api_path)

                console.print("[orange]API-Key gelöscht.[/orange]")
                return "reset"

            else:
                console.print("[green]API-Key bleibt erhalten.[/green]")
                return "reset"
        else:
            return "reset"
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
    affection_value = score["AngrL_LeveLevel"]
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
    "/restart": handle_restart,
    "/slot": handle_slot,
    "/reset": handle_reset,
    "/mood": handle_mood,
    }

    command = user_input.lower().split()[0]
    if command in commands:
        if command == "/again"and history_len > 2:
            sub_user_input = True
            history, sub_user_input = commands[command](highlighted)
            history_len = get_history_length(history)
            return [sub_user_input, history, history_len]
        else:
            result = commands[command]()
    
    elif command in ["/exit", "/delete", "/restart", "/slot", "/reset"] and result in ["exit", "delete", "restart", "slot", "reset"]:
        console.print(f"Aurora.py wird in neu gestartet", end="")
        for _ in range(5, 0, -1):
            console.print(f"[red].[/red]", end="")
            time.sleep(1)
            handle_restart()
        return None
    elif command == "/config" and result == "exit":
        os.system('cls' if os.name == 'nt' else 'clear')
        history, list_msg = organize_chat_and_char()
        print_latest_messages(list_msg, highlighted=highlighted)
        return None
    elif command == "/mood":
            return None
    elif user_input.startswith("/"):
        handle_unknown()
        return None
    else:
        return True