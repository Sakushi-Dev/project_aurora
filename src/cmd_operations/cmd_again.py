# import built-in modules
import os
import re

# Import external modules
from globals import console
from rich.panel import Panel

# Import custom modules
from data_handler import read_json, get_slot, load_history
from task_organizer import print_latest_messages
from history_manager import replay_last_interaction

# Import path from scr/data_handler.py
from data_handler import user_name_path

def execute_again(highlighted):

    # lösche Letze zwei Einträge und gbe die letzte User-Nachricht zurück
    last_user_message = replay_last_interaction()
    if last_user_message:

        # Clear Screen
        os.system('cls' if os.name == 'nt' else 'clear')

        # Alte Usernachricht anzeigen
        user_input = last_user_message["content"]

        data= read_json(user_name_path)
        user = data["user_name"]

        slot = get_slot()

        # History laden und anzeigen
        history, list_msg = load_history(slot)
        print_latest_messages(list_msg, highlighted=highlighted)

        # User-Nachricht anzeigen
        highlighted_text = re.sub(
            r"\*\s*(.*?)\*",
            r"[orange1]\1[/orange1]",
            user_input,
            flags=re.DOTALL
        )
        console.print(
            Panel(
                highlighted_text,
                title=f"[bold]{user}[/bold]",
                expand=True,
                border_style="white"
                )
            )
        print()
        
    return history, user_input