import os
import re
import json
from rich.console import Console
from datetime import datetime
from collections import Counter
from data_handler import load_prompts, load_format_history, load_set, read_json, user_name_path, read_jsonl, get_slot

console = Console()
prompt = load_prompts(memory=True)
prompt = prompt['memory_prompt']
PATH = "data/memory/memory_analysis_slot_"
data_format = ".jsonl"

def control_existing_memory(debug:bool = True):

    global PATH, data_format
    '''
    Checks if the memory file exists
    '''
    import os
    slot = get_slot()

    file_path = PATH + str(slot-1) + data_format

    try:
        if os.path.exists(file_path):
            return True
        
    except FileNotFoundError:
        if debug:
            print(f"Error: Datei {file_path} existiert nicht.")
        return False

def merge_history_in_prompt(prompt, m_interval:int=50) -> str:
    global user_name_path
    '''
    Merges the history into the prompt
    Characters and user names loding in the function
    '''

    char = load_set(char=True)
    user = read_json(user_name_path)
    user = user['user_name']

    dialog = load_format_history(value=m_interval)
    
    # Replace the placeholders in the prompt with the actual values
    prompt = prompt.replace('{{user}}', user)
    prompt = prompt.replace('{{char}}', char)
    prompt = prompt.replace('{{dialogue}}', dialog)

    return prompt

def format_api_prompts(s_prompt: str, p_prompt: str, q_prompt: str)->list:
    '''
    Formats the prompts for the API request
    '''
    
    system_prompt = [{"type": "text", "text": s_prompt}]
    api_messages = [{"role": "assistant", "content": p_prompt}]
    api_messages.append({"role": "user", "content": q_prompt})

    return system_prompt, api_messages


def find_oldest_temporary(data):
    '''
    Finds the oldest temporary memory entry
    '''
    
    oldest_timestamp = None

    for obj in data:
        if obj.get('category') == 'Temporary' and 'timestamp' in obj:
            datum = datetime.strptime(obj["timestamp"], "%Y-%m-%d %H:%M:%S")

            if oldest_timestamp is None or datum < oldest_temporary:
                oldest_temporary = datum
                oldest_timestamp = obj["timestamp"]

    return oldest_timestamp

def number_of_categorys(data) -> tuple:
    '''
    Counts the number of entries in each category
    '''
    counts = Counter(entry.get("category") for entry in data)
    return (
        counts.get("System Core", 0),
        counts.get("Dynamic High", 0),
        counts.get("Dynamic Low", 0),
        counts.get("Temporary", 0)
    )

def create_quiry(first:bool = False, subsequent:bool = False) -> str:

    global PATH, data_format

    '''
    Creates a quiry for the memory analysis

    Parameters:
    first: bool = False
    subsequent: bool = False

    Returns:
    quiry: str
    '''
    
    system_core = "System Core//???//???//???\n"
    dynamic_high = "Dynamic High//???//???//???\n"
    dynamic_low = "Dynamic Low//???//???//???\n"
    temporary = "Temporary//???//???//???\n"

    c_map = [
            "category",
            "title",
            "description",
            "dialogue",
            "timestamp"
        ]

    quiry = ""

    if first:
        quiry = (
            system_core +
            dynamic_high*2 +
            dynamic_low*2 +
            temporary*5
        )
    elif subsequent:
        slot = get_slot()
        
        path = PATH + str(slot-1) + data_format

        data = read_jsonl(path)
        timestamp = find_oldest_temporary(data)
        tuple_value = number_of_categorys(data)
        sc_value, dh_value, dl_value, temp_value = tuple_value

        sc_list = []
        temp_list = []
        
        for entry in data:
            # Get the category for the current entry
            category = entry['category']
            
            if category in ('Dynamic High', 'Dynamic Low'):
                # For Dynamic High and Dynamic Low entries,
                # join the first four fields (Category, Title, Description, Dialogue) with "//"
                line = "//".join(entry[c] for c in c_map[:4])
                # Append the formatted string to the query
                quiry += f"{line}\n"
                
            elif category == 'Temporary':
                # For Temporary entries, include all five fields (with timestamp)
                line = "//".join(entry[c] for c in c_map)
                if temp_value >= 20:
                    # If the temporary count is high, check the timestamp to decide where to add the line
                    if entry['timestamp'] == timestamp:
                        # If the timestamp matches, add directly to the query
                        quiry += f"{line}\n"
                    else:
                        # Otherwise, store the line to temp_list for later use
                        temp_list.append(line)
                else:
                    # If there are fewer than 20 temporary entries, directly store the line
                    temp_list.append(line)
                    
            elif category == 'System Core':
                # For System Core entries, join the first four fields (omit timestamp)
                line = "//".join(entry[c] for c in c_map[:4])
                # Add the formatted line to sc_list for later processing
                sc_list.append(line)

            

        if sc_value < 5:
            quiry += system_core
        if dh_value < 10:
            quiry += dynamic_high*2
        if dl_value < 10:
            quiry += dynamic_low*2
        if temp_value < 20:
            quiry += temporary*5

        return quiry, sc_list, temp_list

    return quiry
    

        
def set_prefill():

    prefill = (
        "Remember to maintain the exact structure and"
        "categorization in your response, ensuring that"
        "each memory entry adheres to the"
        "Category//Title//Description//Dialogue format."
        "Ignore the timestamp field."
    )

    return prefill



