import os
import sys
import base64

from rich.console import Console
from prompt_toolkit.styles import Style

console = Console()

custom_style = Style.from_dict({
        '': 'fg:#87FF87',
    })


# API-Key Path
api_folder = "./API"
api_file_name = "api_key.env"
API_KEY_PATH = f"{api_folder}/{api_file_name}"

ENV_VARIABLE_NAME = "ANTHROPIC_API_KEY"

#===============================================================================

def check_api_key_file():
    
    if not os.path.exists(API_KEY_PATH):
        return False
    else:
        with open(API_KEY_PATH, "r", encoding="utf-8") as file:
            api_key = file.read()
        
        if api_key and api_key != "": 
            return True
        
#===============================================================================        

def is_valid_anthropic_key():
    import requests

    console.print(
        f"{'-'*120}\n"
        "Nur API-Keys von [color(37)]Anthropic[/color(37)] sind erlaubt!\n"
        "Link: https://console.anthropic.com/ Hier kannst du einen API-Key erstellen.\n"
        f"{'-'*120}\n"
        )
    console.print(
        "[orange1]Info:[/orange1] Es wird ein Test-Request an die Anthropic API gesendet.\n"
        "Bei diesem Test-Request fallen keine relevanten Kosten an. (0.0000015$)\n\n"
        f"{'-'*120}\n"
        "Dein API-Key wird verschlüsselt und lokal als Umgebungsvariable gespeichert.\n"
        "Beachte das der API-Key nichtmehr angezeigt wird, nachdem er eingegeben wurde.\n"
        "Bewahre den API-Key sicher auf, da er nicht wiederhergestellt werden kann.\n"
        f"{'-'*120}\n"
        "[red]Wichtig:[/red] Gebe deinen API-Key oder eine Kopie des Programms nicht an Dritte weiter!\n"
        "Jeder der deinen API-Key hat, kann damit auf deine Kosten Anfragen an die Anthropic API senden.\n"
        f"{'-'*120}\n"
        )
    api_key = console.input("[green]Gebe deinen API-Key ein: [/green]")

    # Anthropic API URL für einen einfachen Test-Request
    url = "https://api.anthropic.com/v1/messages"
    
    # Header für Anthropic API
    headers = {
        "x-api-key": api_key,
        "anthropic-version": "2023-06-01",
        "content-type": "application/json"
    }
    
    # Minimaler Test-Request
    data = {
        "model": "claude-3-haiku-20240307",
        "max_tokens": 1,
        "messages": [{"role": "user", "content": "Hi"}]
    }
    
    try:
        response = requests.post(url, headers=headers, json=data)
        
        if response.status_code == 200:
            console.print("[green]Der API-Schlüssel ist gültig![/green]")
            return api_key
        elif response.status_code == 401:
            console.print("[red]Fehler:[/red] Ungültiger API-Schlüssel")
            return None
        else:
            console.print(f"[orange1]Fehler {response.status_code}: {response.text}[/orange1]")
            return None
            
    except requests.exceptions.RequestException as e:
        console.print(f"[orange1]Verbindungsfehler: {e}[/orange1]")
        return None
    
#===============================================================================
    
def save_api_key(api_key):
    
    encoded_key = base64.b64encode(api_key.encode()).decode()
    os.makedirs(os.path.dirname(API_KEY_PATH), exist_ok=True)

    with open(API_KEY_PATH, "w", encoding="utf-8") as file:
        file.write(f"{ENV_VARIABLE_NAME}={encoded_key}")

#===============================================================================

def load_api_key():
    from dotenv import load_dotenv

    if not os.path.exists(API_KEY_PATH):
        console.print("[red]API-Schlüssel nicht gefunden![/red]")
        return None
    
    load_dotenv(API_KEY_PATH, override=True)
    encoded_key = os.getenv(ENV_VARIABLE_NAME)

    if not encoded_key:
        console.print("[red]API-Schlüssel nicht gefunden![/red]")
        return None
    
    try:
        api_key = base64.b64decode(encoded_key).decode("utf-8")
        os.environ[ENV_VARIABLE_NAME] = api_key

        return api_key
    except Exception as e:
        console.print(f"[red]Fehler beim Laden des API-Schlüssels: {e}[/red]")
        return None
    
