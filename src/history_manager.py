import os
import sys
import json
import textwrap
from prompts_processing import first_message


def load_history_from_file(filepath: str = "./src/history/history_backup.py") -> list:
    """
    Lädt den bisherigen Verlauf aus einer lokalen Datei.
    Gibt eine Liste von Nachrichten-Dictionaries zurück.
    """
    global first_message

    if os.path.exists(filepath):
        if "history.history_backup" in sys.modules:
            del sys.modules["history.history_backup"]
        from history.history_backup import history_backup  # type: ignore
        if "history.analytics" in sys.modules:
            del sys.modules["history.analytics"]
        from history.analytics import analytics  # type: ignore

        last_analytics = []
        if analytics:
            last_analytics = analytics[-39:]

        # Erstes Element (oder die "initiale Nachricht")
        if history_backup:
            first_msg = [history_backup[0]]

            # Den Rest: letzten 19 Einträge
            trimmed_history_backup = history_backup[1:]
            last_40_history = trimmed_history_backup[-39:]

        # Wir bauen eine FLACHE Liste
        for i, msg in enumerate(last_40_history):
            
            first_msg.append(msg)

            if len(last_analytics) > i:
                first_msg.append(last_analytics[i])

        return first_msg
    else:
        return first_message


def get_history_length():
    """
    Funktion, um die Länge der History zu ermitteln.
    Überprüft, ob `history_backup.py` existiert und lädt bei Bedarf das Backup.
    
    Returns:
        int: Die Länge der History.
    """
    history_len = 2  # Standardwert
    if os.path.exists("./src/history/history_backup.py"):
        del sys.modules["history.history_backup"]
        try:
            from history.history_backup import history_backup  # type: ignore
            history_len = len(history_backup)+1
        except ImportError:
            pass
    return history_len


def replay_last_interaction(full_history):
    """
    Entfernt die letzte Assistenzantwort aus der history_backup.py 
    und ermöglicht so ein /again (erneutes Abschicken).
    """
    file_path = "./src/history/history_backup.py"
    if not os.path.exists(file_path):
        return None

    # history_backup neu laden
    if "history.history_backup" in sys.modules:
        del sys.modules["history.history_backup"]
    from history.history_backup import history_backup  # type: ignore

    # Entferne letzte analyse und speichere letzte User-Nachricht
    if len(history_backup) >= 3:
        history_backup.pop()  # Ki-Antwort
        last_user_message = history_backup.pop()  # User-Nachricht
        
        # Leher Verlauf
        with open(file_path, "w", encoding="utf-8") as f:
            f.write("history_backup = []")

        # Neuen Verlauf schreiben ohne letzte beiden Einträge
        with open(file_path, "r+", encoding="utf-8") as f:
            f.write("history_backup = [\n")
            for item in history_backup:
                # An die Stelle des finalen `]` springen
                f.seek(0, os.SEEK_END)
                # Zwei Zeichen (Zeilenumbruch + ]) zurück
                f.seek(f.tell() - 1, os.SEEK_SET)
                # Schreibe jedes Element der Liste mit einem Umbruch und Einrückung
                f.write(f"  {item},\n")
            f.write("]")

        # Modul-Reload
        if "history.history_backup" in sys.modules:
            del sys.modules["history.history_backup"]
        from history.history_backup import history_backup # type: ignore
        return full_history, last_user_message
    return None

def append_to_history_file(
        user_msg: dict,
        ai_msg: dict,
        file_path: str = "./src/history/history_backup.py"
):
    """
    Schreibt neue Nachrichten in die bestehende history_backup.py Datei.
    Erzeugt sie, wenn sie nicht existiert.
    """
    if not os.path.exists("./src/history"):
        os.makedirs("./src/history")

    # Falls die Datei noch nicht existiert
    if not os.path.exists(file_path):
        with open(file_path, "w", encoding="utf-8") as f:
            f.write("history_backup = [\n")
            # Falls es eine first_message gibt, schreibe sie einmalig
            if first_message:
                f.write(f"  {first_message[0]},\n")
            f.write(f"  {user_msg},\n")
            f.write(f"  {ai_msg},\n]")
    else:
        # In bestehender Liste ergänzen
        with open(file_path, "r+", encoding="utf-8") as f:
            # Dateiinhalt ganz lesen
            content = f.read()
            # An die Stelle des finalen `]` springen
            f.seek(0, os.SEEK_END)
            # Zwei Zeichen (Zeilenumbruch + ]) zurück
            f.seek(f.tell() - 2, os.SEEK_SET)
            f.write(f"  {user_msg},\n")
            f.write(f"  {ai_msg},\n]")



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