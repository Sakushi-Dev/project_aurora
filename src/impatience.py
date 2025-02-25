from data_handler import (
    read_json,
    imp_prompt_path,
    load_user_char_name,
    load_set
)

char = load_set(char=True)
user = load_user_char_name(user=True)

# Lese die Datei 'impatience_prompt.json' aus dem Ordner 'data' ein
data = read_json(imp_prompt_path)

# Speichere die Werte aus dem Dictionary in Variablen
prefill = data[0]['imp_prefill']
imp_response = data[1]['imp_response']
imp_response_color = data[2]['imp_response_color']
prefill_1 = prefill[0]
prefill_2 = prefill[1]

# Platzhalter in den Strings ersetzen
for key, value in prefill_1.items():
    prefill_1[key] = value.replace("{char}", char).replace("{user}", user)
for key, value in prefill_2.items():
    prefill_2[key] = value.replace("{char}", char).replace("{user}", user)


imp_response = imp_response.replace("{char}", char).replace("{user}", user)
imp_response_color = imp_response_color.replace("{char}", char).replace("{user}", user)

#==================================================================================================

prefill_1 = prefill_1
prefill_2 = prefill_2
imp_response = imp_response
imp_response_color = imp_response_color

#==================================================================================================

import re
import sys
import asyncio
import random

# Rich-Console-Import:
from rich.console import Console
from rich.panel import Panel

# import prompt_toolkit
from prompt_toolkit import PromptSession
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.key_binding.bindings.named_commands import accept_line

#====================================== Setze Global Variables ====================================

console = Console()

kb = KeyBindings()

@kb.add("c-@")
def _(event):
    event.app.current_buffer.insert_text("\n")

@kb.add("c-m")
def _(event):
    accept_line(event)

@kb.add('/')
def _(event):
    console.print(
        "\nBefehle:\n\n"
        "[red]/[/red][green]exit[/green]     - Chat beenden\n"
        "[red]/[/red][green]delete[/green]   - Chatverlauf löschen\n"
        "[red]/[/red][green]reset[/green]    - Aurora.py zurücksetzen\n"
        "[red]/[/red][green]restart[/green]  - Aurora.py neu starten\n"
        "[red]/[/red][green]again[/green]    - Letzte Nachricht wiederholen\n"
        "[red]/[/red][green]config[/green]   - Einstellungen ändern\n"
        "[red]/[/red][green]slot[/green]     - Chat-Slot wechseln\n"
        "[red]/[/red][green]report[/green]   - Fehler melden auf GitHub\n"
        f"[red]/[/red][green]mood[/green]     - Stimmung von {char} ansehen\n"
    )
    event.app.current_buffer.insert_text('/')

session = PromptSession(key_bindings=kb)

buffer = ""
result = False
was_typed = False

#==================================================================================================

# Startet buffer, break_task und User-Eingabe
# Wird beendet, wenn der User eine Eingabe macht oder der Timer abgelaufen ist
# buffer kontrolliert, ob der User etwas eingibt und pausiert break_task (Versetzt ihn in endlos-Schleife)
async def get_user_input(wait):
    global buffer, result, was_typed

    console.print("[green]Input:[/green]")

    asyncio.create_task(get_buffer())
    break_task = asyncio.create_task(break_input(wait))
    prompt_task = asyncio.create_task(session.prompt_async(multiline=True))

    done, pending = await asyncio.wait(
        {break_task, prompt_task}, return_when=asyncio.FIRST_COMPLETED
    )
    if prompt_task in done:
        user_input = prompt_task.result()
        # Wenn der User einen Befehl eingibt
        if user_input.startswith("/"):
            pass 
        else:
            num_lines = 1 # Um 'Input:' zu zählen
            # Hole den bestätigten Eingabetext und lösche die Eingabezeile(n)
            num_lines += user_input.count("\n") + 1
            sys.stdout.write("\033[F\033[K")  # Lösche die aktuelle Zeile
            for i in range(num_lines):
                sys.stdout.write("\r\033[K")  # Lösche alle Zeilen nach \n
                if i < num_lines - 1:
                    sys.stdout.write("\033[F")  # Gehe eine Zeile nach oben
            sys.stdout.flush()
            highlighted_text = re.sub(
                r"\*\s*(.*?)\*",
                r"[orange1]\1[/orange1]",
                user_input,
                flags=re.DOTALL
                )
            # Zeige den Text in einem Rahmen an
            console.print(
                Panel(
                    highlighted_text,
                    title=f"[bold]{user}[/bold]",
                    width=120,
                    expand=True,
                    border_style="white"
                )
            ) 
    # Wenn Timer abgelaufen ist, und der User nichts eingibt
    if break_task in done and break_task.result() is True:
        assistant = break_task.result()
        
        if prompt_task in pending:
            # Wenn der User nichts eingibt, wird prefill_1 ausgegeben
            if was_typed == False:
                assistant = prefill_1
            # Wenn der User etwas getippt hat, aber wieder rückgängig gemacht hat, wird prefill_2 ausgegeben
            if was_typed == True:
                assistant = prefill_2
            # Beendet die Funktion
            prompt_task.cancel()
            break_task.cancel()
            # Setzt die Variablen zurück
            buffer = ""
            result = False
            was_typed = False
            # Gibt die Antwort aus: 'char hat sich entschieden zu antworten' 
            user_input = imp_response
            try:
                await prompt_task
            except asyncio.CancelledError:
                pass

    # Wenn der User etwas eingibt
    elif prompt_task in done and prompt_task.result() != "":
        # Speichert die Eingabe des Users
        user_input = prompt_task.result()
        if break_task in pending:
            # Assistant wird auf None gesetzt
            assistant = None
            # Beendet die Funktion
            break_task.cancel()
            prompt_task.cancel()
            # Setzt die Variablen zurück
            buffer = ""
            result = False
            was_typed = False
            try:
                await break_task
            except asyncio.CancelledError:
                pass

    return user_input, assistant


# Speichert den aktuellen Buffer in der Variable buffer
# in einer Schleife bis result True ist
async def get_buffer():
    global buffer, result

    await asyncio.sleep(0.1)

    while True:
        
        buffer = session.app.current_buffer.text
        lines = buffer.split('\n')
        new_buffer = []
        
        for line in lines:
            while len(line) > 100:
                last_space = line.rfind(' ', 0, 100)
                if last_space != -1:
                    new_buffer.append(line[:last_space+1])
                    line = line[last_space+1:]
                else:
                    new_buffer.append(line[:100])
                    line = line[100:]
            new_buffer.append(line)
        
        buffer = '\n'.join(new_buffer)
        
        session.app.current_buffer.text = buffer
        session.app.current_buffer.cursor_position = len(buffer)

        await asyncio.sleep(0.1)
        if result == True:
            break

# Wartet eine bestimmte Zeit bis der User eine Eingabe macht
# Wenn der User nichts eingibt, wird result True
# Wenn der User etwas eingibt, wird funktion beendet
async def break_input(wait):
    global buffer, result, was_typed

    elapsed_time = 0

    if wait == "neutral":
        # Wartezeit zwischen 1,5 und 3 Minuten
        wait_time = random.randint(90, 180)
    if wait == "off":
        # Wenn "off" wird Wait-Time auf Eine Woche gesetzt
        wait_time = 604800

    while True:
        await asyncio.sleep(0.1)
        elapsed_time += 0.1
        if buffer != "":
            was_typed = True
        if buffer == "" and elapsed_time >= wait_time:
            console.print(imp_response_color)
            result = True
            break
        continue
        
    return result



    
