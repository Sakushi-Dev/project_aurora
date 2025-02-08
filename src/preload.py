import os
import json
import time

from rich.console import Console

from prompt_toolkit import prompt
from prompt_toolkit.styles import Style

from secure_api_key import get_api, save_api_key

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

    if not os.path.exists("./prompts/user_spec/user_name.json") or not os.path.exists("./data/set/set_color.json"):

        print("Willkommen bei Project Aurora!\n")
        if not os.path.exists("./API/api_key.env"):
            while True:
                console.print("Gib deinen API-Key ein um fortzufahren")
                api_key = get_api()
                if api_key:
                    save_api_key(api_key)
                    time.sleep(2)
                    break
                else:
                    continue
        else:
            console.print("API-Key wurde gefunden!\n")
            time.sleep(2)
            pass
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

        user_name = {"user_name": f"{user_name}"}

        with open("./prompts/user_spec/user_name.json", "w") as file:
            json.dump(user_name, file, indent=4, ensure_ascii=False)

        time.sleep(0.5)
    
        from prompts_processing import (
        char_name as char
        )

        print(
            f"Hallo {user_name['user_name']}! Es feut mich dieses Projekt mit dir zu teilen.\n"
            "Als nächstes legst du deine beliebige Aktzentfarbe für deine Ki fest.\n\n"
            )
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
            pass
        else:
            os._exit(0)
        
        os.system('cls' if os.name == 'nt' else 'clear')

        color_choice = {"color_choice": f"{color_choice}"}

        with open("./data/set/set_color.json", "w") as file:
            json.dump(color_choice, file, indent=4, ensure_ascii=False)
        return True
    else:
        return True