def request_memory_analysis(system_prompt, messages):

    from anthropic_api import init_anthropic_client, API_KEY
    from tiktoken_function import count_tokens, output_tokens
    from cost_manager import calculate_cost, save_costs

    client = init_anthropic_client(API_KEY)

    model_name = "claude-3-5-haiku-20241022"

    response = client.messages.create(
        model=model_name,
        max_tokens=4000,
        temperature=0.7,
        system=system_prompt,
        messages=messages,
    )

    ki_response = response.content[0].text

    match = re.search(r"<memory_analysis>(.*?)</memory_analysis>", ki_response, re.DOTALL)

    if match:
        memory_analysis = match.group(1)
        memory_analysis_list = memory_analysis.split('\n')

        memory_analysis_list = [entry for entry in memory_analysis_list if entry.strip()]

    input_token = count_tokens(system_prompt, messages)
    output_token = output_tokens(ki_response)

    total_input_cost, total_output_cost = calculate_cost(model_name, input_token, output_token)

    save_costs(total_input_cost, total_output_cost)

    return memory_analysis_list

def add_time_for_temporary(memory_analysis_list):


    for i, entry in enumerate(memory_analysis_list):
        if entry.startswith('Temporary'):
            parts = entry.split("//")  # Zerlege den Eintrag anhand "//"

            # Falls der Eintrag bereits 5 Teile hat, ist ein Datum vorhanden → ignoriere
            if len(parts) > 4:
                continue  

            # Falls kein Datum existiert, füge es hinzu
            entry = entry + f"//{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
            memory_analysis_list[i] = entry

    return memory_analysis_list

def save_memory_analysis_as_jsonl(memory_analysis_list):

    data = []

    memory_list = add_time_for_temporary(memory_analysis_list)

    slot = get_slot()

    for entry in memory_list:
        if entry.startswith('Temporary'): 
            entry = entry.split('//')
            data.append({
                "category": entry[0],
                "title": entry[1],
                "description": entry[2],
                "dialogue": entry[3],
                "timestamp": entry[4],
            })
        else:
            entry = entry.split('//')
            data.append({
                "category": entry[0],
                "title": entry[1],
                "description": entry[2],
                "dialogue": entry[3]
            })

    category_order = {"System Core": 0, "Dynamic High": 1, "Dynamic Low": 2, "Temporary": 3}

    data = sorted(data, key=lambda x: category_order.get(x["category"], 4))

    if not os.path.exists(f"data/memory"):
        os.makedirs(f"data/memory")
    with open(f"data/memory/memory_analysis_slot_{slot-1}.jsonl", "w", encoding="utf-8") as file:
        for entry in data:
            file.write(json.dumps(entry) + "\n")


# =================================================================================================
# Main Function
# =================================================================================================

def init_prompts(prompt:str, m_interval:int=50):
    '''
    Initializes the prompts
    '''

    s_prompt = merge_history_in_prompt(prompt, m_interval)
    p_prompt = set_prefill()

    file_existing = control_existing_memory()

    sc_list = None
    temp_list = None

    if file_existing:
        q_prompt, sc_list, temp_list = create_quiry(subsequent=True)
    else:
        q_prompt = create_quiry(first=True)
    
    system_prompt, api_messages = format_api_prompts(s_prompt, p_prompt, q_prompt)

    return system_prompt, api_messages, sc_list, temp_list


def execute_memory_request(debug: bool = True, m_interval:int=50):
    global prompt, PATH, data_format
    '''
    Executes the request for the memory analysis and saves the result
    with a more organized debug output.
    '''
    # NOTE: m_interval route: load_format_history (data_handler.py) -> merge_history_in_prompt -> init_prompts

    slot = get_slot()

    path = PATH + str(slot-1) + data_format

    def debug_print(step: str, data=None):

        if debug:
            console.print(f"\n[green]--- {step} ---[/green]\n")
            if data is not None:
                #if data is a list, print each item in a new line
                if isinstance(data, list):
                    for item in data:
                        console.print(item)
                else:
                    console.print(data)

    debug_print("Step 1: Starting memory analysis request (Prompt)", prompt)

    system, messages, sc_list, temp_list = init_prompts(prompt, m_interval)
    debug_print("Step 2: Prompts initialized - System Prompt", system)
    debug_print("Step 2: Prompts initialized - Messages", messages)

    response_list = request_memory_analysis(system, messages)
    debug_print("Step 3: Response list received", response_list)

    memory_list = add_time_for_temporary(response_list)
    debug_print("Step 4: Memory list with timestamps", memory_list)

    if sc_list:
        memory_list.extend(sc_list)
        debug_print("Step 5: Extended with System Core List", sc_list)
    if temp_list:
        memory_list.extend(temp_list)
        debug_print("Step 6: Extended with Temporary List", temp_list)

    save_memory_analysis_as_jsonl(memory_list)
    debug_print("Step 7: Memory analysis saved", memory_list)

    if debug:
        data_lies = read_jsonl(path)
        if len(data_lies) > 45:
            debug_print("Step 8: Control if the memory overloaded", "[red]Memory is overloaded[/red]")
        else:
            debug_print("Step 8: Control if the memory overloaded", "[green]Memory is not overloaded[/green]")
    else:
        data_lies = read_jsonl(path)
        if len(data_lies) > 45:
            console.print("[red]!Memory is overloaded!\nPlease contact the developer[/red]\n[orange1]Your character is storing more than he/she should[/orange1]")


#test
#execute_memory_request(debug=True)


# NOTE: Function must save in slots to access the correct file
#       Function must be called in chat_loop.py
#       Trigger must be set in chat_loop.py (e.g., after 20 messages)
#       Read and integrate as prompt in response_processing.py
#       Design prompt so that AI correctly interprets memory

    



