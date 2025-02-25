import os
import time

from rich.console import Console
from rich.panel import Panel
from rich.columns import Columns

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
    user_gender_path,
    user_language_path
)

from task_organizer import dynamic_typing, loading_animation

from init_data import init_data

debug = False

console = Console(width=120)

# Highlight-Farbe
color = {
    1: "color(124)",    # red
    2: "color(200)",    # pink
    3: "color(56)",     # purple
    4: "color(20)",     # blue
    5: "color(37)",     # turquoise
    6: "color(45)",     # neon blue
    7: "color(118)",    # green
    8: "color(255)"     # white
}

def first_of_all():
    '''
    Function to initialize the program.
    Here all necessary steps are taken to start the program.
    '''
    def clear_screen():
        os.system('cls' if os.name == 'nt' else 'clear')

    def init_api_key(color: dict):
        if not check_api_key_file():
            # Repeat the query until a valid API key is entered
            while not (api_key := is_valid_anthropic_key()):
                console.print("\rPlease try again.", end="\r", style="yellow")
                for i in range(5, 0, -1):
                    console.print(f"Please try again. {i}", end="\r", style="yellow")
                    time.sleep(1)
                clear_screen()
            save_api_key(api_key)
            return "API key was successfully saved!", color[7]
        else:
            return "API key was found!", color[7]
        


    # If the file exists and a username is set, initialization is skipped
    if os.path.exists(user_name_path):
        data = read_json(user_name_path, debug=False)
        if data != None:
            if not debug:
                return True

    # Start initialization
    init_data()
    aurora = ""
    with open("./src/text_files/Project Aurora.txt", "r", encoding="utf-8") as file:
        for line in file:
            aurora += line.strip()+"\n"
    wellcome_message = "Welcome to Project Aurora!"
    dynamic_typing(wellcome_message, mode="print", centered=True, delay=0.05, color=color[7])
    time.sleep(1)
    console.print("\n" + aurora)

    console.input("\n[yellow]Press Enter to continue...[/yellow]")

    clear_screen()

    # Initialize API key
    message, status_color = init_api_key(color)
    loading_animation("API key", wait=3, status=True, color=status_color)
    time.sleep(3)

    clear_screen()

    invalid_input = lambda: dynamic_typing("Invalid input!", mode="print", centered=True, delay=0.05, color=color[1])

    # Enter and confirm username
    while True:
        choice_name = "Choose a name for yourself\n(This will be used in the chat but can be changed later)"
        user_name = dynamic_typing(choice_name, mode="input", centered=True, delay=0.05, color=color[7])
        
        check_name = f"Your name is {user_name}?"
        confirm = dynamic_typing(check_name, mode="input", centered=True, choice=True, delay=0.05, color=color[7])
        if confirm.lower() == "y":
            break
    # Ask for the user's gender
    while True:
        choice_gender = "Are you male, female or diverse?\n(Answer with M, F or D)"
        gender = dynamic_typing(choice_gender, mode="input", centered=True, delay=0.05, color=color[7])
        if gender.lower() in ("m", "f", "d"):
            break
        else:
            invalid_input()
    # Ask for the user's language           
    while True:
        language = "Choose your language for the chat\n(Answer with EN or DE)"
        lang = dynamic_typing(language, mode="input", centered=True, delay=0.05, color=color[7])
        if lang.lower() in ("en", "de"):
            break
        else:
            invalid_input()
            
    clear_screen()

    clear_screen()
    time.sleep(0.5)
    print(f"Choose a character you want to interact with.\n\n")
    chars = {1: "Mia", 2: "Yu-jun"}

    console.print(
    f"[{color[5]}]Name: {chars[1]}\n"
    f"Scenario: Autonomous Simulation[/{color[5]}]\n"
    f"{'-'*40}\n"
    "Description:\n\n"
    f"{chars[1]} is a highly advanced AI and the core of Project Aurora. "
    "It was developed to simulate autonomous behavior and interact with you in a natural way.\n\n"
    "Your interaction with it influences its behavior:\n"
    "- If you treat it with respect, it will trust and appreciate you.\n"
    "- If you treat it badly, it will distance itself and not trust you.\n"
    "\nActive functions:\n"
    f"[{color[7]}]Emotion Analysis | Personality Development | Sense of Time | Deep Memory[/{color[7]}]\n"
    )

    console.print(f"[black]{'─' * 120}[/black]\n")

    console.print(
    f"[{color[5]}]Name: {chars[2]}\n"
    f"Scenario: Roleplay (Early Development Phase)[/{color[5]}]\n"
    f"{'-'*40}\n"
    "Description:\n\n"
    "You are in South Korea, in the bustling metropolis of Seoul. "
    "As the daughter of a wealthy but traditional family, you face a challenge: "
    "Your parents have arranged a marriage for you – with Yu-jun, a celebrated idol known for his cool and egocentric nature.\n\n"
    "⚠️  This scenario is still in an early development phase. "
    "Expect possible adjustments and improvements in future versions.\n"
    "\nActive functions:\n"
    f"[{color[7]}]Emotion Analysis | Personality Development | Deep Memory[/{color[7]}]\n"
    )
    console.print(f"[black]{'─' * 120}[/black]\n")

    choice_char = f"Choose a character\n(Answer with 1 for {chars[1]} and 2 for {chars[2]})"
    while True:
        try:
            choice = int(dynamic_typing(choice_char, mode="input", centered=True, delay=0.05, color=color[7]))
            if choice in (1, 2):
                break
            else:
                print("Invalid input!\n")
        except ValueError:
            print("Please enter a number!\n")
    char = chars[choice]
    save_set(char=True, data=char)

    clear_screen()

    dynamic_typing("Color Demo", mode="print", centered=True, delay=0.05, color=color[7])
    time.sleep(0.5)

    color_demo = []
    # Generate panels
    for i in range(1, 8, 2):  # Steps of 2 to form pairs
        panel1 = Panel(
            f"[{color[i]}]Hello, I am {char}.[/{color[i]}]",
            title=f"[bold {color[i]}]{char}[/bold {color[i]}]",
            width=50,
            expand=True,
            border_style="white",
        )

        panel2 = Panel(
            f"[{color[i+1]}]Hello, I am {char}.[/{color[i+1]}]",
            title=f"[bold {color[i+1]}]{char}[/bold {color[i+1]}]",
            width=50,
            expand=True,
            border_style="white",
        )

        # Display panels side by side
        console.print(Columns([f"{' '*2}{i}.) ", panel1, f"{' '*2}{i+1}.) ", panel2, f"{' '*6}"]))
        console.print(f"[black]{'─' * 120}[/black]\n")
    
    while True:
        try:
            color_choice = int(dynamic_typing("Choose a color (1-8)\n(Can be changed later)", mode="input", centered=True, delay=0.05, color=color[7]))
            if color_choice in range(1, 9):
                break
        except ValueError:
            continue
    color_choice = color[color_choice]

    clear_screen()

    while True:
        console.print(
            "Almost done!\n\n"
            f"[{color[5]}]Note on Command Mode:[/{color[5]}]\n"
            "To switch to Command Mode, add a [red]/[/red] before your command.\n"
            "After entering the slash, all available commands will be displayed.\n\n"
            f"[{color[5]}]Example:[/{color[5]}] [red]/[/red][green]mood[/green]\n"
            "This command shows you the current mood of your character in a score.\n"
        )
        confirm = dynamic_typing(
            "Are you ready?",
            mode="input",
            centered=True,
            choice=True,
            delay=0.05,
            color=color[7]
            )
        if confirm.lower() == "y":
            # Save all data
            user_json = {"user_name": user_name}

            gender_map = {"m": "male", "f": "female", "d": "diverse"}
            gender_json = {"user_gender": gender_map[gender.lower()]}

            language_map = {"en": "english", "de": "german"}
            language_json = {"language": language_map[lang.lower()]}

            write_json(user_name_path, user_json)
            write_json(user_gender_path, gender_json)
            write_json(user_language_path, language_json)
            save_set(color=True, data=color_choice)

            if char == "Mia":
                save_set(time_sense=True, data=True)

            clear_screen()
            return True
        else:
            confirm = dynamic_typing(
            "Do you really want to cancel?",
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

        
# ======================================================================================================================
#test
if debug:
    first_of_all()
