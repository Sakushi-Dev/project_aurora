"""
Project Aurora - Initialization Module
------------------------------------
This module handles the initial setup and configuration process when Aurora is started.
It verifies prerequisites, guides the user through setup, and prepares the environment.
"""

import os
import time

from typing import Tuple, Dict, Any

# Rich components for enhanced UI
from rich.panel import Panel
from rich.columns import Columns

# Project components
from secure_api_key import check_api_key_file, is_valid_anthropic_key, save_api_key
from data_handler import save_set, write_json, read_file
from init_data import init_data
from task_organizer import dynamic_typing, loading_animation
from globals import FOLDER, console


# Color palette with semantic names
COLORS = {
    "primary": "color(56)",      # Purple - Primary theme color
    "secondary": "color(37)",    # Turquoise - Secondary theme color 
    "success": "color(118)",     # Green - Success indicators
    "warning": "color(208)",     # Orange - Warnings
    "error": "color(124)",       # Red - Errors
    "info": "color(20)",         # Blue - Information
    "highlight": "color(200)",   # Pink - Highlights
    "neutral": "color(255)"      # White - Standard text
}

# This will be populated dynamically by scanning the YAML files

# Theme color options for highlighting the character's text
THEME_COLORS = {
    1: {"name": "Red", "code": "color(124)"},
    2: {"name": "Pink", "code": "color(200)"},
    3: {"name": "Purple", "code": "color(56)"},
    4: {"name": "Blue", "code": "color(20)"},
    5: {"name": "Turquoise", "code": "color(37)"},
    6: {"name": "Green", "code": "color(118)"},
    7: {"name": "White", "code": "color(255)"}
}


def clear_screen() -> None:
    """Clear the terminal screen for better readability."""
    os.system('cls' if os.name == 'nt' else 'clear')


def load_characters_from_yaml() -> Dict[int, Dict[str, Any]]:
    """
    Load character information from YAML files in the char_spec folder.
    
    Returns:
        Dict[int, Dict[str, Any]]: Dictionary of character information
    """
    characters = {}
    char_idx = 1
    
    # Get all YAML files in the char_spec directory
    char_spec_dir = FOLDER["char_spec"]
    
    for file_path in char_spec_dir.glob("*.yaml"):
        # Skip example.yaml
        if file_path.name == "example.yaml":
            continue
        
        # Read YAML file
        yaml_data = read_file(file_path)
        if yaml_data:
            # Extract character name and type
            name = yaml_data.get('char_name', "")

            # Extract metadata
            metadata = yaml_data.get('metadata', {})
            
            # Determine character type and features from metadata
            tags = metadata.get('tags', [])

            tag_str = ""
            for tag in tags:
                tag_str += f"{tag.title()}, "

            # The creator of the character
            creator = metadata.get('creator', "")
            if creator:
                creator_lable = f"Created by {creator}"
            
            # Process development status
            development = "Complete"
            if metadata.get('status') and metadata.get('status') != "released":
                development = "Early Development Phase"
            
            # Create character entry
            characters[char_idx] = {
                "name": name,
                "type": metadata.get('type', ""),
                "note": metadata.get('notes', ""),
                "description": metadata.get('desc', ""),
                "features": tag_str,
                "sense_of_time": True if "sense of time" in tags else False,
                "creator": creator_lable,
                "development": development,
                "version": metadata.get('version', ""),
            }
            
            char_idx += 1
    
    return characters


def check_existing_config() -> bool:
    """
    Check if user configuration already exists.
    
    Returns:
        bool: True if configuration exists, False otherwise
    """
    user_name_path = FOLDER["user_spec"] / "user_name.json"
    if user_name_path.exists():
        data = read_file(user_name_path, debug=False)
        if data is not None:
            return True
    return False


