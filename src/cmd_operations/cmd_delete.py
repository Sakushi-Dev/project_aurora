import os
import time

from globals import console
from rich.panel import Panel

from prompt_toolkit import prompt
from prompt_toolkit.styles import Style

from data_handler import (
    get_slot, save_set, slot_content, save_slot_cost, save_current_emo_score, save_msg_time
)
from data_handler import slot_path, char_memory_path

custom_style = Style.from_dict({
    '': 'fg:#87FF87',
})


def execute_delete():
    # Löscht im aktiven slot den aktuellen Chatverlauf
    global slot_path
    delete = console.input("[red]Sind Sie sicher, dass Sie den Chatverlauf löschen möchten? (Y/N): [/red]")
    if delete.lower() == "y":
        # Screen leeren
        os.system('cls' if os.name == 'nt' else 'clear')

        slot= get_slot()
        dialog_path = slot_path + f"/slot_{slot-1}.json"
        mem_path = char_memory_path + f"/memory_analysis_slot_{slot-1}.jsonl"

        console.print("[red]Löschvorgang darf nicht unterbrochen werden![/red]")

        # File-Backup löschen
        with open(dialog_path, "w") as file:
            file.write("")
        print(f"Dialog in Slot {slot} gelöscht.")
        time.sleep(0.2)

        #Prüfen ob Memory-File vorhanden ist
        if os.path.isfile(mem_path):
            # Memory- file löschen
            os.remove(mem_path)
            print(f"Memory in Slot {slot} gelöscht.")

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