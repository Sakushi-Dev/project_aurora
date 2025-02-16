import asyncio


from impatience import get_user_input

# Rich-Console-Import:
from rich.console import Console

# Score-Processing-Import:
from score_processing import score_processing, feelings_over_time

# History-Manager-Import:
from history_manager import (
    get_history_length,
    organize_chat_and_char
)

from data_handler import (
    save_dialog,
    load_set
)

# Time-Manager-Import:
from sense_of_time import save_current_time

# Task-Organizer-Import:
from task_organizer import (
    print_latest_messages
)

# Cost-Manager-Import:
from cost_manager import (
    calculate_cost,
    save_costs
)

from commands import command_dispatcher

# Chat-Response-Import:
from response_manager import stream_chat_response, print_ki_response
import threading

# =================================================================================================
# Debug-Modus

debug = False

if debug:
    print(
        f"DebugMode: chat_loop.py"
        f"\n\n{'='*30}\n\n"
    )

# =================================================================================================
# Globaler Scope

# Rich-Console-Objekt:
console = Console(width=120)

# history-Liste initialisieren
history = []


# =================================================================================================
#   Haupt-Chat-Loop

def main_chat_loop(
            client,
            slot:int=1,
            model:str="claude-3-5-haiku-20241022",
            max_tokens:int=4096,
            frequency:int=2,
            imp:str="off",
            time_sense:bool=False,
            highlighted: str = "purple"
):
    
    global history

    """
    Haupt-Loop: Lädt History, startet Anthropic-Client, 
    wartet auf User-Eingaben und ruft das jeweilige Handling auf.
    """
    history_len = 0
    format_user_input = None

    history, list_msg = organize_chat_and_char()
    history_len = get_history_length(list_msg)
    history_len = history_len
    print_latest_messages(list_msg, highlighted=highlighted)
    char = load_set(char=True)
    

    # 3) Chat-Loop
    while True:
        
        # User-Eingabe
        user_input, assistant_imp = asyncio.run(get_user_input(imp))
        print()

        result = command_dispatcher(user_input, highlighted, history_len)

        sub_user_input = None

        if result == None:
            continue
        if result:
            # Wenn der User '/again' eingibt, wird die letzte Nachricht wiederholt
            if isinstance(result, list):
                sub_user_input = result[0]
                history = result[1]
                history_len = result[2]

                if debug:
                    print(f"Result: {sub_user_input}\n\n{'='*30}\n\n")

        # ----------------------------------
        
        # User-Eingabe formatieren
        if sub_user_input:
            format_user_input = {"role": "user", "content": sub_user_input, "history": True}
        else:
            format_user_input = {"role": "user", "content": user_input, "history": True}
        
        # User-Nachricht in den Verlauf (in-memory)
        history.append(format_user_input) 


        if debug:
            print(f"Full-History:\n\n{history}\n\n{'='*30}\n\n")
        
        # Anfrage an Claude (stream)
        current_tokens = stream_chat_response(
            client,
            model,
            history,
            assistant_imp,
            max_tokens,
            )
        
        if imp == "neutral":
            freq = "🟢"
            imp_status = True
        else:
            freq = "🔴"
            imp_status = False
        
        # Analyse anzeige formatieren
        input_from_user = (
            f"[black]{'─'*120}[/black]\n"
            f"[black]Msg: {history_len} | "
            f"Input/T: {current_tokens} ~ Max/T: {max_tokens}\n"
            f"[black]{'─'*120}[/black]\n"
        )

        # User-Analyse
        console.print(input_from_user)

        # KI-Antwort
        response_tokens, ki_response = print_ki_response(char, highlighted)

        # Kosten berechnen
        input_cost, output_cost = calculate_cost(
            model,
            current_tokens,
            response_tokens
        )

        # Gesamtkosten
        costs = input_cost + output_cost

        # Analyse anzeige formatieren
        output_from_ki = (
            f"[black]{'─'*120}[/black]\n"
            f"[black]Msg: {history_len + 1} | "
            f"formatOutput/T: {response_tokens} | "
            f"Total Cost: ${costs:.3f} | "
            f"[/black]{freq} [black]Impatience Status[/black]\n"
            f"[black]{'─'*120}[/black]\n"
        )

        # KI-Analyse
        console.print(output_from_ki)

        # +1 für die KI-Nachricht
        history_len += 2

        # Zusammensetzen der der nachricht und der analyse
        ki_msg = {
            "role": "assistant",
            "content": ki_response,
            "history": True,
            "analysis":{
                "output_t": response_tokens,
                "msg": history_len
                },
                "history": True
            }
        
        if sub_user_input:
            # User-Eingabe wird auf den Sub-Input gesetzt fals '/again' benutzt wird
            user_input = sub_user_input
            
        format_user_input = {
            "role": "user",
            "content": user_input,
            "history": True,
            "analysis":{ 
                "input_t": current_tokens,
                "msg": (history_len - 1)
                },
                "history": True
            }
        
        history.append(ki_msg)

        # Save last current time as User-Input
        if time_sense:
            if assistant_imp == None:
                save_current_time()

        # Verlauf in Datei ablegen
        save_dialog([format_user_input, ki_msg])
        save_costs(input_cost, output_cost)

        feelings_over_time()

        frequency_of_query = frequency *2 # x2 da Ki response auch als Nachricht zählt

        # Triggered after 4 user messages
        if (history_len - 1) % frequency_of_query == 0:

            # Starte den Thread für die Score-Verarbeitung (ausführen ohne zu warten)
            threading.Thread(target=score_processing, args=(frequency_of_query, slot)).start()

        # ----------------------------------