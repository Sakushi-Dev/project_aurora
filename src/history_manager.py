import os
import sys
import textwrap
from datetime import datetime, timezone
from prompts_processing import first_message
from data_handler import get_slot, load_slot, save_set, load_set, select_slot, load_history
from data_handler import read_json, write_json, slot_path

def organize_chat_and_char():
    """
    Funktion, um den Chatverlauf und den Charakter zu organisieren.
    """
    global first_message
    
    slot = get_slot()

    data = load_slot(slot)

    if data:
        # Wenn ausgewälter Dialog nicht mit Char übereinstimmt, wird Char entsprechend gesetzt
        if load_set(char=True) != data[0]:
            save_set(char=True, data=data[0])
    else:
        # Wenn kein Dialog vorhanden ist, wird ein neuer Dialog erstellt
        current_time = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"
        char = load_set(char=True)
        select_slot(char=char, time=current_time, f_msg=first_message, slot=slot)
        
    history, list_msg = load_history(slot)
    
    return history, list_msg

# test
#print(organize_chat_and_char())
    

def get_history_length(list_msg: list) -> int:
    """
    Gibt die Länge des Chatverlaufs zurück.
    """
    
    if list_msg:
        history_len = len(list_msg)

    return history_len


def replay_last_interaction():
    """
    Entfernt die letzte Assistenzantwort aus der history_backup.py 
    und ermöglicht so ein /again (erneutes Abschicken).
    """
    global slot_path

    slot = get_slot()

    path = slot_path + f"/slot_{slot-1}.json"
    key = f"slot_{slot-1}"

    data = read_json(path)

    if key in data and len(data[key]) > 1 and "chat_history" in data[key][1]:

        history = data[key][1]["chat_history"]
        
        if len(history) > 2:
            history.pop()
            last_user_message = history.pop()

            write_json(path, data)

            return last_user_message
    return None


def save_analytics(input_from_user:str, output_from_ki:str):
    """
    Speichert die Eingabe des Benutzers und die Ausgabe der KI in einer Datei.
    """
    input_from_user = textwrap.dedent(input_from_user).strip()
    output_from_ki = textwrap.dedent(output_from_ki).strip()

    if not os.path.exists("./src/history/"):
        os.makedirs("./src/history/")

    analytics_path = "./src/history/analytics.py"

    # Mit repr() Strings robust im Python-Code unterbringen
    if not os.path.exists(analytics_path):
        # Neu anlegen
        analytics = (
            "analytics = [\n"
            f"  {{'input_from_user': {repr(input_from_user)}}},\n"
            f"  {{'output_from_ki': {repr(output_from_ki)}}},\n]" 
        )
        with open(analytics_path, "w", encoding="utf-8") as f:
            f.write(analytics)
    else:
        # Anhängen
        with open(analytics_path, "r+", encoding="utf-8") as f:
            content = f.read()
            content = content.rstrip()

            # Letzte eckige Klammer entfernen
            if content.endswith("]"):
                content = content[:-1]

            # Neues Objekt
            addition = (
                f"  {{'input_from_user': {repr(input_from_user)}}},\n"
                f"  {{'output_from_ki': {repr(output_from_ki)}}},\n]"
            )

            # Neu zusammensetzen
            new_content = content + addition

            f.seek(0)
            f.write(new_content)
            f.truncate()