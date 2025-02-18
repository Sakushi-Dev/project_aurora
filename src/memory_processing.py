
import re
import json
from datetime import datetime
from collections import Counter
from data_handler import load_prompts, load_format_history, load_set, read_json, user_name_path

prompt = load_prompts(memory=True)
prompt = prompt['memory_prompt']

def read_jsonl(file_path):
    '''
    Reads a jsonl file and returns the data as a list
    '''
    data = []

    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            data.append(json.loads(line.strip()))
    return data

def control_existing_memory(debug:bool = True):
    '''
    Checks if the memory file exists
    '''
    import os

    file_path = "data/memory/memory_analysis.jsonl"

    try:
        if os.path.exists(file_path):
            return True
        
    except FileNotFoundError:
        if debug:
            print(f"Error: Datei {file_path} existiert nicht.")
        return False

def merge_history_in_prompt(prompt):
    global user_name_path
    '''
    Merges the history into the prompt
    Characters and user names loding in the function
    '''

    char = load_set(char=True)
    user = read_json(user_name_path)
    user = user['user_name']

    dialog = load_format_history()
    
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
        data = read_jsonl("data/memory/memory_analysis.jsonl")
        timestamp = find_oldest_temporary(data)
        tuple_value = number_of_categorys(data)
        sc_value, dh_value, dl_value, temp_value = tuple_value

        sc_list = []
        temp_list = []
        
        for entry in data:
            category = entry['category']

            if category == 'Dynamic High' or category == 'Dynamic Low':
                quiry += f"{entry[c_map[0]]}//{entry[c_map[1]]}//{entry[c_map[2]]}//{entry[c_map[3]]}"
                quiry += "\n"
            elif category == 'Temporary' and entry['timestamp'] == timestamp and temp_value == 20:
                quiry += f"{entry[c_map[0]]}//{entry[c_map[1]]}//{entry[c_map[2]]}//{entry[c_map[3]]}//{entry[c_map[4]]}"
                quiry += "\n"
            elif category == 'Temporary' and entry['timestamp'] != timestamp and temp_value == 20:
                temp_list.append(f"{entry[c_map[0]]}//{entry[c_map[1]]}//{entry[c_map[2]]}//{entry[c_map[3]]}//{entry[c_map[4]]}")
            elif category == 'Temporary' and temp_value < 20:
                temp_list.append(f"{entry[c_map[0]]}//{entry[c_map[1]]}//{entry[c_map[2]]}//{entry[c_map[3]]}//{entry[c_map[4]]}")
            elif category == 'System Core':
                sc_list.append(f"{entry[c_map[0]]}//{entry[c_map[1]]}//{entry[c_map[2]]}//{entry[c_map[3]]}")

            

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

    client = init_anthropic_client(API_KEY)

    response = client.messages.create(
        model="claude-3-5-haiku-20241022",
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

    with open("data/memory/memory_analysis.jsonl", "w", encoding="utf-8") as file:
        for entry in data:
            file.write(json.dumps(entry) + "\n")


# =================================================================================================
# Main Function
# =================================================================================================

def init_prompts(prompt:str):
    '''
    Initializes the prompts
    '''

    s_prompt = merge_history_in_prompt(prompt)
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


def execute_request(debug:bool = True):
    global prompt
    '''
    Executes the request for the memory analysis and saves the result
    '''
    if debug:
        print("Requesting Memory Analysis...", f"\n{'='*30}\n")
        print(prompt, f"\n{'='*30}\n")

    system, messages, sc_list, temp_list = init_prompts(prompt)
    if debug:
        print(system, f"\n{'='*30}\n")
        print(messages, f"\n{'='*30}\n")

    response_list = request_memory_analysis(system, messages)
    if debug:
        print(response_list, f"\n{'='*30}\n")

    memory_list = add_time_for_temporary(response_list)
    if debug:
        print(memory_list, f"\n{'='*30}\n")

    if sc_list:
        memory_list.extend(sc_list)
        if debug:
            print(sc_list, f"\n{'='*30}\n")
    if temp_list:
        memory_list.extend(temp_list)
        if debug:
            print(temp_list, f"\n{'='*30}\n")

    save_memory_analysis_as_jsonl(memory_list)

#test
execute_request()




    



