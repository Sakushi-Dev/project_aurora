import re

from rich.console import Console
from rich.text import Text

from tiktoken_function import count_tokens


from prompts_processing import (
    user_name as user,
    char_name as char
)





# Rich-Console-Objekt:
console = Console(width=120)

def truncate_history_for_api(
        full_history: list,
        system_text: str,
        assistant_text: list,
        max_tokens: int = 2048
) -> list:
    """
    Trunkiert so lange Nachrichten, bis die Gesamttokenanzahl unter max_tokens fällt.
    """
    history_copy = full_history[:]
    while count_tokens(system_text, history_copy, assistant_text) > max_tokens:
        if len(history_copy) < 2:
            break
        history_copy.pop(0)  # Lösche ersten Eintrag (Fals First Message, sonst analyise)
        history_copy.pop(0)  # Lösche zweiten Eintrag
    
    return history_copy

def print_latest_messages(
        history: list,
        limit: int = 40,
        highlighted: str = "purple"

        ):
    """
    Gibt die letzten N Nachrichten formatiert in der Konsole aus.
    """
    # Farbe für Highlighting
    color = highlighted


    # Falls history leer ist
    if not history:
        return

    last_n = history[-limit:]

    for msg in last_n:
        # Sicherstellen, dass msg ein Dictionary ist
        if not isinstance(msg, dict):
            console.print(f"[red]Warnung: Unerwarteter Eintrag in history: {msg}[/red]")
            continue

        # "role" sicher holen
        msg_role = msg.get("role", "")
        # "content" sicher holen
        content = msg.get("content", "")

        # Rolle bestimmen
        if msg_role == "user":
            role_str = user
        elif msg_role == "assistant":
            role_str = char
        else:
            # Fallback oder custom handling für andere Rollen
            role_str = msg_role

        # Wenn es ein User ist -> normal ausgeben
        if role_str == user:
            console.print(f"[{role_str}]:\n\n{content}\n")

        # Zusätzliche Felder prüfen
        elif "input_from_user" in msg:
            a_user = msg["input_from_user"]
            console.print(f"{a_user}\n")


        elif role_str == char:
            # Assistant / sonstige Rolle -> highlight
            highlighted_text = re.sub(
                r"\*\s*(.*?)\*",
                r"[orange1]\1[/orange1]",
                content,
                flags=re.DOTALL
            )
            rich_text = Text.from_markup(f"[{color}]{highlighted_text}[/{color}]")
            console.print(f"[{color}][{role_str}]:[/{color}] ", rich_text, "\n")

        # Nicht "elif", damit wir beides sehen können, falls beides vorhanden
        elif "output_from_ki" in msg:
            a_ki = msg["output_from_ki"]
            console.print(f"{a_ki}\n")
