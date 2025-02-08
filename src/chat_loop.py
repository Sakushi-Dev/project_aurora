import os
import json
import time
import asyncio


from impatience import get_user_input

# Rich-Console-Import:
from rich.console import Console

# Score-Processing-Import:
from score_processing import score_processing, feelings_over_time

# Time-Manager-Import:
from sense_of_time import save_last_current_time

# Settings-Import:
from settings import set_config

# History-Manager-Import:
from history_manager import (
    get_history_length,
    load_history_from_file,
    append_to_history_file,
    save_analytics
)

# Task-Organizer-Import:
from task_organizer import (
    print_latest_messages
)

# Cost-Manager-Import:
from cost_manager import (
    calculate_cost,
    save_costs
)

# Command-Handler-Import:
from commands import (
    handle_exit,
    handle_again,
    handle_delete,
    handle_restart,
    handle_unknown
)

# Chat-Response-Import:
from response_manager import stream_chat_response, print_ki_response
import threading

debug = False

if debug:
    print(f"DebugMode: chat_loop.py\n\n=====================================\n\n")

# ======================
#   Globale Variablen
# ======================

# Rich-Console-Objekt:
console = Console(width=120)

# History-Länge laden
history_len = get_history_length()

# full_history-Liste initialisieren
full_history = []

# =================================================================================================

# ======================
#   Haupt-Chatfunktion
# ======================

def main_chat_loop(
            client,
            user:str,
            model:str,
            max_tokens:int=4096,
            frequency:int=2,
            imp:str="off",
            time_sense:bool=False,
            highlighted: str = "purple"
):
    
    global history_len, full_history

    """
    Haupt-Loop: Lädt History, startet Anthropic-Client, 
    wartet auf User-Eingaben und ruft das jeweilige Handling auf.
    """

    # 1) Letzte 20 Nachrichten mit analyse anzeigen (falls vorhanden)
    print_latest_messages(load_history_from_file(), highlighted=highlighted)
    

    # 3) Chat-Loop
    while True:
        
        # User-Eingabe
        # impatience Funktion Aktiviert (char antwortet automatisch)
        # Dies ist eine Endlosschleife, die dauerhaft Kosten verursacht
        user_input, assistant_imp = asyncio.run(get_user_input(imp))
        print()


        # Befehls-Handler als Funktionen definieren
        if user_input.lower() == "/exit":
            if handle_exit() == "exit":
                break
        elif user_input.lower() == "/config":
            # Einstellungen ändern
            # (Farbe, Impatience, Frequenz, Max-Tokens, Time-Sense)
            back = set_config()
            if back == "exit":
                os.system('cls' if os.name == 'nt' else 'clear')
                print_latest_messages(load_history_from_file(), highlighted=highlighted)
                continue
            
        elif user_input.lower() == "/again":
            # Aktuelle History mit Analyse Laden
            
            full_history = load_history_from_file()

            if len(full_history) > 1:

                full_history, sub_user_input = handle_again(user, full_history, highlighted)
                history_len -= 2
                # Weiter im regulären Ablauf
                pass
            else:
                console.print("[red]Du hast noch keine Nachrichten gesendet.[/red]\n")
                continue

        elif user_input.lower() == "/delete":
            result = handle_delete()
            if result == "delete":
                # contdown bis zum Neustart
                console.print("Aurora.py wird in neu gestartet", end="")
                for _ in range(5, 0, -1):
                    console.print(f"[red].[/red]", end="")
                    time.sleep(1)
                if handle_restart() == "restart":
                    break
            if result == "cancel":
                continue
        

        elif user_input.lower() == "/restart":
            console.print(f"Aurora.py wird in neu gestartet", end="")
            for _ in range(5, 0, -1):
                console.print(f"[red].[/red]", end="")
                time.sleep(1)
            if handle_restart() == "restart":
                break