def setup_api_key() -> str:
    """
    Handle API key validation and storage.
    
    Returns:
        str: Status message
    """
    if not check_api_key_file():
        attempts = 0
        max_attempts = 3
        
        while attempts < max_attempts:
            api_key = is_valid_anthropic_key()
            if api_key:
                save_api_key(api_key)
                return "API key successfully validated and saved!"
            
            attempts += 1
            if attempts < max_attempts:
                console.print(f"\n[{COLORS['warning']}]Invalid API key. Attempts remaining: {max_attempts - attempts}[/{COLORS['warning']}]")
                time.sleep(2)
        
        console.print(f"[{COLORS['error']}]Failed to validate API key after multiple attempts.[/{COLORS['error']}]")
        return "API key validation failed!"
    else:
        return "Existing API key found!"


def display_aurora_intro() -> None:
    """Display the Project Aurora introduction and banner."""
    aurora_banner = ""
    
    with open("./src/text_files/Project Aurora.txt", "r", encoding="utf-8") as file:
        for line in file:
            aurora_banner += str(line).strip() + "\n"
    

    
    message = "Welcome to Project Aurora!"
    dynamic_typing(message, mode="print", centered=True, delay=0.05, color="magenta")
    time.sleep(0.5)
    console.print("\n" + aurora_banner)
    console.input(f"\n[{COLORS['info']}]Press Enter to continue...[/{COLORS['info']}]")


def get_user_info() -> Tuple[str, str, str]:
    """
    Collect user information (name, gender, language preference).
    
    Returns:
        Tuple[str, str, str]: User name, gender, and language
    """
    clear_screen()
    
    # Get user name
    while True:
        name_prompt = "Choose a name for yourself\n(This will be used in the chat but can be changed later)"
        user_name = dynamic_typing(name_prompt, mode="input", centered=True, delay=0.05, color=COLORS["neutral"])
        
        confirm_prompt = f"Your name is {user_name}?"
        confirm = dynamic_typing(confirm_prompt, mode="input", centered=True, choice=True, delay=0.05, color=COLORS["neutral"])
        if confirm.lower() == "y":
            break
    
    # Get user gender
    while True:
        gender_prompt = "Are you male, female or diverse?\n(Answer with M, F or D)"
        gender_input = dynamic_typing(gender_prompt, mode="input", centered=True, delay=0.05, color=COLORS["neutral"])
        
        if gender_input.lower() in ("m", "f", "d"):
            gender_map = {"m": "male", "f": "female", "d": "diverse"}
            gender = gender_map[gender_input.lower()]
            break
        else:
            dynamic_typing("Invalid input!", mode="print", centered=True, delay=0.05, color=COLORS["error"])
    
    # Get user language preference
    while True:
        language_prompt = "Choose your language for the chat\n(Answer with EN or DE)"
        lang_input = dynamic_typing(language_prompt, mode="input", centered=True, delay=0.05, color=COLORS["neutral"])
        
        if lang_input.lower() in ("en", "de"):
            language_map = {"en": "english", "de": "german"}
            language = language_map[lang_input.lower()]
            break
        else:
            dynamic_typing("Invalid input!", mode="print", centered=True, delay=0.05, color=COLORS["error"])
    
    return user_name, gender, language


def display_character_info(characters: Dict[int, Dict[str, Any]]) -> None:
    """
    Display information about available characters.
    
    Args:
        characters: Dictionary of character information
    """
    clear_screen()
    console.print(f"Choose a character you want to interact with.\n\n")
    
    for _, char_info in characters.items():
        # Character name and type
        console.print(f"[{COLORS['secondary']}]Name: {char_info['name']}\nScenario: {char_info['type']}[/{COLORS['secondary']}]")
        
        # Development status indicator if needed
        if char_info['development'] != "Complete":
            console.print(f"[{COLORS['warning']}]⚠️ {char_info['development']}[/{COLORS['warning']}]")
        
        console.print(f"{'-'*120}\n")
        
        # Character description
        console.print(f"Description:\n\n{char_info['description']}\n")

        console.print(f"{'-'*120}\n")
        
        # Metadata information
        console.print(f"{char_info['creator']}\n")
        console.print(f"Version: {char_info['version']}\n")
        
        console.print(f"Note: {char_info['note']}")
        features_str = " | ".join(char_info['features'].split(", "))
        console.print(f"Tags: {features_str}\n")
        
        # Separator between characters
        console.print(f"[black]{'─' * 120}[/black]\n")


