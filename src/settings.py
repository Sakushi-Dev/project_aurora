import os
import time

from rich.console import Console

from prompts_processing import char_name as char
from data_handler import load_set, save_set
from commands import handle_restart

console = Console()

# Globale Variablen

# Highlight-Farbe
color_template = {
    1: "color(124)",    # rot
    2: "color(200)",    # pink
    3: "color(56)",     # purple
    4: "color(20)",     # blue
    5: "color(37)",     # türkis
    6: "color(118)",    # grün
    7: "color(255)"     # weiß
}

def set_config():
    global color
    '''
    Setze die Konfiguration für die KI
    '''
    # load Config
    color = load_set(color=True)
    freq = load_set(freq=True)
    imp = load_set(imp=True)
    max_t = load_set(max_t=True)
    time_sense = load_set(time_sense=True)

    os.system('cls' if os.name == 'nt' else 'clear')
    console.print(
            "\nKonfiguration:\n\n"
            f"1) Highlight-Color: [{color}]Du verwendest diese Farbe[/{color}]\n"
            f"2) Mood-Check: {freq}\n"
            f"3) Impatience-Modus: '{imp}'\n"
            f"4) Max Tokens: {max_t}\n"
            f"5) Sense of Time: {time_sense}\n"
            )
    while True:
        choice = eval(console.input("Welche Einstellung möchtest du ändern? (1-5): \nUm zurück zu kehren gebe 0 ein: "))
        
        if isinstance(choice, int):
            if choice == 0:
                return "exit"
            elif choice not in range(1, 6):
                console.print("Ungültige Eingabe!")
                continue
            else:
                break
        
    #==============================================================================================
    os.system('cls' if os.name == 'nt' else 'clear')

    if choice == 1:
        colors = "\n\n".join(
            f"{i}.) [{color_template[i]}]Für diese farbe gebe {i} ein[/{color_template[i]}]"
            for i in range(1, 8)
        )
        console.print(f"Farben die du verwenden kannst:\n\n{colors}\n")
        while True:
            choice = int(console.input("Wähle eine Farbe aus: "))
            if choice in range(1, 8):
                color_choice = color_template[choice]
                save_set(color=True, data=color_choice)
                console.print("[green]Farbe erfolgreich geändert![/green]")
                console.print("Aurora.py wird in neu gestartet", end="")
                for _ in range(5, 0, -1):
                    console.print(f"[red].[/red]", end="")
                    time.sleep(1)
                if handle_restart() == "restart":
                    break
            else:
                continue
    #==============================================================================================
    elif choice == 2:
        console.print(
            "Frequenz des Mood-Checks:\n\n"
            "Hohe Frequenz: \n"
            "    - Sendet mehrere Abfragen, verhalten wirkt sich stärker auf Emotionen aus\n"
            "    - Schlechter interpretierbar, da weniger Kontext\n\n"
            "Niedrige Frequenz: \n"
            "    - Sendet weniger Abfragen, verhalten wirkt sich schwächer auf Emotionen aus\n"
            "    - Genauere interpretation, da mehr Kontext\n\n"
            "[yellow]1 = Hoch | 4 = Niedrig[/yellow]\n"
            "1 sendet nach jedem User-Input eine Anfrage, 4 sendet nach jeder 4. User-Input eine Anfrage\n\n"
        )
        # Frequenz  1 = Hoch | 4 = Niedrig
        while True:
            choice = int(console.input("Wähle eine Frequenz aus (1-4): "))
            if choice in range(1, 5):
                save_set(freq=True, data=choice)
                console.print("[green]Frequenz erfolgreich geändert![/green]")
                console.print("Aurora.py wird in neu gestartet", end="")
                for _ in range(5, 0, -1):
                    console.print(f"[red].[/red]", end="")
                    time.sleep(1)
                if handle_restart() == "restart":
                    break
            else:
                continue
    #==============================================================================================
    elif choice == 3:
        console.print(
            "Impatience-Modus:\n\n"
            "Impatience-Modus 'on': \n"
            f"    - {char} wird ungeduldig, wenn der User nicht antwortet\n"
            f"    - {char} wird nach einer gewissen Zeit eine Nachricht senden\n"
            "    - Wartezeit liegt zwischen 1,5 und 3 Minuten\n\n"
            "Impatience-Modus 'off': \n"
            f"    - {char} wird nicht mehr ungeduldig und Wartet\n\n"
            "[red]Achtung:[/red] Diese Funktion ist eine Endlosschleife!\n"
            "Diese Funktion verursacht dauerhaft Kosten\n\n"
            "[yellow]Info:[/yellow] Bei deaktivierung wird die Schleife nicht komplett deaktiviert.\n"
            "Die dauer der Schleife wurde auf 1 Woche gesetzt\n\n"
            "[yellow]1 = Aktiviert | 2 = Deaktiviert[/yellow]\n"
        )
        # Impatience-Modus  1 = Aktiviert | 2 = Deaktiviert
        while True:
            choice = int(console.input("Wähle eine Einstellung aus (1-2): "))
            if choice in range(1, 3):
                if choice == 1:
                    choice = "neutral"
                else:
                    choice = "off"
                save_set(imp=True, data=choice)
                console.print("[green]Impatience-Modus erfolgreich geändert![/green]")
                console.print("Aurora.py wird in neu gestartet", end="")
                for _ in range(5, 0, -1):
                    console.print(f"[red].[/red]", end="")
                    time.sleep(1)
                if handle_restart() == "restart":
                    break
            else:
                continue
    #==============================================================================================
    # Input-Größe bestimmen bis history (Erinnerung) gelöscht wird Standard: 4096 Tokens
    elif choice == 4:
        console.print(
            "Max Tokens:\n\n"
            "Bestimmt die Größe des Inputs bis die History (Erinnerung) gelöscht wird\n"
            "Standard: 4096 Tokens\n\n"
        )
        while True:
            choice = int(console.input("Wähle eine Einstellung aus (4096-16384): "))
            if choice in range(4096, 16384):
                save_set(max_t=True, data=choice)
                console.print("[green]Max Tokens erfolgreich geändert![/green]")
                console.print("Aurora.py wird in neu gestartet", end="")
                for _ in range(5, 0, -1):
                    console.print(f"[red].[/red]", end="")
                    time.sleep(1)
                if handle_restart() == "restart":
                    break
            else:
                continue
    #==============================================================================================
    # Sense of Time (Zeitgefühl) bestimmen (bool) Standard: False
    elif choice == 5:
        console.print(
            "Sense of Time:\n\n"
            "Bestimmt ob das Zeitgefühl der KI aktiviert ist\n"
            f"Wenn {char} lange auf eine Antwort wartet, kann sie misstrauisch, traurig, besort oder wütend werden\n"
            "Wie stark die reaktion ist, hängt von der Zeit, Emotions-Score und dem Kontext ab\n\n"
            "[yellow]Info:[/yellow] Funktioniert nocht nicht perfekt.\n\n"
            "Standard: False\n\n"
            "[yellow]True = Aktiviert | False = Deaktiviert[/yellow]\n"
        )
        while True:
            choice = console.input("Wähle eine Einstellung aus (True/False): ")
            if choice.lower() == "true" or choice.lower() == "false":
                save_set(time_sense=True, data=choice)
                console.print("[green]Sense of Time erfolgreich geändert![/green]")
                console.print("Aurora.py wird in neu gestartet", end="")
                for _ in range(5, 0, -1):
                    console.print(f"[red].[/red]", end="")
                    time.sleep(1)
                if handle_restart() == "restart":
                    break
            else:
                continue

# Test-Code
if __name__ == "__main__":
    set_config()


    