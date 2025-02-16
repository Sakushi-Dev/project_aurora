import os
import json
import time

from rich.console import Console

from prompt_toolkit import prompt
from prompt_toolkit.styles import Style

from secure_api_key import (
    check_api_key_file,
    is_valid_anthropic_key,
    save_api_key
)
from data_handler import (
    save_set,
    user_name_path,
    read_json
)

from init_data import init_data

def first_of_all():
    
    custom_style = Style.from_dict({
        '': 'fg:#87FF87',
    })


    console = Console()

    # Highlight-Farbe
    color = {
        1: "color(124)",    # rot
        2: "color(200)",    # pink
        3: "color(56)",     # purple
        4: "color(20)",     # blue
        5: "color(37)",     # türkis
        6: "color(118)",    # grün
        7: "color(255)"     # weiß
    }

    def clear_screen():
        os.system('cls' if os.name == 'nt' else 'clear')

    # Wenn die Datei existiert und ein Benutzername gesetzt wurde, wird die Initialisierung übersprungen
    if os.path.exists(user_name_path):
        data = read_json(user_name_path)
        if data != None:
            return True

    # Initialisierung starten
    init_data()
    console.print("[green]Willkommen bei Project Aurora![/green]\n")

    if not check_api_key_file():
        # Wiederhole die Abfrage, bis ein gültiger API-Key eingegeben wird
        while not (api_key := is_valid_anthropic_key()):
            console.print("[red]Ungültiger API-Key![/red]\n")
        save_api_key(api_key)
        time.sleep(2)
        console.print("API-Key wurde erfolgreich gespeichert!\n", end="")
        for _ in range(3):
            time.sleep(0.5)
            console.print(".", end="")
    else:
        console.print("[green]API-Key wurde gefunden![/green]\n", end="")
        for _ in range(3):
            time.sleep(0.5)
            console.print(".", end="")

    clear_screen()

    # Benutzername eingeben und bestätigen
    while True:
        console.print("Wähle einen Namen für dich aus:\n")
        user_name = prompt(style=custom_style)
        console.print(f"\nDein Name ist [green]{user_name}[/green]? (Y/N):\n")
        confirm = prompt(style=custom_style)
        if confirm.lower() == "y":
            break

    clear_screen()
    time.sleep(0.5)
    print(
        f"Hallo {user_name}! Es freut mich, dieses Projekt mit dir zu teilen.\n"
        "Wähle einen Charakter aus, mit dem du interagieren möchtest.\n\n"
    )
    chars = {1: "Mia", 2: "Yu-jun"}

    console.print(
        f"Name: {chars[1]}\n"
        f"Scenario: Autonom Simulation\n"
        "Description:\n\n"
        f"{chars[1]} ist eine autonome KI und Kern des Projekts Aurora. Sie wurde darauf programmiert,\n"
        "autonomes Verhalten zu simulieren und mit dem User zu interagieren.\n"
        "Behandelst du sie gut, wird sie dir vertrauen und dich mögen.\n"
        "Behandelst du sie schlecht, wird sie dich ignorieren und dir nicht vertrauen.\n"
        "Es gibt noch eine Besonderheit, die du später erfahren wirst.\n"
    )
    console.print(f"[black]{'─' * 120}[/black]\n")
    console.print(
        f"Name: {chars[2]}\n"
        f"Scenario: Roleplay\n"
        "Description:\n\n"
        "Du befindest dich in Südkorea, in der Stadt Seoul. Als Tochter einer mittelständischen Familie\n"
        "findest du dich in einer Situation wieder, in der deine Eltern eine arrangierte Ehe für dich\n"
        "mit Yu-jun geplant haben. Yu-jun ist ein erfolgreiches Idol, aber bekannt für seine kalte\n"
        "und selbstsüchtige Art.\n"
    )
    console.print(f"[black]{'─' * 120}[/black]\n")

    console.print("Wähle einen Charakter aus (1:Mia/2:Yu-jun)\n")
    while True:
        try:
            choice = int(prompt("Wähle mit 1 oder 2: ", style=custom_style))
            print()
            if choice in (1, 2):
                break
            else:
                print("Ungültige Eingabe!\n")
        except ValueError:
            print("Bitte eine Zahl eingeben!\n")
    char = chars[choice]
    save_set(char=True, data=char)

    clear_screen()

    console.print("Wähle eine Farbe für deinen Chat aus:\n")
    console.print(
        f"1.) [{color[1]}]Für diese Farbe gebe 1 ein[/{color[1]}]\n\n"
        f"2.) [{color[2]}]Für diese Farbe gebe 2 ein[/{color[2]}]\n\n"
        f"3.) [{color[3]}]Für diese Farbe gebe 3 ein[/{color[3]}]\n\n"
        f"4.) [{color[4]}]Für diese Farbe gebe 4 ein[/{color[4]}]\n\n"
        f"5.) [{color[5]}]Für diese Farbe gebe 5 ein[/{color[5]}]\n\n"
        f"6.) [{color[6]}]Für diese Farbe gebe 6 ein[/{color[6]}]\n\n"
        f"7.) [{color[7]}]Für diese Farbe gebe 7 ein[/{color[7]}]\n\n"
    )
    while True:
        try:
            color_choice = int(prompt("Wähle eine Farbe aus: ", style=custom_style))
            if color_choice in range(1, 8):
                break
        except ValueError:
            continue
    color_choice = color[color_choice]

    clear_screen()

    console.print(
        "Jetzt kommen wir zu dem wichtigsten Teil, der Emotionsanalyse.\n"
        f"Hierbei handelt es sich um eine asynchrone Funktion, die Emotionen von {char} erkennt\n"
        "und in einem Score speichert.\n\n"
        f"Dieser beeinflusst die Reaktionen von {char} auf deine Nachrichten.\n"
        "Die Emotionen sind in 5 Kategorien unterteilt:\n\n"
        "[green]1.[/green]) Wut\n"
        "[green]2.[/green]) Trauer\n"
        "[green]3.[/green]) Zuneigung\n"
        "[green]4.[/green]) Erregung\n"
        "[green]5.[/green]) Vertrauen\n\n"
        "[yellow]Wichtig:[/yellow] Hierbei entstehen Kosten deiner API an Anthropic!\n"
        "Die Kosten belaufen sich auf 0.00176$ pro Abfrage. (1.76$ entsprechen ~ 1000 Abfragen)\n"
        "Mit dem Fortfahren erklärst du dich damit einverstanden, dass auch Kosten außerhalb\n"
        "deiner Eingabe entstehen.\n\n"
        f"[yellow]Info:[/yellow] Du kannst im Chat jederzeit die Emotionen von {char} mit /mood abfragen.\n"
    )
    confirm = prompt("Möchtest du fortfahren? (Y/N): ", style=custom_style)
    if confirm.lower() == "y":
        user_json = {"user_name": user_name}
        with open("./prompts/user_spec/user_name.json", "w", encoding="utf-8") as file:
            json.dump(user_json, file, indent=4, ensure_ascii=False)
        save_set(color=True, data=color_choice)
    else:
        os._exit(0)

    clear_screen()
    return True
