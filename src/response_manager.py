import anthropic

from score_trigger import mood_trigger

from tiktoken_function import count_tokens, output_tokens

from sense_of_time import diff_time_trigger

from memory_processing import control_existing_memory

# Task-Organizer-Import:
from task_organizer import truncate_history_for_api, animated_typing_panel

from globals import FILE, console
from data_handler import load_set, read_json, get_user_name

from prompt_processing import PromptBuilder


# Globale Variablen für um assistent_prompt dynamisch zu verändern
temp_assistant_prompt = []

# Globale Variable für den Denkprozess
load = True

# Globale Variablen für die Anfrage
final_client = None
final_model_name = ""
final_system_prompt = []
fina_messages = []


def get_time_sense(trigger: bool) -> str:
        if trigger:
            return diff_time_trigger()
        
def get_memory():
        if control_existing_memory():
            from inject_memory import memory_prompt_forming
            return memory_prompt_forming()
        return None

def build_api_prompt(time_sense:bool=False) -> list:

    char = load_set(char=True)
    user = get_user_name()

    language = read_json(FILE["user_language"])["language"]
    gender = read_json(FILE["user_gender"])["user_gender"]

    init_prompt = PromptBuilder(
        char_name=char,
        user_name=user,
        language=language,
        gender=gender
    )

    system_prompt = init_prompt.get_system_api()

    init_prompt.mood = mood_trigger()
    init_prompt.time_sense = get_time_sense(time_sense)
    init_prompt.memory_prompt = get_memory()

    return system_prompt, init_prompt.get_reminder_api()

#NOTE: misleading function name
def stream_chat_response(
    client: anthropic.Anthropic,
    model_name: str,
    full_history: list,
    assistant_imp: list = None,
    max_tokens: int = 4096,
    time_sense: bool = False,
) -> str:
    global temp_assistant_prompt, final_client, final_model_name, final_system_prompt, final_messages

    """
    Sendet die Anfrage an das ausgewählte Anthropic-Modell
    und streamt die Antwort chunkweise zurück.
    """

    # API-Prompt-Generierung
    system_prompt, temp_assistant_prompt = build_api_prompt(time_sense)


    if assistant_imp:
        temp_assistant_prompt.append(assistant_imp)

    # Tokenberechnung
    truncate_history = truncate_history_for_api(full_history, system_prompt, temp_assistant_prompt, max_tokens)
    current_tokens = count_tokens(system_prompt, truncate_history, temp_assistant_prompt)

    api_dialogue_start = [{"role": "assistant", "content": "<history>"}]
    api_dialogue_end = [{"role": "assistant", "content": "</history>"}]

    api_messages = [
        {"role": msg["role"], "content": msg["content"]}
        for msg in truncate_history if "role" in msg and "content" in msg
    ]

    api_messages = api_dialogue_start + api_messages + api_dialogue_end

    temp_messages = api_messages + temp_assistant_prompt
 
    final_client = client
    final_model_name = model_name
    final_system_prompt = system_prompt[:]
    final_messages = temp_messages[:]

    
    return current_tokens

def think():
    import time
    global load

    animation = [
        "▰▱▱▱▱▱▱▱▱▱",
        "▰▰▱▱▱▱▱▱▱▱",
        "▰▰▰▱▱▱▱▱▱▱",
        "▰▰▰▰▱▱▱▱▱▱",
        "▰▰▰▰▰▱▱▱▱▱",
        "▰▰▰▰▰▰▱▱▱▱",
        "▰▰▰▰▰▰▰▱▱▱",
        "▰▰▰▰▰▰▰▰▱▱",
        "▰▰▰▰▰▰▰▰▰▱",
        "▰▰▰▰▰▰▰▰▰▰",
    ]

    padding = (120 - 10) // 2
    while load:
        for i in animation:
            console.print(f"\r[bold color(45)]{' ' * padding}{i}[/bold color(45)]", end="\r")
            time.sleep(0.2)
            if load == False:
                break

def print_ki_response(char: str = None, highlighted: str = "purple"):
    import threading
    import time
    
    global final_client, final_model_name, final_system_prompt, final_messages, load

    # Highlighted-Text
    color = highlighted
    
    response_text = ""

    api_request = True
    while_round = 0

    

    def split_response(response_text):
            def extract_sections(text, section_one, section_two):
                import re
                pattern_one = fr"<{section_one}>(.*?)</{section_one}>"
                pattern_two = fr"<{section_two}>(.*?)</{section_two}>"
                
                # if </{section_two}> is not found, the text attempt to match  without the closing tag
                if not re.search(pattern_two, text, re.DOTALL):
                    pattern_two = fr"<{section_two}>(.*)"

                match_one = re.search(pattern_one, text, re.DOTALL)
                match_two = re.search(pattern_two, text, re.DOTALL)
                text_one = match_one.group(1).strip() if match_one else ""
                text_two = match_two.group(1).strip() if match_two else ""
                return text_one, text_two
            (
            character_analysis,
            response
            ) = extract_sections(
                response_text, "inner_reflection", "response"
                )
            return character_analysis, response
    

    while api_request:
                
        threading.Thread(target=think, daemon=True).start()

        try:
            with final_client.messages.stream(
                model=final_model_name,
                max_tokens=512,
                temperature=0.9,
                system=final_system_prompt,
                messages=final_messages
            ) as stream:
                chunks = list(stream.text_stream)

                # Alle Chunks zusammenfügen:
                response_text = "".join(chunks)

        except Exception as e:
            console.print(f"[red]Unexpected error: {e}[/red]")
            break


        inner_reflection, response = split_response(response_text)

        if response == "":
            while_round += 1
            if while_round == 3:
                console.print("[red]Keine Antwort erhalten.[/red]")
                break
            time.sleep(1*(while_round+1))
            continue
        else:
            load = False
            time.sleep(0.25)
            load = True
            

        animated_typing_panel(char, response, color=color)
        

        print()  # Zusätzlicher Zeilenumbruch nach vollständiger Antwort

        response_token = output_tokens(response_text)


        return  response_token, inner_reflection, response
