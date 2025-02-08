import re
import os
import time
import textwrap
import anthropic

from rich.text import Text
from rich.console import Console

from score_trigger import mood_trigger

from tiktoken_function import count_tokens, output_tokens

from sense_of_time import diff_time_trigger

# Task-Organizer-Import:
from task_organizer import truncate_history_for_api

from prompts_processing import (
    system_prompt,
    assistant_prompt,
    char_name as char,
)

debug = False
lokal = False


#==================================================================================================
# Debugging Initialisierung
if debug and lokal:
    print(f"DebugMode: response_manager.py\n\n=========================================\n")

    from anthropic_api import init_anthropic_client, load_api_key
    api_key = load_api_key()
    client = init_anthropic_client(api_key)

    model = "claude-3-5-haiku-20241022"

    from history_manager import load_history_from_file
    full_history = load_history_from_file()
    api_messages = [
            {"role": msg["role"], "content": msg["content"]}
            for msg in full_history if "role" in msg and "content" in msg
        ]
    
    user_input = "Hallo"
    api_messages.append({"role": "user", "content": user_input})
#==================================================================================================


# Rich-Console-Objekt:
console = Console(width=120)

# Globale Variablen für um assistent_prompt dynamisch zu verändern
temp_assistant_prompt = []

# Globale Variablen für die Anfrage
final_client = None
final_model_name = ""
final_system_prompt = []
fina_messages = []



def stream_chat_response(
    client: anthropic.Anthropic,
    model_name: str,
    full_history: list,
    assistant_imp: list = None,
    max_tokens: int = 4096
) -> str:
    global temp_assistant_prompt, final_client, final_model_name, final_system_prompt, final_messages

    """
    Sendet die Anfrage an das ausgewählte Anthropic-Modell
    und streamt die Antwort chunkweise zurück.
    """

    # Lege temporäre Kopie von assistant_prompt an
    temp_assistant_prompt = assistant_prompt[:]

    mood = mood_trigger()
    
    # Pre-fill entfernen und später wieder einfügen
    prefill = temp_assistant_prompt.pop()
    
    # Mood und Sense of Time einfügen
    temp_assistant_prompt.append(mood)

    # Nur Sense of Time einfügen wenn es in data vorhanden ist
    if os.path.exists("data/current_time.txt"):
        sense_of_time = diff_time_trigger()
        temp_assistant_prompt.append(sense_of_time)
    if assistant_imp:
        temp_assistant_prompt.append(assistant_imp)

    # Pre-fill wieder einfügen
    temp_assistant_prompt.append(prefill)

    # Tokenberechnung
    truncate_history = truncate_history_for_api(full_history, system_prompt, temp_assistant_prompt, max_tokens)
    current_tokens = count_tokens(system_prompt, truncate_history, temp_assistant_prompt)

    # Andere werte die nicht "role" und "content" sind, werden nicht übergeben
    api_messages = [
        {"role": msg["role"], "content": msg["content"]}
        for msg in truncate_history if "role" in msg and "content" in msg
    ]

    temp_messages = api_messages + temp_assistant_prompt

    final_client = client
    final_model_name = model_name
    final_system_prompt = system_prompt[:]
    final_messages = temp_messages[:]

    if debug:
        print(f"Model: {model_name}\n")
        print(
            "=========================================\n"
            f"System-Prompt:\n\n{final_system_prompt}\n\n"
            "=========================================\n"
            f"Messages:\n\n{final_messages}\n\n"
            "=========================================\n"
            )

    
    return current_tokens

def print_ki_response(highlighted: str = "purple"):
    global final_client, final_model_name, final_system_prompt, final_messages

    # Highlighted-Text
    color = highlighted
    
    response_text = ""

    try:
        with final_client.messages.stream(
            model=final_model_name,
            max_tokens=512,
            temperature=0.7,
            system=final_system_prompt,
            messages=final_messages
        ) as stream:
            chunks = list(stream.text_stream)

            # Mood wieder entfernen
            temp_assistant_prompt.pop(-2) 

            # Alle Chunks zusammenfügen:
            response_text = "".join(chunks)

    except Exception as e:
        console.print(f"[red]Fehler bei der Anfrage: {e}[/red]")

    # Live-Vorschau fürs finale Ausgeben:
    console.print(f"[{color}][{char}]: [/{color}]\n\n", end="")
    
    wrapped_text = textwrap.dedent(response_text).strip()
    highlighted_text = re.sub(
        r"\*\s*(.*?)\*",
        r"[orange1]\1[/orange1]",
        wrapped_text,
        flags=re.DOTALL
    )

    #Inizialisiere Simulierte Schreibgeschwindigkeit
    lines = highlighted_text.splitlines()
    rich_text_list = [textwrap.fill(line, width=84) for line in lines]
    finally_response = []
    for rich_text in rich_text_list:
        rich_text = Text.from_markup(f"[{color}]{rich_text}[/{color}]")
        finally_response.append(rich_text)
        finally_response.append("\n")
    
    # Zeichenweise Ausgabe
    for text in finally_response:
        for single_char in text:
            console.print(single_char, end="", highlight=False, overflow="fold")
            time.sleep(0.02)


    print()  # Zusätzlicher Zeilenumbruch nach vollständiger Antwort

    response_token = output_tokens(response_text)
    return response_token, response_text


if debug and lokal:
    stream_chat_response(client, model, api_messages)