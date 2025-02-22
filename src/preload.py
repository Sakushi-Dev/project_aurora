import os
import time

from rich.console import Console
from rich.panel import Panel

from secure_api_key import (
    check_api_key_file,
    is_valid_anthropic_key,
    save_api_key
)
from data_handler import (
    save_set,
    read_json,
    write_json,
    user_name_path,
    user_gender_path
)

from task_organizer import dynamic_typing, loading_animation

from init_data import init_data

debug = False

console = Console(width=120)

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

def first_of_all():
    '''
    Funktion zur Initialisierung des Programms.
    Hier werden alle notwendigen Schritte durchgeführt, um das Programm zu starten.
    '''
    def clear_screen():
        os.system('cls' if os.name == 'nt' else 'clear')

    def init_api_key(color: dict):
        if not check_api_key_file():
            # Wiederhole die Abfrage, bis ein gültiger API-Key eingegeben wird
            while not (api_key := is_valid_anthropic_key()):
                return "Ungültiger API-Key!", color[1]
            save_api_key(api_key)
            return "API-Key wurde erfolgreich gespeichert!", color[6]
        else:
            return "API-Key wurde gefunden!", color[6]
        


    # Wenn die Datei existiert und ein Benutzername gesetzt wurde, wird die Initialisierung übersprungen
    if os.path.exists(user_name_path):
        data = read_json(user_name_path, debug=False)
        if data != None:
            if not debug:
                return True

    # Initialisierung starten
    init_data()
    aurora = ""
    with open("./src/text_files/Project Aurora.txt", "r", encoding="utf-8") as file:
        for line in file:
            aurora += line.strip()+"\n"
    wellcome_message = "Willkommen bei Project Aurora!"
    dynamic_typing(wellcome_message, mode="print", centered=True, delay=0.05, color=color[6])
    time.sleep(1)
    console.print("\n" + aurora)

    console.input("\n[yellow]Drücke Enter, um fortzufahren...[/yellow]")

    clear_screen()

    # API-Key initialisieren
    message, status_color = init_api_key(color)
    loading_animation("API-Key", wait=3, status=True, color=status_color)
    time.sleep(3)

    clear_screen()

    # Benutzername eingeben und bestätigen
    while True:
        choice_name = "Wähle einen Namen für dich aus\n(Dieser wird im Chat verwendet, kann aber später geändert werden)"
        user_name = dynamic_typing(choice_name, mode="input", centered=True, delay=0.05, color=color[6])
        
        check_name = f"Dein Name ist {user_name}?"
        confirm = dynamic_typing(check_name, mode="input", centered=True, choice=True, delay=0.05, color=color[6])
        if confirm.lower() == "y":
            # Geschlecht des Benutzers abfragen
            while True:
                choice_gender = "Bist du männlich, weiblich oder divers?\n(Antworte mit M, W oder D)"
                gender = dynamic_typing(choice_gender, mode="input", centered=True, delay=0.05, color=color[6])
                if gender.lower() in ("m", "w", "d"):
                    break
                else:
                    clear_screen()
                    dynamic_typing("Ungültige Eingabe!", mode="print", centered=True, delay=0.05, color=color[1])
            break
        clear_screen()

    clear_screen()
    time.sleep(0.5)
    print(f"Wähle einen Charakter aus, mit dem du interagieren möchtest.\n\n")
    chars = {1: "Mia", 2: "Yu-jun"}

    console.print(
    f"[{color[5]}]Name: {chars[1]}\n"
    f"Scenario: Autonome Simulation[/{color[5]}]\n"
    f"{'-'*40}\n"
    "Beschreibung:\n\n"
    f"{chars[1]} ist eine hochentwickelte KI und der Kern des Projekts Aurora. "
    "Sie wurde entwickelt, um autonomes Verhalten zu simulieren und in natürlicher Weise mit dir zu interagieren.\n\n"
    "Dein Umgang mit ihr beeinflusst ihr Verhalten:\n"
    "- Behandelst du sie mit Respekt, wird sie dir vertrauen und dich schätzen.\n"
    "- Behandelst du sie schlecht, wird sie auf Distanz gehen und dir nicht vertrauen.\n"
    "\nAktive Funktionen:\n"
    f"[{color[6]}]Emotionsanalyse | Persönlichkeitsentwicklung | Zeitwahrnehmung | Deep Memory[/{color[6]}]\n"
    )

    console.print(f"[black]{'─' * 120}[/black]\n")

    console.print(
    f"[{color[5]}]Name: {chars[2]}\n"
    f"Scenario: Roleplay (Frühe Entwicklungsphase)[/{color[5]}]\n"
    f"{'-'*40}\n"
    "Beschreibung:\n\n"
    "Du befindest dich in Südkorea, in der pulsierenden Metropole Seoul. "
    "Als Tochter einer wohlhabenden, aber traditionsbewussten Familie stehst du vor einer Herausforderung: "
    "Deine Eltern haben eine arrangierte Ehe für dich geplant – mit Yu-jun, einem gefeierten Idol, "
    "das für seine kühle und egozentrische Art bekannt ist.\n\n"
    "⚠ Dieses Szenario befindet sich noch in einer frühen Entwicklungsphase. "
    "Erwarte mögliche Anpassungen und Verbesserungen in zukünftigen Versionen.\n"
    f"[{color[6]}]Emotionsanalyse | Persönlichkeitsentwicklung | Deep Memory[/{color[6]}]\n"
    )
    console.print(f"[black]{'─' * 120}[/black]\n")

    choice_char = f"Wähle einen Charakter aus\n(Antworte mit 1 für {chars[1]} und 2 für {chars[2]})"
    while True:
        try:
            choice = int(dynamic_typing(choice_char, mode="input", centered=True, delay=0.05, color=color[6]))
            if choice in (1, 2):
                break
            else:
                print("Ungültige Eingabe!\n")
        except ValueError:
            print("Bitte eine Zahl eingeben!\n")
    char = chars[choice]
    save_set(char=True, data=char)

    clear_screen()

    dynamic_typing("Demo der Farben", mode="print", centered=True, delay=0.05, color=color[6])
    time.sleep(0.5)

    color_demo = []
    for i in range(1, 8):
        color_demo.append(f"[{color[i]}]Hallo ich bin {char}.[/{color[i]}]")
    
    for i, demo in enumerate(color_demo, 1):
        console.print(f"{i}.)")
        console.print(
            Panel(
            demo,
            title=f"[bold {color[i]}]{char}[/bold {color[i]}]",
            width=50,
            expand=True,
            border_style="white",
            )
        )
        console.print(f"[black]{'─' * 120}[/black]\n")
    
    while True:
        try:
            color_choice = int(dynamic_typing("Wähle eine Farbe aus (1-7)\n(Kann später geändert werden)", mode="input", centered=True, delay=0.05, color=color[6]))
            if color_choice in range(1, 8):
                break
        except ValueError:
            continue
    color_choice = color[color_choice]

    clear_screen()

    while True:
        console.print(
            "Fast geschafft!\n\n"
            f"[{color[5]}]Hinweis zu Command-Mode:[/{color[5]}]\n"
            "Um in den Command-Mode zu wechseln, füge ein [red]/[/red] vor deinen Befehl ein.\n"
            "Nach eingabe des slash werden dir alle verfügbaren Befehle angezeigt.\n\n"
            f"[{color[5]}]Beispiel:[/{color[5]}] [red]/[/red][green]mood[/green]\n"
            "Dieser Befehl zeigt dir die aktuelle Stimmung deines Charakters in einem Score an.\n"
        )
        confirm = dynamic_typing(
            "Bist du bereit für dein Abenteuer?",
            mode="input",
            centered=True,
            choice=True,
            delay=0.05,
            color=color[6]
            )
        if confirm.lower() == "y":
            # Speichern aller Daten
            user_json = {"user_name": user_name}
            gender_map = {"m": "männlich", "w": "weiblich", "d": "divers"}
            gender_json = {"user_gender": gender_map[gender.lower()]}

            write_json(user_name_path, user_json)
            write_json(user_gender_path, gender_json)
            save_set(color=True, data=color_choice)

            if char == "Mia":
                save_set(time_sense=True, data=True)

            clear_screen()
            return True
        else:
            confirm = dynamic_typing(
            "Willst du wirklich abbrechen?",
            mode="input",
            centered=True,
            choice=True,
            delay=0.05,
            color=color[1]
            )
            if confirm.lower() == "y":
                os._exit(0)
            else:
                clear_screen()
                continue

        

#test
if debug:
    first_of_all()
