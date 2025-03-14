import anthropic
import re

from globals import FILE, console

from score_trigger import mood_trigger
from tiktoken_function import count_tokens, output_tokens
from sense_of_time import diff_time_trigger
from memory_processing import control_existing_memory
from task_organizer import truncate_history_for_api, animated_typing_panel
from data_handler import load_set, read_json, get_user_name
from prompt_processing import PromptBuilder


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

def init_prompt_builder(
        time_sense:bool=False,
        get_system:bool=False,
        get_sub_system:bool=False,
        get_prefill:bool=False,
        get_history:dict=None
    ):
        
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
        
    def build_api_prompt(
            init_prompt:PromptBuilder,
            time_sense:bool,
            get_system:bool,
            get_sub_system:bool,
            get_prefill:bool,
            get_history:dict
        ) -> list:

        if get_system:
            return init_prompt.get_system_api()
        
        elif get_sub_system:
            init_prompt.mood = mood_trigger()
            init_prompt.time_sense = get_time_sense(time_sense)
            init_prompt.memory_prompt = get_memory()
            return init_prompt.get_sub_system_api()
        
        elif get_prefill:
            return init_prompt.get_reminder_api()
        
        elif get_history:
            init_prompt.history = get_history
            return init_prompt.get_history_api()
        

    return build_api_prompt(
        init_prompt,
        time_sense,
        get_system,
        get_sub_system,
        get_prefill,
        get_history
        )

def prepare_api_request(
    CLIENT: anthropic.Anthropic,
    model_name: str,
    full_history: list,
    assistant_imp: list = None,
    max_tokens: int = 4096,
    time_sense: bool = False,
    ) -> str:

    global final_client, final_model_name, final_system_prompt, final_messages

    """
    Sendet die Anfrage an das ausgewählte Anthropic-Modell
    und streamt die Antwort chunkweise zurück.
    """

    # init-assistant-prompt
    assistant_prompt = []

    # API-Prompt-Generierung (System, Prefill)
    system_prompt = init_prompt_builder(time_sense, get_system=True)
    sub_system_prompt = init_prompt_builder(time_sense, get_sub_system=True)
    prefill_prompt = init_prompt_builder(time_sense, get_prefill=True)

    # Add sub_system_prompt
    system_prompt.extend(sub_system_prompt)

    # Add prefill_prompt
    assistant_prompt.extend(prefill_prompt)

    # Add Impatiece
    if assistant_imp:
        assistant_prompt.extend(assistant_imp)

    # Truncate 'full_history' to fit the API's max token limit
    truncate_history = truncate_history_for_api(
        full_history, system_prompt, assistant_prompt, max_tokens
        )

    # API-Prompt-Generierung (History)
    history_prompt = init_prompt_builder(
        time_sense, get_history=truncate_history
        )

    # Add history_prompt at the beginning
    for i, msg in enumerate(history_prompt):
        assistant_prompt.insert(i, msg)
 
    final_client = CLIENT
    final_model_name = model_name
    final_system_prompt = system_prompt[:]
    final_messages = assistant_prompt[:]

    #NOTE: This is for debugging purposes ========================
    debug = False
    
    if debug:
        import json
        my_json = {
            "system_prompt": final_system_prompt,
            "assistant_prompt": final_messages
        }
        json_str = json.dumps(my_json, ensure_ascii=False, indent=4)
        print(json_str.encode().decode('unicode_escape'))

    #NOTE: End of debugging ======================================
    
    return count_tokens(system_prompt=system_prompt, assistant_prompt=assistant_prompt)

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
        """
        Extracts content from inner_reflection and response tags in a text.
        
        Args:
            response_text (str): The text containing the tagged sections
            
        Returns:
            tuple: (character_analysis, response) as extracted from the tags
        """
        def extract_sections(text, section_one, section_two):
            
            pattern_one = fr"<{section_one}>(.*?)</{section_one}>"
            pattern_two = fr"<{section_two}>(.*?)</{section_two}>"
            
            # Check if closing tag for section_two exists
            if f"</{section_two}>" not in text:
                pattern_two = fr"<{section_two}>(.*)"

            match_one = re.search(pattern_one, text, re.DOTALL)
            match_two = re.search(pattern_two, text, re.DOTALL)

            text_one = match_one.group(1).strip() if match_one else ""
            text_two = match_two.group(1).strip() if match_two else ""

            return text_one, text_two
        (
        inner_reflection,
        response
        ) = extract_sections(
            response_text, "inner_reflection", "response"
            )
        return inner_reflection, response
    

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