def select_character(characters: Dict[int, Dict[str, Any]]) -> Tuple[str, str]:
    """
    Let the user select a character.
    
    Args:
        characters: Dictionary of character information
        
    Returns:
        Tuple[str, str]: Selected character's file name and display name
    """
    display_character_info(characters)
    
    # Get character selection
    while True:
        char_options = ", ".join([f"{idx}:{info['name']}" for idx, info in characters.items()])
        choice_prompt = f"Choose a character\n(Answer with a number from: {char_options})"
        try:
            choice = int(dynamic_typing(choice_prompt, mode="input", centered=True, delay=0.05, color=COLORS["neutral"]))
            if choice in characters:
                return characters[choice]["file_name"], characters[choice]["name"]
            else:
                console.print(f"[{COLORS['error']}]Invalid input![/{COLORS['error']}]\n")
        except ValueError:
            console.print(f"[{COLORS['error']}]Please enter a number![/{COLORS['error']}]\n")


def display_theme_colors() -> None:
    """Display color theme options with visual examples."""
    clear_screen()
    dynamic_typing("Color Theme Selection", mode="print", centered=True, delay=0.05, color=COLORS["neutral"])
    time.sleep(0.5)
    
    # Generate and display color panels in pairs
    for i in range(1, len(THEME_COLORS), 2):
        # Create panels for each color
        panel1 = Panel(
            f"[{THEME_COLORS[i]['code']}]Sample text in {THEME_COLORS[i]['name']}[/{THEME_COLORS[i]['code']}]",
            title=f"[bold {THEME_COLORS[i]['code']}]Option {i}[/bold {THEME_COLORS[i]['code']}]",
            width=50,
            expand=True,
            border_style="white",
        )
        
        # Check if we have a second panel to display (for odd number of colors)
        if i+1 <= len(THEME_COLORS):
            panel2 = Panel(
                f"[{THEME_COLORS[i+1]['code']}]Sample text in {THEME_COLORS[i+1]['name']}[/{THEME_COLORS[i+1]['code']}]",
                title=f"[bold {THEME_COLORS[i+1]['code']}]Option {i+1}[/bold {THEME_COLORS[i+1]['code']}]",
                width=50,
                expand=True,
                border_style="white",
            )
            # Display panels side by side
            console.print(Columns([f"{' '*2}{i}.) ", panel1, f"{' '*2}{i+1}.) ", panel2, f"{' '*6}"]))
        else:
            # Display single panel for last odd-numbered color
            console.print(Columns([f"{' '*2}{i}.) ", panel1, f"{' '*50}"]))
        
        console.print(f"[black]{'─' * 120}[/black]\n")


def select_theme_color() -> str:
    """
    Let the user select a theme color.
    
    Returns:
        str: Color code for the selected theme
    """
    display_theme_colors()
    
    while True:
        try:
            color_prompt = "Choose a color theme (1-7)\n(Can be changed later)"
            color_choice = int(dynamic_typing(color_prompt, mode="input", centered=True, delay=0.05, color=COLORS["neutral"]))
            
            if color_choice in THEME_COLORS:
                return THEME_COLORS[color_choice]["code"]
            else:
                console.print(f"[{COLORS['error']}]Invalid choice. Please select a number between 1 and 7.[/{COLORS['error']}]")
        except ValueError:
            console.print(f"[{COLORS['error']}]Please enter a valid number.[/{COLORS['error']}]")


