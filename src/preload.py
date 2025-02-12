import os
import json
import time

from rich.console import Console

from prompt_toolkit import prompt
from prompt_toolkit.styles import Style

from secure_api_key import (
    check_api_key_folder,
    check_api_key_file,
    is_valid_anthropic_key,
    save_api_key
)
from data_handler import (
    save_set,
    load_user_char_name
)

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

    user_name = load_user_char_name(user=True)

    if user_name == None:

        console.print("[green]Willkommen bei Project Aurora![/green]\n")
        if check_api_key_folder() == False:
            while True:
                api_key = is_valid_anthropic_key()
                if api_key:
                    save_api_key(api_key)
                    time.sleep(2)
                    break
                else:
                    console.print("[red]Ungültiger API-Key![/red]\n")
                
            api_check = check_api_key_file()
            if api_check:
                console.print("API-Key wurde erfolgreich gespeichert!\n", end="")
            for i in range(3):
                time.sleep(0.5)
                console.print(".", end="")
        else:
            console.print("[green]API-Key wurde gefunden![/green]\n", end="")
            for i in range(3):
                time.sleep(0.5)
                console.print(".", end="")
        
        os.system('cls' if os.name == 'nt' else 'clear')
        while True:
            console.print("Wähle einen Namen für dich aus:\n")
            user_name = prompt(style=custom_style)
            console.print(f"\nDein Name ist [green]{user_name}[/green]? (Y/N):\n ")
            confirm = prompt(style=custom_style)
            if confirm.lower() == "y":
                break
            else:
                continue
        os.system('cls' if os.name == 'nt' else 'clear')
        # User-Name wird erst am Ende gespeichert

        time.sleep(0.5)

        print(
            f"Hallo {user_name}! Es feut mich dieses Projekt mit dir zu teilen.\n"
            "Wähle einen Charakter aus, mit dem du interagieren möchtest.\n\n"
            )
        chars = {
            1: "Mia",
            2: "Yu-jun"
        }

        console.print(
            f"Name: {chars[1]}\n"
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

        console.print("Wähle einen Charakter aus (1:Mia/2:Yu-jun)\n")
        while True:
            choice = int(prompt("Wähle mit 1 oder 2: ", style=custom_style))
            print()
            if choice in range(1, 3):
                break
            else:
                print("Ungültige Eingabe!\n")
                continue
        
        if choice == 1:
            char = chars[1]
            save_set(char=True, data=char)
        else:
            char = chars[2]
            save_set(char=True, data=char)

        os.system('cls' if os.name == 'nt' else 'clear')

        console.print("Wähle eine Farbe für deinen Chat aus:\n")

        console.print(
            f"1.) [{color[1]}]Für diese farbe gebe 1 ein[/{color[1]}]\n\n"
            f"2.) [{color[2]}]Für diese farbe gebe 2 ein[/{color[2]}]\n\n"
            f"3.) [{color[3]}]Für diese farbe gebe 3 ein[/{color[3]}]\n\n"
            f"4.) [{color[4]}]Für diese farbe gebe 4 ein[/{color[4]}]\n\n"
            f"5.) [{color[5]}]Für diese farbe gebe 5 ein[/{color[5]}]\n\n"
            f"6.) [{color[6]}]Für diese farbe gebe 6 ein[/{color[6]}]\n\n"
            f"7.) [{color[7]}]Für diese farbe gebe 7 ein[/{color[7]}]\n\n"
        )
        while True:
            color_choice = int(prompt("Wähle eine Farbe aus: ", style=custom_style))
            if color_choice in range(1, 8):
                break
            else:
                continue
        
        color_choice = color[color_choice]

        os.system('cls' if os.name == 'nt' else 'clear')

        console.print(
            "Jetzt kommen wir zu dem wichtigsten Teil, der Emotionsanalyse.\n"
            f"Hierbei handelt es sich um eine Asynchrone Funktion, die Emotionen von {char} erkennt\n"
            "und in einem Score speichert.\n\n"
            f"Dieser beeinflust die Reaktionen von {char} auf deine Nachrichten.\n"
            "Die Emotionen sind in 5 Kategorien unterteilt:\n\n"
            "[green]1.[/green]) Wut\n"
            "[green]2.[/green]) Trauer\n"
            "[green]3.[/green]) Zuneiung\n"
            "[green]4.[/green]) Erregung\n"
            "[green]5.[/green]) Vertrauen\n\n"
            "[yellow]Wichtig:[/yellow] Hierbei entstehen kosten deiner API an Anthropic!\n"
            "Die Kosten belaufen sich auf 0.00176$ pro Abfrage. (1.76$ entsprechen ~ 1000 Abfragen)\n"
            "Mit dem fortsetzen erklärst du dich damit einverstanden, "
            "dass auch kosten auserhalb deiner eingabe entstehen.\n\n"
            f"[yellow]Info:[/yellow] Du kannst im Chat jederzeit die Emotionen von {char} mit /mood abfragen.\n"
        )
        confirm = prompt("Möchtest du fortfahren? (Y/N): ", style=custom_style)
        if confirm.lower() == "y":

            user_name = {"user_name": f"{user_name}"}
            with open("./prompts/user_spec/user_name.json", "w") as file:
                json.dump(user_name, file, indent=4, ensure_ascii=False)
                
                save_set(color=True, data=color_choice)
            pass
        else:
            os._exit(0)
        
        os.system('cls' if os.name == 'nt' else 'clear')

        return True
    else:
        return True