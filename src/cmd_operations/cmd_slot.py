import os

from globals import console
from rich.panel import Panel

from prompt_toolkit import prompt
from prompt_toolkit.styles import Style

from data_handler import slot_content, save_set, load_slot


# NOTE: Refactor the code!
# read the .yaml file and display the content in a panel
# Names are determined by .yaml file and are not previously set as a string in the code


custom_style = Style.from_dict({
    '': 'fg:#87FF87',
})

def execute_slot():
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

        chars = {1: "Mia", 2: "Yu-Jun"}

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
            console.print("Wähle einen Charakter aus (1:Mia/2:Yu-Jun)\n")
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