#=======================================================================================
#====================================Test-Code==========================================

        elif user_input.lower() == "/mood":

            from tabulate import tabulate

             # Read emotion_score.json
            if os.path.exists("./data/emotion_score.json"):
                with open("./data/emotion_score.json", "r", encoding="utf-8") as f:
                    score = json.load(f)

                angry_value = score["Angry_Level"]
                sad_value = score["Sad_Level"]
                affection_value = score["Affection_Level"]
                arousal_value = score["Arousal_Level"]
                trust_value = score["Trust_Level"]

                show_mood = [["Emotionen", "Score"],
                    ["Wut", f"{angry_value}"],
                    ["Trauer", f"{sad_value}"],
                    ["Zuneigung", f"{affection_value}"],
                    ["Erregung", f"{arousal_value}"],
                    ["Vertrauen", f"{trust_value}"]
                ]
                console.print(tabulate(show_mood, headers="firstrow", tablefmt="grid"), "\n")
                continue
            else:
                console.print("[red]Keine Emotionen vorhanden[/red]\n\nMögliche Ursache:\n - Emotionen Score wurden noch nicht initialisiert\n - Emotionen Score wurde deaktiviert\n\n")

                continue

#========================================================================================
#========================================================================================

        elif user_input.startswith("/"):
            handle_unknown()
            continue #
        else:
            sub_user_input = False



        # Normale Nachricht
        # ----------------------------------
        
        # User-Nachricht in den Verlauf (in-memory)
        if sub_user_input:
            format_user_input = {"role": "user", "content": sub_user_input, "history": True}
        else:
            format_user_input = {"role": "user", "content": user_input, "history": True}
            # Initialisiere die History (Wird bei jedem Durchlauf neu geladen)
            full_history = load_history_from_file()
        full_history.append(format_user_input)

        # Save last current time as User-Input
        save_last_current_time()


        if debug:
            print(f"Full-History:\n\n{full_history}\n\n=====================================\n\n")
        
        
        # Anfrage an Claude (stream)
        
        current_tokens = stream_chat_response(
            client,
            model,
            full_history,
            assistant_imp,
            max_tokens
            )
        
        if imp == "neutral":
            freq = "🟢"
        else:
            freq = "🔴"
        

        input_from_user = (
            f"[black]{'=' * 120}[/black]\n"
            f"[black]Modell: {model} | Input/T: {current_tokens} ~ Max/T: {max_tokens} | Msg: {history_len}\n"
            f"[black]{'=' * 120}[/black]\n"
        )
        console.print(input_from_user)

        response_tokens, ki_response = print_ki_response(highlighted)

        # Kosten berechnen
        input_cost, output_cost = calculate_cost(
            model,
            current_tokens,
            response_tokens
        )

        # Gesamtkosten
        costs = input_cost + output_cost

        # +1 für die User-Nachricht
        history_len += 1

        output_from_ki = (
            f"[black]{'=' * 120}[/black]\n"
            f"[black]Modell: {model} | Output/T: {response_tokens} | Total Cost: ${costs:.3f} | Msg: {history_len} | [/black]{freq} [black]Impatience Status[/black]\n"
            f"[black]{'=' * 120}[/black]\n"
        )
        console.print(output_from_ki)

        # +1 für die KI-Nachricht
        history_len += 1

        # Antwort in den Verlauf (in-memory)
        ki_msg = {
            "role": "assistant",
            "content": ki_response,
            "history": True
        }
        full_history.append(ki_msg)

        # Save last current time as User-Input
        if time_sense:
            if assistant_imp == None:
                save_last_current_time()

        # Verlauf auch in Datei ablegen
        append_to_history_file(format_user_input, ki_msg)
        save_analytics(input_from_user, output_from_ki)
        save_costs(input_cost, output_cost)

        # Regelt emotion_score nach jdedem User-Input
        if os.path.exists("./data/emotion_score.json"):
            feelings_over_time()

        frequency_of_query = frequency *2

        # Triggered after 4 user messages
        if (history_len - 2) % frequency_of_query == 0:

            # Starte den Thread für die Score-Verarbeitung (ausführen ohne zu warten)
            threading.Thread(target=score_processing, args=(frequency_of_query,)).start()

            # Warten um gleichzeitigen Zugriff auf die Datei zu vermeiden
            time.sleep(0.1)

            # Kosten der abfrage werden in ./src/history/costs.py gespeichert
            if not os.path.exists("./src/history"):
                os.makedirs("./src/history")

            costs_path = "./src/history/costs.py"
            score_cost = input_cost + 0.00176

            costs = (
            f"total_input_cost = {score_cost}\n"
            f"total_output_cost = {output_cost}"
        )

            with open(costs_path, "w", encoding="utf-8") as f:
                f.write(costs)

            

        
        # ----------------------------------