def display_final_instructions() -> None:
    """Display final setup instructions and command information."""
    clear_screen()
    
    console.print(
        f"Almost done!\n\n"
        f"[{COLORS['secondary']}]Note on Command Mode:[/{COLORS['secondary']}]\n"
        f"To access commands, type [red]/[/red] followed by the command name.\n"
        f"After entering the slash, all available commands will be displayed.\n\n"
        f"[{COLORS['secondary']}]Example:[/{COLORS['secondary']}] [red]/[/red][green]mood[/green]\n"
        f"This command shows you the current mood of your character.\n\n"
        f"[{COLORS['info']}]Other useful commands:[/{COLORS['info']}]\n"
        f"[red]/[/red][green]config[/green] - Adjust settings\n"
        f"[red]/[/red][green]think[/green] - See your character's inner thoughts\n"
        f"[red]/[/red][green]help[/green] - Show all available commands\n"
    )
    
    confirm = dynamic_typing(
        "Are you ready to begin?",
        mode="input",
        centered=True,
        choice=True,
        delay=0.05,
        color=COLORS["neutral"]
    )
    
    if confirm.lower() != "y":
        confirm_exit = dynamic_typing(
            "Do you really want to cancel setup?",
            mode="input",
            centered=True,
            choice=True,
            delay=0.05,
            color=COLORS["error"]
        )
        if confirm_exit.lower() == "y":
            console.print(f"[{COLORS['error']}]Setup cancelled. Exiting program...[/{COLORS['error']}]")
            time.sleep(1)
            os._exit(0)
        else:
            # If user doesn't want to exit, show the instructions again
            display_final_instructions()


def save_user_config(user_name: str, gender: str, language: str, char_file_name: str, char_display_name: str, theme_color: str) -> None:
    """
    Save all user configuration to respective files.
    
    Args:
        user_name: User's chosen name
        gender: User's gender
        language: Preferred language
        char_file_name: Selected character's file name
        char_display_name: Selected character's display name
        theme_color: Selected theme color
    """
    # Save user information
    user_name_path = FOLDER["user_spec"] / "user_name.json"
    user_gender_path = FOLDER["user_spec"] / "user_gender.json"
    user_language_path = FOLDER["user_spec"] / "user_language.json"
    
    write_json(str(user_name_path), {"user_name": user_name})
    write_json(str(user_gender_path), {"user_gender": gender})
    write_json(str(user_language_path), {"language": language})
    
    # Save character and theme settings
    save_set(char=True, data=char_display_name)
    save_set(color=True, data=theme_color)
    
    # Enable sense of time for Mia only (or other characters with time sense feature)
    yaml_file = FOLDER["char_spec"] / f"{char_file_name}.yaml"
    yaml_data = read_file(yaml_file)
    
    if yaml_data:
        metadata = yaml_data.get('metadata', {})
        tags = metadata.get('tags', [])
        
        # Enable time sense if character has the appropriate tags
        if "evolution" in tags or char_display_name.lower() == "mia":
            save_set(time_sense=True, data=True)


def first_of_all() -> bool:
    """
    Main initialization function. Runs the complete setup process if needed.
    
    Returns:
        bool: True if setup is complete and successful
    """
    # Skip setup if configuration already exists
    if check_existing_config() and not os.environ.get("AURORA_FORCE_SETUP"):
        return True
    
    try:
        # Initialize data structures
        init_data()
        
        # Display intro
        display_aurora_intro()
        
        # Setup API key
        clear_screen()
        api_status = setup_api_key()
        loading_animation("API key", wait=3, status=True, color=COLORS["success"])
        time.sleep(2)
        
        # Load character information from YAML files
        characters = load_characters_from_yaml()
        
        if not characters:
            console.print(f"[{COLORS['error']}]No valid character files found in the char_spec directory.[/{COLORS['error']}]")
            time.sleep(3)
            return False
        
        # Collect user information
        user_name, gender, language = get_user_info()
        
        # Character selection
        char_file_name, char_display_name = select_character(characters)
        
        # Theme color selection
        theme_color = select_theme_color()
        
        # Final instructions
        display_final_instructions()
        
        # Save all configuration
        save_user_config(user_name, gender, language, char_file_name, char_display_name, theme_color)
        
        clear_screen()
        return True
        
    except Exception as e:
        console.print(f"[{COLORS['error']}]Setup error: {str(e)}[/{COLORS['error']}]")
        console.print(f"[{COLORS['info']}]Please restart the application to try again.[/{COLORS['info']}]")
        time.sleep(3)
        return False


# For testing purposes when run directly
if __name__ == "__main__":
    # Force setup even if configuration exists
    os.environ["AURORA_FORCE_SETUP"] = "1"
    first_of_all()